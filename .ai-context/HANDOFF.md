# AI HANDOFF DOCUMENT
**Last updated:** 2026-06-25  
**Written for:** AI assistant on a new machine picking up this project  
**Read this first before doing anything.**

---

## 1. Dự án là gì

Hệ thống học TOEIC cá nhân hóa cho **Duong** (người Việt, IT professional).  
Mục tiêu: từ baseline ~250–400 lên **TOEIC 650+** trong **12 tuần (84 ngày)**.  
Thư mục làm việc: `d:\toeic\` (hoặc bất cứ đâu user clone về).  
Nội dung chính nằm trong `English/`.

---

## 2. Trạng thái hiện tại — 2026-06-24 (Day 2)

```
Day:        2 / 84
Level:      2 (TOEIC Rookie)
XP:         135 tổng (35 XP vào Lv 2, threshold 100)
Streak:     1 ngày
Est. Score: ~250–400 (chưa đổi sau Day 1)
```

### Day 1 kết quả (2026-06-23, đã hoàn thành)
| Quest | Kết quả |
|-------|---------|
| Q1 Vocabulary (Finance Set 1) | 4/5 ✅ |
| Q2 Grammar Dungeon (Word Form) | ❌ **SKIPPED** |
| Q3 Photo Detective Part 1 | 5/5 ✅ Perfect |
| Q4 Part 5 Drill (10 câu) | 7/10 ✅ |
| Q5 Flashcard Review | ✅ |
| ★ Bonus: Pronouns & Determiners | ⬜ **CHƯA LÀM** |

### Việc Day 2 đang chờ learner
- `English/DAILY_QUESTS/day2_grammar_lab.html` — **ĐÃ TẠO, chưa làm**  
  Gồm: Verb Tenses + Word Forms + Dependent Prepositions, mỗi topic 10 câu, tổng +300 XP

---

## 3. File structure quan trọng

```
d:\toeic\
├── CLAUDE.md                          ← project instructions cho AI
├── English/
│   ├── PLAYER_PROFILE.md              ← Level/XP/Streak/Achievements
│   ├── TOEIC_PLAN.md                  ← 12-week roadmap
│   ├── TOEIC_PROGRESS.md              ← score history theo ngày
│   ├── TOEIC_MISTAKES.md              ← log lỗi sai
│   ├── TOEIC_VOCABULARY.md            ← từ vựng đã học
│   ├── TOEIC_ACHIEVEMENTS.md          ← badges đã unlock
│   │
│   ├── DAILY_QUESTS/
│   │   ├── day1.html                  ← Day 1 lab (hoàn chỉnh)
│   │   ├── DAY1_2026-06-23.md         ← quest log Day 1 (có kết quả)
│   │   ├── day1_bonus_pronouns.html   ← Bonus chưa làm (+100 XP)
│   │   ├── day2_grammar_lab.html      ← Day 2 Grammar Lab (chờ learner)
│   │
│   ├── RESOURCES/
│   │   ├── vocab_bank.html            ← 120+ từ, search/filter/track
│   │   └── grammar_guide.html         ← 8 grammar rules
│   │
│   ├── PART5/
│   │   ├── lesson_01_word_form.md     ← Word Form strategy + suffix tables
│   │   ├── lesson_02_pronouns_determiners.md
│   │   ├── lesson_03_verb_tenses.md
│   │   └── lesson_04_dependent_prepositions.md
│   │
│   ├── RESULTS/                       ← JSON kết quả tự động (từ HTML)
│   │   └── (*.json files sau khi learner làm bài)
│   │
│   └── WEEKLY_BOSS/                   ← TRỐNG, cần week1_boss.html vào 2026-06-28
│
└── .ai-context/                       ← folder này — context cho AI
    ├── HANDOFF.md                     ← file này
    ├── executive_summary.md
    ├── memory_snapshot.md
    └── english_content_index.md
```

---

## 4. Workflow cộng tác (quan trọng)

### Learner làm gì
1. Chụp ảnh sách → gửi chat → AI tạo lesson + HTML drill
2. Mở HTML trong **Chrome/Edge** → học Theory → làm Practice
3. Kết quả tự lưu vào `English/RESULTS/*.json` (File System Access API)
4. Nhắn **"xong"** hoặc **"done"** → AI đọc JSON → cập nhật progress

### AI làm gì
1. Đọc `English/RESULTS/*.json` (dùng Read tool theo đường dẫn cụ thể)
2. Cập nhật: `PLAYER_PROFILE.md`, `TOEIC_PROGRESS.md`, `TOEIC_ACHIEVEMENTS.md`, quest log
3. Phân tích lỗi sai → ghi vào `TOEIC_MISTAKES.md`
4. Tạo nội dung ngày tiếp theo dựa trên điểm yếu

### Khi learner nói "Start Day N"
1. Đọc quest log ngày N-1 (`DAILY_QUESTS/DAYN-1_*.md`)
2. Đọc `TOEIC_MISTAKES.md`
3. Tạo `DAILY_QUESTS/dayN.html` — 4 quests + bonus nếu cần
4. Tạo `DAILY_QUESTS/DAYN_YYYY-MM-DD.md` — quest log mới

### Khi learner gửi ảnh sách
1. Đọc nội dung ảnh
2. Tạo lesson `.md` trong `English/PART5/` (hoặc PART tương ứng)
3. Tạo HTML drill tương ứng với phần lý thuyết đó
4. Cập nhật `english_content_index.md`

---

## 5. Technical implementations đã build

### Web Speech API (TTS)
- **Có trong:** `day1.html`
- **Dùng cho:** đọc vocab cards (speakVocab), đọc Part 1 options (playP1Audio)
- **Quan trọng:** Part 1 — options `display:none` cho đến khi audio phát xong mới hiện
- **Pattern:**
```javascript
const TTS = {
  queue(texts, rate, onDone) {
    window.speechSynthesis.cancel();
    let idx = 0;
    const next = () => {
      if (idx >= texts.length) { onDone && onDone(); return; }
      const u = new SpeechSynthesisUtterance(texts[idx++]);
      u.lang = 'en-US'; u.rate = rate || 0.88;
      u.onend = () => setTimeout(next, 420);
      window.speechSynthesis.speak(u);
    };
    next();
  }
};
```

### Inline SVG Part 1 Photos
- **Có trong:** `day1.html` — mảng `part1Qs`, mỗi object có property `svg`
- **Tại sao:** không dùng emoji (không phải ảnh thật), không có external image files
- **SVG:** 300×185 viewBox, vẽ geometric shapes thể hiện người/vật/phòng

### File System Access API (Auto-save)
- **Có trong:** `day2_grammar_lab.html` — object `AutoSave`
- **Flow:** click "Kết nối thư mục" 1 lần → chọn `English/` → IndexedDB lưu handle → sau mỗi Submit tự ghi `English/RESULTS/{filename}.json`
- **Chỉ hoạt động trên Chrome/Edge** (Firefox chưa support)
- **Cần thêm vào:** `day1.html`, `day1_bonus_pronouns.html`, và tất cả HTML sau này

### XP System
| Action | XP |
|--------|-----|
| Vocab card viewed | +10 |
| Grammar question đúng | +20 |
| Part 1 question đúng | +30 |
| Part 5 drill đúng | +30 |
| Perfect score bonus | +50 |
| Bonus quest complete | +100 |

Level thresholds: mỗi level = 100 XP (Level 1→2 tại 100 XP, v.v.)

---

## 6. Việc cần làm — theo thứ tự ưu tiên

### Ngay bây giờ (Day 2)
- [ ] Learner làm `day2_grammar_lab.html` → AI đọc RESULTS/*.json → update progress
- [ ] Learner làm `day1_bonus_pronouns.html` (còn +100 XP chưa lấy)
- [ ] Sync 20 từ Finance Set 1 từ `day1.html` vào `TOEIC_VOCABULARY.md`
- [ ] Thêm AutoSave vào `day1.html` và `day1_bonus_pronouns.html`

### Ngắn hạn (Day 3–5)
- [ ] Tạo `day3.html` sau khi có kết quả Day 2 (theme: Passive Voice + Office Vocab)
- [ ] Cập nhật `TOEIC_MISTAKES.md` theo lỗi sai thực tế từ Day 1–2

### Trung hạn (2026-06-28)
- [ ] Tạo `WEEKLY_BOSS/week1_boss.html` — mini test tổng hợp Week 1
- [ ] Update estimated TOEIC score sau Week 1

---

## 7. Nguyên tắc không được vi phạm

1. **Dạy TOEIC** — không dạy tiếng Anh tổng quát
2. **Vocabulary first** — đây là gap lớn nhất của learner
3. **Không reveal đáp án** trước khi learner suy nghĩ (display:none cho options)
4. **Giải thích bằng tiếng Việt** — learner đọc hiểu tốt hơn
5. **Adapt theo kết quả** — sai nhiều Part 5 → tăng Part 5 hôm sau
6. **RPG mechanics** — luôn có XP + progress bar + achievements

---

## 8. Cách đọc kết quả auto-save

Khi learner báo "xong", đọc các file này:
```
English/RESULTS/day2_grammar_lab_tenses.json
English/RESULTS/day2_grammar_lab_wordform.json
English/RESULTS/day2_grammar_lab_prep.json
```

Mỗi JSON có cấu trúc:
```json
{
  "topic": "tenses",
  "date": "2026-06-24T...",
  "score": 8,
  "total": 10,
  "pct": 80,
  "xp": 80,
  "details": [
    { "question": "...", "chosen": "...", "correct": "...", "isCorrect": true }
  ]
}
```

Từ đó cập nhật:
- `PLAYER_PROFILE.md` — XP, Level
- `TOEIC_PROGRESS.md` — thêm dòng mới
- `TOEIC_ACHIEVEMENTS.md` — unlock nếu đủ điều kiện
- `DAILY_QUESTS/DAY2_2026-06-24.md` — tạo mới hoặc cập nhật results section
- `TOEIC_MISTAKES.md` — log những câu isCorrect: false

---

## 9. Data Engineering Track (2026-06-25 — MAJOR UPDATE)

Dự án đã mở rộng sang **Data Engineering Platform**. AI mới phải biết điều này.

### Vấn đề
ETS 2026 PDFs là scan (không có text layer). Cần OCR để extract 2,000 câu hỏi.

### Tool đã chọn: Marker (datalab-to/marker)
- Installed: `.venv-marker/` (Python 3.12)
- Models cached: `C:\Users\phamd\AppData\Local\datalab\` (~3GB)
- Đã test thành công trên 5 trang LISTENING.pdf → `raw/marker_test/`

### Architecture docs đã viết (đọc theo thứ tự nếu cần context)
```
docs/project_analysis.md    ← audit toàn bộ repo
docs/ets_format_spec.md     ← page structure per PDF
docs/toeic_schema.md        ← JSON schema cho 7 parts
docs/data_architecture.md   ← directory layout + data flow
docs/etl_pipeline.md        ← pipeline design + commands
ROADMAP.md                  ← timeline + quick start commands
```

### Scripts đã viết (production-ready, chưa chạy trên full PDFs)
```
scripts/extract/run_marker.py       ← chạy Marker OCR
scripts/extract/parse_reading.py    ← parse Parts 5/6/7 từ READING.md
scripts/extract/parse_transcript.py ← parse answer keys + scripts
scripts/extract/parse_listening.py  ← parse Parts 1/3/4 + extract images
scripts/extract/inject_answers.py   ← merge answers vào all JSONs
scripts/validator/validate_bank.py  ← QA check
scripts/exporter/export_practice_test.py ← generate HTML tests
```

### Trạng thái question_bank/ hiện tại
```
question_bank/
├── part1.json       ← 60 records ✅ (60/60 images)
├── part2.json       ← 250 records ✅ (skeleton, chờ answers)
├── part3.json       ← 390 records ✅ (4 options mỗi câu)
├── part4.json       ← 300 records ✅ (4 options mỗi câu)
├── part5.json       ← chưa có (chờ READING)
├── part6.json       ← chưa có (chờ READING)
├── part7.json       ← chưa có (chờ READING)
├── passages.json    ← chưa có (chờ READING)
├── answer_keys.json ← chưa có (chờ TRANSCRIPT)
└── images/part1/    ← 60 JPEGs (t01_q001.jpg ... t10_q006.jpg) ✅
```

### Trạng thái extraction (2026-06-25)
| PDF | Status | Output |
|-----|--------|--------|
| ETS 2026 LISTENING.pdf (142 pp) | **DONE ✅** | question_bank/part1–4.json + images/part1/ (60 ảnh) |
| ETS 2026 READING.pdf (~304 pp) | **CHƯA CHẠY** | extracted/READING/ (thư mục trống) |
| ETS 2026 TRANSCRIPT.pdf | **CHƯA CHẠY** | — |

**Ghi chú LISTENING:**
- Part 1: 60/60 records, 60/60 images ✅
  - Nguồn ảnh: Marker output (`extracted/LISTENING/ETS 2026 LISTENING/_page_N_Picture_M.jpeg`)
  - Filter size >10KB để loại icon trang trí (<2KB); copy sang `question_bank/images/part1/t{NN}_q{NNN}.jpg`
  - PyMuPDF đã loại bỏ (ảnh extract kèm footer text của sách — không dùng được)
- Part 2: 250 skeleton (audio-only — transcript sẽ fill script + answer)
- Part 3: 390/390 questions, 390/390 complete options
- Part 4: 300/300 questions, 298/300 complete options (2 câu user sửa tay do OCR lỗi scan xấu)
- Answers: chưa inject (chờ TRANSCRIPT extraction)

**Đã dọn dẹp:**
- Xoá: `scripts/build_part{1-7}_bank.py`, `crop_part1.py`, `extract_part1.py`, `ocr_engine.py`, `raw/marker_test/`
- `parse_listening.py` đã rewrite phần extract ảnh: bỏ PyMuPDF, dùng Marker output trực tiếp
- `question_bank/images/part1/` đã xoá ảnh PyMuPDF xấu, thay bằng ảnh sạch từ Marker

### Lệnh tiếp theo (quick start)
```powershell
cd d:\toeic
# Bước 1: READING (4-6 giờ — chạy ban đêm)
.venv-marker\Scripts\python.exe scripts\extract\run_marker.py reading

# Bước 2: Parse READING → part5/6/7.json
.venv-marker\Scripts\python.exe scripts\extract\parse_reading.py

# Bước 3: TRANSCRIPT (2-3 giờ)
.venv-marker\Scripts\python.exe scripts\extract\run_marker.py transcript

# Bước 4: Parse TRANSCRIPT → answer_keys.json
.venv-marker\Scripts\python.exe scripts\extract\parse_transcript.py

# Bước 5: Inject answers vào tất cả JSONs
.venv-marker\Scripts\python.exe scripts\extract\inject_answers.py

# Bước 6: Validate
.venv-marker\Scripts\python.exe scripts\validator\validate_bank.py
```
