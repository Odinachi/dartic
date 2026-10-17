UF = r"""class UF {
  final List<int> p;
  int count;
  UF(int n)
      : p = List.generate(n, (i) => i),
        count = n;

  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);

  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    count--;
    return true;
  }
}
"""

QUESTIONS = [
    mcq(r"""
What problem does Union-Find (Disjoint Set Union) solve?
""", ["Tracking which elements belong to the same group as groups merge",
       "Finding shortest paths", "Sorting elements", "Detecting palindromes"],
        "Tracking which elements belong to the same group as groups merge"),

    mcq(r"""
What does `find(x)` return?
""", ["The representative (root) of x's set", "x's index", "The size of the set",
       "x's parent only"], "The representative (root) of x's set"),

    mcq(r"""
What does `union(a, b)` do?
""", ["Merges the sets containing a and b", "Adds an edge to a list", "Removes a and b",
       "Swaps a and b"], "Merges the sets containing a and b"),

    mcq(r"""
How do you check whether a and b are in the same set?
""", ["find(a) == find(b)", "parent[a] == parent[b]", "a == b", "rank[a] == rank[b]"],
        "find(a) == find(b)"),

    mcq(r"""
How is Union-Find initialized for n elements?
""", ["parent[i] = i: every element is its own set", "parent[i] = 0 for all i",
       "parent[i] = i + 1", "parent is empty"], "parent[i] = i: every element is its own set"),

    mcq(r"""
How do you recognize a root in the parent array?
""", ["parent[x] == x", "parent[x] == 0", "parent[x] == -1 always", "rank[x] == 0"],
        "parent[x] == x"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(5);
  uf.union(0, 1);
  uf.union(3, 4);
  print(uf.find(0) == uf.find(1));
  print(uf.find(1) == uf.find(3));
}
```
""", ["true then false", "true then true", "false then false", "false then true"],
        "true then false"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(6);
  uf.union(0, 1);
  uf.union(2, 3);
  uf.union(1, 3);
  print(uf.count);
}
```
""", ["3", "4", "2", "6"], "3"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(3);
  print(uf.union(0, 1));
  print(uf.union(1, 0));
}
```
""", ["true then false", "true then true", "false then false", "false then true"],
        "true then false"),

    mcq(r"""
Why can naive Union-Find become slow?
""", ["Trees can become long chains, making find O(n)", "Hashing collisions",
       "It sorts on every union", "It uses recursion"],
        "Trees can become long chains, making find O(n)"),

    mcq(r"""
What is "union by rank"?
""", ["Attaching the shorter tree under the taller one", "Merging sets in sorted order",
       "Ranking elements by value", "Always attaching under element 0"],
        "Attaching the shorter tree under the taller one"),

    mcq(r"""
When does a root's rank increase under union by rank?
""", ["When two trees of equal rank are merged", "On every union", "On every find",
       "Never"], "When two trees of equal rank are merged"),

    mcq(r"""
What height bound does union by rank alone guarantee?
""", ["O(log n)", "O(1)", "O(n)", "O(√n)"], "O(log n)"),

    mcq(r"""
What is path compression?
""", ["During find, making every node on the path point directly to the root",
       "Removing nodes from the tree", "Compressing the parent array with gzip",
       "Merging two roots"],
        "During find, making every node on the path point directly to the root"),

    mcq(r"""
With both union by rank and path compression, what is the amortized cost per operation?
""", ["O(α(n)), effectively constant", "O(log n)", "O(n)", "O(n log n)"],
        "O(α(n)), effectively constant"),

    mcq(r"""
What is α(n) in Union-Find's complexity?
""", ["The inverse Ackermann function, at most about 4 for practical n", "The number of sets",
       "The tree height", "log₂ n"],
        "The inverse Ackermann function, at most about 4 for practical n"),

    mcq(r"""
What does this print?

```dart
void main() {
  final p = [0, 0, 1, 2]; // chain 3 → 2 → 1 → 0
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  find(3);
  print(p);
}
```
""", ["[0, 0, 0, 0]", "[0, 0, 1, 2]", "[0, 1, 2, 3]", "[3, 3, 3, 3]"], "[0, 0, 0, 0]"),

    mcq(r"""
In `int find(int x) => p[x] == x ? x : p[x] = find(p[x]);`, what does the assignment achieve?
""", ["It compresses the path by pointing x straight to the root", "It resets x to its own set",
       "It merges two sets", "Nothing; it's just a lookup"],
        "It compresses the path by pointing x straight to the root"),

    order(r"""
Complete union with root linking:

```dart
bool union(int a, int b) {
  final ra = %order%(a), rb = find(b);
  if (ra %order% rb) return false;
  parent[%order%] = rb;
  return true;
}
```
""", ["find", "==", "ra", "!=", "a", "parent"], ["find", "==", "ra"]),

    mcq(r"""
Why must union link ROOTS rather than the elements themselves?
""", ["Changing a non-root's parent can detach it from its own set or half-merge sets",
       "Roots are faster to access", "Elements can't have parents", "It doesn't matter"],
        "Changing a non-root's parent can detach it from its own set or half-merge sets"),

    mcq(r"""
Why is `parent[a] == parent[b]` NOT a valid connectivity check?
""", ["Two elements in the same set can have different direct parents",
       "Parents are always equal", "It's too slow", "It works fine"],
        "Two elements in the same set can have different direct parents"),

    mcq(r"""
How does Union-Find detect a cycle when adding undirected edges?
""", ["If an edge's endpoints already have the same root, adding it creates a cycle",
       "If a vertex has degree 3", "If find returns -1", "It can't"],
        "If an edge's endpoints already have the same root, adding it creates a cycle"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
(int, int)? cycleEdge(int n, List<(int, int)> edges) {
  final uf = UF(n);
  for (final (u, v) in edges) {
    if (!uf.union(u, v)) return (u, v);
  }
  return null;
}

void main() {
  print(cycleEdge(3, [(0, 1), (1, 2), (0, 2)]));
}
```
""", ["(0, 2)", "(1, 2)", "null", "(0, 1)"], "(0, 2)"),

    mcq(r"""
How do you count connected components with Union-Find?
""", ["Start the count at n and decrement on every successful union",
       "Count the edges", "Count the roots at the start", "Run BFS afterwards"],
        "Start the count at n and decrement on every successful union"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(7);
  for (final (a, b) in [(0, 1), (1, 2), (3, 4), (5, 6), (6, 5)]) {
    uf.union(a, b);
  }
  print(uf.count);
}
```
""", ["3", "2", "4", "7"], "3"),

    mcq(r"""
How can Union-Find work with String elements instead of integers?
""", ["Use a Map<String, String> for parents", "Convert strings to their length",
       "It can't", "Use a List<String> indexed by character"],
        "Use a Map<String, String> for parents"),

    mcq(r"""
What does this print?

```dart
void main() {
  final parent = <String, String>{};
  String find(String x) {
    parent.putIfAbsent(x, () => x);
    final p = parent[x]!;
    return p == x ? x : parent[x] = find(p);
  }

  void union(String a, String b) => parent[find(a)] = find(b);

  union('ada@a.com', 'ada@b.com');
  union('ada@b.com', 'ada@c.com');
  print(find('ada@a.com') == find('ada@c.com'));
}
```
""", ["true", "false", "null", "It throws an error"], "true"),

    mcq(r"""
Which operation can Union-Find NOT do efficiently?
""", ["Split a set (remove an element or edge)", "Merge two sets", "Check if two elements share a set",
       "Count the sets"], "Split a set (remove an element or edge)"),

    mcq(r"""
Which famous MST algorithm relies on Union-Find?
""", ["Kruskal's algorithm", "Dijkstra's algorithm", "Bellman-Ford", "Floyd-Warshall"],
        "Kruskal's algorithm"),

    mcq(r"""
Which problem is NOT a good fit for Union-Find?
""", ["Finding the shortest path between two vertices", "Counting connected components",
       "Detecting cycles in an undirected graph", "Grouping accounts that share emails"],
        "Finding the shortest path between two vertices"),

    mcq(r"""
Is Union-Find suitable for reachability in DIRECTED graphs?
""", ["No, it models undirected (symmetric) connectivity", "Yes, always",
       "Only for DAGs", "Only with path compression"],
        "No, it models undirected (symmetric) connectivity"),

    mcq(r"""
In a grid, how can a cell (r, c) be mapped to a single Union-Find index?
""", ["r * cols + c", "r + c", "r * c", "c * rows + r * cols"], "r * cols + c"),

    mcq(r"""
What does this print?

```dart
void main() {
  const cols = 4;
  print(2 * cols + 3);
}
```
""", ["11", "9", "14", "5"], "11"),

    mcq(r"""
When a new land cell joins two existing islands in "islands after each addition", how does the count change?
""", ["+1 for the new cell, then −1 for each distinct island it merges with",
       "It always increases by 1", "It always stays the same", "It resets to 1"],
        "+1 for the new cell, then −1 for each distinct island it merges with"),

    mcq(r"""
What does union by SIZE do?
""", ["Attaches the smaller set's root under the larger set's root", "Merges sets in size order",
       "Limits sets to a maximum size", "Sorts elements by size"],
        "Attaches the smaller set's root under the larger set's root"),

    mcq(r"""
What does this print?

```dart
void main() {
  final p = List.generate(4, (i) => i);
  final size = List.filled(4, 1);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  void union(int a, int b) {
    var ra = find(a), rb = find(b);
    if (ra == rb) return;
    if (size[ra] < size[rb]) {
      final t = ra;
      ra = rb;
      rb = t;
    }
    p[rb] = ra;
    size[ra] += size[rb];
  }

  union(0, 1);
  union(2, 0);
  print(size[find(2)]);
}
```
""", ["3", "2", "1", "4"], "3"),

    mcq(r"""
Given equations a==b, b==c and a!=c, what does Union-Find reveal?
""", ["They're contradictory: a and c end up in the same set but must differ",
       "They're all satisfiable", "Only a==b is valid", "Nothing"],
        "They're contradictory: a and c end up in the same set but must differ"),

    mcq(r"""
In what order should equality and inequality constraints be processed?
""", ["Union all equalities first, then check each inequality",
       "Inequalities first", "Alternate them", "Order doesn't matter at all"],
        "Union all equalities first, then check each inequality"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(3);
  uf.union(0, 1);
  uf.union(1, 2);
  print(uf.find(0) == uf.find(2));
  print(uf.count);
}
```
""", ["true then 1", "false then 2", "true then 2", "true then 3"], "true then 1"),

    mcq(r"""
What happens if you union the same pair many times?
""", ["After the first time, nothing changes", "The count keeps decreasing",
       "It throws an error", "The sets split"], "After the first time, nothing changes"),

    mcq(r"""
Which structure represents the sets in Union-Find?
""", ["A forest of trees built from parent pointers", "A hash table of lists",
       "A single sorted array", "A heap"], "A forest of trees built from parent pointers"),

    mcq(r"""
What does this print?

```dart
void main() {
  final p = [1, 3, 3, 3, 4, 5];
  int find(int x) {
    while (p[x] != x) {
      x = p[x];
    }
    return x;
  }

  print([for (var i = 0; i < 6; i++) find(i)]);
}
```
""", ["[3, 3, 3, 3, 4, 5]", "[1, 3, 3, 3, 4, 5]", "[0, 1, 2, 3, 4, 5]", "[3, 3, 3, 3, 3, 3]"],
        "[3, 3, 3, 3, 4, 5]"),

    mcq(r"""
In the parent array `[1, 3, 3, 3, 4, 5]`, how many sets are there?
""", ["3", "6", "1", "2"], "3"),

    mcq(r"""
What is the "redundant connection" problem?
""", ["Finding an edge whose removal leaves the graph a tree (it closes a cycle)",
       "Finding duplicate vertices", "Finding the heaviest edge", "Finding isolated vertices"],
        "Finding an edge whose removal leaves the graph a tree (it closes a cycle)"),

    mcq(r"""
Why is Union-Find better than re-running BFS each time an edge is added?
""", ["Each union/find is nearly O(1), while BFS costs O(V + E) every time",
       "BFS can't find components", "Union-Find uses less code only", "It isn't better"],
        "Each union/find is nearly O(1), while BFS costs O(V + E) every time"),

    mcq(r"""
What does iterative path compression do in two passes?
""", ["First find the root, then re-point every node on the path to it",
       "First merge, then split", "First sort, then search", "First count, then delete"],
        "First find the root, then re-point every node on the path to it"),

    fill(r"""
Initialize every element as its own parent:

```dart
void main() {
  final parent = List.%fill%(5, (i) => i);
  print(parent); // [0, 1, 2, 3, 4]
}
```
""", "generate"),

    mcq(r"""
What does this print?

```dart
""" + UF + r"""
void main() {
  final uf = UF(4);
  final edges = [(0, 1), (2, 3), (1, 2), (0, 3)];
  var extra = 0;
  for (final (a, b) in edges) {
    if (!uf.union(a, b)) extra++;
  }
  print('$extra ${uf.count}');
}
```
""", ["1 1", "0 1", "1 2", "2 1"], "1 1"),

    mcq(r"""
To connect n computers with cables, at least how many cables are needed?
""", ["n − 1", "n", "n / 2", "2n"], "n − 1"),

    mcq(r"""
Stones sharing a row or column can be "connected". The maximum stones removable is:
""", ["Number of stones − number of connected groups", "Number of groups",
       "Number of rows", "Always 0"], "Number of stones − number of connected groups"),

    mcq(r"""
Which of these is a key property of Union-Find's sets?
""", ["They are disjoint: no element belongs to two sets", "They are always sorted",
       "They can overlap", "They have fixed sizes"],
        "They are disjoint: no element belongs to two sets"),

    mcq(r"""
What does `union` returning false tell you?
""", ["The two elements were already in the same set", "The union failed due to an error",
       "One element doesn't exist", "The sets were empty"],
        "The two elements were already in the same set"),

    mcq(r"""
What does this print?

```dart
void main() {
  final p = List.generate(5, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  for (var i = 0; i < 4; i++) {
    p[find(i)] = find(i + 1);
  }
  print(find(0));
}
```
""", ["4", "0", "1", "3"], "4"),

    mcq(r"""
Finding the earliest moment everyone in a network becomes friends uses Union-Find by:
""", ["Processing friendships in time order until the component count reaches 1",
       "Sorting people by name", "Running Dijkstra", "Counting edges only"],
        "Processing friendships in time order until the component count reaches 1"),
]
