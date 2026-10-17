NODE = r"""import 'dart:collection';

class Node {
  final int v;
  final Node? left, right;
  const Node(this.v, [this.left, this.right]);
}
"""

PIC = r"""```dart
//        1
//       / \
//      2   3
//     / \   \
//    4   5   6
//       /
//      7
```"""

QUESTIONS = [
    mcq(r"""
What order does level-order traversal visit nodes in?
""", ["Level by level, left to right within each level", "Left subtree, node, right subtree",
       "Deepest nodes first", "Random order"],
        "Level by level, left to right within each level"),

    mcq(r"""
Which data structure drives level-order traversal?
""", ["A queue", "A stack", "A hash set", "A sorted list"], "A queue"),

    mcq(r"""
What is another name for level-order traversal of a tree?
""", ["Breadth-first search (BFS)", "Depth-first search (DFS)", "In-order traversal",
       "Binary search"], "Breadth-first search (BFS)"),

    mcq(r"""
What is the level-order traversal of this tree?

""" + PIC, ["1 2 3 4 5 6 7", "1 2 4 5 7 3 6", "4 2 7 5 1 3 6", "7 4 5 6 2 3 1"],
        "1 2 3 4 5 6 7"),

    mcq(r"""
What is the pre-order traversal of this tree?

""" + PIC, ["1 2 4 5 7 3 6", "1 2 3 4 5 6 7", "4 2 7 5 1 3 6", "1 3 6 2 5 7 4"],
        "1 2 4 5 7 3 6"),

    mcq(r"""
Grouped by level, what are this tree's levels?

""" + PIC, ["[[1], [2, 3], [4, 5, 6], [7]]", "[[1], [2, 3, 4], [5, 6, 7]]",
                "[[1, 2], [3, 4], [5, 6], [7]]", "[[1], [2], [3], [4], [5], [6], [7]]"],
        "[[1], [2, 3], [4, 5, 6], [7]]"),

    mcq(r"""
What is the right side view of this tree?

""" + PIC, ["[1, 3, 6, 7]", "[1, 3, 6]", "[1, 2, 4, 7]", "[1, 3, 5, 7]"], "[1, 3, 6, 7]"),

    mcq(r"""
What is the minimum depth (counting nodes) of this tree?

""" + PIC, ["3", "2", "4", "1"], "3"),

    mcq(r"""
Why does level-order visit all of level d before any of level d + 1?
""", ["Children are added to the back of the queue, behind the rest of the current level",
       "Nodes are sorted by depth first", "The queue is a stack", "Recursion forces it"],
        "Children are added to the back of the queue, behind the rest of the current level"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<int> bfs(Node? root) {
  final out = <int>[];
  if (root == null) return out;
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final n = q.removeFirst();
    out.add(n.v);
    if (n.left != null) q.add(n.left!);
    if (n.right != null) q.add(n.right!);
  }
  return out;
}

void main() {
  print(bfs(const Node(1, Node(2, Node(4)), Node(3, Node(5)))));
}
```
""", ["[1, 2, 3, 4, 5]", "[1, 2, 4, 3, 5]", "[4, 2, 1, 5, 3]", "[1, 3, 2, 5, 4]"],
        "[1, 2, 3, 4, 5]"),

    mcq(r"""
What happens if you replace the queue in level-order traversal with a stack (and push right before left)?
""", ["It becomes a depth-first pre-order traversal", "It stays level-order",
       "It becomes in-order", "It visits only leaves"],
        "It becomes a depth-first pre-order traversal"),

    mcq(r"""
How do you know where one level ends during BFS?
""", ["Record the queue's length at the start of the level and process that many nodes",
       "Check whether a node is a leaf", "Wait until the queue is empty", "Use recursion"],
        "Record the queue's length at the start of the level and process that many nodes"),

    mcq(r"""
Why must the level size be saved BEFORE the inner loop?
""", ["Children added during the loop would otherwise change queue.length",
       "Queue.length is O(n)", "Dart can't read length in a loop", "It doesn't matter"],
        "Children added during the loop would otherwise change queue.length"),

    order(r"""
Complete the level grouping:

```dart
while (q.isNotEmpty) {
  final size = q.%order%;
  final level = <int>[];
  for (var i = 0; i < %order%; i++) {
    final n = q.%order%();
    level.add(n.v);
  }
}
```
""", ["length", "size", "removeFirst", "removeLast", "first"], ["length", "size", "removeFirst"]),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<List<int>> levels(Node? root) {
  final res = <List<int>>[];
  if (root == null) return res;
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    final lvl = <int>[];
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      lvl.add(n.v);
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
    res.add(lvl);
  }
  return res;
}

void main() {
  print(levels(const Node(3, Node(9), Node(20, Node(15), Node(7)))));
}
```
""", ["[[3], [9, 20], [15, 7]]", "[[3, 9, 20], [15, 7]]", "[[3], [9], [20], [15, 7]]",
       "[3, 9, 20, 15, 7]"], "[[3], [9, 20], [15, 7]]"),

    mcq(r"""
Which node of each level forms the right side view?
""", ["The last node of the level", "The first node of the level",
       "The node with the largest value", "Only right children"],
        "The last node of the level"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<int> rightView(Node? root) {
  final view = <int>[];
  if (root == null) return view;
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      if (i == size - 1) view.add(n.v);
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
  }
  return view;
}

void main() {
  print(rightView(const Node(1, Node(2, Node(4)), Node(3))));
}
```
""", ["[1, 3, 4]", "[1, 3]", "[1, 2, 4]", "[3, 4]"], "[1, 3, 4]"),

    mcq(r"""
Why is node 4 visible in the right side view of `1(2(4), 3)` even though it's a left child?
""", ["It's the only node on its level", "Left children are always visible",
       "It has the largest value", "It's a leaf"], "It's the only node on its level"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<double> averages(Node root) {
  final out = <double>[];
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    var sum = 0;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      sum += n.v;
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
    out.add(sum / size);
  }
  return out;
}

void main() {
  print(averages(const Node(4, Node(2), Node(6, Node(5), Node(9)))));
}
```
""", ["[4.0, 4.0, 7.0]", "[4.0, 8.0, 14.0]", "[4, 4, 7]", "[4.0, 2.0, 6.0]"],
        "[4.0, 4.0, 7.0]"),

    mcq(r"""
Why can BFS find the minimum depth faster than DFS?
""", ["It reaches shallow nodes first and can stop at the first leaf",
       "It visits fewer nodes in every tree", "It uses less memory always",
       "It sorts the nodes"], "It reaches shallow nodes first and can stop at the first leaf"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int minDepth(Node? root) {
  if (root == null) return 0;
  final q = Queue<(Node, int)>()..add((root, 1));
  while (q.isNotEmpty) {
    final (n, d) = q.removeFirst();
    if (n.left == null && n.right == null) return d;
    if (n.left != null) q.add((n.left!, d + 1));
    if (n.right != null) q.add((n.right!, d + 1));
  }
  return 0;
}

void main() {
  print(minDepth(const Node(1, Node(2, Node(3, Node(4))), Node(5, Node(6)))));
}
```
""", ["3", "2", "4", "1"], "3"),

    mcq(r"""
In the minimum-depth BFS, what does each queue entry store?
""", ["A record of (node, depth)", "Only the node", "Only the depth", "A list of ancestors"],
        "A record of (node, depth)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final (name, level) = ('Ada', 2);
  print('${'-' * level}$name');
}
```
""", ["--Ada", "Ada--", "2Ada", "-Ada"], "--Ada"),

    mcq(r"""
In zigzag level order, how is the right-to-left order produced efficiently?
""", ["Insert values at the front of a deque on alternate levels",
       "Sort each level descending", "Run DFS instead", "Reverse the whole result at the end"],
        "Insert values at the front of a deque on alternate levels"),

    mcq(r"""
What is the zigzag level order of `1(2(4, 5), 3(6, 7))`?
""", ["[[1], [3, 2], [4, 5, 6, 7]]", "[[1], [2, 3], [7, 6, 5, 4]]",
       "[[1], [3, 2], [7, 6, 5, 4]]", "[[1], [2, 3], [4, 5, 6, 7]]"],
        "[[1], [3, 2], [4, 5, 6, 7]]"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final level = ListQueue<int>();
  for (final v in [4, 5, 6]) {
    level.addFirst(v);
  }
  print(level.toList());
}
```
""", ["[6, 5, 4]", "[4, 5, 6]", "[4, 6, 5]", "[5, 4, 6]"], "[6, 5, 4]"),

    mcq(r"""
How does level-order traversal work on a general (n-ary) tree?
""", ["Enqueue every child in order instead of just left and right",
       "It doesn't work on general trees", "Only enqueue the first child",
       "Use a stack instead"], "Enqueue every child in order instead of just left and right"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

class E {
  final String n;
  final List<E> reports;
  const E(this.n, [this.reports = const []]);
}

void main() {
  const ceo = E('A', [E('B', [E('D')]), E('C', [E('E'), E('F')])]);
  final q = Queue<E>()..add(ceo);
  final out = <String>[];
  while (q.isNotEmpty) {
    final e = q.removeFirst();
    out.add(e.n);
    q.addAll(e.reports);
  }
  print(out.join());
}
```
""", ["ABCDEF", "ABDCEF", "ADBECF", "FEDCBA"], "ABCDEF"),

    mcq(r"""
What does `prev?.next = n;` do when `prev` is null?
""", ["Nothing; the assignment is skipped", "Throws a null error",
       "Sets prev to n", "Sets n.next to null"], "Nothing; the assignment is skipped"),

    mcq(r"""
When connecting nodes on the same level with `next` pointers, what is the last node's `next`?
""", ["null", "The first node of the level", "The first node of the next level",
       "Its parent"], "null"),

    mcq(r"""
What is the extra space used by BFS on a tree?
""", ["O(w), where w is the maximum width of a level", "O(h), the height", "O(1)",
       "O(log n) always"], "O(w), where w is the maximum width of a level"),

    mcq(r"""
In a perfect binary tree with n nodes, roughly how many nodes are on the last level?
""", ["About n / 2", "About log n", "1", "About √n"], "About n / 2"),

    mcq(r"""
For a perfect binary tree, which traversal uses less memory?
""", ["DFS (O(log n)) vs BFS (O(n))", "BFS (O(log n)) vs DFS (O(n))", "Both O(1)",
       "They are always equal"], "DFS (O(log n)) vs BFS (O(n))"),

    mcq(r"""
For a very deep, narrow tree (like a linked list), which traversal uses less memory?
""", ["BFS: the queue stays tiny while DFS's stack grows with the height",
       "DFS: the stack stays tiny", "They're the same", "Neither works"],
        "BFS: the queue stays tiny while DFS's stack grows with the height"),

    mcq(r"""
Why is `List.removeAt(0)` a bad choice for the BFS queue?
""", ["It's O(n), making BFS O(n²)", "It removes the wrong element",
       "It doesn't exist on List", "It sorts the list"], "It's O(n), making BFS O(n²)"),

    mcq(r"""
What happens if you add a null root to the queue without checking?
""", ["Accessing its children causes a null error", "Nothing; BFS ignores it",
       "It prints null and stops", "Dart refuses to compile"],
        "Accessing its children causes a null error"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int maxWidth(Node? root) {
  if (root == null) return 0;
  final q = Queue<Node>()..add(root);
  var best = 0;
  while (q.isNotEmpty) {
    final size = q.length;
    if (size > best) best = size;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
  }
  return best;
}

void main() {
  print(maxWidth(const Node(1, Node(2, Node(4), Node(5)), Node(3, null, Node(6)))));
}
```
""", ["3", "2", "6", "4"], "3"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<int> levelMax(Node root) {
  final out = <int>[];
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    var best = q.first.v;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      if (n.v > best) best = n.v;
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
    out.add(best);
  }
  return out;
}

void main() {
  print(levelMax(const Node(1, Node(3, Node(5), Node(3)), Node(2, null, Node(9)))));
}
```
""", ["[1, 3, 9]", "[1, 2, 3]", "[9, 3, 1]", "[1, 3, 5]"], "[1, 3, 9]"),

    mcq(r"""
How do you produce bottom-up level order (deepest level first)?
""", ["Compute normal level order, then reverse the list of levels",
       "Use a stack instead of a queue", "Traverse right children first", "Use in-order"],
        "Compute normal level order, then reverse the list of levels"),

    mcq(r"""
In a complete binary tree, what's true about level order?
""", ["Once a missing child (gap) appears, no real node may follow",
       "Every node has two children", "The last level is always full",
       "All leaves are at the same depth"],
        "Once a missing child (gap) appears, no real node may follow"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
bool isComplete(Node? root) {
  final q = Queue<Node?>()..add(root);
  var gap = false;
  while (q.isNotEmpty) {
    final n = q.removeFirst();
    if (n == null) {
      gap = true;
    } else {
      if (gap) return false;
      q
        ..add(n.left)
        ..add(n.right);
    }
  }
  return true;
}

void main() {
  print(isComplete(const Node(1, Node(2), Node(3))));
  print(isComplete(const Node(1, null, Node(3))));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Which question is a better fit for BFS than DFS?
""", ["\"What is the shallowest leaf?\"", "\"List every root-to-leaf path\"",
       "\"Print a BST in sorted order\"", "\"Compute every subtree's size\""],
        "\"What is the shallowest leaf?\""),

    mcq(r"""
Which question is a better fit for DFS than BFS?
""", ["\"Print a BST in sorted order\"", "\"Average of each level\"",
       "\"Right side view\"", "\"Minimum depth\""], "\"Print a BST in sorted order\""),

    mcq(r"""
What is the time complexity of level-order traversal?
""", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "O(n)"),

    fill(r"""
Create a queue and add the root in one expression:

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>()%fill%add(1);
  print(q);
}
```
""", ".."),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>()..add(1);
  var count = 0;
  while (q.isNotEmpty) {
    final x = q.removeFirst();
    count++;
    if (x < 4) {
      q.add(x * 2);
      q.add(x * 2 + 1);
    }
  }
  print(count);
}
```
""", ["7", "4", "8", "15"], "7"),

    mcq(r"""
What does this print?

```dart
void main() {
  final levels = [[1], [2, 3], [4]];
  for (final (i, lvl) in levels.indexed) {
    if (i == 1) print(lvl);
  }
}
```
""", ["[2, 3]", "[1]", "1", "[4]"], "[2, 3]"),

    order(r"""
Complete the BFS enqueue step for a binary tree:

```dart
final n = q.%order%();
out.add(n.v);
if (n.%order% != null) q.add(n.left!);
if (n.%order% != null) q.add(n.right!);
```
""", ["removeFirst", "left", "right", "removeLast", "next"], ["removeFirst", "left", "right"]),

    mcq(r"""
Which real-world spread is most like BFS?
""", ["Ripples spreading outward in a pond", "Exploring one cave tunnel to its end first",
       "Reading a book page by page", "Stacking plates"],
        "Ripples spreading outward in a pond"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  const t = Node(1, Node(2), Node(3));
  final q = Queue<Node>()..add(t);
  final first = q.removeFirst();
  q
    ..add(first.left!)
    ..add(first.right!);
  print(q.map((n) => n.v).toList());
}
```
""", ["[2, 3]", "[3, 2]", "[1, 2, 3]", "[2]"], "[2, 3]"),

    mcq(r"""
In BFS, when is a node "discovered" vs "visited"?
""", ["Discovered when enqueued; visited when dequeued", "Both happen at the same time",
       "Visited first, discovered later", "Only leaves are discovered"],
        "Discovered when enqueued; visited when dequeued"),

    mcq(r"""
Do you need a `seen` set for BFS on a TREE (not a general graph)?
""", ["No, trees have no cycles and each node has one parent", "Yes, always",
       "Only for binary trees", "Only if values repeat"],
        "No, trees have no cycles and each node has one parent"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int countLeaves(Node? root) {
  if (root == null) return 0;
  final q = Queue<Node>()..add(root);
  var leaves = 0;
  while (q.isNotEmpty) {
    final n = q.removeFirst();
    if (n.left == null && n.right == null) leaves++;
    if (n.left != null) q.add(n.left!);
    if (n.right != null) q.add(n.right!);
  }
  return leaves;
}

void main() {
  print(countLeaves(const Node(1, Node(2, Node(4), Node(5)), Node(3))));
}
```
""", ["3", "2", "5", "4"], "3"),
]
