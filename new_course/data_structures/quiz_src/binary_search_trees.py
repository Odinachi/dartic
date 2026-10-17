BST = r"""class Node {
  int value;
  Node? left, right;
  Node(this.value);
}

Node? insert(Node? n, int v) {
  if (n == null) return Node(v);
  if (v < n.value) {
    n.left = insert(n.left, v);
  } else if (v > n.value) {
    n.right = insert(n.right, v);
  }
  return n;
}

List<int> inOrder(Node? n) =>
    n == null ? [] : [...inOrder(n.left), n.value, ...inOrder(n.right)];
"""

PIC = r"""```dart
//          8
//        /   \
//       3     10
//      / \      \
//     1   6      14
//        / \    /
//       4   7  13
```"""

QUESTIONS = [
    mcq(r"""
What is the binary search tree property?
""", ["For every node, the left subtree is smaller and the right subtree is larger",
       "Each node is larger than its parent", "The tree is always balanced",
       "Every node has exactly two children"],
        "For every node, the left subtree is smaller and the right subtree is larger"),

    mcq(r"""
Which traversal of a BST visits values in sorted order?
""", ["In-order", "Pre-order", "Post-order", "Level-order"], "In-order"),

    mcq(r"""
What is the cost of searching a BST of height h?
""", ["O(h)", "O(n²)", "O(1)", "O(n log n)"], "O(h)"),

    mcq(r"""
What is the height of a balanced BST with n nodes?
""", ["About log₂ n", "About n", "About √n", "Exactly 1"], "About log₂ n"),

    mcq(r"""
Searching for 7 in this BST, which nodes are visited?

""" + PIC, ["8, 3, 6, 7", "8, 10, 14, 13, 7", "1, 3, 4, 6, 7", "8, 3, 1, 6, 7"], "8, 3, 6, 7"),

    mcq(r"""
What is the minimum value in this BST and how do you find it?

""" + PIC, ["1, by following left children from the root", "1, by in-order traversal only",
                "14, by following right children", "8, the root"],
        "1, by following left children from the root"),

    mcq(r"""
What is the in-order successor of 8 in this BST?

""" + PIC, ["10", "7", "13", "14"], "10"),

    mcq(r"""
What is the in-order successor of 7 in this BST?

""" + PIC, ["8", "6", "10", "None"], "8"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
void main() {
  Node? root;
  for (final v in [5, 2, 8, 1, 9, 3]) {
    root = insert(root, v);
  }
  print(inOrder(root));
}
```
""", ["[1, 2, 3, 5, 8, 9]", "[5, 2, 8, 1, 9, 3]", "[5, 2, 1, 3, 8, 9]", "[9, 8, 5, 3, 2, 1]"],
        "[1, 2, 3, 5, 8, 9]"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
void main() {
  Node? root;
  for (final v in [5, 2, 8]) {
    root = insert(root, v);
  }
  print(root!.left!.value);
  print(root.right!.value);
}
```
""", ["2 then 8", "8 then 2", "5 then 8", "2 then 5"], "2 then 8"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
void main() {
  Node? root;
  for (final v in [4, 4, 4, 2]) {
    root = insert(root, v);
  }
  print(inOrder(root));
}
```
""", ["[2, 4]", "[2, 4, 4, 4]", "[4, 4, 4, 2]", "[4, 2]"], "[2, 4]"),

    mcq(r"""
Why must you write `n.left = insert(n.left, v);` instead of just `insert(n.left, v);`?
""", ["The recursive call returns the (possibly new) subtree root, which must be reattached",
       "Dart requires assignments for recursion", "To sort the tree",
       "It doesn't matter; both work"],
        "The recursive call returns the (possibly new) subtree root, which must be reattached"),

    order(r"""
Complete the iterative BST search:

```dart
bool contains(Node? n, int t) {
  while (n %order% null) {
    if (t == n.value) return true;
    n = t %order% n.value ? n.left : n.%order%;
  }
  return false;
}
```
""", ["!=", "<", "right", "==", ">", "left"], ["!=", "<", "right"]),

    mcq(r"""
How do you delete a leaf from a BST?
""", ["Simply remove it (its parent's link becomes null)", "Replace it with its successor",
       "Rebuild the whole tree", "Swap it with the root"],
        "Simply remove it (its parent's link becomes null)"),

    mcq(r"""
How do you delete a BST node with exactly one child?
""", ["Replace the node with its only child", "Replace it with its successor",
       "Delete both the node and its child", "It can't be deleted"],
        "Replace the node with its only child"),

    mcq(r"""
How do you delete a BST node with two children?
""", ["Replace its value with its in-order successor, then delete the successor",
       "Delete the whole subtree", "Replace it with its left child only",
       "Swap it with a random leaf"],
        "Replace its value with its in-order successor, then delete the successor"),

    mcq(r"""
What is the in-order successor of a node with a right subtree?
""", ["The leftmost (smallest) node in its right subtree", "Its right child always",
       "Its parent", "The rightmost node in its left subtree"],
        "The leftmost (smallest) node in its right subtree"),

    mcq(r"""
Why does the in-order successor never have two children when used for deletion?
""", ["It's the leftmost node of a subtree, so it has no left child",
       "Successors are always leaves", "Because BSTs don't allow two children",
       "It always has two children"],
        "It's the leftmost node of a subtree, so it has no left child"),

    mcq(r"""
Which node can replace a deleted two-child node instead of the successor?
""", ["The in-order predecessor (largest in the left subtree)", "The root",
       "Any leaf", "The parent"], "The in-order predecessor (largest in the left subtree)"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
Node? delete(Node? n, int v) {
  if (n == null) return null;
  if (v < n.value) {
    n.left = delete(n.left, v);
  } else if (v > n.value) {
    n.right = delete(n.right, v);
  } else {
    if (n.left == null) return n.right;
    if (n.right == null) return n.left;
    var s = n.right!;
    while (s.left != null) {
      s = s.left!;
    }
    n.value = s.value;
    n.right = delete(n.right, s.value);
  }
  return n;
}

void main() {
  Node? root;
  for (final v in [50, 30, 70, 60, 80]) {
    root = insert(root, v);
  }
  root = delete(root, 50);
  print(root!.value);
  print(inOrder(root));
}
```
""", ["60 then [30, 60, 70, 80]", "70 then [30, 60, 70, 80]", "30 then [30, 60, 70, 80]",
       "60 then [30, 50, 70, 80]"], "60 then [30, 60, 70, 80]"),

    mcq(r"""
What is wrong with validating a BST by only checking each node against its direct children?
""", ["A deeper descendant can violate an ancestor's bound and go unnoticed",
       "It's too slow", "It rejects valid trees", "Nothing; it's correct"],
        "A deeper descendant can violate an ancestor's bound and go unnoticed"),

    mcq(r"""
Is this a valid BST?

```dart
//      10
//     /  \
//    5    15
//        /  \
//       6    20
```
""", ["No: 6 is in 10's right subtree but smaller than 10", "Yes", "No: 20 is too big",
       "No: 5 should be on the right"], "No: 6 is in 10's right subtree but smaller than 10"),

    mcq(r"""
How does the range-based BST validator update bounds when going LEFT?
""", ["The node's value becomes the new maximum", "The node's value becomes the new minimum",
       "Bounds reset to null", "Bounds don't change"],
        "The node's value becomes the new maximum"),

    mcq(r"""
What does this print?

```dart
class N {
  final int v;
  final N? left, right;
  const N(this.v, [this.left, this.right]);
}

bool isBst(N? n, [int? min, int? max]) {
  if (n == null) return true;
  if ((min != null && n.v <= min) || (max != null && n.v >= max)) return false;
  return isBst(n.left, min, n.v) && isBst(n.right, n.v, max);
}

void main() {
  print(isBst(const N(5, N(3, N(1), N(4)), N(8))));
  print(isBst(const N(5, N(3, N(1), N(6)), N(8))));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Another way to validate a BST is to check that its in-order traversal is:
""", ["Strictly increasing", "Strictly decreasing", "Balanced", "Of even length"],
        "Strictly increasing"),

    mcq(r"""
What happens when you insert 1, 2, 3, ..., n in order into a plain BST?
""", ["It becomes a degenerate tree (like a linked list) with height n - 1",
       "It stays perfectly balanced", "It throws an error", "Only the first value is stored"],
        "It becomes a degenerate tree (like a linked list) with height n - 1"),

    mcq(r"""
What is the worst-case cost of search in an unbalanced BST?
""", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "O(n)"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
int height(Node? n) {
  if (n == null) return -1;
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  Node? a, b;
  for (final v in [1, 2, 3, 4, 5, 6, 7]) {
    a = insert(a, v);
  }
  for (final v in [4, 2, 6, 1, 3, 5, 7]) {
    b = insert(b, v);
  }
  print('${height(a)} ${height(b)}');
}
```
""", ["6 2", "2 6", "7 3", "3 3"], "6 2"),

    mcq(r"""
What keeps a BST's height O(log n) regardless of insertion order?
""", ["Self-balancing (e.g. AVL, red-black or splay trees)", "Inserting duplicates",
       "Using in-order traversal", "Storing keys as strings"],
        "Self-balancing (e.g. AVL, red-black or splay trees)"),

    mcq(r"""
What does `floor(x)` return in a BST?
""", ["The largest value ≤ x", "The smallest value ≥ x", "The value closest to the root",
       "The minimum value"], "The largest value ≤ x"),

    mcq(r"""
What does `ceiling(x)` return in a BST?
""", ["The smallest value ≥ x", "The largest value ≤ x", "The maximum value", "x rounded up"],
        "The smallest value ≥ x"),

    mcq(r"""
In this BST, what is floor(5)?

""" + PIC, ["4", "6", "3", "5"], "4"),

    mcq(r"""
In this BST, what is ceiling(11)?

""" + PIC, ["13", "10", "14", "11"], "13"),

    mcq(r"""
In this BST, what is the lowest common ancestor of 4 and 7?

""" + PIC, ["6", "3", "8", "4"], "6"),

    mcq(r"""
In this BST, what is the lowest common ancestor of 1 and 13?

""" + PIC, ["8", "3", "10", "1"], "8"),

    mcq(r"""
How is the LCA found in a BST?
""", ["Walk down until a and b fall on different sides (or one equals the node)",
       "Find both nodes and compare depths only", "Use level-order traversal",
       "It's always the root"],
        "Walk down until a and b fall on different sides (or one equals the node)"),

    mcq(r"""
What does this print?

```dart
class N {
  final int v;
  final N? left, right;
  const N(this.v, [this.left, this.right]);
}

void range(N? n, int lo, int hi, List<int> out) {
  if (n == null) return;
  if (n.v > lo) range(n.left, lo, hi, out);
  if (n.v >= lo && n.v <= hi) out.add(n.v);
  if (n.v < hi) range(n.right, lo, hi, out);
}

void main() {
  final out = <int>[];
  range(const N(8, N(3, N(1), N(6)), N(10, null, N(14))), 2, 9, out);
  print(out);
}
```
""", ["[3, 6, 8]", "[1, 3, 6, 8, 10]", "[8, 3, 6]", "[3, 6]"], "[3, 6, 8]"),

    mcq(r"""
Why is a BST range query faster than scanning everything?
""", ["It skips subtrees that can't contain values in the range", "It sorts first",
       "It uses hashing", "It visits only leaves"],
        "It skips subtrees that can't contain values in the range"),

    mcq(r"""
What does `K extends Comparable<K>` mean in `BinarySearchTree<K extends Comparable<K>, V>`?
""", ["Keys must support compareTo so they can be ordered", "Keys must be ints",
       "Keys must be strings", "Keys are compared with =="],
        "Keys must support compareTo so they can be ordered"),

    mcq(r"""
What does `a.compareTo(b)` return when a < b?
""", ["A negative number", "A positive number", "0", "true"], "A negative number"),

    mcq(r"""
What does a function marked `sync*` do?
""", ["It's a generator that lazily yields values as an Iterable", "It runs synchronously in an isolate",
       "It returns a Future", "It locks a mutex"],
        "It's a generator that lazily yields values as an Iterable"),

    fill(r"""
Produce the next value from a generator:

```dart
Iterable<int> countTo(int n) sync* {
  for (var i = 1; i <= n; i++) {
    %fill% i;
  }
}

void main() {
  print(countTo(3).toList()); // [1, 2, 3]
}
```
""", "yield"),

    mcq(r"""
Which Dart class is a self-balancing BST you can use directly?
""", ["SplayTreeMap", "HashMap", "LinkedHashMap", "ListQueue"], "SplayTreeMap"),

    mcq(r"""
When is a balanced BST a better choice than a hash map?
""", ["When you need sorted order, min/max or range queries along with fast updates",
       "When you only need exact-key lookups", "When keys can't be compared",
       "Never; hash maps are always better"],
        "When you need sorted order, min/max or range queries along with fast updates"),

    mcq(r"""
What is the cost of inserting into a sorted List vs a balanced BST?
""", ["Sorted list O(n) (shifting), balanced BST O(log n)", "Both O(1)",
       "Sorted list O(log n), BST O(n)", "Both O(n²)"],
        "Sorted list O(n) (shifting), balanced BST O(log n)"),

    mcq(r"""
How do you build a balanced BST from a sorted list?
""", ["Use the middle element as the root and recurse on each half",
       "Insert elements in order", "Insert elements in reverse order",
       "Insert every other element first"],
        "Use the middle element as the root and recurse on each half"),

    mcq(r"""
What does this print?

```dart
class N {
  final int v;
  final N? left, right;
  const N(this.v, [this.left, this.right]);
}

N? build(List<int> a, int lo, int hi) {
  if (lo > hi) return null;
  final mid = (lo + hi) ~/ 2;
  return N(a[mid], build(a, lo, mid - 1), build(a, mid + 1, hi));
}

void main() {
  final root = build([1, 2, 3, 4, 5, 6, 7], 0, 6)!;
  print('${root.v} ${root.left!.v} ${root.right!.v}');
}
```
""", ["4 2 6", "1 2 3", "4 3 5", "7 6 5"], "4 2 6"),

    mcq(r"""
In a BST of distinct keys, what is the in-order predecessor of a node with a left subtree?
""", ["The rightmost node in its left subtree", "Its left child always",
       "Its parent", "The leftmost node in its right subtree"],
        "The rightmost node in its left subtree"),

    mcq(r"""
What does this print?

```dart
""" + BST + r"""
int? minValue(Node? n) {
  if (n == null) return null;
  while (n!.left != null) {
    n = n.left;
  }
  return n.value;
}

void main() {
  Node? root;
  for (final v in [20, 10, 30, 5, 15]) {
    root = insert(root, v);
  }
  print(minValue(root));
}
```
""", ["5", "10", "20", "15"], "5"),

    mcq(r"""
Which statement about duplicate keys in a BST is true?
""", ["You must choose a consistent rule: ignore, count, or always send them to one side",
       "BSTs can never store duplicates", "Duplicates are always stored on the left",
       "Duplicates make the BST unbalanced automatically"],
        "You must choose a consistent rule: ignore, count, or always send them to one side"),

    mcq(r"""
What is the cost of iterating all n keys of a BST in sorted order?
""", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
Inserting 1,000 values in random order into a plain BST typically gives a height of about:
""", ["20", "999", "1", "500"], "20"),

    mcq(r"""
What does this print?

```dart
class N {
  final int v;
  final N? left, right;
  const N(this.v, [this.left, this.right]);
}

int? ceil(N? n, int x) {
  int? best;
  while (n != null) {
    if (n.v == x) return x;
    if (n.v > x) {
      best = n.v;
      n = n.left;
    } else {
      n = n.right;
    }
  }
  return best;
}

void main() {
  const t = N(8, N(3, N(1), N(6)), N(10, null, N(14)));
  print(ceil(t, 7));
  print(ceil(t, 15));
}
```
""", ["8 then null", "6 then 14", "10 then null", "8 then 14"], "8 then null"),

    mcq(r"""
Which operation has the same cost in a balanced and a degenerate BST?
""", ["Iterating all keys in sorted order (O(n))", "Search", "Insert", "Delete"],
        "Iterating all keys in sorted order (O(n))"),
]
