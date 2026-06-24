# scripts/extract_part1.py

import fitz
from pathlib import Path

pdf_file = "../raw/ETS_2026_LISTENING.pdf"
output_dir = Path("../English/ETS_BANK/scans")

output_dir.mkdir(parents=True, exist_ok=True)

doc = fitz.open(pdf_file)

for page_num in range(len(doc)):
    page = doc[page_num]

    pix = page.get_pixmap(matrix=fitz.Matrix(3,3))

    output_file = output_dir / f"page_{page_num+1}.png"

    pix.save(str(output_file))

print("Done")