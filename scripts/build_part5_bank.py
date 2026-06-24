# scripts/build_part5_bank.py
# Extract Part 5 (Incomplete Sentences) from READING.pdf
# Part 5: Q101-130 per test (30 questions, 2-column layout)
# READING.pdf: 304 pages, 10 tests, ~30 pages/test
# Test 1 starts at PDF page 1 (0-indexed: 0)

import sys, re, json, fitz
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ocr_engine import ocr_two_column, render_pdf_page

PDF_PATH   = Path("../raw/ETS 2026 READING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part5.json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# READING.pdf structure per test (~30 pages per test, 304 total / 10 = 30.4)
# Page 1 (idx 0): READING TEST directions + PART 5 directions + Q101-108
# Page 2 (idx 1): Q109-116 (continues)
# Pages after Part 5: Part 6 starts around Q131
PAGES_PER_TEST = 30   # approximate
PART5_Q_START  = 101
PART5_Q_END    = 130

# Part 5 occupies ~3-4 pages per test (8 questions/page in 2-column)
PART5_PAGE_OFFSETS = [0, 1, 2, 3]

RE_QNUM   = re.compile(r"^(\d{2,3})[.\:]?\s*$")        # standalone "101." or "101"
RE_QINLINE= re.compile(r"^(\d{2,3})[.\:]\s+(.+)")      # "101. stem text"
RE_OPTION  = re.compile(r"^\(([ABCD])\)\s+(.+)")
RE_BLANK   = re.compile(r"-{4,}")
SKIP_WORDS = {
    "READING TEST", "PART 5", "PART5", "Directions", "GO ON TO THE NEXT PAGE",
    "LISTENING TEST", "PART 3", "PART 4", "TEST 1", "TEST 2", "TEST 3",
    "In the Reading test", "You must mark", "You are encour",
    "answer sheet", "test book", "mark the letter",
}
# Patterns that indicate directions/noise text in a stem
NOISE_PATTERNS = re.compile(
    r"(you will read|reading test|answer sheet|mark the letter|mark your answer"
    r"|directions:|Select the best|four answer choices|word or phrase is missing"
    r"|time allowed|comprehension questions|within the time)",
    re.IGNORECASE
)


def is_noise(line: str) -> bool:
    if len(line) < 3:
        return True
    if any(s.lower() in line.lower() for s in SKIP_WORDS):
        return True
    return False


def clean_stem(stem: str) -> str:
    """Remove directions text that leaked into a stem."""
    # Split on any sentence that looks like directions noise
    parts = re.split(r"\.\s+", stem)
    clean = [p for p in parts if not NOISE_PATTERNS.search(p)]
    result = ". ".join(clean).strip()
    # Trim any leading noise before the actual question sentence
    # (heuristic: real stems are < 200 chars and don't start with lowercase)
    if len(result) > 300:
        # Try to find where the real sentence starts
        m = re.search(r"[A-Z][^.]{10,}", result)
        if m:
            result = result[m.start():]
    return result.strip()


def parse_questions(text: str) -> list[dict]:
    """
    Two-pass parser to handle EasyOCR output where question number
    appears on its own line, separate from the stem text.

    Pattern observed:
        "The lecture will take place..."   ← stem start (before number!)
        "101."                             ← question number
        "which attendees may ask..."       ← stem continuation
        "(A) across"
        "(B) after"
        ...
    """
    lines = [l.strip() for l in text.splitlines() if l.strip() and not is_noise(l.strip())]

    # Pass 1: tag each line
    tagged = []   # (tag, value) where tag in: "qnum", "qinline", "option", "text"
    for line in lines:
        m_num    = RE_QNUM.match(line)
        m_inline = RE_QINLINE.match(line)
        m_opt    = RE_OPTION.match(line)
        if m_num:
            tagged.append(("qnum", int(m_num.group(1))))
        elif m_inline:
            tagged.append(("qinline", (int(m_inline.group(1)), m_inline.group(2).strip())))
        elif m_opt:
            tagged.append(("option", (m_opt.group(1), m_opt.group(2).strip())))
        else:
            tagged.append(("text", line))

    # Pass 2: group into questions
    questions    = []
    current_q    = None
    pending_text = []   # text lines seen before a qnum

    def save_q():
        if current_q and len(current_q["options"]) == 4:
            questions.append(current_q)
        elif current_q:
            questions.append(current_q)  # save even if incomplete

    for tag, val in tagged:
        if tag == "qnum":
            qnum = val
            if PART5_Q_START <= qnum <= PART5_Q_END:
                save_q()
                # pending_text accumulated before this number = start of stem
                stem_start = " ".join(pending_text)
                current_q = {
                    "question": qnum,
                    "stem": RE_BLANK.sub("_______", stem_start),
                    "options": {},
                    "answer": None
                }
            pending_text = []

        elif tag == "qinline":
            qnum, stem_text = val
            if PART5_Q_START <= qnum <= PART5_Q_END:
                save_q()
                pending_text = []
                current_q = {
                    "question": qnum,
                    "stem": RE_BLANK.sub("_______", stem_text),
                    "options": {},
                    "answer": None
                }

        elif tag == "option":
            letter, opt_text = val
            if current_q is not None:
                current_q["options"][letter] = opt_text
            pending_text = []

        elif tag == "text":
            if current_q is not None and len(current_q["options"]) == 0:
                # still building stem
                current_q["stem"] = (current_q["stem"] + " " + RE_BLANK.sub("_______", val)).strip()
            else:
                pending_text.append(val)

    save_q()
    # Clean up stems
    for q in questions:
        q["stem"] = clean_stem(q["stem"])
    return questions


def main():
    doc = fitz.open(str(PDF_PATH))
    all_entries = []

    for test_idx in range(10):
        test_num  = test_idx + 1
        base_page = test_idx * PAGES_PER_TEST
        test_entries = []

        print(f"\n-- Test {test_num} (base PDF page {base_page + 1}) --")
        for offset in PART5_PAGE_OFFSETS:
            page_idx = base_page + offset
            if page_idx >= len(doc):
                break
            print(f"  OCR page {page_idx + 1}...", end=" ", flush=True)
            img  = render_pdf_page(doc, page_idx)
            text = ocr_two_column(img)
            qs   = parse_questions(text)
            print(f"{len(qs)} questions found")
            test_entries.extend(qs)

            # Stop early once we have all 30 Part 5 questions
            if len(test_entries) >= 30:
                break

        for q in test_entries:
            q["test"] = test_num

        all_entries.extend(test_entries)
        print(f"  Total Part 5 questions for Test {test_num}: {len(test_entries)}/30")

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
