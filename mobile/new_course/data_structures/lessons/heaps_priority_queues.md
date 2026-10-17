# Heaps & Priority Queues

Imagine a hospital **emergency room** 🏥.

- Patients don't get treated in arrival order. A heart attack goes **before** a sprained ankle, even if the ankle arrived first.
- New patients keep arriving, and the doctor always asks: *"Who's the **most urgent** right now?"*

A normal queue (FIFO) can't do this. Sorting the whole waiting list every time someone arrives would be slow.

👉 That's what a **priority queue** is for, and a **heap** is how it's built:

> A **priority queue** lets you add items and always remove the one with the **highest priority** (or lowest value). A **binary heap** implements it as a **complete binary tree stored in an array**, giving **O(log n)** add/remove and **O(1)** peek.

---

## 🧠 The Heap Property

A **min-heap** is a complete binary tree where **every parent is ≤ its children**. So the **smallest** element is always at the **root**.

```text
              1
           /     \
          3       2
         / \     / \
        7   4   5   9
       /
      8
```

- `1 ≤ 3` and `1 ≤ 2` ✅, `3 ≤ 7`, `3 ≤ 4` ✅, and so on.
- Siblings have **no** order between them (`3` is left of `2`). A heap is **not** sorted; it only guarantees the root is the minimum.

A **max-heap** is the mirror image: every parent is ≥ its children, so the largest is at the root.

| | BST | Heap |
|---|-----|------|
| Order rule | left < node < right | parent ≤ children |
| Find min | O(log n) | **O(1)** |
| Find any value | O(log n) | O(n) |
| Shape | Any (balanced if lucky) | Always **complete** |
| Storage | Nodes with pointers | **A plain array** |

---

## 🗂️ Storing a Tree in an Array

Because a heap is **complete** (every level full except the last, filled left to right), we can store it in a list with **no gaps and no pointers**:

```text
index:   0  1  2  3  4  5  6  7
value: [ 1, 3, 2, 7, 4, 5, 9, 8 ]
```

For the node at index `i`:

| Relative | Index |
|----------|-------|
| Left child | `2i + 1` |
| Right child | `2i + 2` |
| Parent | `(i − 1) ~/ 2` |

```dart
void main() {
  final heap = [1, 3, 2, 7, 4, 5, 9, 8];
  const i = 1; // value 3
  print('node ${heap[i]}');
  print('left child ${heap[2 * i + 1]}');   // 7
  print('right child ${heap[2 * i + 2]}');  // 4
  print('parent ${heap[(i - 1) ~/ 2]}');    // 1
}
```

**🔍 What This Code Does:**

1. **No Node Objects**: The tree shape is implied by the indexes.
2. **Children of i**: Always at `2i + 1` and `2i + 2`.
3. **Parent of i**: `(i − 1) ~/ 2`, using integer division.
4. **Cache-Friendly**: One contiguous list is fast and memory-efficient.

---

## ⬆️ Insert: Bubble Up (Sift Up)

1. Add the new value at the **end** of the array (the next free spot in the last level).
2. While it's **smaller than its parent**, **swap** them.

```text
insert 0 into [1, 3, 2, 7, 4, 5, 9, 8]:

add at end → [1, 3, 2, 7, 4, 5, 9, 8, 0]   (0 is child of 7)
swap with 7 → [1, 3, 2, 0, 4, 5, 9, 8, 7]
swap with 3 → [1, 0, 2, 3, 4, 5, 9, 8, 7]
swap with 1 → [0, 1, 2, 3, 4, 5, 9, 8, 7]   ✅ new root
```

## ⬇️ Remove the Minimum: Bubble Down (Sift Down)

1. Save the root (the minimum).
2. Move the **last** element to the root and shrink the array.
3. While it's **bigger than its smaller child**, **swap** with that child.

Both operations walk one path of the tree, so they're **O(log n)**.

---

## 🏗️ Building a `MinHeap<T>`

```dart
class MinHeap<T> {
  final List<T> _data = [];
  final int Function(T a, T b) _compare;

  MinHeap(this._compare);

  int get length => _data.length;
  bool get isEmpty => _data.isEmpty;

  T get peek {
    if (_data.isEmpty) throw StateError('Heap is empty');
    return _data.first; // O(1)
  }

  void add(T value) {
    _data.add(value);
    _siftUp(_data.length - 1); // O(log n)
  }

  T removeMin() {
    if (_data.isEmpty) throw StateError('Heap is empty');
    final min = _data.first;
    final last = _data.removeLast();
    if (_data.isNotEmpty) {
      _data[0] = last;
      _siftDown(0); // O(log n)
    }
    return min;
  }

  void _siftUp(int i) {
    while (i > 0) {
      final parent = (i - 1) ~/ 2;
      if (_compare(_data[i], _data[parent]) >= 0) break;
      _swap(i, parent);
      i = parent;
    }
  }

  void _siftDown(int i) {
    final n = _data.length;
    while (true) {
      final left = 2 * i + 1, right = left + 1;
      var smallest = i;
      if (left < n && _compare(_data[left], _data[smallest]) < 0) smallest = left;
      if (right < n && _compare(_data[right], _data[smallest]) < 0) smallest = right;
      if (smallest == i) return;
      _swap(i, smallest);
      i = smallest;
    }
  }

  void _swap(int a, int b) {
    final t = _data[a];
    _data[a] = _data[b];
    _data[b] = t;
  }

  @override
  String toString() => _data.toString();
}

void main() {
  final heap = MinHeap<int>((a, b) => a.compareTo(b));
  for (final x in [5, 3, 8, 1, 9, 2]) {
    heap.add(x);
  }
  print(heap);        // [1, 3, 2, 5, 9, 8] (a valid heap, not sorted)
  print(heap.peek);   // 1

  final sorted = <int>[];
  while (!heap.isEmpty) {
    sorted.add(heap.removeMin());
  }
  print(sorted);      // [1, 2, 3, 5, 8, 9]
}
```

**🔍 What This Code Does:**

This code demonstrates **a generic binary min-heap**:

1. **Comparator**: `_compare(a, b)` returns negative if `a` should come first. Pass a reversed comparator to get a **max-heap**.

2. **`add`**: Appends to the end and sifts up while smaller than the parent.

3. **`removeMin`**: Takes the root, moves the last element to the top, and sifts down toward the smaller child.

4. **Always Pick the Smaller Child**: Swapping with the larger child would break the heap property.

5. **Not Sorted Inside**: `[1, 3, 2, 5, 9, 8]` only guarantees the root is smallest; removing repeatedly yields sorted order.

| Operation | Cost |
|-----------|------|
| `peek` | O(1) |
| `add` | O(log n) |
| `removeMin` | O(log n) |
| Search for an arbitrary value | O(n) |

---

## 🏥 A Real Priority Queue: Emergency Room

```dart
class MinHeap<T> {
  final List<T> _d = [];
  final int Function(T, T) _cmp;
  MinHeap(this._cmp);

  bool get isEmpty => _d.isEmpty;

  void add(T v) {
    _d.add(v);
    var i = _d.length - 1;
    while (i > 0) {
      final p = (i - 1) ~/ 2;
      if (_cmp(_d[i], _d[p]) >= 0) break;
      final tmp = _d[i]; // swap with a record pattern
      _d[i] = _d[p];
      _d[p] = tmp;
      i = p;
    }
  }

  T remove() {
    final top = _d.first, last = _d.removeLast();
    if (_d.isNotEmpty) {
      _d[0] = last;
      var i = 0;
      while (true) {
        final l = 2 * i + 1, r = l + 1;
        var m = i;
        if (l < _d.length && _cmp(_d[l], _d[m]) < 0) m = l;
        if (r < _d.length && _cmp(_d[r], _d[m]) < 0) m = r;
        if (m == i) break;
        final tmp = _d[i];
        _d[i] = _d[m];
        _d[m] = tmp;
        i = m;
      }
    }
    return top;
  }
}

typedef Patient = ({String name, int urgency, int arrival});

void main() {
  // Lower urgency number = more urgent. Ties: whoever arrived first.
  final er = MinHeap<Patient>((a, b) {
    final c = a.urgency.compareTo(b.urgency);
    return c != 0 ? c : a.arrival.compareTo(b.arrival);
  });

  var clock = 0;
  void arrive(String name, int urgency) =>
      er.add((name: name, urgency: urgency, arrival: clock++));

  arrive('Sam (sprained ankle)', 4);
  arrive('Rita (chest pain)', 1);
  arrive('Omar (broken arm)', 3);
  arrive('Lena (allergic reaction)', 1);
  arrive('Tom (cold)', 5);

  while (!er.isEmpty) {
    final p = er.remove();
    print('🩺 urgency ${p.urgency}: ${p.name}');
  }
}
```

**🔍 What This Code Does:**

1. **Named Record Type**: `typedef Patient = ({String name, int urgency, int arrival})` gives the record a readable name.
2. **Two-Level Comparator**: Sort by urgency, then by arrival time, so equally urgent patients are served fairly.
3. **Swap With a Temporary**: `tmp` holds one value while two list slots trade places.
4. **Output Order**: Rita, Lena (both urgency 1, Rita arrived first), Omar, Sam, Tom.
5. **O(log n) per Patient**: Even with thousands waiting.

---

## 🧱 Heapify: Build a Heap in O(n)

Adding n items one at a time costs O(n log n). But if you already have all the items, you can **heapify** in **O(n)**: sift down every non-leaf node, from the last one back to the root.

```dart
void siftDown(List<int> a, int i, int n) {
  while (true) {
    final l = 2 * i + 1, r = l + 1;
    var m = i;
    if (l < n && a[l] < a[m]) m = l;
    if (r < n && a[r] < a[m]) m = r;
    if (m == i) return;
    final t = a[i];
    a[i] = a[m];
    a[m] = t;
    i = m;
  }
}

void heapify(List<int> a) {
  for (var i = a.length ~/ 2 - 1; i >= 0; i--) {
    siftDown(a, i, a.length);
  }
}

void main() {
  final a = [9, 4, 7, 1, 8, 2, 6];
  heapify(a);
  print(a);    // [1, 4, 2, 9, 8, 7, 6]
  print(a[0]); // 1
}
```

**🔍 What This Code Does:**

1. **Leaves Are Already Heaps**: The second half of the array are leaves, so we start at `length ~/ 2 − 1`.
2. **Work Backwards**: Each sift-down fixes a subtree whose children are already valid heaps.
3. **Why O(n)?**: Most nodes are near the bottom and sift down only a little. The total work sums to about 2n.

---

## 🔢 Heap Sort

Heapify, then repeatedly move the root to the end of the array:

```dart
void heapSort(List<int> a) {
  void siftDown(int i, int n) {
    while (true) {
      final l = 2 * i + 1, r = l + 1;
      var m = i;
      if (l < n && a[l] > a[m]) m = l; // max-heap for ascending output
      if (r < n && a[r] > a[m]) m = r;
      if (m == i) return;
      final tmp = a[i];
      a[i] = a[m];
      a[m] = tmp;
      i = m;
    }
  }

  for (var i = a.length ~/ 2 - 1; i >= 0; i--) {
    siftDown(i, a.length); // build max-heap
  }
  for (var end = a.length - 1; end > 0; end--) {
    final tmp = a[0]; // move max to its final spot
    a[0] = a[end];
    a[end] = tmp;
    siftDown(0, end);                // restore the heap on the rest
  }
}

void main() {
  final a = [5, 1, 9, 3, 7, 2];
  heapSort(a);
  print(a); // [1, 2, 3, 5, 7, 9]
}
```

**🔍 What This Code Does:**

1. **Max-Heap**: The largest element is at index 0.
2. **Swap to the End**: The maximum goes to its final sorted position.
3. **Shrink the Heap**: The heap now covers `0..end − 1`; sift down to fix the root.
4. **O(n log n), In Place**: No extra list needed, though it isn't stable.

---

## 🏆 Top-K Problems

**Problem:** Find the `k` largest numbers in a huge list (or an endless stream).

**Trick:** Keep a **min-heap of size k**. The root is the smallest of your current top k; any bigger number replaces it.

```dart
import 'dart:math';

class MinHeap {
  final _d = <int>[];
  int get length => _d.length;
  int get peek => _d.first;

  void add(int v) {
    _d.add(v);
    var i = _d.length - 1;
    while (i > 0 && _d[(i - 1) ~/ 2] > _d[i]) {
      final p = (i - 1) ~/ 2;
      final tmp = _d[i];
      _d[i] = _d[p];
      _d[p] = tmp;
      i = p;
    }
  }

  int removeMin() {
    final top = _d.first, last = _d.removeLast();
    if (_d.isNotEmpty) {
      _d[0] = last;
      var i = 0;
      while (true) {
        final l = 2 * i + 1, r = l + 1;
        var m = i;
        if (l < _d.length && _d[l] < _d[m]) m = l;
        if (r < _d.length && _d[r] < _d[m]) m = r;
        if (m == i) break;
        final tmp = _d[i];
        _d[i] = _d[m];
        _d[m] = tmp;
        i = m;
      }
    }
    return top;
  }

  List<int> toList() => List.of(_d);
}

List<int> topK(Iterable<int> stream, int k) {
  final heap = MinHeap();
  for (final x in stream) {
    if (heap.length < k) {
      heap.add(x);
    } else if (x > heap.peek) {
      heap.removeMin(); // drop the smallest of the current top k
      heap.add(x);
    }
  }
  return heap.toList()..sort((a, b) => b.compareTo(a));
}

void main() {
  print(topK([3, 1, 5, 12, 2, 11, 7], 3)); // [12, 11, 7]

  final rnd = Random(1);
  final scores = List.generate(1000000, (_) => rnd.nextInt(1000000));
  print(topK(scores, 5).length); // 5
}
```

**🔍 What This Code Does:**

1. **Fixed-Size Heap**: Never holds more than `k` items, so memory is O(k).
2. **Compare With the Root**: Only numbers bigger than the current k-th largest get in.
3. **O(n log k)**: Much faster than sorting everything (O(n log n)) when k is small.
4. **Works on Streams**: You never need the whole list in memory.

### Merge k sorted lists

```dart
import 'dart:collection';

List<int> mergeK(List<List<int>> lists) {
  // (value, list index, element index) ordered by value
  final heap = SplayTreeSet<(int, int, int)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    if (c != 0) return c;
    final d = a.$2.compareTo(b.$2);
    return d != 0 ? d : a.$3.compareTo(b.$3);
  });
  for (var i = 0; i < lists.length; i++) {
    if (lists[i].isNotEmpty) heap.add((lists[i][0], i, 0));
  }
  final out = <int>[];
  while (heap.isNotEmpty) {
    final smallest = heap.first;
    heap.remove(smallest);
    final (value, li, ei) = smallest;
    out.add(value);
    if (ei + 1 < lists[li].length) heap.add((lists[li][ei + 1], li, ei + 1));
  }
  return out;
}

void main() {
  print(mergeK([
    [1, 4, 9],
    [2, 3, 8],
    [0, 5, 6, 7],
  ])); // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
}
```

**🔍 What This Code Does:**

1. **One Candidate per List**: The structure holds the current smallest unused element of each list.
2. **Take the Smallest, Replace It**: After using an element, push the next one from the same list.
3. **`SplayTreeSet` as a Priority Queue**: `first` + `remove` gives the minimum in O(log n). The comparator includes the indexes as tie-breakers so equal values aren't treated as duplicates.
4. **O(N log k)**: For N total elements across k lists.

> 💡 For a ready-made heap, `package:collection` provides `PriorityQueue` (`HeapPriorityQueue`) with `add`, `first` and `removeFirst`.

---

## 🧭 When to Use a Heap

| Need | Use |
|------|-----|
| Always get the min/max quickly while items keep arriving | ✅ Heap / priority queue |
| Top-k or k-th largest | ✅ Size-k heap |
| Dijkstra's shortest path, A* search | ✅ Min-heap of distances |
| Task schedulers, event simulations | ✅ Min-heap of times/priorities |
| Median of a stream | ✅ Two heaps (max-heap + min-heap) |
| Sorted iteration of everything | Sort, or a balanced BST |
| Lookup of arbitrary values | Hash map or BST |

---

## ⚠️ Common Mistakes

### 1. Expecting the heap array to be sorted

Only the root is guaranteed. Remove repeatedly (or sort) if you need full order.

### 2. Swapping with the wrong child when sifting down

Always swap with the **smaller** child in a min-heap (the larger in a max-heap).

### 3. Off-by-one in index math

With 0-based arrays: children `2i + 1`, `2i + 2`; parent `(i − 1) ~/ 2`. (1-based heaps use `2i`, `2i + 1` and `i ~/ 2`.)

### 4. Mutating priorities of items already in the heap

Changing a stored item's priority breaks the heap property. Remove and re-add it, or push a new entry and skip stale ones later ("lazy deletion").

---

## 🧪 Try It Yourself

1. Turn `MinHeap` into a max-heap just by changing the comparator.
2. Write `kthLargest(nums, k)` with a size-k min-heap.
3. **Median of a stream**: keep the lower half in a max-heap and the upper half in a min-heap; rebalance so their sizes differ by at most 1.
4. Simulate a **task scheduler** where each task has a start time; always run the earliest task next.

---

## 📌 Key Takeaways

- ✅ A **priority queue** always removes the highest-priority item; a **binary heap** implements it.
- ✅ A **min-heap** keeps every parent ≤ its children, so the minimum is at the **root**.
- ✅ Heaps are **complete trees stored in arrays**: children at `2i + 1`, `2i + 2`; parent at `(i − 1) ~/ 2`.
- ✅ **Insert** sifts up and **removeMin** sifts down: both **O(log n)**; **peek** is **O(1)**.
- ✅ **Heapify** builds a heap in **O(n)**; **heap sort** is O(n log n) in place.
- ✅ A **size-k min-heap** finds the top k in **O(n log k)**.
- ✅ Heaps power **schedulers**, **Dijkstra**, **merging sorted lists** and **stream medians**.

**Next up:** 🔤 **Tries**: prefix trees for autocomplete and word search.
