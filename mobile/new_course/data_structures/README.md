# Data Structures course

Content for the "Data structures" path on the home screen. It's uploaded to
Firestore (`DSA_course`, `DSA_course_modules`) and read by
`lib/features/courses/views/dsa_course_screen.dart`.

## Layout

- `curriculum.json`: modules and lessons (id, module, order, title, desc).
  `order` is `module * 100 + lessonNumber`; the app filters by module with a
  range on `order`.
- `lessons/<id>.md`: lesson markdown.
- `quiz_src/<id>.py`: quiz source, using `mcq(...)`, `fill(...)` and
  `order(...)` helpers (same JSON format as `assets/jsons/quizzes`).
- `quizzes/<id>.json`: generated quizzes (don't edit by hand).

## Workflow

```bash
python3 build.py            # validate every lesson and regenerate quizzes/*.json
python3 check_code.py       # dart analyze every runnable example
python3 verify_outputs.py   # run MCQ snippets and compare output with answers
python3 verify_lessons.py   # run lesson examples and check `// expected` comments
```

`build.py` enforces the quiz widget's rules: blanks only inside code blocks,
`order` answers must be unique options, no question may depend on another
(the app samples 10 at random), and at least 50 questions per lesson.

## Upload

```bash
cd ../../scripts/upload_dsa_course
npm install
node upload.mjs            # dry run
node upload.mjs --commit   # writes to Firestore
```
