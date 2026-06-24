# scripts/build_part3_bank.py
# Extract Part 3 (Conversations) questions from LISTENING.pdf
# Part 3: Q32-70 per test (13 conversations x 3 questions each)
# Page layout: 2-column text, occasionally a graphic (table/map)

import sys, re, json, fitz
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ocr_engine import ocr_two_column, render_pdf_page

PDF_PATH   = Path("../raw/ETS 2026 LISTENING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part3.json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Known page structure: 10 tests, 14 PDF pages each, 0-indexed
# Part 3 starts after Part 2 (which is 1 page of directions + 0 content pages)
# Test N directions at PDF page: 1 + (N-1)*14  (0-indexed)
# Part 1: +1 to +3 (3 pages)
# Part 2: +4 (1 page, directions only — no questions printed)
# Part 3: +5 to +8 (4 pages, ~12 questions per page pair)
# Part 4: +9 to +11
# Answer key: +12 to +13

PART3_PAGE_OFFSETS = [5, 6, 7, 8]   # relative to test directions page
PART3_Q_START = 32
PART3_Q_END   = 70

# Regex patterns for parsing OCR output
RE_QUESTION = re.compile(r"^(\d{2,3})\.\s+(.+)")
RE_OPTION   = re.compile(r"^\(([ABCD])\)\s+(.+)")


def parse_questions(text: str) -> list[dict]:
    """Parse raw OCR text into list of question dicts."""
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
            if PART3_Q_START <= qnum <= PART3_Q_END:
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
        elif current_q and "stem" in current_q and len(current_q["options"]) == 0:
            # continuation of stem
            current_q["stem"] += " " + line

    if current_q:
        questions.append(current_q)

    return questions


def main():
    doc = fitz.open(str(PDF_PATH))
    all_entries = []

    for test_idx in range(10):
        test_num   = test_idx + 1
        dir_page   = 1 + test_idx * 14   # 0-indexed directions page
        test_entries = []

        print(f"\n-- Test {test_num} --")
        for offset in PART3_PAGE_OFFSETS:
            page_idx = dir_page + offset
            print(f"  OCR page {page_idx + 1}...", end=" ", flush=True)

            img  = render_pdf_page(doc, page_idx)
            text = ocr_two_column(img)
            qs   = parse_questions(text)
            print(f"{len(qs)} questions found")
            test_entries.extend(qs)

        # Attach test number and audio filename
        # Part 3 audio naming: Test_01-32-34.mp3, Test_01-35-37.mp3, ...
        for q in test_entries:
            q["test"] = test_num
            # group: which conversation set (every 3 questions)
            offset_from_start = q["question"] - PART3_Q_START
            set_idx   = offset_from_start // 3
            set_first = PART3_Q_START + set_idx * 3
            set_last  = set_first + 2
            q["audio"] = f"Test_{test_num:02d}-{set_first:02d}-{set_last:02d}.mp3"

        all_entries.extend(test_entries)
        print(f"  Total Part 3 questions found for Test {test_num}: {len(test_entries)}/39")

    # Load existing if any, merge
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
