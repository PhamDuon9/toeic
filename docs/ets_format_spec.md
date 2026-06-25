# ETS 2026 Format Specification

**Date:** 2026-06-25  
**Source:** Script analysis + Marker OCR test (5 pages LISTENING.pdf)  
**Status:** LISTENING confirmed; READING/TRANSCRIPT inferred from scripts

---

## 1. PDF Overview

| PDF | Pages (est.) | Encoding | Tests | Content |
|-----|-------------|----------|-------|---------|
| ETS 2026 LISTENING.pdf | ~142 | Scan (no text layer) | 10 | Parts 1–4 + answer keys |
| ETS 2026 READING.pdf | ~304 | Scan (no text layer) | 10 | Parts 5–7 |
| ETS 2026 TRANSCRIPT.pdf | ~200 (est.) | Scan (no text layer) | 10 | Scripts (Parts 2–4) + all answer keys |

All three are scanned books. `pdftotext` returns empty. OCR required.

---

## 2. LISTENING.pdf — Detailed Format

### Page structure per test
Each test occupies exactly **14 pages** (0-indexed).  
Test start formula: `dir_page = 1 + (test_num - 1) * 14`

```
Page offset  Content                        Part    Questions
-----------  -----------------------------  ------  ---------
+0           LISTENING TEST header          —       directions only
             Part 1 directions
+1           Part 1 photos                  Part 1  Q1, Q2
+2           Part 1 photos                  Part 1  Q3, Q4
+3           Part 1 photos                  Part 1  Q5, Q6
+4           Part 2 directions              Part 2  (audio only, no text)
+5           Part 3 questions (2-col)       Part 3  Q32–Q40 (est.)
+6           Part 3 questions (2-col)       Part 3  Q41–Q50 (est.)
+7           Part 3 questions (2-col)       Part 3  Q51–Q62 (est.)
+8           Part 3 questions (2-col)       Part 3  Q63–Q70
+9           Part 4 questions (2-col)       Part 4  Q71–Q80 (est.)
+10          Part 4 questions (2-col)       Part 4  Q81–Q91 (est.)
+11          Part 4 questions (2-col)       Part 4  Q92–Q100
+12          Answer key                     —       answers (visual only)
+13          Answer key continued           —       answers (visual only)
```

Total pages per test = 14. Total LISTENING.pdf pages = 1 (intro?) + 10×14 = 141.

### Part 1 — Marker output (CONFIRMED from test)

Marker extracts photos as separate JPEG files alongside the markdown.

**Confirmed file naming:** `_page_{N}_Picture_{M}.jpeg`  
where N = 1-indexed page number, M = picture index on that page (NOT sequential Q number).

**Test data (pages 1-5 of LISTENING.pdf):**

```
Page 1: _page_1_Picture_4.jpeg          → sample photo (Part 1 directions example)
Page 2: _page_2_Picture_2.jpeg          → Q1 photo candidate
        _page_2_Picture_3.jpeg          → Q2 photo candidate  
        _page_2_Picture_4.jpeg          → (possible noise/decoration)
Page 3: _page_3_Picture_1.jpeg          → Q3 photo
        _page_3_Picture_3.jpeg          → Q4 photo
Page 4: _page_4_Picture_2.jpeg          → Q5 photo
        _page_4_Picture_4.jpeg          → Q6 photo
```

**Markdown pattern for Part 1:**
```markdown
## PART 1

**Directions:** For each question...

![](_page_1_Picture_4.jpeg)

Statement (C), "They're sitting at a table," is the best description...

1.

![](_page_2_Picture_2.jpeg)

![](_page_2_Picture_3.jpeg)

![](_page_2_Picture_4.jpeg)

3.

![](_page_3_Picture_1.jpeg)
...
```

**Parsing challenge observed:** Page 2 produced 3 picture blocks but only Q1 label appears before them (Q2 label absent). This means:
- Either Q2's number didn't render (OCR failure on question number)
- Or one of the 3 pictures is decorative/noise

**Mapping strategy:** Position-based, not label-based.  
Expected: 6 photos across 3 pages (pages +1, +2, +3) = Q1-Q6.  
Sort extracted pictures by (page_num, picture_M), skip the page 1 sample photo.  
Map sequentially: photo[0]→Q1, photo[1]→Q2, ..., photo[5]→Q6.

### Part 2 — LISTENING.pdf content

Only contains: "**Directions:** You will hear a question or statement..."  
No question text printed. All content is audio.

Marker will produce:
```markdown
## PART 2

**Directions:** You will hear a question or statement...

- 7. Mark your answer on your answer sheet.
- 8. Mark your answer on your answer sheet.
...
- 31. Mark your answer on your answer sheet.
```

**Confirmed from Marker test.** No meaningful text to extract — audio files only.

### Part 3 — LISTENING.pdf content (2-column layout)

Each page uses 2-column layout. Questions follow pattern:
```
32. Who is the woman calling?
(A) A store manager
(B) A delivery service
(C) A bank employee
(D) A restaurant owner
```

Marker handles 2-column layout automatically (unlike EasyOCR which requires manual split).

**Note:** Some conversations include a GRAPHIC (table, map, floor plan) — Marker will extract these as `_page_N_Picture_M.jpeg` and reference them inline.

Audio mapping:
- Questions 32–34 → `Test_01-32-34.mp3` (3 questions per conversation)
- Questions 35–37 → `Test_01-35-37.mp3`
- Pattern: `Test_{NN}-{first_Q}-{last_Q}.mp3`

### Part 4 — LISTENING.pdf content (2-column layout)

Same structure as Part 3, Q71–Q100.  
Audio mapping: `Test_{NN}-{first_Q}-{last_Q}.mp3`

---

## 3. READING.pdf — Detailed Format

### Page structure per test
Each test occupies approximately **30 pages** (0-indexed).  
`base_page = test_idx * 30`

```
Page offset  Content                        Part    Questions
-----------  -----------------------------  ------  ---------
+0           READING TEST header            —       directions
             Part 5 directions              Part 5  Q101–108
+1           Part 5 (2-column)              Part 5  Q109–116
+2           Part 5 (2-column)              Part 5  Q117–124
+3           Part 5 (2-column)              Part 5  Q125–130
+4           Part 6 passage 1               Part 6  Q131–134
+5           Part 6 passage 2               Part 6  Q135–138
+6           Part 6 passage 3               Part 6  Q139–142
+7           Part 6 passage 4               Part 6  Q143–146
+8           Part 7 first passage           Part 7  Q147–...
+9 to +29    Part 7 continued              Part 7  ...Q200
```

Note: Some Part 7 pages span 2 pages (double/triple passages). Exact offsets vary per test.

### Part 5 — READING.pdf content (2-column)

Incomplete sentences with a blank (`-------`):
```
101. The company _______ its annual report every March.
(A) publishes
(B) publishing
(C) published
(D) to publish
```

Marker output:
```markdown
**101.** The company _______ its annual report every March.

**(A)** publishes **(B)** publishing **(C)** published **(D)** to publish
```

OR (if formatted differently):
```markdown
101. The company _______ its annual report every March.
(A) publishes
(B) publishing
(C) published
(D) to publish
```

The existing build_part5_bank.py has a sophisticated 2-pass parser for cases where OCR splits question numbers across lines — that logic should be preserved in the new parser.

### Part 6 — READING.pdf content

Format: Full passage text at top with numbered blanks `[131]`, then questions below.
```
Questions 131-134 refer to the following memo.

To: All Staff
From: HR Department
Subject: New Benefit Policy

Effective next month, employees [131] _______ a new health plan...

131. (A) receive   (B) will receive   (C) received   (D) receiving
132. (A) about     (B) with           (C) from       (D) to
```

4 passages per test, 4 questions each = 16 questions total.

### Part 7 — READING.pdf content

Most complex format: passage(s) + question set.

**Passage header format:**
```
Questions 147-151 refer to the following advertisement.
```

**Question format:**
```
147. What is being advertised?
(A) A job opening
(B) A new product
(C) A rental property
(D) A training course
```

Double passages: `Questions 176-180 refer to the following e-mail and response.`  
Triple passages: `Questions 196-200 refer to the following article, review, and e-mail.`

---

## 4. TRANSCRIPT.pdf — Format (Inferred — NOT yet processed)

### Expected content
1. **Scripts for Parts 2, 3, 4** — full printed text of all audio questions and responses
2. **Answer keys for all 10 tests** — answers for all 200 questions per test

### Expected format

**Part 2 scripts:**
```
PART 2

7. Where is the conference being held?
(A) On the third floor.
(B) In the main lobby.
(C) By the reception desk.
```

**Part 3/4 scripts:**
```
Questions 32 through 34 refer to the following conversation.

W: Have you heard back from the client about the proposal?
M: Not yet, but I'm expecting a call this afternoon.
W: I hope they approve it...

32. What are the speakers discussing?
(A) A business proposal
...
```

**Answer keys (ETS typical format):**
```
TEST 1
1. C   2. B   3. D   4. A   5. C   6. B
7. A   8. C   9. B   10. D  11. A  12. C
...
```

OR as a grid table (visual format in scanned books):
```
[Q1][C] [Q2][B] [Q3][D] ...
```

### Priority: TRANSCRIPT.pdf is the key to unlocking ALL answers.

---

## 5. Marker Output Format (Confirmed)

### Files produced per PDF run
```
output_dir/
├── {PDF_name}.md              # Full markdown content
├── {PDF_name}_meta.json       # Page stats + block counts
└── _page_{N}_Picture_{M}.jpeg # All extracted images
```

### Meta.json structure
```json
{
  "table_of_contents": [
    {"title": "LISTENING TEST", "page_id": 1, "polygon": [...]}
  ],
  "page_stats": [
    {
      "page_id": 1,
      "text_extraction_method": "surya",
      "block_counts": [["Line", 19], ["Picture", 1], ...]
    }
  ]
}
```

### Key block types from meta.json
- `Line` — text lines
- `Span` — inline spans  
- `SectionHeader` — `##` headers
- `Text` — paragraphs
- `Picture` — embedded images (extracted as JPEG)
- `PictureGroup` — grouped images
- `ListItem` — bulleted/numbered items
- `ListGroup` — list container
- `PageHeader` / `PageFooter` — page number, running title
- `Caption` — image captions

---

## 6. Known Parsing Risks

| Risk | Part | Severity | Mitigation |
|------|------|----------|-----------|
| Question number OCR failure | All | HIGH | Position-based + fallback regex |
| Option letters merged with text | All | MEDIUM | Multiple regex patterns |
| 2-column text bleeding across | 3,4,5 | MEDIUM | Marker auto-detects columns |
| Part 1 photo = decorative element | 1 | MEDIUM | Filter by image size (px) |
| Passage text mixed with questions | 6,7 | MEDIUM | Header landmark detection |
| Answer key OCR noise | TRANSCRIPT | HIGH | Row × column grid parsing |
| Blank marker varies (`---` vs `___`) | 5,6 | LOW | Normalize in parser |
| Test number watermark on every page | All | LOW | Strip non-question content |

---

## 7. Audio Filename Convention

Based on `build_part3_bank.py` and `build_part4_bank.py`:

```
Part 1:  Test_{NN}-{Q:02d}.mp3               e.g., Test_01-01.mp3
Part 2:  Test_{NN}-{Q:02d}.mp3               e.g., Test_01-07.mp3
Part 3:  Test_{NN}-{first}-{last}.mp3        e.g., Test_01-32-34.mp3  (3Q per conversation)
Part 4:  Test_{NN}-{first}-{last}.mp3        e.g., Test_01-71-73.mp3  (3Q per talk)
```

⚠️ **These are inferred from the scripts — actual file listing must be verified.**  
Run: `dir "d:\toeic\raw\Audio\LISTENING\Camle le\" /b` to get actual names.

---

## 8. Questions Requiring Verification

Before finalizing the ETL pipeline, these must be confirmed by running Marker:

1. Exact page count of READING.pdf (is it exactly 30 pages/test or variable?)
2. Actual audio filenames for Part 1 and Part 2 (individual or grouped?)
3. TRANSCRIPT.pdf page structure (does it have answer keys inside or separate?)
4. How Marker handles the 2-column layout in Parts 3/4/5 (auto-detect or needs hint?)
5. Whether Part 7 triple passages always fit in offsets +8 to +29 per test

These will be answered when Marker processes the full PDFs.
