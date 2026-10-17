# Shortest Paths

Imagine you're using a maps app 🗺️ to drive across the country.

- If every road took **the same time**, the best route would just be the one with the **fewest roads**.
- But roads differ: a short highway might take 20 minutes while a long dirt road takes 2 hours. Now "fewest roads" isn't enough; you need the route with the **smallest total time**.

👉 That's the **shortest path problem**:

> Given a graph and a starting vertex, find the path with the **minimum total cost** to one or all other vertices. In **unweighted** graphs, **BFS** solves it. With **non-negative weights**, use **Dijkstra's algorithm**. With **negative weights**, use **Bellman-Ford**.

---

## 🧭 Which Algorithm?

| Graph | Algorithm | Time |
|-------|-----------|------|
| Unweighted (all edges cost 1) | **BFS** | O(V + E) |
| Weights only 0 or 1 | **0-1 BFS** (deque) | O(V + E) |
| Non-negative weights | **Dijkstra** (with a priority queue) | O((V + E) log V) |
| Negative weights allowed (no negative cycles) | **Bellman-Ford** | O(V × E) |
| DAG (any weights) | Relax edges in **topological order** | O(V + E) |
| All pairs, small graph | **Floyd-Warshall** | O(V³) |

---

## 🌊 Unweighted: BFS Distances

```dart
import 'dart:collection';

Map<String, int> bfsDistances(Map<String, List<String>> g, String start) {
  final dist = {start: 0};
  final q = Queue<String>()..add(start);
  while (q.isNotEmpty) {
    final v = q.removeFirst();
    for (final w in g[v]!) {
      if (!dist.containsKey(w)) {
        dist[w] = dist[v]! + 1;
        q.add(w);
      }
    }
  }
  return dist;
}

void main() {
  final subway = {
    'Central': ['Park', 'Market'],
    'Park': ['Central', 'Zoo'],
    'Market': ['Central', 'Harbor'],
    'Zoo': ['Park', 'Harbor'],
    'Harbor': ['Market', 'Zoo', 'Airport'],
    'Airport': ['Harbor'],
  };
  print(bfsDistances(subway, 'Central'));
  // {Central: 0, Park: 1, Market: 1, Zoo: 2, Harbor: 2, Airport: 3}
}
```

**🔍 What This Code Does:**

1. **Distance Map Doubles as Visited**: A vertex gets its distance the first time it's discovered.
2. **Level by Level**: BFS discovers vertices in order of their number of stops from `Central`.
3. **O(V + E)**: The fastest possible when every edge costs the same.

---

## 🚦 Dijkstra's Algorithm

**Idea:** Grow a set of vertices whose shortest distance is **final**. Always finalize the unfinished vertex with the **smallest known distance** next, then try to improve (**relax**) the distances of its neighbors.

**Relaxation** is the heart of every shortest-path algorithm:

```text
if dist[u] + weight(u, v) < dist[v]:
    dist[v] = dist[u] + weight(u, v)
    previous[v] = u
```

### Why it works

When the closest unfinished vertex `u` is picked, no other route can reach it more cheaply: any other route would have to pass through some vertex that's already **farther** away, and with **non-negative** weights, distances only grow along a path. So `u`'s distance is final.

### Dijkstra with a priority queue

```dart
import 'dart:collection';

typedef Graph = Map<String, Map<String, int>>;

({Map<String, int> dist, Map<String, String> prev}) dijkstra(Graph g, String start) {
  final dist = <String, int>{start: 0};
  final prev = <String, String>{};
  final done = <String>{};

  // Ordered by (distance, vertex) so the smallest distance comes first
  final pq = SplayTreeSet<(int, String)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    return c != 0 ? c : a.$2.compareTo(b.$2);
  })
    ..add((0, start));

  while (pq.isNotEmpty) {
    final (d, u) = pq.first;
    pq.remove(pq.first);
    if (!done.add(u)) continue; // already finalized via a shorter entry

    for (final MapEntry(key: v, value: w) in g[u]!.entries) {
      final candidate = d + w;
      if (candidate < (dist[v] ?? 1 << 62)) {
        dist[v] = candidate; // relax
        prev[v] = u;
        pq.add((candidate, v));
      }
    }
  }
  return (dist: dist, prev: prev);
}

List<String> pathTo(Map<String, String> prev, String start, String target) {
  final path = [target];
  while (path.last != start) {
    path.add(prev[path.last]!);
  }
  return path.reversed.toList();
}

void main() {
  final Graph roads = {
    'A': {'B': 4, 'C': 1},
    'B': {'A': 4, 'C': 2, 'D': 5},
    'C': {'A': 1, 'B': 2, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2},
    'E': {'C': 10, 'D': 2},
  };
  final result = dijkstra(roads, 'A');
  print(result.dist); // {A: 0, B: 3, C: 1, D: 8, E: 10}
  print(pathTo(result.prev, 'A', 'E')); // [A, C, B, D, E]
}
```

**🔍 What This Code Does:**

This code demonstrates **Dijkstra's algorithm with a priority queue**:

1. **Priority Queue of `(distance, vertex)`**: `SplayTreeSet` keeps entries ordered by distance; `first` is always the closest candidate. The vertex name is a tie-breaker so two vertices at the same distance aren't treated as duplicates.

2. **Finalize Once**: When a vertex is popped for the first time, its distance is final; later (stale) entries for it are skipped with `done`.

3. **Relaxation**: If going through `u` gives a shorter route to `v`, update `dist[v]`, remember `prev[v] = u`, and push the new candidate.

4. **"Infinity"**: `1 << 62` stands in for an unknown distance.

5. **Path Reconstruction**: Follow `prev` from the target back to the start, then reverse.

6. **Record Return Type**: `({Map dist, Map prev})` returns both results with named fields.

**Trace from A:**

| Step | Finalize | Updated distances |
|------|----------|-------------------|
| 1 | A (0) | C = 1, B = 4 |
| 2 | C (1) | B = 3 (via C), D = 9, E = 11 |
| 3 | B (3) | D = 8 (via B) |
| 4 | D (8) | E = 10 (via D) |
| 5 | E (10) | — |

> 💡 The direct edge `A → B` costs 4, but `A → C → B` costs only 3. Dijkstra finds it because C is finalized first and relaxes B.

### Complexity

- Each vertex is finalized once; each edge is relaxed once.
- Each push/pop on the priority queue is O(log V).
- Total: **O((V + E) log V)**.

---

## ⛔ Why Dijkstra Fails With Negative Weights

```dart
void main() {
  // A → B costs 2, A → C costs 5, C → B costs -4
  // True shortest A→B: A → C → B = 5 + (-4) = 1
  // Dijkstra finalizes B at distance 2 (the smallest at that moment)
  // and never revisits it, so it reports 2. Wrong!
  const direct = 2;
  const viaC = 5 + -4;
  print('direct: $direct, via C: $viaC'); // direct: 2, via C: 1
}
```

**🔍 What This Code Does:**

1. **Greedy Assumption Broken**: Dijkstra assumes a finalized vertex can't get cheaper later. A negative edge can make it cheaper.
2. **Wrong Answer**: B is finalized at 2, but the real shortest distance is 1.
3. **Use Bellman-Ford** whenever negative weights are possible.

---

## 🔁 Bellman-Ford: Handles Negative Weights

**Idea:** Relax **every** edge, **V − 1** times. A shortest path uses at most V − 1 edges, and each round extends correct distances by at least one more edge. A V-th round that still improves something means there's a **negative cycle**.

```dart
({Map<String, int> dist, bool negativeCycle}) bellmanFord(
    List<String> vertices, List<(String, String, int)> edges, String start) {
  const inf = 1 << 62;
  final dist = {for (final v in vertices) v: inf};
  dist[start] = 0;

  for (var round = 0; round < vertices.length - 1; round++) {
    var changed = false;
    for (final (u, v, w) in edges) {
      if (dist[u]! != inf && dist[u]! + w < dist[v]!) {
        dist[v] = dist[u]! + w;
        changed = true;
      }
    }
    if (!changed) break; // early exit: already optimal
  }

  // One more pass: any improvement now means a negative cycle
  final negativeCycle =
      edges.any((e) => dist[e.$1]! != inf && dist[e.$1]! + e.$3 < dist[e.$2]!);
  return (dist: dist, negativeCycle: negativeCycle);
}

void main() {
  final vertices = ['A', 'B', 'C', 'D'];
  final edges = [
    ('A', 'B', 2),
    ('A', 'C', 5),
    ('C', 'B', -4),
    ('B', 'D', 3),
  ];
  final r = bellmanFord(vertices, edges, 'A');
  print(r.dist);          // {A: 0, B: 1, C: 5, D: 4}
  print(r.negativeCycle); // false

  final cyclic = [...edges, ('D', 'C', -6)]; // C → B → D → C costs -7 total
  print(bellmanFord(vertices, cyclic, 'A').negativeCycle); // true
}
```

**🔍 What This Code Does:**

1. **Edge List Input**: Bellman-Ford simply loops over all edges, so an edge list is ideal.
2. **V − 1 Rounds**: Enough for any shortest path (it can't repeat vertices, so it has at most V − 1 edges).
3. **Unreachable Guard**: `dist[u] != inf` avoids treating "infinity + w" as a real distance.
4. **Early Exit**: If a round changes nothing, all distances are final.
5. **Negative Cycle Check**: If distances can still shrink, you could loop forever to make paths infinitely cheap, so "shortest path" is undefined.
6. **O(V × E)**: Slower than Dijkstra, but more general.

> 💡 Real use: currency exchange. Convert rates to `−log(rate)` weights; a negative cycle means an **arbitrage** opportunity.

---

## 🧱 Shortest Paths on a Weighted Grid

Many games use Dijkstra on grids where each cell has a movement cost (grass = 1, mud = 5, wall = impassable).

```dart
import 'dart:collection';

int cheapestPath(List<List<int>> cost) {
  final rows = cost.length, cols = cost[0].length;
  final best = List.generate(rows, (_) => List.filled(cols, 1 << 62));
  best[0][0] = cost[0][0];
  final pq = SplayTreeSet<(int, int, int)>((a, b) {
    for (final (x, y) in [(a.$1, b.$1), (a.$2, b.$2), (a.$3, b.$3)]) {
      if (x != y) return x.compareTo(y);
    }
    return 0;
  })
    ..add((cost[0][0], 0, 0));

  while (pq.isNotEmpty) {
    final (d, r, c) = pq.first;
    pq.remove(pq.first);
    if (r == rows - 1 && c == cols - 1) return d; // first time we pop the goal
    if (d > best[r][c]) continue; // stale entry
    for (final (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)]) {
      final nr = r + dr, nc = c + dc;
      if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
      final nd = d + cost[nr][nc];
      if (nd < best[nr][nc]) {
        best[nr][nc] = nd;
        pq.add((nd, nr, nc));
      }
    }
  }
  return -1;
}

void main() {
  final terrain = [
    [1, 3, 1, 1],
    [1, 5, 1, 9],
    [4, 2, 1, 1],
  ];
  print(cheapestPath(terrain)); // 8: right, right, down, down, right (1+3+1+1+1+1)
}
```

**🔍 What This Code Does:**

1. **Cells as Vertices**: Entering a cell costs that cell's value.
2. **Stale Entries**: `d > best[r][c]` skips outdated queue entries instead of deleting them ("lazy deletion").
3. **Stop at the Goal**: The first time the bottom-right cell is popped, its cost is final.
4. **Tuple Comparator**: Compares `(distance, row, col)` field by field.

---

## ⚡ 0-1 BFS: When Weights Are Only 0 or 1

If every edge costs 0 or 1, use a **deque**: push 0-cost neighbors to the **front** and 1-cost neighbors to the **back**. The deque stays sorted by distance without a heap.

```dart
import 'dart:collection';

Map<int, int> zeroOneBfs(Map<int, List<(int, int)>> g, int start) {
  final dist = {start: 0};
  final dq = ListQueue<int>()..add(start);
  while (dq.isNotEmpty) {
    final u = dq.removeFirst();
    for (final (v, w) in g[u]!) {
      final nd = dist[u]! + w;
      if (nd < (dist[v] ?? 1 << 62)) {
        dist[v] = nd;
        w == 0 ? dq.addFirst(v) : dq.addLast(v);
      }
    }
  }
  return dist;
}

void main() {
  // (neighbor, weight)
  final g = {
    0: [(1, 1), (2, 0)],
    1: [(3, 0)],
    2: [(1, 0), (3, 1)],
    3: <(int, int)>[],
  };
  print(zeroOneBfs(g, 0)); // {0: 0, 1: 0, 2: 0, 3: 0}
}
```

**🔍 What This Code Does:**

1. **Free Edges Go First**: A 0-weight edge doesn't increase the distance, so the neighbor goes to the front.
2. **Paid Edges Go Last**: A 1-weight edge joins the back, like normal BFS.
3. **O(V + E)**: No logarithmic heap operations.
4. **Result**: `0 → 2 → 1 → 3` uses only free edges, so every vertex has distance 0.

---

## 🌐 All Pairs: Floyd-Warshall

For **small** graphs where you need the distance between **every** pair, Floyd-Warshall tries every vertex `k` as a possible stopover.

```dart
void main() {
  const inf = 1 << 40;
  final d = [
    [0, 3, inf, 7],
    [8, 0, 2, inf],
    [5, inf, 0, 1],
    [2, inf, inf, 0],
  ];
  final n = d.length;
  for (var k = 0; k < n; k++) {
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < n; j++) {
        if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
      }
    }
  }
  for (final row in d) {
    print(row);
  }
  // [0, 3, 5, 6]
  // [5, 0, 2, 3]
  // [3, 6, 0, 1]
  // [2, 5, 7, 0]
}
```

**🔍 What This Code Does:**

1. **Distance Matrix**: `d[i][j]` starts as the direct edge weight (or "infinity").
2. **Stopover `k`**: If going `i → k → j` is cheaper than the best known `i → j`, update it.
3. **Order Matters**: `k` must be the **outer** loop, so each stopover is fully considered before the next.
4. **O(V³) Time, O(V²) Space**: Fine for hundreds of vertices, not millions.

---

## ⚠️ Common Mistakes

### 1. Using BFS on weighted graphs

BFS minimizes the **number of edges**, not the total weight.

### 2. Using Dijkstra with negative edges

It can finalize a vertex too early. Use Bellman-Ford (or check that all weights are ≥ 0).

### 3. Forgetting to skip stale queue entries

With lazy deletion, the same vertex can be in the queue several times. Skip it if it's already finalized or if the popped distance is larger than the best known.

### 4. Overflowing "infinity"

Adding a weight to a huge "infinity" constant can overflow or create a fake path. Guard with `dist[u] != inf` before relaxing.

---

## 🧪 Try It Yourself

1. Modify `dijkstra` to stop early once a specific target is finalized.
2. **Network delay**: given travel times between servers, how long until a signal from server `k` reaches all servers (the maximum shortest distance)?
3. **Cheapest flights within k stops**: run Bellman-Ford for exactly `k + 1` rounds, using a copy of the distances each round.
4. Use Floyd-Warshall to find the city with the fewest neighbors within a distance threshold.

---

## 📌 Key Takeaways

- ✅ **Relaxation** (`dist[u] + w < dist[v]`) is the core step of every shortest-path algorithm.
- ✅ **BFS** solves unweighted graphs in O(V + E); **0-1 BFS** handles 0/1 weights with a deque.
- ✅ **Dijkstra** finalizes the closest vertex first using a **priority queue**: **O((V + E) log V)**, non-negative weights only.
- ✅ **Bellman-Ford** relaxes all edges **V − 1** times, supports negative weights, and **detects negative cycles**: O(V × E).
- ✅ **Floyd-Warshall** computes all pairs in O(V³) for small graphs.
- ✅ Rebuild paths with a **previous-vertex map**.

**Next up:** 🤝 **Union-Find**: tracking which items belong to the same group, almost in O(1).
