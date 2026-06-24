# scripts/build_part2_bank.py
# Part 2 has no printed question text — audio only.
# Generate skeleton JSON from known structure: Q7-31 per test, 10 tests.

import json
from pathlib import Path

OUTPUT_DIR = Path("../English/ETS_BANK")
JSON_PATH  = OUTPUT_DIR / "part2.json"
AUDIO_BASE = Path("../raw/Audio/LISTENING/Camle le")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

QUESTIONS_PER_TEST = 25
FIRST_QUESTION     = 7   # Q1-6 = Part 1

entries = []
for test_num in range(1, 11):
    for q_offset in range(QUESTIONS_PER_TEST):
        q = FIRST_QUESTION + q_offset
        global_q = q  # within-test number
        audio_file = f"Test_{test_num:02d}-{global_q:02d}.mp3"
        entries.append({
            "test":    test_num,
            "question": q,
            "audio":   audio_file,
            "answer":  None   # to be filled manually
        })

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print(f"Done. {len(entries)} entries -> {JSON_PATH}")
