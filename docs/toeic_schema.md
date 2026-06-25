# TOEIC Question Bank — JSON Schema Definitions

**Date:** 2026-06-25  
**Version:** 1.0  
**Purpose:** Canonical data format for all 7 TOEIC parts. All extraction scripts must conform.

---

## Design Principles

1. **Self-contained records** — each question has everything needed to render it
2. **Nullable by design** — fields can be `null` when not yet extracted (never omit)
3. **Part-specific fields** — shared base schema + part-specific extensions
4. **Immutable IDs** — `id` = `"{part}-t{test}-q{question}"` (stable across runs)
5. **Answers separate** — `answer` comes from TRANSCRIPT; initially `null`

---

## Base Question Schema (all parts)

```json
{
  "id":           "p1-t01-q001",
  "part":         1,
  "test":         1,
  "question":     1,
  "answer":       null,
  "difficulty":   null,
  "tags":         []
}
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | `"p{part}-t{NN}-q{NNN}"` — never changes |
| `part` | int | 1–7 |
| `test` | int | 1–10 |
| `question` | int | Within-test question number (1–200) |
| `answer` | string\|null | "A", "B", "C", or "D"; null until TRANSCRIPT processed |
| `difficulty` | string\|null | "easy"\|"medium"\|"hard"; set by AI tutor |
| `tags` | array | Grammar/vocab tags: `["verb_tense", "relative_clause"]` |

---

## Part 1 — Photo Description

```json
{
  "id":           "p1-t01-q001",
  "part":         1,
  "test":         1,
  "question":     1,
  "image":        "images/part1/t01_q001.jpg",
  "audio":        "audio/part1/Test_01-01.mp3",
  "answer":       null,
  "difficulty":   null,
  "tags":         []
}
```

| Field | Type | Notes |
|-------|------|-------|
| `image` | string | Relative path from `question_bank/` root |
| `audio` | string | Relative path from `question_bank/` root |

**No stem or options** — all content is audio + image.

---

## Part 2 — Question-Response

```json
{
  "id":           "p2-t01-q007",
  "part":         2,
  "test":         1,
  "question":     7,
  "audio":        "audio/part2/Test_01-07.mp3",
  "script":       null,
  "answer":       null,
  "difficulty":   null,
  "tags":         []
}
```

| Field | Type | Notes |
|-------|------|-------|
| `audio` | string | Audio file path |
| `script` | string\|null | Printed question text from TRANSCRIPT (initially null) |

**No options A/B/C/D in printed test** — three responses, all in audio.  
`script` will contain the full dialogue when TRANSCRIPT is processed.

---

## Part 3 — Conversations

```json
{
  "id":           "p3-t01-q032",
  "part":         3,
  "test":         1,
  "question":     32,
  "conversation_id": "p3-t01-c01",
  "audio":        "audio/part3/Test_01-32-34.mp3",
  "script":       null,
  "stem":         "What are the speakers discussing?",
  "options": {
    "A": "A project deadline",
    "B": "A budget report",
    "C": "A new hire",
    "D": "A client meeting"
  },
  "graphic":      null,
  "answer":       null,
  "difficulty":   null,
  "tags":         []
}
```

| Field | Type | Notes |
|-------|------|-------|
| `conversation_id` | string | Groups 3 questions per conversation |
| `audio` | string | Shared across all 3 questions in conversation |
| `script` | string\|null | Full conversation text from TRANSCRIPT |
| `stem` | string | The question (printed in test book) |
| `options` | object | Keys: "A", "B", "C", "D" |
| `graphic` | string\|null | Path to table/map image if conversation has visual aid |

---

## Part 4 — Talks

```json
{
  "id":           "p4-t01-q071",
  "part":         4,
  "test":         1,
  "question":     71,
  "talk_id":      "p4-t01-k01",
  "audio":        "audio/part4/Test_01-71-73.mp3",
  "script":       null,
  "stem":         "Who most likely is the speaker?",
  "options": {
    "A": "A tour guide",
    "B": "A news reporter",
    "C": "A company president",
    "D": "A store manager"
  },
  "graphic":      null,
  "answer":       null,
  "difficulty":   null,
  "tags":         []
}
```

Identical structure to Part 3 except `talk_id` instead of `conversation_id`.

---

## Part 5 — Incomplete Sentences

```json
{
  "id":           "p5-t01-q101",
  "part":         5,
  "test":         1,
  "question":     101,
  "stem":         "The board of directors _______ their decision next week.",
  "options": {
    "A": "announced",
    "B": "will announce",
    "C": "announces",
    "D": "to announce"
  },
  "answer":       null,
  "difficulty":   null,
  "tags":         ["verb_tense", "future"]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `stem` | string | Sentence with `_______` for blank |
| `options` | object | Keys: "A", "B", "C", "D" |

**Blank normalization:** All blank markers (`---`, `___`, `-----`) → `_______` (7 underscores).

---

## Part 6 — Text Completion

```json
{
  "id":           "p6-t01-q131",
  "part":         6,
  "test":         1,
  "question":     131,
  "passage_id":   "p6-t01-p01",
  "passage":      "To: All Staff\nFrom: HR Department\n\nEffective next month, employees [131] a new health plan...",
  "stem":         null,
  "options": {
    "A": "receive",
    "B": "will receive",
    "C": "received",
    "D": "receiving"
  },
  "answer":       null,
  "difficulty":   null,
  "tags":         ["verb_tense"]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `passage_id` | string | Groups 4 questions per passage |
| `passage` | string | Full passage text with `[131]` placeholders; only on first question of group (others empty string) |
| `stem` | null | Part 6 has no explicit question stem (the blank IS the question) |

**Passage deduplication:** Store passage text only on the FIRST question of each group (Q131, Q135, Q139, Q143). Others have `"passage": ""`.

---

## Part 7 — Reading Comprehension

```json
{
  "id":           "p7-t01-q147",
  "part":         7,
  "test":         1,
  "question":     147,
  "passage_id":   "p7-t01-p01",
  "passage_type": "single",
  "passage":      "POSITION AVAILABLE\n\nMarketing Coordinator...",
  "passage_range": [147, 151],
  "stem":         "What is being advertised?",
  "options": {
    "A": "A job opening",
    "B": "A new product",
    "C": "A rental property",
    "D": "A training course"
  },
  "answer":       null,
  "difficulty":   null,
  "tags":         ["main_idea", "business_communication"]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `passage_id` | string | Groups all questions for one passage/passage-set |
| `passage_type` | string | "single"\|"double"\|"triple" |
| `passage` | string | Full passage text; only on first question of group |
| `passage_range` | array | `[first_Q, last_Q]` in this passage group |

**Passage deduplication:** Same rule as Part 6 — passage text on first Q only.

---

## Passage Schema (separate collection)

To avoid repeating long passage text across questions, store passages separately:

```json
{
  "id":           "p7-t01-p01",
  "part":         7,
  "test":         1,
  "passage_num":  1,
  "passage_type": "single",
  "question_range": [147, 151],
  "text":         "POSITION AVAILABLE\n\nMarketing Coordinator...",
  "images":       []
}
```

Questions reference `passage_id` to look up the passage.

---

## Answer Key Schema (from TRANSCRIPT)

```json
{
  "test": 1,
  "answers": {
    "1":  "C",
    "2":  "B",
    "3":  "D",
    ...
    "200": "A"
  }
}
```

Stored in: `question_bank/answer_keys/test_{NN}.json`

---

## Merged Question (final form after answer injection)

After TRANSCRIPT processing, answers are injected into each question record:

```json
{
  "id":         "p5-t01-q101",
  "part":       5,
  "test":       1,
  "question":   101,
  "stem":       "The board of directors _______ their decision next week.",
  "options":    {"A": "announced", "B": "will announce", "C": "announces", "D": "to announce"},
  "answer":     "B",
  "difficulty": "medium",
  "tags":       ["verb_tense", "future"]
}
```

---

## Schema Validation Rules

| Rule | Check |
|------|-------|
| `id` uniqueness | No duplicate IDs across entire bank |
| `options` completeness | All 4 of A, B, C, D present (Parts 3–7) |
| `answer` validity | Must be "A", "B", "C", or "D" or null |
| `question` range | Part 1: 1–6, Part 2: 7–31, Part 3: 32–70, Part 4: 71–100, Part 5: 101–130, Part 6: 131–146, Part 7: 147–200 |
| `test` range | 1–10 |
| `image` exists | File must exist at given path (Part 1) |
| `audio` exists | File must exist at given path (Parts 1–4) |
| Passage deduplication | Only first question in group has non-empty `passage` |

---

## File Locations

```
question_bank/
├── part1/         # 60 JSON files: t01_q001.json ... t10_q006.json
├── part2/         # 250 JSON files
├── part3/         # 390 JSON files
├── part4/         # 300 JSON files
├── part5/         # 300 JSON files
├── part6/         # 160 JSON files
├── part7/         # 540 JSON files
├── passages/      # Part 6/7 passage texts (deduplicated)
├── answer_keys/   # test_01.json ... test_10.json
├── images/
│   ├── part1/     # t01_q001.jpg ... t10_q006.jpg
│   └── part7/     # graphic aids from Part 7 passages
└── audio/
    ├── part1/     # symlinks or copies from raw/Audio/
    ├── part2/
    ├── part3/
    └── part4/
```

Alternatively (simpler): one JSON file per part:  
`question_bank/part5.json` — array of all 300 questions across 10 tests.  
See `docs/data_architecture.md` for the decision.
