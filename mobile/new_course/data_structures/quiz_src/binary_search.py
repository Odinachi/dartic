BS = r"""int bs(List<int> a, int t) {
  var lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == t) return mid;
    if (a[mid] < t) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}
"""

LB = r"""int lowerBound(List<int> a, int x) {
  var lo = 0, hi = a.length;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] < x) {
      lo = mid + 1;
    } else {
      hi = mid;
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
"""

QUESTIONS = [
    mcq(r"""
What must be true about data before using binary search?
""", ["It must be sorted (or the condition must be monotonic)", "It must have no duplicates",
       "It must have an even length", "It must be stored in a Set"],
        "It must be sorted (or the condition must be monotonic)"),

    mcq(r"""
What is the time complexity of binary search?
""", ["O(log n)", "O(n)", "O(1)", "O(n log n)"], "O(log n)"),

    mcq(r"""
About how many steps does binary search need for 1,000,000 sorted items?
""", ["About 20", "About 1,000", "About 100", "About 500,000"], "About 20"),

    mcq(r"""
About how many steps for 8 billion sorted items?
""", ["About 33", "About 8,000", "About 1,000,000", "About 100"], "About 33"),

    mcq(r"""
What does this print?

```dart
""" + BS + r"""
void main() {
  final a = [3, 8, 12, 20, 31, 47];
  print(bs(a, 31));
  print(bs(a, 4));
}
```
""", ["4 then -1", "5 then -1", "4 then 0", "3 then -1"], "4 then -1"),

    mcq(r"""
Why compute the middle as `lo + (hi - lo) ~/ 2`?
""", ["It avoids overflow when lo + hi would be too large in fixed-size integers",
       "It's faster than (lo + hi) ~/ 2 in Dart", "It rounds up", "It works on unsorted lists"],
        "It avoids overflow when lo + hi would be too large in fixed-size integers"),

    mcq(r"""
What goes wrong with `final mid = (lo + hi) / 2;` in Dart?
""", ["/ returns a double, which can't be used as a list index", "It overflows",
       "It always returns 0", "Nothing"],
        "/ returns a double, which can't be used as a list index"),

    order(r"""
Complete the classic binary search:

```dart
while (lo %order% hi) {
  final mid = lo + (hi - lo) %order% 2;
  if (a[mid] == t) return mid;
  if (a[mid] < t) {
    lo = mid %order% 1;
  } else {
    hi = mid - 1;
  }
}
```
""", ["<=", "~/", "+", "<", "/", "-"], ["<=", "~/", "+"]),

    mcq(r"""
In the classic `while (lo <= hi)` version, why use `lo = mid + 1` instead of `lo = mid`?
""", ["mid was already checked, and `lo = mid` can loop forever", "To skip duplicates",
       "To make it O(1)", "It doesn't matter"],
        "mid was already checked, and `lo = mid` can loop forever"),

    mcq(r"""
Searching for 23 in `[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]`, which middle values are checked?
""", ["16, 56, 23", "16, 23", "12, 23", "56, 16, 23"], "16, 56, 23"),

    mcq(r"""
With duplicates, which index does the classic binary search return?
""", ["Some matching index, not necessarily the first", "Always the first",
       "Always the last", "-1"], "Some matching index, not necessarily the first"),

    mcq(r"""
How do you modify binary search to find the FIRST occurrence?
""", ["On a match, record it and continue searching left (hi = mid - 1)",
       "On a match, return immediately", "Search from the right end", "Sort descending first"],
        "On a match, record it and continue searching left (hi = mid - 1)"),

    mcq(r"""
What does this print?

```dart
int first(List<int> a, int t) {
  var lo = 0, hi = a.length - 1, ans = -1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == t) {
      ans = mid;
      hi = mid - 1;
    } else if (a[mid] < t) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return ans;
}

void main() {
  print(first([1, 2, 2, 2, 3, 4], 2));
}
```
""", ["1", "2", "3", "-1"], "1"),

    mcq(r"""
What does this print?

```dart
int last(List<int> a, int t) {
  var lo = 0, hi = a.length - 1, ans = -1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == t) {
      ans = mid;
      lo = mid + 1;
    } else if (a[mid] < t) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return ans;
}

void main() {
  print(last([1, 2, 2, 2, 3, 4], 2));
}
```
""", ["3", "1", "2", "4"], "3"),

    mcq(r"""
How can you count occurrences of x in a sorted list in O(log n)?
""", ["lastIndex(x) − firstIndex(x) + 1", "Scan the list", "Use contains",
       "Divide the length by 2"], "lastIndex(x) − firstIndex(x) + 1"),

    mcq(r"""
What does lowerBound(x) return?
""", ["The first index with value ≥ x", "The first index with value > x",
       "The last index with value ≤ x", "-1 if x is missing"],
        "The first index with value ≥ x"),

    mcq(r"""
What does upperBound(x) return?
""", ["The first index with value > x", "The first index with value ≥ x",
       "The last index of x", "The length minus 1"], "The first index with value > x"),

    mcq(r"""
What does this print?

```dart
""" + LB + r"""
void main() {
  final a = [1, 3, 3, 3, 7, 9];
  print(lowerBound(a, 3));
  print(upperBound(a, 3));
}
```
""", ["1 then 4", "1 then 3", "0 then 4", "3 then 4"], "1 then 4"),

    mcq(r"""
What does this print?

```dart
""" + LB + r"""
void main() {
  final a = [1, 3, 3, 3, 7, 9];
  print(lowerBound(a, 5));
  print(lowerBound(a, 100));
}
```
""", ["4 then 6", "-1 then -1", "3 then 5", "4 then 5"], "4 then 6"),

    mcq(r"""
What does this print?

```dart
""" + LB + r"""
void main() {
  final a = [2, 4, 4, 6, 8, 10];
  print(upperBound(a, 8) - lowerBound(a, 4));
}
```
""", ["4", "3", "5", "6"], "4"),

    mcq(r"""
Why does lowerBound use `hi = mid` instead of `hi = mid - 1`?
""", ["mid might be the answer, so it must stay in the range", "To avoid negative indexes",
       "To make it faster", "It's a bug"], "mid might be the answer, so it must stay in the range"),

    mcq(r"""
Why does lowerBound start with `hi = a.length` rather than `a.length - 1`?
""", ["The answer can be \"past the end\" when x is larger than every element",
       "To include an extra sentinel element", "Dart lists start at 1",
       "To avoid the loop running"],
        "The answer can be \"past the end\" when x is larger than every element"),

    mcq(r"""
What does this print?

```dart
""" + LB + r"""
void main() {
  final sorted = <int>[];
  for (final x in [4, 1, 3, 1]) {
    sorted.insert(lowerBound(sorted, x), x);
  }
  print(sorted);
}
```
""", ["[1, 1, 3, 4]", "[4, 1, 3, 1]", "[1, 3, 4]", "[4, 3, 1, 1]"], "[1, 1, 3, 4]"),

    mcq(r"""
Inserting into a sorted List using lowerBound costs what overall per insert?
""", ["O(n): O(log n) to find the spot, O(n) to shift", "O(log n)", "O(1)", "O(n log n)"],
        "O(n): O(log n) to find the spot, O(n) to shift"),

    mcq(r"""
What is the "universal" binary search pattern?
""", ["Find the first value where a monotonic condition becomes true",
       "Find the middle element", "Find the largest element", "Find any element"],
        "Find the first value where a monotonic condition becomes true"),

    mcq(r"""
What does "monotonic" mean for a binary search condition?
""", ["It goes false…false then true…true (never switches back)", "It's always true",
       "It alternates true and false", "It depends on random input"],
        "It goes false…false then true…true (never switches back)"),

    mcq(r"""
What does this print?

```dart
int firstTrue(int lo, int hi, bool Function(int) test) {
  var ans = hi + 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (test(mid)) {
      ans = mid;
      hi = mid - 1;
    } else {
      lo = mid + 1;
    }
  }
  return ans;
}

void main() {
  print(firstTrue(1, 100, (v) => v >= 42));
  print(firstTrue(0, 50, (x) => x * x > 50) - 1);
}
```
""", ["42 then 7", "41 then 7", "42 then 8", "43 then 7"], "42 then 7"),

    mcq(r"""
What is "binary search on the answer"?
""", ["Binary searching a range of candidate answers using a feasibility check",
       "Searching a list for the answer key", "Sorting answers first",
       "Guessing answers randomly"],
        "Binary searching a range of candidate answers using a feasibility check"),

    mcq(r"""
Why can "minimum ship capacity within D days" be solved by binary search?
""", ["If a capacity works, every larger capacity also works (monotonic)",
       "Weights are sorted", "Capacities are small", "Days are sorted"],
        "If a capacity works, every larger capacity also works (monotonic)"),

    mcq(r"""
In the shipping problem, what are the lowest and highest possible capacities?
""", ["The heaviest package and the total weight", "0 and the number of packages",
       "1 and the number of days", "The lightest package and the heaviest"],
        "The heaviest package and the total weight"),

    mcq(r"""
What does this print?

```dart
bool canShip(List<int> w, int cap, int days) {
  var used = 1, load = 0;
  for (final x in w) {
    if (load + x > cap) {
      used++;
      load = 0;
    }
    load += x;
  }
  return used <= days;
}

void main() {
  print(canShip([3, 2, 2, 4, 1, 4], 6, 3));
  print(canShip([3, 2, 2, 4, 1, 4], 5, 3));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What is the complexity of binary search on the answer with an O(n) feasibility check over a range of size R?
""", ["O(n log R)", "O(R)", "O(n × R)", "O(log n)"], "O(n log R)"),

    mcq(r"""
Which problem is a classic "binary search on the answer" problem?
""", ["Minimum eating speed to finish all banana piles in h hours", "Reversing a list",
       "Counting vowels", "Merging two lists"],
        "Minimum eating speed to finish all banana piles in h hours"),

    mcq(r"""
In a rotated sorted array like `[15, 18, 2, 3, 6, 12]`, what's always true at each step?
""", ["At least one half (left or right of mid) is sorted", "Both halves are sorted",
       "The middle is the minimum", "The array is fully sorted"],
        "At least one half (left or right of mid) is sorted"),

    mcq(r"""
What does this print?

```dart
int searchRotated(List<int> a, int t) {
  var lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] == t) return mid;
    if (a[lo] <= a[mid]) {
      if (a[lo] <= t && t < a[mid]) {
        hi = mid - 1;
      } else {
        lo = mid + 1;
      }
    } else {
      if (a[mid] < t && t <= a[hi]) {
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
  }
  return -1;
}

void main() {
  print(searchRotated([4, 5, 6, 7, 0, 1, 2], 0));
  print(searchRotated([4, 5, 6, 7, 0, 1, 2], 3));
}
```
""", ["4 then -1", "0 then -1", "4 then 3", "3 then -1"], "4 then -1"),

    mcq(r"""
What does this print?

```dart
int findMin(List<int> a) {
  var lo = 0, hi = a.length - 1;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] > a[hi]) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return a[lo];
}

void main() {
  print(findMin([30, 40, 50, 10, 20]));
}
```
""", ["10", "30", "20", "50"], "10"),

    mcq(r"""
Which pairing of loop condition and updates is consistent?
""", ["while (lo < hi) with lo = mid + 1 and hi = mid", "while (lo < hi) with lo = mid and hi = mid",
       "while (lo <= hi) with lo = mid and hi = mid", "while (lo != hi) with lo = mid"],
        "while (lo < hi) with lo = mid + 1 and hi = mid"),

    mcq(r"""
What happens if binary search runs on unsorted data?
""", ["It can silently return wrong answers", "It throws an exception", "It sorts the data first",
       "It becomes O(n)"], "It can silently return wrong answers"),

    mcq(r"""
Which edge cases should every binary search be tested with?
""", ["Empty list, one element, target below all, target above all",
       "Only lists with 100 elements", "Only negative numbers", "Only even lengths"],
        "Empty list, one element, target below all, target above all"),

    mcq(r"""
What does this print?

```dart
""" + BS + r"""
void main() {
  print(bs([], 5));
  print(bs([5], 5));
}
```
""", ["-1 then 0", "0 then 0", "-1 then -1", "It throws an error"], "-1 then 0"),

    mcq(r"""
Which Dart package provides a ready-made `lowerBound` for lists?
""", ["package:collection", "dart:core", "dart:math", "dart:async"], "package:collection"),

    mcq(r"""
Which SplayTreeMap method answers "smallest key strictly greater than k" in O(log n)?
""", ["firstKeyAfter", "lastKeyBefore", "containsKey", "keys.where"], "firstKeyAfter"),

    mcq(r"""
Why isn't `set.where((x) => x >= k).first` a binary search on a SplayTreeSet?
""", ["where scans elements one by one (O(n)) and ignores the tree's order",
       "where doesn't exist on sets", "It sorts first", "It is a binary search"],
        "where scans elements one by one (O(n)) and ignores the tree's order"),

    mcq(r"""
What does this print?

```dart
int isqrt(int n) {
  var lo = 0, hi = n, ans = 0;
  while (lo <= hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (mid * mid <= n) {
      ans = mid;
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return ans;
}

void main() {
  print(isqrt(26));
  print(isqrt(49));
}
```
""", ["5 then 7", "6 then 7", "5 then 6", "26 then 49"], "5 then 7"),

    mcq(r"""
What is a "peak element"?
""", ["An element larger than its neighbors", "The largest element in the array",
       "The first element", "An element equal to its neighbors"],
        "An element larger than its neighbors"),

    mcq(r"""
How can binary search find a peak?
""", ["If a[mid] < a[mid + 1], a peak exists to the right; otherwise at mid or to the left",
       "Sort the array and take the last element", "Scan from both ends", "It can't"],
        "If a[mid] < a[mid + 1], a peak exists to the right; otherwise at mid or to the left"),

    mcq(r"""
What does this print?

```dart
int peak(List<int> a) {
  var lo = 0, hi = a.length - 1;
  while (lo < hi) {
    final mid = lo + (hi - lo) ~/ 2;
    if (a[mid] < a[mid + 1]) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return lo;
}

void main() {
  print(peak([1, 3, 7, 4, 2]));
}
```
""", ["2", "3", "0", "4"], "2"),

    mcq(r"""
What does "search insert position" return for target 5 in `[1, 3, 5, 6]` and target 2?
""", ["2 and 1", "2 and 2", "3 and 1", "-1 and 1"], "2 and 1"),

    fill(r"""
Use integer division for the middle index:

```dart
void main() {
  final lo = 3, hi = 8;
  final mid = lo + (hi - lo) %fill% 2;
  print(mid); // 5
}
```
""", "~/"),

    mcq(r"""
Binary search on a range of integers 1 to 10⁹ takes about how many steps?
""", ["About 30", "About 1,000", "About 10⁹", "About 9"], "About 30"),

    mcq(r"""
Which statement about linear vs binary search is true?
""", ["Linear works on unsorted data in O(n); binary needs sorted data but runs in O(log n)",
       "Binary search works on any data", "Linear search is always slower",
       "They have the same complexity"],
        "Linear works on unsorted data in O(n); binary needs sorted data but runs in O(log n)"),

    mcq(r"""
If you search a sorted list many times, is sorting first worth it?
""", ["Yes: one O(n log n) sort, then each search is O(log n)",
       "No, sorting is always too slow", "Only if the list is small", "Only for strings"],
        "Yes: one O(n log n) sort, then each search is O(log n)"),

    mcq(r"""
What does this print?

```dart
""" + LB + r"""
void main() {
  final scores = [55, 60, 72, 80, 91];
  print(scores.length - lowerBound(scores, 70));
}
```
""", ["3", "2", "4", "70"], "3"),

    mcq(r"""
For a sorted list `scores`, what does `scores.length - lowerBound(scores, 70)` count?
""", ["How many scores are ≥ 70", "How many scores are < 70", "The index of 70",
       "The number of 70s"], "How many scores are ≥ 70"),
]
