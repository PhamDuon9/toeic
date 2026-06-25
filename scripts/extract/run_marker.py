"""
Run Marker OCR on ETS 2026 PDFs.

Usage:
    python scripts/extract/run_marker.py [reading|transcript|listening|all]

Default: all (in order: READING → TRANSCRIPT → LISTENING)

Outputs to extracted/{READING,TRANSCRIPT,LISTENING}/
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
VENV_PYTHON = ROOT / ".venv-marker" / "Scripts" / "python.exe"
RAW = ROOT / "raw"
OUT = ROOT / "extracted"

PDFS = {
    "reading":    (RAW / "ETS 2026 READING.pdf",    OUT / "READING"),
    "transcript": (RAW / "ETS 2026 TRANSCRIPT.pdf",  OUT / "TRANSCRIPT"),
    "listening":  (RAW / "ETS 2026 LISTENING.pdf",   OUT / "LISTENING"),
}


def run_marker(pdf_path: Path, output_dir: Path) -> bool:
    output_dir.mkdir(parents=True, exist_ok=True)
    md_file = output_dir / (pdf_path.stem + ".md")

    if md_file.exists():
        print(f"[skip] {md_file} already exists. Delete it to re-run.")
        return True

    print(f"\n{'='*60}")
    print(f"Running Marker on: {pdf_path.name}")
    print(f"Output directory:  {output_dir}")
    print(f"{'='*60}")

    marker_exe = VENV_PYTHON.parent / "marker_single.exe"
    cmd = [
        str(marker_exe),
        str(pdf_path),
        "--output_dir", str(output_dir),
        "--output_format", "markdown",
    ]

    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode != 0:
        print(f"[ERROR] Marker failed on {pdf_path.name} (exit code {result.returncode})")
        return False

    print(f"[OK] {pdf_path.name} → {output_dir}")
    return True


def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if not VENV_PYTHON.exists():
        print(f"[ERROR] Python not found: {VENV_PYTHON}")
        print("Run: uv venv .venv-marker --python 3.12 && .venv-marker\\Scripts\\pip install marker-pdf")
        sys.exit(1)

    order = ["reading", "transcript", "listening"] if target == "all" else [target]

    for name in order:
        if name not in PDFS:
            print(f"[ERROR] Unknown target: {name}. Choose: reading, transcript, listening, all")
            sys.exit(1)
        pdf_path, output_dir = PDFS[name]
        if not pdf_path.exists():
            print(f"[ERROR] PDF not found: {pdf_path}")
            sys.exit(1)
        if not run_marker(pdf_path, output_dir):
            sys.exit(1)

    print("\nAll done. Run next: python scripts/extract/parse_reading.py")


if __name__ == "__main__":
    main()
