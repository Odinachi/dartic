# Representing Graphs

Imagine a **map of airline routes** ✈️. Cities are dots, and flights are lines between them.

- Lagos connects to London, Nairobi and Dubai.
- London connects to Lagos, New York and Dubai.
- There's no single "root" city, and you can fly in **loops**: Lagos → London → Dubai → Lagos.

Trees can't model this: in a tree, everything has one parent and there are no loops. We need something more general.

👉 That's a **graph**:

> A **graph** is a set of **vertices** (nodes) connected by **edges**. Edges can be **directed** (one-way) or **undirected** (two-way), and **weighted** (with a cost) or **unweighted**. Any node can connect to any other, and cycles are allowed.

Graphs model social networks, maps, the internet, dependency trees, recommendation systems and much more. Before running algorithms on them, we need to **store** them well.

---

## 📖 Graph Vocabulary

```text
   A ─── B
   │   ╱ │
   │  ╱  │
   C ─── D       E    (E has no edges)
```

| Term | Meaning | Example |
|------|---------|---------|
| **Vertex / node** | A thing | `A`, `B`, ... |
| **Edge** | A connection between two vertices | `A–B` |
| **Adjacent / neighbors** | Directly connected vertices | `A`'s neighbors: `B`, `C` |
| **Degree** | Number of edges touching a vertex | degree(`B`) = 3 |
| **Path** | A sequence of vertices joined by edges | `A → C → D` |
| **Cycle** | A path that returns to its start | `A → B → C → A` |
| **Connected** | A path exists between every pair | `A`–`D` are connected; `E` is not |
| **Component** | A maximal connected group | `{A, B, C, D}` and `{E}` |
| **V** and **E** | Number of vertices and edges | V = 5, E = 5 |

### Kinds of graphs

| Kind | Edge meaning | Example |
|------|--------------|---------|
| **Undirected** | `A – B` works both ways | Facebook friendships |
| **Directed** (digraph) | `A → B` is one-way | Twitter/X follows, web links |
| **Weighted** | Edges carry a number | Road distances, flight prices |
| **Unweighted** | All edges equal | "Who knows whom" |
| **DAG** | Directed and **acyclic** | Task dependencies, course prerequisites |
| **Dense** | E close to V² | A small group where everyone knows everyone |
| **Sparse** | E much smaller than V² | Road networks, social networks |

> 💡 A **tree** is just a special graph: connected, undirected, with no cycles and exactly V − 1 edges.

---

## 🧱 Representation 1: Edge List

The simplest option: a list of pairs.

```dart
void main() {
  // Undirected edges
  final edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')];

  print('Edges: ${edges.length}');

  // Neighbors of B: scan every edge (O(E))
  final neighborsOfB = [
    for (final (u, v) in edges)
      if (u == 'B') v else if (v == 'B') u,
  ];
  print('B → $neighborsOfB'); // [A, C, D]

  // Is there an edge between A and D? Scan again (O(E))
  final hasAD = edges.any((e) => (e.$1 == 'A' && e.$2 == 'D') || (e.$1 == 'D' && e.$2 == 'A'));
  print('A–D? $hasAD'); // false
}
```

**🔍 What This Code Does:**

1. **Records as Edges**: Each `(String, String)` record is one connection.
2. **Collection-for With Conditions**: Collects whichever end of an edge isn't `B`.
3. **Everything Is a Scan**: Finding neighbors or checking an edge costs **O(E)**.
4. **Good For**: Storing graphs in files, and algorithms that process edges in order (like Kruskal's MST, which sorts edges by weight).

---

## 🧱 Representation 2: Adjacency Matrix

A V × V grid where `matrix[i][j]` is 1 (or the weight) if there's an edge from `i` to `j`.

```dart
void main() {
  const names = ['A', 'B', 'C', 'D'];
  final index = {for (var i = 0; i < names.length; i++) names[i]: i};
  final n = names.length;
  final matrix = List.generate(n, (_) => List.filled(n, 0));

  void addEdge(String a, String b) {
    final i = index[a]!, j = index[b]!;
    matrix[i][j] = 1;
    matrix[j][i] = 1; // undirected: mirror it
  }

  addEdge('A', 'B');
  addEdge('A', 'C');
  addEdge('B', 'C');
  addEdge('B', 'D');
  addEdge('C', 'D');

  print('    ${names.join(' ')}');
  for (var i = 0; i < n; i++) {
    print('${names[i]}   ${matrix[i].join(' ')}');
  }

  print('A–D? ${matrix[index['A']!][index['D']!] == 1}'); // false, O(1)

  final neighborsOfB = [
    for (var j = 0; j < n; j++)
      if (matrix[index['B']!][j] == 1) names[j],
  ];
  print('B → $neighborsOfB'); // [A, C, D], O(V)
}
```

**🔍 What This Code Does:**

1. **Name → Index Map**: Matrices need integer indexes, so we map each vertex name to a row/column number.
2. **Mirror for Undirected Graphs**: Setting both `[i][j]` and `[j][i]` makes the matrix symmetric.
3. **O(1) Edge Check**: Just read one cell.
4. **O(V) Neighbors**: Scan a whole row, even if the vertex has only one neighbor.
5. **O(V²) Memory**: A graph of 100,000 vertices would need 10 **billion** cells. Matrices only make sense for **small or dense** graphs.

```text
    A B C D
A   0 1 1 0
B   1 0 1 1
C   1 1 0 1
D   0 1 1 0
```

---

## 🧱 Representation 3: Adjacency List (the default choice)

Each vertex keeps a list (or set) of its neighbors. In Dart, a `Map<T, List<T>>` or `Map<T, Set<T>>` is perfect.

```dart
class Graph<T> {
  final Map<T, Set<T>> _adj = {};
  final bool directed;

  Graph({this.directed = false});

  void addVertex(T v) => _adj.putIfAbsent(v, () => <T>{});

  void addEdge(T from, T to) {
    addVertex(from);
    addVertex(to);
    _adj[from]!.add(to);
    if (!directed) _adj[to]!.add(from);
  }

  void removeEdge(T from, T to) {
    _adj[from]?.remove(to);
    if (!directed) _adj[to]?.remove(from);
  }

  Iterable<T> neighbors(T v) => _adj[v] ?? const {};
  bool hasEdge(T from, T to) => _adj[from]?.contains(to) ?? false;
  int degree(T v) => _adj[v]?.length ?? 0;

  Iterable<T> get vertices => _adj.keys;
  int get vertexCount => _adj.length;
  int get edgeCount {
    final total = _adj.values.fold(0, (sum, s) => sum + s.length);
    return directed ? total : total ~/ 2;
  }

  @override
  String toString() =>
      _adj.entries.map((e) => '${e.key} → ${e.value.join(', ')}').join('\n');
}

void main() {
  final friends = Graph<String>();
  friends
    ..addEdge('Ada', 'Bob')
    ..addEdge('Ada', 'Cy')
    ..addEdge('Bob', 'Cy')
    ..addEdge('Bob', 'Dee')
    ..addVertex('Eve'); // no friends yet

  print(friends);
  print('Bob has ${friends.degree('Bob')} friends');   // 3
  print('Ada–Dee? ${friends.hasEdge('Ada', 'Dee')}');  // false
  print('V=${friends.vertexCount} E=${friends.edgeCount}'); // V=5 E=4

  final follows = Graph<String>(directed: true)
    ..addEdge('fan', 'star')
    ..addEdge('star', 'brand');
  print(follows.hasEdge('fan', 'star')); // true
  print(follows.hasEdge('star', 'fan')); // false (one-way)
}
```

**🔍 What This Code Does:**

This code demonstrates **a generic adjacency-list graph**:

1. **`Map<T, Set<T>>`**: Each vertex maps to the set of its neighbors. A `Set` prevents duplicate edges and gives O(1) `hasEdge`.

2. **Directed vs Undirected**: Undirected graphs add the edge in **both** directions.

3. **Isolated Vertices**: `addVertex('Eve')` stores a vertex with no edges.

4. **Edge Count**: In undirected graphs each edge appears twice, so divide by 2.

5. **Memory O(V + E)**: Only existing edges are stored, ideal for sparse graphs.

6. **Generic**: Works with `String`, `int`, records, or your own classes (with proper `==` and `hashCode`).

```text
Ada → Bob, Cy
Bob → Ada, Cy, Dee
Cy → Ada, Bob
Dee → Bob
Eve →
```

---

## ⚖️ Weighted Graphs

Store the weight alongside each neighbor: `Map<T, Map<T, num>>` maps `vertex → (neighbor → weight)`.

```dart
class WeightedGraph {
  final Map<String, Map<String, int>> _adj = {};

  void addEdge(String a, String b, int weight, {bool directed = false}) {
    _adj.putIfAbsent(a, () => {})[b] = weight;
    _adj.putIfAbsent(b, () => {});
    if (!directed) _adj[b]![a] = weight;
  }

  Map<String, int> neighbors(String v) => _adj[v] ?? const {};

  int? weight(String a, String b) => _adj[a]?[b];
}

void main() {
  final roads = WeightedGraph()
    ..addEdge('Lagos', 'Ibadan', 128)
    ..addEdge('Ibadan', 'Abuja', 535)
    ..addEdge('Lagos', 'Abuja', 760)
    ..addEdge('Abuja', 'Kano', 425);

  print(roads.neighbors('Abuja')); // {Ibadan: 535, Lagos: 760, Kano: 425}
  print(roads.weight('Lagos', 'Ibadan')); // 128
  print(roads.weight('Lagos', 'Kano'));   // null (no direct road)

  // Total length of a route
  final route = ['Lagos', 'Ibadan', 'Abuja', 'Kano'];
  var km = 0;
  for (var i = 0; i + 1 < route.length; i++) {
    km += roads.weight(route[i], route[i + 1])!;
  }
  print('Route length: $km km'); // 1088 km
}
```

**🔍 What This Code Does:**

1. **Nested Maps**: `_adj['Lagos']['Ibadan']` is the distance between them.
2. **`putIfAbsent(...)[b] = weight`**: Creates the inner map if needed and sets the weight in one line.
3. **Null-Aware Index**: `_adj[a]?[b]` returns `null` if either vertex or edge is missing.
4. **Route Cost**: Sum the weights of consecutive edges.

---

## 📊 Comparing Representations

| Operation | Edge list | Adjacency matrix | Adjacency list (sets) |
|-----------|-----------|------------------|-----------------------|
| Memory | O(E) | **O(V²)** | **O(V + E)** |
| Add edge | O(1) | O(1) | O(1) |
| Remove edge | O(E) | O(1) | O(1) average |
| Is there an edge u–v? | O(E) | **O(1)** | O(1) average |
| List neighbors of v | O(E) | O(V) | **O(degree(v))** |
| Visit all edges | O(E) | O(V²) | O(V + E) |
| Best for | Edge-sorting algorithms, files | Small or dense graphs | **Most real graphs (sparse)** |

> 💡 Real-world graphs are almost always **sparse**: you have hundreds of friends, not billions. That's why the **adjacency list** is the default.

---

## 🗺️ Grids Are Graphs Too

Game boards and mazes are graphs where each cell connects to its neighbors. You often don't store the graph at all; you **compute** neighbors on the fly.

```dart
Iterable<(int, int)> neighbors(List<String> grid, int r, int c) sync* {
  const directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]; // up, down, left, right
  for (final (dr, dc) in directions) {
    final nr = r + dr, nc = c + dc;
    if (nr < 0 || nc < 0 || nr >= grid.length || nc >= grid[0].length) continue;
    if (grid[nr][nc] == '#') continue; // wall
    yield (nr, nc);
  }
}

void main() {
  final maze = [
    '.#.',
    '...',
    '#..',
  ];
  print(neighbors(maze, 1, 1).toList()); // [(2, 1), (1, 0), (1, 2)]
  print(neighbors(maze, 0, 0).toList()); // [(1, 0)]
}
```

**🔍 What This Code Does:**

1. **Implicit Graph**: Vertices are `(row, col)` cells; edges connect open neighboring cells.
2. **Direction Records**: The four moves are stored as `(dr, dc)` pairs.
3. **Bounds and Walls**: Off-grid cells and `#` walls are skipped.
4. **Generator**: `sync*` with `yield` produces neighbors lazily.
5. **No Memory for Edges**: Perfect for huge grids where storing every edge would be wasteful.

---

## 🧮 Useful Graph Facts

```dart
void main() {
  // Handshake lemma: the sum of all degrees = 2 × E (undirected)
  final adj = {
    'A': {'B', 'C'},
    'B': {'A', 'C', 'D'},
    'C': {'A', 'B', 'D'},
    'D': {'B', 'C'},
  };
  final degreeSum = adj.values.fold(0, (s, n) => s + n.length);
  print('sum of degrees = $degreeSum, edges = ${degreeSum ~/ 2}'); // 10, 5

  // Maximum edges in a simple undirected graph with V vertices: V(V-1)/2
  for (final v in [4, 100, 1000000]) {
    print('V=$v → max edges ${v * (v - 1) ~/ 2}');
  }
}
```

**🔍 What This Code Does:**

1. **Handshake Lemma**: Every undirected edge adds 1 to the degree of **both** ends, so degrees sum to `2E`.
2. **Maximum Edges**: Each pair can be connected at most once: `V(V − 1)/2`.
3. **Why Sparse Matters**: A million users could have ~500 billion possible friendships, but real networks have only a tiny fraction.

---

## 🔁 Converting Between Representations

```dart
void main() {
  final edges = [(0, 1), (0, 2), (1, 2), (2, 3)];
  const n = 4;

  // Edge list → adjacency list
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in edges) {
    adj[u].add(v);
    adj[v].add(u);
  }
  print(adj); // [[1, 2], [0, 2], [0, 1, 3], [2]]

  // Adjacency list → adjacency matrix
  final matrix = List.generate(n, (_) => List.filled(n, 0));
  for (var u = 0; u < n; u++) {
    for (final v in adj[u]) {
      matrix[u][v] = 1;
    }
  }
  print(matrix[2]); // [1, 1, 0, 1]
}
```

**🔍 What This Code Does:**

1. **Integer Vertices**: When vertices are `0..n−1`, a `List<List<int>>` works as an adjacency list.
2. **Edge List → Adjacency List**: Add each edge to both endpoints' lists.
3. **Adjacency List → Matrix**: Mark each neighbor in the matrix row.

---

## ⚠️ Common Mistakes

### 1. Forgetting the reverse edge in undirected graphs

If `A – B` is added only as `A → B`, a search starting from `B` will never find `A`.

### 2. Using a matrix for a big sparse graph

O(V²) memory explodes quickly. Use adjacency lists.

### 3. Forgetting isolated vertices

If you only build the adjacency list from edges, vertices with no edges never appear. Add them explicitly.

### 4. Duplicate edges with lists

Using `List` for neighbors allows the same edge twice, which can double-count paths or degrees. Use a `Set` unless you want a **multigraph**.

---

## 🧪 Try It Yourself

1. Add `removeVertex(T v)` to `Graph<T>`, removing all edges that touch it.
2. Build a directed graph of **course prerequisites** and print each course's prerequisites (incoming edges).
3. Given an adjacency matrix, return the vertex with the highest degree.
4. Build the **transpose** of a directed graph (reverse every edge).

```dart
Map<String, Set<String>> transpose(Map<String, Set<String>> g) {
  final t = {for (final v in g.keys) v: <String>{}};
  g.forEach((from, tos) {
    for (final to in tos) {
      t.putIfAbsent(to, () => {}).add(from);
    }
  });
  return t;
}

void main() {
  final follows = {
    'fan': {'star'},
    'star': {'brand'},
    'brand': <String>{},
  };
  print(transpose(follows)); // {fan: {}, star: {fan}, brand: {star}}
}
```

**🔍 What This Code Does:**

1. **Reverse Every Edge**: `from → to` becomes `to → from`.
2. **Keep All Vertices**: The map starts with every vertex, so even ones with no incoming edges remain.
3. **Use Case**: "Who follows X?" becomes a neighbor lookup in the transposed graph.

---

## 📌 Key Takeaways

- ✅ A **graph** is vertices plus edges; edges can be **directed/undirected** and **weighted/unweighted**; cycles are allowed.
- ✅ A **tree** is a connected, acyclic graph with V − 1 edges.
- ✅ **Edge list**: simple, O(E) memory, slow neighbor lookups.
- ✅ **Adjacency matrix**: O(1) edge checks but **O(V²) memory**; good for small or dense graphs.
- ✅ **Adjacency list** (`Map<T, Set<T>>`): **O(V + E)** memory and fast neighbor iteration; the default for real graphs.
- ✅ Weighted graphs store weights per neighbor: `Map<T, Map<T, num>>`.
- ✅ **Grids** are implicit graphs: compute neighbors instead of storing edges.

**Next up:** 🔍 **Graph BFS & DFS**: exploring graphs, finding components and detecting cycles.
