# Balanced Trees

Imagine a **mobile** hanging over a baby's crib 🧸. If you keep adding toys to one side, it tips over and everything ends up dangling in one long line.

A good mobile **rebalances**: when one side gets too heavy, you slide the pivot point so both sides hang evenly again.

👉 That's what **self-balancing binary search trees** do:

> A **balanced tree** restructures itself after inserts and deletes, using small local moves called **rotations**, so its height always stays **O(log n)**. That guarantees O(log n) search, insert and delete, **no matter what order** the data arrives in.

In the last lesson, inserting sorted data turned a BST into a linked list with height n − 1. Balanced trees make that impossible.

---

## 🔄 Rotations: The Basic Move

A **rotation** rearranges three nodes and their subtrees while **preserving the BST order**. It changes heights, not the sorted sequence.

```text
Right rotation at y                 Left rotation at x

       y                x                 x                    y
      / \              / \               / \                  / \
     x   C    ──▶     A   y             A   y      ──▶       x   C
    / \                  / \               / \              / \
   A   B                B   C             B   C            A   B

In-order before and after: A x B y C (unchanged!)
```

- In a **right rotation**, the left child `x` moves up and `y` moves down to the right. Subtree `B` switches parents.
- A **left rotation** is the mirror image.
- Only **three links** change, so a rotation is **O(1)**.

```dart
class Node {
  int key;
  Node? left, right;
  Node(this.key, [this.left, this.right]);
}

Node rotateRight(Node y) {
  final x = y.left!;
  final b = x.right;
  x.right = y; // y becomes x's right child
  y.left = b;  // B moves from x to y
  return x;    // x is the new subtree root
}

Node rotateLeft(Node x) {
  final y = x.right!;
  final b = y.left;
  y.left = x;
  x.right = b;
  return y;
}

List<int> inOrder(Node? n) =>
    n == null ? [] : [...inOrder(n.left), n.key, ...inOrder(n.right)];

void main() {
  //      30
  //     /
  //    20
  //   /
  //  10
  var root = Node(30, Node(20, Node(10)));
  print(inOrder(root)); // [10, 20, 30]

  root = rotateRight(root);
  //    20
  //   /  \
  //  10   30
  print('${root.key} ${root.left!.key} ${root.right!.key}'); // 20 10 30
  print(inOrder(root)); // [10, 20, 30] (order preserved)
}
```

**🔍 What This Code Does:**

1. **Three Pointer Changes**: `x.right = y`, `y.left = b`, and the caller replaces `y` with `x`.
2. **Middle Subtree Moves**: `B` was right of `x` (bigger than `x`) and left of `y` (smaller than `y`), so it fits as `y`'s left child.
3. **Return the New Root**: The caller must reattach it, just like recursive BST insert.
4. **Order Preserved**: In-order output is identical before and after.
5. **Height Reduced**: A chain of height 2 became a tree of height 1.

---

## 🌲 AVL Trees: Strict Balance

The **AVL tree** (Adelson-Velsky and Landis, 1962) was the first self-balancing BST. Every node stores its **height**, and the tree enforces:

> **Balance factor** = height(left) − height(right), which must be **−1, 0 or +1** at every node.

After an insert, walk back up the path. If a node's balance factor becomes **+2** or **−2**, fix it with one or two rotations. There are four cases:

| Case | Shape | Fix |
|------|-------|-----|
| **Left-Left** (LL) | Heavy left, new key went into the left child's **left** | Rotate **right** |
| **Right-Right** (RR) | Heavy right, new key went into the right child's **right** | Rotate **left** |
| **Left-Right** (LR) | Heavy left, new key went into the left child's **right** | Rotate left child **left**, then node **right** |
| **Right-Left** (RL) | Heavy right, new key went into the right child's **left** | Rotate right child **right**, then node **left** |

```text
LR case: insert 30, 10, 20

   30              30             20
  /               /              /  \
 10      ──▶    20      ──▶    10    30
   \            /
    20         10
 (bf +2)   rotate 10 left   rotate 30 right
```

### A complete AVL tree

```dart
class AvlNode {
  final int key;
  AvlNode? left, right;
  int height = 0; // a leaf has height 0
  AvlNode(this.key);
}

class AvlTree {
  AvlNode? root;
  int rotations = 0;

  int _h(AvlNode? n) => n?.height ?? -1;
  int _balance(AvlNode n) => _h(n.left) - _h(n.right);

  void _update(AvlNode n) {
    final l = _h(n.left), r = _h(n.right);
    n.height = 1 + (l > r ? l : r);
  }

  AvlNode _rotateRight(AvlNode y) {
    final x = y.left!;
    y.left = x.right;
    x.right = y;
    _update(y); // y is now lower, update it first
    _update(x);
    rotations++;
    return x;
  }

  AvlNode _rotateLeft(AvlNode x) {
    final y = x.right!;
    x.right = y.left;
    y.left = x;
    _update(x);
    _update(y);
    rotations++;
    return y;
  }

  AvlNode _rebalance(AvlNode n) {
    _update(n);
    final bf = _balance(n);
    if (bf > 1) {
      // left heavy
      if (_balance(n.left!) < 0) n.left = _rotateLeft(n.left!); // LR → LL
      return _rotateRight(n);
    }
    if (bf < -1) {
      // right heavy
      if (_balance(n.right!) > 0) n.right = _rotateRight(n.right!); // RL → RR
      return _rotateLeft(n);
    }
    return n; // already balanced
  }

  AvlNode _insert(AvlNode? n, int key) {
    if (n == null) return AvlNode(key);
    if (key < n.key) {
      n.left = _insert(n.left, key);
    } else if (key > n.key) {
      n.right = _insert(n.right, key);
    } else {
      return n; // duplicate
    }
    return _rebalance(n); // fix balance on the way back up
  }

  void insert(int key) => root = _insert(root, key);

  int get height => _h(root);

  List<int> inOrder() {
    final out = <int>[];
    void walk(AvlNode? n) {
      if (n == null) return;
      walk(n.left);
      out.add(n.key);
      walk(n.right);
    }

    walk(root);
    return out;
  }
}

void main() {
  final avl = AvlTree();
  for (var i = 1; i <= 1000; i++) {
    avl.insert(i); // sorted input: the worst case for a plain BST
  }
  print('height: ${avl.height}');       // 9 (a plain BST would be 999)
  print('rotations: ${avl.rotations}'); // 990
  print('root: ${avl.root!.key}');      // 512
  print(avl.inOrder().take(5).toList()); // [1, 2, 3, 4, 5]
}
```

**🔍 What This Code Does:**

This code demonstrates **an AVL tree that stays balanced under sorted input**:

1. **Height in Every Node**: Stored and updated after changes, so balance factors are O(1) to compute.

2. **Missing Child Height −1**: Makes a leaf's height `1 + max(−1, −1) = 0`.

3. **Rebalance on the Way Up**: After the recursive insert returns, each ancestor checks its balance factor.

4. **Double Rotations**: For LR and RL, the child is rotated first to turn the shape into LL or RR.

5. **Guaranteed Height**: 1,000 sorted inserts produce height 9 instead of 999.

6. **Still a BST**: In-order traversal is still sorted.

> 💡 An AVL tree's height is at most about **1.44 × log₂ n**, so even in the worst case it's very close to perfectly balanced.

---

## 🔴⚫ Red-Black Trees: Relaxed Balance

**Red-black trees** are the most widely used balanced BSTs (Java's `TreeMap`, C++'s `std::map`, the Linux kernel). Every node is colored **red** or **black**, and the tree maintains five rules:

1. Every node is red or black.
2. The root is black.
3. Every missing (null) child counts as black.
4. A red node **cannot have a red child** (no two reds in a row).
5. Every path from a node down to its null children contains the **same number of black nodes** (its *black height*).

Together, rules 4 and 5 guarantee that the longest path is **at most twice** the shortest, so height ≤ **2 × log₂(n + 1)**.

```dart
// A tiny checker that verifies the red-black rules on a hand-built tree.
enum Color { red, black }

class RbNode {
  final int key;
  final Color color;
  final RbNode? left, right;
  const RbNode(this.key, this.color, [this.left, this.right]);
}

/// Returns the black height, or -1 if a rule is broken.
int blackHeight(RbNode? n) {
  if (n == null) return 1; // null leaves are black
  if (n.color == Color.red &&
      (n.left?.color == Color.red || n.right?.color == Color.red)) {
    return -1; // red node with a red child
  }
  final l = blackHeight(n.left), r = blackHeight(n.right);
  if (l == -1 || r == -1 || l != r) return -1;
  return l + (n.color == Color.black ? 1 : 0);
}

void main() {
  const valid = RbNode(10, Color.black,
      RbNode(5, Color.red, RbNode(2, Color.black), RbNode(7, Color.black)),
      RbNode(15, Color.black));
  const twoReds = RbNode(10, Color.black,
      RbNode(5, Color.red, RbNode(2, Color.red)), RbNode(15, Color.black));

  print(blackHeight(valid));   // 3
  print(blackHeight(twoReds)); // -1 (red 5 has a red child)
}
```

**🔍 What This Code Does:**

1. **`enum Color`**: Each node is red or black.
2. **Null Leaves Are Black**: The base case returns a black height of 1.
3. **No Red-Red**: A red node with a red child breaks rule 4.
4. **Equal Black Heights**: Left and right black heights must match at every node (rule 5).
5. **Recursive Check**: Combines both rules in one O(n) pass.

### AVL vs red-black

| | AVL | Red-black |
|---|-----|-----------|
| Balance rule | Heights differ by ≤ 1 | No red-red; equal black heights |
| Max height | ≈ 1.44 log₂ n | ≈ 2 log₂ n |
| Lookups | ✅ Slightly faster (shorter) | Slightly slower |
| Inserts/deletes | More rotations | ✅ Fewer rotations (≤ 2 per insert, ≤ 3 per delete) |
| Typical use | Read-heavy workloads, databases | General-purpose libraries |

---

## 🌀 Splay Trees: Why Dart Uses Them

Dart's `SplayTreeMap` and `SplayTreeSet` are **splay trees**. They take a different approach:

> After **every** access, the accessed node is **splayed** (rotated all the way up) to the **root**.

- No heights or colors are stored.
- Recently used keys are near the top, so **repeated access is very fast** (great for caches and "hot" keys).
- A single operation can take O(n), but any sequence of `m` operations takes **O(m log n)**: **amortized O(log n)**.

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<int, String>();
  for (var i = 1; i <= 100000; i++) {
    m[i] = 'v$i'; // sorted inserts are fine
  }

  final sw = Stopwatch()..start();
  for (var i = 0; i < 100000; i++) {
    m[42]; // the same "hot" key again and again: stays at the root
  }
  print('hot key lookups: ${sw.elapsedMilliseconds} ms');
  print(m.firstKey()); // 1
  print(m.lastKey());  // 100000
}
```

**🔍 What This Code Does:**

1. **Sorted Inserts**: Would wreck a plain BST but are handled smoothly by splaying.
2. **Hot Key**: After the first lookup, key 42 sits at the root, so later lookups are almost instant.
3. **Sorted Operations**: `firstKey` and `lastKey` work as expected.

| Tree | Guarantee | Stored per node | Special strength |
|------|-----------|-----------------|------------------|
| AVL | O(log n) worst case | Height | Fastest lookups |
| Red-black | O(log n) worst case | 1 color bit | Fewest rotations |
| Splay | O(log n) amortized | Nothing extra | Hot keys get faster |

---

## 🌳 Beyond Binary: B-Trees

Databases and file systems use **B-trees**, where each node holds **many** keys (often hundreds) and has many children. Each node fits one disk page, so a tree with billions of keys is only 3–4 levels deep, which means 3–4 disk reads per lookup.

```text
                  [ 20 | 40 ]
                /      |      \
     [5 | 10 | 15]  [25 | 30]  [45 | 50 | 60]
```

All leaves are at the **same depth**, and nodes split or merge to stay balanced.

---

## 📊 Why It All Matters

```dart
import 'dart:math';

void main() {
  for (final n in [1000, 1000000, 1000000000]) {
    final perfect = (log(n + 1) / ln2).ceil() - 1;
    final avl = (1.44 * log(n) / ln2).floor();
    final rb = (2 * log(n + 1) / ln2).floor();
    print('n=$n  perfect≈$perfect  AVL≤$avl  red-black≤$rb  plain BST worst=${n - 1}');
  }
}
```

**🔍 What This Code Does:**

1. **Height Bounds**: Computes the best possible height and the worst-case bounds for AVL and red-black trees.
2. **Billions of Keys**: A balanced tree stays under about 60 levels; an unbalanced one could be a billion levels deep.

---

## ⚠️ Common Mistakes

### 1. Updating heights in the wrong order after a rotation

The node that moved **down** must be updated **first**, because the node that moved up depends on it.

### 2. Forgetting the double-rotation cases

Applying a single rotation to an LR or RL shape just moves the imbalance to the other side. Rotate the child first.

### 3. Forgetting to reattach the rotated subtree

Rotations return a new subtree root. Write `n.left = rotateLeft(n.left!)` and `root = _insert(root, key)`.

### 4. Reimplementing balanced trees in production

Building your own AVL or red-black tree is a great exercise, but in real Dart code use `SplayTreeMap`/`SplayTreeSet`, which are tested and optimized.

---

## 🧪 Try It Yourself

1. Add `contains(int key)` to `AvlTree`.
2. Insert 1–15 into `AvlTree` and print the root after each insert. Which inserts trigger rotations?
3. Add a `delete` to `AvlTree` (BST delete, then `_rebalance` on the way up).
4. Write `isAvl(node)` that verifies every balance factor is −1, 0 or +1.

---

## 📌 Key Takeaways

- ✅ **Rotations** restructure three nodes in O(1) while preserving BST order.
- ✅ **AVL trees** keep every node's balance factor in **[−1, 1]** using single and double rotations; height ≈ **1.44 log n**.
- ✅ **Red-black trees** use colors (no red-red, equal black heights); height ≤ **2 log n**, with fewer rotations.
- ✅ **Splay trees** (Dart's `SplayTreeMap`) move accessed keys to the root; **amortized O(log n)**, great for hot keys.
- ✅ **B-trees** pack many keys per node for databases and disks.
- ✅ All of them guarantee **O(log n)** operations, regardless of insertion order.

**Next up:** ⛰️ **Heaps & Priority Queues**: always get the smallest (or most urgent) item fast.
