ROT = r"""class Node {
  int key;
  Node? left, right;
  Node(this.key, [this.left, this.right]);
}

Node rotateRight(Node y) {
  final x = y.left!;
  y.left = x.right;
  x.right = y;
  return x;
}

Node rotateLeft(Node x) {
  final y = x.right!;
  x.right = y.left;
  y.left = x;
  return y;
}
"""

QUESTIONS = [
    mcq(r"""
What does a self-balancing BST guarantee?
""", ["Height stays O(log n), so operations stay O(log n) regardless of insertion order",
       "Every node has exactly two children", "Keys are stored in a hash table",
       "Search is always O(1)"],
        "Height stays O(log n), so operations stay O(log n) regardless of insertion order"),

    mcq(r"""
What is a rotation?
""", ["A local O(1) restructuring of nodes that preserves BST order",
       "Reversing the whole tree", "Sorting the keys", "Swapping two leaf values"],
        "A local O(1) restructuring of nodes that preserves BST order"),

    mcq(r"""
What is the cost of a single rotation?
""", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "O(1)"),

    mcq(r"""
What does a rotation NOT change?
""", ["The in-order (sorted) sequence of keys", "The heights of nodes", "The root of the subtree",
       "Parent–child links"], "The in-order (sorted) sequence of keys"),

    mcq(r"""
In a right rotation at node y with left child x, what becomes the new subtree root?
""", ["x", "y", "x's left child", "y's right child"], "x"),

    mcq(r"""
In a right rotation at y (left child x), where does x's old right subtree go?
""", ["It becomes y's left subtree", "It becomes x's left subtree", "It's deleted",
       "It becomes y's right subtree"], "It becomes y's left subtree"),

    mcq(r"""
What does this print?

```dart
""" + ROT + r"""
void main() {
  final root = rotateRight(Node(3, Node(2, Node(1))));
  print('${root.key} ${root.left!.key} ${root.right!.key}');
}
```
""", ["2 1 3", "3 2 1", "1 2 3", "2 3 1"], "2 1 3"),

    mcq(r"""
What does this print?

```dart
""" + ROT + r"""
void main() {
  final root = rotateLeft(Node(1, null, Node(2, null, Node(3))));
  print('${root.key} ${root.left!.key} ${root.right!.key}');
}
```
""", ["2 1 3", "1 2 3", "3 2 1", "2 3 1"], "2 1 3"),

    mcq(r"""
What does this print?

```dart
""" + ROT + r"""
List<int> inOrder(Node? n) =>
    n == null ? [] : [...inOrder(n.left), n.key, ...inOrder(n.right)];

void main() {
  final t = Node(4, Node(2, Node(1), Node(3)), Node(5));
  final before = inOrder(t);
  final after = inOrder(rotateRight(t));
  print(before.toString() == after.toString());
}
```
""", ["true", "false", "It throws an error", "[1, 2, 3, 4, 5]"], "true"),

    order(r"""
Complete the left rotation:

```dart
Node rotateLeft(Node x) {
  final y = x.%order%!;
  x.right = y.%order%;
  y.left = %order%;
  return y;
}
```
""", ["right", "left", "x", "y", "null"], ["right", "left", "x"]),

    mcq(r"""
What is an AVL tree's balance factor?
""", ["height(left) − height(right)", "Number of left nodes − number of right nodes",
       "Depth of the deepest leaf", "Key of left child − key of right child"],
        "height(left) − height(right)"),

    mcq(r"""
Which balance factors are allowed at every AVL node?
""", ["-1, 0 or +1", "0 only", "-2 to +2", "Any value"], "-1, 0 or +1"),

    mcq(r"""
An AVL node has balance factor +2 and its left child has balance factor +1. Which case is it and what's the fix?
""", ["Left-Left: rotate right at the node", "Left-Right: rotate left then right",
       "Right-Right: rotate left", "Right-Left: rotate right then left"],
        "Left-Left: rotate right at the node"),

    mcq(r"""
An AVL node has balance factor −2 and its right child has balance factor −1. What's the fix?
""", ["Rotate left at the node", "Rotate right at the node", "Rotate right then left",
       "No rotation needed"], "Rotate left at the node"),

    mcq(r"""
An AVL node has balance factor +2 and its left child has balance factor −1. What's the fix?
""", ["Rotate the left child left, then rotate the node right", "Rotate the node right only",
       "Rotate the node left only", "Rotate the right child right"],
        "Rotate the left child left, then rotate the node right"),

    mcq(r"""
An AVL node has balance factor −2 and its right child has balance factor +1. What's the fix?
""", ["Rotate the right child right, then rotate the node left", "Rotate the node left only",
       "Rotate the node right only", "Rotate the left child left"],
        "Rotate the right child right, then rotate the node left"),

    mcq(r"""
Inserting 30, then 10, then 20 into an empty AVL tree creates which case?
""", ["Left-Right", "Left-Left", "Right-Right", "Right-Left"], "Left-Right"),

    mcq(r"""
Inserting 10, 20, 30 into an empty AVL tree creates which case, and what is the final root?
""", ["Right-Right, root 20", "Left-Left, root 20", "Right-Left, root 30", "No rotation, root 10"],
        "Right-Right, root 20"),

    mcq(r"""
Why does an AVL node store its height?
""", ["So balance factors can be computed in O(1)", "To sort the keys",
       "To count the nodes", "To store colors"], "So balance factors can be computed in O(1)"),

    mcq(r"""
After a rotation, which node's height must be updated first?
""", ["The node that moved down", "The node that moved up", "The root of the whole tree",
       "Every leaf"], "The node that moved down"),

    mcq(r"""
What is the worst-case height of an AVL tree with n nodes, approximately?
""", ["1.44 × log₂ n", "2 × log₂ n", "n − 1", "√n"], "1.44 × log₂ n"),

    mcq(r"""
When does AVL rebalancing happen during insertion?
""", ["On the way back up the insertion path", "Before descending", "Only at the root",
       "Once every 100 inserts"], "On the way back up the insertion path"),

    mcq(r"""
What does this print?

```dart
class N {
  final int key;
  N? left, right;
  int height = 0;
  N(this.key);
}

int h(N? n) => n?.height ?? -1;

void main() {
  final n = N(10)..left = N(5);
  n.height = 1 + (h(n.left) > h(n.right) ? h(n.left) : h(n.right));
  print(h(n.left) - h(n.right));
}
```
""", ["1", "0", "-1", "2"], "1"),

    mcq(r"""
What does `n?.height ?? -1` return when n is null?
""", ["-1", "0", "null", "It throws an error"], "-1"),

    mcq(r"""
Inserting 1, 2, 3, ..., 1000 in order into an AVL tree gives a height of about:
""", ["9 to 10", "999", "500", "1"], "9 to 10"),

    mcq(r"""
Which is a red-black tree rule?
""", ["A red node cannot have a red child", "Every node must be black",
       "Every leaf must be red", "Left children are always red"],
        "A red node cannot have a red child"),

    mcq(r"""
Which other red-black rule, combined with "no red-red", bounds the height?
""", ["Every root-to-null path has the same number of black nodes",
       "Every path has the same number of red nodes", "The tree is perfect",
       "Every node has two children"],
        "Every root-to-null path has the same number of black nodes"),

    mcq(r"""
What color is the root of a red-black tree?
""", ["Black", "Red", "Either", "It has no color"], "Black"),

    mcq(r"""
What color are the null (missing) children in a red-black tree considered to be?
""", ["Black", "Red", "No color", "Same as their parent"], "Black"),

    mcq(r"""
What is the maximum height of a red-black tree with n nodes?
""", ["About 2 × log₂(n + 1)", "About 1.44 × log₂ n", "n − 1", "log₂ n exactly"],
        "About 2 × log₂(n + 1)"),

    mcq(r"""
Why do red-black trees allow taller trees than AVL trees?
""", ["Their balance rule is more relaxed, which means fewer rotations",
       "They don't use rotations", "They store more keys per node", "They're unbalanced"],
        "Their balance rule is more relaxed, which means fewer rotations"),

    mcq(r"""
Which tends to have faster lookups, and which faster inserts?
""", ["AVL: faster lookups; red-black: fewer rotations on inserts/deletes",
       "Red-black: faster lookups; AVL: faster inserts", "They're identical",
       "Splay trees are fastest for both always"],
        "AVL: faster lookups; red-black: fewer rotations on inserts/deletes"),

    mcq(r"""
Which libraries commonly use red-black trees?
""", ["Java's TreeMap and C++'s std::map", "Dart's HashMap", "Python's dict", "JavaScript arrays"],
        "Java's TreeMap and C++'s std::map"),

    mcq(r"""
What does this print?

```dart
enum Color { red, black }

class R {
  final Color c;
  final R? left, right;
  const R(this.c, [this.left, this.right]);
}

int bh(R? n) {
  if (n == null) return 1;
  final l = bh(n.left), r = bh(n.right);
  if (l == -1 || r == -1 || l != r) return -1;
  return l + (n.c == Color.black ? 1 : 0);
}

void main() {
  print(bh(const R(Color.black, R(Color.red), R(Color.red))));
  print(bh(const R(Color.black, R(Color.black), null)));
}
```
""", ["2 then -1", "3 then 2", "2 then 2", "1 then -1"], "2 then -1"),

    mcq(r"""
Which balanced tree does Dart's `SplayTreeMap` use?
""", ["A splay tree", "An AVL tree", "A red-black tree", "A B-tree"], "A splay tree"),

    mcq(r"""
What does a splay tree do after accessing a key?
""", ["Rotates that node all the way up to the root", "Deletes it",
       "Moves it to a leaf", "Recolors it red"], "Rotates that node all the way up to the root"),

    mcq(r"""
What extra data does a splay tree node store for balancing?
""", ["Nothing", "Its height", "A color bit", "A parent count"], "Nothing"),

    mcq(r"""
What guarantee does a splay tree give?
""", ["O(log n) amortized per operation", "O(log n) worst case per operation",
       "O(1) for every operation", "O(n) for every operation"],
        "O(log n) amortized per operation"),

    mcq(r"""
Which access pattern makes splay trees especially fast?
""", ["Repeatedly accessing the same few \"hot\" keys", "Accessing keys in random order",
       "Never accessing any key", "Only deleting keys"],
        "Repeatedly accessing the same few \"hot\" keys"),

    mcq(r"""
Why do databases and file systems use B-trees?
""", ["Each node holds many keys and fits a disk page, keeping the tree very shallow",
       "They avoid comparisons", "They are binary", "They never need balancing"],
        "Each node holds many keys and fits a disk page, keeping the tree very shallow"),

    mcq(r"""
In a B-tree, where are all the leaves?
""", ["At the same depth", "At random depths", "Only on the left", "In a separate list"],
        "At the same depth"),

    mcq(r"""
What problem do balanced trees solve compared to plain BSTs?
""", ["Sorted or adversarial input can no longer create an O(n)-height tree",
       "They make hashing faster", "They remove the need for comparisons",
       "They allow duplicate keys"],
        "Sorted or adversarial input can no longer create an O(n)-height tree"),

    mcq(r"""
After a recursive insert that may rotate, why must you write `root = _insert(root, key)`?
""", ["The subtree's root may change after a rotation", "To count inserts",
       "Because Dart copies trees", "It isn't necessary"],
        "The subtree's root may change after a rotation"),

    mcq(r"""
What happens if you apply a single right rotation to a Left-Right shape?
""", ["The imbalance just moves to the other side", "It's fixed correctly",
       "The tree loses nodes", "It becomes a B-tree"],
        "The imbalance just moves to the other side"),

    mcq(r"""
For production Dart code needing a sorted map, what should you use?
""", ["SplayTreeMap from dart:collection", "A hand-written AVL tree",
       "A HashMap sorted after every insert", "A List with insert(0, x)"],
        "SplayTreeMap from dart:collection"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final s = SplayTreeSet<int>();
  for (var i = 10; i >= 1; i--) {
    s.add(i);
  }
  print(s.take(3).toList());
}
```
""", ["[1, 2, 3]", "[10, 9, 8]", "[1, 10, 2]", "[]"], "[1, 2, 3]"),

    mcq(r"""
Roughly how tall is a perfectly balanced binary tree with 1,000,000,000 keys?
""", ["About 30 levels", "About 1,000 levels", "About 1,000,000 levels", "About 3 levels"],
        "About 30 levels"),

    mcq(r"""
How many rotations at most does a red-black tree need per insert?
""", ["2", "log n", "n", "0"], "2"),

    mcq(r"""
Which statement about rotations and the BST property is true?
""", ["Rotations keep the BST property intact", "Rotations temporarily break it",
       "Rotations sort the tree", "Rotations only work on leaves"],
        "Rotations keep the BST property intact"),

    mcq(r"""
In a left rotation at x with right child y, which subtree switches parents?
""", ["y's left subtree becomes x's right subtree", "x's left subtree",
       "y's right subtree", "None"], "y's left subtree becomes x's right subtree"),

    fill(r"""
Declare an enum for node colors:

```dart
%fill% Color { red, black }

void main() {
  print(Color.red.name); // red
}
```
""", "enum"),

    mcq(r"""
What does this print?

```dart
enum Color { red, black }

void main() {
  print(Color.values.length);
  print(Color.black.index);
}
```
""", ["2 then 1", "2 then 0", "1 then 1", "3 then 2"], "2 then 1"),

    mcq(r"""
Which balanced tree is best described as "rebalances by moving recently used keys to the top"?
""", ["Splay tree", "AVL tree", "Red-black tree", "B-tree"], "Splay tree"),

    mcq(r"""
Which balanced tree is best described as "every node's subtrees differ in height by at most one"?
""", ["AVL tree", "Red-black tree", "Splay tree", "B-tree"], "AVL tree"),

    mcq(r"""
What does this print?

```dart
""" + ROT + r"""
int height(Node? n) {
  if (n == null) return -1;
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  final chain = Node(3, Node(2, Node(1)));
  print(height(chain));
  print(height(rotateRight(chain)));
}
```
""", ["2 then 1", "3 then 2", "2 then 2", "1 then 1"], "2 then 1"),
]
