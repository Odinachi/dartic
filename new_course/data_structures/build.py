"""Builds and validates the Data Structures course.

Quiz sources live in quiz_src/<lesson_id>.py and define QUESTIONS using the
helpers below. Running this script validates every lesson and writes
quizzes/<lesson_id>.json in the same format as assets/jsons/quizzes/*.json.

    python3 new_course/data_structures/build.py            # build all
    python3 new_course/data_structures/build.py big_o      # build one
"""

import json
import re
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
MIN_QUESTIONS = 50
MIN_LESSON_LINES = 400


def mcq(question, options, answer):
    return {"question": question.strip("\n"), "options": options,
            "answer": [answer], "type": "mcq"}


def fill(question, *answers):
    return {"question": question.strip("\n"), "answer": list(answers),
            "type": "fill"}


def order(question, options, answer):
    return {"question": question.strip("\n"), "options": options,
            "answer": answer, "type": "order"}


def validate_question(q, where):
    errors = []
    text, kind, answer = q["question"], q["type"], q["answer"]
    if not text.strip():
        errors.append("empty question")
    if text.count("```") % 2:
        errors.append("unbalanced ``` fences")
    # The quiz widget only renders blanks inside ```code``` blocks.
    outside = re.sub(r"```(\w+)?\n(.*?)\n```", "", text, flags=re.S)
    if "%fill%" in outside or "%order%" in outside:
        errors.append("blank placeholder outside a code block")
    if '\\"' in text:
        errors.append("literal backslash-quote in question")
    # Quizzes are sampled randomly, so questions can't depend on each other.
    if re.search(r"previous (question|example|function|code)|\babove\b|"
                 r"the same `|the completed |in the code above|for the same |in the same scenario",
                 text, re.I):
        errors.append("question refers to another question")
    if kind == "mcq":
        opts = q["options"]
        if len(opts) < 2 or len(set(opts)) != len(opts):
            errors.append("mcq needs 2+ unique options")
        if answer[0] not in opts:
            errors.append(f"mcq answer {answer[0]!r} not in options")
    elif kind == "fill":
        blanks = text.count("%fill%")
        if blanks == 0 or blanks != len(answer):
            errors.append(f"fill has {blanks} blanks but {len(answer)} answers")
        if any(not a or a != a.strip() for a in answer):
            errors.append("fill answers must be non-empty and trimmed")
    elif kind == "order":
        blanks = text.count("%order%")
        opts = q["options"]
        if blanks != len(answer):
            errors.append(f"order has {blanks} blanks but {len(answer)} answers")
        # The quiz UI can't select the same chip twice.
        if len(set(answer)) != len(answer):
            errors.append("order answers must be unique")
        if len(set(opts)) != len(opts):
            errors.append("order options must be unique")
        missing = [a for a in answer if a not in opts]
        if missing:
            errors.append(f"order answers missing from options: {missing}")
    else:
        errors.append(f"unknown type {kind!r}")
    return [f"{where}: {e}" for e in errors]


def build(lesson_id):
    errors = []
    md = ROOT / "lessons" / f"{lesson_id}.md"
    src = ROOT / "quiz_src" / f"{lesson_id}.py"
    if not md.exists():
        errors.append(f"{lesson_id}: missing lesson markdown")
    else:
        text = md.read_text()
        lines = text.count("\n")
        if lines < MIN_LESSON_LINES:
            errors.append(f"{lesson_id}: lesson only {lines} lines")
        if text.count("```") % 2:
            errors.append(f"{lesson_id}: lesson has unbalanced ``` fences")
    if not src.exists():
        return errors + [f"{lesson_id}: missing quiz source"], 0

    scope = {"mcq": mcq, "fill": fill, "order": order}
    exec(compile(src.read_text(), str(src), "exec"), scope)
    questions = scope["QUESTIONS"]
    if len(questions) < MIN_QUESTIONS:
        errors.append(f"{lesson_id}: only {len(questions)} questions")
    seen = set()
    for i, q in enumerate(questions, 1):
        errors += validate_question(q, f"{lesson_id} Q{i}")
        if q["question"] in seen:
            errors.append(f"{lesson_id} Q{i}: duplicate question")
        seen.add(q["question"])

    out = ROOT / "quizzes" / f"{lesson_id}.json"
    out.write_text(json.dumps(questions, indent=2, ensure_ascii=False) + "\n")
    return errors, len(questions)


def main():
    curriculum = json.loads((ROOT / "curriculum.json").read_text())
    ids = [l["id"] for l in curriculum["lessons"]]
    wanted = sys.argv[1:] or ids
    all_errors, total = [], 0
    for lesson_id in wanted:
        errors, count = build(lesson_id)
        total += count
        status = "ok" if not errors else f"{len(errors)} error(s)"
        print(f"{lesson_id:32} {count:4} questions  {status}")
        all_errors += errors
    print(f"\n{total} questions across {len(wanted)} lessons")
    if all_errors:
        print("\n".join(all_errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
