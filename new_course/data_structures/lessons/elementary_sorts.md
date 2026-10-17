# Elementary Sorts

Imagine you're holding a hand of **playing cards** 🃏 and want them in order.

- 🫧 You could repeatedly **swap neighbors** that are out of order until nothing moves (**bubble sort**).
- 👉 You could **find the smallest** card, put it first, then find the next smallest, and so on (**selection sort**).
- ✋ You could pick up cards **one at a time** and **slide each into place** among the cards you already hold (**insertion sort**). This is what most people actually do!

👉 These are the three **elementary sorting algorithms**:

> **Bubble**, **selection** and **insertion sort** are simple, in-place algorithms that take **O(n²)** time in the worst case. They're too slow for large data, but they teach the core ideas of sorting, and **insertion sort** is genuinely the fastest choice for **small** or **nearly sorted** lists.

---

## 📏 Sorting Vocabulary

| Term | Meaning |
|------|---------|
| **In-place** | Uses only O(1) extra memory (rearranges the list itself) |
| **Stable** | Equal elements keep their original relative order |
| **Adaptive** | Runs faster when the input is already partly sorted |
| **Comparison sort** | Decides order only by comparing pairs of elements |
| **Inversion** | A pair `(i, j)` with `i < j` but `a[i] > a[j]`: one "out of order" pair |

> 💡 A sorted list has **0 inversions**; a reversed list has the maximum, **n(n − 1)/2**. Swapping two adjacent out-of-order elements fixes exactly **one** inversion.

---

## 🫧 Bubble Sort

Walk through the list, **swapping adjacent pairs** that are out of order. After each pass, the **largest** remaining element has "bubbled" to the end.

```dart
void bubbleSort(List<int> a) {
  for (var end = a.length - 1; end > 0; end--) {
    var swapped = false;
    for (var i = 0; i < end; i++) {
      if (a[i] > a[i + 1]) {
        final t = a[i];
        a[i] = a[i + 1];
        a[i + 1] = t;
        swapped = true;
      }
    }
    if (!swapped) return; // no swaps: already sorted, stop early
  }
}

void main() {
  final a = [5, 1, 4, 2, 8];
  bubbleSort(a);
  print(a); // [1, 2, 4, 5, 8]
}
```

**🔍 What This Code Does:**

1. **Adjacent Comparisons**: Each pass compares `a[i]` with `a[i + 1]` and swaps if they're out of order.
2. **Shrinking End**: After pass k, the last k elements are in their final positions, so the inner loop stops at `end`.
3. **Early Exit**: If a pass makes no swaps, the list is sorted. This makes bubble sort **O(n)** on already-sorted input.
4. **Stable**: Equal elements are never swapped (`>` not `>=`).

**Pass by pass for `[5, 1, 4, 2, 8]`:**

```text
pass 1: [1, 4, 2, 5, 8]   (5 bubbles toward the end, 8 stays)
pass 2: [1, 2, 4, 5, 8]
pass 3: no swaps → done
```

| Case | Comparisons | Time |
|------|-------------|------|
| Best (sorted) | n − 1 | **O(n)** |
| Average | ~n²/2 | O(n²) |
| Worst (reversed) | n(n − 1)/2 | O(n²) |

---

## 👉 Selection Sort

Find the **minimum** of the unsorted part and **swap** it to the front of that part. Repeat.

```dart
void selectionSort(List<int> a) {
  for (var i = 0; i < a.length - 1; i++) {
    var minIndex = i;
    for (var j = i + 1; j < a.length; j++) {
      if (a[j] < a[minIndex]) minIndex = j;
    }
    if (minIndex != i) {
      final t = a[i];
      a[i] = a[minIndex];
      a[minIndex] = t;
    }
  }
}

void main() {
  final a = [64, 25, 12, 22, 11];
  selectionSort(a);
  print(a); // [11, 12, 22, 25, 64]
}
```

**🔍 What This Code Does:**

1. **Grow a Sorted Prefix**: After step `i`, positions `0..i` hold the `i + 1` smallest elements in order.
2. **Scan for the Minimum**: The inner loop finds the smallest remaining element.
3. **One Swap per Step**: At most n − 1 swaps in total, the fewest of the three algorithms. Useful when writes are expensive (e.g. flash memory).
4. **Not Adaptive**: It always scans the whole unsorted part, so it's O(n²) even on sorted input.
5. **Not Stable**: A long-distance swap can jump an element past an equal one.

```text
[64, 25, 12, 22, 11]
 ↑ swap with min 11 → [11, 25, 12, 22, 64]
     ↑ swap with 12 → [11, 12, 25, 22, 64]
         ↑ swap with 22 → [11, 12, 22, 25, 64]
             ↑ already min → done
```

### Why selection sort isn't stable

```dart
void main() {
  // Sort cards by rank only; suits show the original order
  final cards = [(4, '♠'), (4, '♥'), (2, '♦')];
  for (var i = 0; i < cards.length - 1; i++) {
    var m = i;
    for (var j = i + 1; j < cards.length; j++) {
      if (cards[j].$1 < cards[m].$1) m = j;
    }
    final t = cards[i];
    cards[i] = cards[m];
    cards[m] = t;
  }
  print(cards); // [(2, ♦), (4, ♥), (4, ♠)] → the two 4s swapped order!
}
```

**🔍 What This Code Does:**

1. **Long-Distance Swap**: Moving `(2, ♦)` to the front sends `(4, ♠)` to the back, past `(4, ♥)`.
2. **Instability**: Equal ranks (4♠, 4♥) end up in a different relative order than they started.
3. **Why It Matters**: Stability lets you sort by several keys in sequence (e.g. by date, then by name) without losing the earlier order.

---

## ✋ Insertion Sort

Take each element and **slide it left** past larger elements until it's in the right spot among the already-sorted prefix.

```dart
void insertionSort(List<int> a) {
  for (var i = 1; i < a.length; i++) {
    final current = a[i];
    var j = i - 1;
    while (j >= 0 && a[j] > current) {
      a[j + 1] = a[j]; // shift the bigger element right
      j--;
    }
    a[j + 1] = current; // drop current into the gap
  }
}

void main() {
  final a = [12, 11, 13, 5, 6];
  insertionSort(a);
  print(a); // [5, 6, 11, 12, 13]
}
```

**🔍 What This Code Does:**

1. **Sorted Prefix**: Before step `i`, elements `0..i−1` are sorted.
2. **Hold the Current Element**: `current` is saved so the slot can be overwritten while shifting.
3. **Shift, Don't Swap**: Larger elements move one step right, which is cheaper than repeated swaps.
4. **Drop Into Place**: `current` goes into the gap left behind.
5. **Stable and Adaptive**: Equal elements aren't moved past each other (`>` not `>=`), and on nearly sorted data the `while` loop barely runs.

```text
[12, 11, 13, 5, 6]
i=1: 11 → [11, 12, 13, 5, 6]
i=2: 13 → [11, 12, 13, 5, 6]   (already in place)
i=3: 5  → [5, 11, 12, 13, 6]   (shifts past 3 elements)
i=4: 6  → [5, 6, 11, 12, 13]
```

### Insertion sort's superpower: nearly sorted data

```dart
int insertionSortShifts(List<int> a) {
  var shifts = 0;
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && a[j] > cur) {
      a[j + 1] = a[j];
      j--;
      shifts++;
    }
    a[j + 1] = cur;
  }
  return shifts;
}

void main() {
  final nearly = List.generate(1000, (i) => i)
    ..[10] = 11
    ..[11] = 10; // one pair swapped
  final reversed = List.generate(1000, (i) => 999 - i);

  print('nearly sorted: ${insertionSortShifts(nearly)} shifts');  // 1
  print('reversed: ${insertionSortShifts(reversed)} shifts');     // 499500
}
```

**🔍 What This Code Does:**

1. **Shifts = Inversions**: Insertion sort performs exactly one shift per inversion.
2. **Nearly Sorted**: One swapped pair means one inversion, so just **1 shift**: practically O(n).
3. **Reversed**: n(n − 1)/2 = 499,500 shifts: the O(n²) worst case.
4. **Cascade Index Assignment**: `..[10] = 11` modifies the generated list inline.

> 💡 This is why real-world sorting libraries (like Timsort, used by Python and Java) switch to **insertion sort** for small chunks: it's simple, cache-friendly and extremely fast on short or nearly sorted runs.

---

## 🃏 Sorting Objects With a Comparator

Real data isn't just integers. Make the algorithm generic with a **comparator**.

```dart
void insertionSortBy<T>(List<T> a, int Function(T, T) compare) {
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && compare(a[j], cur) > 0) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = cur;
  }
}

typedef Student = ({String name, int grade});

void main() {
  final students = <Student>[
    (name: 'Zoe', grade: 90),
    (name: 'Ali', grade: 85),
    (name: 'Mia', grade: 90),
    (name: 'Ben', grade: 85),
  ];

  // Sort by name first, then (stably) by grade descending
  insertionSortBy<Student>(students, (a, b) => a.name.compareTo(b.name));
  insertionSortBy<Student>(students, (a, b) => b.grade.compareTo(a.grade));

  for (final s in students) {
    print('${s.grade} ${s.name}');
  }
  // 90 Mia
  // 90 Zoe
  // 85 Ali
  // 85 Ben
}
```

**🔍 What This Code Does:**

1. **Generic Sort**: `T` can be any type; the comparator defines the order.
2. **Comparator Contract**: Negative if `a` comes first, positive if `b` comes first, zero if equal.
3. **Multi-Key Sorting With Stability**: Sorting by name and then stably by grade leaves students with the same grade in alphabetical order.
4. **Descending Order**: `b.grade.compareTo(a.grade)` reverses the natural order.

---

## 📊 Comparing the Three

| | Bubble | Selection | Insertion |
|---|--------|-----------|-----------|
| Best case | O(n) (with early exit) | O(n²) | **O(n)** |
| Average / worst | O(n²) | O(n²) | O(n²) |
| Swaps / writes | O(n²) | **O(n)** | O(n²) shifts |
| Stable | ✅ | ❌ | ✅ |
| Adaptive | ✅ (early exit) | ❌ | ✅✅ |
| In-place | ✅ | ✅ | ✅ |
| Real-world use | Teaching | Minimizing writes | **Small or nearly sorted data, hybrid sorts** |

```dart
import 'dart:math';

void main() {
  final rnd = Random(7);
  final data = List.generate(2000, (_) => rnd.nextInt(100000));

  for (final (name, sort) in [
    ('bubble', bubbleSort),
    ('selection', selectionSort),
    ('insertion', insertionSort),
    ('List.sort', (List<int> a) => a.sort()),
  ]) {
    final copy = [...data];
    final sw = Stopwatch()..start();
    sort(copy);
    print('${name.padRight(10)} ${sw.elapsedMicroseconds} µs');
  }
}

void bubbleSort(List<int> a) {
  for (var end = a.length - 1; end > 0; end--) {
    var swapped = false;
    for (var i = 0; i < end; i++) {
      if (a[i] > a[i + 1]) {
        final t = a[i];
        a[i] = a[i + 1];
        a[i + 1] = t;
        swapped = true;
      }
    }
    if (!swapped) return;
  }
}

void selectionSort(List<int> a) {
  for (var i = 0; i < a.length - 1; i++) {
    var m = i;
    for (var j = i + 1; j < a.length; j++) {
      if (a[j] < a[m]) m = j;
    }
    final t = a[i];
    a[i] = a[m];
    a[m] = t;
  }
}

void insertionSort(List<int> a) {
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && a[j] > cur) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = cur;
  }
}
```

**🔍 What This Code Does:**

1. **Same Random Data**: Each algorithm sorts a copy of the same 2,000 numbers.
2. **Functions in a List**: Records of `(name, function)` let us loop over the algorithms.
3. **Typical Result**: Insertion beats selection beats bubble, and `List.sort` (O(n log n)) beats all of them by a wide margin.

---

## ⚠️ Common Mistakes

### 1. Off-by-one inner loops

In bubble sort, the inner loop must stop at `end` (comparing `a[i]` with `a[i + 1]`), or you'll read past the end of the list.

### 2. Using `>=` and losing stability

`if (a[j] >= cur)` in insertion sort moves equal elements past each other, making it unstable.

### 3. Swapping inside selection sort's inner loop

Swap **once** after finding the minimum, not every time a smaller element is seen.

### 4. Using O(n²) sorts on big data

For more than a few dozen elements, use `List.sort()` (or merge/quick sort from the next lesson).

---

## 🧪 Try It Yourself

1. Count the **inversions** in a list with a double loop, then verify the count equals insertion sort's shifts.
2. Implement **cocktail shaker sort**: bubble sort that alternates left-to-right and right-to-left passes.
3. Write `sortDescending` versions of all three algorithms.
4. Implement **binary insertion sort**: use binary search to find the insertion point. Does it reduce comparisons? Shifts?

```dart
int countInversions(List<int> a) {
  var count = 0;
  for (var i = 0; i < a.length; i++) {
    for (var j = i + 1; j < a.length; j++) {
      if (a[i] > a[j]) count++;
    }
  }
  return count;
}

void main() {
  print(countInversions([2, 4, 1, 3, 5])); // 3: (2,1), (4,1), (4,3)
  print(countInversions([5, 4, 3, 2, 1])); // 10
}
```

**🔍 What This Code Does:**

1. **Every Pair**: Checks all `i < j` pairs.
2. **Out-of-Order Pairs**: Counts those where the earlier element is bigger.
3. **O(n²)**: A merge-sort-based version counts inversions in O(n log n) (next lesson).

---

## 📌 Key Takeaways

- ✅ **Bubble sort** swaps adjacent out-of-order pairs; with an early exit it's O(n) on sorted input.
- ✅ **Selection sort** repeatedly selects the minimum; only **O(n) swaps**, but always O(n²) comparisons and **not stable**.
- ✅ **Insertion sort** slides each element into a sorted prefix; **stable**, **adaptive**, and the best choice for **small or nearly sorted** lists.
- ✅ All three are **in-place** and **O(n²)** in the worst case.
- ✅ Insertion sort's work equals the number of **inversions**.
- ✅ Real libraries use insertion sort inside **hybrid** algorithms; for big data, use **O(n log n)** sorts.

**Next up:** ⚡ **Merge Sort & Quick Sort**: divide and conquer to reach O(n log n).
