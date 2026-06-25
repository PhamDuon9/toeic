# TOEIC Learning Lab — Project Memory
**Last updated:** 2026-06-25

> **AI mới đọc file này trước tiên.** Sau đó đọc `.ai-context/HANDOFF.md` để có đầy đủ context và workflow.

---

## Học viên

| | |
|-|-|
| Tên | Duong — người Việt, IT professional |
| Baseline | TOEIC ~250–400 (Placement Test 6/15 = 40%) |
| Điểm mạnh | Reading comprehension · Listening intuition · Part 1 |
| Điểm yếu | Vocabulary (0/5) · Grammar (1/5) |
| Mục tiêu | TOEIC 650+ trước 2026-09-15 |
| Học | 60–90 phút/ngày |

## Trạng thái hiện tại — 2026-06-24 (Day 2)

```
Day:     2 / 84
Level:   2 (TOEIC Rookie → Word Hunter)
XP:      135 tổng (35 vào Lv 2)
Streak:  1 ngày
Score:   ~250–400 (chưa đổi)
```

- [PLAYER_PROFILE.md](English/PLAYER_PROFILE.md) — user profile chi tiết
- [english_content_index.md](.ai-context/english_content_index.md) — danh sách toàn bộ file đã tạo

---

## Kiến trúc hệ thống

```
d:\toeic\
├── CLAUDE.md                    ← project rules + skills
├── MEMORY.md                    ← file này
├── ROADMAP.md                   ← data engineering roadmap (NEW)
├── skills/toeic-{coach,examiner,rpg-gamemaster}/
├── docs/                        ← architecture docs (NEW — 2026-06-25)
│   ├── project_analysis.md
│   ├── ets_format_spec.md
│   ├── toeic_schema.md
│   ├── data_architecture.md
│   └── etl_pipeline.md
├── scripts/extract/             ← Marker-based ETL
│   ├── run_marker.py            ← runs Marker OCR on PDFs
│   ├── parse_reading.py         ← Parts 5/6/7
│   ├── parse_transcript.py      ← answer keys + scripts
│   ├── parse_listening.py       ← Parts 1/3/4 + images
│   └── inject_answers.py        ← merge answers into JSONs
├── scripts/validator/validate_bank.py  ← QA check
├── scripts/exporter/export_practice_test.py  ← HTML generator
├── question_bank/               ← KNOWLEDGE BASE (Parts 1–4 done)
│   ├── part1.json               ← 60 records, 60/60 images ✅ (Marker source)
│   ├── part2.json               ← 250 skeleton records (audio-only) ✅
│   ├── part3.json               ← 390 records, 390/390 options ✅
│   ├── part4.json               ← 300 records, 300/300 options ✅
│   ├── part5–7.json             ← chờ READING extraction
│   ├── passages.json            ← chờ READING extraction
│   ├── answer_keys.json         ← chờ TRANSCRIPT extraction
│   └── images/part1/            ← 60 JPEGs (t01_q001→t10_q006) ✅
└── English/
    ├── 6 tracking .md files
    ├── DAILY_QUESTS/            ← lab HTML + quest logs MD
    ├── RESOURCES/               ← vocab_bank.html, grammar_guide.html
    ├── PART5/                   ← 4 lesson files
    ├── RESULTS/                 ← JSON auto-save từ HTML quizzes
    └── WEEKLY_BOSS/             ← trống, cần week1_boss.html vào 2026-06-28
```

## Data Engineering Status (2026-06-25)

| PDF | Status | Output |
|-----|--------|--------|
| ETS 2026 LISTENING.pdf (142 pp) | **DONE ✅** | question_bank/part1–4.json + 60 images |
| ETS 2026 READING.pdf (~304 pp) | **CHƯA CHẠY** | extracted/READING/ (trống) |
| ETS 2026 TRANSCRIPT.pdf | **CHƯA CHẠY** | — |

**Ghi chú kỹ thuật — Part 1 images:**  
- Nguồn ảnh: `extracted/LISTENING/ETS 2026 LISTENING/_page_N_Picture_M.jpeg` (Marker output)  
- Filter: bỏ ảnh <10KB (icon trang trí), giữ ảnh thật >10KB  
- Copy vào `question_bank/images/part1/t{NN}_q{NNN}.jpg` với tên semantic  
- PyMuPDF không còn dùng (ảnh xấu, có footer text)

**Next critical action:** Restart Marker READING (4–6 giờ):  
```powershell
.venv-marker\Scripts\python.exe scripts\extract\run_marker.py reading
```  
Sau đó: `parse_reading.py` → part5/6/7.json  
Sau đó: `run_marker.py transcript` → `parse_transcript.py` → answer_keys.json → `inject_answers.py`

OCR tool: **Marker** installed in `.venv-marker/` (Python 3.12).  
Command: `.venv-marker\Scripts\python.exe scripts\extract\run_marker.py [reading|transcript|listening|all]`

---

## Workflow cộng tác

1. **User chụp ảnh sách** → AI tạo lesson `.md` + HTML drill
2. **User làm HTML** (Chrome/Edge) → kết quả tự lưu vào `English/RESULTS/*.json`
3. **User nhắn "xong"** → AI đọc JSON → cập nhật progress files
4. **User gõ "Start Day N"** → AI đọc kết quả ngày trước → tạo `dayN.html` + quest log

---

## Tech đã build (cần duy trì khi tạo HTML mới)

| Feature | Công nghệ | File |
|---------|----------|------|
| Text-to-Speech | Web Speech API · `TTS.queue()` | day1.html |
| Part 1 photos | Inline SVG (không dùng emoji) | day1.html |
| Options ẩn đến khi nghe xong | `display:none` → show sau TTS | day1.html |
| Auto-save kết quả | File System Access API + IndexedDB · object `AutoSave` | day2_grammar_lab.html |
| XP/Level/Achievement | Vanilla JS | tất cả labs |

## Design system

```css
body:    #0a0f1e   card: #111827   border: #1e2448
purple:  #7c6fff   green: #22c55e  red: #f87171  gold: #fbbf24
```

---

## Việc cần làm tiếp

- [ ] Learner làm `day2_grammar_lab.html` → AI update progress
- [ ] Learner làm `day1_bonus_pronouns.html` (+100 XP còn đó)
- [ ] Sync 20 từ Finance Set 1 → `TOEIC_VOCABULARY.md`
- [ ] Tạo `day3.html` — Passive Voice + Office Vocab (sau khi có kết quả Day 2)
- [ ] Tạo `WEEKLY_BOSS/week1_boss.html` trước 2026-06-28

---

## Đọc thêm

- [HANDOFF.md](.ai-context/HANDOFF.md) — **toàn bộ context đầy đủ cho AI mới**
- [memory_snapshot.md](.ai-context/memory_snapshot.md) — quy ước đặt tên, design system, week plan
- [english_content_index.md](.ai-context/english_content_index.md) — danh sách file và trạng thái
- [executive_summary.md](.ai-context/executive_summary.md) — tổng quan + todo list
