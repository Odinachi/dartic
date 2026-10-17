# Graph BFS & DFS

Imagine you've just moved to a new city 🏙️ and want to explore every street.

- 🌊 **Strategy 1 (BFS):** Visit every place **one block** from home, then everything **two blocks** away, then three... like ripples spreading out.
- 🧗 **Strategy 2 (DFS):** Pick a street and keep going as **far** as you can. When you hit a dead end, **backtrack** to the last intersection with an unexplored street, and continue.

Either way, you carry a **notebook** of places you've already been, so you don't walk in circles. 📒

👉 These are the two fundamental graph traversals:

> **Breadth-first search (BFS)** explores a graph level by level using a **queue**; in an unweighted graph it finds **shortest paths**.
> **Depth-first search (DFS)** explores as deep as possible before backtracking, using a **stack** or **recursion**; it's ideal for **connectivity**, **cycles** and **ordering** problems.
> Both need a **visited set**, because graphs (unlike trees) can contain **cycles**.

---

## 🗺️ Our Example Graph

```dart
final cityMap = {
  'Home': ['Cafe', 'Park'],
  'Cafe': ['Home', 'Library', 'Gym'],
  'Park': ['Home', 'Gym'],
  'Library': ['Cafe', 'Museum'],
  'Gym': ['Cafe', 'Park', 'Museum'],
  'Museum': ['Library', 'Gym'],
  'Island': <String>[], // unreachable from Home
};
```

```text
        Home
       /    \
    Cafe ── Park       (Cafe–Gym and Park–Gym)
    /  \     /
Library  Gym
    \    /
    Museum                    Island (alone)
```

---

## 🌊 Breadth-First Search

```dart
import 'dart:collection';

final cityMap = {
  'Home': ['Cafe', 'Park'],
  'Cafe': ['Home', 'Library', 'Gym'],
  'Park': ['Home', 'Gym'],
  'Library': ['Cafe', 'Museum'],
  'Gym': ['Cafe', 'Park', 'Museum'],
  'Museum': ['Library', 'Gym'],
  'Island': <String>[],
};

List<String> bfs(Map<String, List<String>> graph, String start) {
  final visited = <String>{start};
  final queue = Queue<String>()..add(start);
  final order = <String>[];

  while (queue.isNotEmpty) {
    final place = queue.removeFirst();
    order.add(place);
    for (final next in graph[place]!) {
      if (visited.add(next)) { // true only the first time
        queue.add(next);
      }
    }
  }
  return order;
}

void main() {
  print(bfs(cityMap, 'Home'));
  // [Home, Cafe, Park, Library, Gym, Museum]
}
```

**🔍 What This Code Does:**

This code demonstrates **breadth-first search on a graph**:

1. **Visited Set**: `visited.add(next)` returns `true` only if `next` wasn't already seen, so each place is enqueued exactly once.

2. **Mark When Enqueuing**: Marking on enqueue (not on dequeue) prevents the same place from entering the queue several times.

3. **FIFO Order**: Places one step away (`Cafe`, `Park`) are processed before places two steps away (`Library`, `Gym`).

4. **Unreachable Vertices**: `Island` never appears; BFS only visits what's reachable from the start.

5. **O(V + E)**: Every reachable vertex is dequeued once and every edge is examined once (twice in undirected graphs).

### Shortest path in an unweighted graph

Because BFS discovers vertices in order of distance, the **first** time it reaches a vertex is via a shortest path. Record **how** you got there to rebuild the path.

```dart
import 'dart:collection';

final cityMap = {
  'Home': ['Cafe', 'Park'],
  'Cafe': ['Home', 'Library', 'Gym'],
  'Park': ['Home', 'Gym'],
  'Library': ['Cafe', 'Museum'],
  'Gym': ['Cafe', 'Park', 'Museum'],
  'Museum': ['Library', 'Gym'],
  'Island': <String>[],
};

List<String>? shortestPath(Map<String, List<String>> g, String from, String to) {
  final parent = <String, String?>{from: null};
  final queue = Queue<String>()..add(from);

  while (queue.isNotEmpty) {
    final v = queue.removeFirst();
    if (v == to) {
      // walk back through the parents
      final path = <String>[];
      for (String? at = to; at != null; at = parent[at]) {
        path.add(at);
      }
      return path.reversed.toList();
    }
    for (final next in g[v]!) {
      if (!parent.containsKey(next)) {
        parent[next] = v;
        queue.add(next);
      }
    }
  }
  return null; // unreachable
}

void main() {
  print(shortestPath(cityMap, 'Home', 'Museum')); // [Home, Cafe, Library, Museum]
  print(shortestPath(cityMap, 'Park', 'Library')); // [Park, Home, Cafe, Library]
  print(shortestPath(cityMap, 'Home', 'Island'));  // null
}
```

**🔍 What This Code Does:**

1. **Parent Map Doubles as Visited**: If a vertex has a parent entry, it's been discovered.
2. **Rebuild the Path**: Follow `parent` links from the target back to the start, then reverse.
3. **Shortest by Edge Count**: BFS guarantees the fewest edges (here: 3 hops to `Museum`).
4. **Ties**: If several shortest paths exist, BFS returns the one found first, which depends on neighbor order.
5. **`null` for Unreachable**: The queue empties without ever reaching the target.

> ⚠️ BFS only finds shortest paths when every edge has the **same cost**. For weighted graphs you need **Dijkstra's algorithm** (coming soon).

---

## 🧗 Depth-First Search

### Recursive DFS

```dart
final cityMap = {
  'Home': ['Cafe', 'Park'],
  'Cafe': ['Home', 'Library', 'Gym'],
  'Park': ['Home', 'Gym'],
  'Library': ['Cafe', 'Museum'],
  'Gym': ['Cafe', 'Park', 'Museum'],
  'Museum': ['Library', 'Gym'],
  'Island': <String>[],
};

void dfs(Map<String, List<String>> g, String v, Set<String> visited, List<String> order) {
  visited.add(v);
  order.add(v);
  for (final next in g[v]!) {
    if (!visited.contains(next)) {
      dfs(g, next, visited, order); // go deeper before trying siblings
    }
  }
}

void main() {
  final order = <String>[];
  dfs(cityMap, 'Home', {}, order);
  print(order); // [Home, Cafe, Library, Museum, Gym, Park]
}
```

**🔍 What This Code Does:**

1. **Go Deep First**: From `Home` → `Cafe` → `Library` → `Museum` → `Gym` → `Park`, following the first unvisited neighbor each time.
2. **Backtrack Automatically**: When a vertex has no unvisited neighbors, the recursive call returns to the previous vertex.
3. **Visited Set**: Prevents infinite loops around cycles like `Home → Cafe → Gym → Park → Home`.
4. **O(V + E) Time, O(V) Space**: Recursion depth can reach V in the worst case.

### Iterative DFS with an explicit stack

```dart
final cityMap = {
  'Home': ['Cafe', 'Park'],
  'Cafe': ['Home', 'Library', 'Gym'],
  'Park': ['Home', 'Gym'],
  'Library': ['Cafe', 'Museum'],
  'Gym': ['Cafe', 'Park', 'Museum'],
  'Museum': ['Library', 'Gym'],
  'Island': <String>[],
};

List<String> dfsIterative(Map<String, List<String>> g, String start) {
  final visited = <String>{};
  final stack = [start];
  final order = <String>[];
  while (stack.isNotEmpty) {
    final v = stack.removeLast();
    if (!visited.add(v)) continue; // already processed
    order.add(v);
    // push in reverse so the first neighbor is explored first
    for (final next in g[v]!.reversed) {
      if (!visited.contains(next)) stack.add(next);
    }
  }
  return order;
}

void main() {
  print(dfsIterative(cityMap, 'Home')); // [Home, Cafe, Library, Museum, Gym, Park]
}
```

**🔍 What This Code Does:**

1. **Stack Instead of Queue**: LIFO makes the search dive deep.
2. **Mark When Popping**: A vertex may be pushed several times; `visited.add` skips repeats when popped.
3. **Reverse Push**: Makes the visiting order match the recursive version.
4. **No Recursion Limit**: Safe for very deep graphs.

---

## 🧩 Connected Components

How many separate "islands" does a graph have? Run a traversal from every unvisited vertex; each run discovers one component.

```dart
List<List<int>> components(int n, List<(int, int)> edges) {
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in edges) {
    adj[u].add(v);
    adj[v].add(u);
  }
  final visited = List.filled(n, false);
  final result = <List<int>>[];

  for (var start = 0; start < n; start++) {
    if (visited[start]) continue;
    final group = <int>[];
    final stack = [start];
    visited[start] = true;
    while (stack.isNotEmpty) {
      final v = stack.removeLast();
      group.add(v);
      for (final w in adj[v]) {
        if (!visited[w]) {
          visited[w] = true;
          stack.add(w);
        }
      }
    }
    result.add(group..sort());
  }
  return result;
}

void main() {
  final groups = components(7, [(0, 1), (1, 2), (3, 4), (5, 5)]);
  print(groups);        // [[0, 1, 2], [3, 4], [5], [6]]
  print(groups.length); // 4 components
}
```

**🔍 What This Code Does:**

1. **Outer Loop Over All Vertices**: Ensures isolated vertices (like `6`) become their own component.
2. **Inner Traversal**: Collects everything reachable from `start`.
3. **Boolean List as Visited**: When vertices are `0..n−1`, a `List<bool>` is faster than a `Set`.
4. **Self-Loop**: `(5, 5)` is an edge from a vertex to itself; it doesn't connect to anything else.
5. **O(V + E)** overall.

### Counting islands in a grid

```dart
int countIslands(List<String> grid) {
  final rows = grid.length, cols = grid[0].length;
  final seen = <(int, int)>{};
  var islands = 0;

  void sink(int r, int c) {
    if (r < 0 || c < 0 || r >= rows || c >= cols) return;
    if (grid[r][c] != '#' || !seen.add((r, c))) return;
    sink(r + 1, c);
    sink(r - 1, c);
    sink(r, c + 1);
    sink(r, c - 1);
  }

  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      if (grid[r][c] == '#' && !seen.contains((r, c))) {
        islands++;
        sink(r, c); // mark the whole island
      }
    }
  }
  return islands;
}

void main() {
  print(countIslands([
    '##...',
    '##..#',
    '...##',
    '#....',
  ])); // 3
}
```

**🔍 What This Code Does:**

1. **Grid as a Graph**: Land cells (`#`) are vertices; adjacent land cells are connected.
2. **Flood Fill**: `sink` recursively marks every cell of one island as seen.
3. **Count New Islands**: Each unseen land cell found by the scan starts a new island.
4. **Record Keys**: `(r, c)` records make a clean visited set.

---

## 🔄 Cycle Detection

### Undirected graphs: "a visited neighbor that isn't my parent"

```dart
bool hasCycleUndirected(int n, List<(int, int)> edges) {
  final adj = List.generate(n, (_) => <int>[]);
  for (final (u, v) in edges) {
    adj[u].add(v);
    adj[v].add(u);
  }
  final visited = List.filled(n, false);

  bool dfs(int v, int parent) {
    visited[v] = true;
    for (final w in adj[v]) {
      if (!visited[w]) {
        if (dfs(w, v)) return true;
      } else if (w != parent) {
        return true; // reached an already-visited vertex another way
      }
    }
    return false;
  }

  for (var v = 0; v < n; v++) {
    if (!visited[v] && dfs(v, -1)) return true;
  }
  return false;
}

void main() {
  print(hasCycleUndirected(4, [(0, 1), (1, 2), (2, 3)]));         // false (a path)
  print(hasCycleUndirected(4, [(0, 1), (1, 2), (2, 3), (3, 1)])); // true (1-2-3-1)
}
```

**🔍 What This Code Does:**

1. **Skip the Parent**: In an undirected graph, the edge back to where you came from isn't a cycle.
2. **Any Other Visited Neighbor Means a Cycle**: You've reached it by two different routes.
3. **Check Every Component**: The outer loop handles disconnected graphs.

### Directed graphs: three colors

In a directed graph, reaching a visited vertex isn't enough: it must be **on the current path** (still being explored). We track three states:

- ⚪ **White**: not visited yet
- 🔘 **Gray**: on the current DFS path
- ⚫ **Black**: fully explored

A cycle exists if we find an edge to a **gray** vertex (a **back edge**).

```dart
enum State { white, gray, black }

bool hasCycleDirected(Map<String, List<String>> g) {
  final state = {for (final v in g.keys) v: State.white};

  bool dfs(String v) {
    state[v] = State.gray;
    for (final w in g[v]!) {
      if (state[w] == State.gray) return true; // back edge → cycle
      if (state[w] == State.white && dfs(w)) return true;
    }
    state[v] = State.black;
    return false;
  }

  return g.keys.any((v) => state[v] == State.white && dfs(v));
}

void main() {
  final courses = {
    'Intro': ['Data Structures'],
    'Data Structures': ['Algorithms'],
    'Algorithms': <String>[],
  };
  print(hasCycleDirected(courses)); // false

  courses['Algorithms'] = ['Intro']; // circular prerequisites!
  print(hasCycleDirected(courses)); // true
}
```

**🔍 What This Code Does:**

1. **Gray = In Progress**: A vertex stays gray while its descendants are explored.
2. **Back Edge**: An edge to a gray vertex points back up the current path, which is a cycle.
3. **Black Isn't a Cycle**: Reaching a fully explored (black) vertex just means two paths share a destination, like `A → C` and `B → C`.
4. **Real Use**: Detecting impossible prerequisite chains or circular imports.

---

## 🎨 Bipartite Check (Two-Coloring)

Can you split the vertices into two groups so every edge goes **between** groups (e.g. teams with no rivals on the same team)? Color with BFS and look for conflicts.

```dart
import 'dart:collection';

bool isBipartite(List<List<int>> adj) {
  final color = List<int?>.filled(adj.length, null);
  for (var start = 0; start < adj.length; start++) {
    if (color[start] != null) continue;
    color[start] = 0;
    final q = Queue<int>()..add(start);
    while (q.isNotEmpty) {
      final v = q.removeFirst();
      for (final w in adj[v]) {
        if (color[w] == null) {
          color[w] = 1 - color[v]!; // opposite color
          q.add(w);
        } else if (color[w] == color[v]) {
          return false; // neighbors share a color
        }
      }
    }
  }
  return true;
}

void main() {
  // square: 0-1-2-3-0 → bipartite
  print(isBipartite([[1, 3], [0, 2], [1, 3], [2, 0]])); // true
  // triangle: 0-1-2-0 → not bipartite
  print(isBipartite([[1, 2], [0, 2], [0, 1]]));         // false
}
```

**🔍 What This Code Does:**

1. **Alternate Colors**: Each neighbor gets the opposite color (`1 − color`).
2. **Conflict = Not Bipartite**: Two adjacent vertices with the same color means an **odd cycle** exists.
3. **Every Component**: The outer loop colors disconnected parts too.

---

## ⚖️ BFS vs DFS

| | BFS | DFS |
|---|-----|-----|
| Structure | Queue | Stack / recursion |
| Explores | Level by level | One branch deeply, then backtracks |
| Shortest path (unweighted) | ✅ Yes | ❌ No |
| Memory | O(V) frontier, can be wide | O(depth) path, can be deep |
| Great for | Shortest paths, nearest X, levels, bipartite | Components, cycles, topological sort, mazes, backtracking |
| Time | O(V + E) | O(V + E) |

---

## ⚠️ Common Mistakes

### 1. Forgetting the visited set

On a graph with cycles, the traversal loops forever (or until memory runs out).

### 2. Marking visited too late in BFS

Marking on dequeue lets the same vertex be enqueued many times. Mark on **enqueue**.

### 3. Using undirected cycle logic on directed graphs

`A → B` and `B → A` is a cycle in a directed graph, but the "skip the parent" trick would ignore it. Use the three-color method for directed graphs.

### 4. Only starting from one vertex

Disconnected graphs need an outer loop over **all** vertices to find every component or cycle.

---

## 🧪 Try It Yourself

1. Return all vertices within **k** steps of a start vertex using BFS.
2. Find a path (any path) between two vertices using DFS, and print it.
3. Count the **number of provinces** given an adjacency matrix of which cities are connected.
4. **Clone a graph**: deep-copy a graph of node objects using a map from original to copy.

---

## 📌 Key Takeaways

- ✅ Graph traversals need a **visited set** because graphs can have **cycles**.
- ✅ **BFS** uses a **queue**, explores in order of distance and finds **shortest paths** in unweighted graphs.
- ✅ Rebuild BFS paths with a **parent map**.
- ✅ **DFS** uses **recursion** or a **stack** and dives deep before backtracking.
- ✅ Run a traversal from every unvisited vertex to find **connected components**.
- ✅ Detect cycles with **parent tracking** (undirected) or **three colors / back edges** (directed).
- ✅ Both run in **O(V + E)** time.

**Next up:** 📋 **Topological Sort**: ordering tasks that depend on each other.
