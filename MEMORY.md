# TOEIC Learning Lab — Project Memory
**Last updated:** 2026-06-25

> **AI mới đọc file này trước tiên.** Sau đó đọc `.ai-context/HANDOFF.md` để có đầy đủ context.

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

## Trạng thái hiện tại — 2026-06-25 (Day 3)

```
Day:     3 / 84
Level:   2 (TOEIC Rookie)
XP:      135 tổng (35 vào Lv 2)
Streak:  3 ngày
Score:   ~250–400 (chưa đổi)
```

---

## Hệ thống đã build — 2026-06-25 (MAJOR)

### Web App: `app/index.html` + `serve.py`
Đây là hệ thống chính, chạy tại `http://localhost:8000/app/`

| Screen | Tính năng |
|--------|-----------|
| Dashboard | XP/Level/Streak · Achievements panel · Today's Quest · Performance bars · Recommendations |
| SRS Drill | Spaced repetition (SM-2) Part 5 questions · explanation sau khi trả lời |
| Flashcards | 152 từ · 8 categories · filter buttons · TTS pronounce · Save to My Words |
| Full Tests | **Exam Mode** 🎯 — không hint/explain/word-lookup · Part 1–4 audio · Speed Mode ⚡ Part 3/4 |
| Analysis | Mistake patterns · tag/part breakdown · action plan |
| Daily Quests | 12-week plan view · quest cards · link mở lesson HTML · Achievements grid |
| **Study** (mới) | Ôn tập per-part · filter Part/Test/Tag · toggle Hint/Explanation/Auto-reveal · Show Answer button · Word Lookup bật |

### Exam Mode vs Study Mode
| | Full Tests (Exam) | Study |
|---|---|---|
| Explanation sau câu | ❌ | ✅ toggle |
| Hint grammar | ❌ | ✅ toggle |
| Word Lookup | ❌ tắt | ✅ bật |
| Reveal đáp án | ❌ | ✅ nút Show Answer |
| Kết quả | Submit xong | Ngay lập tức |
| Mistakes ghi | ✅ âm thầm | ✅ ngay |

### Word Lookup (double-click bất kỳ từ — trừ Exam Mode)
- Check vocab.json local → Free Dictionary API (definition) + MyMemory API (Vietnamese) — chạy song song
- Word Family map (40+ TOEIC stems) — noun/verb/adj/adv forms
- Save to My Words (localStorage) · TTS Pronounce · Esc để đóng

### Question Bank
```
question_bank/
├── part1.json       ← 60 records ✅ audio paths fixed
├── part2.json       ← 250 records ✅ audio paths fixed
├── part3.json       ← 390 records ✅ audio paths fixed
├── part4.json       ← 300 records ✅ audio paths fixed
├── part5_mock.json  ← 19 records ✅ với explanation đầy đủ
├── vocab.json       ← 152 từ · 8 categories ✅
├── part5.json       ← chờ READING OCR
├── part6.json       ← chờ READING OCR
├── part7.json       ← chờ READING OCR
└── answer_keys.json ← chờ TRANSCRIPT OCR
```

Audio path format: `raw/Audio/LISTENING/Cau_le/Test_XX/Test_XX-NN.mp3`

### LocalStorage keys (app)
| Key | Nội dung |
|-----|---------|
| `toeic_stats` | xp, level, streak, lastStudied, partStats |
| `toeic_srs2` | SM-2 state per question (ef, interval, reps, due) |
| `toeic_mistakes2` | array mistakes {id, date, part, stem, chosen, correct, tags, explanation} |
| `toeic_vocab_state` | {word: {known, seen}} |
| `toeic_mywords` | custom saved words từ Word Lookup |
| `toeic_seeded_v1` | flag đã seed legacy data (chạy 1 lần) |

### Seed data (auto-inject lần đầu)
- Stats: Level 2, 135 XP, streak 3
- 9 mistakes từ Placement Test (pt-q1 → pt-q9)

---

## OCR Status (2026-06-25)

| PDF | Status | Ghi chú |
|-----|--------|---------|
| ETS 2026 LISTENING.pdf | **DONE ✅** | part1–4.json + 60 images |
| ETS 2026 TRANSCRIPT.pdf | **ĐANG CHẠY** ⏳ | Process marker_single PID 32064 · start 11:01 sáng |
| ETS 2026 READING.pdf | **ĐANG CHẠY trên máy khác** ⏳ | Khi xong copy về |

**Khi TRANSCRIPT xong** → folder `extracted/TRANSCRIPT/` có file `.md` → chạy:
```powershell
.venv-marker\Scripts\python.exe scripts\extract\parse_transcript.py
.venv-marker\Scripts\python.exe scripts\extract\inject_answers.py
.venv-marker\Scripts\python.exe scripts\validator\validate_bank.py
```

**Khi READING về từ máy kia** → chạy:
```powershell
.venv-marker\Scripts\python.exe scripts\extract\parse_reading.py
# → part5.json, part6.json, part7.json, passages.json
```

---

## Kiến trúc thư mục

```
d:\duongpt\TOEIC\
├── CLAUDE.md                    ← project rules
├── MEMORY.md                    ← file này
├── ROADMAP.md                   ← data engineering roadmap
├── serve.py                     ← python -m http.server wrapper
├── app/index.html               ← WEB APP chính (single file SPA)
├── question_bank/               ← JSON data
├── raw/Audio/LISTENING/         ← MP3 files ETS 2026
├── extracted/                   ← Marker OCR output
├── scripts/                     ← ETL pipeline Python
├── docs/                        ← architecture docs
├── skills/                      ← toeic-coach, examiner, rpg-gamemaster
└── English/
    ├── PLAYER_PROFILE.md
    ├── TOEIC_PLAN.md            ← 12-week roadmap
    ├── TOEIC_PROGRESS.md
    ├── TOEIC_MISTAKES.md        ← 9 lỗi placement test logged
    ├── TOEIC_VOCABULARY.md
    ├── TOEIC_ACHIEVEMENTS.md
    ├── DAILY_QUESTS/            ← day1.html ✅ · day2_grammar_lab.html ✅
    ├── RESOURCES/               ← vocab_bank.html · grammar_guide.html
    ├── PART5/                   ← 4 lesson files
    └── WEEKLY_BOSS/             ← cần week1_boss.html trước 2026-06-28
```

---

## Việc cần làm — theo thứ tự ưu tiên

### Ngay (Day 3 — 2026-06-25)
- [ ] Tạo `day3.html` — Passive Voice + Logistics Vocab
- [ ] Learner làm `day2_grammar_lab.html` nếu chưa xong

### Ngắn hạn
- [ ] TRANSCRIPT xong → parse → inject answers vào part1–4.json
- [ ] READING về → parse → part5/6/7.json
- [ ] Viết tag-based explanation templates cho Part 5 (không cần API)
- [ ] `WEEKLY_BOSS/week1_boss.html` trước 2026-06-28

### Trung hạn (app improvements)
- [ ] "My Words" screen — hiện danh sách từ đã save từ Word Lookup
- [ ] Part 5/6/7 từ ETS thực (sau khi có OCR data)
- [ ] Transcript viewer cho Part 3/4 (sau khi inject answers)
- [ ] Export mistakes → PDF/CSV để ôn offline

---

## Design system (dùng nhất quán trong mọi HTML)

```css
bg: #0a0f1e  card: #111827  card2: #161d30  border: #1e2448
purple: #7c6fff  green: #22c55e  red: #f87171  gold: #fbbf24  blue: #38bdf8
text: #e2e8f0  muted: #64748b
font: 'Segoe UI', sans-serif
```

## Đọc thêm
- [HANDOFF.md](.ai-context/HANDOFF.md) — full context cho AI mới
- [english_content_index.md](.ai-context/english_content_index.md) — danh sách files
