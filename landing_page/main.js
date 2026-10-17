// Dartic landing page interactions. No dependencies, no build step.

// ── Store links ───────────────────────────────────────────────
// Published store URLs. If one is ever emptied, its button switches to a
// disabled "coming soon" state and a note points to GitHub instead.
const STORE_LINKS = {
  appStore: "https://apps.apple.com/us/app/dartic/id6744124202",
  googlePlay: "https://play.google.com/store/apps/details?id=com.odibillz.dartcoder",
};

// ── Curriculum (mirrors the app's content) ────────────────────
// Dart: mobile/lib/shared/constants.dart (AppData.courses)
// Data structures: mobile/new_course/data_structures/curriculum.json
const CURRICULUM = {
  dart: [
    {
      title: "Basics",
      desc: "Syntax, collections and control flow.",
      lessons: [
        "Introduction", "Variables and Data Types", "Operators", "Comments",
        "Input/Output", "Control Flow", "Switch case", "For Loops", "While Loops",
        "Do-While Loops", "List", "Sets", "Maps", "Functions", "Enums", "Null Safety",
      ],
    },
    {
      title: "Intermediate",
      desc: "Object-oriented and functional Dart.",
      lessons: [
        "Classes and objects", "Inheritance", "Abstract Class", "Mixins",
        "Getters and Setters", "Anonymous Functions", "Higher-Order Functions",
        "Closures", "Try-Catch, finally", "Custom Exception",
      ],
    },
    {
      title: "Advanced",
      desc: "Async code, generics and modern language features.",
      lessons: [
        "Futures", "Async/Await", "Streams", "Generics", "Extension Methods",
        "Sealed Classes", "Unit Testing (Basic)", "Isolates", "Collection Methods",
      ],
    },
  ],
  ds: [
    { title: "Foundations", desc: "Complexity, recursion and how Dart stores data.", lessons: ["Why Data Structures Matter", "Big O: Time & Space", "Amortized Analysis", "Recursion & Iteration", "How Dart Stores Data"] },
    { title: "Linear Structures", desc: "Lists, strings, linked lists, stacks and queues.", lessons: ["Arrays & Dart Lists", "Strings as Data Structures", "Two Pointers & Sliding Window", "Prefix Sums & Difference Arrays", "Singly Linked Lists", "Doubly & Circular Linked Lists", "Stacks", "Queues & Deques"] },
    { title: "Hashing", desc: "Hash tables, collisions and Dart's Map and Set.", lessons: ["Hash Tables from Scratch", "Handling Collisions", "Dart's Map & Set Family", "Hashing Patterns"] },
    { title: "Trees", desc: "Binary trees, BSTs, heaps and tries.", lessons: ["Tree Fundamentals", "Binary Tree Traversals", "Level-Order Traversal", "Binary Search Trees", "Balanced Trees", "Heaps & Priority Queues", "Tries"] },
    { title: "Graphs", desc: "Representations, traversals and shortest paths.", lessons: ["Representing Graphs", "Graph BFS & DFS", "Topological Sort", "Shortest Paths", "Union-Find", "Minimum Spanning Trees"] },
    { title: "Sorting & Searching", desc: "Binary search and the classic sorting algorithms.", lessons: ["Binary Search", "Elementary Sorts", "Merge Sort & Quick Sort", "Counting & Radix Sort"] },
    { title: "Advanced", desc: "Range queries, caches, probabilistic structures and DP.", lessons: ["Segment & Fenwick Trees", "LRU Cache", "Bloom Filters & Skip Lists", "Dynamic Programming Basics"] },
  ],
};

// ── Sample quiz (real questions from the app's question bank) ──
const QUIZ = [
  {
    topic: "Big O",
    question: "What does this print?",
    code: "void main() {\n  var n = 16;\n  var count = 0;\n  while (n > 1) {\n    n ~/= 2;\n    count++;\n  }\n  print(count);\n}",
    options: ["4", "8", "16", "5"],
    answer: "4",
    explain: "The loop halves n each time (16 → 8 → 4 → 2 → 1), so it runs log₂ 16 = 4 times. That's what O(log n) looks like.",
  },
  {
    topic: "Stacks",
    question: "What does this print?",
    code: "void main() {\n  final s = ['a', 'b', 'c'];\n  final out = <String>[];\n  while (s.isNotEmpty) {\n    out.add(s.removeLast());\n  }\n  print(out.join());\n}",
    options: ["cba", "abc", "a", "c"],
    answer: "cba",
    explain: "A List used with removeLast() is a stack: last in, first out. The items come back in reverse order.",
  },
  {
    topic: "Sets",
    question: "What happens when you add a duplicate value to a Set?",
    code: "void main() {\n  Set<int> numbers = {1, 2, 3};\n  numbers.add(2);\n  print(numbers);\n}",
    options: ["{1, 2, 3}", "{1, 2, 3, 2}", "Error", "{2, 3}"],
    answer: "{1, 2, 3}",
    explain: "Sets only keep unique values. add() returns false and the set is unchanged.",
  },
];


const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// ── Header: border on scroll + mobile menu ────────────────────
function initHeader() {
  const header = $(".site-header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const toggle = $(".menu-toggle");
  const links = $("#nav-links");
  const setOpen = (open) => {
    links.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };
  toggle.addEventListener("click", () => setOpen(!links.classList.contains("open")));
  links.addEventListener("click", (e) => {
    if (e.target.closest("a")) setOpen(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
}

// ── Theme toggle (remembers the choice) ───────────────────────
function initTheme() {
  const root = document.documentElement;
  const current = () =>
    root.dataset.theme ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

  $(".theme-toggle").addEventListener("click", () => {
    const next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("dartic-theme", next);
    } catch (e) {
      /* storage unavailable (private mode): the toggle still works for this visit */
    }
  });
}

// ── Topic ticker: every lesson title, duplicated for a seamless loop ──
function initTicker() {
  const track = $("#ticker");
  const topics = [...CURRICULUM.dart, ...CURRICULUM.ds].flatMap((m) => m.lessons);
  const html = topics.map((t) => `<span>${t.replace(/&/g, "&amp;")}</span>`).join("");
  track.innerHTML = html + html;
}

// ── Reveal-on-scroll and number counters ──────────────────────
function initReveal() {
  const items = $$(".reveal");
  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" },
  );
  items.forEach((el) => observer.observe(el));
}

function initCounters() {
  if (prefersReducedMotion || !("IntersectionObserver" in window)) return;
  const format = (n, el) =>
    el.dataset.format === "comma" ? n.toLocaleString("en-US") : String(n);

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const el = entry.target;
      const target = Number(el.dataset.count);
      const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / 1200);
        el.textContent = format(Math.round(target * (1 - Math.pow(1 - t, 4))), el);
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      observer.unobserve(el);
    }
  }, { threshold: 0.6 });
  $$("[data-count]").forEach((el) => observer.observe(el));
}

// ── Code runner demo ──────────────────────────────────────────
function initCodeDemo() {
  const btn = $("#run-btn");
  const out = $("#code-output .out");
  const lines = ["Ada scored 95", "Linus scored 88", "not enrolled"];

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Running…";
    out.classList.remove("idle");
    out.textContent = "";
    await wait(prefersReducedMotion ? 0 : 380);
    for (const line of lines) {
      out.textContent += (out.textContent ? "\n" : "") + line;
      await wait(prefersReducedMotion ? 0 : 200);
    }
    btn.disabled = false;
    btn.textContent = "▶ Run";
  });
}

// ── Curriculum (table of contents) ────────────────────────────
function initCurriculum() {
  const panel = $("#curriculum-panel");
  const tabs = $$(".tab");
  const pad = (n) => String(n).padStart(2, "0");

  const render = (key) => {
    const modules = CURRICULUM[key];
    panel.innerHTML = "";
    modules.forEach((module, i) => {
      const details = document.createElement("details");
      details.className = "module";
      if (i === 0) details.open = true;

      const summary = document.createElement("summary");
      summary.innerHTML = `
        <span class="num">${pad(i + 1)}</span>
        <span><h3></h3><span class="desc"></span></span>
        <span class="count">${module.lessons.length} lessons</span>
        <span class="chev" aria-hidden="true"></span>`;
      summary.querySelector("h3").textContent = module.title;
      summary.querySelector(".desc").textContent = module.desc;

      const list = document.createElement("ol");
      for (const lesson of module.lessons) {
        const li = document.createElement("li");
        li.textContent = lesson;
        list.append(li);
      }
      details.append(summary, list);
      panel.append(details);
    });
    $("#total-modules").textContent = modules.length;
    $("#total-lessons").textContent = modules.reduce((n, m) => n + m.lessons.length, 0);
  };

  const select = (tab) => {
    tabs.forEach((t) => t.setAttribute("aria-selected", String(t === tab)));
    panel.setAttribute("aria-labelledby", tab.id);
    render(tab.dataset.tab);
  };

  tabs.forEach((tab) => tab.addEventListener("click", () => select(tab)));
  // Arrow-key navigation between tabs (WAI-ARIA tabs pattern)
  $(".seg").addEventListener("keydown", (e) => {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    const i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    const next = tabs[(i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length];
    next.focus();
    select(next);
  });

  render("dart");
}

// ── Sample quiz ───────────────────────────────────────────────
function initQuiz() {
  let index = 0;
  let score = 0;
  let answered = false;
  let finished = false;
  const results = [];
  const els = {
    card: $("#quiz-card"),
    topic: $("#quiz-topic"),
    count: $("#quiz-count"),
    question: $("#quiz-question"),
    code: $("#quiz-code"),
    options: $("#quiz-options"),
    feedback: $("#quiz-feedback"),
    hint: $("#quiz-hint"),
    next: $("#quiz-next"),
    score: $$("#quiz-score span"),
  };

  const paintScore = () => {
    els.score.forEach((bar, i) => {
      bar.className =
        results[i] === true ? "good" : results[i] === false ? "bad" : i === index && !finished ? "current" : "";
    });
  };

  const show = () => {
    const q = QUIZ[index];
    answered = false;
    els.topic.textContent = q.topic;
    els.count.textContent = `${index + 1} / ${QUIZ.length}`;
    els.question.textContent = q.question;
    els.code.hidden = !q.code;
    els.code.textContent = q.code || "";
    els.feedback.textContent = "";
    els.hint.textContent = "Pick an answer";
    els.next.hidden = true;
    els.options.innerHTML = "";

    q.options.forEach((option, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option";
      btn.innerHTML = `<span class="key" aria-hidden="true">${i + 1}</span><span></span>`;
      btn.lastChild.textContent = option;
      btn.addEventListener("click", () => choose(btn, option));
      els.options.append(btn);
    });
    paintScore();
  };

  const choose = (btn, option) => {
    if (answered) return;
    answered = true;
    const q = QUIZ[index];
    const correct = option === q.answer;
    if (correct) score++;
    results[index] = correct;
    for (const b of $$(".quiz-option", els.options)) {
      b.disabled = true;
      if (b.lastChild.textContent === q.answer) b.classList.add("correct");
    }
    if (!correct) btn.classList.add("wrong");

    els.feedback.innerHTML = `<strong>${correct ? "Correct." : "Not quite."}</strong> `;
    els.feedback.append(q.explain);
    els.hint.textContent = "Press Enter to continue";
    els.next.hidden = false;
    els.next.textContent = index === QUIZ.length - 1 ? "See score" : "Next";
    paintScore();
  };

  const advance = () => {
    if (finished) {
      finished = false;
      index = 0;
      score = 0;
      results.length = 0;
      show();
      return;
    }
    if (index < QUIZ.length - 1) {
      index++;
      show();
      return;
    }
    finished = true;
    els.topic.textContent = "Result";
    els.count.textContent = `${score} / ${QUIZ.length}`;
    els.question.textContent =
      score === QUIZ.length ? "Perfect score." : `You got ${score} of ${QUIZ.length}.`;
    els.code.hidden = true;
    els.options.innerHTML = "";
    els.feedback.textContent =
      "The app has over 4,000 more like these, with 10 fresh questions on every attempt.";
    els.hint.textContent = "";
    els.next.textContent = "Try again";
    paintScore();
  };

  els.next.addEventListener("click", advance);

  // Keyboard: 1–4 to answer, Enter to continue, while the quiz is on screen
  const inView = () => {
    const r = els.card.getBoundingClientRect();
    return r.top < window.innerHeight * 0.75 && r.bottom > window.innerHeight * 0.25;
  };
  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey || !inView()) return;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName)) return;
    const n = Number(e.key);
    const options = $$(".quiz-option", els.options);
    if (!answered && n >= 1 && n <= options.length) {
      options[n - 1].click();
    } else if (e.key === "Enter" && !els.next.hidden && document.activeElement !== els.next) {
      e.preventDefault();
      advance();
    }
  });

  show();
}

// ── Store buttons ─────────────────────────────────────────────
function initStoreLinks() {
  let missing = 0;
  for (const btn of $$("[data-store]")) {
    const url = STORE_LINKS[btn.dataset.store];
    if (url) {
      btn.href = url;
      // Custom event (recorded on Vercel Pro/Enterprise; ignored otherwise).
      btn.addEventListener("click", () =>
        window.va?.("event", { name: "Store click", data: { store: btn.dataset.store } }),
      );
    } else {
      missing++;
      btn.setAttribute("aria-disabled", "true");
      btn.removeAttribute("href");
      btn.querySelector("small").textContent = "Coming soon to";
    }
  }
  if (missing) {
    $("#store-note").innerHTML =
      'Store listings are on the way. Meanwhile, follow along on <a href="https://github.com/Odinachi/dartcoder" rel="noopener">GitHub</a>.';
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("#year").textContent = String(new Date().getFullYear());
  initHeader();
  initTheme();
  initTicker();
  initCurriculum();
  initQuiz();
  initCodeDemo();
  initStoreLinks();
  initReveal();
  initCounters();
});
