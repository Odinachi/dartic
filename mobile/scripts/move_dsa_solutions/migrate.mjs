// Moves each algorithm problem's `answer` out of the problem doc (which every
// signed-in user can read) into DSA/{id}/solution/main, which Firestore rules
// only let a user read after unlocking it with a gem.
//
//   DSA/{id}/problem/{doc}.answer  ->  DSA/{id}/solution/main { answer }
//
// Usage (from this folder, after `npm install`):
//   node migrate.mjs            # dry run: reads Firestore, prints what would move
//   node migrate.mjs --commit   # writes solution docs and removes `answer` fields
//
// Before --commit, deploy the updated firestore.rules and ship an app version
// with gems (older versions simply stop showing the Solution menu item).
// A backup of every answer is written to backup-<timestamp>.json first.
//
// Credentials: `gcloud auth application-default login`, or set
// GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON key file.

import { writeFile } from 'node:fs/promises';
import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore, FieldValue } from 'firebase-admin/firestore';

const projectId = process.env.FIREBASE_PROJECT ?? 'dartcoder-d57cb';
const commit = process.argv.includes('--commit');

initializeApp({ credential: applicationDefault(), projectId });
const db = getFirestore();

const problems = await db.collection('DSA').get();
const moves = [];
let alreadyMoved = 0;
let noAnswer = 0;

for (const problem of problems.docs) {
  const docs = await problem.ref.collection('problem').get();
  const withAnswer = docs.docs.filter((d) => typeof d.data().answer === 'string' && d.data().answer.trim());
  if (withAnswer.length === 0) {
    const existing = await problem.ref.collection('solution').doc('main').get();
    existing.exists ? alreadyMoved++ : noAnswer++;
    continue;
  }
  // The app reads the first problem doc; use its answer.
  moves.push({ id: problem.id, answer: withAnswer[0].data().answer, refs: withAnswer.map((d) => d.ref) });
}

console.log(`Project:          ${projectId}`);
console.log(`Problems:         ${problems.size}`);
console.log(`To move:          ${moves.length}`);
console.log(`Already moved:    ${alreadyMoved}`);
console.log(`No answer at all: ${noAnswer}`);

if (!commit) {
  console.log('\nDry run only. Re-run with --commit to move the answers.');
  process.exit(0);
}

const backup = `backup-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
await writeFile(backup, JSON.stringify(moves.map(({ id, answer }) => ({ id, answer })), null, 2));
console.log(`\nBacked up ${moves.length} answers to ${backup}`);

// One batch per problem: the solution doc is created and the answer removed
// atomically, so a problem is never left with zero or two copies.
for (const [i, m] of moves.entries()) {
  const batch = db.batch();
  batch.set(db.doc(`DSA/${m.id}/solution/main`), { answer: m.answer, movedAt: FieldValue.serverTimestamp() });
  for (const ref of m.refs) batch.update(ref, { answer: FieldValue.delete() });
  await batch.commit();
  console.log(`Moved ${i + 1}/${moves.length}  ${m.id}`);
}
console.log('\nDone.');
