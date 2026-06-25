# TOEIC Knowledge Base — ROADMAP

**Goal:** Extract all 2,000 ETS 2026 questions into a structured knowledge base powering a TOEIC learning platform.

**Target learner score:** 650+  
**Current learner:** Level 2, 135 XP, Day 2

---

## Phase 0: Architecture Complete ✓ (2026-06-25)

- [x] Repository analysis (`docs/project_analysis.md`)
- [x] ETS format specification (`docs/ets_format_spec.md`)
- [x] JSON schema design (`docs/toeic_schema.md`)
- [x] Data architecture (`docs/data_architecture.md`)
- [x] ETL pipeline design (`docs/etl_pipeline.md`)
- [x] Source code: `scripts/extract/run_marker.py`
- [x] Source code: `scripts/extract/parse_reading.py`
- [x] Source code: `scripts/extract/parse_transcript.py`
- [x] Source code: `scripts/extract/parse_listening.py`
- [x] Source code: `scripts/extract/inject_answers.py`
- [x] Source code: `scripts/validator/validate_bank.py`
- [x] Source code: `scripts/exporter/export_practice_test.py`

---

## Phase 1: Extract READING — Parts 5, 6, 7 (Priority)

**Why first:** Text-only. No audio needed. Covers 50 questions/test = fastest ROI for practice.

**Steps:**
1. `python scripts/extract/run_marker.py reading` — ~4-6 hours
2. `python scripts/extract/parse_reading.py` — ~5 minutes
3. `python scripts/validator/validate_bank.py --part 5` — check output
4. Fix any parse errors (adjust regex patterns in parse_reading.py)
5. Repeat for part 6, 7

**Success criteria:**
- part5.json: 300 questions (10 tests × 30)
- part6.json: 160 questions (10 tests × 16)
- part7.json: 540 questions (10 tests × 54)
- All stems extracted, all options A/B/C/D present
- Passages properly deduplicated

**Deliverable:** Grammar Dungeon (Part 5) practice tests available in browser.

---

## Phase 2: Extract TRANSCRIPT — Answer Keys + Scripts

**Why second:** Unlocks answers for ALL 2,000 questions. Without this, practice tests can't show correct answers.

**Steps:**
1. `python scripts/extract/run_marker.py transcript` — ~3-4 hours
2. `python scripts/extract/parse_transcript.py` — parses answers + scripts
3. `python scripts/extract/inject_answers.py` — injects answers into all part JSONs
4. `python scripts/validator/validate_bank.py` — verify answer coverage

**Success criteria:**
- answer_keys.json: 10 tests × 200 answers = 2,000 total answers
- All part{1-7}.json have `"answer": "A/B/C/D"` (not null)
- Part 2/3/4 scripts injected where available

**Deliverable:** Full scored practice tests for Reading section.

---

## Phase 3: Extract LISTENING — Part 1 Images + Parts 3/4

**Why third:** Requires OCR on 142 pages + image extraction. Audio files already exist in raw/.

**Steps:**
1. `python scripts/extract/run_marker.py listening` — ~2-3 hours
2. `python scripts/extract/parse_listening.py` — extracts images + Part 3/4 text
3. `python scripts/validator/validate_bank.py --part 1` — check image paths
4. Visual inspection of Part 1 images (open a few JPGs to confirm quality)

**Success criteria:**
- question_bank/images/part1/: 60 JPEG files, visually clear
- part1.json: 60 records with image paths
- part3.json: 390 questions with stems + options
- part4.json: 300 questions with stems + options

**Deliverable:** Photo Detective (Part 1) + Conversation Investigation (Part 3) practice available.

---

## Phase 4: Validation & Quality Fixes

**After all 3 PDFs processed:**

1. `python scripts/validator/validate_bank.py` — full report
2. Review `REPORTS/validation_report.json` for errors
3. Fix missing questions (adjust page offsets or regex in parse scripts)
4. Fix OCR errors in stems (common: OCR misreads letters, splits words)
5. Re-run injections and re-validate

**Acceptance gate:** All 2,000 questions present, all have answers, validation clean.

---

## Phase 5: Web App Integration

1. Generate practice HTML for each test/part combo:
   ```
   python scripts/exporter/export_practice_test.py --test 1 --parts 5
   python scripts/exporter/export_practice_test.py --test 1 --parts 6,7
   ```
2. Create DAILY_QUESTS/day3.html incorporating Part 5 questions from question_bank
3. Create WEEKLY_BOSS/week1_boss.html (mock test from Test 1, all parts)
4. Update TOEIC_PLAN.md to reflect available content

---

## Phase 6: Adaptive Learning Layer

1. Tag questions by grammar/vocab category (verb tense, preposition, etc.)
2. Track which tags the learner gets wrong → adaptive quest generation
3. Generate targeted drills: "You missed 3/5 verb tense questions → drill verb tenses"
4. Update PLAYER_PROFILE.md with per-tag accuracy

---

## Estimated Timeline

| Phase | Action | Estimated Effort |
|-------|--------|-----------------|
| 0 | Architecture | Done (2026-06-25) |
| 1 | Extract READING | 1 evening (Marker runs unattended) |
| 2 | Extract TRANSCRIPT | 1 evening |
| 3 | Extract LISTENING | 1 evening |
| 4 | Validation fixes | 2-4 hours |
| 5 | Web app integration | 1-2 days |
| 6 | Adaptive learning | Ongoing |

---

## Quick Start Commands

```powershell
# Start READING extraction (run tonight, let it run)
cd d:\toeic
.venv-marker\Scripts\python.exe scripts\extract\run_marker.py reading

# After it finishes (check tomorrow morning)
.venv-marker\Scripts\python.exe scripts\extract\parse_reading.py
.venv-marker\Scripts\python.exe scripts\validator\validate_bank.py --part 5

# Test: generate a Part 5 practice HTML (if parsing succeeded)
python scripts\exporter\export_practice_test.py --test 1 --parts 5
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `docs/project_analysis.md` | Full repo audit |
| `docs/ets_format_spec.md` | PDF page-by-page format |
| `docs/toeic_schema.md` | JSON schema definitions |
| `docs/data_architecture.md` | Directory layout + data flow |
| `docs/etl_pipeline.md` | Pipeline design + commands |
| `scripts/extract/run_marker.py` | Run Marker OCR on PDFs |
| `scripts/extract/parse_reading.py` | Parse Parts 5/6/7 |
| `scripts/extract/parse_transcript.py` | Parse answers + scripts |
| `scripts/extract/parse_listening.py` | Parse Parts 1/3/4 + images |
| `scripts/extract/inject_answers.py` | Merge answers into JSONs |
| `scripts/validator/validate_bank.py` | QA check |
| `scripts/exporter/export_practice_test.py` | Generate HTML tests |
| `question_bank/` | Final structured output |
| `.venv-marker/` | Python 3.12 env with Marker installed |
