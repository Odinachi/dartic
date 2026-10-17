# Tree Fundamentals

Imagine your **family tree** 🌳.

- At the top is a great-grandparent: the **root** of the family.
- Each person can have **children**, who can have children of their own.
- People with no children are the **leaves** at the bottom.
- Your **depth** is how many generations you are below the root.

Or think about the **folders** on your computer 📁: one top folder containing folders containing files.

👉 That's a **tree**:

> A **tree** is a hierarchy of **nodes** connected by **edges**. There is one **root**, every other node has exactly **one parent**, and there are **no cycles**.

Lists and queues are **linear**: one thing after another. Trees are **hierarchical**: one thing **above** several others. That shape makes searching, sorting, autocomplete and much more fast.

---

## 📖 Tree Vocabulary

```text
                 A          ← root (depth 0)
               / | \
              B  C  D       ← depth 1
             / \     \
            E   F     G     ← depth 2
                     / \
                    H   I   ← depth 3 (leaves)
```

| Term | Meaning | Example above |
|------|---------|---------------|
| **Node** | One element of the tree | `A`, `B`, ... `I` |
| **Root** | The top node, with no parent | `A` |
| **Edge** | A link between a parent and a child | `A–B` |
| **Parent** | The node directly above | `B` is the parent of `E` |
| **Child** | A node directly below | `E` and `F` are children of `B` |
| **Siblings** | Nodes with the same parent | `E` and `F` |
| **Leaf** | A node with no children | `E`, `F`, `C`, `H`, `I` |
| **Internal node** | A node with at least one child | `A`, `B`, `D`, `G` |
| **Ancestor** | Any node on the path up to the root | `A`, `D`, `G` are ancestors of `H` |
| **Descendant** | Any node below | `E`, `F` are descendants of `B` |
| **Subtree** | A node plus all its descendants | The subtree at `D` is `D, G, H, I` |
| **Depth** of a node | Edges from the root to it | depth(`H`) = 3 |
| **Height** of a node | Edges on the longest path down to a leaf | height(`D`) = 2 |
| **Height** of the tree | Height of the root | 3 |
| **Degree** | Number of children | degree(`A`) = 3 |
| **Level** | All nodes at the same depth | Level 1: `B, C, D` |

> 💡 A tree with **n** nodes always has exactly **n − 1** edges: every node except the root has one edge to its parent.

---

## 🧱 Representing a General Tree in Dart

```dart
class TreeNode<T> {
  final T value;
  final List<TreeNode<T>> children = [];

  TreeNode(this.value);

  TreeNode<T> add(T childValue) {
    final child = TreeNode(childValue);
    children.add(child);
    return child;
  }

  bool get isLeaf => children.isEmpty;
}

void main() {
  final a = TreeNode('A');
  final b = a.add('B');
  a.add('C');
  final d = a.add('D');
  b.add('E');
  b.add('F');
  final g = d.add('G');
  g.add('H');
  g.add('I');

  print(a.children.map((c) => c.value).toList()); // [B, C, D]
  print(b.isLeaf); // false
  print(g.children.first.isLeaf); // true (H)
}
```

**🔍 What This Code Does:**

1. **Each Node Owns Its Children**: A `List<TreeNode<T>>` holds any number of children (a general, or **n-ary**, tree).
2. **`add` Returns the Child**: So we can keep building beneath it.
3. **`isLeaf`**: A node with no children.
4. **Recursive Structure**: Every child is itself the root of a smaller tree, which is why recursion fits trees so well.

---

## 🔁 Recursion: The Natural Way to Process Trees

Almost every tree question has the same shape: **answer for the current node, combined with the answers from its subtrees**.

```dart
class TreeNode<T> {
  final T value;
  final List<TreeNode<T>> children;
  TreeNode(this.value, [List<TreeNode<T>>? children]) : children = children ?? [];
}

int countNodes(TreeNode node) =>
    1 + node.children.fold(0, (sum, c) => sum + countNodes(c));

int countLeaves(TreeNode node) => node.children.isEmpty
    ? 1
    : node.children.fold(0, (sum, c) => sum + countLeaves(c));

int height(TreeNode node) {
  if (node.children.isEmpty) return 0;
  var tallest = 0;
  for (final c in node.children) {
    final h = height(c);
    if (h > tallest) tallest = h;
  }
  return 1 + tallest;
}

void printTree(TreeNode node, [String indent = '']) {
  print('$indent${node.value}');
  for (final c in node.children) {
    printTree(c, '$indent  ');
  }
}

void main() {
  final tree = TreeNode('A', [
    TreeNode('B', [TreeNode('E'), TreeNode('F')]),
    TreeNode('C'),
    TreeNode('D', [
      TreeNode('G', [TreeNode('H'), TreeNode('I')]),
    ]),
  ]);

  print(countNodes(tree));  // 9
  print(countLeaves(tree)); // 5
  print(height(tree));      // 3
  printTree(tree);
}
```

**🔍 What This Code Does:**

1. **`countNodes`**: Me (1) plus the count of every subtree.
2. **`countLeaves`**: A leaf counts as 1; otherwise sum the leaves of the children.
3. **`height`**: A leaf has height 0; otherwise 1 + the tallest child's height.
4. **`printTree`**: Prints the node, then its children with more indentation (a **pre-order** traversal).
5. **O(n) Each**: Every node is visited exactly once.
6. **Initializer List**: `children = children ?? []` gives each node its own fresh list.

---

## 📏 Depth vs Height

People mix these up constantly, so let's compute both:

- **Depth** goes **down from the root**: pass it **into** the recursion.
- **Height** comes **up from the leaves**: get it **back** from the recursion.

```dart
class TreeNode {
  final String value;
  final List<TreeNode> children;
  TreeNode(this.value, [this.children = const []]);
}

void printDepths(TreeNode node, [int depth = 0]) {
  print('${node.value}: depth $depth');
  for (final c in node.children) {
    printDepths(c, depth + 1); // depth flows DOWN
  }
}

int heightOf(TreeNode node) => node.children.isEmpty
    ? 0
    : 1 + node.children.map(heightOf).reduce((a, b) => a > b ? a : b); // height flows UP

void main() {
  final tree = TreeNode('A', [
    TreeNode('B', [TreeNode('E')]),
    TreeNode('C'),
  ]);
  printDepths(tree);
  print('height(A) = ${heightOf(tree)}'); // 2
  print('height(C) = ${heightOf(tree.children[1])}'); // 0
}
```

**🔍 What This Code Does:**

1. **Depth Is a Parameter**: Each call passes `depth + 1` to its children.
2. **Height Is a Return Value**: Each call returns `1 + max(children's heights)`.
3. **Leaf Height = 0**: Leaves have no edges below them.
4. **Root Depth = 0**: The root has no edges above it.
5. **`map(heightOf)`**: A tear-off passes the function itself as the mapping.

---

## 🌲 Binary Trees

A **binary tree** is a tree where every node has **at most two** children, called **left** and **right**. Binary trees are the foundation for BSTs, heaps, expression trees and more.

```dart
class BinaryNode<T> {
  T value;
  BinaryNode<T>? left;
  BinaryNode<T>? right;
  BinaryNode(this.value, {this.left, this.right});
}

int size(BinaryNode? n) => n == null ? 0 : 1 + size(n.left) + size(n.right);

int height(BinaryNode? n) {
  if (n == null) return -1; // empty tree has height -1, so a leaf has height 0
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  //        1
  //       / \
  //      2   3
  //     / \    \
  //    4   5    6
  final root = BinaryNode(1,
      left: BinaryNode(2, left: BinaryNode(4), right: BinaryNode(5)),
      right: BinaryNode(3, right: BinaryNode(6)));

  print(size(root));   // 6
  print(height(root)); // 2
}
```

**🔍 What This Code Does:**

1. **Two Nullable Links**: `left` and `right` are `null` when a child is missing.
2. **Named Parameters**: `BinaryNode(2, left: ..., right: ...)` makes construction readable.
3. **Null as the Base Case**: An empty subtree has size 0 and height −1, which makes leaves come out to height 0.
4. **Recursion on Both Sides**: Every binary tree algorithm looks at `left` and `right`.

---

## 🧩 Shapes of Binary Trees

| Shape | Definition | Picture |
|-------|------------|---------|
| **Full** | Every node has **0 or 2** children | No node has just one child |
| **Complete** | Every level is full except possibly the last, which fills **left to right** | Heaps use this shape |
| **Perfect** | All internal nodes have 2 children and all leaves are at the same depth | A perfect triangle |
| **Balanced** | Left and right subtree heights differ by at most 1 **at every node** | Keeps height O(log n) |
| **Degenerate (skewed)** | Every node has only one child | Basically a linked list 😬 |

```text
Perfect (h=2)       Complete            Degenerate
      1                 1               1
    /   \             /   \              \
   2     3           2     3              2
  / \   / \         / \   /                \
 4   5 6   7       4   5 6                  3
```

### Why height matters so much

Many tree operations cost **O(height)**. For n nodes:

| Shape | Height | Example for n = 1,000,000 |
|-------|--------|---------------------------|
| Perfect / balanced | ≈ log₂ n | ≈ **20** |
| Degenerate | n − 1 | **999,999** 😱 |

A perfect binary tree of height h has **2^(h+1) − 1** nodes. That's why balanced trees are so powerful: a million items fit in about 20 levels.

```dart
bool isBalanced(BinaryNode? root) => _check(root) != -1;

// Returns the height, or -1 if the subtree is unbalanced.
int _check(BinaryNode? n) {
  if (n == null) return 0;
  final l = _check(n.left);
  if (l == -1) return -1;
  final r = _check(n.right);
  if (r == -1) return -1;
  if ((l - r).abs() > 1) return -1;
  return 1 + (l > r ? l : r);
}

class BinaryNode {
  final int value;
  final BinaryNode? left, right;
  BinaryNode(this.value, [this.left, this.right]);
}

void main() {
  final balanced = BinaryNode(1, BinaryNode(2, BinaryNode(4)), BinaryNode(3));
  final skewed = BinaryNode(1, BinaryNode(2, BinaryNode(3, BinaryNode(4))));
  print(isBalanced(balanced)); // true
  print(isBalanced(skewed));   // false
}
```

**🔍 What This Code Does:**

1. **Bottom-Up Check**: Each node gets its children's heights first.
2. **Early Failure**: `-1` signals "unbalanced" and bubbles straight up, skipping further work.
3. **Balance Rule**: Heights of the two subtrees differ by at most 1.
4. **O(n)**: Each node is visited once. Computing height separately at every node would be O(n²).
5. **Different Height Convention**: Here an empty tree is 0 (so a leaf is 1); only the differences matter.

---

## 🗺️ Trees in Real Life

| Tree | Where you've seen it |
|------|---------------------|
| **File system** | Folders containing folders and files |
| **Widget tree** 💙 | Every Flutter app is a tree of widgets |
| **HTML DOM** | `<html>` → `<body>` → `<div>` → ... |
| **Org chart** | CEO → managers → teams |
| **JSON** | Objects containing objects and arrays |
| **Decision tree** | Yes/no questions leading to a result |
| **Abstract syntax tree** | How the Dart compiler represents your code |
| **Comment threads** | Replies to replies |

```dart
void main() {
  // JSON is naturally a tree. Count every key at every depth:
  final json = {
    'user': {
      'name': 'Ada',
      'address': {'city': 'London', 'zip': 'N1'},
    },
    'tags': ['admin', 'beta'],
  };

  int countKeys(Object? node) {
    if (node is Map) {
      return node.length +
          node.values.fold<int>(0, (sum, v) => sum + countKeys(v));
    }
    if (node is List) {
      return node.fold<int>(0, (sum, v) => sum + countKeys(v));
    }
    return 0;
  }

  print(countKeys(json)); // 6: user, name, address, city, zip, tags
}
```

**🔍 What This Code Does:**

1. **JSON as a Tree**: Maps and lists are internal nodes; strings and numbers are leaves.
2. **Type Checks**: `is Map` and `is List` choose how to recurse.
3. **Sum of Subtrees**: Each map contributes its own keys plus the keys inside its values.

---

## 🌳 Flutter's Widget Tree

```dart
class Widget {
  final String type;
  final List<Widget> children;
  const Widget(this.type, [this.children = const []]);
}

int depthOf(Widget w, String target, [int depth = 0]) {
  if (w.type == target) return depth;
  for (final c in w.children) {
    final d = depthOf(c, target, depth + 1);
    if (d != -1) return d;
  }
  return -1;
}

void main() {
  const app = Widget('MaterialApp', [
    Widget('Scaffold', [
      Widget('AppBar', [Widget('Text')]),
      Widget('Column', [Widget('Image'), Widget('ElevatedButton', [Widget('Icon')])]),
    ]),
  ]);

  print(depthOf(app, 'Icon'));    // 4
  print(depthOf(app, 'AppBar'));  // 2
  print(depthOf(app, 'Missing')); // -1
}
```

**🔍 What This Code Does:**

1. **A Mini Widget Tree**: Each widget has a type and children, like Flutter's real tree.
2. **Depth Search**: Look at the current widget, then search each subtree with `depth + 1`.
3. **Early Return**: Stops as soon as the target is found.
4. **Why It Matters**: Flutter walks this tree to build, lay out and paint; deep trees mean more work, which is why keeping widgets shallow and `const` helps performance.

---

## ⚠️ Common Mistakes

### 1. Confusing depth and height

Depth is measured **from the root down**; height **from the leaves up**. The root has depth 0; leaves have height 0.

### 2. Forgetting the null base case in binary trees

```dart
class N {
  final int v;
  final N? left, right;
  N(this.v, [this.left, this.right]);
}

// ❌ int sum(N n) => n.v + sum(n.left!) + sum(n.right!); crashes at leaves
int sum(N? n) => n == null ? 0 : n.v + sum(n.left) + sum(n.right); // ✅

void main() {
  print(sum(N(1, N(2), N(3, N(4))))); // 10
}
```

**🔍 What This Code Does:**

1. **Null Children Are Normal**: Most nodes are missing at least one child.
2. **Accept Nullable Input**: Handling `null` as the base case keeps the recursion simple and safe.

### 3. Sharing one children list between nodes

A default like `[this.children = const []]` is fine for read-only trees, but if nodes add children later, each needs its **own** list (as in the first example).

### 4. Assuming trees are balanced

A tree built from sorted input can become a linked list. Always ask: **what's the height?**

---

## 🧪 Try It Yourself

1. Write `maxValue(TreeNode<int> root)` for a general tree.
2. Write `pathTo(TreeNode root, String target)` returning the list of values from the root to the target.
3. Write `countAtDepth(BinaryNode? root, int d)` that counts nodes at depth `d`.
4. Write `mirror(BinaryNode? root)` that swaps every left and right child.

```dart
class BinaryNode {
  int value;
  BinaryNode? left, right;
  BinaryNode(this.value, [this.left, this.right]);
}

BinaryNode? mirror(BinaryNode? n) {
  if (n == null) return null;
  final tmp = n.left;
  n.left = mirror(n.right);
  n.right = mirror(tmp);
  return n;
}

void main() {
  final root = mirror(BinaryNode(1, BinaryNode(2), BinaryNode(3)))!;
  print('${root.left!.value} ${root.right!.value}'); // 3 2
}
```

**🔍 What This Code Does:**

1. **Swap Children**: The left subtree becomes the mirrored right subtree, and vice versa.
2. **Recursive on Both Sides**: Every level gets flipped.
3. **O(n)**: Each node is visited once.

---

## 📌 Key Takeaways

- ✅ A **tree** has one **root**, every other node has **one parent**, and there are **no cycles**; n nodes have **n − 1 edges**.
- ✅ Key terms: **leaf**, **internal node**, **subtree**, **ancestor**, **descendant**, **level**.
- ✅ **Depth** counts edges down from the root; **height** counts edges up from the deepest leaf.
- ✅ Tree algorithms are naturally **recursive**: combine the current node with its subtrees' answers.
- ✅ A **binary tree** has at most two children: **left** and **right**.
- ✅ Shapes: **full**, **complete**, **perfect**, **balanced**, **degenerate**.
- ✅ Height decides speed: **balanced ≈ log n**, **degenerate ≈ n**.

**Next up:** 🚶 **Binary Tree Traversals**: pre-order, in-order and post-order, recursive and iterative.
