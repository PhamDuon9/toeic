# scripts/crop_part1.py

import cv2
from pathlib import Path

INPUT_DIR = Path("../English/ETS_BANK/scans")
OUTPUT_DIR = Path("../English/ETS_BANK/images/part1_crop")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

counter = 1

for image_file in INPUT_DIR.glob("*.png"):

    img = cv2.imread(str(image_file))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.threshold(
        blur,
        240,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        area = w * h

        if area < 300000:
            continue

        crop = img[y:y+h, x:x+w]

        filename = OUTPUT_DIR / f"part1_{counter}.jpg"

        cv2.imwrite(str(filename), crop)

        counter += 1

print("Done")