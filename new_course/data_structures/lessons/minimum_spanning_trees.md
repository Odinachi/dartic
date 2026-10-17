# Minimum Spanning Trees

Imagine you're connecting **five villages** to the internet 🌐. You can lay fiber cable between certain pairs of villages, and each cable has a **cost** depending on distance and terrain.

- Every village must be connected, directly or through other villages.
- You don't need redundant loops; one route between any two villages is enough.
- You want to spend as **little** as possible. 💰

👉 That's the **minimum spanning tree** problem:

> A **spanning tree** of a connected, undirected, weighted graph connects **all V vertices** using exactly **V − 1 edges** and **no cycles**. A **minimum spanning tree (MST)** is a spanning tree with the **smallest possible total weight**.

Two classic **greedy** algorithms find it: **Kruskal's** (sort edges, add the cheapest that doesn't form a cycle) and **Prim's** (grow one tree, always adding the cheapest edge leaving it).

---

## 🌳 What Makes a Spanning Tree

```text
Graph (weights on edges):

    A ──4── B
    │ \     │
    1   3   2
    │     \ │
    C ──5── D ──7── E
```

A spanning tree must:

1. Include **every** vertex (A, B, C, D, E).
2. Use exactly **V − 1 = 4** edges.
3. Contain **no cycles**.

Possible spanning trees include `{A–C, A–B, B–D, D–E}` (cost 1 + 4 + 2 + 7 = 14) and `{A–C, A–D, B–D, D–E}` (cost 1 + 3 + 2 + 7 = **13**). The second one is the MST.

> 💡 MST ≠ shortest path! An MST minimizes the **total** cost of connecting everyone. The path between two specific vertices in an MST is **not** necessarily their shortest path.

---

## 🔑 The Cut Property (Why Greedy Works)

Split the vertices into any two groups (a **cut**). The **cheapest edge crossing the cut** is always safe to include in some MST.

Both Kruskal's and Prim's are just different ways of repeatedly applying this rule.

---

## 🧮 Kruskal's Algorithm

1. **Sort** all edges by weight, cheapest first.
2. Go through them in order. Add an edge **if it connects two different components** (doesn't create a cycle).
3. Stop when you have **V − 1** edges.

Checking "does this edge create a cycle?" is exactly what **Union-Find** does in nearly O(1).

```dart
class UnionFind {
  final List<int> _p, _rank;
  UnionFind(int n)
      : _p = List.generate(n, (i) => i),
        _rank = List.filled(n, 0);

  int find(int x) => _p[x] == x ? x : _p[x] = find(_p[x]);

  bool union(int a, int b) {
    var ra = find(a), rb = find(b);
    if (ra == rb) return false;
    if (_rank[ra] < _rank[rb]) {
      final t = ra;
      ra = rb;
      rb = t;
    }
    _p[rb] = ra;
    if (_rank[ra] == _rank[rb]) _rank[ra]++;
    return true;
  }
}

typedef Edge = ({int u, int v, int w});

({List<Edge> edges, int cost})? kruskal(int n, List<Edge> edges) {
  final sorted = [...edges]..sort((a, b) => a.w.compareTo(b.w));
  final uf = UnionFind(n);
  final mst = <Edge>[];
  var cost = 0;

  for (final e in sorted) {
    if (uf.union(e.u, e.v)) { // different components → safe to add
      mst.add(e);
      cost += e.w;
      if (mst.length == n - 1) break; // spanning tree complete
    }
  }
  return mst.length == n - 1 ? (edges: mst, cost: cost) : null; // null if disconnected
}

void main() {
  const names = ['A', 'B', 'C', 'D', 'E'];
  final edges = <Edge>[
    (u: 0, v: 1, w: 4), // A–B
    (u: 0, v: 2, w: 1), // A–C
    (u: 0, v: 3, w: 3), // A–D
    (u: 1, v: 3, w: 2), // B–D
    (u: 2, v: 3, w: 5), // C–D
    (u: 3, v: 4, w: 7), // D–E
  ];

  final result = kruskal(5, edges)!;
  for (final e in result.edges) {
    print('${names[e.u]}–${names[e.v]} (${e.w})');
  }
  print('Total cost: ${result.cost}'); // 13
}
```

**🔍 What This Code Does:**

This code demonstrates **Kruskal's algorithm with Union-Find**:

1. **Named Record Edges**: `typedef Edge = ({int u, int v, int w})` makes edges readable (`e.w` is the weight).

2. **Sort by Weight**: A copy of the edges is sorted cheapest first. O(E log E).

3. **Greedy Choice**: Each edge is added only if `union` succeeds, meaning its endpoints were in different components.

4. **Skip Cycles**: `C–D (5)` is rejected because C and D are already connected through A.

5. **Early Stop**: Once V − 1 edges are chosen, the tree is complete.

6. **Disconnected Graphs**: If fewer than V − 1 edges get added, no spanning tree exists (we return `null`).

**Trace:**

| Edge | Weight | Action |
|------|--------|--------|
| A–C | 1 | ✅ add |
| B–D | 2 | ✅ add |
| A–D | 3 | ✅ add (joins {A, C} with {B, D}) |
| A–B | 4 | ❌ skip (A and B already connected) |
| C–D | 5 | ❌ skip |
| D–E | 7 | ✅ add (4 edges, done) |

**Complexity:** **O(E log E)** for sorting; Union-Find operations are nearly O(1).

---

## 🌱 Prim's Algorithm

1. Start from any vertex; it's the beginning of the tree.
2. Repeatedly add the **cheapest edge** that connects the tree to a vertex **not yet** in the tree.
3. Stop when every vertex is in the tree.

A **priority queue** finds the cheapest crossing edge quickly. It's very similar to Dijkstra, but the priority is the **edge weight**, not the total distance.

```dart
import 'dart:collection';

typedef WeightedGraph = Map<String, Map<String, int>>;

({List<(String, String, int)> edges, int cost}) prim(WeightedGraph g, String start) {
  final inTree = <String>{start};
  final mst = <(String, String, int)>[];
  var cost = 0;

  // (weight, from, to), ordered by weight then names
  final pq = SplayTreeSet<(int, String, String)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    if (c != 0) return c;
    final d = a.$2.compareTo(b.$2);
    return d != 0 ? d : a.$3.compareTo(b.$3);
  });
  g[start]!.forEach((to, w) => pq.add((w, start, to)));

  while (pq.isNotEmpty && inTree.length < g.length) {
    final (w, from, to) = pq.first;
    pq.remove(pq.first);
    if (inTree.contains(to)) continue; // both ends already in the tree
    inTree.add(to);
    mst.add((from, to, w));
    cost += w;
    g[to]!.forEach((next, w2) {
      if (!inTree.contains(next)) pq.add((w2, to, next));
    });
  }
  return (edges: mst, cost: cost);
}

void main() {
  final WeightedGraph villages = {
    'A': {'B': 4, 'C': 1, 'D': 3},
    'B': {'A': 4, 'D': 2},
    'C': {'A': 1, 'D': 5},
    'D': {'A': 3, 'B': 2, 'C': 5, 'E': 7},
    'E': {'D': 7},
  };
  final result = prim(villages, 'A');
  for (final (from, to, w) in result.edges) {
    print('$from–$to ($w)');
  }
  print('Total cost: ${result.cost}'); // 13
}
```

**🔍 What This Code Does:**

1. **Tree Set**: `inTree` holds vertices already connected.
2. **Candidate Edges**: The priority queue holds edges from the tree to the outside, cheapest first.
3. **Lazy Skipping**: An edge whose target already joined the tree is ignored when popped.
4. **Grow the Frontier**: Each newly added vertex contributes its outgoing edges as new candidates.
5. **Same Total**: Prim's finds `A–C (1), A–D (3), D–B (2), D–E (7)`, also costing **13**.
6. **Complexity**: **O(E log V)** with a binary heap.

| | Kruskal's | Prim's |
|---|-----------|--------|
| Grows | A **forest** that merges | **One** tree outward |
| Key structure | Sorted edges + **Union-Find** | **Priority queue** |
| Input that fits | Edge list | Adjacency list |
| Best for | Sparse graphs, edges given as a list | Dense graphs, adjacency lists |
| Time | O(E log E) | O(E log V) |

**Trace from A:**

| Step | Tree so far | Cheapest edge leaving the tree | Added |
|------|-------------|--------------------------------|-------|
| 1 | {A} | A–C (1), A–D (3), A–B (4) | A–C (1) |
| 2 | {A, C} | A–D (3), A–B (4), C–D (5) | A–D (3) |
| 3 | {A, C, D} | D–B (2), A–B (4), D–E (7) | D–B (2) |
| 4 | {A, B, C, D} | D–E (7) | D–E (7) |

Notice step 3: once D joins, the edge D–B (2) becomes available and beats A–B (4).

---

## 🧩 Borůvka's Algorithm (Bonus)

A third classic approach, and the oldest (1926). In each **round**, **every** component picks its cheapest outgoing edge, and all of those edges are added at once. The number of components at least halves each round, so there are at most **log₂ V** rounds.

```dart
class UnionFind {
  final List<int> p;
  UnionFind(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    return true;
  }
}

int boruvka(int n, List<(int, int, int)> edges) {
  final uf = UnionFind(n);
  var components = n, cost = 0, rounds = 0;
  while (components > 1) {
    rounds++;
    // cheapest outgoing edge for each component root
    final cheapest = <int, (int, int, int)>{};
    for (final e in edges) {
      final (u, v, w) = e;
      final ru = uf.find(u), rv = uf.find(v);
      if (ru == rv) continue;
      for (final r in [ru, rv]) {
        final best = cheapest[r];
        if (best == null || w < best.$3) cheapest[r] = e;
      }
    }
    if (cheapest.isEmpty) break; // disconnected graph
    for (final (u, v, w) in cheapest.values) {
      if (uf.union(u, v)) {
        cost += w;
        components--;
      }
    }
  }
  print('rounds: $rounds');
  return cost;
}

void main() {
  final edges = [(0, 1, 4), (0, 2, 1), (0, 3, 3), (1, 3, 2), (2, 3, 5), (3, 4, 7)];
  print(boruvka(5, edges)); // 13
}
```

**🔍 What This Code Does:**

1. **Every Component Chooses at Once**: For each component, find its cheapest edge to a different component.
2. **Merge in Bulk**: All chosen edges are added in the same round (Union-Find skips any that became redundant).
3. **Few Rounds**: Components at least halve each round, so the loop runs O(log V) times, giving O(E log V) overall.
4. **Parallel-Friendly**: Each component's choice is independent, which makes Borůvka's popular for parallel and distributed systems.
5. **Same Answer**: Total cost 13, matching Kruskal's and Prim's.

---

## 🧠 Why the Greedy Choice Is Safe (Proof Sketch)

Suppose the cheapest edge `e` crossing some cut is **not** in an MST `T`.

1. Adding `e` to `T` creates a **cycle**.
2. That cycle must cross the cut at least **twice**, so it contains another crossing edge `f`.
3. `e` is the cheapest crossing edge, so `weight(e) ≤ weight(f)`.
4. Replace `f` with `e`: the result is still a spanning tree, and it costs **no more** than `T`.

So some MST contains `e`, and choosing it can never hurt. Kruskal's applies this to the cut between an edge's two components; Prim's applies it to the cut between the tree and everything else.

---

## 🧱 Example: Connecting Points With Minimum Wire

Given points on a plane, connect them all with straight wires of minimum total length. Every pair could be connected, so this is a **complete graph** with V(V − 1)/2 edges.

```dart
import 'dart:math';

double minWire(List<Point<double>> pts) {
  final n = pts.length;
  final inTree = List.filled(n, false);
  final best = List.filled(n, double.infinity); // cheapest edge to the tree
  best[0] = 0;
  var total = 0.0;

  for (var step = 0; step < n; step++) {
    // pick the closest point not yet in the tree (O(V) scan: great for dense graphs)
    var u = -1;
    for (var i = 0; i < n; i++) {
      if (!inTree[i] && (u == -1 || best[i] < best[u])) u = i;
    }
    inTree[u] = true;
    total += best[u];
    for (var v = 0; v < n; v++) {
      if (!inTree[v]) {
        final d = pts[u].distanceTo(pts[v]);
        if (d < best[v]) best[v] = d;
      }
    }
  }
  return total;
}

void main() {
  final pts = [
    const Point(0.0, 0.0),
    const Point(2.0, 0.0),
    const Point(2.0, 2.0),
    const Point(5.0, 2.0),
  ];
  print(minWire(pts).toStringAsFixed(2)); // 7.00 (2 + 2 + 3)
}
```

**🔍 What This Code Does:**

1. **Implicit Complete Graph**: Distances are computed on demand, never stored.
2. **Array-Based Prim's**: Without a heap, each step scans all points: **O(V²)**, which beats O(E log V) when E ≈ V².
3. **`best[v]`**: The cheapest known connection from `v` to the current tree.
4. **`dart:math` Points**: `distanceTo` computes Euclidean distance.

---

## 🌍 Where MSTs Show Up

| Application | Vertices | Edge weights |
|-------------|----------|--------------|
| Network cabling (fiber, power, water pipes) | Buildings / towns | Installation cost |
| Circuit design | Pins | Wire length |
| Clustering | Data points | Distance (remove the k − 1 heaviest MST edges to get k clusters) |
| Approximating the traveling salesman | Cities | Distance (an MST gives a tour at most 2× optimal) |
| Image segmentation | Pixels | Color difference |

### Clustering with an MST

```dart
class UnionFind {
  final List<int> p;
  UnionFind(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    return true;
  }
}

List<List<int>> clusters(int n, List<(int, int, int)> edges, int k) {
  final sorted = [...edges]..sort((a, b) => a.$3.compareTo(b.$3));
  final uf = UnionFind(n);
  var groups = n;
  for (final (u, v, _) in sorted) {
    if (groups == k) break; // stop merging once we have k clusters
    if (uf.union(u, v)) groups--;
  }
  final byRoot = <int, List<int>>{};
  for (var i = 0; i < n; i++) {
    byRoot.putIfAbsent(uf.find(i), () => []).add(i);
  }
  return byRoot.values.toList();
}

void main() {
  // Two tight groups {0,1,2} and {3,4} far apart
  final edges = [(0, 1, 1), (1, 2, 2), (0, 2, 2), (3, 4, 1), (2, 3, 20), (1, 4, 25)];
  print(clusters(5, edges, 2)); // [[0, 1, 2], [3, 4]]
}
```

**🔍 What This Code Does:**

1. **Kruskal's, Stopped Early**: Merge the closest points first, but stop when exactly `k` groups remain.
2. **Single-Linkage Clustering**: Equivalent to building the MST and cutting its `k − 1` most expensive edges.
3. **Result**: The far-apart groups stay separate because the expensive edges (20, 25) are never used.

---

## ⚠️ Common Mistakes

### 1. Confusing MST with shortest paths

The MST minimizes the **sum of all chosen edges**. It does **not** guarantee the shortest route between two particular vertices. Use Dijkstra for that.

### 2. Running MST on directed graphs

MSTs are defined for **undirected** graphs. The directed version (minimum spanning **arborescence**) needs a different algorithm.

### 3. Forgetting disconnected graphs

If the graph isn't connected, no spanning tree exists. Kruskal's ends with fewer than V − 1 edges; Prim's never reaches some vertices. You get a minimum spanning **forest** instead.

### 4. Not checking for cycles in Kruskal's

Adding the cheapest edges blindly creates cycles. Union-Find is what makes Kruskal's correct.

---

## 🧪 Try It Yourself

1. Modify `kruskal` to return the MST as an adjacency list.
2. **Minimum cost to connect all cities**: given `n` cities and possible connections with costs, return the minimum cost or −1 if impossible.
3. Verify that Kruskal's and Prim's give the **same total cost** on 10 random graphs. (The edges may differ when weights tie.)
4. Find the **maximum** spanning tree by sorting edges in descending order.

---

## 📌 Key Takeaways

- ✅ A **spanning tree** connects all V vertices with **V − 1 edges** and **no cycles**; the **MST** has minimum total weight.
- ✅ The **cut property** guarantees greedy choices are safe.
- ✅ **Kruskal's**: sort edges, add each one that joins two different components (via **Union-Find**): **O(E log E)**.
- ✅ **Prim's**: grow one tree, always adding the cheapest edge leaving it (via a **priority queue**): **O(E log V)**, or **O(V²)** with arrays for dense graphs.
- ✅ MSTs are for **undirected** graphs and are **not** shortest-path trees.
- ✅ Used for network design, clustering and approximation algorithms.

**Next up:** 🔍 **Module 6: Binary Search**: halving the search space, finding boundaries and searching on the answer.
