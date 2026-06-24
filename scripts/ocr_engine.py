# scripts/ocr_engine.py
# Shared OCR utility used by all build_partN_bank scripts.
# Uses EasyOCR (English). Falls back to pytesseract if easyocr not available.

import numpy as np
import cv2

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        try:
            import easyocr
            _reader = easyocr.Reader(["en"], gpu=False, verbose=False)
            print("[ocr_engine] Using EasyOCR")
        except ImportError:
            _reader = "tesseract"
            print("[ocr_engine] EasyOCR not available, using pytesseract")
    return _reader


def preprocess(img: np.ndarray) -> np.ndarray:
    """Denoise + contrast enhance for scan with watermark."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # CLAHE contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    # Slight sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    return sharpened


def ocr_image(img: np.ndarray) -> str:
    """Run OCR on a BGR numpy image, return lines sorted by Y position."""
    reader = get_reader()
    processed = preprocess(img)

    if reader == "tesseract":
        import pytesseract
        return pytesseract.image_to_string(processed, config="--psm 6")

    # Use detail=True to get bounding boxes, sort by Y so reading order is correct
    results = reader.readtext(processed, detail=True, paragraph=False)
    # Sort by top-left Y coordinate
    results.sort(key=lambda r: r[0][0][1])
    return "\n".join(r[1] for r in results)


def ocr_two_column(img: np.ndarray) -> str:
    """
    For 2-column page layouts (Part 3, 4, 5).
    Split image down the middle, OCR each half separately, concatenate.
    Left column text comes first, then right column.
    """
    h, w = img.shape[:2]
    left  = img[:, :w // 2]
    right = img[:, w // 2:]
    return ocr_image(left) + "\n" + ocr_image(right)


def render_pdf_page(doc, page_idx: int, scale: float = 2.5) -> np.ndarray:
    """Render a PyMuPDF page to BGR numpy array."""
    import fitz
    page = doc[page_idx]
    pix  = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    arr  = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
