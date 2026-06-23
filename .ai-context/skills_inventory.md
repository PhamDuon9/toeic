# Skills Inventory

## Tổng quan

Hệ thống có **3 skills** chuyên biệt, phối hợp theo từng giai đoạn học.

---

## 1. toeic-coach

**File:** `skills/toeic-coach/CLAUDE.md`
**Mục đích:** Dạy học, lập kế hoạch, giải thích ngữ pháp và từ vựng

**Đầu vào:**
- Kết quả placement test / kết quả daily quest
- Yêu cầu từ học viên ("Give me Day N lesson")
- Dữ liệu điểm yếu từ TOEIC_MISTAKES.md

**Đầu ra:**
- 12-week study plan
- Daily lesson content
- Vocabulary sets (20 từ/ngày theo chủ đề)
- Grammar explanations với TOEIC traps
- Adaptive feedback

**Liên hệ với TOEIC:**
- Dạy Vocabulary (Business, Finance, Office, HR, Logistics, Tech, Customer Service)
- Dạy Grammar (Tenses, Passive, Relative Clauses, Conjunctions, Gerunds, Conditionals)
- Tạo drills cho Part 1–7
- Không dạy tiếng Anh tổng quát — chỉ TOEIC

**Quy tắc cốt lõi:**
- Không reveal đáp án trước
- Giải thích lỗi sai: Tại sao sai + Tại sao đúng + TOEIC trap + Ví dụ tương tự
- Luôn adapt lesson theo kết quả gần nhất

---

## 2. toeic-examiner

**File:** `skills/toeic-examiner/CLAUDE.md`
**Mục đích:** Đánh giá khách quan theo chuẩn ETS — không phải giáo viên, là giám khảo

**Đầu vào:**
- Câu trả lời của học viên
- Kết quả bài test

**Đầu ra:**
- Score Summary (Correct/Incorrect/Accuracy%)
- Estimated TOEIC Listening + Reading + Total
- Error analysis (Grammar/Vocab/Listening/Reading/Time/Careless)
- Score prediction (2W/4W/8W/12W)
- Strengths & Weaknesses report

**Liên hệ với TOEIC:**
- Tạo TOEIC-style questions (Easy/Medium/Hard)
- Mini Test, Weekly Test, Monthly Test, Full Simulation
- So sánh với benchmark TOEIC 400/500/650/750/850
- Update TOEIC_PROGRESS.md và TOEIC_MISTAKES.md

**Quy tắc cốt lõi:**
- Strict mode: không inflate điểm, không lạc quan quá mức
- Conservative scoring — accuracy > motivation

---

## 3. toeic-rpg-gamemaster

**File:** `skills/toeic-rpg-gamemaster/CLAUDE.md`
**Mục đích:** Gamification — biến luyện thi thành RPG để giữ engagement

**Đầu vào:**
- Kết quả quest hàng ngày
- XP hiện tại của học viên

**Đầu ra:**
- XP awards (+10/+20/+30 theo độ khó, +50 perfect streak, +100 boss victory)
- Level-up notifications
- Achievement badges
- Quest names (Photo Detective, Grammar Dungeon, v.v.)
- Daily quest structure (5 quests/ngày)

**Liên hệ với TOEIC:**
- Đặt tên RPG cho từng Part:
  - Part 1: Photo Detective
  - Part 2: Quick Response Arena
  - Part 3: Conversation Investigation
  - Part 4: Broadcast Intelligence
  - Part 5: Grammar Dungeon
  - Part 6: Document Repair Workshop
  - Part 7: Corporate Intelligence Mission

**Level System:**
| Level | XP | Tên |
|-------|----|-----|
| 1 | 0 | TOEIC Rookie |
| 2 | 100 | Word Hunter |
| 3 | 250 | Grammar Warrior |
| 4 | 500 | Part 5 Slayer |
| 5 | 1000 | TOEIC Explorer |
| 6 | 2000 | Business English Pro |
| 7 | 4000 | TOEIC Master |

---

## Cách skills phối hợp

```
Học viên gửi kết quả
        ↓
toeic-examiner → chấm điểm, phân tích lỗi → TOEIC_MISTAKES.md
        ↓
toeic-rpg-gamemaster → trao XP, achievement → TOEIC_ACHIEVEMENTS.md
        ↓
toeic-coach → đọc kết quả + mistakes → tạo bài học hôm sau (adapt)
```
