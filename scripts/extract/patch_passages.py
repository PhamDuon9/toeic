"""
Patch passages.json by finding passage text blocks that parse_reading.py missed.

Strategy: for each test block in READING.md, scan Part 7 region.
After the last option of a question group, accumulate text until the next
question number. That text = the passage for the upcoming question group.

Run AFTER: parse_reading.py + inject_answers.py
"""

import re
import json
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent
MD_FILE  = ROOT / "extracted" / "READING" / "ETS 2026 READING" / "ETS 2026 READING.md"
BANK_DIR = ROOT / "question_bank"
P7_FILE  = BANK_DIR / "part7.json"
PSG_FILE = BANK_DIR / "passages.json"

RE_TEST_SPLIT = re.compile(r"\n(?=#{1,4}\s+\*{0,2}READING TEST)", re.IGNORECASE)
RE_Q_HDR      = re.compile(r"Questions?\s+(\d+)[\s\-–]+(\d+)\s+refer", re.IGNORECASE)
RE_Q_NUM      = re.compile(r"^[-*\s]*\*{0,2}(\d{3})\.\*{0,2}\s*")
RE_OPT        = re.compile(r"^[-*\s]*\(([ABCD])\)\s+")
RE_T_SEP      = re.compile(r"^\|[-\s|]+\|$")
PART7_Q       = set(range(147, 201))

NOISE = re.compile(
    r"(answer sheet|mark the letter|directions:|select the best"
    r"|four answer choices|go on to the next page|reading test|part 7"
    r"|you will read|time allowed|questions?\s+\d+.*?refer)",
    re.IGNORECASE,
)


def is_noise(line: str) -> bool:
    return bool(NOISE.search(line)) or len(line.strip()) < 2


def extract_passage_blocks(test_block: str, test_num: int) -> list[dict]:
    """
    Scan a test block and return passage dicts {first_q, last_q, text}
    for ALL passages (both with and without range headers).
    """
    lines = test_block.splitlines()
    results = []

    # State machine
    cur_q        = None
    last_p7_q    = None   # last Part-7 question seen
    in_options   = False
    passage_buf  = []     # accumulating passage text
    after_opts   = False  # True = past last option, accumulating next passage
    cur_group    = []     # question numbers in current group
    cur_range    = None   # from explicit header

    def flush_group():
        nonlocal cur_group, passage_buf, after_opts, cur_range
        if passage_buf and cur_group:
            text = " ".join(l for l in passage_buf if l.strip())
            if len(text.strip()) > 20:
                results.append({
                    "first_q": cur_group[0],
                    "last_q":  cur_group[-1],
                    "range":   cur_range or [cur_group[0], cur_group[-1]],
                    "text":    text.strip(),
                })
        cur_group = []
        passage_buf = []
        after_opts = False
        cur_range = None

    # Passage being built for the NEXT group
    next_passage_buf = []

    for line in lines:
        raw = line.strip()

        # Explicit range header
        m_rng = RE_Q_HDR.search(raw)
        if m_rng:
            # Start of new passage section
            if cur_group:
                flush_group()
            next_passage_buf = []
            cur_range = [int(m_rng.group(1)), int(m_rng.group(2))]
            after_opts = False
            continue

        # Question line
        m_q = RE_Q_NUM.match(raw)
        if m_q:
            qnum = int(m_q.group(1))
            if qnum in PART7_Q:
                # Are we starting a new group?
                if cur_group and qnum != last_p7_q + 1:
                    # New group — flush old
                    flush_group()
                    # The passage for this new group is what we collected
                    passage_buf = next_passage_buf[:]
                    next_passage_buf = []

                if not cur_group:
                    passage_buf = next_passage_buf[:]
                    next_passage_buf = []

                cur_group.append(qnum)
                last_p7_q = qnum
                in_options = False
                after_opts = False
                cur_q = qnum
            else:
                cur_q = None
            continue

        # Option line
        if RE_OPT.match(raw):
            if cur_q in PART7_Q:
                in_options = True
                after_opts = False
            continue

        # After last option = accumulate next passage
        if in_options and cur_q in PART7_Q and raw and not RE_T_SEP.match(raw):
            # We just passed options; reset in_options on next non-option
            in_options = False
            after_opts = True

        if after_opts or (not cur_group and not is_noise(raw) and raw):
            if not is_noise(raw) and not RE_T_SEP.match(raw) and raw:
                next_passage_buf.append(raw)

        # Also accumulate if we have a cur_range and not yet in questions
        if cur_range and not cur_group and not is_noise(raw) and raw and not RE_T_SEP.match(raw):
            if raw not in next_passage_buf:
                pass  # Already handled above

    # Flush last group
    if cur_group:
        if next_passage_buf:
            passage_buf = passage_buf or next_passage_buf
        flush_group()

    return results


def main():
    if not MD_FILE.exists():
        print(f"[ERROR] {MD_FILE} not found")
        return

    print(f"Loading {MD_FILE}...")
    md_text = MD_FILE.read_text(encoding="utf-8")

    passages = json.loads(PSG_FILE.read_text(encoding="utf-8"))
    p7       = json.loads(P7_FILE.read_text(encoding="utf-8"))

    # Build coverage set from existing passages
    covered = {}  # (test, q) -> passage_id
    for p in passages:
        if not p["id"].startswith("p7-"):
            continue
        qr = p.get("question_range", [])
        t  = p["test"]
        if len(qr) == 2:
            for q in range(qr[0], qr[1] + 1):
                covered[(t, q)] = p["id"]

    test_blocks = RE_TEST_SPLIT.split(md_text)
    added = 0

    for test_idx, block in enumerate(test_blocks[1:], start=1):
        blocks_data = extract_passage_blocks(block, test_idx)
        for bd in blocks_data:
            fq, lq = bd["first_q"], bd["last_q"]
            # Skip if already covered
            if all((test_idx, q) in covered for q in range(fq, lq + 1)):
                continue
            # Skip if no useful text
            if len(bd["text"]) < 20:
                continue

            # Find uncovered questions in this group
            uncovered_qs = [q for q in range(fq, lq + 1) if (test_idx, q) not in covered]
            if not uncovered_qs:
                continue

            # Determine passage ID
            existing_t = [p for p in passages if p.get("test") == test_idx and p["id"].startswith("p7-")]
            pnum = len(existing_t) + 1
            pid  = f"p7-t{test_idx:02d}-p{pnum:02d}-x"

            qr = [uncovered_qs[0], uncovered_qs[-1]]
            new_psg = {
                "id":             pid,
                "part":           7,
                "test":           test_idx,
                "passage_num":    pnum,
                "passage_type":   "single",
                "question_range": qr,
                "text":           bd["text"],
                "images":         [],
            }
            passages.append(new_psg)

            for q in uncovered_qs:
                covered[(test_idx, q)] = pid

            print(f"  [T{test_idx}] {pid} q{qr[0]}-{qr[1]}: {bd['text'][:70]}...")
            added += 1

    # Rebuild passage_id in part7.json
    lookup = {}
    for p in passages:
        if not p["id"].startswith("p7-"):
            continue
        t  = p["test"]
        qr = p.get("question_range", [])
        if len(qr) == 2:
            for qn in range(qr[0], qr[1] + 1):
                lookup[(t, qn)] = p["id"]

    fixed = 0
    for q in p7:
        pid = lookup.get((q["test"], q["question"]))
        if pid and pid != q.get("passage_id"):
            q["passage_id"] = pid
            fixed += 1

    PSG_FILE.write_text(json.dumps(passages, indent=2, ensure_ascii=False), encoding="utf-8")
    P7_FILE.write_text(json.dumps(p7, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nAdded {added} passages, fixed {fixed} passage_id links")
    print(f"passages.json: {len(passages)} total\n")

    # Coverage report
    cov_set = set()
    for p in passages:
        if not p["id"].startswith("p7-"):
            continue
        qr = p.get("question_range", [])
        t  = p["test"]
        if len(qr) == 2:
            cov_set.update((t, q) for q in range(qr[0], qr[1] + 1))

    total_cov = 0
    for t in range(1, 11):
        cov = sum(1 for q in range(147, 201) if (t, q) in cov_set)
        total_cov += cov
        status = "OK" if cov == 54 else f"missing {54-cov}"
        print(f"  T{t:2d}: {cov}/54 [{status}]")
    print(f"\nTotal: {total_cov}/540")


if __name__ == "__main__":
    main()
