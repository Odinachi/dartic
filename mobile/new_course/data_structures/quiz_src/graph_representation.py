QUESTIONS = [
    mcq(r"""
What is a graph?
""", ["A set of vertices connected by edges, where cycles are allowed",
       "A tree with exactly one root", "A sorted list of values", "A chart of numbers"],
        "A set of vertices connected by edges, where cycles are allowed"),

    mcq(r"""
What is a directed graph?
""", ["A graph whose edges are one-way (A → B doesn't imply B → A)",
       "A graph with weights", "A graph with no cycles", "A graph drawn left to right"],
        "A graph whose edges are one-way (A → B doesn't imply B → A)"),

    mcq(r"""
Which relationship is naturally UNDIRECTED?
""", ["A mutual friendship", "Following someone on social media", "A web page linking to another",
       "A task depending on another"], "A mutual friendship"),

    mcq(r"""
Which relationship is naturally DIRECTED?
""", ["Following an account on social media", "Two cities joined by a two-way road",
       "Two people shaking hands", "Two computers on the same cable"],
        "Following an account on social media"),

    mcq(r"""
What is a weighted graph?
""", ["A graph whose edges carry values like distance or cost", "A graph with many vertices",
       "A graph with heavy nodes", "A graph with directed edges"],
        "A graph whose edges carry values like distance or cost"),

    mcq(r"""
What is a DAG?
""", ["A directed acyclic graph", "A dense adjacency graph", "A doubly-linked array graph",
       "A disconnected graph"], "A directed acyclic graph"),

    mcq(r"""
Which is a classic example of a DAG?
""", ["Course prerequisites", "A road network with loops", "A friendship network",
       "A circular linked list"], "Course prerequisites"),

    mcq(r"""
What is the degree of a vertex in an undirected graph?
""", ["The number of edges touching it", "Its distance from vertex 0",
       "The number of vertices in the graph", "Its weight"],
        "The number of edges touching it"),

    mcq(r"""
What is a connected component?
""", ["A maximal group of vertices where each can reach every other", "A single edge",
       "A vertex with degree 0", "A cycle of length 3"],
        "A maximal group of vertices where each can reach every other"),

    mcq(r"""
Which statement about trees and graphs is true?
""", ["A tree is a connected, acyclic graph with V − 1 edges", "Every graph is a tree",
       "Trees can have cycles", "Graphs must have a root"],
        "A tree is a connected, acyclic graph with V − 1 edges"),

    mcq(r"""
What is the memory usage of an adjacency matrix?
""", ["O(V²)", "O(V + E)", "O(E)", "O(V)"], "O(V²)"),

    mcq(r"""
What is the memory usage of an adjacency list?
""", ["O(V + E)", "O(V²)", "O(E²)", "O(1)"], "O(V + E)"),

    mcq(r"""
What is the cost of checking whether edge u–v exists in an adjacency matrix?
""", ["O(1)", "O(V)", "O(E)", "O(log V)"], "O(1)"),

    mcq(r"""
What is the cost of listing all neighbors of v in an adjacency matrix?
""", ["O(V)", "O(1)", "O(degree(v))", "O(E)"], "O(V)"),

    mcq(r"""
What is the cost of listing all neighbors of v in an adjacency list?
""", ["O(degree(v))", "O(V)", "O(V²)", "O(E)"], "O(degree(v))"),

    mcq(r"""
What is the cost of finding v's neighbors in a plain edge list?
""", ["O(E)", "O(1)", "O(degree(v))", "O(log E)"], "O(E)"),

    mcq(r"""
Which representation is the usual default for real-world graphs?
""", ["Adjacency list", "Adjacency matrix", "Edge list", "A single string"],
        "Adjacency list"),

    mcq(r"""
Why are adjacency lists preferred for most real graphs?
""", ["Real graphs are sparse, so storing only existing edges saves huge amounts of memory",
       "They give O(1) edge checks always", "They're the only option in Dart",
       "They sort the vertices"],
        "Real graphs are sparse, so storing only existing edges saves huge amounts of memory"),

    mcq(r"""
When is an adjacency matrix a good choice?
""", ["For small or dense graphs where O(1) edge checks matter", "For a social network of millions",
       "For sparse road networks", "Never"],
        "For small or dense graphs where O(1) edge checks matter"),

    mcq(r"""
Which algorithm naturally works on an edge list sorted by weight?
""", ["Kruskal's minimum spanning tree", "Binary search", "Level-order traversal",
       "Heap sort"], "Kruskal's minimum spanning tree"),

    mcq(r"""
What does this print?

```dart
void main() {
  final edges = [('A', 'B'), ('A', 'C'), ('B', 'C')];
  final adj = <String, Set<String>>{};
  for (final (u, v) in edges) {
    adj.putIfAbsent(u, () => {}).add(v);
    adj.putIfAbsent(v, () => {}).add(u);
  }
  print(adj['C']);
}
```
""", ["{A, B}", "{}", "{C}", "null"], "{A, B}"),

    mcq(r"""
What does this print?

```dart
void main() {
  final adj = <String, Set<String>>{};
  void addDirected(String a, String b) {
    adj.putIfAbsent(a, () => {}).add(b);
    adj.putIfAbsent(b, () => {});
  }

  addDirected('fan', 'star');
  print(adj['star']!.contains('fan'));
  print(adj['fan']!.contains('star'));
}
```
""", ["false then true", "true then true", "true then false", "false then false"],
        "false then true"),

    mcq(r"""
In an undirected adjacency list, what must `addEdge(a, b)` do?
""", ["Add b to a's neighbors AND a to b's neighbors", "Add b to a's neighbors only",
       "Add a to b's neighbors only", "Add both to a global list"],
        "Add b to a's neighbors AND a to b's neighbors"),

    mcq(r"""
Why use `Set<T>` instead of `List<T>` for neighbors?
""", ["It prevents duplicate edges and gives O(1) average edge checks",
       "Sets keep neighbors sorted", "Lists can't store strings", "Sets use less memory always"],
        "It prevents duplicate edges and gives O(1) average edge checks"),

    mcq(r"""
What does this print?

```dart
void main() {
  final matrix = List.generate(3, (_) => List.filled(3, 0));
  void add(int i, int j) {
    matrix[i][j] = 1;
    matrix[j][i] = 1;
  }

  add(0, 1);
  add(1, 2);
  print(matrix[1]);
}
```
""", ["[1, 0, 1]", "[0, 1, 0]", "[1, 1, 1]", "[0, 0, 1]"], "[1, 0, 1]"),

    mcq(r"""
What property does the adjacency matrix of an undirected graph have?
""", ["It is symmetric: matrix[i][j] == matrix[j][i]", "Its diagonal is all 1s",
       "Each row sums to 1", "It's always full of 1s"],
        "It is symmetric: matrix[i][j] == matrix[j][i]"),

    mcq(r"""
In an undirected graph, how is the edge count computed from adjacency sets?
""", ["Sum of all set sizes divided by 2", "Sum of all set sizes", "Number of vertices",
       "Number of vertices minus 1"], "Sum of all set sizes divided by 2"),

    mcq(r"""
What does the handshake lemma say?
""", ["In an undirected graph, the degrees sum to 2 × E", "Every vertex has even degree",
       "E always equals V − 1", "Every graph has a cycle"],
        "In an undirected graph, the degrees sum to 2 × E"),

    mcq(r"""
An undirected graph has degrees 3, 2, 2, 1. How many edges does it have?
""", ["4", "8", "3", "2"], "4"),

    mcq(r"""
What is the maximum number of edges in a simple undirected graph with 5 vertices?
""", ["10", "25", "20", "5"], "10"),

    mcq(r"""
What does this print?

```dart
void main() {
  final adj = {
    'A': {'B', 'C'},
    'B': {'A'},
    'C': {'A'},
  };
  final sum = adj.values.fold(0, (s, n) => s + n.length);
  print('$sum ${sum ~/ 2}');
}
```
""", ["4 2", "3 1", "2 1", "4 4"], "4 2"),

    mcq(r"""
How are weights typically stored in an adjacency-list weighted graph in Dart?
""", ["Map<T, Map<T, num>>: vertex → (neighbor → weight)", "Map<T, Set<T>>",
       "List<T>", "A separate List<num> of all weights"],
        "Map<T, Map<T, num>>: vertex → (neighbor → weight)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final roads = <String, Map<String, int>>{};
  void add(String a, String b, int w) {
    roads.putIfAbsent(a, () => {})[b] = w;
    roads.putIfAbsent(b, () => {})[a] = w;
  }

  add('X', 'Y', 5);
  add('Y', 'Z', 3);
  print(roads['Y']);
  print(roads['X']?['Z']);
}
```
""", ["{X: 5, Z: 3} then null", "{Z: 3} then 8", "{X: 5} then 3", "{X: 5, Z: 3} then 8"],
        "{X: 5, Z: 3} then null"),

    fill(r"""
Read a weight safely when either vertex might be missing:

```dart
void main() {
  final g = <String, Map<String, int>>{'A': {'B': 4}};
  print(g['C']%fill%['A']); // null
}
```
""", "?"),

    mcq(r"""
What does this print?

```dart
void main() {
  final w = {
    ('A', 'B'): 2,
    ('B', 'C'): 5,
    ('C', 'D'): 1,
  };
  final route = ['A', 'B', 'C', 'D'];
  var total = 0;
  for (var i = 0; i + 1 < route.length; i++) {
    total += w[(route[i], route[i + 1])]!;
  }
  print(total);
}
```
""", ["8", "7", "3", "6"], "8"),

    mcq(r"""
Why can a grid (like a maze) be treated as an implicit graph?
""", ["Each open cell is a vertex and neighboring open cells are connected by edges",
       "Grids are always trees", "Grids have no edges", "Because grids are sorted"],
        "Each open cell is a vertex and neighboring open cells are connected by edges"),

    mcq(r"""
What is the advantage of computing grid neighbors on the fly?
""", ["No memory is spent storing edges", "It's always O(1) to find a path",
       "It avoids walls automatically", "It sorts the cells"],
        "No memory is spent storing edges"),

    mcq(r"""
What does this print?

```dart
Iterable<(int, int)> nbrs(List<String> g, int r, int c) sync* {
  for (final (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]) {
    final nr = r + dr, nc = c + dc;
    if (nr < 0 || nc < 0 || nr >= g.length || nc >= g[0].length) continue;
    if (g[nr][nc] == '#') continue;
    yield (nr, nc);
  }
}

void main() {
  print(nbrs(['..', '#.'], 0, 0).toList());
}
```
""", ["[(0, 1)]", "[(1, 0), (0, 1)]", "[(0, 1), (1, 1)]", "[]"], "[(0, 1)]"),

    mcq(r"""
How many neighbors can a grid cell have with 4-directional movement?
""", ["At most 4", "Exactly 8", "At most 2", "Any number"], "At most 4"),

    mcq(r"""
What is the transpose of a directed graph?
""", ["The same graph with every edge reversed", "The adjacency matrix rotated 90°",
       "The graph with weights doubled", "The graph without cycles"],
        "The same graph with every edge reversed"),

    mcq(r"""
What does this print?

```dart
void main() {
  final g = {'a': {'b'}, 'b': {'c'}, 'c': <String>{}};
  final t = {for (final v in g.keys) v: <String>{}};
  g.forEach((from, tos) {
    for (final to in tos) {
      t[to]!.add(from);
    }
  });
  print(t);
}
```
""", ["{a: {}, b: {a}, c: {b}}", "{a: {b}, b: {c}, c: {}}", "{c: {b}, b: {a}}",
       "{a: {c}, b: {}, c: {a}}"], "{a: {}, b: {a}, c: {b}}"),

    mcq(r"""
In a transposed "follows" graph, what does a vertex's neighbor set represent?
""", ["Who follows that vertex", "Who that vertex follows", "Mutual follows only",
       "Accounts with no followers"], "Who follows that vertex"),

    mcq(r"""
What problem occurs if an undirected edge is only stored one way?
""", ["A search from the other endpoint can't find the first one", "Edges are counted twice",
       "The graph becomes weighted", "Nothing"],
        "A search from the other endpoint can't find the first one"),

    mcq(r"""
Why add isolated vertices explicitly in an adjacency list?
""", ["Otherwise vertices with no edges won't appear in the graph at all",
       "To make the graph connected", "To add weights", "It isn't necessary"],
        "Otherwise vertices with no edges won't appear in the graph at all"),

    mcq(r"""
What is a multigraph?
""", ["A graph that allows multiple edges between the same pair of vertices",
       "A graph with multiple components", "A graph with weights", "A directed graph"],
        "A graph that allows multiple edges between the same pair of vertices"),

    mcq(r"""
What does this print?

```dart
void main() {
  const n = 3;
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in [(0, 1), (1, 2)]) {
    adj[u].add(v);
    adj[v].add(u);
  }
  print(adj);
}
```
""", ["[[1], [0, 2], [1]]", "[[1], [2], []]", "[[0, 1], [1, 2]]", "[[1, 2], [0], [0]]"],
        "[[1], [0, 2], [1]]"),

    mcq(r"""
When vertices are numbered 0..n−1, what's a compact adjacency list in Dart?
""", ["List<List<int>>", "Map<String, String>", "Set<int>", "String"], "List<List<int>>"),

    mcq(r"""
A social network has 1,000,000 users with about 200 friends each. Roughly how many cells would an adjacency matrix need?
""", ["10¹² (a trillion)", "200 million", "1 million", "200"], "10¹² (a trillion)"),

    mcq(r"""
A social network has 1,000,000 users with about 200 friends each. Roughly how many entries does an adjacency list store?
""", ["About 200 million (1,000,000 × 200)", "10¹²", "1,000", "1 million"],
        "About 200 million (1,000,000 × 200)"),

    mcq(r"""
What does `matrix[i][j] = w` (instead of 1) represent?
""", ["A weighted edge from i to j with weight w", "w copies of the edge",
       "Vertex i has degree w", "An error"], "A weighted edge from i to j with weight w"),

    order(r"""
Complete an undirected addEdge for `Map<T, Set<T>> adj`:

```dart
void addEdge(T a, T b) {
  adj.%order%(a, () => <T>{}).add(b);
  adj.putIfAbsent(b, () => <T>{}).%order%(%order%);
}
```
""", ["putIfAbsent", "add", "a", "remove", "b", "update"], ["putIfAbsent", "add", "a"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final adj = {
    1: {2, 3},
    2: {1},
    3: {1},
    4: <int>{},
  };
  final isolated = adj.entries.where((e) => e.value.isEmpty).map((e) => e.key);
  print(isolated.toList());
}
```
""", ["[4]", "[2, 3]", "[1]", "[]"], "[4]"),

    mcq(r"""
Which structure answers "is there an edge between u and v?" in O(1) average with O(V + E) memory?
""", ["Adjacency list using sets", "Edge list", "Adjacency list using plain lists",
       "Sorted edge list"], "Adjacency list using sets"),

    mcq(r"""
What does this print?

```dart
void main() {
  final names = ['A', 'B', 'C'];
  final index = {for (var i = 0; i < names.length; i++) names[i]: i};
  print(index['C']);
}
```
""", ["2", "3", "C", "null"], "2"),

    mcq(r"""
Why do adjacency matrices often need a name → index map?
""", ["Matrices are indexed by integers, but vertices may be strings or objects",
       "To sort the vertices", "To store weights", "Dart requires it"],
        "Matrices are indexed by integers, but vertices may be strings or objects"),

    mcq(r"""
What is a path?
""", ["A sequence of vertices where each consecutive pair is joined by an edge",
       "Any set of vertices", "A single vertex", "A list of weights"],
        "A sequence of vertices where each consecutive pair is joined by an edge"),

    mcq(r"""
What is a cycle?
""", ["A path that starts and ends at the same vertex", "A vertex with degree 2",
       "A path through every vertex", "An edge with weight 0"],
        "A path that starts and ends at the same vertex"),
]
