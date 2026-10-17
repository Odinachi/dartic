"""Runs every runnable MCQ snippet and checks its output against the answer.

Each snippet becomes its own library; one runner imports them all and calls
each `main()` inside a Zone that captures `print`. A question is flagged when
the normalized output doesn't contain the normalized answer (or vice versa),
so flagged items need a human look rather than being definitely wrong.

    python3 new_course/data_structures/verify_outputs.py [lesson_id ...]
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


def norm(s):
    s = re.sub(r"\bthen\b", " ", s)
    return re.sub(r"[\s'\",]+", "", s).lower()


def main():
    curriculum = json.loads((ROOT / "curriculum.json").read_text())
    ids = sys.argv[1:] or [l["id"] for l in curriculum["lessons"]]
    work = pathlib.Path(tempfile.mkdtemp(prefix="dsa_run_"))
    (work / "pubspec.yaml").write_text(
        "name: dsa_run\nenvironment:\n  sdk: ^3.5.0\n")
    (work / "lib").mkdir()
    cases = []
    for lesson_id in ids:
        quiz = ROOT / "quizzes" / f"{lesson_id}.json"
        if not quiz.exists():
            continue
        for i, q in enumerate(json.loads(quiz.read_text()), 1):
            if q["type"] != "mcq":
                continue
            blocks = BLOCK.findall(q["question"])
            if len(blocks) != 1 or "void main" not in blocks[0]:
                continue
            code = blocks[0]
            if code.lstrip().startswith("// no-analyze"):
                continue
            name = f"{lesson_id}_q{i}"
            (work / "lib" / f"{name}.dart").write_text(code + "\n")
            cases.append((name, lesson_id, i, q["answer"][0]))

    imports = "\n".join(
        f"import 'package:dsa_run/{n}.dart' as {n};" for n, *_ in cases)
    calls = "\n".join(f"  run('{n}', {n}.main);" for n, *_ in cases)
    (work / "bin").mkdir()
    (work / "bin" / "runner.dart").write_text(f"""
import 'dart:async';
import 'dart:convert';
{imports}

final results = <String, String>{{}};

void run(String name, Function body) {{
  final out = StringBuffer();
  runZonedGuarded(() {{
    final r = body();
    if (r is Future) throw StateError('async main not supported');
  }}, (e, _) => out.writeln('THREW: ${{e.runtimeType}}'),
      zoneSpecification: ZoneSpecification(
          print: (_, __, ___, line) => out.writeln(line)));
  results[name] = out.toString();
}}

void main() {{
{calls}
  print(jsonEncode(results));
}}
""")
    subprocess.run(["fvm", "dart", "pub", "get"], cwd=work,
                   capture_output=True)
    result = subprocess.run(["fvm", "dart", "run", "bin/runner.dart"],
                            cwd=work, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-4000:], result.stderr[-4000:])
        sys.exit(1)
    outputs = json.loads(result.stdout.strip().splitlines()[-1])

    flagged = 0
    for name, lesson_id, i, answer in cases:
        out = outputs.get(name, "")
        a, o = norm(answer), norm(out)
        threw = re.match(r"THREW: (\w+)", out.strip())
        if threw and threw.group(1).lower() in a:
            continue
        if not o or (a not in o and o not in a):
            flagged += 1
            print(f"⚠️  {lesson_id} Q{i}\n    answer: {answer!r}\n"
                  f"    output: {out.strip()!r}")
    print(f"\nChecked {len(cases)} runnable MCQs, flagged {flagged}.")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
