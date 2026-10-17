DIJ = r"""import 'dart:collection';

Map<String, int> dijkstra(Map<String, Map<String, int>> g, String s) {
  final dist = <String, int>{s: 0};
  final done = <String>{};
  final pq = SplayTreeSet<(int, String)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    return c != 0 ? c : a.$2.compareTo(b.$2);
  })
    ..add((0, s));
  while (pq.isNotEmpty) {
    final (d, u) = pq.first;
    pq.remove(pq.first);
    if (!done.add(u)) continue;
    for (final MapEntry(key: v, value: w) in g[u]!.entries) {
      if (d + w < (dist[v] ?? 1 << 62)) {
        dist[v] = d + w;
        pq.add((d + w, v));
      }
    }
  }
  return dist;
}
"""

QUESTIONS = [
    mcq(r"""
Which algorithm finds shortest paths in an UNWEIGHTED graph most efficiently?
""", ["BFS", "Dijkstra", "Bellman-Ford", "Floyd-Warshall"], "BFS"),

    mcq(r"""
Which algorithm is the standard choice for shortest paths with NON-NEGATIVE edge weights?
""", ["Dijkstra's algorithm", "BFS", "DFS", "Topological sort"], "Dijkstra's algorithm"),

    mcq(r"""
Which algorithm handles NEGATIVE edge weights (with no negative cycles)?
""", ["Bellman-Ford", "Dijkstra", "BFS", "Prim's algorithm"], "Bellman-Ford"),

    mcq(r"""
What is "relaxation" in shortest-path algorithms?
""", ["Updating dist[v] if dist[u] + weight(u, v) is smaller", "Removing an edge",
       "Resetting all distances to 0", "Sorting the edges"],
        "Updating dist[v] if dist[u] + weight(u, v) is smaller"),

    order(r"""
Complete the relaxation step:

```dart
if (dist[u]! %order% w %order% dist[v]!) {
  dist[v] = dist[u]! + w;
  prev[v] = %order%;
}
```
""", ["+", "<", "u", "-", ">", "v"], ["+", "<", "u"]),

    mcq(r"""
In Dijkstra's algorithm, which vertex is finalized next?
""", ["The unfinished vertex with the smallest known distance", "The vertex with the most edges",
       "A random unfinished vertex", "The most recently discovered vertex"],
        "The unfinished vertex with the smallest known distance"),

    mcq(r"""
Which data structure makes Dijkstra efficient?
""", ["A priority queue (min-heap)", "A FIFO queue", "A stack", "A linked list"],
        "A priority queue (min-heap)"),

    mcq(r"""
What is the time complexity of Dijkstra with a binary heap?
""", ["O((V + E) log V)", "O(V + E)", "O(V × E)", "O(V³)"], "O((V + E) log V)"),

    mcq(r"""
Why can Dijkstra give wrong answers with negative edge weights?
""", ["It finalizes a vertex assuming no later path can be cheaper, which a negative edge breaks",
       "It can't handle numbers below zero", "It loops forever", "It ignores weights"],
        "It finalizes a vertex assuming no later path can be cheaper, which a negative edge breaks"),

    mcq(r"""
What does this print?

```dart
""" + DIJ + r"""
void main() {
  final g = {
    'A': {'B': 4, 'C': 1},
    'B': {'D': 1},
    'C': {'B': 2, 'D': 5},
    'D': <String, int>{},
  };
  print(dijkstra(g, 'A'));
}
```
""", ["{A: 0, B: 3, C: 1, D: 4}", "{A: 0, B: 4, C: 1, D: 5}", "{A: 0, B: 3, C: 1, D: 6}",
       "{A: 0, C: 1, B: 3, D: 4}"], "{A: 0, B: 3, C: 1, D: 4}"),

    mcq(r"""
What does this print?

```dart
""" + DIJ + r"""
void main() {
  final g = {
    'S': {'A': 10, 'B': 1},
    'A': <String, int>{},
    'B': {'A': 1},
  };
  print(dijkstra(g, 'S')['A']);
}
```
""", ["2", "10", "11", "1"], "2"),

    mcq(r"""
What does Dijkstra report for a vertex that isn't reachable from the start (in the lesson's map version)?
""", ["It has no entry in the distance map", "Distance 0", "Distance -1", "It throws"],
        "It has no entry in the distance map"),

    mcq(r"""
Why does the Dijkstra priority queue comparator include the vertex name as a tie-breaker?
""", ["Without it, two vertices at the same distance would be treated as duplicates by the set",
       "To sort vertices alphabetically in the output", "For speed only", "It isn't necessary"],
        "Without it, two vertices at the same distance would be treated as duplicates by the set"),

    mcq(r"""
What is a "stale" priority queue entry in Dijkstra?
""", ["An older entry for a vertex that was later pushed again with a smaller distance",
       "An entry for the start vertex", "An entry with weight 0", "A deleted vertex"],
        "An older entry for a vertex that was later pushed again with a smaller distance"),

    mcq(r"""
How are stale entries usually handled?
""", ["Skip them when popped if the vertex is already finalized (lazy deletion)",
       "Search the queue and delete them", "Ignore the problem", "Restart the algorithm"],
        "Skip them when popped if the vertex is already finalized (lazy deletion)"),

    mcq(r"""
How do you rebuild the actual shortest path after Dijkstra?
""", ["Store prev[v] = u on each successful relaxation, then walk back from the target",
       "Sort vertices by distance", "Run BFS afterwards", "Store only distances"],
        "Store prev[v] = u on each successful relaxation, then walk back from the target"),

    mcq(r"""
What does this print?

```dart
void main() {
  final prev = {'B': 'C', 'C': 'A', 'D': 'B'};
  final path = ['D'];
  while (path.last != 'A') {
    path.add(prev[path.last]!);
  }
  print(path.reversed.join(' → '));
}
```
""", ["A → C → B → D", "D → B → C → A", "A → B → C → D", "A → D"], "A → C → B → D"),

    mcq(r"""
How many rounds of relaxing all edges does Bellman-Ford perform?
""", ["V − 1", "E", "log V", "1"], "V − 1"),

    mcq(r"""
Why are V − 1 rounds enough in Bellman-Ford?
""", ["A shortest path without cycles uses at most V − 1 edges", "Each round finalizes half the vertices",
       "Because the graph has V − 1 edges", "It's an arbitrary choice"],
        "A shortest path without cycles uses at most V − 1 edges"),

    mcq(r"""
How does Bellman-Ford detect a negative cycle?
""", ["If any edge can still be relaxed after V − 1 rounds", "If a distance becomes 0",
       "If the graph has more edges than vertices", "It can't"],
        "If any edge can still be relaxed after V − 1 rounds"),

    mcq(r"""
Why is "shortest path" undefined when a reachable negative cycle exists?
""", ["You could loop around it forever to make the cost arbitrarily small",
       "Negative numbers can't be added", "The graph becomes disconnected", "It's still defined"],
        "You could loop around it forever to make the cost arbitrarily small"),

    mcq(r"""
What is the time complexity of Bellman-Ford?
""", ["O(V × E)", "O((V + E) log V)", "O(V + E)", "O(V³)"], "O(V × E)"),

    mcq(r"""
What does this print?

```dart
void main() {
  const inf = 1 << 62;
  final dist = {'A': 0, 'B': inf, 'C': inf};
  final edges = [('A', 'B', 4), ('A', 'C', 1), ('C', 'B', -2)];
  for (var round = 0; round < 2; round++) {
    for (final (u, v, w) in edges) {
      if (dist[u]! != inf && dist[u]! + w < dist[v]!) dist[v] = dist[u]! + w;
    }
  }
  print(dist);
}
```
""", ["{A: 0, B: -1, C: 1}", "{A: 0, B: 4, C: 1}", "{A: 0, B: 2, C: 1}", "{A: 0, B: -2, C: 1}"],
        "{A: 0, B: -1, C: 1}"),

    mcq(r"""
Why does Bellman-Ford check `dist[u] != inf` before relaxing?
""", ["To avoid treating an unreachable vertex as a real starting point", "To detect cycles",
       "To speed up sorting", "It isn't necessary"],
        "To avoid treating an unreachable vertex as a real starting point"),

    mcq(r"""
What is Bellman-Ford's early-exit optimization?
""", ["Stop when a full round changes nothing", "Stop after the first round",
       "Stop when the target is reached", "Skip negative edges"],
        "Stop when a full round changes nothing"),

    mcq(r"""
Which input format suits Bellman-Ford best?
""", ["An edge list", "An adjacency matrix only", "A tree", "A priority queue"],
        "An edge list"),

    mcq(r"""
What can a negative cycle in a currency-exchange graph (using −log(rate) weights) reveal?
""", ["An arbitrage opportunity", "A broken exchange", "The cheapest currency",
       "Nothing useful"], "An arbitrage opportunity"),

    mcq(r"""
What is 0-1 BFS?
""", ["A shortest-path method for edges weighted 0 or 1 using a deque",
       "BFS that visits only vertices 0 and 1", "A binary search variant", "DFS with two colors"],
        "A shortest-path method for edges weighted 0 or 1 using a deque"),

    mcq(r"""
In 0-1 BFS, where do you push a neighbor reached by a weight-0 edge?
""", ["To the front of the deque", "To the back of the deque", "Nowhere", "Into a heap"],
        "To the front of the deque"),

    mcq(r"""
What is the time complexity of 0-1 BFS?
""", ["O(V + E)", "O((V + E) log V)", "O(V × E)", "O(V²)"], "O(V + E)"),

    mcq(r"""
What does Floyd-Warshall compute?
""", ["Shortest paths between every pair of vertices", "A minimum spanning tree",
       "A topological order", "Connected components only"],
        "Shortest paths between every pair of vertices"),

    mcq(r"""
What is the time complexity of Floyd-Warshall?
""", ["O(V³)", "O(V²)", "O(V + E)", "O(E log V)"], "O(V³)"),

    mcq(r"""
In Floyd-Warshall, which loop variable must be outermost?
""", ["k, the intermediate (stopover) vertex", "i, the source", "j, the destination",
       "Any order works"], "k, the intermediate (stopover) vertex"),

    mcq(r"""
What does this print?

```dart
void main() {
  const inf = 1 << 40;
  final d = [
    [0, 1, inf],
    [inf, 0, 2],
    [inf, inf, 0],
  ];
  for (var k = 0; k < 3; k++) {
    for (var i = 0; i < 3; i++) {
      for (var j = 0; j < 3; j++) {
        if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
      }
    }
  }
  print(d[0][2]);
}
```
""", ["3", "1", "2", "inf"], "3"),

    mcq(r"""
When is Floyd-Warshall a good choice?
""", ["Small graphs where you need distances between all pairs", "Huge sparse graphs",
       "Single-source shortest paths on a road network of millions", "Unweighted graphs only"],
        "Small graphs where you need distances between all pairs"),

    mcq(r"""
For a DAG with arbitrary (even negative) weights, what's the fastest single-source method?
""", ["Relax edges in topological order: O(V + E)", "Dijkstra", "Floyd-Warshall",
       "BFS"], "Relax edges in topological order: O(V + E)"),

    mcq(r"""
What does BFS minimize?
""", ["The number of edges in the path", "The total weight of the path",
       "The number of vertices in the graph", "The maximum edge weight"],
        "The number of edges in the path"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final g = {1: [2, 3], 2: [4], 3: [4], 4: <int>[]};
  final dist = {1: 0};
  final q = Queue<int>()..add(1);
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    for (final w in g[v]!) {
      if (!dist.containsKey(w)) {
        dist[w] = dist[v]! + 1;
        q.add(w);
      }
    }
  }
  print(dist[4]);
}
```
""", ["2", "3", "1", "4"], "2"),

    mcq(r"""
In Dijkstra, once a vertex is popped from the priority queue for the first time, its distance is:
""", ["Final (with non-negative weights)", "Still likely to change", "Always 0", "Unknown"],
        "Final (with non-negative weights)"),

    mcq(r"""
Why is it safe to finalize the closest unfinished vertex in Dijkstra?
""", ["Any other route must pass through a farther vertex, and non-negative weights can't make it shorter",
       "Because the graph is sorted", "Because BFS proved it", "It isn't safe"],
        "Any other route must pass through a farther vertex, and non-negative weights can't make it shorter"),

    mcq(r"""
Edges: A → B costs 4, A → C costs 1, C → B costs 2. Why does Dijkstra from A pick A → C → B (cost 3) over A → B (cost 4)?
""", ["Dijkstra finalizes C (distance 1) first and relaxes B to 1 + 2 = 3",
       "B is alphabetically after C", "Direct edges are ignored", "Random tie-breaking"],
        "Dijkstra finalizes C (distance 1) first and relaxes B to 1 + 2 = 3"),

    mcq(r"""
What does this print?

```dart
""" + DIJ + r"""
void main() {
  final g = {
    'a': {'b': 1},
    'b': {'c': 1},
    'c': {'a': 1},
    'd': <String, int>{},
  };
  final d = dijkstra(g, 'a');
  print('${d['c']} ${d.containsKey('d')}');
}
```
""", ["2 false", "3 false", "2 true", "1 false"], "2 false"),

    mcq(r"""
What problem can a very large "infinity" constant cause in shortest-path code?
""", ["Adding a weight to it can overflow or create a fake path", "It slows down sorting",
       "It makes graphs directed", "Nothing"],
        "Adding a weight to it can overflow or create a fake path"),

    mcq(r"""
In a weighted grid where entering a cell costs its value, what replaces edge weights?
""", ["The cost of the cell being entered", "The number of neighbors",
       "The distance from the start cell", "Always 1"],
        "The cost of the cell being entered"),

    mcq(r"""
In grid Dijkstra, why check `if (d > best[r][c]) continue;` after popping?
""", ["To skip stale entries that have since been improved", "To find the goal",
       "To avoid walls", "To sort the queue"],
        "To skip stale entries that have since been improved"),

    mcq(r"""
What does this print?

```dart
void main() {
  final (int d, String v) = (5, 'X');
  print('$v at $d');
}
```
""", ["X at 5", "5 at X", "(5, X)", "It doesn't compile"], "X at 5"),

    mcq(r"""
Which algorithm would a maps app use to route around traffic with travel-time weights?
""", ["Dijkstra (or A*, an extension of it)", "BFS", "DFS", "Bubble sort"],
        "Dijkstra (or A*, an extension of it)"),

    mcq(r"""
What does A* add on top of Dijkstra?
""", ["A heuristic estimate of remaining distance to guide the search toward the goal",
       "Support for negative cycles", "All-pairs distances", "Random exploration"],
        "A heuristic estimate of remaining distance to guide the search toward the goal"),

    mcq(r"""
For "cheapest flight with at most k stops", which algorithm adapts naturally?
""", ["Bellman-Ford limited to k + 1 rounds", "Plain Dijkstra", "Floyd-Warshall only",
       "DFS without a visited set"], "Bellman-Ford limited to k + 1 rounds"),

    mcq(r"""
What does this print?

```dart
void main() {
  const direct = 2;
  const viaC = 5 + -4;
  print(viaC < direct);
}
```
""", ["true", "false", "1", "-1"], "true"),

    fill(r"""
Return two named results from a function:

```dart
({int dist, bool found}) search() => (dist: 3, found: true);

void main() {
  final r = search();
  print(r.%fill%); // 3
}
```
""", "dist"),

    mcq(r"""
Which is the right algorithm for an unweighted social network "degrees of separation" question?
""", ["BFS", "Dijkstra with weights of 1 (works, but slower)", "Bellman-Ford", "Floyd-Warshall"],
        "BFS"),

    mcq(r"""
In network routing, what does "network delay time" from a source usually mean?
""", ["The largest shortest-path distance from the source to any node", "The sum of all edge weights",
       "The number of nodes", "The smallest edge weight"],
        "The largest shortest-path distance from the source to any node"),

    mcq(r"""
What does this print?

```dart
""" + DIJ + r"""
void main() {
  final g = {
    'k': {'a': 1, 'b': 4},
    'a': {'b': 2},
    'b': <String, int>{},
  };
  final d = dijkstra(g, 'k');
  print(d.values.reduce((x, y) => x > y ? x : y));
}
```
""", ["3", "4", "1", "7"], "3"),
]
