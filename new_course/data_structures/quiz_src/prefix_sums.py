QUESTIONS = [
    mcq(r"""
What does `prefix[k]` store in a prefix sum array with a leading 0?
""", ["The sum of the first k elements", "The k-th element", "The sum of the last k elements",
       "The maximum of the first k elements"], "The sum of the first k elements"),

    mcq(r"""
With `prefix` of length n + 1 and `prefix[0] = 0`, what is the sum of `nums[a..b]` (inclusive)?
""", ["prefix[b + 1] - prefix[a]", "prefix[b] - prefix[a]", "prefix[b] - prefix[a - 1]",
       "prefix[a] + prefix[b]"], "prefix[b + 1] - prefix[a]"),

    mcq(r"""
What is the cost of answering one range-sum query after building a prefix sum?
""", ["O(1)", "O(n)", "O(log n)", "O(b - a)"], "O(1)"),

    mcq(r"""
What is the cost of building a prefix sum array?
""", ["O(n)", "O(1)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
For n elements and q range-sum queries, what is the total cost with prefix sums?
""", ["O(n + q)", "O(n × q)", "O(q log n)", "O(n²)"], "O(n + q)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [2, 4, 6, 8];
  final prefix = List<int>.filled(nums.length + 1, 0);
  for (var i = 0; i < nums.length; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
  }
  print(prefix);
}
```
""", ["[0, 2, 6, 12, 20]", "[2, 6, 12, 20]", "[0, 2, 4, 6, 8]", "[2, 4, 6, 8, 20]"],
        "[0, 2, 6, 12, 20]"),

    fill(r"""
Complete the prefix build:

```dart
List<int> build(List<int> nums) {
  final p = List<int>.filled(nums.length + 1, 0);
  for (var i = 0; i < nums.length; i++) {
    p[i + 1] = p[%fill%] + nums[i];
  }
  return p;
}
```
""", "i"),

    mcq(r"""
Given `prefix = [0, 2, 6, 12, 20]` for `nums = [2, 4, 6, 8]`, what is `prefix[4] - prefix[1]`?
""", ["18", "20", "14", "12"], "18"),

    mcq(r"""
Which elements does `prefix[4] - prefix[1]` add up?
""", ["nums[1], nums[2], nums[3]", "nums[1] to nums[4]", "nums[0] to nums[3]",
       "Only nums[1] and nums[4]"], "nums[1], nums[2], nums[3]"),

    mcq(r"""
Why add a leading 0 to the prefix array?
""", ["So ranges starting at index 0 need no special case", "To make the array sorted",
       "Because Dart lists start at 1", "To handle negative numbers"],
        "So ranges starting at index 0 need no special case"),

    mcq(r"""
When are prefix sums a poor choice?
""", ["When the data changes frequently between queries", "When there are many queries",
       "When the data contains negative numbers", "When the array is large"],
        "When the data changes frequently between queries"),

    mcq(r"""
Which structure handles range sums with frequent point updates in O(log n)?
""", ["Fenwick tree or segment tree", "A Set", "A Queue", "A StringBuffer"],
        "Fenwick tree or segment tree"),

    mcq(r"""
Why can't a sliding window count subarrays summing to k when numbers can be negative?
""", ["Adding an element might decrease the sum, so shrinking/growing logic breaks",
       "Negative numbers can't be summed", "Windows only work on strings",
       "It can; there's no problem"],
        "Adding an element might decrease the sum, so shrinking/growing logic breaks"),

    mcq(r"""
What does this print?

```dart
int subarraySum(List<int> nums, int k) {
  final seen = <int, int>{0: 1};
  var running = 0, count = 0;
  for (final x in nums) {
    running += x;
    count += seen[running - k] ?? 0;
    seen[running] = (seen[running] ?? 0) + 1;
  }
  return count;
}

void main() {
  print(subarraySum([1, 1, 1], 2));
}
```
""", ["2", "1", "3", "0"], "2"),

    mcq(r"""
What does this print?

```dart
int subarraySum(List<int> nums, int k) {
  final seen = <int, int>{0: 1};
  var running = 0, count = 0;
  for (final x in nums) {
    running += x;
    count += seen[running - k] ?? 0;
    seen[running] = (seen[running] ?? 0) + 1;
  }
  return count;
}

void main() {
  print(subarraySum([1, -1, 0], 0));
}
```
""", ["3", "1", "2", "0"], "3"),

    mcq(r"""
Why is the map seeded with `{0: 1}`?
""", ["To count subarrays that start at index 0", "To avoid a null error only",
       "Because Maps can't be empty", "To make the result one larger"],
        "To count subarrays that start at index 0"),

    mcq(r"""
In `subarraySum`, why do we update `count` BEFORE recording the current prefix?
""", ["So we never count an empty subarray when k == 0", "Because Maps are ordered",
       "To make it O(1)", "The order doesn't matter at all"],
        "So we never count an empty subarray when k == 0"),

    fill(r"""
Look up how many earlier prefixes complete a subarray summing to k:

```dart
count += seen[running %fill% k] ?? 0;
```
""", "-"),

    mcq(r"""
What is the time complexity of the prefix-sum + hash map subarray count?
""", ["O(n)", "O(n²)", "O(n log n)", "O(k)"], "O(n)"),

    mcq(r"""
If the running prefix sum has the same value at indexes i and j (i < j), what's true?
""", ["The elements after i up to j sum to 0", "nums[i] == nums[j]",
       "The array is sorted", "There are no negative numbers"],
        "The elements after i up to j sum to 0"),

    mcq(r"""
For "longest subarray with sum 0", which index do you store for each prefix value?
""", ["The FIRST index where it appeared", "The LAST index where it appeared",
       "Every index in a list", "Only index 0"], "The FIRST index where it appeared"),

    mcq(r"""
What does this print?

```dart
int longestZero(List<int> nums) {
  final first = <int, int>{0: -1};
  var run = 0, best = 0;
  for (var i = 0; i < nums.length; i++) {
    run += nums[i];
    final f = first[run];
    if (f != null) {
      if (i - f > best) best = i - f;
    } else {
      first[run] = i;
    }
  }
  return best;
}

void main() {
  print(longestZero([1, 2, -3, 3]));
}
```
""", ["3", "4", "2", "0"], "3"),

    mcq(r"""
In a 2D prefix sum `p`, what does `p[r][c]` represent (with a leading row/column of zeros)?
""", ["The sum of the rectangle from (0,0) to (r-1, c-1)", "The value at grid[r][c]",
       "The sum of row r", "The sum of column c"],
        "The sum of the rectangle from (0,0) to (r-1, c-1)"),

    mcq(r"""
Which principle does the 2D rectangle query formula use?
""", ["Inclusion–exclusion", "Divide and conquer", "Greedy choice", "Backtracking"],
        "Inclusion–exclusion"),

    order(r"""
Complete the 2D rectangle query:

```dart
int rect(List<List<int>> p, int r1, int c1, int r2, int c2) =>
    p[r2 + 1][c2 + 1] %order% p[r1][c2 + 1] - p[r2 + 1][c1] %order% p[r1][c1];
```
""", ["-", "+", "*", "~/"], ["-", "+"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final grid = [
    [1, 2],
    [3, 4],
  ];
  final p = List.generate(3, (_) => List.filled(3, 0));
  for (var r = 0; r < 2; r++) {
    for (var c = 0; c < 2; c++) {
      p[r + 1][c + 1] = grid[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
    }
  }
  print(p[2][2]);
}
```
""", ["10", "4", "7", "3"], "10"),

    mcq(r"""
In the 2D build formula, why is `p[r][c]` subtracted?
""", ["The top-left area was added twice (once from above, once from the left)",
       "To make the result negative", "Because the grid is 0-indexed",
       "To remove the current cell"],
        "The top-left area was added twice (once from above, once from the left)"),

    mcq(r"""
What is a difference array used for?
""", ["Applying many range updates efficiently", "Finding the difference between two arrays",
       "Sorting arrays", "Removing duplicates"], "Applying many range updates efficiently"),

    mcq(r"""
To add `v` to every index in `[start, end]` with a difference array, you do:
""", ["diff[start] += v; diff[end + 1] -= v;", "diff[start] += v; diff[end] -= v;",
       "Loop from start to end adding v", "diff[end] += v; diff[start] -= v;"],
        "diff[start] += v; diff[end + 1] -= v;"),

    mcq(r"""
How do you get the final values from a difference array?
""", ["Take its prefix sum", "Sort it", "Reverse it", "Take its maximum"],
        "Take its prefix sum"),

    mcq(r"""
What does this print?

```dart
void main() {
  const n = 5;
  final diff = List<int>.filled(n + 1, 0);
  void add(int s, int e, int v) {
    diff[s] += v;
    diff[e + 1] -= v;
  }

  add(0, 2, 3);
  add(1, 4, 2);
  final out = <int>[];
  var run = 0;
  for (var i = 0; i < n; i++) {
    run += diff[i];
    out.add(run);
  }
  print(out);
}
```
""", ["[3, 5, 5, 2, 2]", "[3, 3, 3, 2, 2]", "[3, 5, 5, 5, 2]", "[5, 5, 5, 2, 2]"],
        "[3, 5, 5, 2, 2]"),

    mcq(r"""
Why does the difference array have length n + 1?
""", ["So `end + 1` is a valid index even when end is the last element",
       "To store the total sum", "Because Dart requires it", "To store a sentinel -1"],
        "So `end + 1` is a valid index even when end is the last element"),

    mcq(r"""
What is the cost of u range updates followed by one final read using a difference array of size n?
""", ["O(n + u)", "O(n × u)", "O(u log n)", "O(n²)"], "O(n + u)"),

    mcq(r"""
Prefix sums and difference arrays are:
""", ["Inverses of each other", "Exactly the same thing", "Only for 2D grids",
       "Only for strings"], "Inverses of each other"),

    mcq(r"""
In car pooling, passengers ride on `[from, to)` (they leave at `to`). Where do you subtract?
""", ["diff[to]", "diff[to + 1]", "diff[from]", "diff[from - 1]"], "diff[to]"),

    fill(r"""
Destructure a record in a for loop:

```dart
void main() {
  final trips = [(2, 1, 5), (3, 3, 7)];
  for (final (people, from, to) %fill% trips) {
    print('$people from $from to $to');
  }
}
```
""", "in"),

    mcq(r"""
What does `_` mean in the pattern `(_, _, to)`?
""", ["A wildcard that ignores that field", "A variable named underscore",
       "A private field", "A null value"], "A wildcard that ignores that field"),

    mcq(r"""
What does this print?

```dart
List<int> productExceptSelf(List<int> nums) {
  final out = List<int>.filled(nums.length, 1);
  var left = 1;
  for (var i = 0; i < nums.length; i++) {
    out[i] = left;
    left *= nums[i];
  }
  var right = 1;
  for (var i = nums.length - 1; i >= 0; i--) {
    out[i] *= right;
    right *= nums[i];
  }
  return out;
}

void main() {
  print(productExceptSelf([2, 3, 4]));
}
```
""", ["[12, 8, 6]", "[24, 24, 24]", "[2, 6, 24]", "[6, 8, 12]"], "[12, 8, 6]"),

    mcq(r"""
Why does `productExceptSelf` avoid division?
""", ["Division breaks when the array contains a zero", "Dart has no division operator",
       "Division is O(n)", "It makes the output sorted"],
        "Division breaks when the array contains a zero"),

    mcq(r"""
What does this print?

```dart
void main() {
  final t = [3, 1, 4, 1, 5];
  final best = <int>[];
  var cur = t.first;
  for (final x in t) {
    if (x > cur) cur = x;
    best.add(cur);
  }
  print(best);
}
```
""", ["[3, 3, 4, 4, 5]", "[3, 1, 4, 1, 5]", "[5, 5, 5, 5, 5]", "[1, 1, 1, 1, 5]"],
        "[3, 3, 4, 4, 5]"),

    mcq(r"""
Why can't a prefix MAX answer "max of range [a, b]" by subtraction like sums can?
""", ["Max has no inverse operation like subtraction", "Max is O(n²)",
       "Prefix max only works on sorted data", "It can; use prefixMax[b] - prefixMax[a]"],
        "Max has no inverse operation like subtraction"),

    mcq(r"""
What does this print?

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
  print(pivotIndex([2, 1, -1]));
  print(pivotIndex([1, 2, 3]));
}
```
""", ["0 then -1", "1 then -1", "0 then 1", "-1 then -1"], "0 then -1"),

    fill(r"""
Sum a list with an initial value:

```dart
void main() {
  final total = [1, 2, 3].%fill%(0, (a, b) => a + b);
  print(total); // 6
}
```
""", "fold"),

    mcq(r"""
What does this print?

```dart
void main() {
  final prefix = [0, 5, 6, 10];
  print(prefix[2] - prefix[1]);
}
```
""", ["1", "5", "6", "4"], "1"),

    mcq(r"""
For `nums = [5, 1, 4]` and `prefix = [0, 5, 6, 10]`, which expression gives `1 + 4`?
""", ["prefix[3] - prefix[1]", "prefix[2] - prefix[1]", "prefix[3] - prefix[2]",
       "prefix[2] - prefix[0]"], "prefix[3] - prefix[1]"),

    mcq(r"""
Counting subarrays divisible by k uses prefix sums with a map keyed by:
""", ["running % k (normalized to be non-negative)", "running / k", "running * k",
       "The index of each element"], "running % k (normalized to be non-negative)"),

    mcq(r"""
What does this print in Dart?

```dart
void main() {
  print(-7 % 3);
}
```
""", ["2", "-1", "1", "-2"], "2"),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [3, 1, 2];
  var running = 0;
  final p = <int>[];
  for (final x in nums) {
    running += x;
    p.add(running);
  }
  print(p);
}
```
""", ["[3, 4, 6]", "[0, 3, 4, 6]", "[3, 1, 2]", "[6, 3, 2]"], "[3, 4, 6]"),

    mcq(r"""
What is the space overhead of a prefix sum array for n elements?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
Which real-world feature is a natural fit for prefix sums?
""", ["\"Total steps between day a and day b\" in a fitness app",
       "Undo history in a text editor", "Finding the shortest road route",
       "Autocompleting a search box"],
        "\"Total steps between day a and day b\" in a fitness app"),

    mcq(r"""
Which real-world feature is a natural fit for a difference array?
""", ["Applying many \"add X seats to range\" bookings, then reading every seat",
       "Checking if a username exists", "Serving print jobs in order",
       "Sorting a leaderboard"],
        "Applying many \"add X seats to range\" bookings, then reading every seat"),

    mcq(r"""
What does this print?

```dart
class NumArray {
  final List<int> _p;
  NumArray(List<int> nums) : _p = List.filled(nums.length + 1, 0) {
    for (var i = 0; i < nums.length; i++) {
      _p[i + 1] = _p[i] + nums[i];
    }
  }
  int sumRange(int a, int b) => _p[b + 1] - _p[a];
}

void main() {
  final arr = NumArray([-2, 0, 3, -5, 2, -1]);
  print(arr.sumRange(0, 2));
  print(arr.sumRange(2, 5));
}
```
""", ["1 then -1", "1 then 1", "-2 then -1", "3 then -1"], "1 then -1"),

    mcq(r"""
What is the `: _p = List.filled(...)` part of this constructor called?

```dart
class NumArray {
  final List<int> _p;
  NumArray(List<int> nums) : _p = List.filled(nums.length + 1, 0);
}
```
""", ["An initializer list", "A factory", "A mixin", "A getter"], "An initializer list"),

    mcq(r"""
On Dart web, what can go wrong with very large running totals?
""", ["Integers lose precision above 2^53 because they're JavaScript doubles",
       "They throw a StackOverflowError", "They wrap around to negative at 2^31",
       "Nothing; web ints are unlimited"],
        "Integers lose precision above 2^53 because they're JavaScript doubles"),

    mcq(r"""
What does this print?

```dart
void main() {
  final diff = [0, 0, 0, 0, 0];
  diff[1] += 4;
  diff[3] -= 4;
  var run = 0;
  final out = <int>[];
  for (var i = 0; i < 4; i++) {
    run += diff[i];
    out.add(run);
  }
  print(out);
}
```
""", ["[0, 4, 4, 0]", "[0, 4, 4, 4]", "[4, 4, 0, 0]", "[0, 4, 0, -4]"], "[0, 4, 4, 0]"),

    mcq(r"""
Which pair of operations is O(1) with a 2D prefix sum?
""", ["Querying any rectangle's sum", "Updating a single cell",
       "Inserting a new row", "Sorting each row"], "Querying any rectangle's sum"),

    mcq(r"""
Building a 2D prefix sum for an r × c grid costs:
""", ["O(r × c)", "O(r + c)", "O(1)", "O((r × c)²)"], "O(r × c)"),
]
