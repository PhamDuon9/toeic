# Data Architecture — TOEIC Knowledge Base

**Date:** 2026-06-25  
**Decision:** Hybrid layout — per-part JSON arrays + separate media files

---

## 1. Design Decision: One File Per Part vs. One File Per Question

### Option A: One file per question (granular)
```
question_bank/part5/t01_q101.json
question_bank/part5/t01_q102.json
...  (300 files for Part 5 alone)
```
- Pros: Easy to update individual questions, fast single-question lookup
- Cons: 2,000+ files, slow directory listing, messy git history

### Option B: One JSON array per part (chosen)
```
question_bank/part5.json   — array of 300 question objects
question_bank/part6.json   — array of 160 question objects
...
```
- Pros: Simple, fast, easy to load entirely, standard for exam prep tools
- Cons: Must rewrite whole file to update one question

**Decision: Option B (per-part arrays).** The dataset is small enough (2,000 questions) that loading an entire part into memory is trivial. Matches existing script output format.

---

## 2. Full Directory Structure

```
d:\toeic\
├── raw/                               # Immutable source data (never modified)
│   ├── ETS 2026 LISTENING.pdf
│   ├── ETS 2026 READING.pdf
│   ├── ETS 2026 TRANSCRIPT.pdf
│   └── Audio/LISTENING/Camle le/      # 578 MP3 files
│
├── extracted/                         # Marker OCR output (intermediate)
│   ├── LISTENING/
│   │   ├── ETS 2026 LISTENING.md      # Full markdown from Marker
│   │   ├── ETS 2026 LISTENING_meta.json
│   │   └── _page_*.jpeg               # All images extracted by Marker
│   ├── READING/
│   │   ├── ETS 2026 READING.md
│   │   ├── ETS 2026 READING_meta.json
│   │   └── _page_*.jpeg
│   └── TRANSCRIPT/
│       ├── ETS 2026 TRANSCRIPT.md
│       ├── ETS 2026 TRANSCRIPT_meta.json
│       └── _page_*.jpeg
│
├── question_bank/                     # THE KNOWLEDGE BASE (final output)
│   ├── part1.json                     # 60 questions (10 tests × 6)
│   ├── part2.json                     # 250 questions (10 × 25)
│   ├── part3.json                     # 390 questions (10 × 39)
│   ├── part4.json                     # 300 questions (10 × 30)
│   ├── part5.json                     # 300 questions (10 × 30)
│   ├── part6.json                     # 160 questions (10 × 16)
│   ├── part7.json                     # 540 questions (10 × 54)
│   ├── passages.json                  # All Part 6/7 passages (deduplicated)
│   ├── answer_keys.json               # Answers for all 10 tests, all 200Q
│   ├── images/
│   │   ├── part1/                     # t01_q001.jpg ... t10_q006.jpg (60 files)
│   │   └── part7/                     # Graphic aids for Part 7 passages
│   └── audio/                         # Symlinks to raw/Audio/ (no copy needed)
│       ├── part1/ → ../../raw/Audio/…
│       ├── part2/ → ../../raw/Audio/…
│       ├── part3/ → ../../raw/Audio/…
│       └── part4/ → ../../raw/Audio/…
│
├── scripts/                           # Python ETL scripts
│   ├── extract/                       # NEW — Marker-based extractors
│   │   ├── run_marker.py              # Run Marker on all 3 PDFs
│   │   ├── parse_listening.py         # Markdown → part1/2/3/4 JSON
│   │   ├── parse_reading.py           # Markdown → part5/6/7 JSON
│   │   └── parse_transcript.py        # Markdown → answer_keys + scripts
│   ├── validator/                     # NEW — data quality checks
│   │   └── validate_bank.py           # Check completeness + schema
│   ├── exporter/                      # NEW — output for web app
│   │   └── export_practice_test.py    # Generate test HTML/JSON
│   ├── ocr_engine.py                  # OLD — keep for reference, not used
│   ├── build_part1_bank.py            # OLD — superseded
│   └── build_part[2-7]_bank.py        # OLD — superseded
│
├── docs/                              # Architecture documentation
│   ├── project_analysis.md            # This analysis
│   ├── ets_format_spec.md             # PDF format details
│   ├── toeic_schema.md                # JSON schemas
│   ├── data_architecture.md           # This file
│   ├── etl_pipeline.md                # Pipeline design
│   └── ROADMAP.md                     # Project timeline
│
├── English/                           # Learning content (web app)
│   ├── DAILY_QUESTS/                  # HTML learning sessions
│   ├── WEEKLY_BOSS/                   # Weekly tests
│   ├── PART1/ through PART7/          # Lesson markdown files
│   ├── RESULTS/                       # Auto-saved quiz results (JSON)
│   └── ETS_BANK/                      # DEPRECATED — moved to question_bank/
│
├── skills/                            # AI skill CLAUDE.md files
├── REPORTS/                           # Audit reports
└── .ai-context/                       # AI handoff context
```

---

## 3. question_bank/ File Formats

### part1.json
```json
[
  {
    "id": "p1-t01-q001",
    "part": 1, "test": 1, "question": 1,
    "image": "images/part1/t01_q001.jpg",
    "audio": "audio/part1/Test_01-01.mp3",
    "answer": "C",
    "difficulty": null, "tags": []
  }
]
```

### part5.json (largest simple case)
```json
[
  {
    "id": "p5-t01-q101",
    "part": 5, "test": 1, "question": 101,
    "stem": "The board of directors _______ their decision next week.",
    "options": {"A": "announced", "B": "will announce", "C": "announces", "D": "to announce"},
    "answer": "B",
    "difficulty": null, "tags": []
  }
]
```

### passages.json
```json
[
  {
    "id": "p7-t01-p01",
    "part": 7, "test": 1, "passage_num": 1,
    "passage_type": "single",
    "question_range": [147, 151],
    "text": "POSITION AVAILABLE\n\nMarketing Coordinator...",
    "images": []
  }
]
```

### answer_keys.json
```json
{
  "1": {"1": "C", "2": "B", "3": "D", ..., "200": "A"},
  "2": {"1": "A", "2": "C", ..., "200": "B"},
  ...
  "10": {...}
}
```

---

## 4. Data Flow

```
raw/PDFs ──Marker──► extracted/*.md + *.jpeg
                           │
                           ▼
                    parse_*.py scripts
                           │
                 ┌─────────┴──────────┐
                 ▼                    ▼
         question_bank/           passages.json
         part{1-7}.json      answer_keys.json
                 │
                 ▼
         validate_bank.py
                 │
                 ▼
         English/ (web app)
         DAILY_QUESTS/
         WEEKLY_BOSS/
```

---

## 5. Index Files for Fast Lookup

### question_bank/index.json (generated, not hand-written)
```json
{
  "total_questions": 2000,
  "by_part": {"1": 60, "2": 250, "3": 390, "4": 300, "5": 300, "6": 160, "7": 540},
  "by_test": {"1": 200, "2": 200, ..., "10": 200},
  "answers_complete": false,
  "last_updated": "2026-06-25T00:00:00",
  "extraction_status": {
    "READING": "pending",
    "TRANSCRIPT": "pending",
    "LISTENING": "pending"
  }
}
```

This index lets the web app know what's available without loading all 2,000 questions.

---

## 6. Media Management

### Images (Part 1 photos)
- Source: Marker extracts `_page_N_Picture_M.jpeg` from LISTENING.pdf
- Target: `question_bank/images/part1/t{NN}_q{NNN}.jpg`
- Transform: rename only (no quality loss, no resize)
- Size estimate: ~60 images × ~100KB avg = 6MB

### Audio files
- Source: `raw/Audio/LISTENING/Camle le/` (578 MP3s, immutable)
- Strategy: Do NOT copy — store as relative paths from `question_bank/` root
- Web app serves audio directly from `raw/Audio/` directory
- Alternatively: create `question_bank/audio/` as a flat directory with symlinks

### Part 7 Graphic Aids (tables, charts, maps)
- Source: Marker extracts from READING.pdf as `_page_N_Picture_M.jpeg`
- Target: `question_bank/images/part7/t{NN}_p{passage_num}_graphic.jpg`
- Referenced in `passages.json` under `"images"` array

---

## 7. Backward Compatibility

The old `English/ETS_BANK/` output from `build_partN_bank.py` scripts will be superseded.  
Keep old files as-is during transition. Once `question_bank/` is validated, `English/ETS_BANK/` can be deprecated.

Old JSON schemas had:
- `build_part1_bank.py`: `{test, question, image}` — missing answers
- `build_part5_bank.py`: `{test, question, stem, options, answer}` — correct structure

New schemas add: `id`, `part`, `difficulty`, `tags` (plus passage fields for 6/7).

---

## 8. Estimated Storage

| Asset | Files | Est. Size |
|-------|-------|-----------|
| Part 1 images | 60 JPGs | ~6 MB |
| Part 7 graphics | ~50 images | ~5 MB |
| All question JSONs | 7 files | ~2 MB |
| passages.json | 1 file | ~3 MB |
| Audio (existing) | 578 MP3s | ~500 MB (in raw/) |
| Marker output MDs | 3 files | ~10 MB |
| Marker extracted JPEGs | ~1000 images | ~100 MB (in extracted/) |

Total new data: ~120 MB (excluding audio which already exists).
