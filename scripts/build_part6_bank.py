# scripts/build_part6_bank.py
# Extract Part 6 (Text Completion) from READING.pdf
# Part 6: Q131-146 per test (4 passages x 4 questions)
# Each passage has blanks numbered 131, 132, 133, 134 (etc.)
# Layout: passage text at top, 4 questions below (A/B/C/D each)

import sys, re, json, fitz
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ocr_engine import ocr_image, render_pdf_page

PDF_PATH   = Path("../raw/ETS 2026 READING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part6.json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES_PER_TEST    = 30
PART6_Q_START     = 131
PART6_Q_END       = 146
PART6_PAGE_OFFSETS = [4, 5, 6, 7]   # after ~4 pages of Part 5

RE_QUESTION = re.compile(r"^(\d{2,3})\.\s*\(([ABCD])\)\s+(.+)")
RE_OPTION   = re.compile(r"^\(([ABCD])\)\s+(.+)")
RE_Q_NUM    = re.compile(r"^(\d{2,3})\.$")


def parse_part6_page(text: str) -> tuple[str, list[dict]]:
    """
    Returns (passage_text, [question_dicts]).
    Part 6 page: passage at top with [131] [132] placeholders, then questions below.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    passage_lines = []
    questions = []
    current_q = None
    in_questions = False

    for line in lines:
        # Detect question number line like "131." standalone
        m_standalone = RE_Q_NUM.match(line)
        if m_standalone:
            qnum = int(m_standalone.group(1))
            if PART6_Q_START <= qnum <= PART6_Q_END:
                in_questions = True
                if current_q:
                    questions.append(current_q)
                current_q = {"question": qnum, "options": {}, "answer": None}
                continue

        # Inline question like "131. (A) ..."
        m_inline = RE_QUESTION.match(line)
        if m_inline:
            qnum = int(m_inline.group(1))
            if PART6_Q_START <= qnum <= PART6_Q_END:
                in_questions = True
                if current_q:
                    questions.append(current_q)
                current_q = {"question": qnum, "options": {m_inline.group(2): m_inline.group(3).strip()}, "answer": None}
                continue

        m_opt = RE_OPTION.match(line)
        if m_opt and current_q is not None:
            current_q["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        if not in_questions:
            passage_lines.append(line)

    if current_q:
        questions.append(current_q)

    passage = " ".join(passage_lines)
    return passage, questions


def main():
    doc = fitz.open(str(PDF_PATH))
    all_entries = []

    for test_idx in range(10):
        test_num  = test_idx + 1
        base_page = test_idx * PAGES_PER_TEST
        test_entries = []
        passage_texts = {}

        print(f"\n-- Test {test_num} --")
        for offset in PART6_PAGE_OFFSETS:
            page_idx = base_page + offset
            if page_idx >= len(doc):
                break
            print(f"  OCR page {page_idx + 1}...", end=" ", flush=True)
            img  = render_pdf_page(doc, page_idx)
            text = ocr_image(img)
            passage, qs = parse_part6_page(text)
            print(f"{len(qs)} questions found")

            if qs:
                # Attach passage to first question of this page's set
                first_q = qs[0]["question"]
                for q in qs:
                    q["passage_text"] = passage if q["question"] == first_q else ""
                test_entries.extend(qs)

            if len(test_entries) >= 16:
                break

        for q in test_entries:
            q["test"] = test_num

        all_entries.extend(test_entries)
        print(f"  Total Part 6 questions for Test {test_num}: {len(test_entries)}/16")

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
