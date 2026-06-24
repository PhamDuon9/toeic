# scripts/build_part4_bank.py
# Extract Part 4 (Talks) questions from LISTENING.pdf
# Part 4: Q71-100 per test (10 talks x 3 questions each)
# Same 2-column layout as Part 3

import sys, re, json, fitz
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ocr_engine import ocr_two_column, render_pdf_page

PDF_PATH   = Path("../raw/ETS 2026 LISTENING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part4.json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PART4_PAGE_OFFSETS = [9, 10, 11]
PART4_Q_START = 71
PART4_Q_END   = 100

RE_QUESTION = re.compile(r"^(\d{2,3})\.\s+(.+)")
RE_OPTION   = re.compile(r"^\(([ABCD])\)\s+(.+)")


def parse_questions(text: str) -> list[dict]:
    questions = []
    current_q = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m_q = RE_QUESTION.match(line)
        if m_q:
            if current_q:
                questions.append(current_q)
            qnum = int(m_q.group(1))
            if PART4_Q_START <= qnum <= PART4_Q_END:
                current_q = {
                    "question": qnum,
                    "stem": m_q.group(2).strip(),
                    "options": {},
                    "answer": None
                }
            else:
                current_q = None
            continue

        if current_q is None:
            continue

        m_opt = RE_OPTION.match(line)
        if m_opt:
            current_q["options"][m_opt.group(1)] = m_opt.group(2).strip()
        elif current_q and len(current_q["options"]) == 0:
            current_q["stem"] += " " + line

    if current_q:
        questions.append(current_q)

    return questions


def main():
    doc = fitz.open(str(PDF_PATH))
    all_entries = []

    for test_idx in range(10):
        test_num = test_idx + 1
        dir_page = 1 + test_idx * 14
        test_entries = []

        print(f"\n-- Test {test_num} --")
        for offset in PART4_PAGE_OFFSETS:
            page_idx = dir_page + offset
            print(f"  OCR page {page_idx + 1}...", end=" ", flush=True)
            img  = render_pdf_page(doc, page_idx)
            text = ocr_two_column(img)
            qs   = parse_questions(text)
            print(f"{len(qs)} questions found")
            test_entries.extend(qs)

        for q in test_entries:
            q["test"] = test_num
            offset_from_start = q["question"] - PART4_Q_START
            set_idx   = offset_from_start // 3
            set_first = PART4_Q_START + set_idx * 3
            set_last  = set_first + 2
            q["audio"] = f"Test_{test_num:02d}-{set_first:02d}-{set_last:02d}.mp3"

        all_entries.extend(test_entries)
        print(f"  Total Part 4 questions found for Test {test_num}: {len(test_entries)}/30")

    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing_keys = {(e["test"], e["question"]) for e in existing}
        for e in all_entries:
            if (e["test"], e["question"]) not in existing_keys:
                existing.append(e)
        all_entries = existing

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(all_entries)} entries -> {JSON_PATH}")


if __name__ == "__main__":
    main()
