# Segment & Fenwick Trees

Imagine running a **live leaderboard** for a game with 1,000,000 players 🎮.

- Players' scores change **all the time** (point updates).
- Analysts constantly ask: *"What's the total score of players #2,000 to #500,000?"* or *"Who has the highest score between #10 and #9,000?"* (range queries).

With a plain list, an update is O(1) but a range sum is O(n). With **prefix sums**, a range sum is O(1) but every update forces O(n) rebuilding. Neither survives a stream of millions of both.

👉 That's what **segment trees** and **Fenwick trees** solve:

> A **segment tree** stores aggregate answers (sum, min, max, ...) for **ranges** of the array in a binary tree, supporting **range queries** and **point updates** in **O(log n)**.
> A **Fenwick tree** (Binary Indexed Tree) is a compact, clever array-based structure for **prefix sums with updates**, also **O(log n)**, in just a few lines of code.

---

## 📊 The Trade-off Table

| Structure | Update one value | Range sum | Range min/max | Memory |
|-----------|------------------|-----------|---------------|--------|
| Plain list | **O(1)** | O(n) | O(n) | O(n) |
| Prefix sums | O(n) rebuild | **O(1)** | ❌ | O(n) |
| **Fenwick tree** | **O(log n)** | **O(log n)** | ❌ (not directly) | **O(n)**, tiny |
| **Segment tree** | **O(log n)** | **O(log n)** | **O(log n)** | O(n) (about 2–4n) |

---

## 🌳 Segment Trees: The Idea

Each node stores the answer for a **segment** (range) of the array. The root covers everything; each node's children split its range in half; leaves cover single elements.

```text
Array: [5, 8, 6, 3, 2, 7, 2, 6]   (indexes 0..7)

                        [0-7] 39
                 /                    \
          [0-3] 22                    [4-7] 17
          /       \                   /       \
     [0-1] 13   [2-3] 9         [4-5] 9    [6-7] 8
      /   \      /   \           /   \      /   \
     5     8    6     3         2     7    2     6
```

- **Query** `sum(2..5)`: combine just a few nodes that exactly cover the range: `[2-3] 9` + `[4-5] 9` = **18**.
- **Update** `a[3] = 10`: change the leaf, then fix every ancestor on the path to the root (log n nodes).

### Array storage

Like a heap, store the tree in a list: node `i` has children `2i` and `2i + 1` (1-based). An array of size `4n` is always enough.

---

## 🏗️ A Sum Segment Tree

```dart
class SegmentTree {
  final int n;
  final List<int> tree;

  SegmentTree(List<int> data)
      : n = data.length,
        tree = List.filled(4 * data.length, 0) {
    _build(data, 1, 0, n - 1);
  }

  void _build(List<int> data, int node, int lo, int hi) {
    if (lo == hi) {
      tree[node] = data[lo]; // leaf
      return;
    }
    final mid = (lo + hi) ~/ 2;
    _build(data, 2 * node, lo, mid);
    _build(data, 2 * node + 1, mid + 1, hi);
    tree[node] = tree[2 * node] + tree[2 * node + 1]; // combine children
  }

  /// Sum of data[l..r] (inclusive)
  int query(int l, int r) => _query(1, 0, n - 1, l, r);

  int _query(int node, int lo, int hi, int l, int r) {
    if (r < lo || hi < l) return 0;        // no overlap
    if (l <= lo && hi <= r) return tree[node]; // total overlap: use this node
    final mid = (lo + hi) ~/ 2;            // partial overlap: ask both children
    return _query(2 * node, lo, mid, l, r) + _query(2 * node + 1, mid + 1, hi, l, r);
  }

  /// data[index] = value
  void update(int index, int value) => _update(1, 0, n - 1, index, value);

  void _update(int node, int lo, int hi, int index, int value) {
    if (lo == hi) {
      tree[node] = value;
      return;
    }
    final mid = (lo + hi) ~/ 2;
    if (index <= mid) {
      _update(2 * node, lo, mid, index, value);
    } else {
      _update(2 * node + 1, mid + 1, hi, index, value);
    }
    tree[node] = tree[2 * node] + tree[2 * node + 1]; // fix the ancestor
  }
}

void main() {
  final st = SegmentTree([5, 8, 6, 3, 2, 7, 2, 6]);
  print(st.query(0, 7)); // 39
  print(st.query(2, 5)); // 18
  st.update(3, 10);      // 3 → 10
  print(st.query(2, 5)); // 25
  print(st.query(3, 3)); // 10
}
```

**🔍 What This Code Does:**

This code demonstrates **a recursive segment tree for range sums**:

1. **Build in O(n)**: Leaves copy the data; each internal node stores the sum of its two children.

2. **Three Query Cases**:
   - **No overlap**: the node's range is outside `[l, r]`, contributes `0`.
   - **Total overlap**: the node's range is inside `[l, r]`, use its stored sum directly.
   - **Partial overlap**: split and ask both children.

3. **O(log n) Query**: At most about 4 nodes per level are visited.

4. **Point Update in O(log n)**: Walk down to the leaf, change it, and recompute sums on the way back up.

5. **Identity Value**: `0` is the "neutral" value for sums (adding it changes nothing).

---

## 🔁 Any Associative Operation Works

Change the **combine** function and the **identity value**, and the same tree answers different questions.

| Query | Combine | Identity |
|-------|---------|----------|
| Range sum | `a + b` | `0` |
| Range min | `min(a, b)` | `+∞` |
| Range max | `max(a, b)` | `−∞` |
| Range GCD | `gcd(a, b)` | `0` |
| Range product | `a * b` | `1` |

```dart
import 'dart:math';

class GenericSegmentTree<T> {
  final int n;
  final List<T> tree;
  final T identity;
  final T Function(T, T) combine;

  GenericSegmentTree(List<T> data, this.identity, this.combine)
      : n = data.length,
        tree = List.filled(2 * data.length, identity) {
    // Iterative, bottom-up layout: leaves live at tree[n .. 2n-1]
    for (var i = 0; i < n; i++) {
      tree[n + i] = data[i];
    }
    for (var i = n - 1; i > 0; i--) {
      tree[i] = combine(tree[2 * i], tree[2 * i + 1]);
    }
  }

  void update(int index, T value) {
    var i = index + n;
    tree[i] = value;
    while (i > 1) {
      i ~/= 2;
      tree[i] = combine(tree[2 * i], tree[2 * i + 1]);
    }
  }

  /// Aggregate over the half-open range [l, r)
  T query(int l, int r) {
    var resLeft = identity, resRight = identity;
    var lo = l + n, hi = r + n;
    while (lo < hi) {
      if (lo.isOdd) resLeft = combine(resLeft, tree[lo++]);
      if (hi.isOdd) resRight = combine(tree[--hi], resRight);
      lo ~/= 2;
      hi ~/= 2;
    }
    return combine(resLeft, resRight);
  }
}

void main() {
  final temps = [21, 25, 19, 30, 17, 28, 23];
  final maxTree = GenericSegmentTree<int>(temps, -1 << 62, max);
  final minTree = GenericSegmentTree<int>(temps, 1 << 62, min);

  print(maxTree.query(0, 4)); // 30 (max of days 0..3)
  print(minTree.query(2, 7)); // 17 (min of days 2..6)
  maxTree.update(1, 35);
  print(maxTree.query(0, 4)); // 35
}
```

**🔍 What This Code Does:**

1. **Generic Type `T`**: The same tree class handles sums, mins, maxes or anything associative.
2. **Function Parameters**: `max` and `min` from `dart:math` are passed directly as `combine`.
3. **Iterative Layout (2n Size)**: Leaves sit at `tree[n..2n−1]`; parent `i` covers children `2i` and `2i + 1`. No recursion needed.
4. **Half-Open Queries `[l, r)`**: The loop climbs from both ends, collecting nodes that are fully inside the range.
5. **Order Preserved**: `resLeft` and `resRight` are combined in order, so non-commutative operations also work.

---

## 🪄 Fenwick Tree (Binary Indexed Tree)

A Fenwick tree stores **partial sums** in a 1-based array, where index `i` is responsible for a range whose length is the **lowest set bit** of `i`.

```text
i (binary)   lowbit(i)   tree[i] stores sum of...
1  (0001)        1        a[1]
2  (0010)        2        a[1..2]
3  (0011)        1        a[3]
4  (0100)        4        a[1..4]
5  (0101)        1        a[5]
6  (0110)        2        a[5..6]
7  (0111)        1        a[7]
8  (1000)        8        a[1..8]
```

The magic formula: `i & -i` isolates the **lowest set bit** of `i`.

- **Prefix sum** of `1..i`: add `tree[i]`, then jump `i -= i & -i` until 0.
- **Update** at `i`: add to `tree[i]`, then jump `i += i & -i` until past n.

```dart
class Fenwick {
  final List<int> _tree; // 1-based

  Fenwick(int n) : _tree = List.filled(n + 1, 0);

  factory Fenwick.from(List<int> data) {
    final f = Fenwick(data.length);
    for (var i = 0; i < data.length; i++) {
      f.add(i, data[i]);
    }
    return f;
  }

  /// data[index] += delta (index is 0-based)
  void add(int index, int delta) {
    for (var i = index + 1; i < _tree.length; i += i & -i) {
      _tree[i] += delta;
    }
  }

  /// Sum of data[0..index] (inclusive, 0-based)
  int prefixSum(int index) {
    var sum = 0;
    for (var i = index + 1; i > 0; i -= i & -i) {
      sum += _tree[i];
    }
    return sum;
  }

  /// Sum of data[l..r] (inclusive)
  int rangeSum(int l, int r) => prefixSum(r) - (l > 0 ? prefixSum(l - 1) : 0);
}

void main() {
  final scores = Fenwick.from([5, 8, 6, 3, 2, 7, 2, 6]);
  print(scores.rangeSum(0, 7)); // 39
  print(scores.rangeSum(2, 5)); // 18
  scores.add(3, 7);             // 3 → 10 (add the difference)
  print(scores.rangeSum(2, 5)); // 25

  print(6 & -6); // 2: lowest set bit of 0b110
  print(8 & -8); // 8
}
```

**🔍 What This Code Does:**

1. **1-Based Internals**: Index 0 has no lowest set bit, so the tree uses indexes `1..n`; the public API stays 0-based.
2. **`add` Climbs Up**: `i += i & -i` visits every node whose range includes `index`.
3. **`prefixSum` Climbs Down**: `i -= i & -i` collects disjoint chunks that together cover `1..i`.
4. **Range Sum = Difference of Prefixes**: Just like plain prefix sums, but with O(log n) updates.
5. **Deltas, Not Values**: Fenwick updates **add** a change; to set a value, add `newValue − oldValue`.
6. **`factory` Constructor**: Builds and fills the tree in one call (O(n log n); an O(n) build also exists).

**Why `i & -i` works:** In two's complement, `-i` is `~i + 1`, which flips every bit above the lowest 1 and keeps that 1. ANDing leaves only the lowest set bit.

---

## 🧮 Classic Applications

### Counting smaller elements to the right

```dart
class Fenwick {
  final List<int> t;
  Fenwick(int n) : t = List.filled(n + 1, 0);
  void add(int i, int d) {
    for (i++; i < t.length; i += i & -i) {
      t[i] += d;
    }
  }

  int sum(int i) {
    var s = 0;
    for (i++; i > 0; i -= i & -i) {
      s += t[i];
    }
    return s;
  }
}

List<int> smallerToRight(List<int> nums) {
  // Values are small non-negative ints here; compress them otherwise
  final maxV = nums.reduce((a, b) => a > b ? a : b);
  final bit = Fenwick(maxV + 1);
  final result = List<int>.filled(nums.length, 0);
  for (var i = nums.length - 1; i >= 0; i--) {
    result[i] = nums[i] > 0 ? bit.sum(nums[i] - 1) : 0; // how many seen values are smaller
    bit.add(nums[i], 1);                                 // record this value
  }
  return result;
}

void main() {
  print(smallerToRight([5, 2, 6, 1])); // [2, 1, 1, 0]
}
```

**🔍 What This Code Does:**

1. **Scan From the Right**: Values to the right have already been recorded in the tree.
2. **Tree Over Values**: The Fenwick tree counts how many times each **value** has been seen.
3. **Prefix Count**: `sum(v − 1)` = how many seen values are smaller than `v`.
4. **O(n log V)**: Versus O(n²) checking every pair. (For large values, first map them to ranks 0..n−1: **coordinate compression**.)

### Live leaderboard with range max

```dart
import 'dart:math';

void main() {
  // Iterative max segment tree (size 2n)
  final scores = [120, 340, 90, 560, 210, 430];
  final n = scores.length;
  final tree = List<int>.filled(2 * n, 0);
  for (var i = 0; i < n; i++) {
    tree[n + i] = scores[i];
  }
  for (var i = n - 1; i > 0; i--) {
    tree[i] = max(tree[2 * i], tree[2 * i + 1]);
  }

  int bestIn(int l, int r) { // [l, r)
    var best = 0;
    for (var lo = l + n, hi = r + n; lo < hi; lo ~/= 2, hi ~/= 2) {
      if (lo.isOdd) best = max(best, tree[lo++]);
      if (hi.isOdd) best = max(best, tree[--hi]);
    }
    return best;
  }

  void setScore(int i, int v) {
    var p = i + n;
    tree[p] = v;
    for (p ~/= 2; p >= 1; p ~/= 2) {
      tree[p] = max(tree[2 * p], tree[2 * p + 1]);
    }
  }

  print(bestIn(0, 3)); // 340
  setScore(2, 999);
  print(bestIn(0, 3)); // 999
  print(bestIn(3, 6)); // 560
}
```

**🔍 What This Code Does:**

1. **Range Max**: Something prefix sums and Fenwick trees can't do directly.
2. **Updates Propagate Up**: A new high score updates log n ancestors.
3. **Local Functions**: `bestIn` and `setScore` capture `tree` and `n` from `main`.

---

## ⚖️ Segment Tree vs Fenwick Tree

| | Segment tree | Fenwick tree |
|---|--------------|--------------|
| Operations | Any associative combine (sum, min, max, gcd...) | Mainly sums (invertible operations) |
| Range min/max | ✅ | ❌ (not with simple updates) |
| Code size | Larger | **Tiny** (~10 lines) |
| Memory | 2n–4n | **n + 1** |
| Constant factors | Slower | **Faster** |
| Range updates (lazy propagation) | ✅ Advanced extension | Possible for sums with tricks |

> 💡 Rule of thumb: need **sums with updates**? Use a **Fenwick tree**. Need **min/max** or something fancier? Use a **segment tree**.

---

## ⚠️ Common Mistakes

### 1. Mixing 0-based and 1-based indexes in a Fenwick tree

The internal array is 1-based. Convert at the boundary (`index + 1`) and nowhere else.

### 2. Using `set` semantics with Fenwick `add`

`add(i, 10)` **adds** 10; it doesn't set the value to 10. Track the old values to compute deltas.

### 3. Wrong identity value

Using `0` as the identity for a **min** tree gives wrong answers when all values are positive. Use a very large number.

### 4. Allocating too little space

A recursive segment tree needs up to **4n** slots. Using `2n` with the recursive layout can overflow the array.

---

## 🧪 Try It Yourself

1. Add `count of values ≥ x in a range` to a segment tree storing sorted lists in each node (a "merge sort tree").
2. Use a Fenwick tree to count **inversions** in O(n log n).
3. Build a **2D Fenwick tree** for rectangle sums with point updates.
4. Implement **lazy propagation** for "add v to every element in [l, r]" with range-sum queries.

---

## 📌 Key Takeaways

- ✅ Plain arrays are fast to update, prefix sums are fast to query; **segment** and **Fenwick** trees are fast at **both**: **O(log n)**.
- ✅ A **segment tree** stores aggregates for ranges in a binary tree; queries combine **O(log n)** nodes using **no / total / partial overlap**.
- ✅ Segment trees work for any **associative** operation: sum, min, max, gcd, product.
- ✅ A **Fenwick tree** stores partial sums indexed by the **lowest set bit** (`i & -i`); updates climb up, prefix sums climb down.
- ✅ Fenwick trees are tiny and fast for **sums**; segment trees are more **flexible**.
- ✅ Watch indexes (0- vs 1-based), identity values and add-vs-set semantics.

**Next up:** 🗃️ **LRU Cache**: combining a hash map and a linked list for O(1) caching.
