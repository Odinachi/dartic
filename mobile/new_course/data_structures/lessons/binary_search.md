# Binary Search

Imagine looking up the word **"quokka"** 🦘 in a paper dictionary with 1,000 pages.

- You don't start at page 1. You open somewhere in the **middle**: page 500 says **"M"**.
- "Q" comes after "M", so you ignore the whole **first half** and open the middle of the second half: page 750 says **"S"**.
- Too far! Now you look between 500 and 750...

Each glance throws away **half** of what's left. About **10** glances find any word among 1,000 pages.

👉 That's **binary search**:

> **Binary search** finds a target in a **sorted** collection by repeatedly comparing with the **middle** element and discarding the half that can't contain it. It runs in **O(log n)**.

It's also far more than "find a number in a list": binary search finds **boundaries**, **first/last occurrences**, and even **answers to optimization problems**.

---

## 📏 How Fast Is O(log n)?

| Items | Max steps (linear search) | Max steps (binary search) |
|-------|---------------------------|---------------------------|
| 1,000 | 1,000 | 10 |
| 1,000,000 | 1,000,000 | 20 |
| 1,000,000,000 | 1,000,000,000 | 30 |
| Every person on Earth (8 billion) | 8 billion | 33 |

---

## 🔎 The Classic Version

```dart
int binarySearch(List<int> sorted, int target) {
  var lo = 0;
  var hi = sorted.length - 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2; // overflow-safe middle
    final value = sorted[mid];
    if (value == target) return mid;
    if (value < target) {
      lo = mid + 1; // target is to the right
    } else {
      hi = mid - 1; // target is to the left
    }
  }
  return -1; // not found
}

void main() {
  final nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91];
  print(binarySearch(nums, 23)); // 5
  print(binarySearch(nums, 2));  // 0
  print(binarySearch(nums, 91)); // 9
  print(binarySearch(nums, 7));  // -1
}
```

**🔍 What This Code Does:**

This code demonstrates **iterative binary search on a sorted list**:

1. **Search Range `[lo, hi]`**: Both ends are inclusive, so the loop runs while `lo <= hi`.

2. **Middle Index**: `lo + (hi - lo) ~/ 2` avoids overflow in languages with fixed-size integers (and is a good habit in Dart too).

3. **Discard Half**: If the middle is too small, the target can only be right of it (`lo = mid + 1`); if too big, only left of it (`hi = mid - 1`).

4. **`+ 1` and `- 1`**: The middle has already been checked, so it's excluded. Forgetting this causes infinite loops.

5. **Not Found**: When `lo > hi`, the range is empty, so return `-1`.

**Trace for 23:**

| lo | hi | mid | value | decision |
|----|----|-----|-------|----------|
| 0 | 9 | 4 | 16 | 16 < 23 → go right |
| 5 | 9 | 7 | 56 | 56 > 23 → go left |
| 5 | 6 | 5 | 23 | ✅ found at 5 |

---

## 🎯 Finding Boundaries: First and Last Occurrence

With duplicates, the classic version returns **some** matching index, not necessarily the first. A tiny change finds the **leftmost** one: when you find a match, **remember it and keep searching left**.

```dart
int firstIndexOf(List<int> a, int target) {
  var lo = 0, hi = a.length - 1, answer = -1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == target) {
      answer = mid;   // record it...
      hi = mid - 1;   // ...but keep looking to the left
    } else if (a[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return answer;
}

int lastIndexOf(List<int> a, int target) {
  var lo = 0, hi = a.length - 1, answer = -1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == target) {
      answer = mid;
      lo = mid + 1;   // keep looking to the right
    } else if (a[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return answer;
}

void main() {
  final scores = [10, 20, 20, 20, 20, 30, 40];
  print(firstIndexOf(scores, 20)); // 1
  print(lastIndexOf(scores, 20));  // 4
  print(lastIndexOf(scores, 20) - firstIndexOf(scores, 20) + 1); // 4 occurrences
  print(firstIndexOf(scores, 25)); // -1
}
```

**🔍 What This Code Does:**

1. **Don't Stop at the First Match**: Record it as the best answer so far and continue in one direction.
2. **Leftmost vs Rightmost**: Searching left (`hi = mid - 1`) finds the first; searching right (`lo = mid + 1`) finds the last.
3. **Counting in O(log n)**: `last − first + 1` counts occurrences without scanning them.

---

## 🧭 Lower Bound and Upper Bound

A more general and very useful formulation uses a **half-open** range `[lo, hi)`:

- **`lowerBound(x)`**: the first index whose value is **≥ x**
- **`upperBound(x)`**: the first index whose value is **> x**

They always return a valid insertion point (possibly `length`), never −1.

```dart
int lowerBound(List<int> a, int x) {
  var lo = 0, hi = a.length; // half-open [lo, hi)
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] < x) {
      lo = mid + 1;
    } else {
      hi = mid; // mid might be the answer, keep it in range
    }
  }
  return lo;
}

int upperBound(List<int> a, int x) {
  var lo = 0, hi = a.length;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] <= x) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return lo;
}

void main() {
  final a = [1, 3, 3, 3, 7, 9];
  print(lowerBound(a, 3)); // 1 (first 3)
  print(upperBound(a, 3)); // 4 (first value after the 3s)
  print(lowerBound(a, 5)); // 4 (where 5 would be inserted)
  print(lowerBound(a, 0)); // 0
  print(lowerBound(a, 100)); // 6 (past the end)

  // Count of 3s and values in a range in O(log n)
  print(upperBound(a, 3) - lowerBound(a, 3)); // 3
  print(upperBound(a, 8) - lowerBound(a, 2)); // 4 values in [2, 8]: 3, 3, 3, 7

  // Keep a list sorted while inserting
  final sorted = <int>[];
  for (final x in [5, 1, 4, 1, 9]) {
    sorted.insert(lowerBound(sorted, x), x);
  }
  print(sorted); // [1, 1, 4, 5, 9]
}
```

**🔍 What This Code Does:**

1. **Half-Open Range**: `hi = a.length` lets the answer be "past the end".
2. **`hi = mid` (not `mid - 1`)**: The middle might be the answer, so it stays in the range.
3. **`lo < hi` Loop**: Ends when the range shrinks to a single point, which is the answer.
4. **Range Counting**: `upperBound(b) − lowerBound(a)` counts values in `[a, b]`.
5. **Sorted Insert**: Finding the insertion point is O(log n); the `insert` itself is still O(n) because of shifting.

> 💡 Many languages provide these: C++ `lower_bound`, Python `bisect_left`/`bisect_right`. In Dart, `package:collection` has `lowerBound` and `binarySearch` for lists.

---

## 🔍 Searching With a Predicate: The Universal Pattern

Most binary search problems reduce to: **"find the first index where a condition becomes true"**, where the condition is `false, false, ..., false, true, true, ..., true` (monotonic).

```dart
/// Returns the first value in [lo, hi] where test(value) is true,
/// assuming test is false...false then true...true. Returns hi + 1 if never true.
int firstTrue(int lo, int hi, bool Function(int) test) {
  var answer = hi + 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (test(mid)) {
      answer = mid;
      hi = mid - 1;
    } else {
      lo = mid + 1;
    }
  }
  return answer;
}

void main() {
  // First bad version: versions >= 7 are broken
  bool isBad(int version) => version >= 7;
  print(firstTrue(1, 100, isBad)); // 7

  // Integer square root: largest x with x*x <= n  →  (first x with x*x > n) - 1
  int isqrt(int n) => firstTrue(0, n, (x) => x * x > n) - 1;
  print(isqrt(17)); // 4
  print(isqrt(16)); // 4
}
```

**🔍 What This Code Does:**

1. **Monotonic Predicate**: Once `test` becomes true, it stays true for larger values.
2. **One Template, Many Problems**: First bad version, integer square root, first index ≥ x... all the same shape.
3. **Function Parameter**: `bool Function(int) test` makes the search reusable.
4. **O(log(range))**: Searches a numeric range, not just a list.

---

## 💡 Binary Search on the Answer

Some optimization problems ask for the **minimum** (or maximum) value that makes something possible. If "possible" is monotonic (once it works, bigger values also work), you can binary search **the answer itself**.

### Shipping packages within D days

**Problem:** Packages with weights must ship **in order**. Find the **smallest ship capacity** that ships everything within `days` days.

```dart
bool canShip(List<int> weights, int capacity, int days) {
  var used = 1, load = 0;
  for (final w in weights) {
    if (load + w > capacity) {
      used++;     // start a new day
      load = 0;
    }
    load += w;
  }
  return used <= days;
}

int minCapacity(List<int> weights, int days) {
  var lo = weights.reduce((a, b) => a > b ? a : b); // must fit the heaviest package
  var hi = weights.reduce((a, b) => a + b);         // ship everything in one day
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (canShip(weights, mid, days)) {
      hi = mid;      // works: try smaller
    } else {
      lo = mid + 1;  // too small: need more capacity
    }
  }
  return lo;
}

void main() {
  final weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  print(minCapacity(weights, 5)); // 15
  print(minCapacity(weights, 1)); // 55
  print(minCapacity(weights, 10)); // 10
}
```

**🔍 What This Code Does:**

1. **Feasibility Check**: `canShip` greedily packs each day; it's O(n).
2. **Monotonic**: If capacity `c` works, any larger capacity also works.
3. **Search Range**: At least the heaviest package, at most the total weight.
4. **Binary Search the Capacity**: O(n log(sum)) instead of trying every capacity.
5. **Pattern**: "Minimize the maximum" or "maximize the minimum" problems often fit this template (e.g. Koko eating bananas, splitting arrays, placing routers).

---

## 🔄 Rotated Sorted Arrays

A sorted array rotated at some pivot, like `[15, 18, 2, 3, 6, 12]`. At every step, **one half is still sorted**, so you can decide which half to keep.

```dart
int searchRotated(List<int> a, int target) {
  var lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == target) return mid;
    if (a[lo] <= a[mid]) {
      // left half [lo..mid] is sorted
      if (a[lo] <= target && target < a[mid]) {
        hi = mid - 1;
      } else {
        lo = mid + 1;
      }
    } else {
      // right half [mid..hi] is sorted
      if (a[mid] < target && target <= a[hi]) {
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
  }
  return -1;
}

void main() {
  final a = [15, 18, 2, 3, 6, 12];
  print(searchRotated(a, 3));  // 3
  print(searchRotated(a, 15)); // 0
  print(searchRotated(a, 7));  // -1
}
```

**🔍 What This Code Does:**

1. **Identify the Sorted Half**: If `a[lo] <= a[mid]`, the left half has no rotation point in it.
2. **Range Check**: If the target lies within the sorted half's range, search there; otherwise search the other half.
3. **Still O(log n)**: Each step halves the range.

---

## 🧰 Binary Search in Dart Collections

```dart
import 'dart:collection';

void main() {
  // SplayTreeSet gives O(log n) ordered queries without manual binary search
  final prices = SplayTreeSet<int>.of([5, 12, 20, 35, 50]);
  print(prices.lookup(20));            // 20 (exists)
  print(prices.where((p) => p >= 18).first); // 20 (but this scans: O(n))

  final map = SplayTreeMap<int, String>.fromIterable([5, 12, 20, 35, 50],
      value: (p) => 'item\$$p');
  print(map.firstKeyAfter(18));  // 20: O(log n) "ceiling-like" query
  print(map.lastKeyBefore(18));  // 12: O(log n) "floor-like" query
}
```

**🔍 What This Code Does:**

1. **Sorted Collections**: `SplayTreeSet` and `SplayTreeMap` are trees, not arrays, but answer similar questions.
2. **`firstKeyAfter` / `lastKeyBefore`**: Strictly greater / strictly smaller keys in O(log n).
3. **Beware `where(...)`**: It scans linearly; it doesn't use the tree's order.

---

## ⚠️ Common Mistakes

### 1. Searching unsorted data

Binary search **requires** sorted (or monotonic) data. On unsorted data it returns wrong answers silently.

### 2. Infinite loops from wrong bounds

```dart
void main() {
  // ❌ With lo = mid (instead of mid + 1) and lo < hi, lo can get stuck.
  // Example: lo = 2, hi = 3 → mid = 2 → lo = mid = 2 forever.
  // ✅ Pair the loop condition with the right updates:
  //    while (lo <= hi): lo = mid + 1, hi = mid - 1
  //    while (lo < hi):  lo = mid + 1, hi = mid
  var lo = 2, hi = 3, steps = 0;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (mid < 3) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
    steps++;
  }
  print('converged at $lo after $steps step(s)'); // converged at 3 after 1 step(s)
}
```

**🔍 What This Code Does:**

1. **Matching Templates**: Each loop condition has a matching pair of updates; mixing them causes infinite loops or skipped answers.
2. **Always Shrink**: Every iteration must make the range strictly smaller.

### 3. Off-by-one in the answer

Decide up front whether you want "first ≥", "first >", "last ≤", or "exact", and test edge cases: empty list, one element, target smaller than everything, larger than everything.

### 4. Forgetting `~/`

`(lo + hi) / 2` gives a `double` in Dart, which can't be used as a list index. Use `~/`.

---

## 🧪 Try It Yourself

1. **Search insert position**: return the index where `target` is or would be inserted.
2. **Find the minimum in a rotated sorted array** in O(log n).
3. **Koko eating bananas**: find the minimum eating speed to finish all piles within `h` hours.
4. **Peak element**: find any index where `a[i] > a[i - 1]` and `a[i] > a[i + 1]`, in O(log n).

```dart
int findMinRotated(List<int> a) {
  var lo = 0, hi = a.length - 1;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] > a[hi]) {
      lo = mid + 1; // minimum is to the right of mid
    } else {
      hi = mid;     // mid could be the minimum
    }
  }
  return a[lo];
}

void main() {
  print(findMinRotated([4, 5, 6, 7, 0, 1, 2])); // 0
  print(findMinRotated([1, 2, 3]));             // 1
}
```

**🔍 What This Code Does:**

1. **Compare With the Right End**: If `a[mid] > a[hi]`, the rotation point (minimum) is to the right.
2. **Otherwise**: The right half is sorted, so the minimum is at `mid` or to its left.
3. **Converge**: `lo` and `hi` meet at the minimum.

---

## 📌 Key Takeaways

- ✅ **Binary search** halves the search range each step: **O(log n)**; it needs **sorted** or **monotonic** data.
- ✅ Classic loop: `while (lo <= hi)` with `lo = mid + 1` / `hi = mid - 1`; compute `mid = lo + (hi - lo) ~/ 2`.
- ✅ For duplicates, keep searching after a match to find the **first** or **last** occurrence.
- ✅ **Lower/upper bound** (half-open `[lo, hi)`) give insertion points and O(log n) range counts.
- ✅ The universal pattern: find the **first index where a monotonic condition becomes true**.
- ✅ **Binary search on the answer** solves "minimum capacity / speed / time" problems with a feasibility check.
- ✅ Rotated arrays still allow O(log n) search because one half is always sorted.

**Next up:** 🫧 **Elementary Sorts**: bubble, selection and insertion sort, and why they're O(n²).
