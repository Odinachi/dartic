# Binary Search Trees

Remember the number guessing game? 🎯 *"I'm thinking of a number between 1 and 100."*

- You guess **50**. *"Higher!"* So you ignore everything from 1 to 50.
- You guess **75**. *"Lower!"* Now only 51–74 remain.
- Each answer cuts the possibilities **in half**.

Now imagine organizing your data so **every lookup works like that game**. Every node says *"smaller things are to my left, bigger things to my right"*.

👉 That's a **binary search tree (BST)**:

> A **binary search tree** is a binary tree where, for **every** node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger**. Search, insert and delete follow one path from the root, costing **O(height)**.

When the tree is balanced, that's **O(log n)**: a million items in about 20 steps. 🚀

---

## 📜 The BST Property

```text
              8
            /   \
           3     10
          / \      \
         1   6      14
            / \    /
           4   7  13
```

- Everything left of `8` (1, 3, 4, 6, 7) is **< 8**.
- Everything right of `8` (10, 13, 14) is **> 8**.
- And the same holds at **every** node: left of `3` is `1`; right of `3` is `4, 6, 7`.

> ⚠️ It's not enough for each node to be bigger than its left **child**. The rule applies to the **whole** subtree. That's the most common BST bug.

**In-order traversal** (left, node, right) of a BST visits values in **sorted order**: `1 3 4 6 7 8 10 13 14`.

---

## 🔎 Search

```dart
class Node {
  int value;
  Node? left, right;
  Node(this.value);
}

bool contains(Node? root, int target) {
  var current = root;
  while (current != null) {
    if (target == current.value) return true;
    current = target < current.value ? current.left : current.right;
  }
  return false;
}

Node? insert(Node? root, int value) {
  if (root == null) return Node(value);
  if (value < root.value) {
    root.left = insert(root.left, value);
  } else if (value > root.value) {
    root.right = insert(root.right, value);
  } // equal: ignore duplicates
  return root;
}

void main() {
  Node? root;
  for (final v in [8, 3, 10, 1, 6, 14, 4, 7, 13]) {
    root = insert(root, v);
  }
  print(contains(root, 6));  // true
  print(contains(root, 5));  // false
  print(contains(root, 13)); // true
}
```

**🔍 What This Code Does:**

This code demonstrates **BST search and insertion**:

1. **One Comparison per Level**: At each node, go left if the target is smaller, right if larger.

2. **Never Backtrack**: The BST property guarantees the target can only be on one side.

3. **Insert Where Search Would Fail**: `insert` walks the same path as search and attaches a new node at the empty spot.

4. **Recursive Rewiring**: `root.left = insert(root.left, value)` returns the (possibly new) subtree root and reattaches it.

5. **Duplicates Ignored**: This version treats the tree as a **set**. (Alternatives: count duplicates, or always send them right.)

6. **O(h)**: Both operations visit one node per level.

**Searching for 7:** `8 → (7 < 8) left → 3 → (7 > 3) right → 6 → (7 > 6) right → 7 ✅` (4 comparisons)

---

## 🏗️ A Complete `BinarySearchTree` Class

```dart
class _Node<K extends Comparable<K>, V> {
  K key;
  V value;
  _Node<K, V>? left, right;
  _Node(this.key, this.value);
}

class BinarySearchTree<K extends Comparable<K>, V> {
  _Node<K, V>? _root;
  int _size = 0;

  int get length => _size;

  V? operator [](K key) {
    var n = _root;
    while (n != null) {
      final c = key.compareTo(n.key);
      if (c == 0) return n.value;
      n = c < 0 ? n.left : n.right;
    }
    return null;
  }

  void operator []=(K key, V value) {
    _root = _put(_root, key, value);
  }

  _Node<K, V> _put(_Node<K, V>? n, K key, V value) {
    if (n == null) {
      _size++;
      return _Node(key, value);
    }
    final c = key.compareTo(n.key);
    if (c < 0) {
      n.left = _put(n.left, key, value);
    } else if (c > 0) {
      n.right = _put(n.right, key, value);
    } else {
      n.value = value; // existing key: update
    }
    return n;
  }

  K? get minKey {
    var n = _root;
    if (n == null) return null;
    while (n!.left != null) {
      n = n.left;
    }
    return n.key;
  }

  K? get maxKey {
    var n = _root;
    if (n == null) return null;
    while (n!.right != null) {
      n = n.right;
    }
    return n.key;
  }

  Iterable<K> get keys sync* {
    // in-order traversal = sorted keys
    final stack = <_Node<K, V>>[];
    var n = _root;
    while (n != null || stack.isNotEmpty) {
      while (n != null) {
        stack.add(n);
        n = n.left;
      }
      final top = stack.removeLast();
      yield top.key;
      n = top.right;
    }
  }
}

void main() {
  final phoneBook = BinarySearchTree<String, String>();
  phoneBook['Linus'] = '555-0102';
  phoneBook['Ada'] = '555-0100';
  phoneBook['Grace'] = '555-0199';
  phoneBook['Ada'] = '555-0101'; // update

  print(phoneBook['Ada']);       // 555-0101
  print(phoneBook['Bjarne']);    // null
  print(phoneBook.keys.toList()); // [Ada, Grace, Linus]
  print(phoneBook.minKey);       // Ada
  print(phoneBook.maxKey);       // Linus
  print(phoneBook.length);       // 3
}
```

**🔍 What This Code Does:**

1. **Generic Keys With `Comparable`**: `K extends Comparable<K>` means keys can be ordered with `compareTo`, so `String`, `int`, `DateTime` all work.
2. **Map-Like API**: `operator []` and `operator []=` make the tree feel like a `Map`.
3. **`compareTo`**: Negative means "go left", positive "go right", zero "found".
4. **Min and Max**: The minimum is the **leftmost** node; the maximum is the **rightmost**.
5. **Sorted Keys With `sync*`**: A generator function lazily `yield`s keys in in-order sequence.
6. **This Is What `SplayTreeMap` Does**: Plus self-balancing so the height stays small.

---

## 🗑️ Deletion: Three Cases

Deleting is the trickiest BST operation, because the tree must stay a valid BST.

```text
Case 1: delete a leaf (4)        Case 2: delete a node with one child (10)

      6              6                 8                 8
     / \     →        \                 \       →         \
    4   7              7                 10                14
                                           \
                                            14

Case 3: delete a node with two children (3)
Its in-order successor (4, the smallest value in its right subtree) takes its place.

        8                        8
       /                        /
      3            →           4
     / \                      / \
    1   6                    1   6
       / \                        \
      4   7                        7
```

1. **Leaf**: Just remove it.
2. **One child**: Replace the node with its child.
3. **Two children**: Replace its value with its **in-order successor** (the smallest value in the right subtree), then delete that successor from the right subtree. The successor has no left child, so deleting it falls into case 1 or 2.

```dart
class Node {
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

Node? delete(Node? n, int v) {
  if (n == null) return null; // not found
  if (v < n.value) {
    n.left = delete(n.left, v);
  } else if (v > n.value) {
    n.right = delete(n.right, v);
  } else {
    // Found it!
    if (n.left == null) return n.right; // case 1 or 2
    if (n.right == null) return n.left; // case 2
    // case 3: two children → use the in-order successor
    var successor = n.right!;
    while (successor.left != null) {
      successor = successor.left!;
    }
    n.value = successor.value;
    n.right = delete(n.right, successor.value);
  }
  return n;
}

List<int> inOrder(Node? n) =>
    n == null ? [] : [...inOrder(n.left), n.value, ...inOrder(n.right)];

void main() {
  Node? root;
  for (final v in [8, 3, 10, 1, 6, 14, 4, 7, 13]) {
    root = insert(root, v);
  }
  root = delete(root, 4);  // leaf
  print(inOrder(root));    // [1, 3, 6, 7, 8, 10, 13, 14]
  root = delete(root, 10); // one child
  print(inOrder(root));    // [1, 3, 6, 7, 8, 13, 14]
  root = delete(root, 3);  // two children
  print(inOrder(root));    // [1, 6, 7, 8, 13, 14]
  root = delete(root, 8);  // the root itself
  print(inOrder(root));    // [1, 6, 7, 13, 14]
  print(root!.value);      // 13 (successor of 8 became the root)
}
```

**🔍 What This Code Does:**

1. **Find the Node**: Recursively go left or right, reattaching the returned subtree.
2. **Zero or One Child**: Return the other child (possibly `null`), which splices the node out.
3. **Two Children**: Copy the successor's value into this node, then delete the successor from the right subtree.
4. **Why the Successor?**: It's the smallest value bigger than the deleted one, so the BST order is preserved.
5. **Sorted Check**: `inOrder` stays sorted after every deletion, proving the tree is still a valid BST.
6. **Spread Operator**: `[...left, value, ...right]` builds the in-order list (fine for small demos; O(n log n)–O(n²) copying in total).

> 💡 Using the **in-order predecessor** (the largest value in the left subtree) works equally well.

---

## ✅ Validating a BST

The classic bug: checking only parent–child pairs. Each node must fit within a **range** determined by **all** its ancestors.

```dart
class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

// ❌ Only compares children with their direct parent
bool isBstWrong(Node? n) {
  if (n == null) return true;
  if (n.left != null && n.left!.value >= n.value) return false;
  if (n.right != null && n.right!.value <= n.value) return false;
  return isBstWrong(n.left) && isBstWrong(n.right);
}

// ✅ Carries the allowed range down the tree
bool isBst(Node? n, [int? min, int? max]) {
  if (n == null) return true;
  if ((min != null && n.value <= min) || (max != null && n.value >= max)) {
    return false;
  }
  return isBst(n.left, min, n.value) && isBst(n.right, n.value, max);
}

void main() {
  //      10
  //     /  \
  //    5    15
  //        /  \
  //       6    20      ← 6 is in the RIGHT subtree of 10 but smaller than 10!
  const tricky = Node(10, Node(5), Node(15, Node(6), Node(20)));
  print(isBstWrong(tricky)); // true  ❌ fooled
  print(isBst(tricky));      // false ✅ correct
}
```

**🔍 What This Code Does:**

1. **The Trap**: `6 < 15` is fine locally, but `6` sits in the right subtree of `10`, so it must be **> 10**.
2. **Ranges Flow Down**: Going left tightens the **max**; going right tightens the **min**.
3. **Nullable Bounds**: `null` means "no limit yet" at the root.
4. **Alternative**: An in-order traversal must be **strictly increasing**.

---

## 🧭 More BST Queries

```dart
class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

// Largest value <= x
int? floor(Node? n, int x) {
  int? best;
  while (n != null) {
    if (n.value == x) return x;
    if (n.value < x) {
      best = n.value; // candidate; try for something bigger on the right
      n = n.right;
    } else {
      n = n.left;
    }
  }
  return best;
}

// Smallest value >= x
int? ceiling(Node? n, int x) {
  int? best;
  while (n != null) {
    if (n.value == x) return x;
    if (n.value > x) {
      best = n.value;
      n = n.left;
    } else {
      n = n.right;
    }
  }
  return best;
}

// All values in [lo, hi], in sorted order, skipping irrelevant subtrees
void range(Node? n, int lo, int hi, List<int> out) {
  if (n == null) return;
  if (n.value > lo) range(n.left, lo, hi, out);
  if (n.value >= lo && n.value <= hi) out.add(n.value);
  if (n.value < hi) range(n.right, lo, hi, out);
}

// Lowest common ancestor of a and b
int lca(Node n, int a, int b) {
  var cur = n;
  while (true) {
    if (a < cur.value && b < cur.value) {
      cur = cur.left!;
    } else if (a > cur.value && b > cur.value) {
      cur = cur.right!;
    } else {
      return cur.value; // the paths split here
    }
  }
}

const tree = Node(8,
    Node(3, Node(1), Node(6, Node(4), Node(7))),
    Node(10, null, Node(14, Node(13))));

void main() {
  print(floor(tree, 5));    // 4
  print(ceiling(tree, 11)); // 13
  print(floor(tree, 0));    // null
  final out = <int>[];
  range(tree, 4, 10, out);
  print(out);               // [4, 6, 7, 8, 10]
  print(lca(tree, 4, 7));   // 6
  print(lca(tree, 1, 13));  // 8
}
```

**🔍 What This Code Does:**

1. **Floor / Ceiling**: Walk down, remembering the best candidate so far. O(h).
2. **Range Query**: Only explores subtrees that can contain values in `[lo, hi]`. O(h + k) for `k` results.
3. **Lowest Common Ancestor**: The first node where `a` and `b` go in different directions (or one of them is the node).
4. **Dart's Equivalent**: `SplayTreeMap.lastKeyBefore` / `firstKeyAfter` answer strict floor/ceiling questions.

---

## ⚖️ The Catch: Height Depends on Insertion Order

```dart
class Node {
  int value;
  Node? left, right;
  Node(this.value);
}

Node insert(Node? n, int v) {
  if (n == null) return Node(v);
  if (v < n.value) {
    n.left = insert(n.left, v);
  } else {
    n.right = insert(n.right, v);
  }
  return n;
}

int height(Node? n) {
  if (n == null) return -1;
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  Node? sorted, shuffled;
  final values = List.generate(1000, (i) => i);
  for (final v in values) {
    sorted = insert(sorted, v);
  }
  for (final v in [...values]..shuffle()) {
    shuffled = insert(shuffled, v);
  }
  print('sorted inserts → height ${height(sorted)}'); // 999 😱
  print('random inserts → height ~${height(shuffled)}'); // around 20
}
```

**🔍 What This Code Does:**

1. **Sorted Input**: Each new value is bigger than all previous ones, so it always goes right. The "tree" becomes a linked list with height 999.
2. **Random Input**: Values land on both sides, producing a height of around 20 (≈ 2–3 × log₂ n on average).
3. **Consequence**: The same 1,000 values give O(n) or O(log n) operations depending only on the **order** they were inserted.
4. **The Fix**: **Self-balancing** trees (next lesson) restructure themselves to keep the height O(log n) no matter what.

| Operation | Balanced BST | Degenerate BST |
|-----------|--------------|----------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Min / max | O(log n) | O(n) |
| Sorted iteration | O(n) | O(n) |

---

## 🆚 BST vs Hash Map vs Sorted List

| | Hash map | Sorted list | Balanced BST |
|---|----------|-------------|--------------|
| Lookup | **O(1)** avg | O(log n) | O(log n) |
| Insert / delete | **O(1)** avg | O(n) (shifting) | **O(log n)** |
| Min / max | O(n) | **O(1)** | O(log n) |
| Sorted iteration | O(n log n) | **O(n)** | **O(n)** |
| Floor / ceiling / range | ❌ O(n) | O(log n) | **O(log n)** |

> 💡 Choose a BST (in Dart, `SplayTreeMap`/`SplayTreeSet`) when you need **ordering** *and* frequent **inserts/deletes**.

---

## ⚠️ Common Mistakes

### 1. Validating with parent–child comparisons only

Use ranges, or check that the in-order traversal is strictly increasing.

### 2. Forgetting to reattach after recursive insert/delete

Write `n.left = insert(n.left, v)`, not just `insert(n.left, v)`. Otherwise new nodes are created and then lost.

### 3. Assuming O(log n) without balancing

Sorted or nearly sorted input destroys a plain BST's performance.

### 4. Inconsistent duplicate handling

Decide up front: ignore duplicates, count them, or always send them to one side. Mixing rules breaks searches.

---

## 🧪 Try It Yourself

1. Write `kthSmallest(root, k)` using an in-order traversal that stops early.
2. Build a **balanced** BST from a **sorted** list: pick the middle element as the root, recurse on each half.
3. Write `successor(root, x)`: the next larger value after `x`.
4. Count how many nodes have values in `[lo, hi]` without visiting the whole tree.

```dart
class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

Node? fromSorted(List<int> a, [int lo = 0, int? hi]) {
  hi ??= a.length - 1;
  if (lo > hi) return null;
  final mid = (lo + hi) ~/ 2;
  return Node(a[mid], fromSorted(a, lo, mid - 1), fromSorted(a, mid + 1, hi));
}

int height(Node? n) {
  if (n == null) return -1;
  final l = height(n.left), r = height(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  final root = fromSorted(List.generate(1000, (i) => i));
  print(root!.value);   // 499
  print(height(root));  // 9 (perfectly balanced)
}
```

**🔍 What This Code Does:**

1. **Middle as Root**: Half the values go left, half go right.
2. **Recursive Halves**: Each subtree is built the same way.
3. **Minimal Height**: 1,000 nodes fit in height 9, the best possible.

---

## 📌 Key Takeaways

- ✅ A **BST** keeps every left subtree **smaller** and every right subtree **larger** than the node.
- ✅ **Search**, **insert** and **delete** follow one root-to-leaf path: **O(h)**.
- ✅ **In-order traversal** returns values in **sorted order**.
- ✅ Deletion has three cases; nodes with two children are replaced by their **in-order successor**.
- ✅ Validate with **min/max ranges**, not just parent–child checks.
- ✅ BSTs support **floor, ceiling, range** and **LCA** queries efficiently.
- ✅ Height depends on insertion order: **sorted input** creates a linked list. Use **balanced trees** to guarantee O(log n).

**Next up:** ⚖️ **Balanced Trees**: rotations, AVL, red-black trees, and why `SplayTreeMap` exists.
