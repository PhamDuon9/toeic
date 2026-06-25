"""
Export a practice test as a self-contained HTML file.

Usage:
    python scripts/exporter/export_practice_test.py --test 1 --parts 5,6,7
    python scripts/exporter/export_practice_test.py --test 1 --parts 5 --output English/DAILY_QUESTS/test1_part5.html

Reads:  question_bank/part{N}.json, passages.json
Writes: English/DAILY_QUESTS/test{N}_part{P}.html  (default)
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

ROOT     = Path(__file__).parent.parent.parent
BANK_DIR = ROOT / "question_bank"
OUT_DIR  = ROOT / "English" / "DAILY_QUESTS"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PART_NAMES = {
    1: "Photo Detective",
    2: "Quick Response Arena",
    3: "Conversation Investigation",
    4: "Broadcast Intelligence",
    5: "Grammar Dungeon",
    6: "Document Repair Workshop",
    7: "Corporate Intelligence Mission",
}

XP_PER_CORRECT = {"easy": 10, "medium": 20, "hard": 30, None: 15}


def load_json(path: Path) -> list | dict:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def get_questions(test_num: int, parts: list[int]) -> list[dict]:
    result = []
    for p in parts:
        questions = load_json(BANK_DIR / f"part{p}.json")
        result.extend(q for q in questions if q.get("test") == test_num)
    return result


def get_passages() -> dict[str, dict]:
    passages = load_json(BANK_DIR / "passages.json")
    return {p["id"]: p for p in passages}


def escape_html(text: str) -> str:
    if not text:
        return ""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def render_question_html(q: dict, passages: dict, idx: int) -> str:
    part = q["part"]
    qid  = escape_html(q["id"])
    ans  = q.get("answer") or "?"
    diff = q.get("difficulty")
    xp   = XP_PER_CORRECT[diff]

    html = [f'<div class="question" id="q_{qid}" data-answer="{ans}" data-xp="{xp}">']
    html.append(f'<div class="q-header">Q{q["question"]} <span class="part-tag">Part {part}</span></div>')

    # Passage (Part 6/7 — only if non-empty)
    if part in (6, 7):
        passage_text = q.get("passage", "")
        if not passage_text and q.get("passage_id"):
            p_obj = passages.get(q["passage_id"], {})
            passage_text = p_obj.get("text", "")
        if passage_text:
            html.append(f'<div class="passage">{escape_html(passage_text).replace(chr(10), "<br>")}</div>')

    # Question stem
    if part in (3, 4, 5, 6, 7):
        stem = q.get("stem") or ""
        html.append(f'<div class="stem">{escape_html(stem)}</div>')

    # Image (Part 1)
    if part == 1 and q.get("image"):
        img_rel = q["image"].replace("\\", "/")
        html.append(f'<div class="img-wrap"><img src="../../question_bank/{img_rel}" alt="Part 1 photo"></div>')

    # Audio (Parts 1-4)
    if part <= 4 and q.get("audio"):
        audio_rel = q["audio"].replace("\\", "/")
        html.append(f'<audio controls src="../../raw/Audio/LISTENING/Camle le/{Path(audio_rel).name}"></audio>')

    # Options (Parts 2-7)
    if part >= 2:
        html.append('<div class="options">')
        opts = q.get("options") or {}
        for letter in ["A", "B", "C", "D"]:
            text = opts.get(letter, "")
            html.append(
                f'<label class="option" data-letter="{letter}">'
                f'<input type="radio" name="{qid}" value="{letter}"> '
                f'<span class="letter">{letter}.</span> {escape_html(text)}'
                f'</label>'
            )
        html.append("</div>")

    html.append('<div class="feedback hidden"></div>')
    html.append("</div>")
    return "\n".join(html)


def build_html(test_num: int, parts: list[int], questions: list[dict], passages: dict) -> str:
    part_labels = " + ".join(f"Part {p} ({PART_NAMES.get(p, '')})" for p in parts)
    total_xp = sum(XP_PER_CORRECT[q.get("difficulty")] for q in questions if q.get("answer"))

    q_blocks = "\n".join(render_question_html(q, passages, i) for i, q in enumerate(questions))

    answers_js = json.dumps({q["id"]: q.get("answer") for q in questions})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Test {test_num} — {part_labels}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
  h1 {{ color: #f0883e; margin-bottom: 8px; font-size: 1.4rem; }}
  .subtitle {{ color: #8b949e; font-size: 0.9rem; margin-bottom: 24px; }}
  .question {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
  .q-header {{ font-size: 0.85rem; color: #8b949e; margin-bottom: 10px; }}
  .part-tag {{ background: #21262d; border-radius: 4px; padding: 2px 6px; font-size: 0.75rem; }}
  .passage {{ background: #0d1117; border-left: 3px solid #30363d; padding: 12px 16px; margin-bottom: 14px; font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap; }}
  .stem {{ font-size: 1rem; margin-bottom: 14px; line-height: 1.5; font-weight: 500; }}
  .options {{ display: flex; flex-direction: column; gap: 8px; }}
  .option {{ display: flex; align-items: flex-start; gap: 10px; padding: 10px 14px; background: #21262d; border-radius: 6px; cursor: pointer; border: 2px solid transparent; transition: border-color 0.15s; }}
  .option:hover {{ border-color: #388bfd; }}
  .option.correct {{ border-color: #2ea043; background: #1a2f22; }}
  .option.wrong   {{ border-color: #f85149; background: #2d1a1a; }}
  .letter {{ font-weight: bold; color: #f0883e; min-width: 20px; }}
  .feedback {{ margin-top: 12px; padding: 10px; border-radius: 6px; font-size: 0.9rem; }}
  .feedback.correct {{ background: #1a2f22; color: #2ea043; }}
  .feedback.wrong   {{ background: #2d1a1a; color: #f85149; }}
  .hidden {{ display: none; }}
  .img-wrap img {{ max-width: 100%; border-radius: 6px; margin-bottom: 12px; }}
  audio {{ width: 100%; margin-bottom: 12px; }}
  #submit-btn {{ background: #238636; color: #fff; border: none; padding: 12px 32px; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 20px; }}
  #submit-btn:hover {{ background: #2ea043; }}
  #score-panel {{ display: none; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 24px; margin-top: 20px; text-align: center; }}
  #score-panel h2 {{ color: #f0883e; font-size: 1.8rem; margin-bottom: 8px; }}
  #score-panel .xp {{ color: #7ee787; font-size: 1.2rem; }}
</style>
</head>
<body>
<h1>Test {test_num} — {part_labels}</h1>
<p class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d')} | {len(questions)} questions | Max XP: {total_xp}</p>

{q_blocks}

<button id="submit-btn" onclick="submitAll()">Submit Answers</button>

<div id="score-panel">
  <h2 id="score-text">Score</h2>
  <p class="xp" id="xp-text">+0 XP</p>
  <p id="breakdown-text" style="color:#8b949e; margin-top:8px; font-size:0.9rem;"></p>
</div>

<script>
const ANSWERS = {answers_js};

function submitAll() {{
  let correct = 0, total = 0, xpEarned = 0;
  document.querySelectorAll('.question').forEach(qEl => {{
    const qid = qEl.id.replace('q_', '');
    const correctAns = ANSWERS[qid];
    const xp = parseInt(qEl.dataset.xp || '15');
    const chosen = qEl.querySelector('input[type=radio]:checked');
    const feedback = qEl.querySelector('.feedback');
    total++;

    qEl.querySelectorAll('.option').forEach(opt => {{
      opt.style.pointerEvents = 'none';
      if (opt.dataset.letter === correctAns) opt.classList.add('correct');
    }});

    if (chosen) {{
      const chosenLetter = chosen.value;
      if (chosenLetter === correctAns) {{
        correct++;
        xpEarned += xp;
        feedback.textContent = '✓ Correct! +' + xp + ' XP';
        feedback.className = 'feedback correct';
      }} else {{
        chosen.closest('.option').classList.add('wrong');
        feedback.textContent = '✗ Correct answer: ' + correctAns;
        feedback.className = 'feedback wrong';
      }}
    }} else {{
      feedback.textContent = 'Not answered. Correct: ' + correctAns;
      feedback.className = 'feedback wrong';
    }}
    feedback.classList.remove('hidden');
  }});

  document.getElementById('score-text').textContent = correct + ' / ' + total + ' correct';
  document.getElementById('xp-text').textContent = '+' + xpEarned + ' XP earned';
  document.getElementById('breakdown-text').textContent =
    'Accuracy: ' + Math.round(correct/total*100) + '%';
  document.getElementById('score-panel').style.display = 'block';
  document.getElementById('submit-btn').style.display = 'none';

  // Save result to localStorage
  const result = {{ date: new Date().toISOString(), test: {test_num}, parts: {json.dumps(parts)},
    score: correct, total: total, pct: Math.round(correct/total*100), xp: xpEarned }};
  try {{ localStorage.setItem('toeic_test_{test_num}_p{','.join(map(str, parts))}', JSON.stringify(result)); }} catch(e) {{}}
}}
</script>
</body>
</html>"""


def main():
    args = sys.argv[1:]
    test_num = 1
    parts    = [5, 6, 7]
    out_file = None

    if "--test" in args:
        test_num = int(args[args.index("--test") + 1])
    if "--parts" in args:
        parts = [int(p) for p in args[args.index("--parts") + 1].split(",")]
    if "--output" in args:
        out_file = ROOT / args[args.index("--output") + 1]

    if out_file is None:
        part_str = "_".join(str(p) for p in parts)
        out_file = OUT_DIR / f"test{test_num}_part{part_str}.html"

    questions = get_questions(test_num, parts)
    passages  = get_passages()

    if not questions:
        print(f"[ERROR] No questions found for test={test_num}, parts={parts}")
        print("Run the parse scripts first.")
        return

    answered = sum(1 for q in questions if q.get("answer"))
    print(f"Generating: Test {test_num}, Parts {parts}")
    print(f"Questions: {len(questions)}, With answers: {answered}")

    html = build_html(test_num, parts, questions, passages)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"[saved] {out_file}")


if __name__ == "__main__":
    main()
