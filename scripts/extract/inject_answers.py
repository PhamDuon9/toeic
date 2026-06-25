"""
Inject answers from answer_keys.json into all part{1-7}.json files.

Run AFTER: parse_transcript.py (to get answer_keys.json)
Run BEFORE: validate_bank.py
"""

import json
import sys
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent
BANK_DIR = ROOT / "question_bank"
KEYS_FILE = BANK_DIR / "answer_keys.json"

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
    print(f"Loaded answer keys for {len(keys)} tests.")

    total_injected = 0
    total_missing  = 0

    for part_num in target_parts:
        part_file = BANK_DIR / f"part{part_num}.json"
        if not part_file.exists():
            print(f"[skip] {part_file} not found")
            continue

        questions = json.loads(part_file.read_text(encoding="utf-8"))
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
