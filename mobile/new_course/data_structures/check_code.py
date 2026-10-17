"""Runs `dart analyze` on every complete Dart example in the course.

A block is checked when it contains `void main` and has no quiz blanks.
Blocks that intentionally fail to compile can be skipped by putting
`// no-analyze` on their first line.

    python3 new_course/data_structures/check_code.py [lesson_id ...]
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent
BLOCK = re.compile(r"```dart\n(.*?)\n```", re.S)


def blocks_for(lesson_id):
    sources = []
    md = ROOT / "lessons" / f"{lesson_id}.md"
    if md.exists():
        sources += [("md", b) for b in BLOCK.findall(md.read_text())]
    quiz = ROOT / "quizzes" / f"{lesson_id}.json"
    if quiz.exists():
        for i, q in enumerate(json.loads(quiz.read_text()), 1):
            sources += [(f"q{i}", b) for b in BLOCK.findall(q["question"])]
    return [
        (tag, code) for tag, code in sources
        if "void main" in code
        and "%fill%" not in code and "%order%" not in code
        and not code.lstrip().startswith("// no-analyze")
    ]


def main():
    curriculum = json.loads((ROOT / "curriculum.json").read_text())
    ids = sys.argv[1:] or [l["id"] for l in curriculum["lessons"]]
    work = pathlib.Path(tempfile.mkdtemp(prefix="dsa_code_"))
    (work / "pubspec.yaml").write_text(
        "name: dsa_check\nenvironment:\n  sdk: ^3.5.0\n")
    (work / "analysis_options.yaml").write_text(
        "analyzer:\n  errors:\n    unused_local_variable: ignore\n"
        "    unused_element: ignore\n    dead_code: ignore\n"
        "    equal_elements_in_set: ignore\n    equal_keys_in_map: ignore\n"
        "    unnecessary_type_check: ignore\n")
    lib = work / "bin"
    lib.mkdir()
    count = 0
    for lesson_id in ids:
        for n, (tag, code) in enumerate(blocks_for(lesson_id), 1):
            (lib / f"{lesson_id}__{tag}_{n}.dart").write_text(code + "\n")
            count += 1
    print(f"Analyzing {count} Dart examples...")
    result = subprocess.run(
        ["fvm", "dart", "analyze", "--no-fatal-warnings", "."],
        cwd=work, capture_output=True, text=True)
    issues = [l for l in result.stdout.splitlines()
              if " error " in l or "error -" in l or "warning -" in l]
    print("\n".join(issues) or "No errors or warnings.")
    shutil.rmtree(work, ignore_errors=True)
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
