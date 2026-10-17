# Counting & Radix Sort

Imagine sorting **10,000 exam scores**, each between **0 and 100** 📝.

You *could* compare scores against each other with merge sort. But there's a smarter way:

- Set up **101 boxes**, labeled 0 to 100. 📦
- Drop each paper into the box matching its score. No comparisons at all!
- Empty the boxes in order: box 0, box 1, ..., box 100. Sorted. ✅

That took **one pass** over the papers plus one pass over the boxes.

👉 That's the idea behind **non-comparison sorts**:

> **Counting sort**, **radix sort** and **bucket sort** don't compare elements against each other. They use the **values themselves** (as indexes or digits) to place elements, which lets them run in **O(n + k)** or **O(d × (n + b))** time, beating the O(n log n) limit of comparison sorts when the **range of keys is small** or keys have **few digits**.

---

## 🚧 Breaking the O(n log n) Barrier

In the last lesson we saw that **comparison** sorts need about n log n comparisons in the worst case. That limit only applies when the algorithm learns about the data **solely by comparing** pairs.

If we know something extra, like "all keys are integers from 0 to 100", we can **index** directly instead of comparing.

| Algorithm | Time | Extra space | Stable | Works when |
|-----------|------|-------------|--------|------------|
| **Counting sort** | O(n + k) | O(n + k) | ✅ | Integer keys in a small range of size k |
| **Radix sort (LSD)** | O(d × (n + b)) | O(n + b) | ✅ | Keys with d digits in base b (ints, fixed-length strings) |
| **Bucket sort** | O(n) average | O(n + buckets) | ✅ (usually) | Values spread evenly over a known range |

---

## 🔢 Counting Sort: The Simple Version

```dart
List<int> countingSortSimple(List<int> a, int maxValue) {
  final counts = List<int>.filled(maxValue + 1, 0);
  for (final x in a) {
    counts[x]++; // tally each value
  }
  final out = <int>[];
  for (var v = 0; v <= maxValue; v++) {
    for (var c = 0; c < counts[v]; c++) {
      out.add(v); // emit each value as many times as it appeared
    }
  }
  return out;
}

void main() {
  final scores = [88, 72, 95, 72, 100, 60, 88, 88];
  print(countingSortSimple(scores, 100));
  // [60, 72, 72, 88, 88, 88, 95, 100]
}
```

**🔍 What This Code Does:**

1. **Count Array**: `counts[v]` is how many times value `v` appears; its size is the key range `k = maxValue + 1`.
2. **Tally Pass**: O(n), one increment per element.
3. **Output Pass**: Walk values in increasing order and write each the right number of times: O(n + k).
4. **No Comparisons**: The values themselves are used as array indexes.
5. **Limitation**: This version rebuilds values from counts, so it only works for plain integers, not records with extra data.

---

## 🏷️ Stable Counting Sort (for Records)

Real data has **keys** attached to **records**: sort students by grade while keeping each student's name. We need the **position** where each key's group starts, computed with a **prefix sum** of the counts.

```dart
typedef Student = ({String name, int grade});

List<Student> countingSortBy(List<Student> items, int maxKey) {
  final counts = List<int>.filled(maxKey + 1, 0);
  for (final s in items) {
    counts[s.grade]++;
  }
  // Prefix sums: counts[k] becomes the starting index for key k
  var total = 0;
  for (var k = 0; k <= maxKey; k++) {
    final c = counts[k];
    counts[k] = total;
    total += c;
  }
  // Place items in original order → stable
  final out = List<Student?>.filled(items.length, null);
  for (final s in items) {
    out[counts[s.grade]++] = s;
  }
  return out.cast<Student>();
}

void main() {
  final students = <Student>[
    (name: 'Zoe', grade: 3),
    (name: 'Ali', grade: 1),
    (name: 'Mia', grade: 3),
    (name: 'Ben', grade: 2),
    (name: 'Kai', grade: 1),
  ];
  for (final s in countingSortBy(students, 3)) {
    print('${s.grade} ${s.name}');
  }
  // 1 Ali
  // 1 Kai
  // 2 Ben
  // 3 Zoe
  // 3 Mia
}
```

**🔍 What This Code Does:**

1. **Count Each Key**: How many students have each grade.
2. **Prefix Sums → Starting Positions**: Grade 1 starts at 0, grade 2 starts after all grade-1 students, and so on (see **Prefix Sums**).
3. **Place in Input Order**: Walking the input from left to right and writing to `counts[key]++` keeps equal keys in their original order, so the sort is **stable** (Zoe before Mia, Ali before Kai).
4. **`cast<Student>()`**: Converts the filled `List<Student?>` into a non-nullable view.
5. **O(n + k)** time and space.

```text
grades:   [3, 1, 3, 2, 1]
counts:   [0, 2, 1, 2]       (key 0..3)
starts:   [0, 0, 2, 3]       (prefix sums)
placing:  Zoe(3)→3, Ali(1)→0, Mia(3)→4, Ben(2)→2, Kai(1)→1
result:   [Ali, Kai, Ben, Zoe, Mia]
```

### Handling negative numbers

Shift every key by the minimum so indexes start at 0.

```dart
List<int> countingSortRange(List<int> a) {
  if (a.isEmpty) return a;
  final lo = a.reduce((x, y) => x < y ? x : y);
  final hi = a.reduce((x, y) => x > y ? x : y);
  final counts = List<int>.filled(hi - lo + 1, 0);
  for (final x in a) {
    counts[x - lo]++; // offset so the smallest value maps to index 0
  }
  return [
    for (var i = 0; i < counts.length; i++)
      for (var c = 0; c < counts[i]; c++) i + lo,
  ];
}

void main() {
  print(countingSortRange([3, -2, 0, -2, 5, 1])); // [-2, -2, 0, 1, 3, 5]
}
```

**🔍 What This Code Does:**

1. **Find the Range**: The minimum and maximum define `k = hi − lo + 1`.
2. **Offset Keys**: `x − lo` turns −2 into index 0.
3. **Nested Collection-for**: Builds the output in one expression.

### When counting sort is a bad idea

```dart
void main() {
  final a = [1, 1000000000]; // only 2 elements...
  final k = a[1] - a[0] + 1;
  print('count array would need $k slots'); // 1000000000 slots for 2 numbers!
}
```

**🔍 What This Code Does:**

1. **Range Matters, Not Size**: Counting sort's cost and memory depend on **k**, the key range.
2. **Huge k = Huge Waste**: A billion-slot array to sort two numbers. Use a comparison sort or radix sort instead.

---

## 📟 Radix Sort (LSD)

What if keys are big numbers, like 6-digit zip codes or 32-bit integers? A count array would be enormous. **Radix sort** sorts **one digit at a time**, using a stable counting sort on each digit, starting from the **least significant digit** (LSD).

```dart
List<int> radixSort(List<int> a) {
  if (a.isEmpty) return a;
  var current = [...a];
  final maxValue = current.reduce((x, y) => x > y ? x : y);

  for (var exp = 1; maxValue ~/ exp > 0; exp *= 10) {
    // Stable counting sort by the digit at position `exp`
    final counts = List<int>.filled(10, 0);
    for (final x in current) {
      counts[(x ~/ exp) % 10]++;
    }
    var total = 0;
    for (var d = 0; d < 10; d++) {
      final c = counts[d];
      counts[d] = total;
      total += c;
    }
    final next = List<int>.filled(current.length, 0);
    for (final x in current) {
      next[counts[(x ~/ exp) % 10]++] = x;
    }
    current = next;
    print('after digit $exp: $current');
  }
  return current;
}

void main() {
  print(radixSort([170, 45, 75, 90, 802, 24, 2, 66]));
}
```

**🔍 What This Code Does:**

This code demonstrates **least-significant-digit radix sort in base 10**:

1. **Digit Extraction**: `(x ~/ exp) % 10` gives the ones digit when `exp = 1`, the tens digit when `exp = 10`, and so on.

2. **One Stable Pass per Digit**: Each pass is a counting sort with only **10** buckets.

3. **Why Stability Is Essential**: After sorting by the tens digit, numbers with the same tens digit must **keep** the order from the ones-digit pass. That's how earlier digits keep mattering.

4. **Number of Passes**: d = number of digits in the maximum (3 for 802).

5. **Complexity**: O(d × (n + 10)), effectively **O(n)** when d is a small constant.

**Output:**

```text
after digit 1:   [170, 90, 802, 2, 24, 45, 75, 66]
after digit 10:  [802, 2, 24, 45, 66, 170, 75, 90]
after digit 100: [2, 24, 45, 66, 75, 90, 170, 802]
[2, 24, 45, 66, 75, 90, 170, 802]
```

> 💡 Real implementations often use base **256** (one byte per pass), so a 32-bit integer needs only 4 passes.

### Radix sort on strings

Fixed-length strings like dates (`'2026-03-09'`), product codes or license plates can be sorted character by character from **right to left**.

```dart
List<String> radixSortStrings(List<String> words) {
  final width = words.first.length; // all strings have the same length
  var current = [...words];
  for (var pos = width - 1; pos >= 0; pos--) {
    final buckets = List.generate(128, (_) => <String>[]); // ASCII
    for (final w in current) {
      buckets[w.codeUnitAt(pos)].add(w); // stable: appended in order
    }
    current = [for (final b in buckets) ...b];
  }
  return current;
}

void main() {
  print(radixSortStrings(['dab', 'cab', 'fad', 'bad', 'dad', 'ebb', 'ace', 'add']));
  // [ace, add, bad, cab, dab, dad, ebb, fad]
}
```

**🔍 What This Code Does:**

1. **Right to Left**: The last character is the least significant.
2. **Buckets as Lists**: Appending to a bucket in input order keeps each pass stable.
3. **Flatten**: Concatenating buckets in code-unit order gives the next ordering.
4. **O(width × (n + 128))** for n strings.

---

## 🪣 Bucket Sort

When values are **floating-point numbers spread evenly** over a range, split the range into **n buckets**, sort each small bucket (insertion sort is ideal), and concatenate.

```dart
List<double> bucketSort(List<double> a) {
  final n = a.length;
  final buckets = List.generate(n, (_) => <double>[]);
  for (final x in a) {
    final i = (x * n).floor().clamp(0, n - 1); // values in [0, 1)
    buckets[i].add(x);
  }
  for (final b in buckets) {
    b.sort(); // each bucket is tiny on average
  }
  return [for (final b in buckets) ...b];
}

void main() {
  print(bucketSort([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]));
  // [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
}
```

**🔍 What This Code Does:**

1. **Bucket Index**: A value `x` in `[0, 1)` goes to bucket `floor(x × n)`.
2. **Small Buckets**: With evenly spread data, each bucket holds about one element.
3. **Sort and Join**: Sorting tiny buckets is fast; concatenating them gives the final order.
4. **O(n) Average**: But if all values land in one bucket, it degrades to that bucket's sort time.

---

## 🧮 Counting Without Sorting

Often you don't need the sorted list at all, just **counts** or the **top values**. Counting arrays answer those directly.

```dart
void main() {
  final ratings = [5, 3, 4, 5, 2, 5, 4, 1, 5, 3];
  final counts = List<int>.filled(6, 0); // stars 0..5
  for (final r in ratings) {
    counts[r]++;
  }
  for (var star = 5; star >= 1; star--) {
    print('$star★ ${'█' * counts[star]} ${counts[star]}');
  }
  final average = ratings.reduce((a, b) => a + b) / ratings.length;
  print('average: ${average.toStringAsFixed(1)}'); // average: 3.7
}
```

**🔍 What This Code Does:**

1. **Histogram**: Counts per star rating, just like the first half of counting sort.
2. **Bar Chart**: `'█' * n` repeats a block character for a quick text chart.
3. **O(n + k)**: No sorting needed to summarize.

---

## 🧭 Choosing a Sort

| Your data | Best choice |
|-----------|-------------|
| General objects, unknown range | `List.sort` (comparison, O(n log n)) |
| Small integer range (ages, scores, ratings) | **Counting sort** |
| Large integers or fixed-length strings | **Radix sort** |
| Uniformly distributed floats in a known range | **Bucket sort** |
| Need stable + general | Merge sort (`package:collection`) |
| Nearly sorted, small | Insertion sort |

---

## ⚠️ Common Mistakes

### 1. Using counting sort with a huge range

Memory and time grow with **k**, not n. Two numbers far apart can require a gigantic count array.

### 2. Using an unstable sort inside radix sort

Each digit pass **must** be stable, or the work of earlier passes is destroyed.

### 3. Forgetting negative numbers

Negative values can't be array indexes. Offset by the minimum, or handle negatives separately.

### 4. Radix sort on variable-length strings without padding

`'ab'` vs `'abc'`: LSD radix sort assumes equal lengths. Pad strings or use MSD (most significant digit first) radix sort.

---

## 🧪 Try It Yourself

1. Sort a list of people by **age** (0–120) with a stable counting sort.
2. Implement radix sort with **base 256** using bit operations: `(x >> shift) & 0xFF`.
3. **Sort colors**: sort a list containing only 0, 1 and 2 in one pass (Dutch national flag).
4. Find the **h-index**: the largest h such that a researcher has h papers with at least h citations each, using counting.

```dart
void sortColors(List<int> a) {
  var low = 0, mid = 0, high = a.length - 1;
  while (mid <= high) {
    if (a[mid] == 0) {
      final t = a[low];
      a[low++] = a[mid];
      a[mid++] = t;
    } else if (a[mid] == 2) {
      final t = a[high];
      a[high--] = a[mid];
      a[mid] = t;
    } else {
      mid++;
    }
  }
}

void main() {
  final a = [2, 0, 2, 1, 1, 0];
  sortColors(a);
  print(a); // [0, 0, 1, 1, 2, 2]
}
```

**🔍 What This Code Does:**

1. **Three Regions**: `[0, low)` holds 0s, `[low, mid)` holds 1s, `(high, end]` holds 2s.
2. **One Pass, In Place**: Each element is examined at most once or twice.
3. **Same Idea as Three-Way Partitioning**: From the quick sort lesson, with known values 0, 1 and 2.

---

## 📌 Key Takeaways

- ✅ **Non-comparison sorts** use key values directly and can beat **O(n log n)**.
- ✅ **Counting sort**: count each key, prefix-sum to positions, place stably: **O(n + k)**; only good for a **small key range k**.
- ✅ **Radix sort**: stable counting sort on each digit from least to most significant: **O(d × (n + b))**.
- ✅ **Stability** is what makes radix sort work.
- ✅ **Bucket sort**: distribute evenly spread values into buckets, sort each, concatenate: **O(n) average**.
- ✅ When the range is large or keys aren't integers, use a comparison sort like `List.sort`.

**Next up:** 🌲 **Module 7: Segment & Fenwick Trees**: range queries and updates in O(log n).
