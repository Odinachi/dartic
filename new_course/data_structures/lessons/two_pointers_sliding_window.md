# Two Pointers & Sliding Window

Imagine two friends searching a **bookshelf** 📚 sorted by price, looking for **two books that cost exactly $30 together**.

- 👈 One friend starts at the **cheapest** book on the left.
- 👉 The other starts at the **most expensive** book on the right.
- If the pair costs **too much**, the right friend steps **left** (cheaper).
- If it costs **too little**, the left friend steps **right** (pricier).
- They meet in the middle having checked each book **at most once**. 🎯

Now imagine looking through a **train window** 🚆 that shows exactly 3 houses at a time. As the train moves, one house **slides in** on the right and one **slides out** on the left. You never need to look at the whole street again.

👉 These are the two most useful patterns for arrays and strings:

> **Two pointers**: use two indexes that move toward each other (or in the same direction) to avoid checking every pair.
>
> **Sliding window**: maintain a contiguous range `[left, right]` and update it incrementally as it slides, instead of recomputing from scratch.

Both often turn **O(n²)** brute force into **O(n)**. 🚀

---

## 🐢 The Brute Force Problem

**Problem:** In a **sorted** list, find two numbers that add up to a target.

```dart
(int, int)? pairSumBrute(List<int> nums, int target) {
  for (var i = 0; i < nums.length; i++) {
    for (var j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] == target) return (i, j);
    }
  }
  return null;
}

void main() {
  print(pairSumBrute([1, 3, 4, 6, 8, 11], 10)); // (2, 3) → 4 + 6
}
```

**🔍 What This Code Does:**

1. **Every Pair**: The nested loops check all `n(n−1)/2` pairs.
2. **Record Return Type**: `(int, int)?` returns the two indexes, or `null` if no pair exists.
3. **Result**: The first pair found is `(2, 3)` (4 + 6 = 10).
4. **O(n²)**: Fine for 100 items, painfully slow for 1,000,000.

> The brute force ignores a huge clue: **the list is sorted**. Two pointers exploits that.

---

## 👉👈 Pattern 1: Opposite-Direction Pointers

```dart
(int, int)? pairSum(List<int> nums, int target) {
  var left = 0;
  var right = nums.length - 1;

  while (left < right) {
    final sum = nums[left] + nums[right];
    if (sum == target) return (left, right);
    if (sum < target) {
      left++;  // need a bigger sum
    } else {
      right--; // need a smaller sum
    }
  }
  return null;
}

void main() {
  final prices = [1, 3, 4, 6, 8, 11];
  print(pairSum(prices, 10)); // (2, 3)  → 4 + 6
  print(pairSum(prices, 19)); // (4, 5)  → 8 + 11
  print(pairSum(prices, 100)); // null
}
```

**🔍 What This Code Does:**

This code demonstrates **the classic sorted two-sum with two pointers**:

1. **Start at Both Ends**: `left` at the smallest value, `right` at the largest.

2. **Too Small → Move Left Up**: Since the list is sorted, moving `left` right can only **increase** the sum.

3. **Too Big → Move Right Down**: Moving `right` left can only **decrease** the sum.

4. **Why It's Safe**: When we move `left` past a value, that value can't be part of any answer with the remaining `right` values (they'd all be too small). So nothing is missed.

5. **O(n) Time, O(1) Space**: Each step moves one pointer, at most `n` steps total.

**Trace for target 10:**

| left | right | values | sum | action |
|------|-------|--------|-----|--------|
| 0 | 5 | 1 + 11 | 12 | too big → right-- |
| 0 | 4 | 1 + 8 | 9 | too small → left++ |
| 1 | 4 | 3 + 8 | 11 | too big → right-- |
| 1 | 3 | 3 + 6 | 9 | too small → left++ |
| 2 | 3 | 4 + 6 | 10 | ✅ found |

---

### 🏞️ Container With Most Water

Given heights of vertical lines, find two lines that hold the most water.

```dart
import 'dart:math';

int maxArea(List<int> heights) {
  var left = 0, right = heights.length - 1;
  var best = 0;
  while (left < right) {
    final width = right - left;
    final h = min(heights[left], heights[right]);
    best = max(best, width * h);
    // Move the shorter line: the taller one can't help while the short one limits us
    if (heights[left] < heights[right]) {
      left++;
    } else {
      right--;
    }
  }
  return best;
}

void main() {
  print(maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])); // 49
}
```

**🔍 What This Code Does:**

1. **Area**: Width between the lines × the **shorter** line's height.
2. **Greedy Move**: Moving the **taller** line inward can only shrink the width without raising the limiting height, so we always move the **shorter** one.
3. **`min` / `max`**: From `dart:math`.
4. **O(n)**: Instead of checking all O(n²) pairs.

---

### 🔺 Three Sum (sort + two pointers)

Find all **unique** triplets that sum to zero.

```dart
List<List<int>> threeSum(List<int> input) {
  final nums = [...input]..sort();
  final result = <List<int>>[];

  for (var i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] == nums[i - 1]) continue; // skip duplicate anchors
    var left = i + 1, right = nums.length - 1;
    while (left < right) {
      final sum = nums[i] + nums[left] + nums[right];
      if (sum == 0) {
        result.add([nums[i], nums[left], nums[right]]);
        left++;
        right--;
        while (left < right && nums[left] == nums[left - 1]) left++;
        while (left < right && nums[right] == nums[right + 1]) right--;
      } else if (sum < 0) {
        left++;
      } else {
        right--;
      }
    }
  }
  return result;
}

void main() {
  print(threeSum([-1, 0, 1, 2, -1, -4])); // [[-1, -1, 2], [-1, 0, 1]]
}
```

**🔍 What This Code Does:**

1. **Sort First**: O(n log n), which makes the two-pointer trick possible.
2. **Fix One, Two-Pointer the Rest**: For each anchor `nums[i]`, find pairs summing to `-nums[i]`.
3. **Skip Duplicates**: Equal anchors and equal neighbors are skipped so each triplet appears once.
4. **O(n²) Total**: n anchors × O(n) scan, much better than O(n³) brute force.

---

## 🐢🐇 Pattern 2: Same-Direction Pointers (Fast & Slow)

Both pointers move left to right, but at **different speeds** or for **different jobs**: one **reads**, the other **writes**.

### Remove duplicates in place (sorted)

```dart
int removeDuplicates(List<int> nums) {
  if (nums.isEmpty) return 0;
  var slow = 0;
  for (var fast = 1; fast < nums.length; fast++) {
    if (nums[fast] != nums[slow]) {
      slow++;
      nums[slow] = nums[fast];
    }
  }
  return slow + 1; // number of unique values
}

void main() {
  final nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4];
  final k = removeDuplicates(nums);
  print(k);                    // 5
  print(nums.sublist(0, k));   // [0, 1, 2, 3, 4]
}
```

**🔍 What This Code Does:**

1. **Fast Pointer Reads**: `fast` scans every element.
2. **Slow Pointer Writes**: `slow` marks the end of the unique section.
3. **Only Advance on New Values**: When `fast` finds something different, it's copied to `slow + 1`.
4. **O(n) Time, O(1) Space**: The list is compacted in place.

### Is subsequence?

```dart
bool isSubsequence(String small, String big) {
  var i = 0;
  for (var j = 0; j < big.length && i < small.length; j++) {
    if (small[i] == big[j]) i++;
  }
  return i == small.length;
}

void main() {
  print(isSubsequence('ace', 'abcde')); // true
  print(isSubsequence('aec', 'abcde')); // false
}
```

**🔍 What This Code Does:**

1. **Two Strings, Two Pointers**: `i` walks `small`, `j` walks `big`.
2. **Match Advances `i`**: Characters must appear in order, but not necessarily next to each other.
3. **O(n + m)**: Each pointer only moves forward.

### Merge two sorted lists

```dart
List<int> mergeSorted(List<int> a, List<int> b) {
  final out = <int>[];
  var i = 0, j = 0;
  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) {
      out.add(a[i++]);
    } else {
      out.add(b[j++]);
    }
  }
  out
    ..addAll(a.sublist(i))
    ..addAll(b.sublist(j));
  return out;
}

void main() {
  print(mergeSorted([1, 4, 7], [2, 3, 8, 9])); // [1, 2, 3, 4, 7, 8, 9]
}
```

**🔍 What This Code Does:**

1. **Compare Heads**: Take the smaller of `a[i]` and `b[j]`.
2. **Post-Increment**: `a[i++]` uses `i`, then increments it.
3. **Leftovers**: When one list runs out, append the rest of the other.
4. **O(n + m)**: This is the heart of **merge sort**.

---

## 🪟 Pattern 3: Fixed-Size Sliding Window

**Problem:** Find the maximum sum of any `k` consecutive elements.

```dart
int maxSumBrute(List<int> nums, int k) {
  var best = -1 << 62;
  for (var i = 0; i + k <= nums.length; i++) {
    var sum = 0;
    for (var j = i; j < i + k; j++) {
      sum += nums[j]; // recomputes the overlap every time ❌
    }
    if (sum > best) best = sum;
  }
  return best;
}

int maxSumWindow(List<int> nums, int k) {
  var windowSum = 0;
  for (var i = 0; i < k; i++) {
    windowSum += nums[i]; // first window
  }
  var best = windowSum;
  for (var right = k; right < nums.length; right++) {
    windowSum += nums[right] - nums[right - k]; // slide: add new, drop old ✅
    if (windowSum > best) best = windowSum;
  }
  return best;
}

void main() {
  final sales = [2, 1, 5, 1, 3, 2, 9, 1];
  print(maxSumBrute(sales, 3));  // 14
  print(maxSumWindow(sales, 3)); // 14
}
```

**🔍 What This Code Does:**

1. **Brute Force Is O(n × k)**: Every window is summed from scratch, even though neighboring windows share `k − 1` elements.
2. **Sliding Update**: Moving the window right adds `nums[right]` and removes `nums[right - k]`, O(1) per step.
3. **First Window**: Summed once before sliding.
4. **O(n) Total**: Each element enters and leaves the window once.
5. **Very Small Start**: `-1 << 62` is a large negative number to start the maximum safely.

**Window positions for k = 3:**

```text
[2 1 5] 1 3 2 9 1   sum = 8
2 [1 5 1] 3 2 9 1   sum = 8 - 2 + 1 = 7
2 1 [5 1 3] 2 9 1   sum = 7 - 1 + 3 = 9
2 1 5 [1 3 2] 9 1   sum = 9 - 5 + 2 = 6
2 1 5 1 [3 2 9] 1   sum = 6 - 1 + 9 = 14 ✅
2 1 5 1 3 [2 9 1]   sum = 14 - 3 + 1 = 12
```

### Moving average

```dart
List<double> movingAverage(List<num> values, int k) {
  final out = <double>[];
  num sum = 0;
  for (var i = 0; i < values.length; i++) {
    sum += values[i];
    if (i >= k) sum -= values[i - k];
    if (i >= k - 1) out.add(sum / k);
  }
  return out;
}

void main() {
  print(movingAverage([10, 20, 30, 40, 50], 2)); // [15.0, 25.0, 35.0, 45.0]
}
```

**🔍 What This Code Does:**

1. **Add Incoming**: Every value joins the running sum.
2. **Remove Outgoing**: Once the window is full, drop the value `k` steps back.
3. **Emit When Full**: Averages start once `k` values are in the window.
4. **Real Use**: Smoothing stock prices, sensor readings or frame times.

---

## 🪗 Pattern 4: Variable-Size Sliding Window

The window **grows** on the right and **shrinks** from the left whenever a condition is broken.

### Longest substring without repeating characters

```dart
int longestUniqueSubstring(String s) {
  final lastSeen = <String, int>{};
  var left = 0;
  var best = 0;

  for (var right = 0; right < s.length; right++) {
    final ch = s[right];
    final prev = lastSeen[ch];
    if (prev != null && prev >= left) {
      left = prev + 1; // jump past the previous copy
    }
    lastSeen[ch] = right;
    final length = right - left + 1;
    if (length > best) best = length;
  }
  return best;
}

void main() {
  print(longestUniqueSubstring('abcabcbb')); // 3 ("abc")
  print(longestUniqueSubstring('bbbbb'));    // 1 ("b")
  print(longestUniqueSubstring('pwwkew'));   // 3 ("wke")
}
```

**🔍 What This Code Does:**

1. **Expand Right**: Every step adds `s[right]` to the window.
2. **Shrink Left on Repeat**: If the character was seen **inside** the current window, move `left` just past its last position.
3. **`prev >= left` Check**: Ignores old positions that are already outside the window.
4. **Window Length**: `right - left + 1`.
5. **O(n)**: `left` and `right` each move forward at most `n` times.

### Smallest subarray with sum ≥ target

```dart
int minSubarrayLen(int target, List<int> nums) {
  var left = 0, sum = 0;
  var best = nums.length + 1;
  for (var right = 0; right < nums.length; right++) {
    sum += nums[right];
    while (sum >= target) {
      final len = right - left + 1;
      if (len < best) best = len;
      sum -= nums[left++]; // shrink while still valid
    }
  }
  return best > nums.length ? 0 : best;
}

void main() {
  print(minSubarrayLen(7, [2, 3, 1, 2, 4, 3])); // 2 ([4, 3])
  print(minSubarrayLen(100, [1, 2, 3]));        // 0 (impossible)
}
```

**🔍 What This Code Does:**

1. **Grow Until Valid**: Add elements until the sum reaches the target.
2. **Shrink While Valid**: Remove from the left to find the **shortest** valid window ending at `right`.
3. **Sentinel**: `nums.length + 1` means "not found yet"; we return 0 if it never changes.
4. **Positive Numbers Only**: This works because adding always increases the sum and removing always decreases it.
5. **O(n)**: The inner `while` looks nested, but `left` only moves forward, n times in total.

### Longest window with at most k distinct characters

```dart
int longestKDistinct(String s, int k) {
  final counts = <String, int>{};
  var left = 0, best = 0;
  for (var right = 0; right < s.length; right++) {
    counts[s[right]] = (counts[s[right]] ?? 0) + 1;
    while (counts.length > k) {
      final out = s[left++];
      final c = counts[out]! - 1;
      if (c == 0) {
        counts.remove(out);
      } else {
        counts[out] = c;
      }
    }
    if (right - left + 1 > best) best = right - left + 1;
  }
  return best;
}

void main() {
  print(longestKDistinct('eceba', 2));   // 3 ("ece")
  print(longestKDistinct('aabbcc', 1));  // 2
}
```

**🔍 What This Code Does:**

1. **Frequency Map as Window State**: Tracks how many of each character are inside the window.
2. **`counts.length`**: The number of **distinct** characters currently in the window.
3. **Shrink When Too Many**: Remove characters from the left until only `k` distinct remain.
4. **Clean Up Zeros**: Remove keys whose count drops to 0 so `length` stays accurate.

---

## 🧭 Choosing the Right Pattern

| Clue in the problem | Pattern |
|---------------------|---------|
| Sorted array, find a pair/triplet with a sum | 👉👈 Opposite pointers |
| Palindrome, reverse in place | 👉👈 Opposite pointers |
| Remove/compact elements in place | 🐢🐇 Read/write pointers |
| Merge two sorted sequences | 🐢🐇 One pointer per sequence |
| "Every window of size k" | 🪟 Fixed window |
| "Longest/shortest contiguous subarray/substring such that..." | 🪗 Variable window |
| Unsorted array, pair with a sum | Hash set (see **Hashing Patterns**) |

> 💡 Sliding windows need **contiguous** ranges. If the problem is about any subset (not contiguous), it's usually not a window problem.

---

## ⚠️ Common Mistakes

### 1. Using opposite pointers on an unsorted list

```dart
void main() {
  final unsorted = [8, 1, 6, 3];
  final sorted = [...unsorted]..sort(); // ✅ sort first (or use a Set)
  var l = 0, r = sorted.length - 1;
  while (l < r) {
    final s = sorted[l] + sorted[r];
    if (s == 9) {
      print('${sorted[l]} + ${sorted[r]}');
      break;
    }
    if (s < 9) {
      l++;
    } else {
      r--;
    }
  }
}
```

**🔍 What This Code Does:**

1. **The Logic Depends on Order**: "Move left to increase the sum" only holds when sorted.
2. **Sort a Copy**: Sorting costs O(n log n) but makes the O(n) scan valid. The output is `1 + 8`.

### 2. Off-by-one window length

The length of `[left, right]` (both inclusive) is `right - left + 1`, not `right - left`.

### 3. Forgetting to shrink

In a variable window, the `while` loop that shrinks from the left is what keeps the window valid. Using `if` instead of `while` can leave the window invalid when one step isn't enough.

### 4. Sliding windows with negative numbers

The "shrink while sum ≥ target" trick assumes **non-negative** numbers. With negatives, use **prefix sums** with a hash map instead (next lesson).

---

## 🧪 Try It Yourself

1. **Squares of a sorted array**: given `[-4, -1, 0, 3, 10]`, return the sorted squares `[0, 1, 9, 16, 100]` in O(n) using opposite pointers.
2. **Max consecutive ones with k flips**: longest run of 1s if you may flip at most `k` zeros.
3. **Find all anagrams**: return every start index in `s` where an anagram of `p` begins (fixed window + counts).
4. **Valid palindrome II**: can the string become a palindrome by deleting at most one character?

```dart
List<int> sortedSquares(List<int> nums) {
  final out = List<int>.filled(nums.length, 0);
  var l = 0, r = nums.length - 1;
  for (var w = nums.length - 1; w >= 0; w--) {
    final a = nums[l] * nums[l], b = nums[r] * nums[r];
    if (a > b) {
      out[w] = a;
      l++;
    } else {
      out[w] = b;
      r--;
    }
  }
  return out;
}

void main() {
  print(sortedSquares([-4, -1, 0, 3, 10])); // [0, 1, 9, 16, 100]
}
```

**🔍 What This Code Does:**

1. **Biggest Squares Are at the Ends**: Large negatives and large positives both square to big numbers.
2. **Fill From the Back**: Write the larger square into the last open slot.
3. **O(n)**: No sorting needed after squaring.

---

## 📌 Key Takeaways

- ✅ **Opposite pointers** exploit sorted order: move the pointer that brings you closer to the goal.
- ✅ **Read/write pointers** compact or filter in place with O(1) extra space.
- ✅ **Fixed windows** update in O(1) per step: add the incoming element, remove the outgoing one.
- ✅ **Variable windows** grow on the right and shrink on the left while a condition is violated.
- ✅ Both patterns usually turn **O(n²)** brute force into **O(n)**, because each pointer only moves forward.
- ✅ Windows require **contiguous** ranges; the "shrink" trick needs **non-negative** values.

**Next up:** ➕ **Prefix Sums & Difference Arrays**: answer any range-sum question in O(1).
