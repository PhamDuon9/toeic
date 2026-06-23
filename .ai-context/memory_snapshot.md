# Memory Snapshot
**Last updated:** 2026-06-24

---

## Học viên

- **Tên:** Duong, người Việt, IT professional
- **Baseline:** TOEIC ~250–400 (Placement Test: 6/15 = 40%)
- **Điểm mạnh:** Reading comprehension, Listening intuition, Part 1 (5/5 Day 1)
- **Điểm yếu nghiêm trọng:** Vocabulary (0/5 placement), Grammar (1/5 placement)
- **Mục tiêu:** TOEIC 650+ trước 2026-09-15
- **Học:** 60–90 phút/ngày, bắt đầu 2026-06-23
- **Hiện tại:** Day 2 / 84 · Level 2 · 135 XP · Streak 1

---

## Trạng thái Day 1 (đã hoàn thành 2026-06-23)

| Quest | Score | XP |
|-------|-------|----|
| Q1 Vocabulary Finance Set 1 | 4/5 | ✅ |
| Q2 Grammar Dungeon Word Form | SKIPPED | ❌ |
| Q3 Part 1 Photos | 5/5 Perfect | ✅ |
| Q4 Part 5 Drill | 7/10 | ✅ |
| Q5 Flashcard | done | ✅ |
| Bonus Pronouns | chưa làm | ⬜ |

**XP nhận được:** 135 / 310 available

---

## Quy ước đặt tên file

| Loại | Pattern | Ví dụ |
|------|---------|-------|
| Daily lab | `English/DAILY_QUESTS/dayN.html` | `day1.html` |
| Quest log | `English/DAILY_QUESTS/DAYN_YYYY-MM-DD.md` | `DAY1_2026-06-23.md` |
| Bonus lab | `English/DAILY_QUESTS/dayN_bonus_topic.html` | `day1_bonus_pronouns.html` |
| Grammar lab | `English/DAILY_QUESTS/dayN_grammar_lab.html` | `day2_grammar_lab.html` |
| Weekly boss | `English/WEEKLY_BOSS/weekN_boss.html` | `week1_boss.html` |
| Part lesson | `English/PARTN/lesson_NN_topic.md` | `lesson_03_verb_tenses.md` |
| Auto-save results | `English/RESULTS/filename_topic.json` | `day2_grammar_lab_tenses.json` |

---

## Design system (HTML labs)

```css
body background:  #0a0f1e
card background:  #111827
border:           #1e2448 (default) / #2a2f5e (hover)
accent purple:    #7c6fff
accent green:     #22c55e
accent red:       #f87171
accent gold:      #fbbf24
```

- Chọn option → Submit → đáp án highlight + giải thích tiếng Việt
- Options **luôn ẩn** (display:none) trong Part 1 cho đến khi TTS đọc xong
- XP hiển thị real-time trong HUD
- Mỗi HTML có nút "🔗 Kết nối thư mục" để auto-save kết quả

---

## Week 1 plan (2026-06-23 to 2026-06-29)

| Ngày | Date | Theme | File |
|------|------|-------|------|
| Day 1 | 2026-06-23 | Finance Vocab + Word Form + Part 1 | day1.html ✅ |
| Day 2 | 2026-06-24 | Verb Tenses + Word Forms + Dep. Prepositions | day2_grammar_lab.html ✅ |
| Day 3 | 2026-06-25 | Passive Voice + Office Vocab | **chưa tạo** |
| Day 4 | 2026-06-26 | Conjunctions + HR Vocab | **chưa tạo** |
| Day 5 | 2026-06-27 | Relative Clauses + Meetings Vocab | **chưa tạo** |
| Day 6 | 2026-06-28 | Mini Test + Review + Week1 Boss | **chưa tạo** |
| Day 7 | 2026-06-29 | REST (flashcard only) | **chưa tạo** |

---

## Lỗi từ Placement Test (9 lỗi — cần dạy)

| Lỗi | Số lượng | Priority | Đã dạy? |
|-----|---------|---------|---------|
| Business Vocabulary | 4 | 🔴 Critical | Đang học (Day 1+) |
| Passive Voice | 2 | 🔴 High | ❌ Chưa |
| Word Form | 2 | 🟡 Medium | Partially (Day 2) |
| Verb Tense | 1 | 🟡 Medium | Day 2 ✅ |
| Conjunction | 1 | 🟡 Medium | ❌ Chưa |
| Relative Clause | 1 | 🟡 Medium | ❌ Chưa |

---

## Nguyên tắc coaching

1. Dạy TOEIC — không dạy tiếng Anh tổng quát
2. Vocabulary first (gap lớn nhất)
3. Không reveal đáp án trước khi learner làm (display:none)
4. Giải thích bằng tiếng Việt trong HTML
5. Adapt theo kết quả thực tế (đọc RESULTS/*.json)
6. RPG mechanics — XP + Level + Achievement mọi session
