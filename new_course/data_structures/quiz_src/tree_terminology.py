BN = r"""class N {
  final int v;
  final N? left, right;
  N(this.v, [this.left, this.right]);
}
"""

TREE_PIC = r"""```dart
//        A
//      / | \
//     B  C  D
//    / \     \
//   E   F     G
//            / \
//           H   I
```"""

QUESTIONS = [
    mcq(r"""
Which statement describes a tree?
""", ["One root, every other node has exactly one parent, and no cycles",
       "Every node has exactly two children", "Nodes connected in a single line",
       "Any set of nodes with edges, cycles allowed"],
        "One root, every other node has exactly one parent, and no cycles"),

    mcq(r"""
How many edges does a tree with n nodes have?
""", ["n - 1", "n", "n + 1", "2n"], "n - 1"),

    mcq(r"""
What is a leaf?
""", ["A node with no children", "The root node", "A node with exactly one child",
       "A node at depth 1"], "A node with no children"),

    mcq(r"""
What is the root?
""", ["The only node with no parent", "Any node with no children",
       "The node with the largest value", "The deepest node"], "The only node with no parent"),

    mcq(r"""
In this tree, which nodes are leaves?

""" + TREE_PIC, ["E, F, C, H, I", "A, B, D, G", "H and I only", "B, C, D"], "E, F, C, H, I"),

    mcq(r"""
In this tree, what is the depth of H?

""" + TREE_PIC, ["3", "2", "4", "0"], "3"),

    mcq(r"""
In this tree, what is the height of D?

""" + TREE_PIC, ["2", "1", "3", "0"], "2"),

    mcq(r"""
In this tree, what is the height of the whole tree?

""" + TREE_PIC, ["3", "2", "4", "9"], "3"),

    mcq(r"""
In this tree, which nodes are siblings of E?

""" + TREE_PIC, ["F", "C and D", "B", "H and I"], "F"),

    mcq(r"""
In this tree, which nodes are ancestors of H?

""" + TREE_PIC, ["G, D, A", "I", "B, E, F", "Only G"], "G, D, A"),

    mcq(r"""
In this tree, which nodes make up the subtree rooted at D?

""" + TREE_PIC, ["D, G, H, I", "D only", "G, H, I", "A, D"], "D, G, H, I"),

    mcq(r"""
What does depth measure?
""", ["Edges from the root down to the node", "Edges from the node down to its deepest leaf",
       "Number of children", "Number of siblings"], "Edges from the root down to the node"),

    mcq(r"""
What does height measure?
""", ["Edges on the longest path from the node down to a leaf", "Edges from the root to the node",
       "Number of nodes in the tree", "Number of leaves"],
        "Edges on the longest path from the node down to a leaf"),

    mcq(r"""
What is the depth of the root?
""", ["0", "1", "The tree's height", "-1"], "0"),

    mcq(r"""
What is the height of a leaf?
""", ["0", "1", "-1", "The tree's height"], "0"),

    mcq(r"""
In recursive code, how does depth usually flow?
""", ["Passed DOWN as a parameter (depth + 1)", "Returned UP from children",
       "Stored in a global variable only", "Computed by sorting"],
        "Passed DOWN as a parameter (depth + 1)"),

    mcq(r"""
In recursive code, how does height usually flow?
""", ["Returned UP: 1 + the max of the children's heights", "Passed DOWN as a parameter",
       "Read from the root's value", "Always equal to depth"],
        "Returned UP: 1 + the max of the children's heights"),

    mcq(r"""
What is a binary tree?
""", ["A tree where every node has at most two children", "A tree with exactly two levels",
       "A tree that stores only 0s and 1s", "A tree with two roots"],
        "A tree where every node has at most two children"),

    mcq(r"""
What does this print?

```dart
""" + BN + r"""
int size(N? n) => n == null ? 0 : 1 + size(n.left) + size(n.right);

void main() {
  print(size(N(1, N(2, N(4)), N(3))));
}
```
""", ["4", "3", "10", "2"], "4"),

    mcq(r"""
What does this print?

```dart
""" + BN + r"""
int height(N? n) {
  if (n == null) return -1;
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  print(height(N(1, N(2, N(4)), N(3))));
  print(height(N(7)));
}
```
""", ["2 then 0", "3 then 1", "2 then 1", "1 then 0"], "2 then 0"),

    mcq(r"""
Why does the lesson's binary `height` return -1 for null?
""", ["So that a leaf ends up with height 0", "Because null is negative",
       "To mark errors", "Dart requires it"], "So that a leaf ends up with height 0"),

    mcq(r"""
What does this print?

```dart
""" + BN + r"""
int sum(N? n) => n == null ? 0 : n.v + sum(n.left) + sum(n.right);

void main() {
  print(sum(N(5, N(3, null, N(1)), N(2))));
}
```
""", ["11", "10", "5", "8"], "11"),

    mcq(r"""
What is a full binary tree?
""", ["Every node has 0 or 2 children", "Every level is completely filled",
       "All leaves are at depth 1", "Every node has exactly one child"],
        "Every node has 0 or 2 children"),

    mcq(r"""
What is a complete binary tree?
""", ["All levels full except possibly the last, which fills left to right",
       "Every node has 2 children", "All leaves on different levels",
       "A tree with no leaves"],
        "All levels full except possibly the last, which fills left to right"),

    mcq(r"""
What is a perfect binary tree?
""", ["All internal nodes have 2 children and all leaves are at the same depth",
       "A tree with height 1", "A tree with only a root", "A tree sorted left to right"],
        "All internal nodes have 2 children and all leaves are at the same depth"),

    mcq(r"""
What is a balanced binary tree (height-balanced)?
""", ["At every node, left and right subtree heights differ by at most 1",
       "It has the same number of nodes on each side of the root",
       "All values are equal", "It has an even number of nodes"],
        "At every node, left and right subtree heights differ by at most 1"),

    mcq(r"""
What does a degenerate (skewed) binary tree behave like?
""", ["A linked list", "A hash table", "A heap", "A perfect tree"], "A linked list"),

    mcq(r"""
How many nodes does a perfect binary tree of height 3 have?
""", ["15", "8", "7", "16"], "15"),

    mcq(r"""
What is the approximate height of a balanced binary tree with 1,000,000 nodes?
""", ["About 20", "About 1,000", "About 500,000", "About 1,000,000"], "About 20"),

    mcq(r"""
What is the height of a degenerate binary tree with n nodes?
""", ["n - 1", "log₂ n", "1", "n / 2"], "n - 1"),

    mcq(r"""
Many tree operations cost O(height). Why do balanced trees matter?
""", ["They keep height around log n instead of n", "They use less memory per node",
       "They avoid recursion", "They sort values automatically"],
        "They keep height around log n instead of n"),

    mcq(r"""
What does this print?

```dart
""" + BN + r"""
bool isBalanced(N? root) => _check(root) != -1;

int _check(N? n) {
  if (n == null) return 0;
  final l = _check(n.left);
  if (l == -1) return -1;
  final r = _check(n.right);
  if (r == -1) return -1;
  if ((l - r).abs() > 1) return -1;
  return 1 + (l > r ? l : r);
}

void main() {
  print(isBalanced(N(1, N(2), N(3))));
  print(isBalanced(N(1, N(2, N(3)))));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Why is the bottom-up balance check O(n) rather than O(n²)?
""", ["Each node's height is computed once and reused by its parent",
       "It only checks the root", "It uses a hash map", "It stops after one level"],
        "Each node's height is computed once and reused by its parent"),

    mcq(r"""
What does this print?

```dart
class T {
  final String v;
  final List<T> kids;
  T(this.v, [this.kids = const []]);
}

int countLeaves(T n) =>
    n.kids.isEmpty ? 1 : n.kids.fold(0, (s, c) => s + countLeaves(c));

void main() {
  print(countLeaves(T('a', [T('b', [T('d'), T('e')]), T('c')])));
}
```
""", ["3", "5", "2", "4"], "3"),

    mcq(r"""
What does this print?

```dart
class T {
  final String v;
  final List<T> kids;
  T(this.v, [this.kids = const []]);
}

void show(T n, [int depth = 0]) {
  print('${'-' * depth}${n.v}');
  for (final k in n.kids) {
    show(k, depth + 1);
  }
}

void main() {
  show(T('a', [T('b', [T('c')])]));
}
```
""", ["a then -b then --c", "a then b then c", "--a then -b then c", "c then b then a"],
        "a then -b then --c"),

    mcq(r"""
Which is NOT naturally a tree?
""", ["A road network with loops between cities", "A file system", "A Flutter widget tree",
       "An HTML document"], "A road network with loops between cities"),

    mcq(r"""
In a JSON document, what are the leaves?
""", ["Primitive values like strings, numbers and booleans", "Maps", "Lists",
       "The top-level object"], "Primitive values like strings, numbers and booleans"),

    mcq(r"""
What does this print?

```dart
int countKeys(Object? node) {
  if (node is Map) {
    return node.length + node.values.fold<int>(0, (s, v) => s + countKeys(v));
  }
  if (node is List) return node.fold<int>(0, (s, v) => s + countKeys(v));
  return 0;
}

void main() {
  print(countKeys({'a': {'b': 1, 'c': 2}, 'd': [ {'e': 3} ]}));
}
```
""", ["5", "3", "4", "6"], "5"),

    mcq(r"""
What is the degree of a node?
""", ["The number of its children", "Its depth", "Its height", "Its value"],
        "The number of its children"),

    mcq(r"""
What is an internal node?
""", ["A node with at least one child", "A node with no children", "Only the root",
       "A node inside a cycle"], "A node with at least one child"),

    mcq(r"""
What is a level of a tree?
""", ["All nodes at the same depth", "All leaves", "A path from root to leaf",
       "All nodes with the same value"], "All nodes at the same depth"),

    mcq(r"""
What does this print?

```dart
""" + BN + r"""
int countAt(N? n, int d) {
  if (n == null) return 0;
  if (d == 0) return 1;
  return countAt(n.left, d - 1) + countAt(n.right, d - 1);
}

void main() {
  final t = N(1, N(2, N(4), N(5)), N(3, null, N(6)));
  print(countAt(t, 2));
}
```
""", ["3", "2", "6", "1"], "3"),

    mcq(r"""
What does this print?

```dart
class B {
  int v;
  B? left, right;
  B(this.v, [this.left, this.right]);
}

B? mirror(B? n) {
  if (n == null) return null;
  final tmp = n.left;
  n.left = mirror(n.right);
  n.right = mirror(tmp);
  return n;
}

void main() {
  final r = mirror(B(1, B(2, B(4)), B(3)))!;
  print('${r.left!.v} ${r.right!.v} ${r.right!.right!.v}');
}
```
""", ["3 2 4", "2 3 4", "3 2 null", "4 2 3"], "3 2 4"),

    mcq(r"""
What is the time complexity of visiting every node of a tree once?
""", ["O(n)", "O(log n)", "O(n²)", "O(height)"], "O(n)"),

    mcq(r"""
What is the extra space of a recursive traversal, due to the call stack?
""", ["O(height)", "O(1)", "O(n²)", "O(log n) always"], "O(height)"),

    fill(r"""
Check whether a general tree node is a leaf:

```dart
class TreeNode {
  final List<TreeNode> children = [];
  bool get isLeaf => children.%fill%;
}
```
""", "isEmpty"),

    order(r"""
Complete the recursive node count for a binary tree:

```dart
int size(N? n) => n %order% null ? 0 : 1 %order% size(n.left) + size(n.%order%);
```
""", ["==", "+", "right", "!=", "-", "left"], ["==", "+", "right"]),

    order(r"""
Complete the binary tree height:

```dart
int height(N? n) {
  if (n == null) return %order%;
  final l = height(n.left), r = height(n.right);
  return %order% + (l > r ? %order% : r);
}
```
""", ["-1", "1", "l", "0", "r", "2"], ["-1", "1", "l"]),

    mcq(r"""
Which Flutter concept is a tree?
""", ["The widget tree", "A Stream", "A Future", "A StatefulWidget's State object"],
        "The widget tree"),

    mcq(r"""
What does this print?

```dart
class W {
  final String t;
  final List<W> kids;
  const W(this.t, [this.kids = const []]);
}

int depthOf(W w, String target, [int d = 0]) {
  if (w.t == target) return d;
  for (final k in w.kids) {
    final r = depthOf(k, target, d + 1);
    if (r != -1) return r;
  }
  return -1;
}

void main() {
  const app = W('App', [W('Scaffold', [W('Body', [W('Text')])])]);
  print(depthOf(app, 'Text'));
}
```
""", ["3", "4", "2", "-1"], "3"),

    mcq(r"""
How many children can a node have in a general (n-ary) tree?
""", ["Any number", "At most 2", "Exactly 2", "At most 1"], "Any number"),

    mcq(r"""
Which tree shape do binary heaps always use?
""", ["Complete", "Degenerate", "Full only", "Unbalanced"], "Complete"),

    mcq(r"""
A tree has 10 nodes. How many edges does it have?
""", ["9", "10", "11", "20"], "9"),

    mcq(r"""
What problem can occur if you build a node class with a shared default children list and later add children to nodes?
""", ["Nodes may end up sharing one list, so children appear in the wrong places",
       "The tree becomes balanced", "Dart throws a compile error", "Nothing"],
        "Nodes may end up sharing one list, so children appear in the wrong places"),

    mcq(r"""
What does this print?

```dart
void main() {
  var perfectNodes = 0;
  for (var level = 0; level <= 4; level++) {
    perfectNodes += 1 << level;
  }
  print(perfectNodes);
}
```
""", ["31", "16", "32", "15"], "31"),
]
