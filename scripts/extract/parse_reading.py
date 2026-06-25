"""
Parse extracted/READING/ETS 2026 READING.md → question_bank/part5.json, part6.json, part7.json, passages.json

Run AFTER: python scripts/extract/run_marker.py reading
Run BEFORE: python scripts/extract/inject_answers.py
"""

import re
import json
from pathlib import Path

ROOT        = Path(__file__).parent.parent.parent
MD_FILE     = ROOT / "extracted" / "READING" / "ETS 2026 READING.md"
BANK_DIR    = ROOT / "question_bank"
BANK_DIR.mkdir(parents=True, exist_ok=True)

# ── Regexes ──────────────────────────────────────────────────────────────────
# Marker may wrap bold text: **101.** or plain 101.
RE_QNUM      = re.compile(r"^\*{0,2}(\d{3})\.\*{0,2}\s*(.*)")
RE_OPTION    = re.compile(r"^\({0,1}\*{0,2}([ABCD])\*{0,2}\){0,1}[.)]\s+(.+)")
RE_BLANK     = re.compile(r"[-_]{4,}")
RE_TEST_HDR  = re.compile(r"(?:^|\n)(?:#+ )?(?:READING TEST|TEST\s+(\d+))", re.IGNORECASE)
RE_PART_HDR  = re.compile(r"(?:^|\n)(?:#+ )?PART\s+([567])", re.IGNORECASE)
RE_P67_RANGE = re.compile(r"Questions?\s+(\d+)[\s\-–]+(\d+)\s+refer", re.IGNORECASE)

NOISE = re.compile(
    r"(reading test|answer sheet|mark the letter|mark your answer"
    r"|directions:|select the best|four answer choices|word or phrase"
    r"|time allowed|comprehension questions|go on to the next page"
    r"|you will read|in the reading test|part 5|part 6|part 7)",
    re.IGNORECASE,
)

PART5_Q = range(101, 131)  # 101-130
PART6_Q = range(131, 147)  # 131-146
PART7_Q = range(147, 201)  # 147-200


def make_id(part: int, test: int, question: int) -> str:
    return f"p{part}-t{test:02d}-q{question:03d}"


def normalize_blank(text: str) -> str:
    return RE_BLANK.sub("_______", text)


def is_noise(line: str) -> bool:
    return bool(NOISE.search(line)) or len(line.strip()) < 3


# ── Part 5 parser ─────────────────────────────────────────────────────────────

def parse_part5(lines: list[str], test_num: int) -> list[dict]:
    """2-pass parser: handles Marker output where q-number may be on its own line."""
    tagged = []
    for line in lines:
        line = line.strip()
        if not line or is_noise(line):
            continue
        m_q = RE_QNUM.match(line)
        m_o = RE_OPTION.match(line)
        if m_q:
            qnum = int(m_q.group(1))
            rest = m_q.group(2).strip()
            tagged.append(("Q", qnum, rest))
        elif m_o:
            tagged.append(("O", m_o.group(1), m_o.group(2).strip()))
        else:
            tagged.append(("T", None, line))

    questions = []
    cur = None
    pending = []

    def save():
        if cur and int(cur["question"]) in PART5_Q:
            questions.append(cur)

    for tag, val1, val2 in tagged:
        if tag == "Q":
            qnum = val1
            save()
            stem_prefix = normalize_blank(" ".join(pending) + " " + val2).strip()
            cur = {"question": qnum, "stem": stem_prefix, "options": {}}
            pending = []
        elif tag == "O":
            if cur:
                cur["options"][val1] = val2
            pending = []
        elif tag == "T":
            if cur and not cur["options"]:
                cur["stem"] = normalize_blank(cur["stem"] + " " + val2).strip()
            else:
                pending.append(val2)

    save()

    result = []
    for q in questions:
        if int(q["question"]) not in PART5_Q:
            continue
        result.append({
            "id":         make_id(5, test_num, q["question"]),
            "part":       5,
            "test":       test_num,
            "question":   q["question"],
            "stem":       q["stem"],
            "options":    q["options"],
            "answer":     None,
            "difficulty": None,
            "tags":       [],
        })
    return result


# ── Part 6 parser ─────────────────────────────────────────────────────────────

def parse_part6(lines: list[str], test_num: int) -> tuple[list[dict], list[dict]]:
    """Returns (questions, passages). Passage text stored only on first Q of group."""
    passages = []
    questions = []
    passage_lines = []
    cur_range = None
    cur_q = None
    in_qs = False

    def flush_passage():
        if cur_range and passage_lines:
            passages.append({
                "id":            f"p6-t{test_num:02d}-p{len(passages)+1:02d}",
                "part":          6,
                "test":          test_num,
                "passage_num":   len(passages) + 1,
                "passage_type":  "text_completion",
                "question_range": cur_range,
                "text":          " ".join(passage_lines).strip(),
                "images":        [],
            })

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        m_range = RE_P67_RANGE.match(raw)
        if m_range:
            flush_passage()
            cur_range = [int(m_range.group(1)), int(m_range.group(2))]
            passage_lines = []
            in_qs = False
            continue

        m_q = RE_QNUM.match(raw)
        if m_q:
            qnum = int(m_q.group(1))
            if qnum in PART6_Q:
                in_qs = True
                if cur_q:
                    questions.append(cur_q)
                cur_q = {"question": qnum, "options": {}, "passage_ref": len(passages)}
                continue

        m_o = RE_OPTION.match(raw)
        if m_o and cur_q is not None and int(cur_q["question"]) in PART6_Q:
            cur_q["options"][m_o.group(1)] = m_o.group(2).strip()
            continue

        if not in_qs and not is_noise(raw):
            passage_lines.append(raw)

    if cur_q:
        questions.append(cur_q)
    flush_passage()

    result = []
    passage_first_q = {}  # passage_ref → first qnum seen
    for q in questions:
        if int(q["question"]) not in PART6_Q:
            continue
        pref = q.get("passage_ref", 0)
        is_first = pref not in passage_first_q
        if is_first:
            passage_first_q[pref] = q["question"]
            passage_text = passages[pref]["text"] if pref < len(passages) else ""
        else:
            passage_text = ""

        result.append({
            "id":         make_id(6, test_num, q["question"]),
            "part":       6,
            "test":       test_num,
            "question":   q["question"],
            "passage_id": passages[pref]["id"] if pref < len(passages) else None,
            "passage":    passage_text,
            "stem":       None,
            "options":    q["options"],
            "answer":     None,
            "difficulty": None,
            "tags":       [],
        })
    return result, passages


# ── Part 7 parser ─────────────────────────────────────────────────────────────

def passage_type(header_line: str) -> str:
    hl = header_line.lower()
    ands = hl.count(" and ")
    if ands >= 2:
        return "triple"
    if ands == 1 or "double" in hl:
        return "double"
    return "single"


def parse_part7(lines: list[str], test_num: int) -> tuple[list[dict], list[dict]]:
    passages = []
    questions = []
    passage_lines = []
    cur_range = None
    cur_ptype = "single"
    cur_q = None
    in_qs = False

    def flush_passage():
        nonlocal passage_lines, cur_range, cur_ptype
        if cur_range and passage_lines:
            passages.append({
                "id":            f"p7-t{test_num:02d}-p{len(passages)+1:02d}",
                "part":          7,
                "test":          test_num,
                "passage_num":   len(passages) + 1,
                "passage_type":  cur_ptype,
                "question_range": cur_range,
                "text":          " ".join(passage_lines).strip(),
                "images":        [],
            })
        passage_lines = []
        cur_range = None

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        m_range = RE_P67_RANGE.match(raw)
        if m_range:
            if not in_qs:
                flush_passage()
            cur_range = [int(m_range.group(1)), int(m_range.group(2))]
            cur_ptype = passage_type(raw)
            in_qs = False
            continue

        m_q = RE_QNUM.match(raw)
        if m_q:
            qnum = int(m_q.group(1))
            if qnum in PART7_Q:
                if not in_qs:
                    flush_passage()
                in_qs = True
                if cur_q:
                    questions.append(cur_q)
                cur_q = {
                    "question": qnum,
                    "stem":     normalize_blank(m_q.group(2).strip()),
                    "options":  {},
                    "passage_ref": len(passages),
                }
                continue

        m_o = RE_OPTION.match(raw)
        if m_o and cur_q is not None:
            cur_q["options"][m_o.group(1)] = m_o.group(2).strip()
            continue

        if cur_q and not cur_q["options"]:
            cur_q["stem"] = (cur_q["stem"] + " " + raw).strip()
        elif not in_qs and not is_noise(raw):
            passage_lines.append(raw)

    if cur_q:
        questions.append(cur_q)
    flush_passage()

    result = []
    passage_first_q = {}
    for q in questions:
        if int(q["question"]) not in PART7_Q:
            continue
        pref = q.get("passage_ref", 0)
        is_first = pref not in passage_first_q
        if is_first:
            passage_first_q[pref] = q["question"]
            passage_text = passages[pref]["text"] if pref < len(passages) else ""
        else:
            passage_text = ""

        result.append({
            "id":            make_id(7, test_num, q["question"]),
            "part":          7,
            "test":          test_num,
            "question":      q["question"],
            "passage_id":    passages[pref]["id"] if pref < len(passages) else None,
            "passage_type":  passages[pref]["passage_type"] if pref < len(passages) else "single",
            "passage":       passage_text,
            "passage_range": passages[pref]["question_range"] if pref < len(passages) else None,
            "stem":          q["stem"],
            "options":       q["options"],
            "answer":        None,
            "difficulty":    None,
            "tags":          [],
        })
    return result, passages


# ── Main ──────────────────────────────────────────────────────────────────────

def split_by_test(md_text: str) -> list[str]:
    """
    Split the full markdown into 10 per-test sections.
    ETS book has "TEST N" or repeated "READING TEST" headers.
    Returns list of 10 strings, index 0 = Test 1.
    """
    # Try split on "# READING TEST" or numbered test markers
    parts = re.split(r"\n(?=(?:#{1,3}\s+)?(?:TEST\s+\d+|READING TEST))", md_text, flags=re.IGNORECASE)
    if len(parts) >= 10:
        return parts[-10:]  # last 10 chunks are the 10 tests

    # Fallback: split evenly by character count
    total = len(md_text)
    chunk = total // 10
    return [md_text[i * chunk:(i + 1) * chunk] for i in range(10)]


def extract_part_section(test_text: str, part_num: int) -> list[str]:
    """Extract lines belonging to Part N within a test's text block."""
    lines = test_text.splitlines()
    result = []
    in_part = False
    for line in lines:
        m = RE_PART_HDR.match(line)
        if m:
            found_part = int(m.group(1))
            in_part = (found_part == part_num)
            continue
        if in_part:
            result.append(line)
    return result if result else lines  # fallback: return all lines if detection fails


def main():
    if not MD_FILE.exists():
        print(f"[ERROR] Not found: {MD_FILE}")
        print("Run first: python scripts/extract/run_marker.py reading")
        return

    print(f"Loading {MD_FILE} ...")
    md_text = MD_FILE.read_text(encoding="utf-8")

    all_p5, all_p6, all_p7, all_passages = [], [], [], []

    test_sections = split_by_test(md_text)
    print(f"Detected {len(test_sections)} test sections.")

    for i, test_text in enumerate(test_sections[:10]):
        test_num = i + 1
        print(f"\n-- Test {test_num} --")

        p5_lines = extract_part_section(test_text, 5)
        p5 = parse_part5(p5_lines, test_num)
        print(f"  Part 5: {len(p5)}/30 questions")
        all_p5.extend(p5)

        p6_lines = extract_part_section(test_text, 6)
        p6, passages6 = parse_part6(p6_lines, test_num)
        print(f"  Part 6: {len(p6)}/16 questions, {len(passages6)} passages")
        all_p6.extend(p6)
        all_passages.extend(passages6)

        p7_lines = extract_part_section(test_text, 7)
        p7, passages7 = parse_part7(p7_lines, test_num)
        print(f"  Part 7: {len(p7)}/54 questions, {len(passages7)} passages")
        all_p7.extend(p7)
        all_passages.extend(passages7)

    def write_json(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[saved] {path} ({len(data)} records)")

    write_json(BANK_DIR / "part5.json", all_p5)
    write_json(BANK_DIR / "part6.json", all_p6)
    write_json(BANK_DIR / "part7.json", all_p7)
    write_json(BANK_DIR / "passages.json", all_passages)

    print(f"\nTotal: {len(all_p5)} Part 5 + {len(all_p6)} Part 6 + {len(all_p7)} Part 7 = {len(all_p5)+len(all_p6)+len(all_p7)} questions")
    print("Run next: python scripts/extract/parse_transcript.py")


if __name__ == "__main__":
    main()
