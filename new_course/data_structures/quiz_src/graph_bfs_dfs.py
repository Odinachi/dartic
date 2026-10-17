G = r"""final g = {
  'A': ['B', 'C'],
  'B': ['A', 'D'],
  'C': ['A', 'D'],
  'D': ['B', 'C', 'E'],
  'E': ['D'],
};
"""

PIC = r"""```dart
// A: [B, C]
// B: [A, D]
// C: [A, D]
// D: [B, C, E]
// E: [D]
```"""

QUESTIONS = [
    mcq(r"""
Why do graph traversals need a visited set while tree traversals usually don't?
""", ["Graphs can have cycles, so without it you could loop forever",
       "Graphs are always larger", "Trees store visited flags automatically",
       "Visited sets make traversal sorted"],
        "Graphs can have cycles, so without it you could loop forever"),

    mcq(r"""
Which data structure drives BFS?
""", ["A queue", "A stack", "A heap", "A hash map only"], "A queue"),

    mcq(r"""
Which data structure (or mechanism) drives DFS?
""", ["A stack or recursion", "A queue", "A heap", "A sorted list"], "A stack or recursion"),

    mcq(r"""
What is the time complexity of BFS and DFS with an adjacency list?
""", ["O(V + E)", "O(V²)", "O(E log V)", "O(V × E)"], "O(V + E)"),

    mcq(r"""
Starting BFS at A (neighbors visited in list order), what is the visit order?

""" + PIC, ["A B C D E", "A B D C E", "A C D B E", "A B D E C"], "A B C D E"),

    mcq(r"""
Starting recursive DFS at A (neighbors visited in list order), what is the visit order?

""" + PIC, ["A B D C E", "A B C D E", "A C D E B", "A B D E C"], "A B D C E"),

    mcq(r"""
What is the shortest path (fewest edges) from A to E?

""" + PIC, ["3 edges, e.g. A → B → D → E", "2 edges", "4 edges", "1 edge"],
        "3 edges, e.g. A → B → D → E"),

    mcq(r"""
Which traversal guarantees the shortest path in an UNWEIGHTED graph?
""", ["BFS", "DFS", "Both always", "Neither"], "BFS"),

    mcq(r"""
Why does BFS find shortest paths in unweighted graphs?
""", ["It discovers vertices in order of their distance from the start",
       "It sorts vertices by name", "It explores the deepest vertex first",
       "It uses edge weights"],
        "It discovers vertices in order of their distance from the start"),

    mcq(r"""
Does BFS find shortest paths in WEIGHTED graphs?
""", ["No, you need an algorithm like Dijkstra's", "Yes, always", "Only if weights are negative",
       "Only if the graph is directed"], "No, you need an algorithm like Dijkstra's"),

    mcq(r"""
In BFS, when should a vertex be marked as visited?
""", ["When it's added to the queue", "When it's removed from the queue",
       "After the whole search", "Never"], "When it's added to the queue"),

    mcq(r"""
What goes wrong if BFS marks vertices visited only when they're dequeued?
""", ["The same vertex can be enqueued many times, wasting time and memory",
       "BFS stops working entirely", "It becomes DFS", "Nothing"],
        "The same vertex can be enqueued many times, wasting time and memory"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

""" + G + r"""
void main() {
  final visited = {'A'};
  final q = Queue<String>()..add('A');
  final order = <String>[];
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    order.add(v);
    for (final w in g[v]!) {
      if (visited.add(w)) q.add(w);
    }
  }
  print(order.join());
}
```
""", ["ABCDE", "ABDCE", "ACBDE", "ABDEC"], "ABCDE"),

    mcq(r"""
What does this print?

```dart
""" + G + r"""
void dfs(String v, Set<String> seen, List<String> out) {
  seen.add(v);
  out.add(v);
  for (final w in g[v]!) {
    if (!seen.contains(w)) dfs(w, seen, out);
  }
}

void main() {
  final out = <String>[];
  dfs('A', {}, out);
  print(out.join());
}
```
""", ["ABDCE", "ABCDE", "ACDBE", "ABDEC"], "ABDCE"),

    mcq(r"""
How do you rebuild the actual shortest path after BFS?
""", ["Store each vertex's parent when it's discovered, then walk back from the target",
       "Sort the visited set", "Run DFS afterwards", "Store distances only"],
        "Store each vertex's parent when it's discovered, then walk back from the target"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

""" + G + r"""
void main() {
  final parent = <String, String?>{'A': null};
  final q = Queue<String>()..add('A');
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    for (final w in g[v]!) {
      if (!parent.containsKey(w)) {
        parent[w] = v;
        q.add(w);
      }
    }
  }
  final path = <String>[];
  for (String? at = 'E'; at != null; at = parent[at]) {
    path.add(at);
  }
  print(path.reversed.join(' → '));
}
```
""", ["A → B → D → E", "A → C → D → E", "E → D → B → A", "A → D → E"], "A → B → D → E"),

    mcq(r"""
In the path-rebuilding code, why is `path` reversed at the end?
""", ["Following parents goes from the target back to the start", "To sort the path",
       "Because BFS visits backwards", "It isn't necessary"],
        "Following parents goes from the target back to the start"),

    mcq(r"""
What does BFS return for a target that isn't reachable from the start?
""", ["It never reaches it; the queue empties (e.g. return null)", "The start vertex",
       "An infinite loop", "The closest vertex"],
        "It never reaches it; the queue empties (e.g. return null)"),

    mcq(r"""
In iterative DFS, why push neighbors in reverse order?
""", ["So the first neighbor is popped first, matching the recursive order",
       "To find shortest paths", "To avoid the visited set", "To sort the output"],
        "So the first neighbor is popped first, matching the recursive order"),

    mcq(r"""
In iterative DFS that marks vertices when popped, why check `if (!visited.add(v)) continue;`?
""", ["A vertex may have been pushed more than once; skip it if already processed",
       "To count edges", "To reverse the order", "It's required by Dart"],
        "A vertex may have been pushed more than once; skip it if already processed"),

    mcq(r"""
What is a connected component?
""", ["A maximal set of vertices that are all reachable from each other",
       "Any edge", "A vertex with no edges", "A path of length 2"],
        "A maximal set of vertices that are all reachable from each other"),

    mcq(r"""
How do you find all connected components?
""", ["Start a traversal from every unvisited vertex; each run finds one component",
       "Run one BFS from vertex 0", "Sort the edges", "Count the edges"],
        "Start a traversal from every unvisited vertex; each run finds one component"),

    mcq(r"""
What does this print?

```dart
int countComponents(int n, List<(int, int)> edges) {
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in edges) {
    adj[u].add(v);
    adj[v].add(u);
  }
  final seen = List.filled(n, false);
  var count = 0;
  for (var s = 0; s < n; s++) {
    if (seen[s]) continue;
    count++;
    final stack = [s];
    seen[s] = true;
    while (stack.isNotEmpty) {
      for (final w in adj[stack.removeLast()]) {
        if (!seen[w]) {
          seen[w] = true;
          stack.add(w);
        }
      }
    }
  }
  return count;
}

void main() {
  print(countComponents(6, [(0, 1), (2, 3), (3, 4)]));
}
```
""", ["3", "2", "4", "6"], "3"),

    mcq(r"""
Why is an outer loop over all vertices needed when counting components?
""", ["Disconnected parts (including isolated vertices) are never reached from a single start",
       "To sort the components", "To make it O(1)", "It isn't needed"],
        "Disconnected parts (including isolated vertices) are never reached from a single start"),

    mcq(r"""
What does this print?

```dart
int islands(List<String> grid) {
  final seen = <(int, int)>{};
  var count = 0;
  void sink(int r, int c) {
    if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length) return;
    if (grid[r][c] != '#' || !seen.add((r, c))) return;
    sink(r + 1, c);
    sink(r - 1, c);
    sink(r, c + 1);
    sink(r, c - 1);
  }

  for (var r = 0; r < grid.length; r++) {
    for (var c = 0; c < grid[0].length; c++) {
      if (grid[r][c] == '#' && !seen.contains((r, c))) {
        count++;
        sink(r, c);
      }
    }
  }
  return count;
}

void main() {
  print(islands(['#.#', '...', '#.#']));
  print(islands(['##', '##']));
}
```
""", ["4 then 1", "1 then 1", "4 then 4", "2 then 1"], "4 then 1"),

    mcq(r"""
What is the "flood fill" technique?
""", ["Starting from one cell and visiting every connected cell of the same kind",
       "Filling a list with zeros", "Sorting a grid", "Counting all cells"],
        "Starting from one cell and visiting every connected cell of the same kind"),

    mcq(r"""
In an undirected graph, how does DFS detect a cycle?
""", ["Finding a visited neighbor that isn't the vertex we came from (the parent)",
       "Finding any visited neighbor at all", "Finding a vertex with degree 1",
       "Counting edges"],
        "Finding a visited neighbor that isn't the vertex we came from (the parent)"),

    mcq(r"""
Why must undirected cycle detection ignore the parent?
""", ["The edge back to the parent is the same edge we just used, not a cycle",
       "Parents are never visited", "To speed things up", "It shouldn't ignore it"],
        "The edge back to the parent is the same edge we just used, not a cycle"),

    mcq(r"""
What does this print?

```dart
bool hasCycle(int n, List<(int, int)> edges) {
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in edges) {
    adj[u].add(v);
    adj[v].add(u);
  }
  final seen = List.filled(n, false);
  bool dfs(int v, int parent) {
    seen[v] = true;
    for (final w in adj[v]) {
      if (!seen[w]) {
        if (dfs(w, v)) return true;
      } else if (w != parent) {
        return true;
      }
    }
    return false;
  }

  for (var v = 0; v < n; v++) {
    if (!seen[v] && dfs(v, -1)) return true;
  }
  return false;
}

void main() {
  print(hasCycle(3, [(0, 1), (1, 2)]));
  print(hasCycle(3, [(0, 1), (1, 2), (2, 0)]));
}
```
""", ["false then true", "true then true", "false then false", "true then false"],
        "false then true"),

    mcq(r"""
In directed-graph cycle detection with three colors, what does GRAY mean?
""", ["The vertex is on the current DFS path (still being explored)", "Not visited yet",
       "Fully explored", "Part of a cycle for sure"],
        "The vertex is on the current DFS path (still being explored)"),

    mcq(r"""
In three-color DFS, which edge indicates a cycle?
""", ["An edge to a gray vertex (a back edge)", "An edge to a black vertex",
       "An edge to a white vertex", "Any edge"], "An edge to a gray vertex (a back edge)"),

    mcq(r"""
Why isn't reaching a BLACK vertex a cycle in a directed graph?
""", ["Black means fully explored on another path; two paths can share a destination without a loop",
       "Black vertices have no edges", "Black means unvisited", "It actually is a cycle"],
        "Black means fully explored on another path; two paths can share a destination without a loop"),

    mcq(r"""
What does this print?

```dart
enum S { white, gray, black }

bool cyclic(Map<String, List<String>> g) {
  final st = {for (final v in g.keys) v: S.white};
  bool dfs(String v) {
    st[v] = S.gray;
    for (final w in g[v]!) {
      if (st[w] == S.gray) return true;
      if (st[w] == S.white && dfs(w)) return true;
    }
    st[v] = S.black;
    return false;
  }

  return g.keys.any((v) => st[v] == S.white && dfs(v));
}

void main() {
  print(cyclic({'a': ['b', 'c'], 'b': ['c'], 'c': []}));
  print(cyclic({'a': ['b'], 'b': ['c'], 'c': ['a']}));
}
```
""", ["false then true", "true then true", "false then false", "true then false"],
        "false then true"),

    mcq(r"""
Why can't you use the undirected "ignore the parent" trick on directed graphs?
""", ["A → B and B → A is a real cycle, but the trick would ignore it",
       "Directed graphs have no parents", "It would be too slow", "It works fine"],
        "A → B and B → A is a real cycle, but the trick would ignore it"),

    mcq(r"""
What is a bipartite graph?
""", ["A graph whose vertices split into two groups with every edge going between groups",
       "A graph with exactly two vertices", "A graph with two components",
       "A graph where every vertex has degree 2"],
        "A graph whose vertices split into two groups with every edge going between groups"),

    mcq(r"""
Which structure makes a graph NOT bipartite?
""", ["An odd-length cycle", "An even-length cycle", "A tree", "Isolated vertices"],
        "An odd-length cycle"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

bool bipartite(List<List<int>> adj) {
  final color = List<int?>.filled(adj.length, null);
  for (var s = 0; s < adj.length; s++) {
    if (color[s] != null) continue;
    color[s] = 0;
    final q = Queue<int>()..add(s);
    while (q.isNotEmpty) {
      final v = q.removeFirst();
      for (final w in adj[v]) {
        if (color[w] == null) {
          color[w] = 1 - color[v]!;
          q.add(w);
        } else if (color[w] == color[v]) {
          return false;
        }
      }
    }
  }
  return true;
}

void main() {
  print(bipartite([[1], [0, 2], [1]]));
  print(bipartite([[1, 2], [0, 2], [0, 1]]));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What does `1 - color[v]!` compute in the bipartite check?
""", ["The opposite color (0 ↔ 1)", "The vertex's degree", "A random color",
       "The number of colors used"], "The opposite color (0 ↔ 1)"),

    mcq(r"""
Which problem is a better fit for DFS than BFS?
""", ["Detecting cycles in a directed graph", "Shortest path in an unweighted maze",
       "Finding everyone within 2 hops", "Level-by-level spreading"],
        "Detecting cycles in a directed graph"),

    mcq(r"""
Which problem is a better fit for BFS than DFS?
""", ["Fewest moves to reach a target in an unweighted grid", "Topological sorting",
       "Finding back edges", "Exploring all paths with backtracking"],
        "Fewest moves to reach a target in an unweighted grid"),

    mcq(r"""
What is the extra memory of BFS in the worst case?
""", ["O(V) for the queue and visited set", "O(1)", "O(E²)", "O(log V)"],
        "O(V) for the queue and visited set"),

    mcq(r"""
What risk does recursive DFS have on very large graphs?
""", ["Stack overflow from deep recursion", "Wrong answers on cycles",
       "It can't find components", "It uses O(V²) memory always"],
        "Stack overflow from deep recursion"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

""" + G + r"""
void main() {
  final dist = {'A': 0};
  final q = Queue<String>()..add('A');
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    for (final w in g[v]!) {
      if (!dist.containsKey(w)) {
        dist[w] = dist[v]! + 1;
        q.add(w);
      }
    }
  }
  print(dist);
}
```
""", ["{A: 0, B: 1, C: 1, D: 2, E: 3}", "{A: 0, B: 1, C: 2, D: 3, E: 4}",
       "{A: 0, B: 1, C: 1, D: 2, E: 2}", "{A: 0}"], "{A: 0, B: 1, C: 1, D: 2, E: 3}"),

    mcq(r"""
In BFS, what does `dist[w] = dist[v] + 1` compute?
""", ["The number of edges on the shortest path from the start to w", "w's degree",
       "The total number of vertices", "The weight of edge v–w"],
        "The number of edges on the shortest path from the start to w"),

    mcq(r"""
Which vertices does a single BFS from s visit?
""", ["Exactly those reachable from s", "Every vertex in the graph", "Only s's neighbors",
       "Only leaves"], "Exactly those reachable from s"),

    order(r"""
Complete the BFS loop:

```dart
while (queue.%order%) {
  final v = queue.%order%();
  for (final w in graph[v]!) {
    if (visited.%order%(w)) queue.add(w);
  }
}
```
""", ["isNotEmpty", "removeFirst", "add", "removeLast", "contains", "isEmpty"],
        ["isNotEmpty", "removeFirst", "add"]),

    mcq(r"""
In three-color DFS, what color is a vertex set to when its DFS call FINISHES?
""", ["Black", "Gray", "White", "It's removed from the map"], "Black"),

    mcq(r"""
What does this print?

```dart
List<int> withinK(Map<int, List<int>> g, int start, int k) {
  var frontier = [start];
  final seen = {start};
  for (var step = 0; step < k; step++) {
    final next = <int>[];
    for (final v in frontier) {
      for (final w in g[v]!) {
        if (seen.add(w)) next.add(w);
      }
    }
    frontier = next;
  }
  return seen.toList()..sort();
}

void main() {
  final g = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]};
  print(withinK(g, 1, 2));
}
```
""", ["[1, 2, 3]", "[1, 2]", "[1, 2, 3, 4]", "[2, 3]"], "[1, 2, 3]"),

    mcq(r"""
What does a BFS/DFS from one vertex on a DISCONNECTED graph miss?
""", ["Every vertex in other components", "Nothing", "Only isolated vertices with self-loops",
       "Every leaf"], "Every vertex in other components"),

    mcq(r"""
Which visited structure is fastest when vertices are numbered 0..n−1?
""", ["List<bool>", "Set<String>", "Map<String, bool>", "A sorted list"], "List<bool>"),

    mcq(r"""
In a social network, which traversal finds "friends of friends" (exactly 2 hops) naturally?
""", ["BFS, stopping after level 2", "DFS to maximum depth", "In-order traversal",
       "Binary search"], "BFS, stopping after level 2"),

    mcq(r"""
To clone a graph of node objects, what helps avoid copying a node twice (and infinite loops)?
""", ["A map from original node to its copy", "Sorting the nodes", "A queue only",
       "Recursion without a map"], "A map from original node to its copy"),

    mcq(r"""
What does this print?

```dart
void main() {
  final g = {'x': ['y'], 'y': ['x']};
  final seen = <String>{};
  void visit(String v) {
    if (!seen.add(v)) return;
    for (final w in g[v]!) {
      visit(w);
    }
  }

  visit('x');
  print(seen.length);
}
```
""", ["2", "1", "It loops forever", "0"], "2"),
]
