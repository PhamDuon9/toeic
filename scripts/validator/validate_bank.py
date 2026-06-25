"""
Validate question_bank/ completeness and schema correctness.

Usage:
    python scripts/validator/validate_bank.py [--part 5] [--fix]

Output: terminal summary + REPORTS/validation_report.json
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

ROOT      = Path(__file__).parent.parent.parent
BANK_DIR  = ROOT / "question_bank"
REPORT_DIR = ROOT / "REPORTS"
REPORT_DIR.mkdir(exist_ok=True)

EXPECTED_COUNTS = {1: 60, 2: 250, 3: 390, 4: 300, 5: 300, 6: 160, 7: 540}
PART_Q_RANGES   = {
    1: range(1, 7),    2: range(7, 32),
    3: range(32, 71),  4: range(71, 101),
    5: range(101, 131), 6: range(131, 147),
    7: range(147, 201),
}
VALID_ANSWERS = {"A", "B", "C", "D"}


def load_part(part_num: int) -> list[dict]:
    path = BANK_DIR / f"part{part_num}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def check_part(part_num: int) -> dict:
    questions = load_part(part_num)
    expected  = EXPECTED_COUNTS[part_num]
    q_range   = PART_Q_RANGES[part_num]

    errors = []
    warnings = []

    # Count check
    if len(questions) != expected:
        errors.append(f"Count: got {len(questions)}, expected {expected}")

    # Per-question checks
    seen_ids = set()
    answer_count = 0

    for q in questions:
        qid = q.get("id", "MISSING_ID")

        # Duplicate IDs
        if qid in seen_ids:
            errors.append(f"Duplicate ID: {qid}")
        seen_ids.add(qid)

        # Question number in valid range
        qnum = q.get("question")
        if qnum not in q_range:
            warnings.append(f"Q{qnum} outside expected range {q_range.start}-{q_range.stop-1}")

        # Test number valid
        tnum = q.get("test")
        if not (1 <= (tnum or 0) <= 10):
            errors.append(f"{qid}: test={tnum} out of range")

        # Options completeness (parts 3-7)
        if part_num >= 3:
            opts = q.get("options", {})
            missing_opts = VALID_ANSWERS - set(opts.keys())
            if missing_opts:
                warnings.append(f"{qid}: missing options {missing_opts}")

        # Answer validity
        ans = q.get("answer")
        if ans is not None:
            if ans not in VALID_ANSWERS:
                errors.append(f"{qid}: invalid answer '{ans}'")
            else:
                answer_count += 1

        # Media files (Part 1)
        if part_num == 1:
            img = q.get("image")
            if img:
                img_path = BANK_DIR / img
                if not img_path.exists():
                    warnings.append(f"{qid}: image not found: {img}")
            else:
                warnings.append(f"{qid}: no image path")

    return {
        "part":          part_num,
        "total":         len(questions),
        "expected":      expected,
        "count_ok":      len(questions) == expected,
        "answers":       answer_count,
        "answers_pct":   round(answer_count / expected * 100, 1) if expected > 0 else 0,
        "errors":        errors,
        "warnings":      warnings,
    }


def check_answer_keys() -> dict:
    keys_file = BANK_DIR / "answer_keys.json"
    if not keys_file.exists():
        return {"exists": False, "tests": 0, "complete": False}

    keys = json.loads(keys_file.read_text(encoding="utf-8"))
    complete_tests = sum(1 for t, v in keys.items() if len(v) >= 200)
    return {
        "exists":         True,
        "tests":          len(keys),
        "complete_tests": complete_tests,
        "complete":       complete_tests == 10,
    }


def check_unique_ids_across_parts(target_parts: list[int]) -> list[str]:
    all_ids = []
    for p in target_parts:
        for q in load_part(p):
            all_ids.append(q.get("id"))
    dups = [i for i in all_ids if all_ids.count(i) > 1]
    return list(set(dups))


def print_summary(results: list[dict], key_result: dict, cross_dups: list[str]):
    print("\n" + "=" * 60)
    print("TOEIC KNOWLEDGE BASE — VALIDATION REPORT")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    total_q = sum(r["total"] for r in results)
    total_expected = sum(r["expected"] for r in results)
    total_answers  = sum(r["answers"] for r in results)

    for r in results:
        status = "OK" if r["count_ok"] and not r["errors"] else "FAIL"
        print(f"\nPart {r['part']} [{status}]")
        print(f"  Questions : {r['total']}/{r['expected']}")
        print(f"  Answers   : {r['answers']}/{r['expected']} ({r['answers_pct']}%)")
        if r["errors"]:
            for e in r["errors"][:5]:
                print(f"  [ERROR]   {e}")
        if r["warnings"]:
            for w in r["warnings"][:5]:
                print(f"  [WARN]    {w}")
            if len(r["warnings"]) > 5:
                print(f"  ... and {len(r['warnings'])-5} more warnings")

    print(f"\n{'='*60}")
    print(f"TOTAL  : {total_q}/{total_expected} questions ({total_q/total_expected*100:.0f}%)" if total_expected else "")
    print(f"ANSWERS: {total_answers}/{total_expected} ({total_answers/total_expected*100:.0f}%)" if total_expected else "")
    print(f"KEYS   : {key_result}")
    if cross_dups:
        print(f"CROSS-PART DUPLICATE IDs: {cross_dups}")
    print("=" * 60)


def main():
    args = sys.argv[1:]
    target_parts = list(range(1, 8))

    if "--part" in args:
        idx = args.index("--part")
        target_parts = [int(args[idx + 1])]

    results = [check_part(p) for p in target_parts]
    key_result = check_answer_keys()
    cross_dups = check_unique_ids_across_parts(target_parts)

    print_summary(results, key_result, cross_dups)

    # Write JSON report
    report = {
        "date":       datetime.now().isoformat(),
        "parts":      results,
        "answer_keys": key_result,
        "cross_duplicate_ids": cross_dups,
    }
    report_path = REPORT_DIR / "validation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[saved] {report_path}")


if __name__ == "__main__":
    main()
