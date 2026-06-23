# Project Overview — TOEIC Learning Lab

## Mục tiêu hệ thống

Giúp học viên người Việt **Duong** (IT professional) đạt **TOEIC L&R 650+** từ mức baseline ~250–400 điểm trong **12 tuần** (2026-06-23 → 2026-09-15), học 60–90 phút/ngày.

---

## Cách vận hành

Hệ thống hoạt động theo workflow 6 bước:

```
1. Assess   → Placement test + weekly check-in
2. Teach    → Daily lesson HTML lab (4 quests/ngày)
3. Practice → TOEIC-style drills theo từng part
4. Evaluate → toeic-examiner chấm điểm + phân tích lỗi
5. Update   → Cập nhật PLAYER_PROFILE, PROGRESS, MISTAKES, VOCABULARY
6. Adapt    → Điều chỉnh kế hoạch dựa trên kết quả thực tế
```

Mỗi ngày học viên nhận 1 file HTML interactive (`DAILY_QUESTS/dayN.html`) gồm 4 quests:
- Quest 1: Vocabulary (20 từ mới theo chủ đề tuần)
- Quest 2: Grammar Dungeon (topic của tuần)
- Quest 3: Listening Part (Part 1–4 luân phiên)
- Quest 4: Reading/Grammar Drill (Part 5–7)

---

## Cấu trúc học tập

### Giai đoạn 1 — Foundation (Week 1–4)
- Vocabulary: 100 từ/tuần, các chủ đề Business, Office, Finance, HR
- Grammar: Word Form → Verb Tense → Passive Voice → Subject-Verb Agreement
- Parts: Part 1, Part 2, Part 5 tập trung

### Giai đoạn 2 — Skill Building (Week 5–8)
- Vocabulary: 80–100 từ/tuần, Logistics, Customer Service, Technology, Mixed
- Grammar: Conjunctions → Relative Clauses → Gerunds → Conditionals
- Parts: Part 3, Part 4, Part 6, Part 7 thêm vào

### Giai đoạn 3 — Test Simulation (Week 9–12)
- Vocabulary: 20–60 từ/tuần (consolidation)
- Full mock tests, speed reading, test strategy
- Mục tiêu cuối: TOEIC 650+

---

## Score Milestones

| Milestone | Score | ETA |
|-----------|-------|-----|
| Baseline | 250–400 | 2026-06-23 |
| Checkpoint 1 | 450 | 2026-07-21 (Week 4) |
| Checkpoint 2 | 550 | 2026-08-17 (Week 8) |
| Final Goal | 650+ | 2026-09-15 (Week 12) |

---

## Nguyên tắc thiết kế

- **Dark RPG theme**: background `#0a0f1e`, accent blue/purple/gold
- **Giải thích bằng tiếng Việt** (người học là người Việt)
- **Không reveal đáp án trước** — buộc học viên suy nghĩ
- **XP + Level + Achievement** để giữ motivation
- **Dạy TOEIC, không dạy tiếng Anh tổng quát**
- **Adapt theo kết quả** — sai nhiều Part 5 → tăng Part 5 content hôm sau
