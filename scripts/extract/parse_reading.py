"""
Parse extracted/READING/ETS 2026 READING/ETS 2026 READING.md
→ question_bank/part5.json, part6.json, part7.json, passages.json

Marker output formats for question numbers:
  1. Table:      | 101. | stem text |  (followed by continuation rows)
  2. List bold:  - **105.** stem text
  3. List plain: - 112. stem text
Options always: - (A) text  or  (A) text
Part 6 quirk:   - **131.** (A) option_text  (option A on same line as question)
"""

import re
import json
from pathlib import Path

ROOT        = Path(__file__).parent.parent.parent
MD_FILE     = ROOT / "extracted" / "READING" / "ETS 2026 READING" / "ETS 2026 READING.md"
BANK_DIR    = ROOT / "question_bank"
BANK_DIR.mkdir(parents=True, exist_ok=True)

# ── Regexes ──────────────────────────────────────────────────────────────────
RE_Q_TABLE  = re.compile(r"^\|\s*\*{0,2}(\d{3})\.\*{0,2}\s*\|(.*)")             # | 101. | rest of row
RE_Q_TABLE4 = re.compile(r"^\|\s*\*{0,2}(\d{3})\.\*{0,2}\s*\|([^|]*)\|\s*\*{0,2}(\d{3})\.\*{0,2}\s*\|([^|]*)\|")  # | N. | | M. | |
RE_Q_LIST   = re.compile(r"^[-*]\s+\*{0,2}(\d{3})\.\*{0,2}\s*(.*)")             # - **105.** text
RE_Q_BARE   = re.compile(r"^\*{0,2}(\d{3})\.\*{0,2}\s+(.*)")                    # 101. text
RE_T_CONT   = re.compile(r"^\|\s*\|\s*(.*)")                                     # |   | continuation (full row)
RE_T4_CONT  = re.compile(r"^\|\s*\|([^|]*)\|\s*\|([^|]*)\|")                    # |   | text1 |   | text2 |
RE_T_SEP    = re.compile(r"^\|[-\s|]+\|$")                                       # |---|---|
RE_OPT      = re.compile(r"^[-*\s]*\(([ABCD])\)\s+(.*)")                         # - (A) text
RE_INLINE_OPT = re.compile(r"\(([ABCD])\)\s+([^(]+?)(?=\s*\([ABCD]\)|$)")       # inline (A) opt (B) opt
RE_BLANK    = re.compile(r"-{4,}|_{4,}")
RE_PART_HDR = re.compile(r"(?:#+ )?PART\s+([567])", re.IGNORECASE)
RE_P67_RNG  = re.compile(r"Questions?\s+(\d+)[\s\-–]+(\d+)\s+refer", re.IGNORECASE)
RE_TEST_SPL = re.compile(r"\n(?=#{1,4}\s+\*{0,2}READING TEST)", re.IGNORECASE)  # exact 10 occurrences

NOISE = re.compile(
    r"(answer sheet|mark the letter|mark your answer|directions:"
    r"|select the best|four answer choices|word or phrase|time allowed"
    r"|comprehension questions|go on to the next page|you will read"
    r"|in the reading test|reading test|part 5|part 6|part 7)",
    re.IGNORECASE,
)

PART5_Q = range(101, 131)
PART6_Q = range(131, 147)
PART7_Q = range(147, 201)


def make_id(part: int, test: int, question: int) -> str:
    return f"p{part}-t{test:02d}-q{question:03d}"


def normalize_blank(text: str) -> str:
    return RE_BLANK.sub("_______", text).strip()


def is_noise(line: str) -> bool:
    return bool(NOISE.search(line)) or len(line.strip()) < 3


def parse_inline(text: str) -> tuple[str, dict]:
    """Split 'stem (A) opt (B) opt (C) opt (D) opt' into (stem, options).
    Returns (text, {}) if no inline options found."""
    m_first = RE_INLINE_OPT.search(text)
    if not m_first:
        return text.strip(), {}
    stem = text[:m_first.start()].strip()
    opts = {m.group(1): m.group(2).strip() for m in RE_INLINE_OPT.finditer(text)}
    return stem, opts


RE_HTML_TAG = re.compile(r"<[^>]+>")

def parse_table_cells(text: str) -> str:
    """Join all table cells after the question number cell.
    If multiple cells: insert _______ between first and remaining cells
    (the blank in the book creates extra whitespace → Marker splits into multiple columns).
    Strip HTML tags."""
    text = RE_HTML_TAG.sub("", text)
    parts = [p.strip() for p in text.split("|") if p.strip()]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    # Multi-cell: blank was between cell 1 and the rest
    return parts[0] + " _______ " + " ".join(parts[1:])


def apply_cell(q: dict, text: str, is_continuation: bool = False):
    """Apply table cell/continuation text: parse opts or extend stem.
    is_continuation=True → insert _______ before joining if stem has no blank yet."""
    text = RE_HTML_TAG.sub("", text).strip()
    if not text:
        return
    _, opts = parse_inline(text)
    if opts:
        q["options"].update(opts)
    elif not q["options"]:
        if is_continuation and "_______" not in q["stem"]:
            q["stem"] = q["stem"] + " _______ " + text
        else:
            q["stem"] = (q["stem"] + " " + text).strip()


def match_qnum(line: str):
    """Try list/bare formats only (not table — handled separately). Returns (qnum, rest) or None."""
    for pat in (RE_Q_LIST, RE_Q_BARE):
        m = pat.match(line)
        if m:
            return int(m.group(1)), m.group(2).strip()
    return None


# ── Part 5 ────────────────────────────────────────────────────────────────────

def parse_part5(lines: list[str], test_num: int) -> list[dict]:
    """Handles table (2-col & 4-col), list-bold, and list-plain formats."""
    questions = {}
    cur_q  = None   # primary (or only) question
    cur_q2 = None   # right-column question in 4-col table rows

    for line in lines:
        raw = line.strip()
        if not raw or is_noise(raw) or RE_T_SEP.match(raw):
            continue

        # ── 4-column table row: | N. | text | M. | text | ──
        m4 = RE_Q_TABLE4.match(raw)
        if m4:
            cur_q2 = None
            q1, t1 = int(m4.group(1)), m4.group(2)
            q2, t2 = int(m4.group(3)), m4.group(4)
            if q1 in PART5_Q:
                s, o = parse_inline(t1)
                questions[q1] = {"stem": s, "options": o}
                cur_q = q1
            if q2 in PART5_Q:
                s, o = parse_inline(t2)
                questions[q2] = {"stem": s, "options": o}
                cur_q2 = q2
            continue

        # ── 4-column continuation: |   | text1 |   | text2 | ──
        m4c = RE_T4_CONT.match(raw)
        if m4c and cur_q2 is not None:
            if cur_q  in questions: apply_cell(questions[cur_q],  m4c.group(1), is_continuation=True)
            if cur_q2 in questions: apply_cell(questions[cur_q2], m4c.group(2), is_continuation=True)
            continue

        # ── Table row with question number: | N. | rest-of-row | ──
        m2 = RE_Q_TABLE.match(raw)
        if m2:
            cur_q2 = None
            qnum   = int(m2.group(1))
            cells  = parse_table_cells(m2.group(2))   # handles multi-cell blank insertion
            if qnum in PART5_Q:
                s, o = parse_inline(cells)
                questions[qnum] = {"stem": s, "options": o}
                cur_q = qnum
            else:
                cur_q = None
            continue

        # ── Table continuation row: |   | text | (may have multiple cells from word-wrap) ──
        m_cont = RE_T_CONT.match(raw)
        if m_cont and cur_q in questions and cur_q2 is None:
            # Join all non-empty cells with space (word-wrap artifact, no blank)
            cont_text = " ".join(c.strip() for c in m_cont.group(1).split("|") if c.strip())
            apply_cell(questions[cur_q], cont_text, is_continuation=True)
            continue

        # ── List-format question ──
        result = match_qnum(raw)
        if result:
            cur_q2 = None
            qnum, rest = result
            if qnum in PART5_Q:
                s, o = parse_inline(rest)
                questions[qnum] = {"stem": s, "options": o}
                cur_q = qnum
            else:
                cur_q = None
            continue

        # ── Option line ──
        m_opt = RE_OPT.match(raw)
        if m_opt and cur_q in questions:
            questions[cur_q]["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        # ── Stem continuation ──
        if cur_q in questions and not questions[cur_q]["options"]:
            questions[cur_q]["stem"] += " " + raw

    return [
        {
            "id":         make_id(5, test_num, q),
            "part":       5,
            "test":       test_num,
            "question":   q,
            "stem":       normalize_blank(questions[q]["stem"]),
            "options":    questions[q]["options"],
            "answer":     None,
            "difficulty": None,
            "tags":       [],
        }
        for q in sorted(questions) if q in PART5_Q
    ]


# ── Part 6 ────────────────────────────────────────────────────────────────────

def parse_part6(lines: list[str], test_num: int) -> tuple[list[dict], list[dict]]:
    passages      = []
    questions     = {}
    passage_lines = []
    cur_range     = None
    cur_q         = None
    in_qs         = False

    def flush_passage():
        if cur_range and passage_lines:
            passages.append({
                "id":             f"p6-t{test_num:02d}-p{len(passages)+1:02d}",
                "part":           6,
                "test":           test_num,
                "passage_num":    len(passages) + 1,
                "passage_type":   "text_completion",
                "question_range": cur_range,
                "text":           " ".join(passage_lines).strip(),
                "images":         [],
            })

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        m_rng = RE_P67_RNG.search(raw)
        if m_rng:
            flush_passage()
            cur_range     = [int(m_rng.group(1)), int(m_rng.group(2))]
            passage_lines = []
            in_qs         = False
            cur_q         = None
            continue

        result = match_qnum(raw)
        if result:
            qnum, rest = result
            if qnum in PART6_Q:
                in_qs = True
                cur_q = qnum
                questions[qnum] = {"options": {}, "passage_ref": len(passages)}
                # Option A may be inline: - **131.** (A) text
                m_opt = RE_OPT.match(rest)
                if m_opt:
                    questions[qnum]["options"][m_opt.group(1)] = m_opt.group(2).strip()
            else:
                cur_q = None
            continue

        m_opt = RE_OPT.match(raw)
        if m_opt and cur_q in questions:
            questions[cur_q]["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        if not in_qs and not is_noise(raw) and not RE_T_SEP.match(raw):
            passage_lines.append(raw)

    flush_passage()

    result      = []
    first_q_ref = {}
    for qnum in sorted(questions):
        if qnum not in PART6_Q:
            continue
        q    = questions[qnum]
        pref = q["passage_ref"]
        is_first = pref not in first_q_ref
        if is_first:
            first_q_ref[pref] = qnum
        result.append({
            "id":         make_id(6, test_num, qnum),
            "part":       6,
            "test":       test_num,
            "question":   qnum,
            "passage_id": passages[pref]["id"] if pref < len(passages) else None,
            "passage":    passages[pref]["text"] if (is_first and pref < len(passages)) else "",
            "stem":       None,
            "options":    q["options"],
            "answer":     None,
            "difficulty": None,
            "tags":       [],
        })
    return result, passages


# ── Part 7 ────────────────────────────────────────────────────────────────────

def passage_type(header: str) -> str:
    hl = header.lower()
    if hl.count(" and ") >= 2:
        return "triple"
    if hl.count(" and ") == 1 or "double" in hl:
        return "double"
    return "single"


def parse_part7(lines: list[str], test_num: int) -> tuple[list[dict], list[dict]]:
    passages      = []
    questions     = {}
    passage_lines = []
    cur_range     = None
    cur_ptype     = "single"
    cur_q         = None
    in_qs         = False

    def flush_passage():
        nonlocal passage_lines, cur_range, cur_ptype
        if cur_range and passage_lines:
            passages.append({
                "id":             f"p7-t{test_num:02d}-p{len(passages)+1:02d}",
                "part":           7,
                "test":           test_num,
                "passage_num":    len(passages) + 1,
                "passage_type":   cur_ptype,
                "question_range": cur_range,
                "text":           " ".join(passage_lines).strip(),
                "images":         [],
            })
        passage_lines = []
        cur_range     = None

    pending_passage_lines: list[str] = []   # lines seen before a Q-header-less passage

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        m_rng = RE_P67_RNG.search(raw)
        if m_rng:
            if not in_qs:
                flush_passage()
            cur_range = [int(m_rng.group(1)), int(m_rng.group(2))]
            cur_ptype = passage_type(raw)
            in_qs     = False
            pending_passage_lines = []
            continue

        result = match_qnum(raw)
        if result:
            qnum, rest = result
            if qnum in PART7_Q:
                if not in_qs:
                    # Flush previous passage
                    flush_passage()
                    # If we accumulated lines without a range header, synthesize passage now
                    if pending_passage_lines and cur_range is None:
                        # Range will be set when we see this and following questions
                        passage_lines = pending_passage_lines[:]
                    pending_passage_lines = []
                in_qs = True
                cur_q = qnum
                # If no range header was found, start tracking from this question
                if cur_range is None:
                    cur_range = [qnum, qnum]
                else:
                    cur_range[1] = max(cur_range[1], qnum)
                questions[qnum] = {
                    "stem":        normalize_blank(rest),
                    "options":     {},
                    "passage_ref": len(passages),
                }
            else:
                cur_q = None
            continue

        m_opt = RE_OPT.match(raw)
        if m_opt and cur_q in questions:
            questions[cur_q]["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        if cur_q in questions and not questions[cur_q]["options"]:
            questions[cur_q]["stem"] = (questions[cur_q]["stem"] + " " + raw).strip()
        elif not in_qs and not is_noise(raw) and not RE_T_SEP.match(raw):
            passage_lines.append(raw)
            if cur_range is None:
                pending_passage_lines.append(raw)

    flush_passage()

    result      = []
    first_q_ref = {}
    for qnum in sorted(questions):
        if qnum not in PART7_Q:
            continue
        q    = questions[qnum]
        pref = q["passage_ref"]
        is_first = pref not in first_q_ref
        if is_first:
            first_q_ref[pref] = qnum
        result.append({
            "id":            make_id(7, test_num, qnum),
            "part":          7,
            "test":          test_num,
            "question":      qnum,
            "passage_id":    passages[pref]["id"]             if pref < len(passages) else None,
            "passage_type":  passages[pref]["passage_type"]   if pref < len(passages) else "single",
            "passage":       passages[pref]["text"]           if (is_first and pref < len(passages)) else "",
            "passage_range": passages[pref]["question_range"] if pref < len(passages) else None,
            "stem":          q["stem"],
            "options":       q["options"],
            "answer":        None,
            "difficulty":    None,
            "tags":          [],
        })
    return result, passages


# ── Split & Main ──────────────────────────────────────────────────────────────

def split_by_test(md_text: str) -> list[str]:
    """Split on '#### **READING TEST**' — appears exactly 10 times in ETS 2026."""
    parts = re.split(RE_TEST_SPL, md_text)
    # Drop leading preamble (before first READING TEST marker)
    reading = [p for p in parts if re.search(r"READING TEST", p, re.IGNORECASE)]
    return reading[:10] if len(reading) >= 10 else parts


def extract_part_section(test_text: str, part_num: int) -> list[str]:
    lines    = test_text.splitlines()
    result   = []
    in_part  = False
    for line in lines:
        m = RE_PART_HDR.match(line.strip())
        if m:
            in_part = int(m.group(1)) == part_num
            continue
        if in_part:
            result.append(line)
    return result if result else lines


def main():
    if not MD_FILE.exists():
        print(f"[ERROR] Not found: {MD_FILE}")
        print("Run first: python scripts/extract/run_marker.py reading")
        return

    print(f"Loading {MD_FILE.name} ...")
    md_text = MD_FILE.read_text(encoding="utf-8")
    print(f"  {len(md_text):,} chars, {len(md_text.splitlines())} lines\n")

    all_p5, all_p6, all_p7, all_passages = [], [], [], []
    test_sections = split_by_test(md_text)
    print(f"Detected {len(test_sections)} test sections.\n")

    for i, test_text in enumerate(test_sections[:10]):
        test_num = i + 1
        print(f"-- Test {test_num} --")

        p5 = parse_part5(extract_part_section(test_text, 5), test_num)
        p5_full = sum(1 for q in p5 if len(q["options"]) == 4)
        flag5 = "" if len(p5) == 30 else f" << MISSING {30-len(p5)}"
        print(f"  Part 5: {len(p5)}/30 ({p5_full} complete){flag5}")
        all_p5.extend(p5)

        p6, passages6 = parse_part6(extract_part_section(test_text, 6), test_num)
        p6_full = sum(1 for q in p6 if len(q["options"]) == 4)
        flag6 = "" if len(p6) == 16 else f" << MISSING {16-len(p6)}"
        print(f"  Part 6: {len(p6)}/16 ({p6_full} complete), {len(passages6)} passages{flag6}")
        all_p6.extend(p6)
        all_passages.extend(passages6)

        p7, passages7 = parse_part7(extract_part_section(test_text, 7), test_num)
        p7_full = sum(1 for q in p7 if len(q["options"]) == 4)
        flag7 = "" if len(p7) == 54 else f" << MISSING {54-len(p7)}"
        print(f"  Part 7: {len(p7)}/54 ({p7_full} complete), {len(passages7)} passages{flag7}")
        all_p7.extend(p7)
        all_passages.extend(passages7)

    def write_json(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n[saved] {path}  ({len(data)} records)")

    write_json(BANK_DIR / "part5.json", all_p5)
    write_json(BANK_DIR / "part6.json", all_p6)
    write_json(BANK_DIR / "part7.json", all_p7)
    write_json(BANK_DIR / "passages.json", all_passages)

    p5_full = sum(1 for q in all_p5 if len(q["options"]) == 4)
    p6_full = sum(1 for q in all_p6 if len(q["options"]) == 4)
    p7_full = sum(1 for q in all_p7 if len(q["options"]) == 4)
    print(f"\n{'='*55}")
    print(f"Part 5: {len(all_p5)}/300  ({p5_full} complete)")
    print(f"Part 6: {len(all_p6)}/160  ({p6_full} complete)")
    print(f"Part 7: {len(all_p7)}/540  ({p7_full} complete)")
    print(f"Passages: {len(all_passages)}")
    print("Run next: python scripts/extract/parse_transcript.py")


if __name__ == "__main__":
    main()
