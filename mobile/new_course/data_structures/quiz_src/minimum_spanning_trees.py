KRUSKAL = r"""class UF {
  final List<int> p;
  UF(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    return true;
  }
}

int? kruskal(int n, List<(int, int, int)> edges) {
  final sorted = [...edges]..sort((a, b) => a.$3.compareTo(b.$3));
  final uf = UF(n);
  var cost = 0, used = 0;
  for (final (u, v, w) in sorted) {
    if (uf.union(u, v)) {
      cost += w;
      used++;
    }
  }
  return used == n - 1 ? cost : null;
}
"""

PIC = r"""```dart
//     A ──4── B
//     │ \     │
//     1   3   2
//     │     \ │
//     C ──5── D ──7── E
```"""

QUESTIONS = [
    mcq(r"""
What is a spanning tree of a connected undirected graph?
""", ["A subset of edges connecting all vertices with no cycles",
       "Any path through the graph", "The graph's shortest path tree",
       "A tree containing only the heaviest edges"],
        "A subset of edges connecting all vertices with no cycles"),

    mcq(r"""
How many edges does a spanning tree of V vertices have?
""", ["V − 1", "V", "V + 1", "2V"], "V − 1"),

    mcq(r"""
What is a minimum spanning tree (MST)?
""", ["A spanning tree with the smallest total edge weight", "The spanning tree with the fewest vertices",
       "The shortest path between two vertices", "A tree of height 1"],
        "A spanning tree with the smallest total edge weight"),

    mcq(r"""
What is the total weight of the MST of this graph?

""" + PIC, ["13", "14", "12", "17"], "13"),

    mcq(r"""
Which edges form the MST of this graph?

""" + PIC, ["A–C, B–D, A–D, D–E", "A–C, A–B, B–D, D–E", "A–B, B–D, C–D, D–E",
                "A–C, C–D, B–D, D–E"], "A–C, B–D, A–D, D–E"),

    mcq(r"""
In this graph, which edge must be in every spanning tree, and why?

""" + PIC, ["D–E, because it's E's only connection", "A–C, because it's the cheapest",
                "C–D, because it's in the middle", "A–B, because A is first"],
        "D–E, because it's E's only connection"),

    mcq(r"""
Is the MST the same as the set of shortest paths between vertices?
""", ["No, an MST minimizes total connection cost, not individual routes",
       "Yes, always", "Only for trees", "Only when all weights are equal"],
        "No, an MST minimizes total connection cost, not individual routes"),

    mcq(r"""
What kind of graph is an MST defined for?
""", ["Connected, undirected, weighted graphs", "Directed acyclic graphs only",
       "Unweighted graphs only", "Any directed graph"],
        "Connected, undirected, weighted graphs"),

    mcq(r"""
What is the first step of Kruskal's algorithm?
""", ["Sort all edges by weight", "Pick a starting vertex", "Run BFS",
       "Compute in-degrees"], "Sort all edges by weight"),

    mcq(r"""
In Kruskal's algorithm, when is an edge added?
""", ["When it connects two different components (doesn't create a cycle)",
       "Always", "Only if it touches the start vertex", "Only if it's the heaviest"],
        "When it connects two different components (doesn't create a cycle)"),

    mcq(r"""
Which data structure makes Kruskal's cycle check nearly O(1)?
""", ["Union-Find", "A stack", "A queue", "A trie"], "Union-Find"),

    mcq(r"""
What is the time complexity of Kruskal's algorithm?
""", ["O(E log E), dominated by sorting", "O(V³)", "O(V + E)", "O(E²)"],
        "O(E log E), dominated by sorting"),

    mcq(r"""
What does this print?

```dart
""" + KRUSKAL + r"""
void main() {
  print(kruskal(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4), (0, 2, 5)]));
}
```
""", ["6", "10", "15", "7"], "6"),

    mcq(r"""
What does this print?

```dart
""" + KRUSKAL + r"""
void main() {
  print(kruskal(4, [(0, 1, 1), (2, 3, 1)]));
}
```
""", ["null", "2", "1", "0"], "null"),

    mcq(r"""
A graph has 4 vertices and only the edges 0–1 and 2–3. Why does Kruskal's fail to produce a spanning tree?
""", ["The graph is disconnected, so no spanning tree exists", "The weights are equal",
       "There are too many edges", "Kruskal can't handle ties"],
        "The graph is disconnected, so no spanning tree exists"),

    mcq(r"""
When can Kruskal's algorithm stop early?
""", ["Once V − 1 edges have been added", "After the first edge", "After half the edges",
       "It can never stop early"], "Once V − 1 edges have been added"),

    order(r"""
Complete Kruskal's loop:

```dart
final sorted = [...edges]..%order%((a, b) => a.w.compareTo(b.w));
for (final e in sorted) {
  if (uf.%order%(e.u, e.v)) {
    mst.%order%(e);
  }
}
```
""", ["sort", "union", "add", "find", "remove", "reverse"], ["sort", "union", "add"]),

    mcq(r"""
How does Prim's algorithm grow the MST?
""", ["From one vertex, repeatedly adding the cheapest edge leaving the current tree",
       "By sorting all edges globally first", "By removing the heaviest edges",
       "By running DFS"], "From one vertex, repeatedly adding the cheapest edge leaving the current tree"),

    mcq(r"""
Which data structure does Prim's algorithm typically use?
""", ["A priority queue of candidate edges", "Union-Find", "A FIFO queue", "A stack"],
        "A priority queue of candidate edges"),

    mcq(r"""
What is the time complexity of Prim's algorithm with a binary heap?
""", ["O(E log V)", "O(V³)", "O(E²)", "O(V + E)"], "O(E log V)"),

    mcq(r"""
How is Prim's algorithm similar to Dijkstra's?
""", ["Both use a priority queue; Prim's prioritizes by edge weight, Dijkstra's by total distance",
       "They are identical", "Both use Union-Find", "Both sort all edges first"],
        "Both use a priority queue; Prim's prioritizes by edge weight, Dijkstra's by total distance"),

    mcq(r"""
In lazy Prim's, what happens when a popped edge leads to a vertex already in the tree?
""", ["It's skipped", "It's added anyway", "The algorithm restarts", "It's added twice"],
        "It's skipped"),

    mcq(r"""
Which algorithm suits a dense graph stored as an adjacency matrix best?
""", ["Array-based Prim's in O(V²)", "Kruskal's with sorting all V² edges",
       "Bellman-Ford", "BFS"], "Array-based Prim's in O(V²)"),

    mcq(r"""
Which algorithm suits a sparse graph given as an edge list best?
""", ["Kruskal's", "Array-based Prim's", "Floyd-Warshall", "Topological sort"],
        "Kruskal's"),

    mcq(r"""
What does the cut property say?
""", ["The cheapest edge crossing any cut of the vertices is safe to include in an MST",
       "The heaviest edge is always in the MST", "Every cut has exactly one edge",
       "Cutting an MST edge makes it shorter"],
        "The cheapest edge crossing any cut of the vertices is safe to include in an MST"),

    mcq(r"""
Why are Kruskal's and Prim's called greedy algorithms?
""", ["They make the locally cheapest safe choice at each step", "They use a lot of memory",
       "They try every possible tree", "They always choose the heaviest edge"],
        "They make the locally cheapest safe choice at each step"),

    mcq(r"""
If all edge weights are distinct, how many MSTs does a connected graph have?
""", ["Exactly one", "Possibly many", "Zero", "V − 1"], "Exactly one"),

    mcq(r"""
If several edges share the same weight, can there be multiple MSTs?
""", ["Yes, with the same total weight", "No, never", "Yes, with different total weights",
       "Only for directed graphs"], "Yes, with the same total weight"),

    mcq(r"""
What happens if you run Kruskal's on a disconnected graph?
""", ["You get a minimum spanning forest (fewer than V − 1 edges)", "It loops forever",
       "It adds fake edges", "It returns the shortest path"],
        "You get a minimum spanning forest (fewer than V − 1 edges)"),

    mcq(r"""
How do you get a MAXIMUM spanning tree with Kruskal's?
""", ["Sort edges in descending order of weight", "Use a stack instead of Union-Find",
       "Negate the vertex ids", "It's impossible"], "Sort edges in descending order of weight"),

    mcq(r"""
What does this print?

```dart
""" + KRUSKAL + r"""
void main() {
  final edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)];
  final negated = [for (final (u, v, w) in edges) (u, v, -w)];
  print(-kruskal(4, negated)!);
}
```
""", ["9", "6", "10", "4"], "9"),

    mcq(r"""
How can an MST be used for clustering into k groups?
""", ["Build the MST and remove its k − 1 most expensive edges",
       "Remove the k cheapest edges", "Run Kruskal's k times", "Pick k random vertices"],
        "Build the MST and remove its k − 1 most expensive edges"),

    mcq(r"""
What does this print?

```dart
class UF {
  final List<int> p;
  UF(int n) : p = List.generate(n, (i) => i);
  int find(int x) => p[x] == x ? x : p[x] = find(p[x]);
  bool union(int a, int b) {
    final ra = find(a), rb = find(b);
    if (ra == rb) return false;
    p[ra] = rb;
    return true;
  }
}

void main() {
  final edges = [(0, 1, 1), (2, 3, 1), (1, 2, 10)]..sort((a, b) => a.$3.compareTo(b.$3));
  final uf = UF(4);
  var groups = 4;
  for (final (u, v, _) in edges) {
    if (groups == 2) break;
    if (uf.union(u, v)) groups--;
  }
  print(uf.find(0) == uf.find(2));
}
```
""", ["false", "true", "2", "null"], "false"),

    mcq(r"""
Which real problem is an MST problem?
""", ["Laying cable to connect every building at minimum total cost",
       "Finding the fastest route from home to work", "Ordering course prerequisites",
       "Counting islands in a grid"],
        "Laying cable to connect every building at minimum total cost"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  print(const Point(0, 0).distanceTo(const Point(3, 4)));
}
```
""", ["5.0", "7.0", "25.0", "1.0"], "5.0"),

    mcq(r"""
In array-based Prim's, what does `best[v]` store?
""", ["The cheapest known edge weight connecting v to the current tree",
       "v's distance from the start", "v's degree", "v's parent's id"],
        "The cheapest known edge weight connecting v to the current tree"),

    mcq(r"""
What does this print?

```dart
void main() {
  final edges = [(0, 1, 3), (0, 2, 1), (1, 2, 2)];
  final sorted = [...edges]..sort((a, b) => a.$3.compareTo(b.$3));
  print(sorted.map((e) => e.$3).toList());
}
```
""", ["[1, 2, 3]", "[3, 1, 2]", "[3, 2, 1]", "[1, 3, 2]"], "[1, 2, 3]"),

    mcq(r"""
In Kruskal's on edges A–C(1), B–D(2), A–D(3), A–B(4), why is A–B skipped?
""", ["A and B are already connected through A–D–B, so it would create a cycle",
       "It's the heaviest edge", "A has too many edges", "B is a leaf"],
        "A and B are already connected through A–D–B, so it would create a cycle"),

    mcq(r"""
How many edges does Kruskal's examine at most?
""", ["E (all of them)", "V − 1 exactly", "log E", "V²"], "E (all of them)"),

    mcq(r"""
What does this print?

```dart
typedef Edge = ({int u, int v, int w});

void main() {
  final Edge e = (u: 1, v: 2, w: 9);
  print('${e.u}-${e.v}:${e.w}');
}
```
""", ["1-2:9", "(1, 2, 9)", "u-v:w", "It doesn't compile"], "1-2:9"),

    mcq(r"""
What is the total weight of the MST of a triangle with edge weights 1, 2 and 3?
""", ["3", "6", "5", "1"], "3"),

    mcq(r"""
In a graph where all edges have weight 1, what is the MST's total weight for V vertices?
""", ["V − 1", "V", "E", "1"], "V − 1"),

    mcq(r"""
What does an MST give for the traveling salesman problem?
""", ["A basis for a tour at most twice the optimal length", "The exact optimal tour",
       "Nothing useful", "The shortest edge only"],
        "A basis for a tour at most twice the optimal length"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final pq = SplayTreeSet<(int, String)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    return c != 0 ? c : a.$2.compareTo(b.$2);
  });
  pq.addAll([(4, 'AB'), (1, 'AC'), (3, 'AD')]);
  print(pq.first.$2);
}
```
""", ["AC", "AB", "AD", "It throws an error"], "AC"),

    mcq(r"""
Which statement about MSTs and cycles is true?
""", ["Adding any non-tree edge to an MST creates exactly one cycle",
       "MSTs contain exactly one cycle", "Removing an MST edge creates a cycle",
       "MSTs have V cycles"], "Adding any non-tree edge to an MST creates exactly one cycle"),

    mcq(r"""
Removing any single edge from a spanning tree results in:
""", ["Two disconnected components", "A cycle", "A smaller spanning tree", "No change"],
        "Two disconnected components"),

    mcq(r"""
Which property does every edge in an MST have (with distinct weights)?
""", ["It's the cheapest edge crossing some cut", "It's the heaviest edge in the graph",
       "It touches the start vertex", "It has weight 1"],
        "It's the cheapest edge crossing some cut"),

    mcq(r"""
What does this print?

```dart
""" + KRUSKAL + r"""
void main() {
  print(kruskal(1, []));
}
```
""", ["0", "null", "1", "It throws an error"], "0"),

    mcq(r"""
Which of these algorithms is NOT used to compute an MST?
""", ["Dijkstra's algorithm", "Kruskal's algorithm", "Prim's algorithm", "Borůvka's algorithm"],
        "Dijkstra's algorithm"),

    mcq(r"""
In Prim's algorithm, what is the starting vertex's effect on the MST's total weight?
""", ["None: any start gives the same total weight", "It changes the total weight",
       "It must be the vertex with the most edges", "It must be vertex 0"],
        "None: any start gives the same total weight"),

    fill(r"""
Sort edge records by their third field (the weight):

```dart
void main() {
  final edges = [(0, 1, 5), (1, 2, 2)];
  edges.sort((a, b) => a.%fill%.compareTo(b.$3));
  print(edges.first); // (1, 2, 2)
}
```
""", "$3"),

    mcq(r"""
What does this print?

```dart
""" + KRUSKAL + r"""
void main() {
  final edges = [(0, 1, 2), (0, 1, 1), (1, 2, 3)];
  print(kruskal(3, edges));
}
```
""", ["4", "5", "6", "3"], "4"),

    mcq(r"""
What happens to parallel edges (two edges between the same vertices) in Kruskal's?
""", ["Only the cheaper one is used; the other would form a cycle", "Both are used",
       "It crashes", "The heavier one is preferred"],
        "Only the cheaper one is used; the other would form a cycle"),

    mcq(r"""
Which strategy does Borůvka's algorithm use?
""", ["Each component adds its cheapest outgoing edge in rounds", "Sorting all edges once",
       "Growing a single tree", "Removing heaviest edges first"],
        "Each component adds its cheapest outgoing edge in rounds"),
]
