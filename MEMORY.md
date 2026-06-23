# TOEIC Learning Lab — Project Memory

> Đây là file ngữ cảnh dự án. Khi mở project trên máy mới, Claude Code đọc file này để hiểu toàn bộ hệ thống và tiếp tục làm việc đúng hướng.

---

## Mục tiêu dự án

Giúp học viên người Việt đạt **TOEIC L&R 650+** từ mức baseline ~300 điểm trong **12 tuần**, học 60–90 phút/ngày.

---

## Học viên

| Thông tin | Chi tiết |
|-----------|----------|
| Tên | Duong |
| Tiếng mẹ đẻ | Tiếng Việt |
| Nghề nghiệp | IT |
| Baseline TOEIC | ~250–400 (Placement Test: 6/15) |
| Điểm mạnh | Reading comprehension, Listening intuition |
| Điểm yếu | Vocabulary (0/5), Grammar (1/5) |
| Target | TOEIC 650+ |
| Timeline | 12 tuần từ 2026-06-23 đến 2026-09-15 |
| Loại thi | TOEIC Listening & Reading (200 câu, 990 điểm) |

---

## Kiến trúc hệ thống

```
TOEIC/
├── CLAUDE.md                  ← System instruction (skills, workflow)
├── MEMORY.md                  ← File này — ngữ cảnh dự án
├── skills/
│   ├── toeic-coach/           ← Role: dạy, lập plan, giải thích
│   ├── toeic-examiner/        ← Role: đánh giá khách quan kiểu ETS
│   └── toeic-rpg-gamemaster/  ← Role: gamification (XP, Level, Quest)
└── English/
    ├── PLAYER_PROFILE.md      ← Hồ sơ học viên (Level, XP, stats)
    ├── TOEIC_PLAN.md          ← 12-week roadmap
    ├── TOEIC_PROGRESS.md      ← Lịch sử điểm số
    ├── TOEIC_MISTAKES.md      ← Log lỗi sai có phân tích
    ├── TOEIC_VOCABULARY.md    ← Tracker từ vựng đã học
    ├── TOEIC_ACHIEVEMENTS.md  ← Badge hệ thống
    ├── placement_test.html    ← Bài test đầu vào (interactive)
    ├── DAILY_QUESTS/          ← Lesson hàng ngày (HTML interactive)
    │   ├── DAY1_2026-06-23.md ← Quest log Day 1
    │   └── day1.html          ← Lab Day 1 (Vocab + Grammar + Part 1 + Part 5)
    ├── WEEKLY_BOSS/           ← Mini test cuối tuần
    ├── PART1/ → PART7/        ← Lesson theo từng phần thi
    │   └── PART5/lesson_01_word_form.md
    └── RESOURCES/
        ├── vocab_bank.html    ← Kho 120+ từ vựng TOEIC có search/filter/tracker
        └── grammar_guide.html ← 8 grammar rules cho Part 5 & 6
```

---

## Những gì đã làm (tính đến 2026-06-23)

### 1. Placement Test
- Tạo `placement_test.html` — interactive lab 15 câu (Vocab, Grammar, Reading, Listening)
- Kết quả: Vocab 0/5, Grammar 1/5, Reading 3/3, Listening 2/2
- Estimated TOEIC: 250–400

### 2. Tracking Files
- `PLAYER_PROFILE.md` — đã điền đầy đủ baseline, milestones, weak/strong areas
- `TOEIC_PROGRESS.md` — đã ghi nhận kết quả placement test
- `TOEIC_MISTAKES.md` — đã phân tích 9 lỗi sai từ placement test
- `TOEIC_VOCABULARY.md` — đã seed 9 từ ban đầu từ placement test
- `TOEIC_PLAN.md` — đã tạo 12-week roadmap + Week 1 detailed plan

### 3. Day 1 Lab
- `DAILY_QUESTS/day1.html` — full interactive RPG-style lab gồm:
  - Quest 1: Vocab flashcards 20 từ Finance + quiz 5 câu
  - Quest 2: Grammar Lesson — Word Form strategy
  - Quest 3: Part 1 Photo Detective 5 câu
  - Quest 4: Part 5 Word Form Drill 10 câu
  - Hệ thống XP + Level + Achievement
- `DAILY_QUESTS/DAY1_2026-06-23.md` — quest log

### 4. Resources
- `RESOURCES/vocab_bank.html` — 120+ từ vựng TOEIC, 8 chủ đề, search + filter + status tracker (lưu localStorage)
- `RESOURCES/grammar_guide.html` — 8 grammar rules, có bảng + ví dụ + TOEIC Traps

---

## Hướng đi tiếp theo

### Ngắn hạn (Week 1)
- [ ] Học viên hoàn thành Day 1 → gửi kết quả
- [ ] Tạo `day2.html` dựa trên kết quả Day 1 (adapt theo điểm yếu)
- [ ] Mỗi ngày: 1 HTML lab trong `DAILY_QUESTS/`
- [ ] Cuối tuần (Day 6): `WEEKLY_BOSS/week1_boss.html` — mini test tổng hợp

### Trung hạn (Week 1–4)
- Tập trung: Vocabulary + Grammar (Part 5)
- Mỗi tuần: 100 từ mới + 1 grammar topic
- Week 2: Office & Meetings + Verb Tense
- Week 3: Finance deep dive + Passive Voice
- Week 4: HR vocabulary + Subject-Verb Agreement

### Dài hạn (Week 5–12)
- Week 5–8: Build Part 3, 4, 6, 7 skills
- Week 9–10: Full mock test simulation
- Week 11–12: Score optimization + test strategy

---

## Cách tạo Daily Quest (workflow chuẩn)

Khi học viên gõ **"Start Day N"**:

1. Đọc kết quả ngày hôm trước từ `DAILY_QUESTS/DAYN-1_*.md`
2. Kiểm tra `TOEIC_MISTAKES.md` để xác định điểm yếu hiện tại
3. Tạo `DAILY_QUESTS/dayN.html` — interactive lab gồm 4 quests:
   - Quest 1: Vocabulary (20 từ mới theo chủ đề tuần đó)
   - Quest 2: Grammar Lesson (topic của tuần)
   - Quest 3: Listening Part (Part 1–4 luân phiên)
   - Quest 4: Reading/Grammar Drill (Part 5–7)
4. Tạo `DAILY_QUESTS/DAYN_YYYY-MM-DD.md` — quest log
5. Cập nhật `PLAYER_PROFILE.md` sau khi học viên submit kết quả

---

## Quy tắc thiết kế Lab (HTML)

- Dark theme: background `#0a0f1e`, accent `#38bdf8` (blue), `#a78bfa` (purple), `#f59e0b` (gold)
- Mỗi câu hỏi: click chọn → submit → hiển thị đáp án + giải thích tiếng Việt
- Giải thích phải có: ✅ Correct answer + lý do + TOEIC trap (nếu có)
- XP system: Easy +10, Medium +20, Hard +30, Perfect streak +50
- Liên kết đến `../RESOURCES/vocab_bank.html` và `../RESOURCES/grammar_guide.html`

---

## Nguyên tắc coaching

1. **Dạy TOEIC, không dạy tiếng Anh tổng quát** — mọi bài học phải cải thiện điểm thi
2. **Vocabulary first** — đây là gap lớn nhất hiện tại
3. **Không reveal đáp án trước** — để học viên suy nghĩ
4. **Giải thích bằng tiếng Việt** — học viên là người Việt, giải thích ngắn gọn bằng TV giúp hiểu nhanh hơn
5. **Adapt dựa trên kết quả** — nếu học viên sai nhiều Part 5, tăng Part 5 content ngày hôm sau
6. **RPG mechanics** — XP, Level, Achievement giữ motivation

---

## XP & Level System

| Level | XP cần | Tên |
|-------|--------|-----|
| 1 | 0 | TOEIC Rookie |
| 2 | 100 | Word Hunter |
| 3 | 250 | Grammar Warrior |
| 4 | 500 | Part 5 Slayer |
| 5 | 1000 | TOEIC Explorer |
| 6 | 2000 | Business English Pro |
| 7 | 4000 | TOEIC Master |

---

## Trạng thái hiện tại của học viên

```
Level:    1 (0 XP)
Day:      1 / 84
Streak:   0 days
Score:    ~300 (baseline)
Week:     1 — Finance Vocabulary + Word Form
Status:   Day 1 lab đã tạo, chưa có kết quả từ học viên
```
