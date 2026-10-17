QUESTIONS = [
    mcq(r"""
What is the main benefit of the two-pointer technique?
""", ["It often turns O(n²) pair checks into O(n)", "It sorts the list for free",
       "It uses O(n) extra memory", "It only works on strings"],
        "It often turns O(n²) pair checks into O(n)"),

    mcq(r"""
Opposite-direction two pointers for pair-sum require the list to be:
""", ["Sorted", "Unique", "Even length", "Non-empty and reversed"], "Sorted"),

    mcq(r"""
In sorted pair-sum, the current sum is smaller than the target. What do you do?
""", ["Move the left pointer right", "Move the right pointer left",
       "Move both pointers", "Return null"], "Move the left pointer right"),

    mcq(r"""
In sorted pair-sum, the current sum is larger than the target. What do you do?
""", ["Move the right pointer left", "Move the left pointer right",
       "Restart from the beginning", "Swap the pointers"], "Move the right pointer left"),

    mcq(r"""
What does this print?

```dart
(int, int)? pairSum(List<int> a, int t) {
  var l = 0, r = a.length - 1;
  while (l < r) {
    final s = a[l] + a[r];
    if (s == t) return (l, r);
    if (s < t) {
      l++;
    } else {
      r--;
    }
  }
  return null;
}

void main() {
  print(pairSum([2, 7, 11, 15], 9));
}
```
""", ["(0, 1)", "(1, 2)", "null", "(0, 3)"], "(0, 1)"),

    mcq(r"""
What does this print?

```dart
(int, int)? pairSum(List<int> a, int t) {
  var l = 0, r = a.length - 1;
  while (l < r) {
    final s = a[l] + a[r];
    if (s == t) return (l, r);
    if (s < t) {
      l++;
    } else {
      r--;
    }
  }
  return null;
}

void main() {
  print(pairSum([2, 7, 11, 15], 100));
}
```
""", ["null", "(0, 3)", "(-1, -1)", "It throws an error"], "null"),

    order(r"""
Complete the pair-sum loop:

```dart
while (left %order% right) {
  final sum = nums[left] + nums[right];
  if (sum == target) return (left, right);
  if (sum < target) {
    left%order%;
  } else {
    right%order%;
  }
}
```
""", ["<", "++", "--", "<=", ">", "+= 2"], ["<", "++", "--"]),

    mcq(r"""
What is the time complexity of sorted pair-sum with two pointers?
""", ["O(n)", "O(n²)", "O(n log n)", "O(log n)"], "O(n)"),

    mcq(r"""
In "container with most water", which pointer should move inward?
""", ["The one at the shorter line", "The one at the taller line", "Both, always",
       "Neither; use a nested loop"], "The one at the shorter line"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int maxArea(List<int> h) {
  var l = 0, r = h.length - 1, best = 0;
  while (l < r) {
    best = max(best, (r - l) * min(h[l], h[r]));
    if (h[l] < h[r]) {
      l++;
    } else {
      r--;
    }
  }
  return best;
}

void main() {
  print(maxArea([1, 1]));
  print(maxArea([4, 3, 2, 1, 4]));
}
```
""", ["1 then 16", "1 then 4", "2 then 16", "1 then 12"], "1 then 16"),

    mcq(r"""
What is the time complexity of the sort + two pointers approach to 3Sum?
""", ["O(n²)", "O(n)", "O(n³)", "O(n log n)"], "O(n²)"),

    mcq(r"""
Why does 3Sum sort the array first?
""", ["So two pointers can be used and duplicates are adjacent",
       "Because the output must be sorted", "Sorting makes it O(n)",
       "To remove negative numbers"],
        "So two pointers can be used and duplicates are adjacent"),

    mcq(r"""
In the read/write (fast/slow) pointer pattern, what does the slow pointer usually represent?
""", ["Where the next kept element should be written", "The last element of the list",
       "The middle of the list", "A random index"],
        "Where the next kept element should be written"),

    mcq(r"""
What does this print?

```dart
int dedupe(List<int> a) {
  var slow = 0;
  for (var fast = 1; fast < a.length; fast++) {
    if (a[fast] != a[slow]) a[++slow] = a[fast];
  }
  return slow + 1;
}

void main() {
  final a = [1, 1, 2, 2, 2, 3];
  final k = dedupe(a);
  print(a.sublist(0, k));
}
```
""", ["[1, 2, 3]", "[1, 1, 2]", "[1, 2, 2, 3]", "[3]"], "[1, 2, 3]"),

    mcq(r"""
What does this print?

```dart
bool isSub(String s, String t) {
  var i = 0;
  for (var j = 0; j < t.length && i < s.length; j++) {
    if (s[i] == t[j]) i++;
  }
  return i == s.length;
}

void main() {
  print(isSub('abc', 'ahbgdc'));
  print(isSub('axc', 'ahbgdc'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What does this print?

```dart
List<int> merge(List<int> a, List<int> b) {
  final out = <int>[];
  var i = 0, j = 0;
  while (i < a.length && j < b.length) {
    out.add(a[i] <= b[j] ? a[i++] : b[j++]);
  }
  return out
    ..addAll(a.sublist(i))
    ..addAll(b.sublist(j));
}

void main() {
  print(merge([1, 5, 9], [2, 3, 10]));
}
```
""", ["[1, 2, 3, 5, 9, 10]", "[1, 5, 9, 2, 3, 10]", "[1, 2, 5, 3, 9, 10]", "[10, 9, 5, 3, 2, 1]"],
        "[1, 2, 3, 5, 9, 10]"),

    mcq(r"""
What does `a[i++]` do?
""", ["Reads a[i], then increments i", "Increments i, then reads a[i]",
       "Increments a[i]", "Reads a[i + 1]"], "Reads a[i], then increments i"),

    mcq(r"""
What does `a[++i]` do?
""", ["Increments i, then reads a[i]", "Reads a[i], then increments i",
       "Reads a[i] twice", "Doesn't compile"], "Increments i, then reads a[i]"),

    mcq(r"""
What is the time complexity of merging two sorted lists of sizes n and m?
""", ["O(n + m)", "O(n × m)", "O((n + m) log(n + m))", "O(1)"], "O(n + m)"),

    mcq(r"""
What is a sliding window?
""", ["A contiguous range [left, right] updated incrementally as it moves",
       "Any subset of the array", "A sorted copy of the array", "A pair of random indexes"],
        "A contiguous range [left, right] updated incrementally as it moves"),

    mcq(r"""
When a fixed window of size k slides one step right, how do you update its sum?
""", ["Add the new right element and subtract the element that left",
       "Recompute the whole sum", "Multiply by k", "Subtract the new element"],
        "Add the new right element and subtract the element that left"),

    fill(r"""
Complete the sliding update:

```dart
for (var right = k; right < nums.length; right++) {
  windowSum += nums[right] - nums[right %fill% k];
}
```
""", "-"),

    mcq(r"""
What does this print?

```dart
int maxSum(List<int> a, int k) {
  var sum = 0;
  for (var i = 0; i < k; i++) sum += a[i];
  var best = sum;
  for (var r = k; r < a.length; r++) {
    sum += a[r] - a[r - k];
    if (sum > best) best = sum;
  }
  return best;
}

void main() {
  print(maxSum([1, 4, 2, 10, 2, 3, 1, 0, 20], 4));
}
```
""", ["24", "17", "20", "39"], "24"),

    mcq(r"""
What is the complexity of the brute-force "max sum of every window of size k"?
""", ["O(n × k)", "O(n)", "O(k)", "O(log n)"], "O(n × k)"),

    mcq(r"""
What is the complexity of the sliding-window version?
""", ["O(n)", "O(n × k)", "O(n²)", "O(k²)"], "O(n)"),

    mcq(r"""
What does this print?

```dart
List<double> movingAvg(List<num> v, int k) {
  final out = <double>[];
  num sum = 0;
  for (var i = 0; i < v.length; i++) {
    sum += v[i];
    if (i >= k) sum -= v[i - k];
    if (i >= k - 1) out.add(sum / k);
  }
  return out;
}

void main() {
  print(movingAvg([2, 4, 6, 8], 3));
}
```
""", ["[4.0, 6.0]", "[2.0, 4.0, 6.0]", "[6.0, 8.0]", "[4.0, 6.0, 8.0]"], "[4.0, 6.0]"),

    mcq(r"""
What is the length of the window [left, right] when both ends are inclusive?
""", ["right - left + 1", "right - left", "right + left", "left - right"],
        "right - left + 1"),

    mcq(r"""
What does this print?

```dart
int longestUnique(String s) {
  final last = <String, int>{};
  var left = 0, best = 0;
  for (var right = 0; right < s.length; right++) {
    final prev = last[s[right]];
    if (prev != null && prev >= left) left = prev + 1;
    last[s[right]] = right;
    if (right - left + 1 > best) best = right - left + 1;
  }
  return best;
}

void main() {
  print(longestUnique('abcabcbb'));
  print(longestUnique('dvdf'));
}
```
""", ["3 then 3", "3 then 2", "8 then 4", "2 then 3"], "3 then 3"),

    mcq(r"""
In `longestUnique`, why check `prev >= left`?
""", ["To ignore old positions that are already outside the window",
       "To avoid negative indexes", "To sort the characters", "It isn't needed"],
        "To ignore old positions that are already outside the window"),

    mcq(r"""
What does this print?

```dart
int minLen(int target, List<int> a) {
  var left = 0, sum = 0, best = a.length + 1;
  for (var right = 0; right < a.length; right++) {
    sum += a[right];
    while (sum >= target) {
      if (right - left + 1 < best) best = right - left + 1;
      sum -= a[left++];
    }
  }
  return best > a.length ? 0 : best;
}

void main() {
  print(minLen(11, [1, 2, 3, 4, 5]));
  print(minLen(4, [1, 4, 4]));
}
```
""", ["3 then 1", "5 then 1", "3 then 2", "0 then 1"], "3 then 1"),

    mcq(r"""
Why is the variable window still O(n) despite the inner while loop?
""", ["The left pointer only moves forward, at most n times in total",
       "The while loop runs at most once", "Dart optimizes nested loops",
       "It isn't; it's O(n²)"],
        "The left pointer only moves forward, at most n times in total"),

    mcq(r"""
The "shrink while sum ≥ target" window assumes the numbers are:
""", ["Non-negative", "Sorted", "Unique", "Even"], "Non-negative"),

    mcq(r"""
What should you use instead of a sliding window when the array has negative numbers and you need subarray sums?
""", ["Prefix sums with a hash map", "Binary search", "A stack", "Bubble sort"],
        "Prefix sums with a hash map"),

    fill(r"""
In a variable window, keep shrinking until valid. Which keyword (not `if`)?

```dart
%fill% (counts.length > k) {
  // remove s[left] from the window
  left++;
}
```
""", "while"),

    mcq(r"""
What does this print?

```dart
int longestK(String s, int k) {
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
  print(longestK('aaabbcc', 2));
}
```
""", ["5", "7", "3", "4"], "5"),

    mcq(r"""
In `longestK`, why remove a key when its count reaches 0?
""", ["So counts.length equals the number of distinct characters in the window",
       "To free memory only", "Because Maps can't store 0", "To sort the keys"],
        "So counts.length equals the number of distinct characters in the window"),

    mcq(r"""
Which clue suggests a variable-size sliding window?
""", ["\"Longest/shortest contiguous substring such that...\"",
       "\"Find any subset with sum k\"", "\"Sort the array\"", "\"Find the median\""],
        "\"Longest/shortest contiguous substring such that...\""),

    mcq(r"""
Which clue suggests opposite-direction pointers?
""", ["A sorted array and a pair that must meet a sum", "Counting word frequencies",
       "Shortest path in a graph", "Removing the first element repeatedly"],
        "A sorted array and a pair that must meet a sum"),

    mcq(r"""
For an UNSORTED array, what's the O(n) way to find a pair with a given sum?
""", ["Use a hash set of seen values", "Opposite two pointers directly",
       "A sliding window", "Nested loops"], "Use a hash set of seen values"),

    mcq(r"""
What does this print?

```dart
List<int> sortedSquares(List<int> a) {
  final out = List<int>.filled(a.length, 0);
  var l = 0, r = a.length - 1;
  for (var w = a.length - 1; w >= 0; w--) {
    final x = a[l] * a[l], y = a[r] * a[r];
    if (x > y) {
      out[w] = x;
      l++;
    } else {
      out[w] = y;
      r--;
    }
  }
  return out;
}

void main() {
  print(sortedSquares([-3, -2, 1, 4]));
}
```
""", ["[1, 4, 9, 16]", "[9, 4, 1, 16]", "[16, 9, 4, 1]", "[1, 9, 4, 16]"], "[1, 4, 9, 16]"),

    mcq(r"""
Why does `sortedSquares` fill the output from the back?
""", ["The largest squares come from the two ends of the input",
       "Lists can only be filled backwards", "To reverse the input",
       "To avoid a RangeError"], "The largest squares come from the two ends of the input"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = 'racecar';
  var l = 0, r = s.length - 1, ok = true;
  while (l < r) {
    if (s[l++] != s[r--]) {
      ok = false;
      break;
    }
  }
  print(ok);
}
```
""", ["true", "false", "racecar", "It throws an error"], "true"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, 0, 1, 0, 2];
  var w = 0;
  for (final x in a) {
    if (x != 0) a[w++] = x;
  }
  print(w);
}
```
""", ["3", "5", "2", "0"], "3"),

    mcq(r"""
Sliding windows apply to which kind of range?
""", ["Contiguous subarrays or substrings", "Any subset of elements",
       "Only the first and last elements", "Only sorted subsequences"],
        "Contiguous subarrays or substrings"),

    order(r"""
Complete the fixed-window setup:

```dart
int firstWindow(List<int> nums, int k) {
  var sum = 0;
  %order% (var i = 0; i %order% k; i%order%) {
    sum += nums[i];
  }
  return sum;
}
```
""", ["for", "<", "++", "while", "<=", "--"], ["for", "<", "++"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [5, 1, 3];
  var sum = 0;
  for (var i = 0; i < 2; i++) sum += nums[i];
  sum += nums[2] - nums[0];
  print(sum);
}
```
""", ["4", "6", "9", "8"], "4"),

    mcq(r"""
What happens if you use `if` instead of `while` to shrink a variable window?
""", ["The window may stay invalid when one shrink step isn't enough",
       "It becomes O(n²)", "It throws an error", "Nothing changes"],
        "The window may stay invalid when one shrink step isn't enough"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(-1 << 3);
}
```
""", ["-8", "8", "-4", "0"], "-8"),

    mcq(r"""
Each element in a sliding window algorithm typically:
""", ["Enters the window once and leaves it at most once", "Is visited k times",
       "Is visited n times", "Is sorted into place"],
        "Enters the window once and leaves it at most once"),

    mcq(r"""
Which pattern is used inside merge sort's merge step?
""", ["Two pointers, one per sorted half", "Sliding window", "Hash map counting",
       "Binary search"], "Two pointers, one per sorted half"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3, 4, 5, 6];
  var l = 0, r = a.length - 1;
  while (l < r) {
    final t = a[l];
    a[l++] = a[r];
    a[r--] = t;
  }
  print(a);
}
```
""", ["[6, 5, 4, 3, 2, 1]", "[1, 2, 3, 4, 5, 6]", "[6, 2, 4, 3, 5, 1]", "[2, 1, 4, 3, 6, 5]"],
        "[6, 5, 4, 3, 2, 1]"),

    mcq(r"""
How many anchor iterations does 3Sum's outer loop run for n elements, roughly?
""", ["n", "n²", "log n", "1"], "n"),

    mcq(r"""
To find ALL start indexes where an anagram of `p` occurs in `s`, which pattern fits best?
""", ["Fixed window of size p.length with character counts", "Opposite pointers on sorted s",
       "Binary search", "Recursion with backtracking"],
        "Fixed window of size p.length with character counts"),

    mcq(r"""
What is the extra space used by opposite two pointers on a list?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = 'aab';
  var best = 0, left = 0;
  final seen = <String>{};
  for (var right = 0; right < s.length; right++) {
    while (seen.contains(s[right])) {
      seen.remove(s[left++]);
    }
    seen.add(s[right]);
    if (right - left + 1 > best) best = right - left + 1;
  }
  print(best);
}
```
""", ["2", "3", "1", "0"], "2"),
]
