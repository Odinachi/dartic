# Topological Sort

Imagine getting dressed in the morning 👔.

- Socks go on **before** shoes. 🧦 → 👟
- Underwear goes on **before** trousers, and trousers **before** shoes and belt.
- A shirt goes on **before** a tie and a jacket.

Some items depend on others; some (like a watch ⌚) don't depend on anything. You need an order that **respects every rule**. Putting shoes on before socks? Not happening.

👉 That's **topological sort**:

> A **topological order** of a **directed acyclic graph (DAG)** is a linear ordering of its vertices such that for every edge **u → v**, **u comes before v**. It exists **only if the graph has no cycles**.

Topological sort powers build systems, package managers (including `pub get` resolving dependencies), course planners, spreadsheet recalculation and task schedulers.

---

## 🧠 Modeling Dependencies as a DAG

Draw an edge **u → v** meaning *"u must happen before v"*.

```text
underwear → trousers → shoes
                    ↘
socks ───────────→ shoes
trousers → belt
shirt → tie → jacket
shirt → belt
watch (no dependencies)
```

Valid orders include:

- `underwear, socks, shirt, watch, trousers, tie, belt, shoes, jacket`
- `watch, shirt, tie, jacket, socks, underwear, trousers, belt, shoes`

> 💡 A DAG usually has **many** valid topological orders. Any order that respects every edge is correct.

---

## 🧮 Kahn's Algorithm (BFS with In-Degrees)

The **in-degree** of a vertex is the number of edges pointing **into** it: how many things must happen first.

1. Compute every vertex's in-degree.
2. Put all vertices with in-degree **0** (nothing blocking them) in a queue.
3. Repeatedly take a vertex from the queue, add it to the result, and "remove" its outgoing edges by decrementing each neighbor's in-degree. Any neighbor that drops to 0 joins the queue.
4. If the result contains **every** vertex, it's a valid order. If not, the leftover vertices are stuck in a **cycle**.

```dart
import 'dart:collection';

List<String>? kahn(Map<String, List<String>> graph) {
  // 1. In-degrees
  final inDegree = {for (final v in graph.keys) v: 0};
  for (final targets in graph.values) {
    for (final t in targets) {
      inDegree[t] = (inDegree[t] ?? 0) + 1;
    }
  }

  // 2. Start with everything that has no prerequisites
  final ready = Queue<String>.from(
      inDegree.entries.where((e) => e.value == 0).map((e) => e.key));
  final order = <String>[];

  // 3. Peel off vertices layer by layer
  while (ready.isNotEmpty) {
    final v = ready.removeFirst();
    order.add(v);
    for (final next in graph[v] ?? const <String>[]) {
      inDegree[next] = inDegree[next]! - 1;
      if (inDegree[next] == 0) ready.add(next);
    }
  }

  // 4. Every vertex placed? Otherwise there's a cycle.
  return order.length == inDegree.length ? order : null;
}

void main() {
  final dressing = {
    'underwear': ['trousers'],
    'socks': ['shoes'],
    'trousers': ['shoes', 'belt'],
    'shirt': ['tie', 'belt'],
    'tie': ['jacket'],
    'belt': ['jacket'],
    'shoes': <String>[],
    'jacket': <String>[],
    'watch': <String>[],
  };
  print(kahn(dressing));
  // [underwear, socks, shirt, watch, trousers, tie, shoes, belt, jacket]
}
```

**🔍 What This Code Does:**

This code demonstrates **Kahn's algorithm for topological sorting**:

1. **In-Degree Map**: Counts how many prerequisites each vertex has. Vertices that only appear as targets are handled with `?? 0`.

2. **Ready Queue**: Vertices with in-degree 0 can be done right away.

3. **Removing a Vertex**: Each outgoing edge is "deleted" by decrementing the target's in-degree. When a target reaches 0, all its prerequisites are done, so it becomes ready.

4. **Cycle Detection Built In**: Vertices in a cycle never reach in-degree 0, so they're never placed. If `order` is shorter than the vertex count, we return `null`.

5. **O(V + E)**: Each vertex is queued once and each edge decremented once.

---

## 🔄 Detecting Impossible Plans

```dart
import 'dart:collection';

List<String>? kahn(Map<String, List<String>> g) {
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = (inDeg[t] ?? 0) + 1;
    }
  }
  final q = Queue.of(inDeg.keys.where((v) => inDeg[v] == 0));
  final out = <String>[];
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    out.add(v);
    for (final w in g[v] ?? const <String>[]) {
      if ((inDeg[w] = inDeg[w]! - 1) == 0) q.add(w);
    }
  }
  return out.length == inDeg.length ? out : null;
}

void main() {
  final courses = {
    'Intro to Dart': ['Flutter Basics'],
    'Flutter Basics': ['State Management'],
    'State Management': ['Advanced Flutter'],
    'Advanced Flutter': <String>[],
  };
  print(kahn(courses));
  // [Intro to Dart, Flutter Basics, State Management, Advanced Flutter]

  courses['Advanced Flutter'] = ['Intro to Dart']; // circular!
  print(kahn(courses)); // null: no valid order exists
}
```

**🔍 What This Code Does:**

1. **A Chain**: Four courses in a strict sequence produce exactly one valid order.
2. **Adding a Cycle**: Now every course depends (indirectly) on itself, so no course ever reaches in-degree 0.
3. **`null` Result**: Signals that the schedule is impossible.
4. **Assignment as an Expression**: `(inDeg[w] = inDeg[w]! - 1) == 0` updates and tests in one step.

---

## 🧗 DFS-Based Topological Sort

The other classic approach: run DFS, and add each vertex to a list **after** all its descendants are finished (post-order). **Reversing** that list gives a topological order.

Why? A vertex finishes only after everything it points to has finished, so in the reversed list it appears **before** all of them.

```dart
List<String>? topoDfs(Map<String, List<String>> g) {
  final state = <String, int>{}; // 0/missing = unvisited, 1 = visiting, 2 = done
  final postOrder = <String>[];
  var hasCycle = false;

  void visit(String v) {
    if (hasCycle) return;
    state[v] = 1;
    for (final w in g[v] ?? const <String>[]) {
      final s = state[w] ?? 0;
      if (s == 1) {
        hasCycle = true; // back edge
        return;
      }
      if (s == 0) visit(w);
    }
    state[v] = 2;
    postOrder.add(v); // all of v's dependents are already in the list
  }

  for (final v in g.keys) {
    if ((state[v] ?? 0) == 0) visit(v);
  }
  return hasCycle ? null : postOrder.reversed.toList();
}

void main() {
  final build = {
    'download': ['compile'],
    'compile': ['test', 'package'],
    'test': ['deploy'],
    'package': ['deploy'],
    'deploy': <String>[],
  };
  print(topoDfs(build)); // [download, compile, package, test, deploy]
}
```

**🔍 What This Code Does:**

1. **Three States**: Like cycle detection: unvisited, visiting (on the current path), done.
2. **Post-Order Append**: A vertex is added only after all vertices it points to are done.
3. **Reverse at the End**: Turns "dependents first" into "prerequisites first".
4. **Back Edge = Cycle**: Meeting a "visiting" vertex means the graph isn't a DAG.
5. **O(V + E)**, the same as Kahn's.

| | Kahn's (BFS) | DFS-based |
|---|--------------|-----------|
| Idea | Repeatedly take vertices with no remaining prerequisites | Reverse post-order of DFS |
| Cycle detection | Leftover vertices | Back edge to a "visiting" vertex |
| Natural extras | Parallel "waves", lexicographic order | Fits recursive code |
| Recursion | None | Yes (or an explicit stack) |

---

## 🌊 Parallel Scheduling: Levels of a DAG

Kahn's algorithm naturally finds **waves** of tasks that can run **at the same time**: everything with in-degree 0 now, then everything unlocked by them, and so on. The number of waves is the minimum number of rounds needed with unlimited workers.

```dart
List<List<String>> waves(Map<String, List<String>> g) {
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = inDeg[t]! + 1;
    }
  }
  var current = [for (final v in g.keys) if (inDeg[v] == 0) v];
  final result = <List<String>>[];
  while (current.isNotEmpty) {
    result.add(current);
    final next = <String>[];
    for (final v in current) {
      for (final w in g[v]!) {
        inDeg[w] = inDeg[w]! - 1;
        if (inDeg[w] == 0) next.add(w);
      }
    }
    current = next;
  }
  return result;
}

void main() {
  final pipeline = {
    'fetch deps': ['build app', 'build docs'],
    'lint': ['build app'],
    'build app': ['run tests'],
    'build docs': ['publish'],
    'run tests': ['publish'],
    'publish': <String>[],
  };
  final plan = waves(pipeline);
  for (final (i, wave) in plan.indexed) {
    print('round ${i + 1}: $wave');
  }
  // round 1: [fetch deps, lint]
  // round 2: [build app, build docs]
  // round 3: [run tests]
  // round 4: [publish]
}
```

**🔍 What This Code Does:**

1. **Level-by-Level Kahn's**: Process the whole current wave before building the next one.
2. **Parallel Rounds**: Tasks in the same wave don't depend on each other, so a CI system could run them simultaneously.
3. **Critical Path**: The number of rounds (4) is the longest dependency chain.

---

## 🔤 Lexicographically Smallest Order

When several tasks are ready, which comes first? Using a **priority queue** (instead of a FIFO queue) always picks the alphabetically smallest ready task, giving a deterministic, canonical order.

```dart
import 'dart:collection';

List<String> smallestTopo(Map<String, List<String>> g) {
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = inDeg[t]! + 1;
    }
  }
  final ready = SplayTreeSet<String>.of(inDeg.keys.where((v) => inDeg[v] == 0));
  final out = <String>[];
  while (ready.isNotEmpty) {
    final v = ready.first;
    ready.remove(v);
    out.add(v);
    for (final w in g[v]!) {
      if ((inDeg[w] = inDeg[w]! - 1) == 0) ready.add(w);
    }
  }
  return out;
}

void main() {
  print(smallestTopo({
    'c': ['a'],
    'b': ['a'],
    'a': <String>[],
    'd': <String>[],
  })); // [b, c, a, d]
}
```

**🔍 What This Code Does:**

1. **Sorted Ready Set**: `SplayTreeSet` keeps ready vertices in alphabetical order.
2. **Always the Smallest**: `ready.first` picks the alphabetically first available task.
3. **Deterministic Output**: Useful when tests or users need the same answer every time.

---

## 🧩 Real Example: Alien Dictionary

Given a list of words **sorted** in an unknown alphabet, figure out the letter order. Each adjacent pair of words reveals one rule at their first differing letter.

```dart
import 'dart:collection';

String? alienOrder(List<String> words) {
  final graph = <String, Set<String>>{};
  for (final w in words) {
    for (final ch in w.split('')) {
      graph.putIfAbsent(ch, () => {});
    }
  }
  for (var i = 0; i + 1 < words.length; i++) {
    final a = words[i], b = words[i + 1];
    final len = a.length < b.length ? a.length : b.length;
    var found = false;
    for (var j = 0; j < len; j++) {
      if (a[j] != b[j]) {
        graph[a[j]]!.add(b[j]); // a[j] comes before b[j]
        found = true;
        break;
      }
    }
    if (!found && a.length > b.length) return null; // "abc" before "ab" is invalid
  }

  final inDeg = {for (final c in graph.keys) c: 0};
  graph.forEach((_, outs) {
    for (final o in outs) {
      inDeg[o] = inDeg[o]! + 1;
    }
  });
  final q = Queue.of(inDeg.keys.where((c) => inDeg[c] == 0));
  final out = StringBuffer();
  var placed = 0;
  while (q.isNotEmpty) {
    final c = q.removeFirst();
    out.write(c);
    placed++;
    for (final n in graph[c]!) {
      if ((inDeg[n] = inDeg[n]! - 1) == 0) q.add(n);
    }
  }
  return placed == graph.length ? out.toString() : null;
}

void main() {
  print(alienOrder(['wrt', 'wrf', 'er', 'ett', 'rftt'])); // wertf
  print(alienOrder(['z', 'x', 'z']));                     // null (cycle)
}
```

**🔍 What This Code Does:**

1. **Build the Graph**: Each adjacent word pair gives one edge at the first position where they differ (`t → f`, `w → e`, `r → t`, `e → r`).
2. **Invalid Prefix Case**: A longer word can't come before its own prefix.
3. **Kahn's Algorithm**: Produces the letter order.
4. **Contradiction Detection**: `z → x` and `x → z` form a cycle, so there's no valid alphabet.

---

## ⚠️ Common Mistakes

### 1. Reversing the edge direction

Decide clearly: `u → v` means **u before v**. Mixing "depends on" and "is required by" flips the answer.

### 2. Forgetting vertices that only appear as targets

If `'shoes'` is never a key, your in-degree map might miss it. Initialize every vertex, including pure targets.

### 3. Not checking for cycles

Kahn's algorithm silently returns a **partial** order when there's a cycle. Always compare the result length with the vertex count.

### 4. Expecting one unique answer

Most DAGs have many valid orders. Tests should check that every edge is respected, or use the lexicographic variant for a canonical answer.

---

## 🧪 Try It Yourself

1. **Course schedule**: given `numCourses` and prerequisite pairs, return `true` if all courses can be finished.
2. **Build order**: given packages and their dependencies, print an install order or report a circular dependency.
3. **Longest path in a DAG**: after topological sorting, compute the longest chain of tasks (the critical path).
4. Write `isValidOrder(graph, order)` that checks whether a proposed order respects every edge.

```dart
bool isValidOrder(Map<String, List<String>> g, List<String> order) {
  final position = {for (final (i, v) in order.indexed) v: i};
  if (position.length != g.length) return false;
  for (final MapEntry(key: u, value: targets) in g.entries) {
    for (final v in targets) {
      if (position[u]! > position[v]!) return false; // edge u → v violated
    }
  }
  return true;
}

void main() {
  final g = {'a': ['b'], 'b': ['c'], 'c': <String>[]};
  print(isValidOrder(g, ['a', 'b', 'c'])); // true
  print(isValidOrder(g, ['b', 'a', 'c'])); // false
}
```

**🔍 What This Code Does:**

1. **Position Map**: Records where each vertex appears in the proposed order.
2. **Check Every Edge**: For `u → v`, `u` must come first.
3. **Map Entry Pattern**: `MapEntry(key: u, value: targets)` destructures each entry with custom names.

---

## 📌 Key Takeaways

- ✅ A **topological order** lists a DAG's vertices so every edge **u → v** has **u before v**.
- ✅ It exists **only for DAGs**; a cycle makes it impossible.
- ✅ **Kahn's algorithm**: repeatedly take vertices with **in-degree 0**; leftovers mean a cycle.
- ✅ **DFS approach**: **reverse post-order**; a back edge means a cycle.
- ✅ Both run in **O(V + E)**.
- ✅ Level-by-level Kahn's gives **parallel waves**; a **priority queue** gives the lexicographically smallest order.
- ✅ Used in build systems, package managers, course planning and spreadsheets.

**Next up:** 🛣️ **Shortest Paths**: BFS for unweighted graphs and Dijkstra for weighted ones.
