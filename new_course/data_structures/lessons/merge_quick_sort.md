# Merge Sort & Quick Sort

Imagine sorting **1,000 exam papers** 📄 by student name.

- 🤝 **Merge strategy:** Split the pile in half and give each half to a friend. They split theirs again, and so on, until everyone holds just one paper (already "sorted"!). Then pairs of friends **merge** their sorted piles by repeatedly taking the smaller top paper. Piles combine until one sorted pile remains.
- 🎯 **Quick strategy:** Pick one paper, say "M", as the **pivot**. Put every name before M on the left and every name after M on the right. Now sort each side the same way. No merging needed: once both sides are sorted, the whole pile is sorted.

👉 These are the two most famous **divide and conquer** sorting algorithms:

> **Merge sort** splits the list in half, sorts each half recursively, then **merges** them: always **O(n log n)**, **stable**, but needs **O(n)** extra memory.
> **Quick sort** **partitions** the list around a pivot, then sorts each side recursively: **O(n log n)** on average, **in place**, but **O(n²)** in the worst case.

---

## 🧩 Divide and Conquer

Both follow the same three-step recipe:

1. **Divide** the problem into smaller subproblems.
2. **Conquer** each subproblem recursively (tiny ones are solved directly).
3. **Combine** the sub-results into the final answer.

| | Merge sort | Quick sort |
|---|-----------|------------|
| Divide | Trivial: split at the middle | Hard work: **partition** around a pivot |
| Combine | Hard work: **merge** two sorted halves | Trivial: nothing to do |

---

## 🤝 Merge Sort

### Step 1: Merging two sorted lists

The key operation: combine two sorted lists into one sorted list in **O(n)**, using two pointers.

```dart
List<int> merge(List<int> left, List<int> right) {
  final out = <int>[];
  var i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) { // <= keeps equal elements in order (stable)
      out.add(left[i++]);
    } else {
      out.add(right[j++]);
    }
  }
  out
    ..addAll(left.sublist(i))  // leftovers are already sorted
    ..addAll(right.sublist(j));
  return out;
}

void main() {
  print(merge([1, 4, 7, 9], [2, 3, 8])); // [1, 2, 3, 4, 7, 8, 9]
}
```

**🔍 What This Code Does:**

1. **Compare Fronts**: Take the smaller of `left[i]` and `right[j]`.
2. **`<=` for Stability**: On ties, the element from the left half goes first, preserving original order.
3. **Leftovers**: When one list runs out, the rest of the other is appended as-is.
4. **O(n + m)**: Each element is moved once.

### Step 2: Split, sort, merge

```dart
List<int> merge(List<int> left, List<int> right) {
  final out = <int>[];
  var i = 0, j = 0;
  while (i < left.length && j < right.length) {
    out.add(left[i] <= right[j] ? left[i++] : right[j++]);
  }
  return out
    ..addAll(left.sublist(i))
    ..addAll(right.sublist(j));
}

List<int> mergeSort(List<int> a) {
  if (a.length <= 1) return a; // base case: already sorted
  final mid = a.length ~/ 2;
  final left = mergeSort(a.sublist(0, mid));
  final right = mergeSort(a.sublist(mid));
  return merge(left, right);
}

void main() {
  print(mergeSort([38, 27, 43, 3, 9, 82, 10])); // [3, 9, 10, 27, 38, 43, 82]
}
```

**🔍 What This Code Does:**

1. **Base Case**: Lists of 0 or 1 elements are sorted.
2. **Divide**: Split at the middle index.
3. **Conquer**: Recursively sort each half.
4. **Combine**: Merge the two sorted halves.

```text
                 [38, 27, 43, 3, 9, 82, 10]
                /                          \
        [38, 27, 43]                  [3, 9, 82, 10]
        /         \                    /          \
     [38]      [27, 43]           [3, 9]       [82, 10]
               /     \            /    \        /     \
            [27]    [43]        [3]    [9]    [82]   [10]
               \     /            \    /        \     /
              [27, 43]            [3, 9]       [10, 82]
        \         /                    \          /
        [27, 38, 43]                  [3, 9, 10, 82]
                \                          /
                 [3, 9, 10, 27, 38, 43, 82]
```

### Why O(n log n)?

- The list is halved repeatedly, so there are **log₂ n levels**.
- At each level, merging all the pieces together touches **n elements**.
- Total: **n × log n**, in the **best, average and worst** case.

| Property | Merge sort |
|----------|------------|
| Time | **O(n log n)** always |
| Extra space | O(n) for the merged lists |
| Stable | ✅ Yes (with `<=`) |
| In-place | ❌ No |
| Great for | Linked lists, external sorting (huge files), when stability matters |

### Bottom-up merge sort (no recursion)

```dart
void mergeSortBottomUp(List<int> a) {
  final n = a.length;
  var buffer = List<int>.filled(n, 0);
  var src = a;
  for (var width = 1; width < n; width *= 2) {
    for (var lo = 0; lo < n; lo += 2 * width) {
      final mid = (lo + width).clamp(0, n);
      final hi = (lo + 2 * width).clamp(0, n);
      var i = lo, j = mid, k = lo;
      while (i < mid && j < hi) {
        buffer[k++] = src[i] <= src[j] ? src[i++] : src[j++];
      }
      while (i < mid) {
        buffer[k++] = src[i++];
      }
      while (j < hi) {
        buffer[k++] = src[j++];
      }
    }
    final t = src;
    src = buffer;
    buffer = t; // swap roles each pass
  }
  if (!identical(src, a)) a.setAll(0, src); // copy back if needed
}

void main() {
  final a = [5, 2, 9, 1, 5, 6, 3];
  mergeSortBottomUp(a);
  print(a); // [1, 2, 3, 5, 5, 6, 9]
}
```

**🔍 What This Code Does:**

1. **Runs of Width 1, 2, 4, 8...**: First merge pairs of single elements, then pairs of pairs, and so on.
2. **Two Buffers**: Each pass merges from `src` into `buffer`, then they swap roles, avoiding repeated allocation.
3. **`clamp`**: Keeps boundaries inside the list when the last run is shorter.
4. **No Recursion**: Same O(n log n) work without a call stack.

---

## 🎯 Quick Sort

### Step 1: Partitioning

Pick a **pivot**. Rearrange the list so everything **smaller** than the pivot is on its left and everything **larger** is on its right. The pivot is then in its **final** sorted position.

```dart
// Lomuto partition: uses the last element as the pivot
int partition(List<int> a, int lo, int hi) {
  final pivot = a[hi];
  var store = lo; // next spot for a "small" element
  for (var i = lo; i < hi; i++) {
    if (a[i] < pivot) {
      final t = a[i];
      a[i] = a[store];
      a[store] = t;
      store++;
    }
  }
  final t = a[store];
  a[store] = a[hi];
  a[hi] = t; // put the pivot between the two groups
  return store;
}

void main() {
  final a = [7, 2, 9, 4, 3, 8, 5];
  final p = partition(a, 0, a.length - 1);
  print(a); // [2, 4, 3, 5, 9, 8, 7]
  print('pivot ${a[p]} is at index $p'); // pivot 5 is at index 3
}
```

**🔍 What This Code Does:**

1. **Pivot = Last Element**: Here, `5`.
2. **`store` Pointer**: Marks the boundary of the "smaller than pivot" region.
3. **Grow the Small Region**: Every element smaller than the pivot is swapped into the small region.
4. **Place the Pivot**: Finally, the pivot is swapped into position `store`: everything left is smaller, everything right is larger or equal.
5. **O(n)**: One pass over the range.

### Step 2: Recurse on both sides

```dart
import 'dart:math';

final _random = Random(42);

void quickSort(List<int> a, [int lo = 0, int? hi]) {
  hi ??= a.length - 1;
  if (lo >= hi) return; // 0 or 1 elements

  // Random pivot avoids the O(n²) worst case on sorted input
  final r = lo + _random.nextInt(hi - lo + 1);
  final t = a[r];
  a[r] = a[hi];
  a[hi] = t;

  final p = _partition(a, lo, hi);
  quickSort(a, lo, p - 1);
  quickSort(a, p + 1, hi);
}

int _partition(List<int> a, int lo, int hi) {
  final pivot = a[hi];
  var store = lo;
  for (var i = lo; i < hi; i++) {
    if (a[i] < pivot) {
      final t = a[i];
      a[i] = a[store];
      a[store] = t;
      store++;
    }
  }
  final t = a[store];
  a[store] = a[hi];
  a[hi] = t;
  return store;
}

void main() {
  final a = [10, 80, 30, 90, 40, 50, 70];
  quickSort(a);
  print(a); // [10, 30, 40, 50, 70, 80, 90]
}
```

**🔍 What This Code Does:**

1. **Random Pivot**: A random element is swapped to the end and used as the pivot.
2. **Partition**: Puts the pivot in its final place.
3. **Recurse**: Sort the left part and the right part independently.
4. **In Place**: No extra lists; only the recursion stack (O(log n) on average).

### Why the pivot choice matters

| Pivot splits the list... | Recursion depth | Time |
|--------------------------|-----------------|------|
| Evenly (half and half) | log n | **O(n log n)** |
| Roughly 10% / 90% | still O(log n) | O(n log n) |
| Always 0 / everything (e.g. first element on sorted input) | n | **O(n²)** 😱 |

```dart
int comparisons = 0;

void quickSortFirstPivot(List<int> a, int lo, int hi) {
  if (lo >= hi) return;
  final pivot = a[lo]; // always the first element: risky!
  var store = lo + 1;
  for (var i = lo + 1; i <= hi; i++) {
    comparisons++;
    if (a[i] < pivot) {
      final t = a[i];
      a[i] = a[store];
      a[store] = t;
      store++;
    }
  }
  final t = a[lo];
  a[lo] = a[store - 1];
  a[store - 1] = t;
  quickSortFirstPivot(a, lo, store - 2);
  quickSortFirstPivot(a, store, hi);
}

void main() {
  final sorted = List.generate(1000, (i) => i);
  quickSortFirstPivot(sorted, 0, sorted.length - 1);
  print('already sorted input: $comparisons comparisons'); // 499500

  comparisons = 0;
  final shuffled = List.generate(1000, (i) => i)..shuffle();
  quickSortFirstPivot(shuffled, 0, shuffled.length - 1);
  print('shuffled input: ~$comparisons comparisons'); // around 11,000
}
```

**🔍 What This Code Does:**

1. **First-Element Pivot on Sorted Input**: The pivot is always the smallest, so one side is empty and the other has n − 1 elements.
2. **Quadratic Blow-Up**: n(n − 1)/2 = 499,500 comparisons for 1,000 elements.
3. **Random Order Fixes It**: The same algorithm on shuffled data does about 2n ln n ≈ 14,000 or fewer comparisons.
4. **Lesson**: Use a **random** or **median-of-three** pivot.

### Three-way partitioning (many duplicates)

When the list has lots of equal values, split into **< pivot**, **= pivot** and **> pivot**. The middle group is already done.

```dart
void quickSort3Way(List<int> a, [int lo = 0, int? hi]) {
  hi ??= a.length - 1;
  if (lo >= hi) return;
  final pivot = a[lo];
  var lt = lo, i = lo, gt = hi;
  while (i <= gt) {
    if (a[i] < pivot) {
      final t = a[lt];
      a[lt++] = a[i];
      a[i++] = t;
    } else if (a[i] > pivot) {
      final t = a[gt];
      a[gt--] = a[i];
      a[i] = t;
    } else {
      i++;
    }
  }
  quickSort3Way(a, lo, lt - 1); // only the "less than" part
  quickSort3Way(a, gt + 1, hi); // only the "greater than" part
}

void main() {
  final votes = [2, 1, 2, 3, 2, 1, 2, 3, 2, 2];
  quickSort3Way(votes);
  print(votes); // [1, 1, 2, 2, 2, 2, 2, 2, 3, 3]
}
```

**🔍 What This Code Does:**

1. **Three Regions**: `[lo, lt)` is less, `[lt, i)` is equal, `(gt, hi]` is greater.
2. **Equal Elements Stay Put**: They're never recursed on again.
3. **Big Win on Duplicates**: With only a few distinct values, this approaches O(n).

| Property | Quick sort |
|----------|------------|
| Time | **O(n log n)** average, O(n²) worst |
| Extra space | O(log n) recursion stack (average) |
| Stable | ❌ No |
| In-place | ✅ Yes |
| Great for | General-purpose in-memory sorting of arrays |

---

## 🧰 Sorting in Dart: `List.sort` and Comparators

You'll rarely write these by hand. Dart's `List.sort` is an optimized O(n log n) sort (a dual-pivot quicksort with insertion sort for small ranges). Its stability is **not guaranteed**.

```dart
class Task {
  final String title;
  final int priority;
  final DateTime due;
  Task(this.title, this.priority, this.due);

  @override
  String toString() => '$title(p$priority)';
}

void main() {
  final tasks = [
    Task('Write tests', 2, DateTime(2026, 3, 5)),
    Task('Fix bug', 1, DateTime(2026, 3, 9)),
    Task('Deploy', 1, DateTime(2026, 3, 2)),
    Task('Docs', 3, DateTime(2026, 3, 1)),
  ];

  // Sort by priority, then by due date (explicit tie-breaker = no stability needed)
  tasks.sort((a, b) {
    final byPriority = a.priority.compareTo(b.priority);
    return byPriority != 0 ? byPriority : a.due.compareTo(b.due);
  });
  print(tasks); // [Deploy(p1), Fix bug(p1), Write tests(p2), Docs(p3)]

  final words = ['banana', 'Apple', 'cherry'];
  words.sort((a, b) => a.toLowerCase().compareTo(b.toLowerCase()));
  print(words); // [Apple, banana, cherry]
}
```

**🔍 What This Code Does:**

1. **Comparator Function**: Returns negative, zero or positive.
2. **Explicit Tie-Breaker**: Comparing due dates when priorities are equal makes the order fully defined, so stability doesn't matter.
3. **`DateTime.compareTo`**: Dates are comparable out of the box.
4. **Need Stability?** Use `mergeSort` from `package:collection`, or add a tie-breaker such as the original index.

---

## 🔢 Bonus: Counting Inversions With Merge Sort

During a merge, whenever an element from the **right** half is taken before remaining elements of the **left** half, it forms an inversion with **all** of them.

```dart
(List<int>, int) sortAndCount(List<int> a) {
  if (a.length <= 1) return (a, 0);
  final mid = a.length ~/ 2;
  final (left, invL) = sortAndCount(a.sublist(0, mid));
  final (right, invR) = sortAndCount(a.sublist(mid));
  final merged = <int>[];
  var i = 0, j = 0, cross = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      merged.add(left[i++]);
    } else {
      cross += left.length - i; // right[j] is smaller than every remaining left element
      merged.add(right[j++]);
    }
  }
  merged
    ..addAll(left.sublist(i))
    ..addAll(right.sublist(j));
  return (merged, invL + invR + cross);
}

void main() {
  final (sorted, inversions) = sortAndCount([2, 4, 1, 3, 5]);
  print(sorted);     // [1, 2, 3, 4, 5]
  print(inversions); // 3
}
```

**🔍 What This Code Does:**

1. **Records Return Two Values**: The sorted list and the inversion count.
2. **Cross Inversions**: Counted in bulk during the merge.
3. **O(n log n)**: Versus O(n²) for checking every pair.

---

## ⚖️ Merge Sort vs Quick Sort

| | Merge sort | Quick sort |
|---|-----------|------------|
| Average time | O(n log n) | O(n log n), usually faster in practice |
| Worst time | **O(n log n)** | O(n²) (rare with random pivots) |
| Extra memory | O(n) | **O(log n)** |
| Stable | ✅ | ❌ |
| Cache behavior | Good | **Excellent** (works in place) |
| Linked lists | ✅ Natural fit | Awkward |
| Huge files on disk | ✅ External merge sort | ❌ |

> 💡 No comparison sort can beat **O(n log n)** in the worst case. There are n! possible orderings, and each comparison only halves the possibilities, so you need about log₂(n!) ≈ n log n comparisons.

---

## ⚠️ Common Mistakes

### 1. Forgetting the base case

Without `if (a.length <= 1) return a;`, merge sort recurses forever.

### 2. Using `<` instead of `<=` in merge

The merge still sorts correctly, but it's no longer **stable**.

### 3. Always picking the first or last element as the pivot

Sorted or reversed input then triggers O(n²). Pick randomly or use median-of-three.

### 4. Off-by-one in partition ranges

Recurse on `lo..p−1` and `p+1..hi`. Including `p` again can cause infinite recursion.

---

## 🧪 Try It Yourself

1. Implement **merge sort on a linked list** (find the middle with fast/slow pointers).
2. Implement **quickselect**: find the k-th smallest element in O(n) average by partitioning and recursing into only one side.
3. Implement **median-of-three** pivot selection.
4. Sort a list of `(name, score)` records by score descending, then name ascending, using `List.sort`.

```dart
import 'dart:math';

int quickselect(List<int> a, int k, [Random? rnd]) {
  rnd ??= Random(1);
  var lo = 0, hi = a.length - 1;
  while (true) {
    if (lo == hi) return a[lo];
    final r = lo + rnd.nextInt(hi - lo + 1);
    var t = a[r];
    a[r] = a[hi];
    a[hi] = t;
    final pivot = a[hi];
    var store = lo;
    for (var i = lo; i < hi; i++) {
      if (a[i] < pivot) {
        t = a[i];
        a[i] = a[store];
        a[store] = t;
        store++;
      }
    }
    t = a[store];
    a[store] = a[hi];
    a[hi] = t;
    if (k == store) return a[store];
    if (k < store) {
      hi = store - 1;
    } else {
      lo = store + 1;
    }
  }
}

void main() {
  final scores = [7, 10, 4, 3, 20, 15];
  print(quickselect([...scores], 2)); // 7 (third smallest, k is 0-based)
}
```

**🔍 What This Code Does:**

1. **Partition Once per Round**: Like quick sort.
2. **Recurse Into One Side Only**: The k-th smallest is either the pivot, on the left, or on the right.
3. **O(n) Average**: n + n/2 + n/4 + ... ≈ 2n work.

---

## 📌 Key Takeaways

- ✅ **Divide and conquer**: split, solve recursively, combine.
- ✅ **Merge sort**: split in half, sort both, **merge**; **O(n log n) always**, **stable**, **O(n) extra space**.
- ✅ **Quick sort**: **partition** around a pivot, sort both sides; **O(n log n) average**, **in place**, **O(n²) worst**.
- ✅ Use **random** or **median-of-three** pivots; **three-way partitioning** handles duplicates.
- ✅ Dart's `List.sort` is a fast O(n log n) sort that **isn't guaranteed stable**; add tie-breakers or use `mergeSort` from `package:collection`.
- ✅ Comparison sorts can't beat **O(n log n)** in the worst case.

**Next up:** 🔢 **Counting & Radix Sort**: beating O(n log n) when you know the range of your keys.
