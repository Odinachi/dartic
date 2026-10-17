# Binary Tree Traversals

Imagine you're touring a **castle** 🏰 with rooms connected like a tree. At every room you can do three things: **look around** 👀, explore the **left** wing ⬅️, and explore the **right** wing ➡️.

The **order** you do them in changes the story of your tour:

- 👀 ⬅️ ➡️ Look first, then explore: you describe each room **before** its wings (**pre-order**).
- ⬅️ 👀 ➡️ Left wing first, then look, then right: you describe rooms in **left-to-right** order (**in-order**).
- ⬅️ ➡️ 👀 Explore both wings, then look: you describe each room **after** everything below it (**post-order**).

👉 A **traversal** visits every node of a tree exactly once in a specific order:

> **Pre-order:** node → left → right
> **In-order:** left → node → right
> **Post-order:** left → right → node

These three depth-first traversals are the building blocks of almost every tree algorithm.

---

## 🌳 Our Example Tree

```text
            F
          /   \
         B     G
        / \     \
       A   D     I
          / \   /
         C   E H
```

| Traversal | Order | Result |
|-----------|-------|--------|
| **Pre-order** | node, left, right | `F B A D C E G I H` |
| **In-order** | left, node, right | `A B C D E F G H I` |
| **Post-order** | left, right, node | `A C E D B H I G F` |

Notice the **in-order** result is **alphabetical**. That's not a coincidence: this tree is a **binary search tree**, and in-order traversal of a BST always gives sorted output (next lessons!).

---

## 🔁 Recursive Traversals

```dart
class Node<T> {
  final T value;
  final Node<T>? left, right;
  const Node(this.value, [this.left, this.right]);
}

void preOrder<T>(Node<T>? n, List<T> out) {
  if (n == null) return;
  out.add(n.value);        // 1. visit node
  preOrder(n.left, out);   // 2. left
  preOrder(n.right, out);  // 3. right
}

void inOrder<T>(Node<T>? n, List<T> out) {
  if (n == null) return;
  inOrder(n.left, out);    // 1. left
  out.add(n.value);        // 2. visit node
  inOrder(n.right, out);   // 3. right
}

void postOrder<T>(Node<T>? n, List<T> out) {
  if (n == null) return;
  postOrder(n.left, out);  // 1. left
  postOrder(n.right, out); // 2. right
  out.add(n.value);        // 3. visit node
}

const tree = Node('F',
    Node('B', Node('A'), Node('D', Node('C'), Node('E'))),
    Node('G', null, Node('I', Node('H'))));

void main() {
  final pre = <String>[], inn = <String>[], post = <String>[];
  preOrder(tree, pre);
  inOrder(tree, inn);
  postOrder(tree, post);
  print(pre.join(' '));  // F B A D C E G I H
  print(inn.join(' '));  // A B C D E F G H I
  print(post.join(' ')); // A C E D B H I G F
}
```

**🔍 What This Code Does:**

1. **Same Skeleton, Different Order**: All three functions recurse left and right; only the position of `out.add(n.value)` changes.
2. **Null Base Case**: Missing children simply return.
3. **Accumulator List**: Results are collected into `out` instead of printed, which is easier to test.
4. **`const` Tree**: The whole tree is a compile-time constant because `Node` has a `const` constructor and final fields.
5. **O(n) Time, O(h) Space**: Every node is visited once; the call stack grows to the tree's height `h`.

### Using a callback instead of a list

```dart
class Node<T> {
  final T value;
  final Node<T>? left, right;
  const Node(this.value, [this.left, this.right]);
}

void inOrder<T>(Node<T>? n, void Function(T) visit) {
  if (n == null) return;
  inOrder(n.left, visit);
  visit(n.value);
  inOrder(n.right, visit);
}

void main() {
  const t = Node(5, Node(3, Node(1), Node(4)), Node(8));
  var sum = 0;
  inOrder(t, (int v) => sum += v);
  print(sum); // 21

  final buffer = StringBuffer();
  inOrder(t, buffer.write);
  print(buffer); // 13458
}
```

**🔍 What This Code Does:**

1. **Function Parameter**: `void Function(T) visit` lets the caller decide what to do with each value.
2. **Closures**: The lambda updates `sum` from the outer scope.
3. **Tear-offs**: `buffer.write` is passed directly as the callback.

---

## 🎯 When to Use Which

| Traversal | Visits a node... | Classic uses |
|-----------|------------------|--------------|
| **Pre-order** | **Before** its children | Copying/serializing a tree, printing folder structures, prefix expressions |
| **In-order** | **Between** left and right | Getting **sorted** values from a BST, validating a BST |
| **Post-order** | **After** its children | Deleting/freeing a tree, computing sizes/heights, evaluating expressions |

### Post-order: evaluating an expression tree

```dart
sealed class Expr {}

class Num extends Expr {
  final double value;
  Num(this.value);
}

class Op extends Expr {
  final String symbol;
  final Expr left, right;
  Op(this.symbol, this.left, this.right);
}

double evaluate(Expr e) => switch (e) {
      Num(:final value) => value,
      Op(:final symbol, :final left, :final right) => switch (symbol) {
          '+' => evaluate(left) + evaluate(right),
          '-' => evaluate(left) - evaluate(right),
          '*' => evaluate(left) * evaluate(right),
          _ => evaluate(left) / evaluate(right),
        },
    };

String toInfix(Expr e) => switch (e) {
      Num(:final value) => value.toStringAsFixed(0),
      Op(:final symbol, :final left, :final right) =>
        '(${toInfix(left)} $symbol ${toInfix(right)})',
    };

void main() {
  //        *
  //      /   \
  //     +     -
  //    / \   / \
  //   3   4 10  6
  final expr = Op('*', Op('+', Num(3), Num(4)), Op('-', Num(10), Num(6)));
  print(toInfix(expr));  // ((3 + 4) * (10 - 6))
  print(evaluate(expr)); // 28.0
}
```

**🔍 What This Code Does:**

1. **Sealed Class Hierarchy**: An `Expr` is either a `Num` (leaf) or an `Op` (internal node with two children).
2. **Post-Order Evaluation**: Both children are evaluated **before** the operator is applied, because you need both operands first.
3. **Exhaustive `switch`**: Because `Expr` is `sealed`, Dart checks that every subtype is handled.
4. **Object Patterns**: `Op(:final symbol, :final left, :final right)` destructures fields by name.
5. **In-Order Printing**: `toInfix` prints left, operator, right, which is in-order with parentheses.

### Pre-order: serializing a tree

```dart
class Node {
  final int value;
  final Node? left, right;
  Node(this.value, [this.left, this.right]);
}

String serialize(Node? n) =>
    n == null ? '#' : '${n.value},${serialize(n.left)},${serialize(n.right)}';

Node? deserialize(String data) {
  final tokens = data.split(',').iterator;
  Node? build() {
    tokens.moveNext();
    final t = tokens.current;
    if (t == '#') return null;
    final value = int.parse(t);
    final left = build();
    final right = build();
    return Node(value, left, right);
  }

  return build();
}

void main() {
  final tree = Node(1, Node(2), Node(3, Node(4), Node(5)));
  final s = serialize(tree);
  print(s); // 1,2,#,#,3,4,#,#,5,#,#

  final copy = deserialize(s)!;
  print(serialize(copy) == s); // true (round trip works)
  print(copy.right!.left!.value); // 4
}
```

**🔍 What This Code Does:**

1. **Pre-Order With Null Markers**: `#` records missing children, so the shape is unambiguous.
2. **Rebuild in the Same Order**: `deserialize` reads tokens in pre-order: value, then left subtree, then right subtree.
3. **Iterator**: `moveNext()` and `current` read tokens one at a time across recursive calls.
4. **Local Function**: `build` is declared inside `deserialize` and captures `tokens`.
5. **Round Trip**: Serializing the copy produces the identical string.

---

## 🧱 Iterative Traversals With an Explicit Stack

Recursion uses the call stack. For very deep trees, or just to understand what's happening, we can manage the stack ourselves.

### Iterative pre-order

```dart
class Node {
  final String value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<String> preOrderIterative(Node? root) {
  final out = <String>[];
  if (root == null) return out;
  final stack = <Node>[root];
  while (stack.isNotEmpty) {
    final n = stack.removeLast();
    out.add(n.value);
    if (n.right != null) stack.add(n.right!); // push right FIRST
    if (n.left != null) stack.add(n.left!);   // so left is popped first
  }
  return out;
}

const tree = Node('F',
    Node('B', Node('A'), Node('D', Node('C'), Node('E'))),
    Node('G', null, Node('I', Node('H'))));

void main() {
  print(preOrderIterative(tree).join(' ')); // F B A D C E G I H
}
```

**🔍 What This Code Does:**

1. **Pop, Visit, Push Children**: Just like recursion, but explicit.
2. **Right Before Left**: The stack is LIFO, so pushing right first means left is processed first.
3. **Same Output** as the recursive version.

### Iterative in-order

```dart
class Node {
  final String value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<String> inOrderIterative(Node? root) {
  final out = <String>[];
  final stack = <Node>[];
  var current = root;
  while (current != null || stack.isNotEmpty) {
    while (current != null) {   // 1. go as far left as possible
      stack.add(current);
      current = current.left;
    }
    final n = stack.removeLast(); // 2. visit the leftmost unvisited node
    out.add(n.value);
    current = n.right;            // 3. then explore its right subtree
  }
  return out;
}

const tree = Node('F',
    Node('B', Node('A'), Node('D', Node('C'), Node('E'))),
    Node('G', null, Node('I', Node('H'))));

void main() {
  print(inOrderIterative(tree).join(' ')); // A B C D E F G H I
}
```

**🔍 What This Code Does:**

1. **Dive Left**: Push every node on the way down the left edge.
2. **Visit**: Pop the deepest one; it has no unvisited left subtree.
3. **Go Right**: Repeat the process for its right subtree.
4. **Stack Holds the Path**: At most `h` nodes are on the stack at once.

### Iterative post-order (two-stack trick)

```dart
class Node {
  final String value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<String> postOrderIterative(Node? root) {
  if (root == null) return [];
  final stack = <Node>[root];
  final reversed = <String>[];
  while (stack.isNotEmpty) {
    final n = stack.removeLast();
    reversed.add(n.value);                    // node, right, left order...
    if (n.left != null) stack.add(n.left!);
    if (n.right != null) stack.add(n.right!);
  }
  return reversed.reversed.toList();          // ...reversed = left, right, node
}

const tree = Node('F',
    Node('B', Node('A'), Node('D', Node('C'), Node('E'))),
    Node('G', null, Node('I', Node('H'))));

void main() {
  print(postOrderIterative(tree).join(' ')); // A C E D B H I G F
}
```

**🔍 What This Code Does:**

1. **Modified Pre-Order**: Visiting in node → right → left order...
2. **Reversal**: ...and reversing the result gives left → right → node, which is post-order.
3. **Simple and Correct**: Costs O(n) extra space for the result list, which we need anyway.

---

## 🧠 Traversal-Powered Algorithms

### Maximum depth (post-order thinking)

```dart
class Node {
  final int v;
  final Node? left, right;
  const Node(this.v, [this.left, this.right]);
}

int maxDepth(Node? n) {
  if (n == null) return 0;
  final l = maxDepth(n.left), r = maxDepth(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  print(maxDepth(const Node(1, Node(2, Node(4)), Node(3)))); // 3 (counts nodes)
}
```

**🔍 What This Code Does:**

1. **Children First**: We need both subtree depths before computing ours, which is post-order.
2. **Counts Nodes on the Path**: This version counts nodes (a leaf = 1), a common convention in coding problems.

### Root-to-leaf path sums (pre-order with state)

```dart
class Node {
  final int v;
  final Node? left, right;
  const Node(this.v, [this.left, this.right]);
}

void pathSums(Node? n, int soFar, List<int> out) {
  if (n == null) return;
  final total = soFar + n.v;            // visit: update state on the way down
  if (n.left == null && n.right == null) {
    out.add(total);                     // reached a leaf
    return;
  }
  pathSums(n.left, total, out);
  pathSums(n.right, total, out);
}

void main() {
  //      5
  //     / \
  //    4   8
  //   /   / \
  //  11  13  4
  const t = Node(5, Node(4, Node(11)), Node(8, Node(13), Node(4)));
  final sums = <int>[];
  pathSums(t, 0, sums);
  print(sums); // [20, 26, 17]
}
```

**🔍 What This Code Does:**

1. **State Flows Down**: The running total is passed into each child, pre-order style.
2. **Leaves Record Results**: A node with no children ends a path.
3. **Paths**: 5→4→11 = 20, 5→8→13 = 26, 5→8→4 = 17.

### Are two trees identical?

```dart
class Node {
  final int v;
  final Node? left, right;
  const Node(this.v, [this.left, this.right]);
}

bool same(Node? a, Node? b) {
  if (a == null || b == null) return a == b; // both null → true; one null → false
  return a.v == b.v && same(a.left, b.left) && same(a.right, b.right);
}

void main() {
  print(same(const Node(1, Node(2)), const Node(1, Node(2))));       // true
  print(same(const Node(1, Node(2)), const Node(1, null, Node(2)))); // false
}
```

**🔍 What This Code Does:**

1. **Null Handling in One Line**: If either is null, they're the same only if both are.
2. **Short-Circuit `&&`**: Stops comparing as soon as a difference is found.
3. **Shape Matters**: Same values in different positions are not identical.

---

## 🪄 Bonus: Morris Traversal (O(1) Space)

Morris in-order traversal temporarily rewires right pointers to avoid any stack. It's an advanced trick: you won't need it often, but it shows how much clever pointer work trees allow.

```dart
class Node {
  final int v;
  Node? left, right;
  Node(this.v, [this.left, this.right]);
}

List<int> morrisInOrder(Node? root) {
  final out = <int>[];
  var cur = root;
  while (cur != null) {
    if (cur.left == null) {
      out.add(cur.v);
      cur = cur.right;
    } else {
      var pred = cur.left!;
      while (pred.right != null && !identical(pred.right, cur)) {
        pred = pred.right!;
      }
      if (pred.right == null) {
        pred.right = cur;  // create a temporary thread back to cur
        cur = cur.left;
      } else {
        pred.right = null; // remove the thread, restoring the tree
        out.add(cur.v);
        cur = cur.right;
      }
    }
  }
  return out;
}

void main() {
  final t = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)));
  print(morrisInOrder(t)); // [1, 2, 3, 4, 5, 6, 7]
}
```

**🔍 What This Code Does:**

1. **Predecessor**: The rightmost node of the left subtree comes just before `cur` in in-order.
2. **Threading**: Pointing that predecessor's `right` back to `cur` lets us return without a stack.
3. **Unthreading**: The second time we arrive, we remove the thread, so the tree ends up unchanged.
4. **O(n) Time, O(1) Extra Space**.

---

## ⚠️ Common Mistakes

### 1. Mixing up the orders

Remember by **where the node goes**: **pre** = node first, **in** = node in the middle, **post** = node last. Left always comes before right.

### 2. Pushing children in the wrong order on a stack

In iterative pre-order, push **right then left**, because the last pushed is popped first.

### 3. Stack overflow on deep trees

A degenerate tree of 1,000,000 nodes makes recursive traversal 1,000,000 calls deep. Use the iterative versions for untrusted or very deep trees.

### 4. Modifying the tree while traversing

Changing children mid-traversal (other than in carefully designed algorithms like Morris) leads to skipped or repeated nodes.

---

## 🧪 Try It Yourself

1. Write `leaves(Node? root)` that returns leaf values left to right.
2. Write `kthSmallest(Node? bstRoot, int k)` using in-order traversal with an early stop.
3. Rebuild a tree from its **pre-order** and **in-order** lists (assume unique values).
4. Write `invert` (mirror) using an iterative pre-order traversal.

---

## 📌 Key Takeaways

- ✅ **Pre-order**: node → left → right; great for copying and serializing.
- ✅ **In-order**: left → node → right; gives **sorted** output for a BST.
- ✅ **Post-order**: left → right → node; great for sizes, heights, deletion and expression evaluation.
- ✅ All three are **O(n)** time and **O(h)** space.
- ✅ Iterative versions use an **explicit stack**; push **right before left** for pre-order.
- ✅ Many problems are just a traversal plus state passed **down** (depth, path sums) or returned **up** (heights, sizes).

**Next up:** 🌊 **Level-Order Traversal**: visiting a tree level by level with a queue.
