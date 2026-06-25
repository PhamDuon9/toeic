# ETL Pipeline Design — TOEIC Knowledge Base

**Date:** 2026-06-25  
**Tool:** Marker (datalab-to/marker) via `.venv-marker/` (Python 3.12)  
**Replaces:** EasyOCR-based `build_partN_bank.py` scripts

---

## Pipeline Overview

```
EXTRACT        │  TRANSFORM       │  LOAD
───────────────┼──────────────────┼──────────────────
Marker OCR     │  Parse Markdown  │  Write JSON
(PDF → MD)     │  (MD → dict)     │  (dict → files)
               │  Inject answers  │  Validate schema
               │  Map media       │  Build index
```

**3 phases, 3 scripts, run in order:**

```
scripts/extract/run_marker.py          # Phase 1: Extract (OCR)
scripts/extract/parse_all.py           # Phase 2: Transform (Parse)
scripts/validator/validate_bank.py     # Phase 3: Validate (QA)
```

---

## Phase 1: Extract (Marker OCR)

### Script: `scripts/extract/run_marker.py`

**What it does:**
1. Activates `.venv-marker/` environment
2. Runs Marker on all 3 PDFs sequentially (READING → TRANSCRIPT → LISTENING)
3. Outputs to `extracted/READING/`, `extracted/TRANSCRIPT/`, `extracted/LISTENING/`

**Why READING first:**
- Fastest to validate (no audio, text-only)
- Can build Part 5 practice tool immediately
- 304 pages but all text — Marker handles well

**Why TRANSCRIPT second:**
- Unlocks ALL answers
- Scripts for Parts 2/3/4
- Must process before LISTENING validation

**Why LISTENING last:**
- Part 1 images only (OCR on text confirms what scripts already have)
- Can run while working on READING/TRANSCRIPT data

### Marker command (per PDF)
```bash
.venv-marker\Scripts\python.exe -m marker.convert \
    "d:\toeic\raw\ETS 2026 READING.pdf" \
    "d:\toeic\extracted\READING" \
    --workers 1 \
    --output_format markdown
```

### Estimated time
| PDF | Pages | Estimated time |
|-----|-------|---------------|
| READING.pdf | ~304 | 4–6 hours |
| TRANSCRIPT.pdf | ~200 (est.) | 3–4 hours |
| LISTENING.pdf | ~142 | 2–3 hours |

Run overnight. Each PDF is independent — can run in separate terminal windows if RAM allows (each Marker instance needs ~4GB).

### Output validation
After each run, check:
```bash
# File exists and has content
dir "d:\toeic\extracted\READING\ETS 2026 READING.md"
# Image count (should be > 0 for LISTENING)
dir "d:\toeic\extracted\LISTENING\_page_*.jpeg" | find /c "jpeg"
```

---

## Phase 2: Transform (Parse)

### Script set: `scripts/extract/parse_*.py`

#### 2A. `parse_reading.py` — READING.pdf → Parts 5, 6, 7

**Algorithm:**

```python
# 1. Load extracted/READING/ETS 2026 READING.md
# 2. Split by test: look for "READING TEST" or "TEST {N}" headers
# 3. For each test:
#    a. Find "PART 5" section → extract Q101-130
#    b. Find "PART 6" section → extract passages + Q131-146
#    c. Find "PART 7" section → extract passages + Q147-200
# 4. For each question: build dict per toeic_schema.md
# 5. Save: question_bank/part5.json, part6.json, part7.json, passages.json
```

**Part 5 parser (most complex — adapted from build_part5_bank.py):**
```python
RE_QNUM    = re.compile(r"^\*{0,2}(\d{3})\.\*{0,2}\s*(.*)") 
RE_OPTION  = re.compile(r"^\({0,1}\*{0,2}([ABCD])\*{0,2}\){0,1}\s+(.+)")
RE_BLANK   = re.compile(r"[-_]{4,}")
```

Marker wraps bold text in `**` — regex must handle both plain and bold formats.

**Part 6 passage detection:**
```python
RE_P6_RANGE = re.compile(r"Questions?\s+(\d+)[\s\-–]+(\d+)\s+refer")
```

**Part 7 passage type detection:**
```python
if "e-mail and" in header_line.lower() or "letter and" in header_line.lower():
    passage_type = "double"
elif header_line.count("and") >= 2:
    passage_type = "triple"
else:
    passage_type = "single"
```

#### 2B. `parse_transcript.py` — TRANSCRIPT.pdf → answers + scripts

**Algorithm:**
```python
# 1. Load extracted/TRANSCRIPT/ETS 2026 TRANSCRIPT.md
# 2. Find answer key section (look for grid of letters: "1 C  2 B  3 D ...")
#    OR look for "ANSWER KEY" / "ANSWERS" header
# 3. Parse answer grid → answer_keys.json
# 4. Find script sections (Part 2, 3, 4)
# 5. Match scripts to question numbers → inject into part2/3/4.json
```

**Answer key detection (2 possible formats):**

Format A (list):
```
1. C    2. B    3. D    4. A    5. C
```
```python
RE_ANSWER_LIST = re.compile(r"(\d+)\.\s+([ABCD])")
```

Format B (grid table from OCR — Marker may produce markdown table):
```markdown
| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | C | 2 | B | 3 | D |
```
```python
# Parse markdown table: extract Q and A columns
```

**Script injection (Part 3/4):**
```python
# Match "Questions 32 through 34" header → assign to conversation_id
# Extract W:/M:/Narrator: lines as script text
# Join into part3[q]["script"] for all 3 questions in set
```

#### 2C. `parse_listening.py` — LISTENING.pdf → Parts 1, 3, 4 + images

**Algorithm:**
```python
# 1. Load extracted/LISTENING/ETS 2026 LISTENING.md
# 2. Part 1: find all ![](_page_*.jpeg) references per test
#    Map to question numbers: skip page 1 sample, assign Q1-Q6 per test
# 3. Copy/rename: _page_N_Picture_M.jpeg → question_bank/images/part1/t{NN}_q{NNN}.jpg
# 4. Part 3/4: extract question stems + options (confirm against parse_transcript output)
# 5. Merge audio filenames into part3.json, part4.json
```

**Part 1 image mapping:**
```python
# Page 1 (test 1, index 1): skip (sample image)
# Pages 2, 3, 4 (test 1): extract images in order
# Each page has 2 real photos + possibly 1 noise element
# Sort by (page_num, picture_index), filter by file size > 10KB
# Assign: img[0]→Q1, img[1]→Q2, img[2]→Q3, img[3]→Q4, img[4]→Q5, img[5]→Q6
```

#### 2D. `inject_answers.py` — merge answers into all part JSONs

```python
# Run AFTER parse_transcript.py produces answer_keys.json
# For each part{N}.json: load → fill q["answer"] from answer_keys.json → save
```

---

## Phase 3: Validate

### Script: `scripts/validator/validate_bank.py`

**Checks performed:**

```python
def validate():
    results = {}
    
    # 1. Question count
    for part in [1, 2, 3, 4, 5, 6, 7]:
        expected = {1:60, 2:250, 3:390, 4:300, 5:300, 6:160, 7:540}[part]
        actual = len(load_part(part))
        results[f"part{part}_count"] = (actual == expected, f"{actual}/{expected}")
    
    # 2. No duplicate IDs
    all_ids = [q["id"] for q in all_questions()]
    results["unique_ids"] = (len(all_ids) == len(set(all_ids)))
    
    # 3. Options completeness (Parts 3-7)
    for q in all_questions():
        if q["part"] >= 3:
            missing = set("ABCD") - set(q["options"].keys())
            if missing:
                flag(q["id"], f"missing options: {missing}")
    
    # 4. Answers present
    answered = sum(1 for q in all_questions() if q["answer"] is not None)
    results["answers_complete"] = (answered == 2000, f"{answered}/2000")
    
    # 5. Media files exist
    for q in all_questions():
        if q["part"] == 1:
            check_file(q["image"], q["audio"])
        elif q["part"] <= 4:
            check_file(q["audio"])
    
    return results
```

**Output:** `REPORTS/validation_report.json` + terminal summary.

---

## Phase 4: Export (feeds web app)

### Script: `scripts/exporter/export_practice_test.py`

Generates a complete practice test HTML from question_bank/ data:

```python
# Args: --test 1 --parts 5,6,7 --output English/DAILY_QUESTS/test1_reading.html
# Reads: question_bank/part5.json, part6.json, part7.json, passages.json
# Outputs: self-contained HTML with embedded questions + answer checker
```

---

## Running the Pipeline

### Prerequisites
```powershell
# Verify Marker is installed
d:\toeic\.venv-marker\Scripts\python.exe -c "import marker; print('OK')"

# Check available disk space (need ~10GB for extracted output)
Get-PSDrive D
```

### Step-by-step execution
```powershell
# STEP 1a: Extract READING (run overnight — 4-6 hours)
cd d:\toeic
.venv-marker\Scripts\python.exe -m marker.convert `
    "raw\ETS 2026 READING.pdf" `
    "extracted\READING" `
    --workers 1

# STEP 1b: Extract TRANSCRIPT (3-4 hours)
.venv-marker\Scripts\python.exe -m marker.convert `
    "raw\ETS 2026 TRANSCRIPT.pdf" `
    "extracted\TRANSCRIPT" `
    --workers 1

# STEP 1c: Extract LISTENING (2-3 hours)
.venv-marker\Scripts\python.exe -m marker.convert `
    "raw\ETS 2026 LISTENING.pdf" `
    "extracted\LISTENING" `
    --workers 1

# STEP 2: Parse (run after each PDF completes)
.venv-marker\Scripts\python.exe scripts\extract\parse_reading.py
.venv-marker\Scripts\python.exe scripts\extract\parse_transcript.py
.venv-marker\Scripts\python.exe scripts\extract\parse_listening.py
.venv-marker\Scripts\python.exe scripts\extract\inject_answers.py

# STEP 3: Validate
.venv-marker\Scripts\python.exe scripts\validator\validate_bank.py
```

---

## Error Handling Strategy

| Error type | Detection | Recovery |
|-----------|-----------|---------|
| OCR failure on question number | Regex no match | Position-based fallback (question N = offset N from section start) |
| Missing option D | Validate step flags | Manual fill or skip question |
| Duplicate question ID | Validate step flags | Deduplicate by keeping last occurrence |
| Part boundary detection failure | Wrong question count | Manual page offset override in parse script |
| Image noise in Part 1 | File size < 10KB | Skip small images |
| Answer key OCR error | Letter not in ABCD | Flag for manual review |

All parser errors logged to `REPORTS/parse_errors_{part}.log`.

---

## Incremental Update Strategy

The pipeline is designed to be re-runnable:
- Phase 1 (Marker): Only re-run if source PDF changes (slow)
- Phase 2 (parse): Re-run any time; overwrites output files
- Phase 3 (validate): Always re-run after Phase 2
- Phase 4 (export): Re-run to regenerate web content

For partial re-runs (e.g., only fixing Part 5 parser):
```powershell
python scripts\extract\parse_reading.py --part 5
python scripts\extract\inject_answers.py --part 5
python scripts\validator\validate_bank.py --part 5
```
