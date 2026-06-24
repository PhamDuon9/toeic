# scripts/build_part7_bank.py
# Extract Part 7 (Reading Comprehension) from READING.pdf
# Part 7: Q147-200 per test (single/double/triple passages)
# Layout: passage(s) + questions with A/B/C/D below or beside

import sys, re, json, fitz
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ocr_engine import ocr_image, render_pdf_page

PDF_PATH   = Path("../raw/ETS 2026 READING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part7.json"
IMAGE_DIR  = OUTPUT_DIR / "images" / "part7"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES_PER_TEST    = 30
PART7_Q_START     = 147
PART7_Q_END       = 200
PART7_PAGE_OFFSETS = list(range(8, 30))  # pages 8-29 within test block

RE_QUESTION = re.compile(r"^(\d{2,3})\.\s+(.+)")
RE_OPTION   = re.compile(r"^\(([ABCD])\)\s+(.+)")
RE_PASSAGE_HEADER = re.compile(
    r"Questions?\s+(\d+)[\s\-]+(\d+)\s+refer", re.IGNORECASE
)


def parse_part7_text(text: str, page_idx: int, test_num: int) -> tuple[list[dict], list[dict]]:
    """
    Returns (passages, questions).
    passages: [{"question_range": [147, 150], "text": "..."}]
    questions: [{"question": 147, "stem": "...", "options": {...}, "answer": None, "passage_ref": 0}]
    """
    lines     = [l.strip() for l in text.splitlines() if l.strip()]
    passages  = []
    questions = []
    current_q = None
    current_passage_lines = []
    current_passage_range = None
    passage_idx = -1

    for line in lines:
        # Passage header: "Questions 147-150 refer to the following..."
        m_header = RE_PASSAGE_HEADER.match(line)
        if m_header:
            if current_passage_lines and current_passage_range:
                passages.append({
                    "range": current_passage_range,
                    "text": " ".join(current_passage_lines)
                })
                passage_idx += 1
            current_passage_range = [int(m_header.group(1)), int(m_header.group(2))]
            current_passage_lines = []
            continue

        m_q = RE_QUESTION.match(line)
        if m_q:
            qnum = int(m_q.group(1))
            if PART7_Q_START <= qnum <= PART7_Q_END:
                # Save accumulated passage text before first question
                if current_passage_lines and current_passage_range:
                    passages.append({
                        "range": current_passage_range,
                        "text": " ".join(current_passage_lines)
                    })
                    passage_idx += 1
                    current_passage_lines = []
                    current_passage_range = None

                if current_q:
                    questions.append(current_q)
                current_q = {
                    "question": qnum,
                    "stem": m_q.group(2).strip(),
                    "options": {},
                    "answer": None,
                    "passage_idx": max(0, passage_idx)
                }
                continue

        m_opt = RE_OPTION.match(line)
        if m_opt and current_q is not None:
            current_q["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        # Accumulate passage text
        if current_q is None and current_passage_range is not None:
            current_passage_lines.append(line)

    if current_q:
        questions.append(current_q)

    return passages, questions


def main():
    doc = fitz.open(str(PDF_PATH))
    all_entries = []

    for test_idx in range(10):
        test_num  = test_idx + 1
        base_page = test_idx * PAGES_PER_TEST
        test_passages  = []
        test_questions = []

        print(f"\n-- Test {test_num} --")
        for offset in PART7_PAGE_OFFSETS:
            page_idx = base_page + offset
            if page_idx >= len(doc):
                break
            print(f"  OCR page {page_idx + 1}...", end=" ", flush=True)
            img  = render_pdf_page(doc, page_idx)
            text = ocr_image(img)
            passages, qs = parse_part7_text(text, page_idx, test_num)
            print(f"{len(qs)} questions, {len(passages)} passages")
            test_passages.extend(passages)
            test_questions.extend(qs)

            if len(test_questions) >= 54:
                break

        # Build final entries — embed passage text into first question of each passage
        passage_map = {}
        for p in test_passages:
            for qnum in range(p["range"][0], p["range"][1] + 1):
                passage_map[qnum] = p["text"]

        for q in test_questions:
            q["test"] = test_num
            q_start = q["question"]
            # attach passage text to entry (full text only on first Q of a range)
            q["passage"] = passage_map.get(q_start, "")
            all_entries.append(q)

        print(f"  Total Part 7 questions for Test {test_num}: {len(test_questions)}/54")

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
