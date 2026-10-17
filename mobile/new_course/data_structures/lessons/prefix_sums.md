# Prefix Sums & Difference Arrays

Imagine you're on a **road trip** 🚗 and the car's **odometer** shows the total distance driven since you left home.

- At the start of day 3, it reads **240 km**.
- At the end of day 5, it reads **610 km**.

How far did you drive on days 3 to 5? You don't add up every single day. You just subtract: **610 − 240 = 370 km**. 🧮

👉 That's a **prefix sum**:

> A **prefix sum** array stores the running total up to each position. Then the sum of **any range** is just **one subtraction**, O(1), no matter how long the range is.

And its mirror image, the **difference array**, lets you **add a value to a whole range** in O(1). Together they make range problems fast.

---

## 🐢 The Problem: Repeated Range Sums

A fitness app stores daily step counts. Users keep asking: *"How many steps between day `a` and day `b`?"*

```dart
int rangeSumSlow(List<int> steps, int a, int b) {
  var total = 0;
  for (var i = a; i <= b; i++) {
    total += steps[i]; // O(b - a + 1) per question
  }
  return total;
}

void main() {
  final steps = [3000, 8000, 6500, 10000, 4200, 12000, 7000];
  print(rangeSumSlow(steps, 1, 3)); // 24500
  print(rangeSumSlow(steps, 0, 6)); // 50700
}
```

**🔍 What This Code Does:**

1. **Loop Per Query**: Each question re-adds every day in the range.
2. **O(n) Per Query**: A long range costs as much as the whole array.
3. **Many Queries Hurt**: With `q` queries, total work is **O(n × q)**. A year of data and a million queries is far too slow.

---

## ✅ The Solution: Build Once, Answer Instantly

```dart
List<int> buildPrefix(List<int> nums) {
  final prefix = List<int>.filled(nums.length + 1, 0);
  for (var i = 0; i < nums.length; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
  }
  return prefix;
}

int rangeSum(List<int> prefix, int a, int b) => prefix[b + 1] - prefix[a];

void main() {
  final steps = [3000, 8000, 6500, 10000, 4200, 12000, 7000];
  final prefix = buildPrefix(steps);

  print(prefix);
  // [0, 3000, 11000, 17500, 27500, 31700, 43700, 50700]

  print(rangeSum(prefix, 1, 3)); // 24500
  print(rangeSum(prefix, 0, 6)); // 50700
  print(rangeSum(prefix, 4, 4)); // 4200
}
```

**🔍 What This Code Does:**

This code demonstrates **O(1) range sums after an O(n) build**:

1. **One Extra Slot**: `prefix` has length `n + 1`, with `prefix[0] = 0`. This avoids special cases for ranges starting at 0.

2. **Running Total**: `prefix[i + 1] = prefix[i] + nums[i]`, so `prefix[k]` is the sum of the **first k** elements.

3. **Range Formula**: Sum of `nums[a..b]` (inclusive) = `prefix[b + 1] − prefix[a]`.

4. **Build O(n), Query O(1)**: Total for `q` queries is **O(n + q)** instead of O(n × q).

5. **Single Element**: `rangeSum(prefix, 4, 4)` is just `nums[4]`.

**Visualizing it:**

```text
index:     0     1     2      3     4      5     6
nums:   3000  8000  6500  10000  4200  12000  7000
prefix: 0  3000 11000 17500 27500 31700 43700 50700
           ↑                 ↑
       prefix[1]         prefix[4]

sum(nums[1..3]) = prefix[4] - prefix[1] = 27500 - 3000 = 24500
```

> 💡 The trade-off: O(n) extra memory and a one-time O(n) build. It's worth it whenever you answer more than a handful of range queries and the data **doesn't change**.

---

## 🧩 Prefix Sums + Hash Map: Subarray Sum Equals K

**Problem:** Count how many **contiguous** subarrays sum to exactly `k`. The numbers can be **negative**, so a sliding window won't work.

**Insight:** The sum of `nums[i..j]` is `prefix[j+1] − prefix[i]`. We want that to equal `k`, so:

```text
prefix[i] = prefix[j+1] − k
```

As we walk forward, we ask: *"How many earlier prefixes equal `current − k`?"* A hash map counts them.

```dart
int subarraySum(List<int> nums, int k) {
  final seen = <int, int>{0: 1}; // empty prefix seen once
  var running = 0;
  var count = 0;

  for (final x in nums) {
    running += x;
    count += seen[running - k] ?? 0;
    seen[running] = (seen[running] ?? 0) + 1;
  }
  return count;
}

void main() {
  print(subarraySum([1, 1, 1], 2));          // 2  ([1,1] twice)
  print(subarraySum([1, 2, 3], 3));          // 2  ([1,2] and [3])
  print(subarraySum([3, 4, -7, 1, 3, 3], 7)); // 3
}
```

**🔍 What This Code Does:**

1. **Running Prefix**: `running` is the sum of everything so far, so we don't even need the full prefix array.
2. **Look Back With a Map**: `seen[running - k]` tells us how many earlier starting points produce a subarray summing to `k`.
3. **`{0: 1}` Seed**: Accounts for subarrays that start at index 0.
4. **Order Matters**: Count first, then record the current prefix, so a subarray can't be empty.
5. **O(n) Time, O(n) Space**: Handles negative numbers, unlike the sliding window.

### Longest subarray with sum zero

```dart
int longestZeroSum(List<int> nums) {
  final firstIndex = <int, int>{0: -1};
  var running = 0, best = 0;
  for (var i = 0; i < nums.length; i++) {
    running += nums[i];
    final first = firstIndex[running];
    if (first != null) {
      if (i - first > best) best = i - first;
    } else {
      firstIndex[running] = i; // only store the FIRST time
    }
  }
  return best;
}

void main() {
  print(longestZeroSum([15, -2, 2, -8, 1, 7, 10, 23])); // 5  ([-2, 2, -8, 1, 7])
}
```

**🔍 What This Code Does:**

1. **Same Prefix Twice = Zero Sum Between**: If `running` repeats, the elements in between sum to 0.
2. **Keep the Earliest Index**: Storing only the first occurrence maximizes the length.
3. **`0: -1` Seed**: Handles zero-sum subarrays starting at index 0.

---

## 🧱 2D Prefix Sums: Rectangles in O(1)

Images, heat maps and game boards often need the sum of a **rectangle**.

```dart
List<List<int>> build2D(List<List<int>> grid) {
  final rows = grid.length, cols = grid[0].length;
  final p = List.generate(rows + 1, (_) => List.filled(cols + 1, 0));
  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      p[r + 1][c + 1] = grid[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
    }
  }
  return p;
}

int rectSum(List<List<int>> p, int r1, int c1, int r2, int c2) =>
    p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];

void main() {
  final grid = [
    [3, 0, 1, 4],
    [5, 6, 3, 2],
    [1, 2, 0, 1],
  ];
  final p = build2D(grid);
  print(rectSum(p, 1, 1, 2, 2)); // 6 + 3 + 2 + 0 = 11
  print(rectSum(p, 0, 0, 2, 3)); // whole grid = 28
}
```

**🔍 What This Code Does:**

1. **`p[r][c]`**: The sum of the rectangle from `(0, 0)` up to (but not including) row `r`, column `c`.
2. **Build Formula**: Add the cell, the area above, and the area to the left, then **subtract** the top-left area that was counted twice.
3. **Query Formula (Inclusion–Exclusion)**: Take the big rectangle, remove the strip above and the strip to the left, then **add back** the corner removed twice.
4. **O(rows × cols) Build, O(1) Query**: Perfect for many rectangle questions.

```text
  ┌───────────┬──────┐
  │    A      │  B   │      rect = total - (A+B) - (A+C) + A
  ├───────────┼──────┤
  │    C      │ rect │
  └───────────┴──────┘
```

---

## ➖ Difference Arrays: Range Updates in O(1)

Now flip the problem. A concert venue 🎟️ receives bookings like *"add 50 people to seats 10–40"*. After **all** bookings, you need the count at every seat.

Updating every seat for every booking is O(n) per booking. A **difference array** records only where changes **start** and **stop**.

```dart
List<int> applyRangeAdds(int n, List<(int, int, int)> updates) {
  final diff = List<int>.filled(n + 1, 0);
  for (final (start, end, value) in updates) {
    diff[start] += value;   // start adding here
    diff[end + 1] -= value; // stop adding after `end`
  }
  // Prefix sum of the differences gives the final values
  final result = List<int>.filled(n, 0);
  var running = 0;
  for (var i = 0; i < n; i++) {
    running += diff[i];
    result[i] = running;
  }
  return result;
}

void main() {
  final seats = applyRangeAdds(8, [
    (1, 3, 10), // seats 1..3 get +10
    (2, 6, 5),  // seats 2..6 get +5
    (0, 7, 1),  // every seat gets +1
  ]);
  print(seats); // [1, 11, 16, 16, 6, 6, 6, 1]
}
```

**🔍 What This Code Does:**

1. **Mark Boundaries**: `+value` at the start index and `-value` just after the end index.
2. **Record Destructuring**: `for (final (start, end, value) in updates)` unpacks each `(int, int, int)` record.
3. **One Final Pass**: A prefix sum over `diff` spreads every update across its range.
4. **O(1) Per Update + O(n) Once**: Total O(n + u) for `u` updates instead of O(n × u).
5. **Extra Slot**: `diff` has `n + 1` entries so `end + 1` is always valid.

**Trace:**

```text
after (1,3,10): diff = [0, 10,  0,  0, -10,  0,  0,  0,  0]
after (2,6,5):  diff = [0, 10,  5,  0, -10,  0,  0, -5,  0]
after (0,7,1):  diff = [1, 10,  5,  0, -10,  0,  0, -5, -1]
prefix sums:          [1, 11, 16, 16,   6,  6,  6,  1]
```

> 💡 **Prefix sums** and **difference arrays** are inverses: the prefix sum of a difference array gives back the original values.

### Car pooling: is capacity ever exceeded?

```dart
bool carPooling(List<(int, int, int)> trips, int capacity) {
  // (passengers, from, to): passengers ride from `from` and leave AT `to`
  var maxStop = 0;
  for (final (_, _, to) in trips) {
    if (to > maxStop) maxStop = to;
  }
  final diff = List<int>.filled(maxStop + 1, 0);
  for (final (people, from, to) in trips) {
    diff[from] += people;
    diff[to] -= people; // they leave at `to`, so no +1
  }
  var onboard = 0;
  for (final change in diff) {
    onboard += change;
    if (onboard > capacity) return false;
  }
  return true;
}

void main() {
  print(carPooling([(2, 1, 5), (3, 3, 7)], 4)); // false (5 people on board at stop 3)
  print(carPooling([(2, 1, 5), (3, 5, 7)], 4)); // true  (first group leaves at 5)
}
```

**🔍 What This Code Does:**

1. **Wildcard Patterns**: `(_, _, to)` ignores the fields we don't need.
2. **Half-Open Ranges**: Passengers occupy `[from, to)`, so the decrease goes exactly at `to`.
3. **Sweep**: Running through the diff array simulates the trip stop by stop.
4. **Early Exit**: Return `false` as soon as capacity is exceeded.

---

## ✖️ Beyond Sums: Prefix Products and Prefix Max

The idea works for any operation you can "accumulate".

### Product of array except self (no division)

```dart
List<int> productExceptSelf(List<int> nums) {
  final n = nums.length;
  final out = List<int>.filled(n, 1);

  var left = 1;
  for (var i = 0; i < n; i++) {
    out[i] = left;      // product of everything to the left
    left *= nums[i];
  }

  var right = 1;
  for (var i = n - 1; i >= 0; i--) {
    out[i] *= right;    // times product of everything to the right
    right *= nums[i];
  }
  return out;
}

void main() {
  print(productExceptSelf([1, 2, 3, 4])); // [24, 12, 8, 6]
}
```

**🔍 What This Code Does:**

1. **Prefix Products (Left)**: `out[i]` first holds the product of all elements before `i`.
2. **Suffix Products (Right)**: A backward pass multiplies in the product of all elements after `i`.
3. **No Division**: Works even when the array contains zeros.
4. **O(n) Time, O(1) Extra Space**: Besides the output list.

### Running maximum

```dart
void main() {
  final temps = [12, 15, 11, 18, 14, 20, 19];
  final best = <int>[];
  var current = temps.first;
  for (final t in temps) {
    if (t > current) current = t;
    best.add(current);
  }
  print(best); // [12, 15, 15, 18, 18, 20, 20]
}
```

**🔍 What This Code Does:**

1. **Prefix Maximum**: `best[i]` is the highest temperature up to day `i`.
2. **One Pass**: Each new value is compared to the running max.
3. **Limitation**: Unlike sums, you **can't** subtract maxima, so a prefix max can't answer arbitrary range-max queries. That needs a **segment tree** (Module 7).

---

## 🧮 Quick Reference

| Task | Technique | Build | Query/Update |
|------|-----------|-------|--------------|
| Sum of range `[a, b]` (static data) | Prefix sum | O(n) | O(1) query |
| Count subarrays with sum k | Prefix sum + hash map | — | O(n) total |
| Sum of a rectangle | 2D prefix sum | O(rows × cols) | O(1) query |
| Add value to many ranges, read at the end | Difference array | O(n) final pass | O(1) update |
| Range sums with frequent point updates | Fenwick / segment tree | O(n) | O(log n) both |

---

## ⚠️ Common Mistakes

### 1. Off-by-one in the range formula

```dart
void main() {
  final nums = [5, 1, 4];
  final prefix = [0, 5, 6, 10];
  // sum of nums[1..2] = 1 + 4 = 5
  print(prefix[2] - prefix[1]); // ❌ 1 (only nums[1])
  print(prefix[3] - prefix[1]); // ✅ 5
}
```

**🔍 What This Code Does:**

1. **Inclusive End**: The range `[a, b]` needs `prefix[b + 1]`, not `prefix[b]`.
2. **Tip**: With the extra leading `0`, `prefix[k]` means "sum of the first k elements".

### 2. Forgetting the `{0: 1}` seed

Without it, subarrays starting at index 0 are never counted in "subarray sum equals k".

### 3. Using prefix sums on changing data

If values change after building, every later prefix entry is wrong, and rebuilding costs O(n). For frequent updates, use a **Fenwick tree** or **segment tree**.

### 4. Integer overflow

Long running totals can grow very large. Dart's native `int` is 64-bit on the VM, so overflow is rare, but on the **web** integers are JavaScript doubles and lose precision above 2⁵³.

---

## 🧪 Try It Yourself

1. **Pivot index**: find an index where the sum of the left side equals the sum of the right side.
2. **Range sum queries**: build an `NumArray` class with `sumRange(a, b)` in O(1).
3. **Subarrays divisible by k**: count subarrays whose sum is divisible by `k`. *(Hint: store `running % k` in the map, careful with negatives.)*
4. **Flight bookings**: given bookings `(first, last, seats)`, return the total seats booked on each flight using a difference array.

```dart
int pivotIndex(List<int> nums) {
  final total = nums.fold(0, (a, b) => a + b);
  var left = 0;
  for (var i = 0; i < nums.length; i++) {
    if (left == total - left - nums[i]) return i;
    left += nums[i];
  }
  return -1;
}

void main() {
  print(pivotIndex([1, 7, 3, 6, 5, 6])); // 3
}
```

**🔍 What This Code Does:**

1. **Total Once**: `fold` sums the whole list.
2. **Right Side Without a Second Array**: `total - left - nums[i]` is the sum to the right.
3. **O(n)**: A single pass after the total.

---

## 📌 Key Takeaways

- ✅ A **prefix sum** stores running totals so any range sum is `prefix[b + 1] − prefix[a]`, **O(1)**.
- ✅ Build is **O(n)**; the leading **0** removes edge cases.
- ✅ **Prefix sum + hash map** counts subarrays with a target sum in **O(n)**, even with negative numbers.
- ✅ **2D prefix sums** answer rectangle sums in O(1) using inclusion–exclusion.
- ✅ A **difference array** applies range updates in **O(1)** each; one prefix pass produces the final values.
- ✅ The idea generalizes to **products**, and **running max/min** (with limits).
- ✅ For data that **changes often**, use Fenwick or segment trees instead.

**Next up:** 🔗 **Singly Linked Lists**, our first structure built entirely from **references**.
