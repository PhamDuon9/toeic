# AI HANDOFF DOCUMENT
**Last updated:** 2026-06-26
**Written for:** AI assistant picking up this project in a new session.
**Read MEMORY.md first, then this file.**

---

## 1. Dự án là gì

Hệ thống học TOEIC cá nhân hóa cho **Duong** (người Việt, IT professional).
Mục tiêu: từ baseline ~250–400 lên **TOEIC 650+** trong **12 tuần** (kết thúc 2026-09-15).

---

## 2. Những gì đã xây dựng — tính đến 2026-06-26

### A. Web App (`app/index.html`)
Single-file SPA, chạy bằng `python serve.py` → `http://localhost:8000/app/`

**7 screens:**
1. **Dashboard** — XP/Level/Streak stats, Today's Quest card, Performance bars per Part, Recommendations, Achievements mini-panel
2. **SRS Drill** — SM-2 spaced repetition, Part 5 questions, inline explanation sau khi trả lời
3. **Flashcards** — 152 từ từ vocab.json, 8 category filter buttons, TTS pronounce, Save to My Words
4. **Full Tests** — **Exam Mode** (không hint/explain/word-lookup) · Part 1–4 audio (10 tests) · **Part 5/6/7 thực (ETS data)** · Speed Mode ⚡
5. **Analysis** — mistake patterns by tag/part, bar charts, action plan
6. **Daily Quests** — 12-week plan bar, daily quest cards với "Open Lesson" links, Achievements grid
7. **Study** *(mới)* — Ôn tập per-part: filter Part/Test/Grammar Tag (**P1–P7**) · toggle Hints/Explanations/Auto-reveal · nút Show Answer · Word Lookup bật · **Passage box cho P6/P7**

**Triết lý 2 chế độ:**
- **Full Tests = thi thật** — không gợi ý, không explain, submit xong mới xem kết quả
- **Study = ôn tập** — đầy đủ hỗ trợ: hint, explanation, word lookup, reveal đáp án bất cứ lúc nào

**Word Lookup** (double-click bất kỳ từ trong bài):
- Parallel fetch: Free Dictionary API (definition/phonetics) + MyMemory API (Vietnamese translation)
- Local vocab.json check (Vietnamese + category)
- Word Family map (40+ TOEIC stems) — noun/verb/adj/adv
- Save to My Words, TTS, Esc để đóng

**Data persistence:** tất cả trong localStorage (không cần backend)

### B. Question Bank (`question_bank/`)
- `part1.json` — 60 records, audio + image paths ✅
- `part2.json` — 250 records, audio paths ✅
- `part3.json` — 390 records, full options ✅
- `part4.json` — 300 records, full options ✅
- `part5_mock.json` — 19 câu mock **với explanation đầy đủ** ✅
- `vocab.json` — 152 từ, 8 categories ✅
- `part5.json` — 299 records ✅ **QA passed** · LIVE trong web (Full Tests + Study)
- `part6.json` — 160 records ✅ **QA passed** · LIVE trong web với passage UI
- `part7.json` — **540/540 records** ✅ **QA passed (100%)** · LIVE trong web với passage UI
- `passages.json` — **145 passages** ✅ (40 Part 6 + 105 Part 7) · QA clean (0 issues)
- `answer_keys.json` — chờ TRANSCRIPT OCR (tất cả `answer: null` hiện tại)

### C. ETL Pipeline (`scripts/`)
- `run_marker.py` — chạy Marker OCR (AI-based, ~3GB models)
- `parse_transcript.py` — extract answer keys + listening scripts
- `parse_reading.py` — extract Part 5/6/7 questions
- `inject_answers.py` — merge answers vào all JSONs
- `validate_bank.py` — QA check

### D. Lesson System (`English/`)
- `DAILY_QUESTS/day1.html` — Day 1 lab (hoàn chỉnh)
- `DAILY_QUESTS/day2_grammar_lab.html` — Day 2 Grammar Lab
- `RESOURCES/vocab_bank.html` — 152 từ searchable
- `RESOURCES/grammar_guide.html` — 8 grammar rules
- `PART5/lesson_01–04.md` — Word Form, Pronouns, Verb Tenses, Prepositions

---

## 3. OCR Status

| PDF | Status | Action cần |
|-----|--------|-----------|
| ETS 2026 LISTENING.pdf | **DONE ✅** | — |
| ETS 2026 TRANSCRIPT.pdf | **ĐANG CHẠY** ⏳ | Đợi `extracted/TRANSCRIPT/*.md` xuất hiện |
| ETS 2026 READING.pdf | **DONE ✅** | part5/6/7 parsed + QA verified |

**Khi TRANSCRIPT xong:**
```powershell
.venv-marker\Scripts\python.exe scripts\extract\parse_transcript.py
.venv-marker\Scripts\python.exe scripts\extract\inject_answers.py
```
→ Kết quả: `answer_keys.json` + answers inject vào part1–4.json + part5/6/7.json

**Part 7 QA notes (final — 2026-06-26):**
- **540/540 records clean** — 17 câu missing đã recover thành công
  - 12 câu: tìm lại từ READING.md OCR (test-boundary search + mid-line regex)
  - 5 câu: user cung cấp từ ảnh chụp sách (T9-Q156, T9-Q179, T9-Q184, T10-Q161, T10-Q172)
- Fixes applied: insert-sentence option C (6 câu), Q196-200 passage_id (50 câu), truncated stems/options (5 câu)
- Q186-200 triple passages: off-by-one passage linking bug (pre-existing). Q196-200 fixed. Q186-195 vẫn shifted nhưng có passage_id.
- **Part 7 LIVE trong web** — passage hiện trong scrollable box (max 220px), word-lookup enabled

**Part 6 notes (2026-06-26):**
- 160 câu, 40 passages (4/passage), 10 tests. LIVE trong web.
- Blank markers không nhất quán: 22/40 passages có đúng 4 blanks, 18/40 chỉ có 1-3 blanks (OCR drop)
- JS regex detect: `/(?:\\_)+|-{5,}|[^\x00-\x7f]{4,}/g` (escaped underscores OR dashes OR em-dashes)
- Active blank (cho question đang xem) được highlight với `.p6-blank.active`

**passages.json notes:**
- Part 6 text chứa blank markers: `\_\_\_\_` (Markdown escaped underscores) hoặc `-----` hoặc `————` (em-dashes)
- Part 7 text là raw passage text, có thể dài 3-5 paragraphs — hiện trong scrollable box

**Part 5 QA notes (quan trọng cho AI sau):**
- Marker OCR drop blank dashes trong table-format questions → blank position sai
- parse_reading.py dùng heuristic (đặt blank tại line break đầu tiên) → ~15 câu sai
- Đã manually verify + fix tất cả 299 câu so với sách ETS 2026
- Nếu re-run parse_reading.py → phải manual fix lại Part 5 blank positions

---

## 4. Hướng phát triển tiếp theo

### Ưu tiên 1 — Ngay bây giờ (2026-06-26)
- [ ] **Tạo `day3.html`** — Passive Voice + Logistics Vocab (quá hạn 1 ngày)
- [ ] **`WEEKLY_BOSS/week1_boss.html`** — deadline 2026-06-28 (còn 2 ngày)
- [ ] **"My Words" screen** — hiển thị từ đã save qua Word Lookup

### Ưu tiên 2 — Khi TRANSCRIPT OCR xong
- [ ] Inject answers vào part1–4.json + part5/6/7.json
- [ ] Review mode cho Part 5/6/7 sẽ hiện đúng/sai thực sự (hiện answer: null)
- [ ] **Transcript viewer** cho Part 3/4 — hiện script sau khi làm bài

### Ưu tiên 3 — App improvements
- [ ] Load Part 1–4 vào Study screen (hiện chỉ có P5/6/7)
- [ ] Explanation templates cho Part 5 (tag-based, không cần API)
- [ ] Export mistakes → PDF/CSV để ôn offline

### ✅ HOÀN THÀNH (2026-06-26)
- [x] Part 7 QA: 523→540 records (17 missing recovered)
- [x] passages.json: 145 passages QA clean
- [x] Web app Part 5/6/7 LIVE — Full Tests + Study screen

---

## 5. Workflow learner ↔ AI

### Khi learner nói "Start Day N" hoặc "Tạo Day N"
1. Đọc kết quả Day N-1 từ `English/RESULTS/*.json`
2. Đọc `TOEIC_MISTAKES.md` — chú ý top error tags
3. Tạo `English/DAILY_QUESTS/dayN.html` — 4 quests + bonus
4. Tạo `English/DAILY_QUESTS/DAYN_YYYY-MM-DD.md` — quest log
5. Update `TOEIC_PLAN.md` nếu cần điều chỉnh

### Khi learner nói "xong" (sau khi làm HTML)
1. Đọc `English/RESULTS/*.json`
2. Update: `PLAYER_PROFILE.md`, `TOEIC_PROGRESS.md`, `TOEIC_ACHIEVEMENTS.md`
3. Log mistakes → `TOEIC_MISTAKES.md`
4. Báo cáo kết quả + gợi ý tiếp theo

### Khi learner gửi ảnh sách / đề bài
1. Đọc ảnh, extract câu hỏi
2. Tạo lesson `.md` trong `English/PART{N}/`
3. Tạo HTML drill tương ứng
4. Update `english_content_index.md`

---

## 6. Nguyên tắc không vi phạm

1. **Dạy TOEIC** — không dạy tiếng Anh tổng quát
2. **Vocabulary first** — gap lớn nhất, block tất cả sections
3. **Giải thích bằng tiếng Việt** khi cần
4. **Không reveal đáp án** trước khi learner suy nghĩ
5. **Adapt theo kết quả** — sai nhiều Part 5 → tăng Part 5 hôm sau
6. **RPG mechanics** — luôn có XP + progress + achievements

---

## 7. Design system (dùng nhất quán)

```css
--bg: #0a0f1e  --card: #111827  --card2: #161d30  --border: #1e2448
--purple: #7c6fff  --green: #22c55e  --red: #f87171  --gold: #fbbf24  --blue: #38bdf8
--text: #e2e8f0  --muted: #64748b
font: 'Segoe UI', sans-serif
border-radius: 12–14px cho cards, 8px cho buttons
```

---

## 8. Files tham khảo khác

- `MEMORY.md` — tóm tắt nhanh (đọc trước)
- `.ai-context/english_content_index.md` — danh sách toàn bộ file đã tạo
- `.ai-context/executive_summary.md` — tổng quan + todo
- `docs/toeic_schema.md` — JSON schema cho question bank
- `docs/etl_pipeline.md` — ETL pipeline chi tiết
