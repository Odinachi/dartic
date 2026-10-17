# Union-Find

Imagine a school 🏫 where students keep forming friend groups.

- Ada and Bob become friends. Now they're in the **same group**.
- Cy and Dee become friends: a second group.
- Bob and Cy become friends, so **both groups merge** into one big group.

Two questions keep coming up:

1. *"Are Ada and Dee in the same group?"* (**find**)
2. *"Merge the groups of these two students."* (**union**)

Running a full BFS every time someone asks would be slow. Instead, each group elects a **leader**, and everyone remembers who to ask to reach that leader. Two students are in the same group if they have the **same leader**. 👑

👉 That's **Union-Find**, also called the **Disjoint Set Union (DSU)**:

> **Union-Find** maintains a collection of **disjoint sets**. `find(x)` returns the **representative** (root) of x's set, and `union(a, b)` merges two sets. With **path compression** and **union by rank**, both run in **nearly O(1)** amortized time.

---

## 🌲 The Idea: A Forest of Parent Pointers

Each element points to a **parent**. Following parents leads to the **root**, which represents the whole set. A root is its own parent.

```text
Sets: {0, 1, 2, 3}   {4, 5}   {6}

     0          4       6
    / \         |
   1   2        5
       |
       3

parent = [0, 0, 0, 2, 4, 4, 6]
find(3): 3 → 2 → 0   (root 0)
find(5): 5 → 4       (root 4)
same set? find(3) == find(5) → 0 == 4 → no
```

---

## 🐢 Version 1: Naive Union-Find

```dart
class NaiveUnionFind {
  final List<int> parent;

  NaiveUnionFind(int n) : parent = List.generate(n, (i) => i); // everyone is their own root

  int find(int x) {
    while (parent[x] != x) {
      x = parent[x]; // climb to the root
    }
    return x;
  }

  void union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra != rb) parent[ra] = rb; // attach one root under the other
  }

  bool connected(int a, int b) => find(a) == find(b);
}

void main() {
  final uf = NaiveUnionFind(6);
  uf.union(0, 1);
  uf.union(2, 3);
  uf.union(1, 3);
  print(uf.connected(0, 2)); // true
  print(uf.connected(0, 4)); // false
  print(uf.parent);          // [1, 3, 3, 3, 4, 5]
}
```

**🔍 What This Code Does:**

1. **Initialization**: `parent[i] = i` means every element starts in its own set of one.
2. **`find`**: Follows parent pointers until reaching an element that is its own parent: the root.
3. **`union`**: Finds both roots and makes one the parent of the other, merging the sets.
4. **`connected`**: Same root means same set.

### The problem: tall trees

```dart
class NaiveUnionFind {
  final List<int> parent;
  NaiveUnionFind(int n) : parent = List.generate(n, (i) => i);

  int find(int x) {
    var steps = 0;
    while (parent[x] != x) {
      x = parent[x];
      steps++;
    }
    lastSteps = steps;
    return x;
  }

  int lastSteps = 0;

  void union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra != rb) parent[ra] = rb;
  }
}

void main() {
  const n = 10000;
  final uf = NaiveUnionFind(n);
  for (var i = 0; i < n - 1; i++) {
    uf.union(i, i + 1); // always attaches the old root under the new element
  }
  uf.find(0);
  print('find(0) took ${uf.lastSteps} steps'); // 9999: a linked list!
}
```

**🔍 What This Code Does:**

1. **Unlucky Unions**: Each union hangs the whole existing tree under a single new element.
2. **Degenerate Tree**: The result is a chain of 10,000 nodes.
3. **O(n) Finds**: `find(0)` walks the entire chain. We need two fixes.

---

## ⚡ Fix 1: Union by Rank (or Size)

Always attach the **shorter** tree under the **taller** one. Then a tree's height only grows when two trees of **equal** height merge, which keeps height at most **log₂ n**.

## ⚡ Fix 2: Path Compression

During `find`, make every node on the path point **directly to the root**. The next `find` on any of them takes one step.

```text
Before find(3):        After find(3) with path compression:
      0                        0
      |                     / | \
      1                    1  2  3
      |
      2
      |
      3
```

## 🏆 The Optimized Union-Find

```dart
class UnionFind {
  final List<int> _parent;
  final List<int> _rank;
  int _components;

  UnionFind(int n)
      : _parent = List.generate(n, (i) => i),
        _rank = List.filled(n, 0),
        _components = n;

  int get components => _components;

  int find(int x) {
    // Path compression (iterative): first find the root...
    var root = x;
    while (_parent[root] != root) {
      root = _parent[root];
    }
    // ...then point every node on the path straight at it
    while (_parent[x] != root) {
      final next = _parent[x];
      _parent[x] = root;
      x = next;
    }
    return root;
  }

  /// Merges the sets of a and b. Returns false if they were already joined.
  bool union(int a, int b) {
    var ra = find(a), rb = find(b);
    if (ra == rb) return false;
    if (_rank[ra] < _rank[rb]) {
      final t = ra;
      ra = rb;
      rb = t; // ensure ra is the taller tree
    }
    _parent[rb] = ra; // shorter tree goes under the taller one
    if (_rank[ra] == _rank[rb]) _rank[ra]++;
    _components--;
    return true;
  }

  bool connected(int a, int b) => find(a) == find(b);
}

void main() {
  const n = 10000;
  final uf = UnionFind(n);
  for (var i = 0; i < n - 1; i++) {
    uf.union(i, i + 1);
  }
  print(uf.connected(0, n - 1)); // true
  print(uf.components);          // 1

  final friends = UnionFind(6);
  friends.union(0, 1); // Ada–Bob
  friends.union(2, 3); // Cy–Dee
  print(friends.components);        // 4: {0,1} {2,3} {4} {5}
  print(friends.union(1, 3));       // true  (groups merge)
  print(friends.union(0, 2));       // false (already in the same group)
  print(friends.components);        // 3
  print(friends.connected(0, 3));   // true
}
```

**🔍 What This Code Does:**

This code demonstrates **union-find with union by rank and path compression**:

1. **Rank**: An upper bound on each root's tree height. Only roots' ranks matter.

2. **Union by Rank**: The root with the smaller rank is attached under the larger one. Ranks only grow (by 1) when two equal-rank trees merge.

3. **Path Compression**: `find` re-points every node it passes directly at the root, flattening the tree for future calls.

4. **Component Counter**: Starts at `n` and drops by one on every successful union. Great for "how many groups?" questions.

5. **`union` Returns a bool**: `false` means the two elements were already connected, which is exactly what cycle detection needs.

6. **Nearly O(1)**: Together, these optimizations make each operation **O(α(n))** amortized, where α is the inverse Ackermann function: at most **4** for any input size that fits in our universe. 🌌

| Version | `find` / `union` |
|---------|------------------|
| Naive | O(n) worst case |
| Union by rank only | O(log n) |
| Path compression only | O(log n) amortized |
| **Both** | **O(α(n)) ≈ O(1)** amortized |

---

## 🔁 Detecting a Cycle in an Undirected Graph

Add edges one at a time. If an edge connects two vertices that are **already** in the same set, adding it creates a **cycle**.

```dart
class UnionFind {
  final List<int> p;
  UnionFind(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]); // recursive compression
  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    return true;
  }
}

(int, int)? firstCycleEdge(int n, List<(int, int)> edges) {
  final uf = UnionFind(n);
  for (final (u, v) in edges) {
    if (!uf.union(u, v)) return (u, v); // already connected → cycle
  }
  return null;
}

void main() {
  print(firstCycleEdge(4, [(0, 1), (1, 2), (2, 3)]));         // null
  print(firstCycleEdge(4, [(0, 1), (1, 2), (2, 0), (2, 3)])); // (2, 0)
}
```

**🔍 What This Code Does:**

1. **Recursive Path Compression**: `p[x] = find(p[x])` sets the parent to the root on the way back up, and the assignment's value is returned.
2. **Cycle Edge**: `(2, 0)` connects 2 and 0, which were already linked through 1.
3. **Redundant Connection**: This is exactly the "which cable can be removed without disconnecting the network?" problem.
4. **O(E · α(V))**: Practically linear.

---

## 🏝️ Counting Groups

### Number of connected components

```dart
class UnionFind {
  final List<int> p;
  int count;
  UnionFind(int n)
      : p = List.generate(n, (i) => i),
        count = n;
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  void union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra != rb) {
      p[ra] = rb;
      count--;
    }
  }
}

void main() {
  final uf = UnionFind(7);
  for (final (a, b) in [(0, 1), (1, 2), (3, 4), (5, 6), (6, 5)]) {
    uf.union(a, b);
  }
  print(uf.count); // 3: {0,1,2} {3,4} {5,6}
}
```

**🔍 What This Code Does:**

1. **Start With n Groups**: Every element is alone.
2. **Each Successful Union Merges Two Groups**: `count--`.
3. **Duplicates Are Harmless**: `(6, 5)` finds the same root and changes nothing.

### Grouping accounts by shared email

```dart
class UnionFind {
  final Map<String, String> _parent = {};

  String find(String x) {
    _parent.putIfAbsent(x, () => x);
    final p = _parent[x]!;
    if (p == x) return x;
    final root = find(p);
    _parent[x] = root;
    return root;
  }

  void union(String a, String b) => _parent[find(a)] = find(b);
}

void main() {
  final accounts = [
    ['ada@mail.com', 'ada@work.com'],
    ['bob@mail.com'],
    ['ada@work.com', 'lovelace@home.com'],
    ['bob@mail.com', 'bobby@chat.com'],
  ];

  final uf = UnionFind();
  for (final emails in accounts) {
    for (final e in emails.skip(1)) {
      uf.union(emails.first, e); // all emails in one account belong together
    }
    uf.find(emails.first); // register single-email accounts too
  }

  final groups = <String, List<String>>{};
  for (final e in accounts.expand((a) => a).toSet()) {
    groups.putIfAbsent(uf.find(e), () => []).add(e);
  }
  for (final g in groups.values) {
    print(g..sort());
  }
  // [ada@mail.com, ada@work.com, lovelace@home.com]
  // [bob@mail.com, bobby@chat.com]
}
```

**🔍 What This Code Does:**

1. **String Elements**: A `Map<String, String>` replaces the parent list, so elements can be any hashable value.
2. **Lazy Registration**: `find` adds unseen elements as their own root.
3. **Link Within Accounts**: Every email in an account is unioned with the account's first email.
4. **Transitive Merging**: Accounts 1 and 3 share `ada@work.com`, so all three of Ada's emails end up together.
5. **Group by Root**: Collect emails under their representative.

---

## 🧱 Union-Find on a Grid

```dart
class UnionFind {
  final List<int> p;
  UnionFind(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  void union(int a, int b) => p[find(a)] = find(b);
}

int islandsAfterEachLand(int rows, int cols, List<(int, int)> lands) {
  final uf = UnionFind(rows * cols);
  final isLand = <int>{};
  var islands = 0;
  for (final (r, c) in lands) {
    final id = r * cols + c; // flatten (r, c) to one index
    if (!isLand.add(id)) continue;
    islands++;
    for (final (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)]) {
      final nr = r + dr, nc = c + dc;
      final nid = nr * cols + nc;
      if (nr < 0 || nc < 0 || nr >= rows || nc >= cols || !isLand.contains(nid)) {
        continue;
      }
      if (uf.find(id) != uf.find(nid)) {
        uf.union(id, nid);
        islands--; // two islands merged into one
      }
    }
    print('after land at ($r, $c): $islands island(s)');
  }
  return islands;
}

void main() {
  islandsAfterEachLand(3, 3, [(0, 0), (0, 1), (1, 2), (2, 1), (1, 1)]);
}
```

**🔍 What This Code Does:**

1. **Flattened Cells**: `r * cols + c` gives each cell an integer id.
2. **Dynamic Connectivity**: Land appears one cell at a time; each new cell starts as its own island.
3. **Merge With Neighbors**: Each union with a different island reduces the count.
4. **Why Union-Find?**: Re-running BFS after every new land cell would be far slower.
5. **Output**: 1, 1, 2, 3, then 1 when the center cell joins everything.

---

## 🧭 When to Use Union-Find

| Problem | Union-Find? |
|---------|-------------|
| "Are a and b connected?" with edges only being **added** | ✅ Perfect |
| Counting components as edges arrive | ✅ |
| Cycle detection in undirected graphs | ✅ |
| **Kruskal's** minimum spanning tree | ✅ (next lesson!) |
| Grouping items by transitive "same as" relations | ✅ |
| Edges being **removed** | ❌ Union-Find can't split sets |
| Shortest paths, actual path between a and b | ❌ Use BFS/Dijkstra |
| Directed graphs (reachability) | ❌ |

---

## ⚠️ Common Mistakes

### 1. Linking elements instead of roots

```dart
void main() {
  final parent = [0, 0, 2, 2]; // sets {0,1} and {2,3}
  // ❌ parent[1] = 3; links non-roots: 0's set and 2's set aren't properly merged
  // ✅ link the roots
  int find(int x) => parent[x] == x ? x : find(parent[x]);
  parent[find(1)] = find(3);
  print(find(0) == find(2)); // true
}
```

**🔍 What This Code Does:**

1. **Always Union Roots**: Changing a non-root's parent can detach it from its old set or leave sets half-merged.
2. **The Fix**: `parent[find(a)] = find(b)`.

### 2. Forgetting path compression on huge inputs

Without it (and without union by rank), finds can degrade to O(n).

### 3. Comparing parents instead of roots

`parent[a] == parent[b]` is **not** the same as being connected; always compare `find(a) == find(b)`.

### 4. Expecting deletions

Union-Find only merges. To support removals, process deletions in reverse as additions, or use a different structure.

---

## 🧪 Try It Yourself

1. Add **union by size** (track set sizes) and a `sizeOf(x)` method returning the size of x's group.
2. **Satisfiability of equations**: given `a==b`, `b!=c`, `c==a`, decide whether all can hold at once.
3. **Most stones removed**: stones sharing a row or column can be connected; answer = stones − components.
4. Find the earliest time when everyone in a social network becomes connected, given timestamped friendships.

---

## 📌 Key Takeaways

- ✅ **Union-Find (DSU)** tracks disjoint sets with `find` (representative) and `union` (merge).
- ✅ Sets are trees of **parent pointers**; the **root** represents the set.
- ✅ **Union by rank/size** keeps trees short; **path compression** flattens them.
- ✅ With both, operations are **O(α(n))**, effectively **constant** time.
- ✅ `union` returning **false** means the elements were already connected: instant **cycle detection**.
- ✅ Great for components, grouping, dynamic connectivity and **Kruskal's MST**; it **can't** split sets or find paths.

**Next up:** 🌉 **Minimum Spanning Trees**: connecting everything as cheaply as possible.
