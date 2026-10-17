// Uploads the Data Structures course in new_course/data_structures to Firestore.
//
// Firestore layout:
//   DSA_course_modules/{module}        { module, title, desc, lessonCount }
//   DSA_course/{lessonId}              { title, desc, module, moduleTitle, order,
//                                        videos, questionCount, readMinutes }
//   DSA_course/{lessonId}/content/main { markdown }
//   DSA_course/{lessonId}/quiz/main    { questions: [...] }
//
// Lesson docs stay small so the list screen can paginate cheaply; the markdown
// and quiz are only fetched when a lesson is opened.
//
// Usage (from this folder, after `npm install`):
//   node upload.mjs                 # dry run: validates and prints a summary
//   node upload.mjs --commit        # writes to Firestore
//
// Credentials: either run `gcloud auth application-default login`, or set
// GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON key file.

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const courseDir = path.resolve(here, '../../new_course/data_structures');
const projectId = process.env.FIREBASE_PROJECT ?? 'dartcoder-d57cb';
const commit = process.argv.includes('--commit');

const curriculum = JSON.parse(
  await readFile(path.join(courseDir, 'curriculum.json'), 'utf8'),
);
const moduleTitles = new Map(curriculum.modules.map((m) => [m.module, m.title]));

const lessons = [];
for (const lesson of curriculum.lessons) {
  const markdown = await readFile(
    path.join(courseDir, 'lessons', `${lesson.id}.md`), 'utf8');
  const questions = JSON.parse(await readFile(
    path.join(courseDir, 'quizzes', `${lesson.id}.json`), 'utf8'));
  const words = markdown.split(/\s+/).filter(Boolean).length;
  lessons.push({
    ...lesson,
    markdown,
    questions,
    readMinutes: Math.max(1, Math.round(words / 200)),
  });
}

// Firestore documents are limited to 1 MiB; leave a safety margin.
const limit = 900 * 1024;
for (const l of lessons) {
  for (const [what, size] of [
    ['markdown', Buffer.byteLength(l.markdown)],
    ['quiz', Buffer.byteLength(JSON.stringify(l.questions))],
  ]) {
    if (size > limit) throw new Error(`${l.id} ${what} is too large: ${size} bytes`);
  }
}

const writes = [];
for (const m of curriculum.modules) {
  writes.push({
    path: `DSA_course_modules/${m.module}`,
    data: {
      module: m.module,
      title: m.title,
      desc: m.desc,
      lessonCount: lessons.filter((l) => l.module === m.module).length,
    },
  });
}
for (const l of lessons) {
  writes.push({
    path: `DSA_course/${l.id}`,
    data: {
      title: l.title,
      desc: l.desc,
      module: l.module,
      moduleTitle: moduleTitles.get(l.module),
      order: l.order,
      videos: [],
      questionCount: l.questions.length,
      readMinutes: l.readMinutes,
    },
  });
  writes.push({ path: `DSA_course/${l.id}/content/main`, data: { markdown: l.markdown } });
  writes.push({ path: `DSA_course/${l.id}/quiz/main`, data: { questions: l.questions } });
}

const totalQuestions = lessons.reduce((n, l) => n + l.questions.length, 0);
console.log(`Project:   ${projectId}`);
console.log(`Modules:   ${curriculum.modules.length}`);
console.log(`Lessons:   ${lessons.length}`);
console.log(`Questions: ${totalQuestions}`);
console.log(`Documents: ${writes.length}`);

if (!commit) {
  console.log('\nDry run only. Re-run with --commit to write to Firestore.');
  process.exit(0);
}

const { initializeApp, applicationDefault } = await import('firebase-admin/app');
const { getFirestore } = await import('firebase-admin/firestore');

initializeApp({ credential: applicationDefault(), projectId });
const db = getFirestore();

// Large docs (markdown, quizzes) are written in small batches to stay well
// under Firestore's 10 MiB per-request limit.
const batchSize = 20;
for (let i = 0; i < writes.length; i += batchSize) {
  const batch = db.batch();
  for (const w of writes.slice(i, i + batchSize)) {
    batch.set(db.doc(w.path), w.data);
  }
  await batch.commit();
  console.log(`Wrote ${Math.min(i + batchSize, writes.length)}/${writes.length}`);
}
console.log('\nDone.');
