# scripts/build_part1_bank.py
# Extracts Part 1 photographs from ETS_2026_LISTENING.pdf
# Output: ETS_BANK/images/part1/test{N}_q{Q}.jpg + part1.json

import fitz
import cv2
import json
import numpy as np
from pathlib import Path

PDF_PATH   = Path("../raw/ETS 2026 LISTENING.pdf")
OUTPUT_DIR = Path("../English/ETS_BANK/images/part1")
JSON_PATH  = Path("../English/ETS_BANK/part1.json")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Known structure ──────────────────────────────────────────────────────────
# 10 tests, Part 1 directions page at PDF pages: 2,16,30,44,58,72,86,100,114,128
# (0-indexed: 1,15,29,43,57,71,85,99,113,127)
# Photo pages = directions+1, directions+2, directions+3
DIRECTIONS_PAGES = [1 + i * 14 for i in range(10)]   # 0-indexed
NUM_TESTS = 10
QUESTIONS_PER_PAGE = 2
PAGES_PER_PART1 = 3   # → 6 questions per test

# ── Render PDF ───────────────────────────────────────────────────────────────
print("Opening PDF...")
doc = fitz.open(str(PDF_PATH))

def render_page(page_idx):
    page = doc[page_idx]
    pix  = page.get_pixmap(matrix=fitz.Matrix(3, 3))
    arr  = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def find_two_photos(img):
    """Return top 2 large photo bounding boxes sorted top→bottom."""
    h, w = img.shape[:2]
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = []
    # Try progressively lower thresholds to handle watermarked pages
    for tval in [240, 220, 200]:
        blur   = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, tval, 255, cv2.THRESH_BINARY_INV)[1]
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        candidates = []
        for c in cnts:
            x, y, cw, ch = cv2.boundingRect(c)
            area = cw * ch
            if area < w * h * 0.06:
                continue
            if area > w * h * 0.65:
                continue
            aspect = cw / ch
            if not (0.5 < aspect < 4.0):
                continue
            candidates.append((y, x, cw, ch, area))

        candidates.sort()
        # Pick top 2 by area among top-positioned candidates
        if len(candidates) >= 2:
            results = candidates[:2]
            break

    return [(x, y, cw, ch) for (y, x, cw, ch, _) in results]

# ── Process each test ────────────────────────────────────────────────────────
mapping = []

for test_idx, dir_page in enumerate(DIRECTIONS_PAGES):
    test_num = test_idx + 1
    print(f"\n-- Test {test_num} (directions=PDF p{dir_page+1}) --")
    q = 1

    for offset in range(1, PAGES_PER_PART1 + 1):
        page_idx = dir_page + offset
        print(f"  Page {page_idx + 1} ...", end=" ")

        filename_a = f"test{test_num}_q{q}.jpg"
        filename_b = f"test{test_num}_q{q+1}.jpg"
        both_exist = (OUTPUT_DIR / filename_a).exists() and (OUTPUT_DIR / filename_b).exists()

        if both_exist:
            print(f"[skip] {filename_a} & {filename_b} exist")
            mapping.append({"test": test_num, "question": q,   "image": filename_a})
            mapping.append({"test": test_num, "question": q+1, "image": filename_b})
            q += 2
            continue

        img    = render_page(page_idx)
        boxes  = find_two_photos(img)

        if len(boxes) < 2:
            print(f"WARNING: only {len(boxes)} photo(s) found on page {page_idx+1}")

        for i, (x, y, cw, ch) in enumerate(boxes):
            qi       = q + i
            filename = f"test{test_num}_q{qi}.jpg"
            out_path = OUTPUT_DIR / filename

            if out_path.exists():
                print(f"[skip] {filename}", end=" ")
            else:
                crop = img[y:y+ch, x:x+cw]
                cv2.imwrite(str(out_path), crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
                print(f"[save] {filename}", end=" ")

            mapping.append({"test": test_num, "question": qi, "image": filename})

        print()
        q += len(boxes)

# ── Write JSON ───────────────────────────────────────────────────────────────
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f"\nDone. {len(mapping)} entries → {JSON_PATH}")
