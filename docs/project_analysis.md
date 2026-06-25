# Project Analysis — TOEIC Knowledge Base Platform

**Date:** 2026-06-25  
**Analyst:** Senior Data Engineer + Learning Platform Architect  
**Purpose:** Full audit of existing assets, scripts, and gaps before building the ETL pipeline.

---

## 1. Repository Overview

```
d:\toeic\
├── raw/                          # Source data (PDFs + audio)
│   ├── ETS 2026 LISTENING.pdf    # Scan-only PDF, ~142 pages (14 pages × 10 tests)
│   ├── ETS 2026 READING.pdf      # Scan-only PDF, ~304 pages (30 pages × 10 tests)
│   ├── ETS 2026 TRANSCRIPT.pdf   # Scan-only PDF (answers + scripts)
│   ├── Audio/LISTENING/Camle le/ # 578 MP3 files
│   ├── ETS_BANK/part1.json       # Bad quality image mapping (no answers)
│   └── marker_test/              # Marker OCR test output (5 pages of LISTENING)
├── scripts/                      # 10 Python extraction scripts
│   ├── ocr_engine.py             # Shared OCR utility (EasyOCR + pytesseract fallback)
│   ├── build_part1_bank.py       # PyMuPDF + OpenCV contour (produces BAD images)
│   ├── build_part2_bank.py       # Skeleton generator (audio-only, no OCR needed)
│   ├── build_part3_bank.py       # EasyOCR, 2-column, LISTENING.pdf
│   ├── build_part4_bank.py       # EasyOCR, 2-column, LISTENING.pdf
│   ├── build_part5_bank.py       # EasyOCR, 2-column, READING.pdf
│   ├── build_part6_bank.py       # EasyOCR, single-column, READING.pdf
│   ├── build_part7_bank.py       # EasyOCR, single-column, READING.pdf
│   ├── crop_part1.py             # Experimental (superseded)
│   └── extract_part1.py          # Experimental (superseded)
├── skills/                       # AI skill definitions
│   ├── toeic-coach/CLAUDE.md     # Coaching methodology
│   ├── toeic-examiner/CLAUDE.md  # Evaluation & scoring
│   └── toeic-rpg-gamemaster/CLAUDE.md  # RPG gamification
├── English/                      # Learning content (HTML quests, lesson .md files)
│   ├── DAILY_QUESTS/             # day1.html, day2_grammar_lab.html
│   ├── PART5/                    # lesson_01_word_form.md, lesson_03_verb_tenses.md, etc.
│   └── ETS_BANK/                 # (empty — no JSON yet extracted)
├── docs/                         # THIS DIRECTORY — architecture docs
├── REPORTS/TOEIC_SYSTEM_ASSESSMENT.md  # Prior audit (649 lines)
└── .ai-context/HANDOFF.md        # Cross-machine AI context
```

---

## 2. Raw Data Inventory

### 2.1 PDFs (All scan-only — pdftotext returns empty)

| File | Pages (est.) | Content | Status |
|------|-------------|---------|--------|
| ETS 2026 LISTENING.pdf | ~142 pp | Parts 1–4, 10 tests | Marker tested ✓ (5 pages) |
| ETS 2026 READING.pdf | ~304 pp | Parts 5–7, 10 tests | Not yet processed |
| ETS 2026 TRANSCRIPT.pdf | unknown | Scripts + answer keys | Not yet processed |

**Critical fact:** All PDFs are scanned images. No text layer. OCR is mandatory.

### 2.2 Audio Files

- Location: `raw/Audio/LISTENING/Camle le/`
- Count: 578 MP3 files
- Naming convention (inferred from scripts):
  - Part 1: `Test_01-01.mp3` through `Test_01-06.mp3`
  - Part 2: `Test_01-07.mp3` through `Test_01-31.mp3`
  - Part 3: `Test_01-32-34.mp3` (grouped by conversation — 3 questions per file)
  - Part 4: `Test_01-71-73.mp3` (grouped by talk — 3 questions per file)
- Status: Files exist, not yet verified individually

### 2.3 Existing JSON (from previous run)

- `raw/ETS_BANK/part1.json` — 60 entries (10 tests × 6 questions), image filenames only, **NO answers**
- `English/ETS_BANK/` — **completely empty**, no JSON files exist

---

## 3. ETS 2026 Content Structure

### Questions per test (fixed ETS format)

| Part | Description | Q range (per test) | Count | Source PDF | Audio |
|------|-------------|-------------------|-------|-----------|-------|
| 1 | Photo Description | Q1–Q6 | 6 | LISTENING | Yes |
| 2 | Question-Response | Q7–Q31 | 25 | LISTENING (directions only) | Yes |
| 3 | Conversations | Q32–Q70 | 39 | LISTENING | Yes (grouped 3Q/file) |
| 4 | Talks | Q71–Q100 | 30 | LISTENING | Yes (grouped 3Q/file) |
| 5 | Incomplete Sentences | Q101–Q130 | 30 | READING | No |
| 6 | Text Completion | Q131–Q146 | 16 | READING | No |
| 7 | Reading Comprehension | Q147–Q200 | 54 | READING | No |
| **Total** | | | **200** | | |

**Scale:** 10 tests × 200 questions = **2,000 total questions**

### LISTENING.pdf page structure (per test, 0-indexed from test directions page)

```
dir_page+0  : LISTENING TEST header + Part 1 directions
dir_page+1  : Part 1 photos (Q1, Q2)
dir_page+2  : Part 1 photos (Q3, Q4)
dir_page+3  : Part 1 photos (Q5, Q6)
dir_page+4  : Part 2 directions (no questions — audio only)
dir_page+5  : Part 3 questions (2-column, Q32–Q40ish)
dir_page+6  : Part 3 questions (2-column, continued)
dir_page+7  : Part 3 questions (2-column, continued)
dir_page+8  : Part 3 questions (2-column, Q~68–Q70)
dir_page+9  : Part 4 questions (2-column, Q71–Q80ish)
dir_page+10 : Part 4 questions (2-column, continued)
dir_page+11 : Part 4 questions (2-column, Q~98–Q100)
dir_page+12 : Answer key (Test N)
dir_page+13 : Answer key continued
```

Test 1 starts at dir_page=1 (0-indexed). Each test = 14 pages.  
Formula: `dir_page = 1 + (test_num - 1) * 14`

### READING.pdf page structure (per test, 0-indexed within test block)

```
offset+0  : READING TEST header + Part 5 directions + Q101–108
offset+1  : Part 5 Q109–116 (2-column)
offset+2  : Part 5 Q117–124 (2-column)
offset+3  : Part 5 Q125–130 (2-column)
offset+4  : Part 6 passage 1 + Q131–134
offset+5  : Part 6 passage 2 + Q135–138
offset+6  : Part 6 passage 3 + Q139–142
offset+7  : Part 6 passage 4 + Q143–146
offset+8  : Part 7 starts (single passage) Q147–...
offset+9 to +29 : Part 7 continued (single/double/triple passages)
```

Each test = ~30 pages. `base_page = test_idx * 30`

---

## 4. OCR Technology Assessment

### Current: EasyOCR via ocr_engine.py

| Capability | Rating | Notes |
|-----------|--------|-------|
| Text accuracy | ~75-85% | Degrades with watermarks, scan quality |
| Two-column parsing | Built-in | `ocr_two_column()` splits image at midpoint |
| Image extraction | None | Cannot extract photos from PDF |
| Processing speed | Slow | GPU=False on this machine |
| Preprocessing | CLAHE + sharpen | Helps with contrast |

**Problems identified:**
- `build_part1_bank.py` uses OpenCV contour detection → produces bad quality crops
- EasyOCR has no mechanism to extract embedded images from PDF
- No language model — pure OCR, no contextual correction

### Better: Marker (datalab-to/marker)

| Capability | Rating | Notes |
|-----------|--------|-------|
| Text accuracy | ~95%+ | Deep learning OCR (Surya engine) |
| Structure detection | Excellent | Detects columns, sections, lists automatically |
| Image extraction | Native | Extracts pictures as separate JPEG files at original quality |
| Processing speed | ~2-3 min/page | Slower but far more accurate |
| Installation | Done | `.venv-marker/` with Python 3.12, models cached |
| Test result | Confirmed | 5-page test on LISTENING.pdf succeeded |

**Marker output for Part 1 (confirmed from test):**
```markdown
![](_page_2_Picture_2.jpeg)
![](_page_2_Picture_3.jpeg)
![](_page_2_Picture_4.jpeg)
```
→ Extracts photos as separate files, page-numbered, original quality.

**Meta.json confirms:**
- Page 2 (0-indexed): 3 Picture blocks extracted
- Page 3: 2 Picture blocks extracted  
- Extraction method: `surya` (Marker's own OCR engine)

**Verdict:** Marker is the correct tool for this project. Replace EasyOCR approach entirely.

---

## 5. Existing Scripts Analysis

### What's implemented

| Script | Method | Status | Quality |
|--------|--------|--------|---------|
| build_part1_bank.py | PyMuPDF + OpenCV contour | Ran, 60 images | BAD — redo with Marker |
| build_part2_bank.py | No OCR (skeleton) | Logic ready | OK — just needs audio mapping verification |
| build_part3_bank.py | EasyOCR 2-column | Not run | Unproven — needs Marker replacement |
| build_part4_bank.py | EasyOCR 2-column | Not run | Unproven — needs Marker replacement |
| build_part5_bank.py | EasyOCR 2-column | Not run | Has sophisticated parser (2-pass) |
| build_part6_bank.py | EasyOCR | Not run | Has passage + question parser |
| build_part7_bank.py | EasyOCR | Not run | Has passage-header detection |
| ocr_engine.py | EasyOCR + pytesseract | Shared utility | Will be replaced by Marker |

### What's missing in all scripts

1. **No answer extraction** — every script has `"answer": None`
2. **No TRANSCRIPT.pdf processing** — the source of all answers
3. **No audio file validation** — scripts assume filenames, don't check existence
4. **No deduplication logic across tests** — partial dedup only (same test+question)
5. **No validation step** — no check that all 30/39/54 questions were captured
6. **No Marker integration** — all scripts use EasyOCR

---

## 6. Skills / Game System Analysis

### toeic-coach
- Methodology: Assess → Study Plan → Daily Training → Vocabulary → Grammar → Correction
- Prioritization: Part 5 grammar is highest ROI for 650+ target
- Vocabulary topics: Business, Office, HR, Finance, Meetings, Travel, Technology, Legal, Manufacturing, Marketing

### toeic-examiner
- Scoring: Part-by-part score tracking with estimated TOEIC range
- Error categories: vocabulary, grammar, reading speed, inference, trap recognition
- Adaptive: generates more content for weak parts

### toeic-rpg-gamemaster
- XP awards: Easy=10, Medium=20, Hard=30, Perfect Streak=50, Weekly Boss=100
- Level gates: L1(0), L2(100), L3(250), L4(500), L5(1000), L6(2000), L7(4000)
- World map: Part 1=Photo Detective, Part 2=Quick Response Arena, Part 3=Conversation Investigation, Part 4=Broadcast Intelligence, Part 5=Grammar Dungeon, Part 6=Document Repair Workshop, Part 7=Corporate Intelligence Mission

### Current player state (as of Day 2)
- Level 2, 135 XP, Streak 1
- Strong: Part 1 (5/5 perfect), Vocab (4/5)
- Weak: Part 5 (7/10 — grammar gaps in verb tenses, word forms)
- Estimated TOEIC: ~400-450 (baseline)

---

## 7. Critical Gaps Summary

| Gap | Impact | Priority |
|-----|--------|----------|
| No answers for ANY question | Cannot build practice tests | CRITICAL |
| Part 1 images are bad quality | Unusable for Part 1 practice | HIGH |
| TRANSCRIPT.pdf not processed | Blocks all answers + scripts | HIGH |
| EasyOCR not yet run | No question text extracted | HIGH |
| No question_bank/ directory | No structured data storage | MEDIUM |
| No validation pipeline | Can't verify extraction quality | MEDIUM |
| Audio filenames not verified | Some may be missing/wrong | MEDIUM |
| No schema definitions | Inconsistent JSON across parts | MEDIUM |

---

## 8. Recommended Architecture Decision

**Replace EasyOCR pipeline with Marker-based pipeline.**

Rationale:
1. Marker is already installed and confirmed working
2. Marker solves Part 1 image quality (extracts at original resolution)
3. Marker handles scan quality and watermarks better (~95% vs ~75%)
4. Marker produces structured Markdown with semantic blocks
5. Parsing structured Markdown is more reliable than parsing raw OCR output

**Processing order:**
1. READING.pdf first → Parts 5, 6, 7 (text-only, fastest to validate)
2. TRANSCRIPT.pdf second → answers for all parts + scripts for Parts 2, 3, 4
3. LISTENING.pdf last → Part 1 images + confirm Parts 3/4 questions

**This order maximizes early value:** Parts 5/7 can become a practice platform before audio is needed.

---

## 9. Next Steps (feeds into subsequent docs)

- `docs/ets_format_spec.md` — Exact page-by-page format per PDF (Step 2)
- `docs/toeic_schema.md` — Canonical JSON schema for all 7 parts (Step 3)
- `docs/data_architecture.md` — question_bank/ directory layout + indexing (Step 4)
- `docs/etl_pipeline.md` — Marker-based extraction pipeline design (Step 5)
- `scripts/extract/` — New Marker-based extraction scripts replacing build_partN_bank.py (Step 6)
