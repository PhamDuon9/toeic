"""
Parse extracted/LISTENING/ETS 2026 LISTENING/ETS 2026 LISTENING.md
→ question_bank/part1.json, part2.json, part3.json, part4.json
Part 1 images copied from Marker output (filter tiny decorative images by size).

Marker output format:
- Questions: "- **N.** stem"  or "- N. stem"
- Options:   "  - (A) text"  (indented sub-list)
- Tables:    markdown pipe tables (visual aids)
- Images:    ![](_page_N_Picture_M.jpeg)
"""

import re
import json
import shutil
from pathlib import Path

ROOT        = Path(__file__).parent.parent.parent
MD_FILE     = ROOT / "extracted" / "LISTENING" / "ETS 2026 LISTENING" / "ETS 2026 LISTENING.md"
IMG_SRC_DIR = ROOT / "extracted" / "LISTENING" / "ETS 2026 LISTENING"
BANK_DIR    = ROOT / "question_bank"
IMG_DST_DIR = BANK_DIR / "images" / "part1"
BANK_DIR.mkdir(parents=True, exist_ok=True)
IMG_DST_DIR.mkdir(parents=True, exist_ok=True)

# ── Regexes ──────────────────────────────────────────────────────────────────
# Primary: "- **N.** stem" or "- N. stem" (standard Marker list format)
RE_Q         = re.compile(r"^[-*]\s+\*{0,2}(\d{1,3})\.\*{0,2}\s*(.*)")
# Fallback: "N. stem" or "**N.** stem" at start of line (no leading dash)
RE_Q_PLAIN   = re.compile(r"^\*{0,2}(\d{2,3})\.\*{0,2}\s+(.*)")
RE_OPT_INDENT= re.compile(r"^\s{2,4}[-*]\s+\(([ABCD])\)\s+(.*)")
RE_OPT_PLAIN = re.compile(r"^\(([ABCD])\)\s+(.*)")
RE_IMG       = re.compile(r"!\[\]\((_page_\d+_(?:Picture|Figure)_\d+\.jpe?g)\)")
RE_TABLE_ROW = re.compile(r"^\|")
# Match "TEST 01"..."TEST 10" (2-digit or "10") anywhere in line.
# Answer key uses bare "TEST 1"/"TEST 2" (single digit) which won't match 0[1-9]|10.
RE_TEST_BOUNDARY = re.compile(r"TEST\s+(0[1-9]|10)\b")

PART1_Q = range(1, 7)
PART2_Q = range(7, 32)
PART3_Q = range(32, 71)
PART4_Q = range(71, 101)


def make_id(part: int, test: int, question: int) -> str:
    return f"p{part}-t{test:02d}-q{question:03d}"


# ── Split markdown into exactly 10 test blocks ───────────────────────────────

def split_tests(md_text: str) -> list[tuple[int, str]]:
    """Returns [(test_num, block_text), ...] for exactly 10 tests.
    Stops when test numbers go backward (= answer key section).
    Ignores within-block duplicates (same test number appearing twice in its header)."""
    lines    = md_text.splitlines()
    segments = []  # (test_num, start_line_idx)
    seen     = set()
    max_t    = 0

    for i, line in enumerate(lines):
        m = RE_TEST_BOUNDARY.search(line)
        if m:
            t = int(m.group(1))
            if t < max_t:       # going backward → answer key section, stop
                break
            if t == max_t:      # same test repeated in-block header, skip
                continue
            # new test, going forward
            max_t = t
            seen.add(t)
            segments.append((t, i))
            if len(segments) == 10:
                break

    results = []
    for idx, (t, start) in enumerate(segments):
        end   = segments[idx + 1][1] if idx + 1 < len(segments) else len(lines)
        block = "\n".join(lines[start:end])
        results.append((t, block))

    return results


# ── Part 1: copy images from Marker output ───────────────────────────────────

RE_PAGE_NUM = re.compile(r"_page_(\d+)_Picture_(\d+)\.jpe?g$", re.IGNORECASE)
MIN_SIZE_BYTES = 10_000  # real photos >10KB; tiny decorative elements <2KB

def extract_part1_images_from_marker() -> dict[tuple[int, int], str]:
    """
    Copy Part 1 images from Marker output into question_bank/images/part1/.
    Marker names them _page_N_Picture_M.jpeg on known photo pages.
    Each test: dir_page = 1+(test-1)*14 (0-indexed); photo pages = +1,+2,+3.
    Each photo page has 2 real photos; filter out tiny (<10KB) decorative images.
    Returns {(test_num, q_num): relative_path_str}
    """
    if not IMG_SRC_DIR.exists():
        print(f"[WARN] Marker output not found: {IMG_SRC_DIR}")
        return {}

    # Index all Marker images by page number, sorted by Picture number
    page_images: dict[int, list[Path]] = {}
    for f in IMG_SRC_DIR.iterdir():
        m = RE_PAGE_NUM.match(f.name)
        if m and f.stat().st_size >= MIN_SIZE_BYTES:
            pg = int(m.group(1))
            page_images.setdefault(pg, []).append(f)
    for pg in page_images:
        page_images[pg].sort(key=lambda f: int(RE_PAGE_NUM.match(f.name).group(2)))

    result = {}
    for test_idx in range(10):
        test_num = test_idx + 1
        dir_page = 1 + test_idx * 14   # 0-indexed
        q_num    = 1

        for offset in range(1, 4):      # photo pages: +1, +2, +3
            page_idx = dir_page + offset
            imgs     = page_images.get(page_idx, [])

            for src in imgs[:2]:        # at most 2 photos per page
                if q_num > 6:
                    break
                dst_name = f"t{test_num:02d}_q{q_num:03d}.jpg"
                dst_path = IMG_DST_DIR / dst_name
                if not dst_path.exists():
                    shutil.copy2(src, dst_path)
                result[(test_num, q_num)] = f"images/part1/{dst_name}"
                q_num += 1

        imgs_saved = sum(1 for (t, _) in result if t == test_num)
        print(f"    Test {test_num}: {imgs_saved}/6 Part 1 images")

    return result


def build_part1_json(img_mapping: dict) -> list[dict]:
    questions = []
    for test_num in range(1, 11):
        for q_num in range(1, 7):
            key = (test_num, q_num)
            questions.append({
                "id":         make_id(1, test_num, q_num),
                "part":       1,
                "test":       test_num,
                "question":   q_num,
                "image":      img_mapping.get(key),
                "audio":      f"audio/part1/Test_{test_num:02d}-{q_num:02d}.mp3",
                "answer":     None,
                "difficulty": None,
                "tags":       [],
            })
    return questions


# ── Part 2 skeleton ───────────────────────────────────────────────────────────

def build_part2_json() -> list[dict]:
    questions = []
    for test_num in range(1, 11):
        for q_num in range(7, 32):
            questions.append({
                "id":         make_id(2, test_num, q_num),
                "part":       2,
                "test":       test_num,
                "question":   q_num,
                "audio":      f"audio/part2/Test_{test_num:02d}-{q_num:02d}.mp3",
                "script":     None,
                "answer":     None,
                "difficulty": None,
                "tags":       [],
            })
    return questions


# ── Parts 3 & 4 parser ────────────────────────────────────────────────────────

def parse_part34(test_block: str, test_num: int, part_num: int) -> list[dict]:
    q_range = PART3_Q if part_num == 3 else PART4_Q
    start   = 32    if part_num == 3 else 71

    lines     = test_block.splitlines()
    questions = {}
    cur_q     = None
    graphic   = ""

    for line in lines:
        # Image reference → save as graphic for next question
        m_img = RE_IMG.search(line)
        if m_img:
            fn = m_img.group(1)
            graphic = (graphic + " " + fn).strip()
            continue

        # Table row → append to graphic
        if RE_TABLE_ROW.match(line.strip()):
            graphic = (graphic + "\n" + line).strip()
            continue

        # Question line (try list format first, then plain)
        m_q = RE_Q.match(line) or RE_Q_PLAIN.match(line)
        if m_q:
            q_num = int(m_q.group(1))
            if q_num in q_range:
                if q_num not in questions:
                    questions[q_num] = {
                        "stem":    m_q.group(2).strip(),
                        "options": {},
                        "graphic": graphic or None,
                    }
                    graphic = ""
                cur_q = q_num
            else:
                cur_q = None
            continue

        # Option line (indented sub-list or plain)
        m_opt = RE_OPT_INDENT.match(line)
        if not m_opt:
            m_opt = RE_OPT_PLAIN.match(line.strip())

        if m_opt and cur_q is not None and cur_q in questions:
            questions[cur_q]["options"][m_opt.group(1)] = m_opt.group(2).strip()
            continue

        # Stem continuation
        if cur_q is not None and cur_q in questions:
            stripped = line.strip()
            if (stripped and not RE_TABLE_ROW.match(stripped)
                    and not RE_IMG.search(stripped)
                    and not questions[cur_q]["options"]):
                questions[cur_q]["stem"] += " " + stripped

    # Build sorted records
    result = []
    for q_num in sorted(questions.keys()):
        if q_num not in q_range:
            continue
        q      = questions[q_num]
        offset = q_num - start
        sidx   = offset // 3
        first  = start + sidx * 3
        last   = first + 2
        ckey   = "conversation_id" if part_num == 3 else "talk_id"
        pfx    = "p3" if part_num == 3 else "p4"

        result.append({
            "id":       make_id(part_num, test_num, q_num),
            "part":     part_num,
            "test":     test_num,
            "question": q_num,
            ckey:       f"{pfx}-t{test_num:02d}-c{sidx+1:02d}",
            "audio":    f"audio/part{part_num}/Test_{test_num:02d}-{first:02d}-{last:02d}.mp3",
            "script":   None,
            "stem":     q["stem"].strip(),
            "options":  q["options"],
            "graphic":  q["graphic"],
            "answer":   None,
            "difficulty": None,
            "tags":     [],
        })
    return result


def extract_part_block(test_block: str, part_num: int) -> str:
    """Extract lines belonging to Part N."""
    RE_PART = re.compile(r"PART\s+" + str(part_num), re.IGNORECASE)
    RE_NEXT = re.compile(r"PART\s+[1234]", re.IGNORECASE)
    lines   = test_block.splitlines()
    result  = []
    in_part = False
    for line in lines:
        if RE_PART.search(line):
            in_part = True
            continue
        if in_part:
            # Stop at next part header
            if RE_NEXT.search(line) and not RE_PART.search(line):
                break
            result.append(line)
    return "\n".join(result) if result else test_block


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not MD_FILE.exists():
        print(f"[ERROR] Not found: {MD_FILE}")
        return

    print(f"Loading {MD_FILE.name} ...")
    md_text = MD_FILE.read_text(encoding="utf-8")
    print(f"  {len(md_text):,} chars, {len(md_text.splitlines())} lines\n")

    # ── Part 1: copy images from Marker output ──
    print("Step 1: Copy Part 1 images from Marker output...")
    img_mapping = extract_part1_images_from_marker()
    part1 = build_part1_json(img_mapping)
    print()

    # ── Part 2 skeleton ──
    part2 = build_part2_json()

    # ── Split into test blocks ──
    print("Step 2: Split markdown into test blocks...")
    test_blocks = split_tests(md_text)
    print(f"  Detected {len(test_blocks)} test blocks\n")

    # ── Parts 3/4 ──
    print("Step 3: Parse Part 3 & 4 questions...")
    all_p3, all_p4 = [], []

    for test_num, block in test_blocks:
        p3 = parse_part34(extract_part_block(block, 3), test_num, 3)
        p4 = parse_part34(extract_part_block(block, 4), test_num, 4)
        all_p3.extend(p3)
        all_p4.extend(p4)

        p3_full = sum(1 for q in p3 if len(q["options"]) == 4)
        p4_full = sum(1 for q in p4 if len(q["options"]) == 4)
        flag3 = "" if len(p3) == 39 else f" << MISSING {39-len(p3)}"
        flag4 = "" if len(p4) == 30 else f" << MISSING {30-len(p4)}"
        print(f"  Test {test_num:2d}: Part3 {len(p3)}/39 ({p3_full} complete){flag3} | Part4 {len(p4)}/30 ({p4_full} complete){flag4}")

    # ── Save ──
    def write_json(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[saved] {path}  ({len(data)} records)")

    print()
    write_json(BANK_DIR / "part1.json", part1)
    write_json(BANK_DIR / "part2.json", part2)
    write_json(BANK_DIR / "part3.json", all_p3)
    write_json(BANK_DIR / "part4.json", all_p4)

    p1_imgs  = sum(1 for q in part1 if q["image"])
    p3_full  = sum(1 for q in all_p3 if len(q["options"]) == 4)
    p4_full  = sum(1 for q in all_p4 if len(q["options"]) == 4)
    print(f"\n{'='*50}")
    print(f"Part 1: {p1_imgs}/60 images  |  Part 2: {len(part2)} skeleton")
    print(f"Part 3: {len(all_p3)}/390 questions, {p3_full} with 4 options")
    print(f"Part 4: {len(all_p4)}/300 questions, {p4_full} with 4 options")


if __name__ == "__main__":
    main()
