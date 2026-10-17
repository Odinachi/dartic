# Level-Order Traversal

Imagine dropping a pebble into a still pond 💧. The ripples spread out in rings: first the ring closest to the pebble, then the next one, then the next.

Or picture a company announcing news 📣: the CEO tells the managers, the managers tell their teams, and the teams tell their interns. Each **level** hears it before the next.

👉 That's **level-order traversal**, also called **breadth-first search (BFS)** on a tree:

> **Level-order traversal** visits nodes **level by level**, from the root downward, and **left to right** within each level. It uses a **queue**: first discovered, first visited.

Depth-first traversals (pre/in/post-order) dive **deep** first. Level-order spreads **wide** first.

---

## 🌳 Example

```text
            1               level 0
          /   \
         2     3            level 1
        / \     \
       4   5     6          level 2
          /
         7                  level 3
```

| Traversal | Result |
|-----------|--------|
| Pre-order (DFS) | `1 2 4 5 7 3 6` |
| **Level-order (BFS)** | **`1 2 3 4 5 6 7`** |

---

## 🚶‍♀️ Basic Level-Order With a Queue

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<int> levelOrder(Node? root) {
  final out = <int>[];
  if (root == null) return out;
  final queue = Queue<Node>()..add(root);
  while (queue.isNotEmpty) {
    final n = queue.removeFirst();   // oldest discovered node
    out.add(n.value);
    if (n.left != null) queue.addLast(n.left!);
    if (n.right != null) queue.addLast(n.right!);
  }
  return out;
}

const tree = Node(1,
    Node(2, Node(4), Node(5, Node(7))),
    Node(3, null, Node(6)));

void main() {
  print(levelOrder(tree)); // [1, 2, 3, 4, 5, 6, 7]
}
```

**🔍 What This Code Does:**

This code demonstrates **breadth-first traversal of a binary tree**:

1. **Start With the Root**: The queue begins holding just the root.

2. **Remove From the Front**: `removeFirst()` always takes the node discovered **earliest**.

3. **Add Children to the Back**: Children wait behind every node already in the queue, which includes the rest of the current level.

4. **Why It Works**: All nodes at depth `d` enter the queue before any node at depth `d + 1`, so levels come out in order.

5. **O(n) Time, O(w) Space**: Each node is enqueued and dequeued once; the queue holds at most one full level, where `w` is the tree's maximum **width**.

> 💡 Swap the **queue** for a **stack** and the exact same loop becomes a depth-first (pre-order-like) traversal. The data structure decides the order!

---

## 📚 Grouping Nodes by Level

Many problems need to know **where one level ends**. The trick: before processing a level, record the queue's **current length**. That's exactly how many nodes belong to this level.

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<List<int>> levels(Node? root) {
  final result = <List<int>>[];
  if (root == null) return result;
  final queue = Queue<Node>()..add(root);

  while (queue.isNotEmpty) {
    final levelSize = queue.length; // nodes on this level
    final level = <int>[];
    for (var i = 0; i < levelSize; i++) {
      final n = queue.removeFirst();
      level.add(n.value);
      if (n.left != null) queue.add(n.left!);
      if (n.right != null) queue.add(n.right!);
    }
    result.add(level);
  }
  return result;
}

const tree = Node(1,
    Node(2, Node(4), Node(5, Node(7))),
    Node(3, null, Node(6)));

void main() {
  final byLevel = levels(tree);
  print(byLevel); // [[1], [2, 3], [4, 5, 6], [7]]
  for (final (depth, values) in byLevel.indexed) {
    print('level $depth: $values');
  }
}
```

**🔍 What This Code Does:**

1. **Snapshot the Size**: `levelSize = queue.length` is taken **before** the inner loop adds the next level's children.
2. **Process Exactly One Level**: The inner loop removes exactly `levelSize` nodes.
3. **Children Wait**: Nodes added during the loop belong to the **next** level.
4. **`indexed`**: Pairs each level with its depth for printing.

---

## 🧩 Level-Based Problems

Once you can group by level, lots of problems become easy.

### Right side view

What would you see standing to the **right** of the tree? The **last** node of each level.

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<int> rightSideView(Node? root) {
  final view = <int>[];
  if (root == null) return view;
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      if (i == size - 1) view.add(n.value); // last on this level
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
  }
  return view;
}

void main() {
  const t = Node(1, Node(2, null, Node(5)), Node(3, null, Node(4)));
  print(rightSideView(t)); // [1, 3, 4]

  const leftHeavy = Node(1, Node(2, Node(4)), Node(3));
  print(rightSideView(leftHeavy)); // [1, 3, 4] (4 is visible from the right!)
}
```

**🔍 What This Code Does:**

1. **Last of Each Level**: `i == size - 1` identifies the rightmost node of the level.
2. **Not Just the Right Edge**: In `leftHeavy`, node `4` is on the left side, but it's the only node at level 2, so it's visible.

### Level averages

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<double> levelAverages(Node root) {
  final out = <double>[];
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    var sum = 0;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      sum += n.value;
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
    out.add(sum / size);
  }
  return out;
}

void main() {
  const t = Node(3, Node(9), Node(20, Node(15), Node(7)));
  print(levelAverages(t)); // [3.0, 14.5, 11.0]
}
```

**🔍 What This Code Does:**

1. **Sum per Level**: Accumulate values only within the current level.
2. **Divide by the Level Size**: `sum / size` gives a `double`.

### Minimum depth (BFS stops early!)

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

int minDepth(Node? root) {
  if (root == null) return 0;
  final q = Queue<(Node, int)>()..add((root, 1));
  while (q.isNotEmpty) {
    final (n, depth) = q.removeFirst();
    if (n.left == null && n.right == null) return depth; // first leaf found
    if (n.left != null) q.add((n.left!, depth + 1));
    if (n.right != null) q.add((n.right!, depth + 1));
  }
  return 0;
}

void main() {
  const t = Node(1,
      Node(2, Node(4, Node(8), Node(9)), Node(5)),
      Node(3));
  print(minDepth(t)); // 2 (node 3 is a leaf at depth 2)
}
```

**🔍 What This Code Does:**

1. **Depth Travels With Each Node**: The queue stores `(node, depth)` records.
2. **First Leaf Wins**: BFS reaches shallow nodes first, so the **first** leaf dequeued has the minimum depth.
3. **Early Exit**: The deep left subtree is never fully explored. A DFS would have to visit every node to be sure.

> 💡 **Rule of thumb:** when the question is about the **nearest** or **shallowest** something, BFS can stop early. When it's about the **deepest** or **all paths**, DFS is often simpler.

### Zigzag level order

Alternate directions: left-to-right, then right-to-left, and so on.

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

List<List<int>> zigzag(Node? root) {
  final result = <List<int>>[];
  if (root == null) return result;
  final q = Queue<Node>()..add(root);
  var leftToRight = true;
  while (q.isNotEmpty) {
    final size = q.length;
    final level = ListQueue<int>(); // a deque!
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      if (leftToRight) {
        level.addLast(n.value);
      } else {
        level.addFirst(n.value);
      }
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
    result.add(level.toList());
    leftToRight = !leftToRight;
  }
  return result;
}

void main() {
  const t = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)));
  print(zigzag(t)); // [[1], [3, 2], [4, 5, 6, 7]]
}
```

**🔍 What This Code Does:**

1. **Normal BFS Order**: Nodes are always dequeued left to right.
2. **Deque for Output**: On right-to-left levels, `addFirst` reverses the order as values are added.
3. **Toggle**: `leftToRight = !leftToRight` flips direction after each level.

---

## 🌐 Level-Order on General Trees

The same idea works for trees with any number of children, like a company org chart.

```dart
import 'dart:collection';

class Employee {
  final String name;
  final List<Employee> reports;
  const Employee(this.name, [this.reports = const []]);
}

void main() {
  const ceo = Employee('Ada (CEO)', [
    Employee('Bob (CTO)', [Employee('Dev 1'), Employee('Dev 2')]),
    Employee('Cy (CFO)', [Employee('Accountant')]),
  ]);

  final q = Queue<(Employee, int)>()..add((ceo, 0));
  while (q.isNotEmpty) {
    final (e, level) = q.removeFirst();
    print('${'  ' * level}level $level: ${e.name}');
    for (final r in e.reports) {
      q.add((r, level + 1));
    }
  }
}
```

**🔍 What This Code Does:**

1. **Any Number of Children**: Loop over `reports` instead of checking `left`/`right`.
2. **Announcements Flow Down**: Everyone at level 1 is printed before anyone at level 2.
3. **Real Uses**: Org charts, category menus, folder listings one level at a time.

---

## 🔗 Connecting Nodes on the Same Level

A classic: point every node's `next` to the node on its right in the same level (or `null` at the end).

```dart
import 'dart:collection';

class Node {
  final int value;
  Node? left, right, next;
  Node(this.value, [this.left, this.right]);
}

void connect(Node? root) {
  if (root == null) return;
  final q = Queue<Node>()..add(root);
  while (q.isNotEmpty) {
    final size = q.length;
    Node? prev;
    for (var i = 0; i < size; i++) {
      final n = q.removeFirst();
      prev?.next = n; // link the previous node on this level to n
      prev = n;
      if (n.left != null) q.add(n.left!);
      if (n.right != null) q.add(n.right!);
    }
  }
}

void main() {
  final root = Node(1, Node(2, Node(4), Node(5)), Node(3, null, Node(7)));
  connect(root);
  print(root.left!.next!.value);        // 3
  print(root.left!.right!.next!.value); // 7
  print(root.right!.next);              // null
}
```

**🔍 What This Code Does:**

1. **`prev` per Level**: Reset to `null` at the start of each level.
2. **Null-Aware Assignment**: `prev?.next = n` does nothing for the first node of the level.
3. **Last Node Stays Null**: Its `next` is never assigned.

---

## 📐 BFS vs DFS on Trees

| | BFS (level-order) | DFS (pre/in/post-order) |
|---|-------------------|-------------------------|
| Data structure | Queue | Stack / recursion |
| Order | Level by level | Branch by branch |
| Extra space | O(max width) | O(height) |
| Best for | Nearest/shallowest, per-level answers | Paths, subtree computations, sorted BST output |
| Wide, shallow tree | 😬 Large queue | ✅ Small stack |
| Deep, narrow tree | ✅ Small queue | 😬 Deep stack |

> 💡 In a perfect binary tree, the last level holds about **half** of all nodes, so BFS can need O(n) memory, while DFS needs only O(log n).

---

## ⚠️ Common Mistakes

### 1. Using `List.removeAt(0)` as the queue

Each `removeAt(0)` is O(n), making the traversal O(n²). Use `Queue` from `dart:collection`.

### 2. Reading `queue.length` inside the loop condition

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>.from([1, 2]);
  var processed = 0;
  // ❌ for (var i = 0; i < q.length; i++) { ...q.add(...) } keeps growing
  final size = q.length; // ✅ snapshot first
  for (var i = 0; i < size; i++) {
    final x = q.removeFirst();
    q.add(x * 10); // next level
    processed++;
  }
  print('processed $processed, next level: $q'); // processed 2, next level: {10, 20}
}
```

**🔍 What This Code Does:**

1. **Moving Target**: `q.length` changes as you remove and add, so it can't mark a level boundary.
2. **Snapshot**: Saving `size` first processes exactly one level.

### 3. Forgetting the empty-tree case

Adding a `null` root to the queue leads to null errors. Check `root == null` first.

### 4. Assuming BFS always saves memory

BFS memory depends on **width**. For wide trees, DFS can be far lighter.

---

## 🧪 Try It Yourself

1. **Bottom-up level order**: return levels from the deepest to the root.
2. **Largest value in each level**.
3. **Maximum width**: the most nodes on any level.
4. **Is the tree complete?** BFS until the first missing child; after that, every node must be a leaf with no children.

```dart
import 'dart:collection';

class Node {
  final int value;
  final Node? left, right;
  const Node(this.value, [this.left, this.right]);
}

bool isComplete(Node? root) {
  final q = Queue<Node?>()..add(root);
  var seenGap = false;
  while (q.isNotEmpty) {
    final n = q.removeFirst();
    if (n == null) {
      seenGap = true;
    } else {
      if (seenGap) return false; // a node after a gap
      q
        ..add(n.left)
        ..add(n.right);
    }
  }
  return true;
}

void main() {
  print(isComplete(const Node(1, Node(2, Node(4)), Node(3))));       // true
  print(isComplete(const Node(1, Node(2, null, Node(5)), Node(3)))); // false
}
```

**🔍 What This Code Does:**

1. **Queue of Nullable Nodes**: Missing children are enqueued as `null` gaps.
2. **Gap Rule**: In a complete tree, once a gap appears in level order, no real node can follow.
3. **O(n)**: Every node and gap is processed once.

---

## 📌 Key Takeaways

- ✅ **Level-order (BFS)** visits nodes level by level, left to right, using a **queue**.
- ✅ Snapshot **`queue.length`** at the start of a level to process exactly one level.
- ✅ Per-level problems (right view, averages, zigzag, connecting `next` pointers) all reuse that pattern.
- ✅ BFS finds the **shallowest** answer first and can **stop early** (minimum depth).
- ✅ BFS uses **O(width)** memory; DFS uses **O(height)**.
- ✅ Swapping the queue for a stack turns BFS into DFS: the structure defines the order.

**Next up:** 🔎 **Binary Search Trees**: keep data sorted for O(log n) search, insert and delete.
