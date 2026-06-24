# BÁO CÁO ĐÁNH GIÁ HỆ THỐNG TOEIC LEARNING LAB

**Ngày audit:** 2026-06-24  
**Thực hiện bởi:** Claude Code (READ-ONLY audit)  
**Phạm vi:** Toàn bộ thư mục `D:\duongpt\TOEIC\`

---

## 1. KIỂM KÊ TÀI SẢN (INVENTORY)

### 1.1 Tài liệu gốc (raw/)

| File | Kích thước | Mô tả |
|------|-----------|-------|
| `raw/ETS 2026 LISTENING.pdf` | 209.5 MB | Sách ETS 2026 phần Listening (10 tests) |
| `raw/ETS 2026 READING.pdf` | 337.3 MB | Sách ETS 2026 phần Reading (10 tests) |
| `raw/ETS 2026 TRANSCRIPT.pdf` | 478.0 MB | Script transcript toàn bộ (10 tests) |
| **Tổng** | **~1,025 MB** | 3 PDF nguồn chính |

### 1.2 Audio (raw/Audio/)

**Cấu trúc thư mục:**
```
raw/Audio/LISTENING/
├── Câu lẻ/       ← Audio từng câu riêng lẻ (Parts 1-4)
│   ├── Test_01/ — Test_10/   (10 tests)
└── Part/          ← Audio nguyên Part (4 parts/test)
    ├── Test_01/ — Test_10/   (10 tests)
```

**Thống kê chi tiết:**

| Loại | Nội dung | Số file |
|------|---------|---------|
| Câu lẻ (Test 01–09) | ~54 file MP3/test | ~486 files |
| Câu lẻ (Test 10) | 54 file MP3 | 54 files |
| Câu lẻ (Test 07) | 52 file MP3 (thiếu 2) | 52 files |
| Part audio (Test 01–10) | 4 file MP3/test (Part1–Part4) | 40 files |
| **TỔNG** | | **578 files MP3** |

**Ví dụ cấu trúc file "Câu lẻ":**
- `Test_01-01.mp3` đến `Test_01-31.mp3` — Part 1 (6 câu) + Part 2 (25 câu)
- `Test_01-32-34.mp3`, `Test_01-35-37.mp3`, ... — Part 3 (theo nhóm 3 câu)
- `Test_01-68-70.mp3`, ... — Part 4 (theo nhóm 3 câu)

**Ví dụ cấu trúc file "Part":**
- `Test_01-Part1.mp3`, `Test_01-Part2.mp3`, `Test_01-Part3.mp3`, `Test_01-Part4.mp3`

> **Nhận xét:** Test 07 có thể thiếu 2 file MP3 (52 thay vì 54). Cần kiểm tra lại.

### 1.3 Hình ảnh Part 1 đã xử lý (raw/ETS_BANK/)

| Thư mục | Số file | Mô tả |
|---------|---------|-------|
| `raw/ETS_BANK/images/part1/` | 60 ảnh JPG | Ảnh Part 1 đã crop (test1–test10, 6 ảnh/test) |
| `raw/ETS_BANK/scans/` | 144 ảnh PNG | Scan trang sách từ PDF Listening (3x resolution) |

**Mapping Part 1:** `raw/ETS_BANK/part1.json` — 60 entries, cấu trúc:
```json
{ "test": 1, "question": 1, "image": "test1_q1.jpg" }
```

### 1.4 Nội dung học tập (English/)

**Tracking files (6 files):**

| File | Trạng thái | Nội dung hiện tại |
|------|-----------|-------------------|
| `PLAYER_PROFILE.md` | Cập nhật | Level 2 · 135 XP · Streak 1 · Est. 250-400 |
| `TOEIC_PLAN.md` | Đầy đủ | 12-week roadmap + Week 1 chi tiết |
| `TOEIC_PROGRESS.md` | Cập nhật | Placement + Day 1 results |
| `TOEIC_MISTAKES.md` | Partial | 9 lỗi placement test, chưa có lỗi Day 1 |
| `TOEIC_VOCABULARY.md` | Partial | 9 từ, chưa sync 20 từ Finance Set 1 |
| `TOEIC_ACHIEVEMENTS.md` | Chính xác | 3 unlocked, 9 locked |

**HTML Interactive Labs:**

| File | Trạng thái | Nội dung |
|------|-----------|---------|
| `placement_test.html` | Hoàn chỉnh | 15 câu test đầu vào |
| `DAILY_QUESTS/day1.html` | Hoàn chỉnh | 20 vocab + Word Form + Part 1 SVG/TTS + Part 5 |
| `DAILY_QUESTS/day1_bonus_pronouns.html` | Tạo xong, chưa làm | Pronouns & Determiners · 10 câu · +100 XP |
| `DAILY_QUESTS/day2_grammar_lab.html` | Tạo xong, chưa làm | 30 câu grammar + AutoSave |
| `RESOURCES/vocab_bank.html` | Hoàn chỉnh | 120+ từ · 8 chủ đề · TTS/localStorage |
| `RESOURCES/grammar_guide.html` | Hoàn chỉnh | 8 grammar rules + TOEIC traps |

**Lesson Files (PART5/):**

| File | Trạng thái |
|------|-----------|
| `lesson_01_word_form.md` | Hoàn chỉnh |
| `lesson_02_pronouns_determiners.md` | Hoàn chỉnh |
| `lesson_03_verb_tenses.md` | Hoàn chỉnh |
| `lesson_04_dependent_prepositions.md` | Hoàn chỉnh |

**Quest Logs:**
- `DAILY_QUESTS/DAY1_2026-06-23.md` — Quest log Day 1 có kết quả thực tế

### 1.5 Skills (3 files)

| File | Mô tả |
|------|-------|
| `skills/toeic-coach/CLAUDE.md` | AI Coach: lên kế hoạch, dạy học, tạo lesson |
| `skills/toeic-examiner/CLAUDE.md` | AI Examiner: chấm điểm ETS-style, phân tích lỗi |
| `skills/toeic-rpg-gamemaster/CLAUDE.md` | AI Game Master: XP/Level/Achievement, gamification |

### 1.6 AI Context (9 files trong .ai-context/)

| File | Nội dung |
|------|---------|
| `HANDOFF.md` | Toàn bộ context + workflow cho AI mới |
| `executive_summary.md` | Tổng quan trạng thái + việc cần làm |
| `english_content_index.md` | Chỉ mục toàn bộ file English/ |
| `gap_analysis.md` | Phân tích thiếu sót |
| `learning_path.md` | Lộ trình học tập |
| `memory_snapshot.md` | Snapshot trạng thái + quy ước đặt tên |
| `project_overview.md` | Tổng quan kiến trúc hệ thống |
| `skills_inventory.md` | Mô tả 3 skills chi tiết |

---

## 2. PHÂN TÍCH DỮ LIỆU THEO TỪNG PART

### Part 1 — Photographs

**Trạng thái: SẴN SÀNG SỬ DỤNG**

| Tài sản | Số lượng | Trạng thái |
|---------|---------|-----------|
| Ảnh đã extract (JPG) | 60 ảnh (6/test × 10 tests) | Sẵn dùng |
| Mapping JSON (`part1.json`) | 60 entries | Hoàn chỉnh |
| Audio câu lẻ Part 1 | ~60 file MP3 (6/test × 10 tests) | Sẵn dùng |
| Audio nguyên Part 1 | 10 file MP3 | Sẵn dùng |
| Lesson file | Chưa có `PART1/lesson_*.md` | Thiếu |
| Drill HTML sử dụng ảnh thật | Chưa có (day1.html dùng SVG giả) | Thiếu |

**Nhận xét:** Đây là Part duy nhất đã có pipeline hoàn chỉnh (PDF → extract → crop → JSON). Ảnh 60 bức đã sẵn sàng nhúng vào HTML drill. Bước tiếp theo là tạo `PART1/lesson_01.md` và cập nhật `day1.html` dùng ảnh thật thay SVG.

### Part 2 — Question-Response

**Trạng thái: CÓ AUDIO, THIẾU NỘI DUNG**

| Tài sản | Số lượng | Trạng thái |
|---------|---------|-----------|
| Audio câu lẻ Part 2 | ~250 file MP3 (25/test × 10 tests) | Sẵn dùng |
| Audio nguyên Part 2 | 10 file MP3 | Sẵn dùng |
| Lesson file | 0 | Thiếu |
| Drill HTML | 0 | Thiếu |
| Transcripts | Có trong PDF nhưng chưa extract | Cần OCR |

**Nhận xét:** Part 2 có ~250 câu hỏi audio sẵn sàng. Không cần ảnh. Khó tạo drill vì cần biết nội dung (A/B/C/D + đáp án) từ TRANSCRIPT.pdf. Đây là Part cần OCR transcript để tạo question bank.

### Part 3 — Conversations

**Trạng thái: CÓ AUDIO, THIẾU NỘI DUNG**

| Tài sản | Số lượng | Trạng thái |
|---------|---------|-----------|
| Audio nhóm 3 câu | ~130 file MP3 (~13 nhóm/test × 10 tests) | Sẵn dùng |
| Audio nguyên Part 3 | 10 file MP3 | Sẵn dùng |
| Lesson file | 0 | Thiếu |
| Drill HTML | 0 | Thiếu |

**Nhận xét:** Phức tạp nhất vì cần cả audio + transcript + question text + answer choices. Không thể tạo drill chỉ từ audio.

### Part 4 — Talks

**Trạng thái: CÓ AUDIO, THIẾU NỘI DUNG**

Tương tự Part 3. Có audio nhóm 3 câu. Cần transcript để tạo drill.

### Part 5 — Incomplete Sentences

**Trạng thái: ĐANG PHÁT TRIỂN TỐT NHẤT**

| Tài sản | Số lượng | Trạng thái |
|---------|---------|-----------|
| Lesson files | 4 files | Hoàn chỉnh |
| Grammar guide | 1 HTML | Hoàn chỉnh (8 rules) |
| Drill trong day1.html | 10 câu | Hoàn chỉnh |
| Drill trong day2_grammar_lab.html | 30 câu (3 topics × 10) | Tạo xong, chờ learner |
| Không cần audio/ảnh | — | — |

**Nhận xét:** Part 5 là part phù hợp nhất để phát triển nhanh vì chỉ cần text. 4 lesson files đã đủ nền tảng. Cần thêm 20–40 bài drill nữa cho Week 1–4.

### Part 6 — Text Completion

**Trạng thái: TRỐNG**

Chưa có bất kỳ nội dung nào. Cần nội dung từ READING.pdf (đã có 337 MB).

### Part 7 — Reading Comprehension

**Trạng thái: TRỐNG**

Chưa có bất kỳ nội dung nào. Cần nội dung từ READING.pdf. Đây là Part chiếm nhiều điểm nhất (55 câu).

---

## 3. PHÂN TÍCH SCRIPTS

### Script 1: `scripts/extract_part1.py`

| Thuộc tính | Chi tiết |
|-----------|---------|
| **Chức năng** | Render từng trang PDF Listening sang PNG (3x resolution) |
| **Input** | `raw/ETS_2026_LISTENING.pdf` (hardcode — tên sai, thiếu khoảng trắng) |
| **Output** | `English/ETS_BANK/scans/page_N.png` |
| **Thư viện** | PyMuPDF (fitz) |
| **Hoàn chỉnh** | 90% — Đã chạy (144 file scans có mặt). Vấn đề: đường dẫn PDF hardcode sai tên (thiếu space và "2026") |
| **Reusability** | Thấp — hardcode path, không có tham số CLI, không có logging |
| **Tình trạng output** | `raw/ETS_BANK/scans/` có 144 PNG — đã chạy thành công |

### Script 2: `scripts/crop_part1.py`

| Thuộc tính | Chi tiết |
|-----------|---------|
| **Chức năng** | Crop ảnh lớn từ mỗi trang scan (dùng contour detection) |
| **Input** | `English/ETS_BANK/scans/*.png` |
| **Output** | `English/ETS_BANK/images/part1_crop/part1_N.jpg` |
| **Thư viện** | OpenCV (cv2) |
| **Hoàn chỉnh** | 70% — Logic threshold đơn giản (240), không sort theo vị trí trên trang, counter toàn cục (không theo test/question) |
| **Vấn đề nghiêm trọng** | (1) Output `part1_crop/` nhưng thư mục chưa tồn tại (chỉ có `part1/`); (2) Không biết file nào thuộc test nào — mất mapping; (3) Không lọc trang direction vs trang ảnh |
| **Reusability** | Thấp — đây là script thử nghiệm, superseded bởi build_part1_bank.py |

### Script 3: `scripts/build_part1_bank.py`

| Thuộc tính | Chi tiết |
|-----------|---------|
| **Chức năng** | Pipeline đầy đủ: PDF → render → detect 2 ảnh/trang → crop → save JPG + JSON |
| **Input** | `raw/ETS 2026 LISTENING.pdf` (đường dẫn chính xác) |
| **Output** | `English/ETS_BANK/images/part1/testN_qQ.jpg` + `English/ETS_BANK/part1.json` |
| **Thư viện** | PyMuPDF + OpenCV + NumPy |
| **Hoàn chỉnh** | 95% — Đã chạy thành công (60 ảnh + JSON). Có skip logic (idempotent). Có fallback threshold (240→220→200) |
| **Vấn đề nhỏ** | (1) Không lưu bounding boxes vào JSON (chỉ filename); (2) Nếu trang có < 2 ảnh thì WARNING nhưng không dừng; (3) Đường dẫn output hardcode sang `English/ETS_BANK/` thay vì `raw/ETS_BANK/` |
| **Reusability** | Cao — script này là best practice, có thể mở rộng cho Part 2-7 |

**Lưu ý về đường dẫn không nhất quán:**
- `extract_part1.py` output vào `English/ETS_BANK/scans/`
- `build_part1_bank.py` output vào `English/ETS_BANK/images/part1/`
- Nhưng file thực tế lại nằm ở `raw/ETS_BANK/` (không phải `English/ETS_BANK/`)
- Đây là vấn đề về organization cần làm rõ

---

## 4. PHÂN TÍCH SKILLS

### 4.1 toeic-coach

**File:** `skills/toeic-coach/CLAUDE.md`

| Khía cạnh | Đánh giá |
|----------|---------|
| Định nghĩa role | Rõ ràng — "elite TOEIC coach" |
| Phạm vi | Đúng — chỉ TOEIC, không dạy tiếng Anh tổng quát |
| Assessment | Có (6 thông tin cần thu thập) |
| Study plan | Có (12-week / monthly / weekly / daily) |
| Daily training | Có (5 bước: Vocab → Grammar → Listening → Reading → Review) |
| Vocabulary | Có (8 chủ đề, track từ đã học) |
| Grammar | Có (8 grammar point ưu tiên) |
| Test simulation | Có (Easy/Medium/Hard) |
| Performance tracking | Có |
| Correction mode | Có (4-bước giải thích) |
| Ngôn ngữ giải thích | Không chỉ định (thực tế dùng tiếng Việt) |
| **Điểm mạnh** | Cấu trúc đầy đủ, rõ ràng, đủ để AI hoạt động |
| **Điểm yếu** | Không chỉ định đọc file nào khi startup; không có protocol tạo HTML lab |

### 4.2 toeic-examiner

**File:** `skills/toeic-examiner/CLAUDE.md`

| Khía cạnh | Đánh giá |
|----------|---------|
| Role | Rõ ràng — ETS-style evaluator, không phải giáo viên |
| Cấu trúc TOEIC | Đủ 7 parts |
| Exam generation | Có (Easy/Medium/Hard, business vocab, ETS-style distractors) |
| Scoring | Có (Correct/Incorrect/Accuracy%/Listening/Reading/Total) |
| Performance analysis | Có (5 sections: Summary/Strengths/Weaknesses/Error/Recommendations) |
| Error analysis | Có (6 loại lỗi) |
| Score prediction | Có (2W/4W/8W/12W) |
| Time management | Có |
| Mock tests | Có (Mini/Weekly/Monthly/Full) |
| Benchmarks | Có (400/500/650/750/850) |
| Reporting | Có (update TOEIC_PROGRESS.md, TOEIC_MISTAKES.md) |
| Strict mode | Có — conservative scoring, no inflation |
| **Điểm mạnh** | Cực kỳ đầy đủ, professional grade |
| **Điểm yếu** | Không có hướng dẫn về cách generate câu hỏi từ question bank |

### 4.3 toeic-rpg-gamemaster

**File:** `skills/toeic-rpg-gamemaster/CLAUDE.md`

| Khía cạnh | Đánh giá |
|----------|---------|
| Role | Game Master — biến TOEIC thành RPG |
| World mapping | Đủ 7 parts → 7 dungeon names |
| XP system | Có (Easy+10/Medium+20/Hard+30/Perfect+50/Boss+100) |
| Level system | Có (7 levels, 0→4000 XP) |
| Daily quests | Có (5 quest types/ngày) |
| Feedback rules | Có (4-bước, không chỉ nói "Wrong") |
| Progress tracking | Có (update 3 files: PROGRESS/MISTAKES/VOCABULARY) |
| Adaptive learning | Có (nếu fail Part 2 nhiều → thêm Part 2) |
| **Điểm mạnh** | Motivation mechanism mạnh, phù hợp với IT learner |
| **Điểm yếu** | Level 7 cần 4000 XP — với 60-90 phút/ngày và ~100 XP/ngày, mất ~40 ngày. Nên có level cap hợp lý hơn |

**Phối hợp 3 skills:**
```
Learner gửi kết quả
        ↓
toeic-examiner → chấm điểm → TOEIC_MISTAKES.md
        ↓
toeic-rpg-gamemaster → XP/Achievement → TOEIC_ACHIEVEMENTS.md
        ↓
toeic-coach → đọc mistakes → tạo bài học adaptive hôm sau
```
Pipeline này được thiết kế tốt, 3 skills không chồng chéo.

---

## 5. GAP ANALYSIS

| Component | Có | Thiếu | Độ ưu tiên |
|-----------|-----|-------|-----------|
| PDF nguồn | 3 PDFs (1,025 MB) | — | — |
| Audio Part 1 | 60 file MP3 (câu lẻ) + 10 (nguyên part) | — | — |
| Audio Part 2 | ~250 file MP3 | — | — |
| Audio Part 3-4 | ~268 file MP3 | — | — |
| Ảnh Part 1 | 60 JPGs + JSON mapping | Không có đáp án + transcript | CRITICAL |
| Part 1 JSON (mapping) | 60 entries | Transcript, correct answer | CRITICAL |
| Scans PDF Listening | 144 PNG | — (đã có) | — |
| Part 2-7 question bank | 0 | Toàn bộ | HIGH |
| TRANSCRIPT.pdf extract | 0 | Script OCR/extract | HIGH |
| READING.pdf extract | 0 | Script OCR/extract | HIGH |
| Skills (3 files) | 100% | — | — |
| AI Context docs | 9 files | — | — |
| Tracking files | 6 files | Finance Set 1 vocab chưa sync | MEDIUM |
| Day 1 lab | Hoàn chỉnh | AutoSave chưa add | LOW |
| Day 2 lab | Tạo xong | Learner chưa làm | — |
| Day 3-84 labs | 0 | 82 ngày còn lại | HIGH (on-demand) |
| Week 1 Boss | 0 | week1_boss.html (cần 2026-06-28) | HIGH |
| PART1/ lessons | 0 | lesson files | MEDIUM |
| PART2-7/ lessons | 0 | lesson files | HIGH |
| WEEKLY_BOSS/ | 0 | 12 boss tests | MEDIUM |
| RESULTS/ | 0 JSONs | Learner chưa submit | — |
| ETS_BANK answers | 0 | Đáp án cho 60 Part 1 questions | CRITICAL |
| Part 2-7 answers | 0 | Toàn bộ đáp án | CRITICAL |

---

## 6. ĐỀ XUẤT KIẾN TRÚC

### Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
│  raw/                                                               │
│  ├── ETS 2026 LISTENING.pdf (209MB)                                 │
│  ├── ETS 2026 READING.pdf (337MB)                                   │
│  ├── ETS 2026 TRANSCRIPT.pdf (478MB)                                │
│  ├── Audio/ (578 MP3 files)                                         │
│  └── ETS_BANK/ (60 JPGs + 144 PNGs + part1.json)                  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ scripts/
┌─────────────────────────────────────────────────────────────────────┐
│                      QUESTION BANK LAYER                             │
│  English/ETS_BANK/                                                  │
│  ├── part1.json  (60 entries — DONE)                               │
│  ├── part2.json  (250 entries — TODO)                              │
│  ├── part3.json  (130 entries — TODO)                              │
│  ├── part4.json  (~ 80 entries — TODO)                             │
│  ├── part5.json  (400 entries — TODO)                              │
│  ├── part6.json  (~160 entries — TODO)                             │
│  ├── part7.json  (~220 entries — TODO)                             │
│  ├── images/part1/ (60 JPGs — DONE)                               │
│  ├── images/part2/ (không cần ảnh)                                 │
│  └── audio/       (symlink hoặc copy từ raw/Audio/)                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       TEST ENGINE LAYER                              │
│  English/DAILY_QUESTS/dayN.html                                     │
│  - Đọc JSON từ ETS_BANK → render câu hỏi                           │
│  - Web Speech API TTS (audio)                                       │
│  - Inline <img> từ images/part1/ (Part 1)                          │
│  - Auto-save kết quả → RESULTS/*.json                               │
│  English/WEEKLY_BOSS/weekN_boss.html                                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       SCORING LAYER                                  │
│  toeic-examiner skill                                               │
│  - Đọc RESULTS/*.json                                               │
│  - Tính Estimated TOEIC Listening/Reading/Total                     │
│  - Error analysis (6 loại)                                          │
│  - Score prediction (2W/4W/8W/12W)                                 │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PROGRESS TRACKING LAYER                           │
│  English/                                                           │
│  ├── PLAYER_PROFILE.md (Level/XP/Streak)                           │
│  ├── TOEIC_PROGRESS.md (score history)                             │
│  ├── TOEIC_MISTAKES.md (error log)                                 │
│  ├── TOEIC_VOCABULARY.md (vocab tracker)                           │
│  └── TOEIC_ACHIEVEMENTS.md (badges)                                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        COACH LAYER                                   │
│  toeic-coach + toeic-rpg-gamemaster skills                         │
│  - Đọc MISTAKES → tạo adaptive lesson hôm sau                      │
│  - Trao XP + Achievement                                           │
│  - Tạo dayN+1.html on demand                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. ROADMAP THỰC HIỆN

### Phase 1 — Foundation (Tuần 1–2, đang làm)

**Mục tiêu:** Hoàn thiện cơ sở hạ tầng học tập

| Việc cần làm | Ưu tiên | Deadline |
|-------------|--------|---------|
| Learner làm `day2_grammar_lab.html` → sync progress | CRITICAL | 2026-06-24 |
| Sync 20 từ Finance Set 1 → `TOEIC_VOCABULARY.md` | HIGH | 2026-06-24 |
| Tạo `day3.html` (Passive Voice + Office Vocab) | HIGH | 2026-06-25 |
| Tạo `WEEKLY_BOSS/week1_boss.html` | HIGH | 2026-06-28 |
| Thêm AutoSave vào `day1.html` + `day1_bonus_pronouns.html` | MEDIUM | Tuần 1 |
| Tạo `PART1/lesson_01.md` (Part 1 strategy) | MEDIUM | Tuần 1 |

### Phase 2 — Data Extraction (Tuần 2–3)

**Mục tiêu:** Xây dựng question bank từ raw data

| Việc cần làm | Công nghệ | Output |
|-------------|----------|-------|
| Extract đáp án Part 1 từ TRANSCRIPT.pdf | PyMuPDF + regex | Thêm `answer` field vào `part1.json` |
| Extract Part 2 text + đáp án từ TRANSCRIPT.pdf | PyMuPDF + regex | `part2.json` |
| Extract Part 5 từ READING.pdf | PyMuPDF + pdfplumber | `part5.json` |
| Viết `scripts/extract_answers.py` | Python | Answer keys cho cả 10 tests |
| Xác minh Test 07 audio (thiếu 2 file?) | File check | Confirm hoặc recount |

**Thực tế:** TRANSCRIPT.pdf (478 MB) có transcript đầy đủ. Cần script OCR/extract thông minh vì PDF có thể là scan (không phải text-selectable).

### Phase 3 — Question Bank (Tuần 3–5)

**Mục tiêu:** JSON database cho tất cả 7 parts

| Part | Số câu/test | 10 tests | Ưu tiên |
|------|------------|---------|--------|
| Part 1 | 6 | 60 câu | HIGH (ảnh đã có, thiếu đáp án) |
| Part 2 | 25 | 250 câu | HIGH (audio đã có) |
| Part 3 | 39 | 390 câu | MEDIUM |
| Part 4 | 30 | 300 câu | MEDIUM |
| Part 5 | 30 | 300 câu | HIGH (Reading section) |
| Part 6 | 16 | 160 câu | MEDIUM |
| Part 7 | 54 | 540 câu | HIGH (nhiều điểm nhất) |
| **Total** | **210** | **2,000 câu** | |

### Phase 4 — Test Engine (Tuần 5–8)

**Mục tiêu:** HTML labs dùng dữ liệu thật từ ETS_BANK

| Việc cần làm | Mô tả |
|-------------|-------|
| Nâng cấp `day1.html` | Dùng ảnh thật từ `ETS_BANK/images/part1/` thay SVG |
| Tạo Part 2 drill template | Dùng `<audio>` tag với MP3 thật |
| Tạo Part 5 drill template | Text-only, dùng `part5.json` |
| Standardize HTML template | Một template base cho tất cả parts |
| Full Mock Test engine | Ghép tất cả 7 parts, 200 câu, timed |

### Phase 5 — Learning Analytics (Tuần 8–12)

**Mục tiêu:** Hệ thống phân tích học sâu

| Việc cần làm | Mô tả |
|-------------|-------|
| Vocabulary mastery tracker | Spaced repetition (Leitner box) |
| Error pattern analysis | Tự động nhận dạng recurring mistakes |
| Score prediction model | Dựa trên accuracy trajectory |
| Weekly performance dashboard | HTML chart hiển thị progress |
| Full simulation (200 câu, 2 giờ) | Test thực chiến Week 9, 11, 12 |

---

## 8. PHÂN TÍCH RỦI RO

### Rủi ro 1: Chất lượng dữ liệu OCR/extract — MỨC ĐỘ CAO

**Mô tả:** TRANSCRIPT.pdf (478 MB) và READING.pdf (337 MB) có thể là PDF scan (ảnh), không phải text-selectable. Nếu vậy, cần OCR (Tesseract, Google Vision, hoặc GPT-4V) để extract text.

**Hậu quả:** Nếu OCR không chính xác, đáp án sai → toàn bộ question bank bị lỗi → học sai.

**Biện pháp:**
- Kiểm tra ngay: mở PDF bằng PyMuPDF, dùng `page.get_text()` — nếu trả về text thì OK
- Nếu là scan: dùng Google Document AI hoặc Claude Vision để extract
- Luôn manual verify mẫu 10 câu trước khi dùng

### Rủi ro 2: Audio không khớp với câu hỏi — MỨC ĐỘ TRUNG BÌNH

**Mô tả:** Audio "Câu lẻ" được đánh số (`Test_01-01.mp3` = câu 1) nhưng không có confirmation rằng file MP3 số N thực sự là câu N trong sách. Đặc biệt Test 07 thiếu 2 file.

**Biện pháp:**
- Nghe thử `Test_01-01.mp3` và đối chiếu với câu 1 trong sách
- Kiểm tra đầy đủ Test 07 (52 thay vì 54 file)

### Rủi ro 3: Pipeline ảnh Part 1 chưa có đáp án — MỨC ĐỘ CAO

**Mô tả:** Đã extract được 60 ảnh Part 1 nhưng `part1.json` chỉ có `test/question/image`, không có `correct_answer` (A/B/C/D) và không có `transcript`. Không thể tạo interactive quiz nếu không có đáp án.

**Biện pháp:**
- Extract đáp án từ TRANSCRIPT.pdf hoặc READING.pdf answer key section
- Hoặc: nhập thủ công từ sách (60 câu × 10 tests = 60 đáp án)

### Rủi ro 4: Phạm vi quá rộng (Scope Creep) — MỨC ĐỘ CAO

**Mô tả:** Muốn build đầy đủ 7 parts × 10 tests = 2,000 câu là công việc lớn. Learner đang cần học ngay từ ngày mai (Day 3), không thể đợi infrastructure hoàn chỉnh.

**Biện pháp:**
- Nguyên tắc "Just In Time": chỉ tạo nội dung đủ cho tuần hiện tại
- Week 1: Part 5 text-only (không cần infrastructure phức tạp)
- Week 2+: Dần dần bổ sung Part 1 (ảnh thật), Part 2 (audio thật)

### Rủi ro 5: Phụ thuộc vào File System Access API — MỨC ĐỘ TRUNG BÌNH

**Mô tả:** Auto-save trong `day2_grammar_lab.html` dùng File System Access API, chỉ hoạt động trên Chrome/Edge. Firefox không support.

**Biện pháp:**
- Fallback: học viên copy-paste kết quả hoặc screenshot
- Thêm download JSON button như phương án dự phòng

### Rủi ro 6: AI Context drift qua nhiều sessions — MỨC ĐỘ TRUNG BÌNH

**Mô tả:** Mỗi session AI mới cần đọc 4–5 file context để restore state. Nếu không đọc đủ hoặc đọc file cũ, sẽ tạo nội dung trùng lặp hoặc không phù hợp.

**Biện pháp:**
- HANDOFF.md và MEMORY.md là nguồn truth duy nhất — đã có
- Startup Procedure đã được định nghĩa trong CLAUDE.md
- Nên thêm "last updated" timestamp vào mọi tracking file

---

## 9. KHUYẾN NGHỊ TRƯỚC KHI VIẾT CODE

### Khuyến nghị 1: Kiểm tra text-selectability của PDF (Ngay bây giờ)

Chạy thử đoạn Python này trước khi viết bất kỳ extraction script nào:

```python
import fitz
doc = fitz.open("raw/ETS 2026 TRANSCRIPT.pdf")
page = doc[10]  # trang 11
text = page.get_text()
print(repr(text[:500]))  # nếu có text = PDF dạng text, nếu rỗng = PDF scan
```

Kết quả quyết định toàn bộ strategy extraction (text parsing vs. OCR).

### Khuyến nghị 2: Nhập đáp án Part 1 thủ công (Ưu tiên cao)

60 đáp án Part 1 (A/B/C/D) × 10 tests = 60 dòng. Nhập thủ công mất 30 phút nhưng đảm bảo độ chính xác 100%. Thêm vào `part1.json`:

```json
{
  "test": 1, "question": 1, "image": "test1_q1.jpg",
  "answer": "B",
  "transcript": "(A) ... (B) ... (C) ... (D) ..."
}
```

### Khuyến nghị 3: Chuẩn hóa đường dẫn (Ngay bây giờ)

Hiện tại có sự không nhất quán giữa:
- `raw/ETS_BANK/` (nơi file thực sự nằm)
- `English/ETS_BANK/` (nơi scripts output, nhưng thực tế không tồn tại dưới English/)

Quyết định ngay: tất cả processed data nên ở `raw/ETS_BANK/` hay `English/ETS_BANK/`? Sau đó cập nhật tất cả scripts.

### Khuyến nghị 4: Không phá vỡ luồng học hiện tại

Learner đang ở Day 2. Đừng để engineering work làm delay việc học:
- Day 3–7 có thể tạo bằng text-only Part 5 (không cần infrastructure)
- ETS_BANK chỉ cần sẵn sàng từ Week 2–3 trở đi
- Ưu tiên: `day3.html` → `week1_boss.html` → sau đó mới `part2.json`

### Khuyến nghị 5: Viết unit test cho scripts

Trước khi chạy script extract trên toàn bộ 10 tests:
1. Test trên 1 test duy nhất (ví dụ Test 01)
2. Manual verify: so sánh output với sách
3. Sau đó mới chạy batch cho 10 tests

### Khuyến nghị 6: Tạo `scripts/verify_assets.py`

Script kiểm tra tính toàn vẹn của tài sản:
- Xác nhận 578 audio files có mặt đầy đủ
- Xác nhận Test 07 thực sự thiếu 2 files và files nào
- Xác nhận 60 ảnh Part 1 không bị corrupt
- Output: danh sách assets OK / MISSING / CORRUPT

### Khuyến nghị 7: Không tạo Part 2-7 JSON cho đến khi có transcript

Tạo JSON rỗng (`part2.json`) với cấu trúc placeholder là không có giá trị. Chỉ tạo JSON khi đã có nội dung thực từ extraction.

---

## 10. TỔNG KẾT ĐÁNH GIÁ

### Điểm mạnh của hệ thống hiện tại

1. **Infrastructure hoàn chỉnh** — 3 skills, 6 tracking files, AI context docs, startup procedure đều đã có
2. **Part 1 pipeline duy nhất đã hoàn chỉnh** — 60 ảnh đã extract, JSON mapping đã có
3. **Tech stack đã được chọn đúng** — Web Speech API, File System Access API, vanilla JS (không dependency)
4. **Design system nhất quán** — Dark RPG theme đẹp, motivating
5. **Gamification thực sự hoạt động** — XP/Level/Achievement đã được implement
6. **Tài liệu gốc phong phú** — 578 MP3, 3 PDFs × 1TB content gốc từ ETS

### Điểm yếu cần giải quyết ngay

1. **Part 1 JSON thiếu đáp án** — Ảnh có nhưng không thể tạo quiz nếu không có A/B/C/D
2. **Parts 2-7 hoàn toàn trống** — Không có question bank, không có lesson files
3. **TOEIC_VOCABULARY.md chưa sync** — 20 từ Finance Set 1 từ Day 1 chưa được ghi nhận
4. **scripts/crop_part1.py obsolete** — Không nên dùng, đã được thay thế bởi build_part1_bank.py
5. **Không có đường dẫn chuẩn cho ETS_BANK** — Nhập nhằng giữa raw/ và English/

### Trạng thái tổng thể: ~15% hoàn thành về dài hạn

```
Infrastructure:        ████████████  100%
Part 1 pipeline:       █████████░░░   85% (thiếu đáp án)
Day 1-2 labs:          ████████████  100% (tạo xong)
Day 3-84 labs:         ░░░░░░░░░░░░    0% (on-demand)
Parts 2-7 content:     ░░░░░░░░░░░░    0%
Question banks:        ██░░░░░░░░░░   15% (chỉ Part 1 ảnh, thiếu đáp án)
Weekly bosses:         ░░░░░░░░░░░░    0%
Full mock tests:       ░░░░░░░░░░░░    0%
Vocabulary (9 words):  █░░░░░░░░░░░    5% (target 1200 words)
```

**Mức hoàn thiện phù hợp với giai đoạn:** Đây là ngày thứ 2 trong 84 ngày. Không có gì sai với 15% — mọi thứ cần thiết cho ngày học hiện tại đã sẵn sàng.

---

*Báo cáo này được tạo ngày 2026-06-24 bởi Claude Code (audit READ-ONLY).*  
*Không có file nào bị sửa đổi trong quá trình audit.*
