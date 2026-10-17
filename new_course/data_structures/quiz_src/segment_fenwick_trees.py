FEN = r"""class Fenwick {
  final List<int> t;
  Fenwick(int n) : t = List.filled(n + 1, 0);

  void add(int i, int d) {
    for (i++; i < t.length; i += i & -i) {
      t[i] += d;
    }
  }

  int prefix(int i) {
    var s = 0;
    for (i++; i > 0; i -= i & -i) {
      s += t[i];
    }
    return s;
  }

  int range(int l, int r) => prefix(r) - (l > 0 ? prefix(l - 1) : 0);
}
"""

SEG = r"""class Seg {
  final int n;
  final List<int> tree;
  Seg(List<int> data)
      : n = data.length,
        tree = List.filled(2 * data.length, 0) {
    for (var i = 0; i < n; i++) {
      tree[n + i] = data[i];
    }
    for (var i = n - 1; i > 0; i--) {
      tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
  }

  void set(int i, int v) {
    var p = i + n;
    tree[p] = v;
    for (p ~/= 2; p >= 1; p ~/= 2) {
      tree[p] = tree[2 * p] + tree[2 * p + 1];
    }
  }

  int sum(int l, int r) { // [l, r)
    var s = 0;
    for (var lo = l + n, hi = r + n; lo < hi; lo ~/= 2, hi ~/= 2) {
      if (lo.isOdd) s += tree[lo++];
      if (hi.isOdd) s += tree[--hi];
    }
    return s;
  }
}
"""

QUESTIONS = [
    mcq(r"""
What problem do segment trees and Fenwick trees solve?
""", ["Fast range queries AND fast point updates on an array", "Sorting arrays",
       "Finding shortest paths", "Hashing strings"],
        "Fast range queries AND fast point updates on an array"),

    mcq(r"""
With plain prefix sums, what is the cost of updating one element?
""", ["O(n), because later prefixes must be rebuilt", "O(1)", "O(log n)", "O(n²)"],
        "O(n), because later prefixes must be rebuilt"),

    mcq(r"""
What is the cost of a range query and a point update in a segment tree?
""", ["O(log n) each", "O(1) each", "O(n) each", "O(n log n) each"], "O(log n) each"),

    mcq(r"""
What is the cost of building a segment tree from n elements?
""", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
What does each node of a sum segment tree store?
""", ["The sum of the array range it covers", "A single array element",
       "The index of its parent", "The number of leaves"],
        "The sum of the array range it covers"),

    mcq(r"""
In a segment tree query, what happens when a node's range is completely inside the query range?
""", ["Its stored value is used directly", "Both children are queried",
       "It contributes the identity value", "The query stops with an error"],
        "Its stored value is used directly"),

    mcq(r"""
In a segment tree query, what happens when a node's range doesn't overlap the query at all?
""", ["It contributes the identity value (e.g. 0 for sums)", "Its value is used",
       "Both children are queried", "The query restarts"],
        "It contributes the identity value (e.g. 0 for sums)"),

    mcq(r"""
In a segment tree query, what happens on partial overlap?
""", ["Query both children and combine the results", "Use the node's value",
       "Return the identity", "Skip the node"], "Query both children and combine the results"),

    mcq(r"""
How many array slots does a recursive (1-based) segment tree safely need for n elements?
""", ["4n", "n", "n + 1", "log n"], "4n"),

    mcq(r"""
In the iterative segment tree layout of size 2n, where are the leaves stored?
""", ["tree[n .. 2n − 1]", "tree[0 .. n − 1]", "tree[1 .. n]", "At random positions"],
        "tree[n .. 2n − 1]"),

    mcq(r"""
In a 1-based array tree, what are the children of node i?
""", ["2i and 2i + 1", "2i + 1 and 2i + 2", "i − 1 and i + 1", "i ~/ 2"], "2i and 2i + 1"),

    mcq(r"""
What does this print?

```dart
""" + SEG + r"""
void main() {
  final s = Seg([5, 8, 6, 3, 2, 7, 2, 6]);
  print(s.sum(0, 8));
  print(s.sum(2, 6));
}
```
""", ["39 then 18", "39 then 16", "38 then 18", "39 then 11"], "39 then 18"),

    mcq(r"""
What does this print?

```dart
""" + SEG + r"""
void main() {
  final s = Seg([1, 2, 3, 4]);
  s.set(0, 10);
  print(s.sum(0, 2));
  print(s.tree[1]);
}
```
""", ["12 then 19", "3 then 10", "12 then 10", "11 then 19"], "12 then 19"),

    mcq(r"""
What does `tree[1]` hold in an iterative sum segment tree?
""", ["The sum of the whole array", "The first element", "The last element", "Nothing"],
        "The sum of the whole array"),

    mcq(r"""
After a point update, which nodes must be recomputed?
""", ["The leaf and all its ancestors up to the root", "Every node", "Only the leaf",
       "Only the root"], "The leaf and all its ancestors up to the root"),

    mcq(r"""
Which operation can a segment tree aggregate?
""", ["Any associative operation like sum, min, max or gcd", "Only sums",
       "Only operations with an inverse", "Only string concatenation"],
        "Any associative operation like sum, min, max or gcd"),

    mcq(r"""
What identity value should a range-MIN segment tree use?
""", ["A very large number (like +∞)", "0", "1", "-1"], "A very large number (like +∞)"),

    mcq(r"""
What identity value should a range-MAX segment tree use?
""", ["A very small number (like −∞)", "0 always", "1", "A very large number"],
        "A very small number (like −∞)"),

    mcq(r"""
What identity value should a range-PRODUCT segment tree use?
""", ["1", "0", "-1", "∞"], "1"),

    mcq(r"""
What goes wrong with identity 0 in a min segment tree of positive values?
""", ["Queries that touch empty ranges return 0, which is smaller than every real value",
       "It throws", "Nothing", "It becomes a sum tree"],
        "Queries that touch empty ranges return 0, which is smaller than every real value"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  final temps = [21, 25, 19, 30];
  final n = temps.length;
  final t = List<int>.filled(2 * n, 0);
  for (var i = 0; i < n; i++) {
    t[n + i] = temps[i];
  }
  for (var i = n - 1; i > 0; i--) {
    t[i] = max(t[2 * i], t[2 * i + 1]);
  }
  print(t[1]);
}
```
""", ["30", "95", "21", "25"], "30"),

    mcq(r"""
What is a Fenwick tree also called?
""", ["Binary Indexed Tree (BIT)", "Binary Search Tree", "B-tree", "Splay tree"],
        "Binary Indexed Tree (BIT)"),

    mcq(r"""
What does `i & -i` compute?
""", ["The lowest set bit of i", "The highest set bit of i", "i squared", "−i"],
        "The lowest set bit of i"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(12 & -12);
  print(7 & -7);
  print(16 & -16);
}
```
""", ["4 then 1 then 16", "12 then 7 then 16", "8 then 1 then 16", "4 then 7 then 1"],
        "4 then 1 then 16"),

    mcq(r"""
Why does a Fenwick tree use 1-based indexing internally?
""", ["Index 0 has no lowest set bit, so the jumps wouldn't work", "Dart lists start at 1",
       "To save memory", "It doesn't; it's 0-based"],
        "Index 0 has no lowest set bit, so the jumps wouldn't work"),

    mcq(r"""
In a Fenwick update, how does the index move?
""", ["i += i & -i (up to larger ranges)", "i -= i & -i", "i ~/= 2", "i *= 2"],
        "i += i & -i (up to larger ranges)"),

    mcq(r"""
In a Fenwick prefix-sum query, how does the index move?
""", ["i -= i & -i (down to smaller ranges)", "i += i & -i", "i++", "i *= 2"],
        "i -= i & -i (down to smaller ranges)"),

    mcq(r"""
What does this print?

```dart
""" + FEN + r"""
void main() {
  final f = Fenwick(5);
  for (final (i, v) in [5, 2, 7, 1, 3].indexed) {
    f.add(i, v);
  }
  print(f.prefix(2));
  print(f.range(1, 3));
}
```
""", ["14 then 10", "7 then 10", "14 then 9", "18 then 10"], "14 then 10"),

    mcq(r"""
What does this print?

```dart
""" + FEN + r"""
void main() {
  final f = Fenwick(3);
  f.add(1, 5);
  f.add(1, 5);
  print(f.range(1, 1));
}
```
""", ["10", "5", "0", "15"], "10"),

    mcq(r"""
A Fenwick tree's `add(i, d)` is called twice with the same i and d. What does position i now hold?
""", ["The original value plus 2d, because add applies a delta", "Exactly d",
       "The original value", "2 times the original value"],
        "The original value plus 2d, because add applies a delta"),

    mcq(r"""
How do you SET position i to a new value in a Fenwick tree?
""", ["add(i, newValue − oldValue)", "add(i, newValue)", "Rebuild the tree", "It's impossible"],
        "add(i, newValue − oldValue)"),

    mcq(r"""
How is a range sum [l, r] computed with a Fenwick tree?
""", ["prefix(r) − prefix(l − 1)", "prefix(l) + prefix(r)", "prefix(r) only",
       "Scan from l to r"], "prefix(r) − prefix(l − 1)"),

    mcq(r"""
What memory does a Fenwick tree use for n elements?
""", ["n + 1 integers", "4n integers", "n² integers", "log n integers"], "n + 1 integers"),

    mcq(r"""
Which can a simple Fenwick tree NOT answer directly with point updates?
""", ["Range minimum queries", "Range sums", "Prefix sums", "Point updates"],
        "Range minimum queries"),

    mcq(r"""
Why can Fenwick trees answer range sums but not range mins via prefixes?
""", ["Sums can be subtracted (prefix(r) − prefix(l−1)); mins have no inverse",
       "Mins are slower to compute", "Fenwick trees can't store negative numbers",
       "They can answer both"],
        "Sums can be subtracted (prefix(r) − prefix(l−1)); mins have no inverse"),

    mcq(r"""
When should you prefer a Fenwick tree over a segment tree?
""", ["When you only need sums with updates and want tiny, fast code", "When you need range max",
       "When the array never changes", "Never"],
        "When you only need sums with updates and want tiny, fast code"),

    mcq(r"""
When should you prefer a segment tree over a Fenwick tree?
""", ["When you need min, max or other non-invertible operations", "Only for sums",
       "When memory must be n + 1", "Never"],
        "When you need min, max or other non-invertible operations"),

    mcq(r"""
How do you count "smaller elements to the right" with a Fenwick tree?
""", ["Scan right to left, query how many recorded values are smaller, then record the current value",
       "Sort the array first", "Use two pointers", "Compare every pair"],
        "Scan right to left, query how many recorded values are smaller, then record the current value"),

    mcq(r"""
What does this print?

```dart
""" + FEN + r"""
List<int> smallerRight(List<int> a) {
  final mx = a.reduce((x, y) => x > y ? x : y);
  final f = Fenwick(mx + 1);
  final res = List<int>.filled(a.length, 0);
  for (var i = a.length - 1; i >= 0; i--) {
    res[i] = a[i] > 0 ? f.prefix(a[i] - 1) : 0;
    f.add(a[i], 1);
  }
  return res;
}

void main() {
  print(smallerRight([3, 1, 2, 0]));
}
```
""", ["[3, 1, 1, 0]", "[0, 1, 1, 3]", "[2, 0, 1, 0]", "[3, 2, 1, 0]"], "[3, 1, 1, 0]"),

    mcq(r"""
What is coordinate compression?
""", ["Mapping large or sparse values to small ranks 0..n−1 before using them as indexes",
       "Compressing a file", "Removing duplicates", "Sorting coordinates by distance"],
        "Mapping large or sparse values to small ranks 0..n−1 before using them as indexes"),

    mcq(r"""
What does this print?

```dart
void main() {
  final values = [500, 10, 999999, 10];
  final sorted = values.toSet().toList()..sort();
  final rank = {for (final (i, v) in sorted.indexed) v: i};
  print(values.map((v) => rank[v]).toList());
}
```
""", ["[1, 0, 2, 0]", "[2, 0, 1, 0]", "[500, 10, 999999, 10]", "[0, 1, 2, 3]"], "[1, 0, 2, 0]"),

    mcq(r"""
What is lazy propagation in segment trees used for?
""", ["Applying range UPDATES (e.g. add v to [l, r]) in O(log n)", "Making queries slower",
       "Deleting nodes", "Sorting the leaves"],
        "Applying range UPDATES (e.g. add v to [l, r]) in O(log n)"),

    mcq(r"""
Which real-world feature fits a segment tree with range max?
""", ["\"Highest score among players #10 to #9,000\" with live score updates",
       "Undo history", "Spell checking", "Finding a word by prefix"],
        "\"Highest score among players #10 to #9,000\" with live score updates"),

    mcq(r"""
If the array NEVER changes and you only need range sums, what's simplest?
""", ["Plain prefix sums (O(1) queries)", "A segment tree", "A Fenwick tree", "A heap"],
        "Plain prefix sums (O(1) queries)"),

    mcq(r"""
In the iterative segment tree query over [l, r), why check `lo.isOdd`?
""", ["An odd left index is a right child, so it must be included before moving up",
       "To skip even numbers", "To detect negative indexes", "It's a style choice"],
        "An odd left index is a right child, so it must be included before moving up"),

    order(r"""
Complete the Fenwick prefix sum:

```dart
int prefix(int i) {
  var s = 0;
  for (i++; i %order% 0; i %order% i & -i) {
    s %order% t[i];
  }
  return s;
}
```
""", [">", "-=", "+=", "<", "*="], [">", "-=", "+="]),

    order(r"""
Complete the iterative segment tree build:

```dart
for (var i = n %order% 1; i > 0; i--) {
  tree[i] = tree[%order% * i] + tree[2 * i %order% 1];
}
```
""", ["-", "2", "+", "*", "4"], ["-", "2", "+"]),

    mcq(r"""
What does this print?

```dart
void main() {
  var i = 6;
  final visited = <int>[];
  while (i > 0) {
    visited.add(i);
    i -= i & -i;
  }
  print(visited);
}
```
""", ["[6, 4]", "[6, 5, 4]", "[6, 3]", "[6, 2]"], "[6, 4]"),

    mcq(r"""
What does this print?

```dart
void main() {
  var i = 3;
  final visited = <int>[];
  while (i <= 8) {
    visited.add(i);
    i += i & -i;
  }
  print(visited);
}
```
""", ["[3, 4, 8]", "[3, 5, 7]", "[3, 6, 8]", "[3, 4, 6, 8]"], "[3, 4, 8]"),

    mcq(r"""
In a Fenwick tree of size 8, which range does tree[6] (binary 110) cover?
""", ["Elements 5..6 (length 2)", "Elements 1..6", "Element 6 only", "Elements 1..8"],
        "Elements 5..6 (length 2)"),

    mcq(r"""
Which property makes an operation usable in a segment tree?
""", ["Associativity: (a ⊕ b) ⊕ c == a ⊕ (b ⊕ c)", "Commutativity only",
       "Having an inverse", "Being O(1) to undo"],
        "Associativity: (a ⊕ b) ⊕ c == a ⊕ (b ⊕ c)"),

    mcq(r"""
How many nodes does a segment tree query touch per level, at most?
""", ["About 4 (a small constant)", "All of them", "Exactly 1", "log n"],
        "About 4 (a small constant)"),

    mcq(r"""
What is a 2D Fenwick tree used for?
""", ["Rectangle sums with point updates on a grid", "Sorting 2D points",
       "Finding shortest paths on grids", "Rotating matrices"],
        "Rectangle sums with point updates on a grid"),

    fill(r"""
Isolate the lowest set bit of i:

```dart
void main() {
  const i = 10; // 0b1010
  print(i %fill% -i); // 2
}
```
""", "&"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  final f = max;
  print(f(3, 9));
}
```
""", ["9", "3", "12", "It doesn't compile"], "9"),
]
