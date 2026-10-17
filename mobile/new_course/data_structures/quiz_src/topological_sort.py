KAHN = r"""import 'dart:collection';

List<String>? kahn(Map<String, List<String>> g) {
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = inDeg[t]! + 1;
    }
  }
  final q = Queue.of(inDeg.keys.where((v) => inDeg[v] == 0));
  final out = <String>[];
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    out.add(v);
    for (final w in g[v]!) {
      inDeg[w] = inDeg[w]! - 1;
      if (inDeg[w] == 0) q.add(w);
    }
  }
  return out.length == inDeg.length ? out : null;
}
"""

QUESTIONS = [
    mcq(r"""
What is a topological order?
""", ["An ordering of a DAG's vertices where every edge u → v has u before v",
       "Vertices sorted alphabetically", "A BFS order of any graph",
       "An order of vertices by degree"],
        "An ordering of a DAG's vertices where every edge u → v has u before v"),

    mcq(r"""
Which graphs have a topological order?
""", ["Directed acyclic graphs (DAGs)", "Any graph", "Only trees", "Undirected graphs"],
        "Directed acyclic graphs (DAGs)"),

    mcq(r"""
Why can't a graph with a cycle be topologically sorted?
""", ["Each vertex in the cycle would have to come before itself",
       "Cycles have no edges", "The algorithm would be too slow", "It can be"],
        "Each vertex in the cycle would have to come before itself"),

    mcq(r"""
How many valid topological orders can a DAG have?
""", ["Possibly many", "Always exactly one", "Always zero", "Exactly two"], "Possibly many"),

    mcq(r"""
What is the in-degree of a vertex?
""", ["The number of edges pointing into it", "The number of edges leaving it",
       "Its position in the order", "The number of vertices"],
        "The number of edges pointing into it"),

    mcq(r"""
In Kahn's algorithm, which vertices start in the queue?
""", ["All vertices with in-degree 0", "All vertices with out-degree 0",
       "Only the first vertex", "All vertices"], "All vertices with in-degree 0"),

    mcq(r"""
In Kahn's algorithm, what happens when a vertex is removed from the queue?
""", ["Its neighbors' in-degrees are decremented; any that reach 0 join the queue",
       "Its neighbors are removed from the graph", "Every vertex's in-degree resets",
       "The algorithm stops"],
        "Its neighbors' in-degrees are decremented; any that reach 0 join the queue"),

    mcq(r"""
How does Kahn's algorithm detect a cycle?
""", ["The result contains fewer vertices than the graph", "The queue never empties",
       "A vertex gets negative in-degree", "It can't detect cycles"],
        "The result contains fewer vertices than the graph"),

    mcq(r"""
What is the time complexity of Kahn's algorithm?
""", ["O(V + E)", "O(V²)", "O(E log V)", "O(V log V)"], "O(V + E)"),

    mcq(r"""
What does this print?

```dart
""" + KAHN + r"""
void main() {
  print(kahn({'a': ['b'], 'b': ['c'], 'c': []}));
}
```
""", ["[a, b, c]", "[c, b, a]", "null", "[a, c, b]"], "[a, b, c]"),

    mcq(r"""
What does this print?

```dart
""" + KAHN + r"""
void main() {
  print(kahn({'a': ['b'], 'b': ['a'], 'c': []}));
}
```
""", ["null", "[c]", "[a, b, c]", "[c, a, b]"], "null"),

    mcq(r"""
What does this print?

```dart
""" + KAHN + r"""
void main() {
  print(kahn({'x': ['z'], 'y': ['z'], 'z': []}));
}
```
""", ["[x, y, z]", "[z, x, y]", "[x, z, y]", "null"], "[x, y, z]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final g = {'a': ['b', 'c'], 'b': ['c'], 'c': <String>[]};
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = inDeg[t]! + 1;
    }
  }
  print(inDeg);
}
```
""", ["{a: 0, b: 1, c: 2}", "{a: 2, b: 1, c: 0}", "{a: 0, b: 0, c: 0}", "{a: 1, b: 1, c: 1}"],
        "{a: 0, b: 1, c: 2}"),

    order(r"""
Complete Kahn's main loop:

```dart
while (ready.isNotEmpty) {
  final v = ready.%order%();
  order.add(v);
  for (final w in graph[v]!) {
    inDegree[w] = inDegree[w]! %order% 1;
    if (inDegree[w] %order% 0) ready.add(w);
  }
}
```
""", ["removeFirst", "-", "==", "removeLast", "+", "!="], ["removeFirst", "-", "=="]),

    mcq(r"""
In the DFS-based topological sort, when is a vertex appended to the list?
""", ["After all the vertices it points to are finished (post-order)",
       "When it's first discovered", "Before exploring any neighbor", "Never"],
        "After all the vertices it points to are finished (post-order)"),

    mcq(r"""
What must you do with the DFS post-order list to get a topological order?
""", ["Reverse it", "Sort it", "Nothing", "Remove duplicates"], "Reverse it"),

    mcq(r"""
How does the DFS approach detect a cycle?
""", ["Finding an edge to a vertex that is still \"visiting\" (a back edge)",
       "Finding an edge to a finished vertex", "When the list is empty",
       "When in-degrees become negative"],
        "Finding an edge to a vertex that is still \"visiting\" (a back edge)"),

    mcq(r"""
What does this print?

```dart
List<String> topo(Map<String, List<String>> g) {
  final done = <String>{};
  final post = <String>[];
  void visit(String v) {
    if (!done.add(v)) return;
    for (final w in g[v]!) {
      visit(w);
    }
    post.add(v);
  }

  g.keys.forEach(visit);
  return post.reversed.toList();
}

void main() {
  print(topo({'a': ['b'], 'b': ['c'], 'c': []}));
}
```
""", ["[a, b, c]", "[c, b, a]", "[b, a, c]", "[a, c, b]"], "[a, b, c]"),

    mcq(r"""
What does this print?

```dart
List<String> post(Map<String, List<String>> g) {
  final done = <String>{};
  final out = <String>[];
  void visit(String v) {
    if (!done.add(v)) return;
    for (final w in g[v]!) {
      visit(w);
    }
    out.add(v);
  }

  g.keys.forEach(visit);
  return out;
}

void main() {
  print(post({'a': ['b'], 'b': ['c'], 'c': []}));
}
```
""", ["[c, b, a]", "[a, b, c]", "[b, c, a]", "[a, c, b]"], "[c, b, a]"),

    mcq(r"""
Why does reversed post-order put prerequisites first?
""", ["A vertex finishes only after everything it points to, so reversing puts it before them",
       "DFS visits prerequisites last", "Because the list is sorted", "It's a coincidence"],
        "A vertex finishes only after everything it points to, so reversing puts it before them"),

    mcq(r"""
Which approach naturally produces "waves" of tasks that can run in parallel?
""", ["Level-by-level Kahn's algorithm", "DFS reverse post-order", "Binary search",
       "Heap sort"], "Level-by-level Kahn's algorithm"),

    mcq(r"""
In a DAG of tasks, what does the number of Kahn "waves" tell you?
""", ["The minimum number of rounds needed with unlimited parallel workers",
       "The number of tasks", "The number of edges", "The number of cycles"],
        "The minimum number of rounds needed with unlimited parallel workers"),

    mcq(r"""
What does this print?

```dart
List<List<String>> waves(Map<String, List<String>> g) {
  final inDeg = {for (final v in g.keys) v: 0};
  for (final ts in g.values) {
    for (final t in ts) {
      inDeg[t] = inDeg[t]! + 1;
    }
  }
  var cur = [for (final v in g.keys) if (inDeg[v] == 0) v];
  final res = <List<String>>[];
  while (cur.isNotEmpty) {
    res.add(cur);
    final next = <String>[];
    for (final v in cur) {
      for (final w in g[v]!) {
        if ((inDeg[w] = inDeg[w]! - 1) == 0) next.add(w);
      }
    }
    cur = next;
  }
  return res;
}

void main() {
  print(waves({'a': ['c'], 'b': ['c'], 'c': ['d'], 'd': []}));
}
```
""", ["[[a, b], [c], [d]]", "[[a], [b], [c], [d]]", "[[a, b, c, d]]", "[[d], [c], [a, b]]"],
        "[[a, b], [c], [d]]"),

    mcq(r"""
How do you get the lexicographically smallest topological order?
""", ["Use a priority queue (sorted set) for ready vertices instead of a FIFO queue",
       "Sort the final result", "Use DFS", "Reverse the alphabet"],
        "Use a priority queue (sorted set) for ready vertices instead of a FIFO queue"),

    mcq(r"""
Why can't you simply sort a topological order alphabetically?
""", ["Sorting can break dependency rules", "Sorting is too slow", "Strings can't be sorted",
       "You can; it's equivalent"], "Sorting can break dependency rules"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final g = {'c': ['a'], 'b': ['a'], 'a': <String>[], 'd': <String>[]};
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
  print(out);
}
```
""", ["[b, c, a, d]", "[a, b, c, d]", "[c, b, a, d]", "[b, c, d, a]"], "[b, c, a, d]"),

    mcq(r"""
In a prerequisite graph, what does an edge u → v mean?
""", ["u must be done before v", "v must be done before u", "u and v can't both be done",
       "u and v are the same task"], "u must be done before v"),

    mcq(r"""
Which real tools rely on topological sorting?
""", ["Build systems and package managers resolving dependencies", "Image compression",
       "Password hashing", "Random number generators"],
        "Build systems and package managers resolving dependencies"),

    mcq(r"""
Why must every vertex (including ones that only appear as edge targets) be in the in-degree map?
""", ["Otherwise some vertices are never placed or cause null errors", "To sort the result",
       "To make it O(1)", "It isn't necessary"],
        "Otherwise some vertices are never placed or cause null errors"),

    mcq(r"""
What happens if you accidentally reverse every edge's meaning ("depends on" vs "must come before")?
""", ["You get the order backwards", "The algorithm crashes", "Cycles appear", "Nothing changes"],
        "You get the order backwards"),

    mcq(r"""
What does `(inDeg[w] = inDeg[w]! - 1) == 0` do?
""", ["Decrements inDeg[w] and checks whether the new value is 0", "Compares without changing",
       "Sets inDeg[w] to 0", "Throws an error"],
        "Decrements inDeg[w] and checks whether the new value is 0"),

    mcq(r"""
Given words sorted in an alien alphabet ['wrt', 'wrf'], what letter rule do you learn?
""", ["t comes before f", "f comes before t", "w comes before r", "Nothing"],
        "t comes before f"),

    mcq(r"""
Given sorted alien words ['abc', 'ab'], what can you conclude?
""", ["The input is invalid: a word can't come before its own prefix",
       "c comes before nothing", "a comes before b", "b comes before c"],
        "The input is invalid: a word can't come before its own prefix"),

    mcq(r"""
In the alien dictionary problem, which pair of words gives a rule?
""", ["Adjacent words, at their first differing letter", "Every pair of letters in a word",
       "The first and last word only", "Words of equal length only"],
        "Adjacent words, at their first differing letter"),

    mcq(r"""
What does this print?

```dart
bool valid(Map<String, List<String>> g, List<String> order) {
  final pos = {for (final (i, v) in order.indexed) v: i};
  for (final MapEntry(key: u, value: ts) in g.entries) {
    for (final v in ts) {
      if (pos[u]! > pos[v]!) return false;
    }
  }
  return true;
}

void main() {
  final g = {'a': ['c'], 'b': ['c'], 'c': <String>[]};
  print(valid(g, ['b', 'a', 'c']));
  print(valid(g, ['a', 'c', 'b']));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What is the longest path in a DAG used for in project planning?
""", ["Finding the critical path: the minimum total time to finish", "Finding cycles",
       "Counting tasks", "Sorting tasks alphabetically"],
        "Finding the critical path: the minimum total time to finish"),

    mcq(r"""
How can you compute the longest path in a DAG efficiently?
""", ["Process vertices in topological order, relaxing longest distances",
       "Use Dijkstra's algorithm directly", "Use BFS on the undirected version",
       "It requires trying every path"],
        "Process vertices in topological order, relaxing longest distances"),

    mcq(r"""
What does this print?

```dart
void main() {
  final order = ['a', 'b', 'c', 'd'];
  final edges = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': <String>[]};
  final longest = {for (final v in order) v: 0};
  for (final u in order) {
    for (final v in edges[u]!) {
      if (longest[u]! + 1 > longest[v]!) longest[v] = longest[u]! + 1;
    }
  }
  print(longest['d']);
}
```
""", ["2", "3", "1", "4"], "2"),

    mcq(r"""
If a course schedule graph has a cycle, what does that mean for students?
""", ["It's impossible to complete all the courses", "They can take courses in any order",
       "Only the first course is required", "Courses can be skipped"],
        "It's impossible to complete all the courses"),

    mcq(r"""
Which structure does Kahn's algorithm use, and which does the DFS approach use?
""", ["Kahn: a queue of ready vertices; DFS: recursion/stack", "Kahn: a stack; DFS: a queue",
       "Both use a heap", "Both use only arrays"],
        "Kahn: a queue of ready vertices; DFS: recursion/stack"),

    mcq(r"""
In a spreadsheet, why is topological sorting used?
""", ["To recalculate cells after the cells they depend on", "To sort rows alphabetically",
       "To compress the file", "To pick cell colors"],
        "To recalculate cells after the cells they depend on"),

    mcq(r"""
What does a spreadsheet report when formulas depend on each other in a loop?
""", ["A circular reference error", "The sum of the cells", "Zero", "Nothing"],
        "A circular reference error"),

    fill(r"""
Create a queue from an existing iterable:

```dart
import 'dart:collection';

void main() {
  final q = Queue.%fill%(['a', 'b']);
  print(q.first); // a
}
```
""", "of"),

    mcq(r"""
What does this print?

```dart
""" + KAHN + r"""
void main() {
  final r = kahn({'shoes': [], 'socks': ['shoes']});
  print(r);
}
```
""", ["[socks, shoes]", "[shoes, socks]", "null", "[]"], "[socks, shoes]"),

    mcq(r"""
In Kahn's algorithm, can a vertex enter the ready queue more than once?
""", ["No, its in-degree reaches 0 exactly once", "Yes, once per incoming edge",
       "Yes, always twice", "Only in undirected graphs"],
        "No, its in-degree reaches 0 exactly once"),

    mcq(r"""
What does a vertex with in-degree 0 represent in a task graph?
""", ["A task with no prerequisites that can start immediately", "The final task",
       "A task in a cycle", "An invalid task"],
        "A task with no prerequisites that can start immediately"),

    mcq(r"""
What does a vertex with out-degree 0 represent in a task graph?
""", ["A task that nothing else depends on", "A task with no prerequisites",
       "A task in a cycle", "The first task"], "A task that nothing else depends on"),

    mcq(r"""
Which statement about topological sort on a tree (edges parent → child) is true?
""", ["Any pre-order or level-order traversal is a valid topological order",
       "Trees can't be topologically sorted", "Only in-order works",
       "Only post-order works"],
        "Any pre-order or level-order traversal is a valid topological order"),

    mcq(r"""
What does this print?

```dart
""" + KAHN + r"""
void main() {
  final r = kahn({'a': [], 'b': [], 'c': []});
  print(r);
}
```
""", ["[a, b, c]", "[]", "null", "[c, b, a]"], "[a, b, c]"),

    mcq(r"""
For a graph with no edges, how many topological orders exist for 3 vertices?
""", ["6 (any permutation)", "1", "0", "3"], "6 (any permutation)"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final graph = <String, Set<String>>{'w': {'e'}, 'e': {'r'}, 'r': {}};
  final inDeg = {for (final c in graph.keys) c: 0};
  graph.forEach((_, outs) {
    for (final o in outs) {
      inDeg[o] = inDeg[o]! + 1;
    }
  });
  final q = Queue.of(inDeg.keys.where((c) => inDeg[c] == 0));
  final sb = StringBuffer();
  while (q.isNotEmpty) {
    final c = q.removeFirst();
    sb.write(c);
    for (final n in graph[c]!) {
      if ((inDeg[n] = inDeg[n]! - 1) == 0) q.add(n);
    }
  }
  print(sb);
}
```
""", ["wer", "rew", "erw", "w"], "wer"),

    mcq(r"""
Which pub command depends on resolving a dependency graph?
""", ["dart pub get", "dart format", "dart analyze", "dart run"], "dart pub get"),

    mcq(r"""
In Kahn's algorithm with a FIFO queue, which ready vertex is processed next?
""", ["The one that became ready earliest", "The alphabetically smallest",
       "The one with the most edges", "A random one"],
        "The one that became ready earliest"),
]
