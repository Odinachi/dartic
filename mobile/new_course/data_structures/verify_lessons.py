"""Runs lesson examples and checks `print(...); // expected` comments.

For each runnable ```dart block in a lesson whose number of output lines equals
its number of commented print statements, every output line is compared with
its comment (the text before two spaces or " (" is used, so trailing notes
like `// 3  ([1,2] and [3])` are allowed). Mismatches are reported for review.

    python3 new_course/data_structures/verify_lessons.py [lesson_id ...]
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
PRINT_COMMENT = re.compile(r"^\s*print\(.*\);\s*//\s?(.*)$")


def expected_value(comment):
    text = re.sub(r"^[✅❌]\s*", "", comment.strip())
    text = re.split(r"\s{2,}| \(| ←| ✅| ❌| →|: |, not ", text)[0].strip()
    if " = " in text:
        text = text.rsplit(" = ", 1)[1]
    # Purely descriptive comments ("unchanged", "positive") aren't checkable.
    if not re.search(r"[\d\[\]{}()]|^(true|false|null)$|^[A-Z]", text):
        return ""
    return text


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    curriculum = json.loads((ROOT / "curriculum.json").read_text())
    ids = sys.argv[1:] or [l["id"] for l in curriculum["lessons"]]
    work = pathlib.Path(tempfile.mkdtemp(prefix="dsa_lessons_"))
    (work / "pubspec.yaml").write_text(
        "name: dsa_lessons\nenvironment:\n  sdk: ^3.5.0\n")
    (work / "lib").mkdir()
    cases = []
    for lesson_id in ids:
        md = ROOT / "lessons" / f"{lesson_id}.md"
        if not md.exists():
            continue
        for n, code in enumerate(BLOCK.findall(md.read_text()), 1):
            if "void main" not in code or "Stopwatch" in code:
                continue
            if code.lstrip().startswith("// no-analyze"):
                continue
            expected = []
            for line in code.splitlines():
                m = PRINT_COMMENT.match(line)
                if m:
                    expected.append(expected_value(m.group(1)))
            if not expected:
                continue
            name = f"{lesson_id}_b{n}"
            (work / "lib" / f"{name}.dart").write_text(code + "\n")
            cases.append((name, lesson_id, n, expected,
                          code.count("print(")))

    imports = "\n".join(
        f"import 'package:dsa_lessons/{c[0]}.dart' as {c[0]};" for c in cases)
    calls = "\n".join(f"  run('{c[0]}', {c[0]}.main);" for c in cases)
    (work / "bin").mkdir()
    (work / "bin" / "runner.dart").write_text(f"""
import 'dart:async';
import 'dart:convert';
{imports}

final results = <String, List<String>>{{}};

void run(String name, Function body) {{
  final out = <String>[];
  runZonedGuarded(() {{
    body();
  }}, (e, _) => out.add('THREW: ${{e.runtimeType}}'),
      zoneSpecification: ZoneSpecification(
          print: (_, __, ___, line) => out.addAll(line.split('\\n'))));
  results[name] = out;
}}

void main() {{
{calls}
  print(jsonEncode(results));
}}
""")
    subprocess.run(["fvm", "dart", "pub", "get"], cwd=work, capture_output=True)
    result = subprocess.run(["fvm", "dart", "run", "bin/runner.dart"],
                            cwd=work, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-4000:], result.stderr[-4000:])
        sys.exit(1)
    outputs = json.loads(result.stdout.strip().splitlines()[-1])

    checked = flagged = 0
    for name, lesson_id, n, expected, prints in cases:
        out = outputs.get(name, [])
        # Only compare blocks where every print is commented and printed once.
        if len(expected) != prints or len(out) != len(expected):
            continue
        checked += 1
        for exp, got in zip(expected, out):
            e, g = norm(exp), norm(got)
            if e and not g.startswith(e) and e not in g \
                    and not (g and e.startswith(g + ",")):
                flagged += 1
                print(f"⚠️  {lesson_id} block {n}\n    comment: {exp!r}\n"
                      f"    output:  {got!r}")
    print(f"\nChecked {checked} lesson blocks, flagged {flagged} lines.")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
