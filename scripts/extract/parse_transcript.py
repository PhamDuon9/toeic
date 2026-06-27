"""
Parse extracted/TRANSCRIPT/ETS 2026 TRANSCRIPT.md → question_bank/answer_keys.json + scripts for Parts 2/3/4.

Run AFTER: python scripts/extract/run_marker.py transcript
Run BEFORE: python scripts/extract/inject_answers.py
"""

import re
import json
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent
MD_FILE  = ROOT / "extracted" / "TRANSCRIPT" / "ETS 2026 TRANSCRIPT" / "ETS 2026 TRANSCRIPT.md"
BANK_DIR = ROOT / "question_bank"
BANK_DIR.mkdir(parents=True, exist_ok=True)

# ── Regexes ──────────────────────────────────────────────────────────────────
RE_ANSWER_INLINE = re.compile(r"(\d+)[.)]\s*([ABCD])")
RE_ANSWER_SPACED = re.compile(r"(\d+)\s+([ABCD])(?=\s|$)")
RE_TEST_HDR      = re.compile(r"TEST\s+(\d+)", re.IGNORECASE)
RE_PART_HDR      = re.compile(r"PART\s+([234])", re.IGNORECASE)
RE_Q_RANGE       = re.compile(r"Questions?\s+(\d+)[\s\-–]+(\d+)", re.IGNORECASE)
RE_Q_NUM_SCRIPT  = re.compile(r"^(\d+)\.\s+(.+)")
RE_SPEAKER       = re.compile(r"^(W|M|Man|Woman|Narrator)[:\s]+(.+)", re.IGNORECASE)
RE_TABLE_ROW     = re.compile(r"\|\s*(\d+)\s*\|\s*([ABCD])\s*\|")
# Format: | <b>7</b> (B) | or | 7 (B) | — actual ETS 2026 TRANSCRIPT format
RE_HTML_CELL     = re.compile(r"(?:<b>)?(\d+)(?:</b>)?\s*\(([ABCD])\)")
# Format: | 기출 | TEST | 1 | — actual section header in answer table
RE_TEST_TBLHDR   = re.compile(r"\|\s*기출.*?\|\s*TEST\s*\|\s*(\d+)\s*\|")

VALID_ANSWERS = {"A", "B", "C", "D"}


def make_id(part: int, test: int, question: int) -> str:
    return f"p{part}-t{test:02d}-q{question:03d}"


# ── Answer key extraction ─────────────────────────────────────────────────────

def extract_answer_keys(md_text: str) -> dict:
    """
    Returns {test_num: {q_num: answer}} for all 10 tests.
    Tries multiple patterns since ETS answer key format varies.
    """
    keys = {}
    current_test = None

    for line in md_text.splitlines():
        # Priority 1: table section header | 기출 | TEST | N | (actual data blocks)
        m_tbl = RE_TEST_TBLHDR.search(line)
        if m_tbl:
            current_test = int(m_tbl.group(1))
            if current_test not in keys:
                keys[current_test] = {}
            continue

        # Priority 2: plain TEST N header (used as fallback for non-table formats)
        m_test = RE_TEST_HDR.search(line)
        if m_test and "기출" not in line and "|" not in line:
            t = int(m_test.group(1))
            if t not in keys:
                keys[t] = {}
            # Don't change current_test here — index lines shouldn't switch context
            continue

        if current_test is None:
            continue

        # Format: | <b>7</b> (B) | — ETS 2026 actual format
        for m in RE_HTML_CELL.finditer(line):
            q, ans = int(m.group(1)), m.group(2)
            if 1 <= q <= 200 and ans in VALID_ANSWERS:
                keys[current_test][q] = ans

        # Fallback: markdown table row | 7 | B |
        for m in RE_TABLE_ROW.finditer(line):
            q, ans = int(m.group(1)), m.group(2)
            if 1 <= q <= 200 and ans in VALID_ANSWERS and q not in keys[current_test]:
                keys[current_test][q] = ans

        # Fallback: "7. B" or "7) B"
        for m in RE_ANSWER_INLINE.finditer(line):
            q, ans = int(m.group(1)), m.group(2)
            if 1 <= q <= 200 and ans in VALID_ANSWERS and q not in keys[current_test]:
                keys[current_test][q] = ans

    return keys


# ── Script extraction ─────────────────────────────────────────────────────────

def extract_scripts(md_text: str) -> dict:
    """
    Returns {(test_num, q_num): script_text} for Parts 2, 3, 4.
    Part 2: individual question scripts
    Parts 3/4: conversation/talk shared across 3 questions
    """
    scripts = {}
    current_test = None
    current_part = None
    current_range = None
    current_lines = []

    def flush():
        if current_test and current_range and current_lines:
            text = "\n".join(current_lines).strip()
            for q in range(current_range[0], current_range[1] + 1):
                scripts[(current_test, q)] = text

    for line in md_text.splitlines():
        raw = line.strip()

        m_test = RE_TEST_HDR.search(raw)
        if m_test:
            flush()
            current_test = int(m_test.group(1))
            current_part = None
            current_range = None
            current_lines = []
            continue

        m_part = RE_PART_HDR.search(raw)
        if m_part:
            flush()
            current_part = int(m_part.group(1))
            current_range = None
            current_lines = []
            continue

        if current_part is None:
            continue

        m_range = RE_Q_RANGE.search(raw)
        if m_range:
            flush()
            current_range = [int(m_range.group(1)), int(m_range.group(2))]
            current_lines = []
            continue

        # Part 2: individual question script
        m_q = RE_Q_NUM_SCRIPT.match(raw)
        if m_q and current_part == 2:
            flush()
            qnum = int(m_q.group(1))
            current_range = [qnum, qnum]
            current_lines = [m_q.group(2).strip()]
            continue

        # Accumulate script lines (speaker turns, narrative text)
        if current_range and raw and not RE_TEST_HDR.search(raw) and not RE_PART_HDR.search(raw):
            # Skip answer letters standing alone (e.g., "(A) On the third floor.")
            # Keep them if they appear to be actual response text
            current_lines.append(raw)

    flush()
    return scripts


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not MD_FILE.exists():
        print(f"[ERROR] Not found: {MD_FILE}")
        print("Run first: python scripts/extract/run_marker.py transcript")
        return

    print(f"Loading {MD_FILE} ...")
    md_text = MD_FILE.read_text(encoding="utf-8")

    # 1. Extract answer keys
    print("\nExtracting answer keys...")
    keys = extract_answer_keys(md_text)
    print(f"  Found answer keys for {len(keys)} tests.")
    for t, answers in sorted(keys.items()):
        coverage = len(answers)
        print(f"  Test {t:2d}: {coverage}/200 answers found {'[OK]' if coverage >= 200 else '[INCOMPLETE]'}")

    answer_keys_path = BANK_DIR / "answer_keys.json"
    answer_keys_path.write_text(
        json.dumps({str(t): {str(q): a for q, a in v.items()} for t, v in keys.items()},
                   indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"[saved] {answer_keys_path}")

    # 2. Extract scripts for Parts 2/3/4
    print("\nExtracting scripts...")
    scripts = extract_scripts(md_text)
    print(f"  Found {len(scripts)} script entries.")

    # 3. Inject scripts into part2/3/4.json if they exist
    for part_num, q_range in [(2, range(7, 32)), (3, range(32, 71)), (4, range(71, 101))]:
        part_file = BANK_DIR / f"part{part_num}.json"
        if not part_file.exists():
            print(f"  [skip] {part_file} not found — run parse_listening.py first")
            continue

        questions = json.loads(part_file.read_text(encoding="utf-8-sig"))
        injected = 0
        for q in questions:
            key = (q["test"], q["question"])
            if key in scripts:
                q["script"] = scripts[key]
                injected += 1
        part_file.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [saved] part{part_num}.json — {injected} scripts injected")

    print("\nRun next: python scripts/extract/inject_answers.py")


if __name__ == "__main__":
    main()
