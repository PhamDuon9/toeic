"""
Inject answers from answer_keys.json into all part{1-7}.json files.
Also extracts Reading answer keys from READING.md and merges them in.

Run AFTER: parse_transcript.py (to get answer_keys.json)
Run BEFORE: validate_bank.py
"""

import re
import json
import sys
from pathlib import Path

ROOT      = Path(__file__).parent.parent.parent
BANK_DIR  = ROOT / "question_bank"
KEYS_FILE = BANK_DIR / "answer_keys.json"
READING_MD = ROOT / "extracted" / "READING" / "ETS 2026 READING" / "ETS 2026 READING.md"

RE_HTML_CELL   = re.compile(r"(?:<b>)?(\d+)(?:</b>)?\s*\(([ABCD])\)")
RE_TEST_TBLHDR = re.compile(r"\|\s*기출.*?\|\s*TEST\s*\|\s*(\d+)\s*\|")
VALID_ANSWERS  = {"A", "B", "C", "D"}


def extract_reading_keys(md_text: str) -> dict:
    """Extract answer keys for questions 101-200 from READING.md."""
    keys = {}
    current_test = None
    for line in md_text.splitlines():
        m_tbl = RE_TEST_TBLHDR.search(line)
        if m_tbl:
            current_test = int(m_tbl.group(1))
            if current_test not in keys:
                keys[current_test] = {}
            continue
        if current_test is None:
            continue
        for m in RE_HTML_CELL.finditer(line):
            q, ans = int(m.group(1)), m.group(2)
            if 101 <= q <= 200 and ans in VALID_ANSWERS:
                keys[current_test][q] = ans
    return keys

PART_RANGES = {
    1: range(1, 7),
    2: range(7, 32),
    3: range(32, 71),
    4: range(71, 101),
    5: range(101, 131),
    6: range(131, 147),
    7: range(147, 201),
}


def main():
    target_parts = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 8))

    if not KEYS_FILE.exists():
        print(f"[ERROR] {KEYS_FILE} not found. Run parse_transcript.py first.")
        return

    keys = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded answer keys for {len(keys)} tests (listening).")

    # Merge Reading answer keys (q101-200)
    if READING_MD.exists():
        reading_keys = extract_reading_keys(READING_MD.read_text(encoding="utf-8"))
        merged = 0
        for t, answers in reading_keys.items():
            tk = str(t)
            if tk not in keys:
                keys[tk] = {}
            for q, a in answers.items():
                keys[tk][str(q)] = a
                merged += 1
        print(f"Merged {merged} reading answer keys (q101-200) from READING.md.")
        # Save merged keys back
        KEYS_FILE.write_text(
            json.dumps({t: {str(q): a for q, a in v.items()} if isinstance(list(v.keys())[0], int) else v
                        for t, v in keys.items()}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    else:
        print(f"[skip] READING.md not found — only listening keys available.")

    total_injected = 0
    total_missing  = 0

    for part_num in target_parts:
        part_file = BANK_DIR / f"part{part_num}.json"
        if not part_file.exists():
            print(f"[skip] {part_file} not found")
            continue

        questions = json.loads(part_file.read_text(encoding="utf-8-sig"))
        injected = 0
        missing  = 0

        for q in questions:
            test_key = str(q["test"])
            q_key    = str(q["question"])
            answer   = keys.get(test_key, {}).get(q_key)
            if answer:
                q["answer"] = answer
                injected += 1
            else:
                missing += 1

        part_file.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
        total_injected += injected
        total_missing  += missing
        print(f"  part{part_num}.json: {injected} answers injected, {missing} missing")

    print(f"\nTotal: {total_injected} answers injected, {total_missing} still null")
    if total_missing > 0:
        print("Run validate_bank.py to see which questions are missing answers.")


if __name__ == "__main__":
    main()
