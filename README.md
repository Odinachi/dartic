# Dartic

**Learn Dart, practice algorithms and master data structures, all from your phone.**

Dartic is a Flutter learning app. It pairs short, friendly lessons with a real
Dart code runner, thousands of quiz questions and graded algorithm problems.
This repository holds the mobile app and its marketing site.

| | |
|---|---|
| **Lessons** | 73 (35 Dart + 38 data structures) |
| **Quiz questions** | 4,151 (about 2,060 Dart + 2,090 data structures) |
| **Platforms** | iOS and Android (Flutter) |
| **Backend** | Firebase: Auth, Firestore, Analytics, Crashlytics, Messaging, Hosting |
| **Website** | <https://dartic.odinachi.space> |

---

## Contents

- [Repository layout](#repository-layout)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Mobile app](#mobile-app)
  - [Prerequisites](#prerequisites)
  - [First-time setup](#first-time-setup)
  - [Running](#running)
  - [Building releases](#building-releases)
  - [Testing and analysis](#testing-and-analysis)
  - [App architecture](#app-architecture)
- [Firebase](#firebase)
  - [Firestore data model](#firestore-data-model)
  - [Security rules](#security-rules)
- [Course content](#course-content)
  - [Dart course (bundled)](#dart-course-bundled)
  - [Data structures course (Firestore)](#data-structures-course-firestore)
  - [Quiz format](#quiz-format)
- [Buying gems (RevenueCat)](#buying-gems-revenuecat)
- [Landing page](#landing-page)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

---

## Repository layout

```
dartcoder/
├── README.md                  ← you are here
├── mobile/                    ← Flutter app (iOS & Android)
│   ├── lib/                   ← app source
│   ├── assets/                ← bundled lessons, quizzes, fonts, images, Lottie files
│   ├── android/  ios/  web/   ← platform projects
│   ├── test/                  ← unit and widget tests
│   ├── new_course/
│   │   └── data_structures/   ← DS course source: lessons, quiz sources, validators
│   ├── scripts/
│   │   └── upload_dsa_course/ ← Node script that uploads the DS course to Firestore
│   ├── firestore.rules        ← Firestore security rules
│   ├── .firebaserc            ← Firebase project alias (dartcoder-d57cb)
│   └── pubspec.yaml
└── landing_page/              ← website + API (Vercel; the site also on Firebase Hosting)
    ├── public/                ← static site: index.html, styles.css, main.js, legal pages, assets/
    ├── api/                   ← FastAPI server (Vercel Function)
    │   ├── index.py           ← app: /api/health, /api/revenuecat/webhook
    │   ├── gem_webhook.py     ← credits gem purchases to Firestore wallets
    │   ├── tests/             ← webhook tests (Firestore emulator)
    │   └── .env.example       ← environment variables to set on Vercel
    ├── pyproject.toml         ← Python deps + Vercel entrypoint (must sit at the project root)
    ├── vercel.json  .vercelignore
    └── firebase.json  .firebaserc
```

The two projects are independent. Neither one builds or imports the other, but
they share the same Firebase project (`dartcoder-d57cb`).

---

## Features

### 🎓 Dart course
- 35 lessons in three levels: **Basics** (variables to null safety),
  **Intermediate** (classes, mixins, closures, exceptions) and **Advanced**
  (futures, streams, generics, sealed classes, isolates).
- Lessons are Markdown with syntax-highlighted code, analogies and embedded
  YouTube explanations.
- Shipped inside the app bundle, so it works offline and needs no account.

### 🧱 Data structures course
- 38 lessons across 7 modules: Foundations, Linear Structures, Hashing, Trees,
  Graphs, Sorting & Searching, Advanced.
- More than 50 quiz questions per lesson (2,090 in total). Every runnable
  example was checked with `dart analyze`, and every "what does this print?"
  answer was verified by running the code.
- Stored in Firestore and **restricted to signed-in users**. The list is
  paginated and can be filtered by module. A lesson's content and quiz are
  fetched only when the lesson is opened.

### 🧠 Quizzes
- Three question types: multiple choice, fill in the blank (typed into a gap
  in code) and drag-to-order tokens.
- Each attempt draws 10 random questions from the lesson's bank. Passing marks
  the lesson as complete, with a confetti score screen.

### 💻 Code editor and runner
- Full editor with syntax highlighting (Nord / Atom One Light), formatting
  (`dart_style`), undo/redo and auto-save.
- Runs Dart on the device through a fork of
  [`dart_eval`](https://github.com/Odinachi/dart_eval), so no server round-trip
  is needed.
- Every lesson has a **Practice** button that opens the editor.

### 🧩 Algorithm practice
- Coding problems stored in Firestore (`DSA`), sorted by difficulty and loaded
  page by page.
- Solutions are checked against automated test cases (`test_runner_service.dart`).
  Solved problems are recorded in the user's progress.

### 💎 Gems
- Viewing a problem's reference solution costs **1 gem**. Once unlocked, it
  stays unlocked.
- New accounts start with **3 gems**, and solving a problem for the first
  time earns **1 gem**.
- The balance shows on the problem list and in the editor. The solution
  opens read-only, with **Copy** and **Use in editor**.
- Gems can also be bought in packs through Apple / Google in-app purchase
  (via RevenueCat) from the **Get gems** sheet. Purchased gems are credited by
  the server (see [Buying gems](#buying-gems-revenuecat)).
- Settings live in `GemRules` (`lib/features/wallet/models/wallet_model.dart`).
  `firestore.rules` and `landing_page/api/gem_webhook.py` use the same numbers, so
  change them together.

### 👤 Accounts and progress
- Sign in with Google or Apple, then create a profile with a unique username
  and skill level.
- Firestore syncs the current lesson, passed lessons and solved problems
  across devices.
- Guests can use the Dart course and editor. Signing in unlocks the data
  structures course and progress sync.

### 🎨 Experience
- Light and dark themes, a native-style bottom navigation bar, shimmer
  loading states, Lottie animations and a daily Dart tip.
- Push and local notifications (Firebase Messaging and `flutter_local_notifications`).

---

## Tech stack

| Area | Packages |
|---|---|
| UI | Flutter 3.44, `flutter_screenutil`, `flutter_svg`, `lottie`, `confetti`, `shimmer_animation` |
| State | `flutter_bloc` (Cubits), `equatable` |
| Code editor | `flutter_code_editor`, `flutter_highlight`, `highlight`, `dart_style` |
| Code execution | `dart_eval` (fork: `github.com/Odinachi/dart_eval`) |
| Content | `markdown_widget`, `youtube_player_flutter` |
| Auth | `firebase_auth`, `google_sign_in`, `sign_in_with_apple` |
| Data | `cloud_firestore`, `shared_preferences` |
| Ops | `firebase_analytics`, `firebase_crashlytics`, `firebase_messaging`, `flutter_local_notifications` |
| Links | `url_launcher` |
| Content tooling | Python 3 (build and validators), Dart SDK (`dart analyze`, `dart run`), Node 18+ with `firebase-admin` (upload) |
| Website | Plain HTML, CSS and JS (no build step), Firebase Hosting |

---

## Mobile app

All commands in this section run from `mobile/`.

### Prerequisites

- **[FVM](https://fvm.app)**: the project pins Flutter **3.44.0** in
  `.fvmrc`. Run Flutter through `fvm flutter …` so everyone uses the same SDK.
- Xcode (iOS) and/or Android Studio with an Android SDK.
- CocoaPods for iOS (`sudo gem install cocoapods` or Homebrew).
- The [Firebase CLI](https://firebase.google.com/docs/cli) and
  [FlutterFire CLI](https://firebase.flutter.dev/docs/cli/), only if you need
  to regenerate Firebase config or deploy rules.

### First-time setup

```bash
cd mobile
fvm install            # installs the pinned Flutter version
fvm flutter pub get
```

**Firebase config.** These files hold project credentials and are **not
committed**:

| File | How to get it |
|---|---|
| `lib/firebase_options.dart` | `flutterfire configure --project=dartcoder-d57cb` |
| `android/app/google-services.json` | Generated by `flutterfire configure`, or download from the Firebase console |
| `ios/Runner/GoogleService-Info.plist` | Generated by `flutterfire configure`, or download from the Firebase console |
| `firebase.json` | Generated by `flutterfire configure`; also holds the `firestore` rules path |

To use your own Firebase project, run `flutterfire configure` against it,
deploy `firestore.rules`, and upload the course content (see
[Data structures course](#data-structures-course-firestore)).

**Compile-time defines.** Passed with `--dart-define`:

| Define | Purpose |
|---|---|
| `CLIENT_ID` | Apple Services ID used for web-based Sign in with Apple on Android |
| `REDIRECT_URI` | Callback URL registered for that Services ID |
| `RC_APPLE_KEY` | RevenueCat public SDK key for iOS (`appl_…`). Without it, the gem store is hidden |
| `RC_GOOGLE_KEY` | RevenueCat public SDK key for Android (`goog_…`) |

`String.fromEnvironment` reads them in `lib/services/firebase_services.dart`
and `lib/services/gem_store_service.dart`.
Locally they live in `.vscode/launch.json` (VS Code) and in a gitignored
`makefile`. Keep real values out of commits.

### Running

```bash
fvm flutter run \
  --dart-define=CLIENT_ID=<apple-services-id> \
  --dart-define=REDIRECT_URI=<redirect-uri>
```

In VS Code, pick the launch configuration from `.vscode/launch.json` and press
F5. Google sign-in and every other feature work without the defines. Only
Apple sign-in on Android needs them.

### Building releases

```bash
fvm flutter build ios --release        --dart-define=CLIENT_ID=… --dart-define=REDIRECT_URI=…
fvm flutter build apk --release        --dart-define=CLIENT_ID=… --dart-define=REDIRECT_URI=…
fvm flutter build appbundle --release  --dart-define=CLIENT_ID=… --dart-define=REDIRECT_URI=…
```

A local `makefile` (gitignored) wraps these commands as `make "build ios"`,
`make "build apk"` and `make "build appbundle"`. The version comes from
`pubspec.yaml` (`version: 2.0.3+11`). Bump it before each store upload.

### Testing and analysis

```bash
fvm flutter analyze    # must be clean
fvm flutter test       # unit and widget tests in test/
```

### App architecture

```
mobile/lib/
├── main.dart                     ← Firebase init, theme, BlocProviders, router
├── features/
│   ├── authetication/            ← onboarding, Google/Apple sign-in, profile creation
│   │   ├── models/  view_model/  views/
│   ├── dashboard/                ← home, activity, bottom-nav shell
│   ├── courses/                  ← Dart course list/details, DS course, quiz widgets, score screen
│   │   ├── models/               ← course, DsaModule, DsaCourseModel, DsaLessonContent
│   │   └── views/                ← courses_list, course_details, course_quiz, dsa_course_screen, …
│   ├── editor/                   ← code editor and algorithm problems (EditorCubit, test cases)
│   └── profile/                  ← profile and badges
├── services/
│   ├── firebase_services.dart    ← every Auth and Firestore call (with an in-memory lesson cache)
│   ├── test_runner_service.dart  ← runs user code against problem test cases
│   ├── cache_service.dart        ← shared_preferences wrapper
│   └── notification_service.dart
├── shared/
│   ├── constants.dart            ← Dart course catalogue (AppData.courses)
│   ├── navigation/router.dart    ← named routes and the auth guard
│   ├── theme.dart  assets.dart  app_string.dart  text_editor.dart
│   └── widgets/                  ← reusable UI (animated nav bar, buttons, …)
└── views/                        ← shared screens and widgets
```

- **State management:** each feature owns a Cubit in `view_model/`. Screens
  listen with `BlocBuilder`/`BlocListener`.
- **Data access:** all Firebase calls go through `FirebaseServices`. Methods
  return Dart records such as `({T? data, String? error})` instead of
  throwing.
- **Routing:** `router.dart` maps route names to screens. Routes in
  `_authRequired` (the DS course list and details) render the onboarding
  screen when `FirebaseAuth.instance.currentUser` is `null`. The home card
  also sends guests to sign-in, and Firestore rules enforce the same
  restriction on the server.

---

## Firebase

Project ID: **`dartcoder-d57cb`**

| Service | Used for |
|---|---|
| Authentication | Google and Apple sign-in |
| Cloud Firestore | Profiles, progress, algorithm problems, data structures course |
| Analytics / Crashlytics | Usage and crash reporting |
| Cloud Messaging | Push notifications |
| Hosting | `landing_page/` (website and legal pages) |

### Firestore data model

```
Users/{uid}                              profile: firstName, lastName, username, email,
│                                        photoUrl, currentLevel, createdAt
├── progress/current                     current_course: num
│                                        passed_courses: [num]     ← Dart lessons passed
│                                        passed_dsa:     [string]  ← algorithm problems solved
└── wallet/main                          gems: num
                                         unlocked: [string]  ← problems whose solution was bought
                                         rewarded: [string]  ← problems already paid a solve reward

DSA/{problemId}                          algorithm problem summary (title, difficulty, …)
├── problem/{docId}                      question and test suite
└── solution/main                        answer (readable only once unlocked)

Purchases/{store}_{transactionId}        uid, productId, gems, store, environment,
                                         status: credited | refunded   ← written by the webhook

DSA_course_modules/{module}              module, title, desc, lessonCount
DSA_course/{lessonId}                    title, desc, module, moduleTitle, order,
│                                        videos, questionCount, readMinutes
├── content/main                         markdown
└── quiz/main                            questions: [ … ]   (see Quiz format)
```

`DSA_course.order` is `module * 100 + lessonNumber`. To filter by module, the
app runs a range query on `order` (`>= m*100`, `< (m+1)*100`), so no composite
index is needed. Lesson documents stay small so the list paginates cheaply.
The markdown and quiz live in subcollections and are fetched only when a
lesson is opened.

### Security rules

The rules are in `mobile/firestore.rules`:

| Path | Read | Write |
|---|---|---|
| `DSA_course/**`, `DSA_course_modules/*` | signed-in users | nobody (content is uploaded with the Admin SDK) |
| `DSA/{id}`, `DSA/{id}/problem/*` | signed-in users | nobody |
| `DSA/{id}/solution/main` | signed-in users who have `{id}` in their `wallet.unlocked` | nobody |
| `Users/{uid}` | signed-in users (needed for the username availability check) | owner only |
| `Users/{uid}/progress/*` | owner only | owner only |
| `Users/{uid}/wallet/main` | owner only | owner, limited to three moves (below); the webhook adds purchased gems with the Admin SDK |
| `Purchases/{id}` | the purchasing user | nobody (webhook only) |

The wallet can't be edited freely. The client can only:
1. create it with exactly the welcome bonus and empty lists;
2. spend exactly 1 gem to add one existing problem to `unlocked`;
3. earn exactly 1 gem to add one existing problem to `rewarded`.

Anything else is rejected, such as setting a balance, unlocking two problems
for one gem, unlocking a problem that doesn't exist, or earning twice for the
same problem. Purchased gems never pass through the client: only the webhook
server can add them. The owner can delete the wallet so account deletion
works. A determined user could delete it to reclaim the 3-gem welcome bonus,
but they'd lose everything in it, including purchased gems.

Deploy them from `mobile/`:

```bash
firebase deploy --only firestore:rules
```

---

## Course content

### Dart course (bundled)

- Lessons: `mobile/assets/courses/*.md`
- Quizzes: `mobile/assets/jsons/quizzes/*.json`
- Catalogue (titles, levels, file names, videos): `AppData.courses` in
  `mobile/lib/shared/constants.dart`

To add a lesson, write the Markdown file and the quiz JSON, register both in
`AppData.courses`, and make sure the files fall under an asset folder that
`pubspec.yaml` already declares.

### Moving solutions behind the gem paywall

Problem docs used to carry the solution in an `answer` field, which every
signed-in user downloads. `mobile/scripts/move_dsa_solutions` moves each
answer to `DSA/{id}/solution/main` and removes it from the problem doc:

```bash
cd mobile/scripts/move_dsa_solutions
npm install
node migrate.mjs            # dry run: shows what would move
node migrate.mjs --commit   # backs up answers locally, then moves them
```

Order of operations: deploy the rules, release the app version with gems,
then run the migration. Until it runs, the app falls back to the old field.
After it runs, older app versions just stop showing their Solution menu item.
Re-running the script is safe: problems that were already moved are skipped.
New problems should be added with their answer in `solution/main`.

### Data structures course (Firestore)

The source lives in `mobile/new_course/data_structures/`:

| Path | What it is |
|---|---|
| `curriculum.json` | Modules and lessons (`id`, `module`, `order`, `title`, `desc`) |
| `lessons/<id>.md` | Lesson Markdown |
| `quiz_src/<id>.py` | Quiz source written with `mcq(...)`, `fill(...)` and `order(...)` helpers |
| `quizzes/<id>.json` | Generated quizzes (**do not edit by hand**) |
| `build.py` | Validates every quiz and regenerates `quizzes/*.json` |
| `check_code.py` | Runs `dart analyze` on every runnable example |
| `verify_outputs.py` | Runs each MCQ snippet and compares its output with the answer |
| `verify_lessons.py` | Runs lesson examples and checks their `// expected` comments |

Workflow (from `mobile/new_course/data_structures/`, with Python 3 and the
Dart SDK on your `PATH`):

```bash
python3 build.py
python3 check_code.py
python3 verify_outputs.py
python3 verify_lessons.py
```

`build.py` enforces the quiz widget's constraints:
- at least 50 questions per lesson;
- blanks only inside code blocks;
- `order` answers made of unique options;
- **no question may depend on another**, because the app samples 10 at random.

**Uploading to Firestore** (from `mobile/scripts/upload_dsa_course/`):

```bash
npm install
node upload.mjs            # dry run: validates and prints a summary
node upload.mjs --commit   # writes the 7 module docs and 38 lessons (121 docs)
```

The script needs Admin credentials. Use either
`gcloud auth application-default login` or `GOOGLE_APPLICATION_CREDENTIALS`
pointing to a service-account key. Set `FIREBASE_PROJECT` to target a project
other than `dartcoder-d57cb`. Uploads overwrite documents by lesson ID, so
re-running the script is safe.

### Quiz format

Both courses use the same JSON format: an array of questions. Code goes
inside the `question` text as a fenced ```` ```dart ```` block, and `answer` is
always a list.

```json
[
  {
    "type": "mcq",
    "question": "What does this print?\n\n```dart\nvoid main() {\n  print([1, 2, 3].length);\n}\n```",
    "options": ["3", "2", "4", "Error"],
    "answer": ["3"]
  },
  {
    "type": "fill",
    "question": "Fill in the blank to make the loop run 5 times:\n\n```dart\nfor (int i = 0; i < %fill%; i++) {\n  print(i);\n}\n```",
    "answer": ["5"]
  },
  {
    "type": "order",
    "question": "Complete the declaration:\n\n```dart\n%order% %order% = %order%;\n```",
    "options": ["const", "pi", "3.14", "var", "final"],
    "answer": ["const", "pi", "3.14"]
  }
]
```

| Type | How it works |
|---|---|
| `mcq` | Pick one of `options`. `answer[0]` is the correct option. |
| `fill` | Each `%fill%` in the code is a text field. `answer` lists the expected values in order. |
| `order` | Each `%order%` is a slot. The learner taps tokens from `options` (which can include distractors) to fill the slots in the order given by `answer`. |

---

## Buying gems (RevenueCat)

Gems are consumable in-app purchases sold through Apple and Google billing,
using RevenueCat. That is what both stores require for in-app currency, so
the **Get gems** sheet is allowed inside the app. The flow:

1. The app logs the user in to RevenueCat with their Firebase uid.
2. The user buys a pack in the **Get gems** sheet (Apple / Google payment
   sheet).
3. RevenueCat calls `POST /api/revenuecat/webhook` on the Vercel deployment.
4. The webhook adds the pack's gems to `Users/{uid}/wallet/main` and records
   `Purchases/{store}_{transactionId}`, so retries never credit twice.
5. The app's wallet streams from Firestore, so the new balance appears
   within seconds. Refunds take the gems back, never below zero.

**One-time setup**

1. **Stores.** Create consumable products named `dartic_gems_<amount>`, for
   example `dartic_gems_10`, `dartic_gems_30` and `dartic_gems_100`. The amount
   in the ID is what the user receives. Use App Store Connect (In-App Purchases)
   and Play Console (Monetize → In-app products).
2. **RevenueCat.** Create a project with the iOS and Android apps. Add the
   products, and put them in an offering with identifier **`gems`**.
3. **Webhook.** In RevenueCat → Integrations → Webhooks, set the URL to
   `https://<your-vercel-domain>/api/revenuecat/webhook`. Set an Authorization
   header value (a long random string). Optionally enable HMAC signing.
4. **Vercel environment variables** (see `landing_page/api/.env.example`):
   `REVENUECAT_WEBHOOK_AUTH` (the same Authorization value),
   `REVENUECAT_WEBHOOK_SECRET` (optional signing secret), and
   `FIREBASE_SERVICE_ACCOUNT`. For the last one, use Firebase console →
   Project settings → Service accounts → Generate new private key, and paste
   the JSON as one line.
5. **App build.** Pass `--dart-define=RC_APPLE_KEY=appl_…` and
   `--dart-define=RC_GOOGLE_KEY=goog_…` (RevenueCat → API keys → public
   app-specific keys).
6. **Review.** Attach the in-app purchases to the app version in App Store
   Connect. Apple's reviewer buys in the sandbox, and the webhook credits
   sandbox purchases too.

Use RevenueCat's **Send test event** to check the URL and auth. Test events
are acknowledged and ignored.

## Landing page

`landing_page/` holds the website and a small FastAPI app. The static site in
`public/` has no build step. On Vercel, `public/` is served from the CDN and
the FastAPI app in `api/` runs as a Python function (`/api/*`). Firebase Hosting can also serve
`public/` at <https://dartcoder-d57cb.web.app>, but the API only runs on Vercel.

| File (in `public/` unless noted) | Purpose |
|---|---|
| `index.html` | Page markup: hero with app screenshots, topic ticker, "inside the app" grid, curriculum, sample quiz, FAQ, download CTA. Includes SEO, Open Graph, JSON-LD and Smart App Banner metadata. |
| `styles.css` | Design system (paper/ink palette with one accent, light/dark themes, Space Grotesk + system mono) and all components |
| `main.js` | Theme toggle (saved in `localStorage`), mobile menu, scroll reveals, counters, topic ticker, code-runner demo, curriculum explorer, sample quiz (keys 1–4 / Enter), store links |
| `privacy/`, `terms/`, `legal.css`, `legal.js` | Legal pages at `/privacy/` and `/terms/`. **The app links to these URLs** (`AppLinks` in `mobile/lib/shared/app_string.dart`). Old `.html` URLs redirect. |
| `404.html`, `robots.txt`, `sitemap.xml` | Hosting extras |
| `analytics.js` | Vercel Web Analytics loader (skipped on Firebase Hosting and localhost) |
| `api/` (root) | FastAPI app (`index.py`) and gem-purchase webhook (`gem_webhook.py`), see [Buying gems](#buying-gems-revenuecat) |
| `pyproject.toml` (root) | Python dependencies and the Vercel entrypoint `api.index:app` |
| `firebase.json` (root) | Firebase Hosting config (serves `public/`) and cache headers |
| `vercel.json`, `.vercelignore` (root) | Vercel function config and the same cache headers |

**Preview the site locally:**

```bash
cd landing_page
python3 -m http.server 8080 --directory public   # then open http://localhost:8080
```

**Run the API tests** (Firestore emulator, Java 21+):

```bash
cd landing_page
pip install -e ".[test]"
firebase emulators:exec --only firestore --project demo-dartic \
  "FIREBASE_PROJECT_ID=demo-dartic python -m pytest -q"
```

**Deploy to Vercel:** create a Vercel project with **Root Directory** set to
`landing_page`. Vercel detects FastAPI from `pyproject.toml`, which points it at
`api/index.py`.
Add the environment variables above, then deploy (or run `vercel --prod`
from `landing_page/`).

**Deploy the site to Firebase Hosting** (static only):

```bash
cd landing_page
firebase deploy --only hosting
```

**Analytics.** `analytics.js` adds [Vercel Web Analytics](https://vercel.com/docs/analytics)
to every page. It only records on Vercel deployments: enable **Analytics** for the
project in the Vercel dashboard, then redeploy. On Firebase Hosting and local
previews the tracking script is skipped. Clicks on the store buttons are sent as
a `Store click` custom event, which Vercel records on Pro and Enterprise plans.

**Store links.** The App Store and Google Play URLs live in `STORE_LINKS` at the
top of `main.js` (and in the footer and JSON-LD in `index.html`). If a link is
ever emptied, its button switches to a disabled "Coming soon" state.

**Screenshots.** `public/assets/img/screens/*.jpg` are real captures from the iOS
simulator (720px wide JPEGs). To refresh them, run the app in the simulator,
set a clean status bar with
`xcrun simctl status_bar booted override --time 9:41 --batteryLevel 100`,
save with `xcrun simctl io booted screenshot <name>.png`, then resize.

**Keeping it in sync.** The curriculum explorer and the stats in `index.html`
mirror the app's content (`CURRICULUM` and `QUIZ` in `main.js`). Update them
when lessons are added.

The page supports `prefers-color-scheme`, `prefers-reduced-motion`, keyboard
navigation (including arrow keys on the curriculum tabs) and still renders
its content without JavaScript.

---

## Contributing

Contributions are welcome: code, lessons, quiz questions, problems and design.

1. Fork the repo and branch from `dev`: `git checkout -b feature/my-change dev`.
2. Make your change:
   - **App code:** run `fvm flutter analyze` and `fvm flutter test`. Follow
     the existing feature/Cubit structure and keep Firebase calls in
     `FirebaseServices`.
   - **DS lessons or quizzes:** edit `lessons/*.md` or `quiz_src/*.py`, then
     run all four validators. Never hand-edit `quizzes/*.json`.
   - **Dart lessons:** keep code samples runnable and outputs accurate.
   - **Landing page:** check it at desktop and phone widths, in both light
     and dark themes.
3. Use [Conventional Commits](https://www.conventionalcommits.org)
   (`feat:`, `fix:`, `refactor:`, `chore:` …), with scopes like `feat(landing):`.
4. Open a pull request against `dev`, describe the change, and add
   screenshots for UI work.

Report bugs and request features in
[GitHub Issues](https://github.com/Odinachi/dartcoder/issues).

---

## Roadmap

- [ ] Search across lessons
- [ ] Algorithms course (the third learning path) with the same pipeline as the DS course
- [ ] Data structures capstone project
- [ ] Export and import code snippets
- [ ] Leaderboards and streak rewards
- [ ] Web build of the app

---

## License

No license file has been added yet, so all rights are reserved by default.
If you plan to reuse the code, open an issue first.

## Contact

- **Issues:** <https://github.com/Odinachi/dartcoder/issues>
- **Email:** [odinachidavid@yahoo.com](mailto:odinachidavid@yahoo.com)

Inspired by [DartPad](https://dartpad.dev). Thanks to the Flutter and Dart teams.
