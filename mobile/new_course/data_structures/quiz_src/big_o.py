QUESTIONS = [
    mcq(r"""
What does Big O notation describe?
""", [
        "How work or memory grows as the input size grows",
        "The exact running time in milliseconds",
        "The number of lines of code",
        "How many bugs a function has",
    ], "How work or memory grows as the input size grows"),

    mcq(r"""
What is the Big O of this function?

```dart
int first(List<int> items) => items[0];
```
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the Big O of this function?

```dart
int total(List<int> items) {
  var sum = 0;
  for (final x in items) {
    sum += x;
  }
  return sum;
}
```
""", ["O(n)", "O(1)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
What is the Big O of this function?

```dart
void pairs(List<int> items) {
  for (final a in items) {
    for (final b in items) {
      print('$a$b');
    }
  }
}
```
""", ["O(n²)", "O(n)", "O(2n)", "O(n log n)"], "O(n²)"),

    mcq(r"""
Simplify `O(3n + 10)`:
""", ["O(n)", "O(3n)", "O(n + 10)", "O(1)"], "O(n)"),

    mcq(r"""
Simplify `O(n² + 5n + 100)`:
""", ["O(n²)", "O(n² + n)", "O(n)", "O(100)"], "O(n²)"),

    mcq(r"""
Simplify `O(n log n + n)`:
""", ["O(n log n)", "O(n)", "O(log n)", "O(n² log n)"], "O(n log n)"),

    order(r"""
Order these complexities from fastest (best) to slowest (worst):

```dart
// %order% < %order% < %order% < %order% < %order%
```
""", ["O(n log n)", "O(1)", "O(n²)", "O(log n)", "O(n)"],
        ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"]),

    mcq(r"""
A loop that halves `n` every iteration runs about how many times?
""", ["log₂ n", "n", "n / 2", "n²"], "log₂ n"),

    mcq(r"""
What does this print?

```dart
void main() {
  var n = 16;
  var count = 0;
  while (n > 1) {
    n ~/= 2;
    count++;
  }
  print(count);
}
```
""", ["4", "8", "16", "5"], "4"),

    fill(r"""
Fill in the operator for integer division:

```dart
void main() {
  final mid = (0 + 9) %fill% 2;
  print(mid); // 4
}
```
""", "~/"),

    mcq(r"""
About how many steps does binary search need for 1,000,000 sorted items?
""", ["About 20", "About 1,000", "About 500,000", "About 1,000,000"], "About 20"),

    mcq(r"""
What must be true about a list before you can binary search it?
""", ["It must be sorted", "It must have an even length", "It must contain no zeros",
       "It must be a Set"], "It must be sorted"),

    mcq(r"""
What is the time complexity of Dart's `List.sort()`?
""", ["O(n log n)", "O(n)", "O(n²)", "O(log n)"], "O(n log n)"),

    mcq(r"""
What is the Big O of this function?

```dart
void printBoth(List<int> a, List<int> b) {
  for (final x in a) print(x);
  for (final y in b) print(y);
}
```
""", ["O(a + b)", "O(a × b)", "O(n²)", "O(1)"], "O(a + b)"),

    mcq(r"""
What is the Big O of this function?

```dart
void grid(List<int> rows, List<int> cols) {
  for (final r in rows) {
    for (final c in cols) {
      print('$r,$c');
    }
  }
}
```
""", ["O(r × c)", "O(r + c)", "O(n)", "O(log n)"], "O(r × c)"),

    mcq(r"""
Why is this function O(n²) even though it has only one visible loop?

```dart
List<int> common(List<int> a, List<int> b) =>
    a.where((x) => b.contains(x)).toList();
```
""", [
        "b.contains is O(n) and runs once per element of a",
        "where() always sorts the list first",
        "toList() is O(n²)",
        "It isn't O(n²); it's O(n)",
    ], "b.contains is O(n) and runs once per element of a"),

    fill(r"""
Make the lookup O(1) average by converting `b` first:

```dart
List<int> common(List<int> a, List<int> b) {
  final bSet = b.%fill%();
  return a.where(bSet.contains).toList();
}

void main() {
  print(common([1, 2, 3], [2, 3, 4]));
}
```
""", "toSet"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3, 4];
  final bSet = {3, 4, 5};
  print(a.where(bSet.contains).toList());
}
```
""", ["[3, 4]", "[1, 2]", "[3, 4, 5]", "[]"], "[3, 4]"),

    mcq(r"""
What is the cost of `list.insert(0, x)` on a Dart List with n items?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the cost of `list.removeLast()`?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the overall complexity of this loop?

```dart
void main() {
  final out = <int>[];
  for (final x in [1, 2, 3, 4]) {
    out.insert(0, x);
  }
  print(out);
}
```
""", ["O(n²)", "O(n)", "O(log n)", "O(1)"], "O(n²)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final out = <int>[];
  for (final x in [1, 2, 3, 4]) {
    out.insert(0, x);
  }
  print(out);
}
```
""", ["[4, 3, 2, 1]", "[1, 2, 3, 4]", "[1, 4, 3, 2]", "[4]"], "[4, 3, 2, 1]"),

    mcq(r"""
What is the cost of `map.containsValue(v)`?
""", ["O(n)", "O(1)", "O(log n)", "O(n log n)"], "O(n)"),

    mcq(r"""
What is the average cost of `map.containsKey(k)` on a Dart `Map`?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the space complexity of this function (extra memory)?

```dart
int sum(List<int> nums) {
  var total = 0;
  for (final n in nums) total += n;
  return total;
}
```
""", ["O(1)", "O(n)", "O(n²)", "O(log n)"], "O(1)"),

    mcq(r"""
What is the space complexity of this function?

```dart
List<int> doubled(List<int> nums) => [for (final n in nums) n * 2];
```
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
Why does this recursive function use O(n) extra space?

```dart
int sumRec(List<int> nums, [int i = 0]) {
  if (i == nums.length) return 0;
  return nums[i] + sumRec(nums, i + 1);
}
```
""", [
        "Each recursive call adds a stack frame, and there are n calls",
        "It copies the list on every call",
        "It creates a Set of visited indexes",
        "Recursion always uses O(n²) space",
    ], "Each recursive call adds a stack frame, and there are n calls"),

    mcq(r"""
What does this print?

```dart
int sumRec(List<int> nums, [int i = 0]) {
  if (i == nums.length) return 0;
  return nums[i] + sumRec(nums, i + 1);
}

void main() {
  print(sumRec([2, 4, 6]));
}
```
""", ["12", "6", "0", "246"], "12"),

    mcq(r"""
What is the time complexity of the naive recursive Fibonacci?

```dart
int fib(int n) => n <= 1 ? n : fib(n - 1) + fib(n - 2);
```
""", ["Exponential (about O(2ⁿ))", "O(n)", "O(log n)", "O(n²)"],
        "Exponential (about O(2ⁿ))"),

    mcq(r"""
What does this print?

```dart
int fib(int n) => n <= 1 ? n : fib(n - 1) + fib(n - 2);

void main() {
  print(fib(10));
}
```
""", ["55", "89", "34", "10"], "55"),

    mcq(r"""
Which technique turns the naive exponential Fibonacci into O(n)?
""", ["Memoization (remembering computed results)", "Using a Set instead of recursion",
       "Calling sort() first", "Using double instead of int"],
        "Memoization (remembering computed results)"),

    mcq(r"""
For linear search, what is the best case?
""", ["O(1): the target is the first item", "O(n): the target is missing",
       "O(log n): the list is halved", "O(n²): every pair is checked"],
        "O(1): the target is the first item"),

    mcq(r"""
For linear search, what is the worst case?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
Hash map lookups are usually quoted as O(1). Which case is that?
""", ["Average case", "Worst case", "Best case only", "Amortized worst case"],
        "Average case"),

    mcq(r"""
What is the worst case of a hash map lookup when everything collides?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
Which sorting algorithm has a worst case of O(n²)?
""", ["Quick sort", "Merge sort", "Heap sort", "None of them"], "Quick sort"),

    mcq(r"""
What is the overall complexity?

```dart
void mystery(List<int> items) {
  items.sort();
  for (final x in items) {
    print(x);
  }
}
```
""", ["O(n log n)", "O(n)", "O(n²)", "O(n² log n)"], "O(n log n)"),

    mcq(r"""
What is the overall complexity of a loop over n items where each iteration does an O(log n) halving loop?
""", ["O(n log n)", "O(n)", "O(log n)", "O(n²)"], "O(n log n)"),

    order(r"""
Complete binary search:

```dart
int search(List<int> a, int t) {
  var lo = 0, hi = a.length - 1;
  while (lo %order% hi) {
    final mid = (lo + hi) %order% 2;
    if (a[mid] == t) return mid;
    if (a[mid] < t) {
      lo = mid %order% 1;
    } else {
      hi = mid %order% 1;
    }
  }
  return -1;
}
```
""", ["<=", "~/", "+", "-", "/", "*", ">="], ["<=", "~/", "+", "-"]),

    mcq(r"""
What does this print?

```dart
int search(List<int> a, int t) {
  var lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    final mid = (lo + hi) ~/ 2;
    if (a[mid] == t) return mid;
    if (a[mid] < t) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}

void main() {
  print(search([1, 3, 5, 7, 9, 11], 9));
}
```
""", ["4", "3", "5", "-1"], "4"),

    mcq(r"""
What does this print?

```dart
int search(List<int> a, int t) {
  var lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    final mid = (lo + hi) ~/ 2;
    if (a[mid] == t) return mid;
    if (a[mid] < t) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}

void main() {
  print(search([1, 3, 5, 7], 4));
}
```
""", ["-1", "2", "null", "It throws an error"], "-1"),

    mcq(r"""
Which change makes duplicate detection O(n) instead of O(n²)?
""", [
        "Track seen items in a Set",
        "Use two nested for loops",
        "Sort the list after every check",
        "Use list.indexOf for every item",
    ], "Track seen items in a Set"),

    fill(r"""
Complete the O(n) duplicate check:

```dart
bool hasDup(List<int> items) {
  final seen = <int>{};
  for (final x in items) {
    if (!seen.%fill%(x)) return true;
  }
  return false;
}
```
""", "add"),

    mcq(r"""
What does this print?

```dart
bool hasDup(List<int> items) {
  final seen = <int>{};
  for (final x in items) {
    if (!seen.add(x)) return true;
  }
  return false;
}

void main() {
  print(hasDup([1, 2, 3]));
  print(hasDup([1, 2, 1]));
}
```
""", ["false then true", "true then false", "false then false", "true then true"],
        "false then true"),

    mcq(r"""
If an algorithm is O(n²) and takes 1 second for 1,000 items, roughly how long for 10,000 items?
""", ["About 100 seconds", "About 10 seconds", "About 1 second", "About 1,000 seconds"],
        "About 100 seconds"),

    mcq(r"""
If an algorithm is O(n) and takes 2 seconds for 1 million items, roughly how long for 2 million?
""", ["About 4 seconds", "About 2 seconds", "About 8 seconds", "About 3 seconds"],
        "About 4 seconds"),

    mcq(r"""
Going from 1 million to 1 billion items adds roughly how many steps to binary search?
""", ["About 10", "About 1,000", "About 1 million", "It doubles"], "About 10"),

    mcq(r"""
What is the Big O of a function that always prints only the first 10 items of a list (or fewer if shorter)?
""", ["O(1)", "O(n)", "O(10n)", "O(log n)"], "O(1)"),

    fill(r"""
Complete the import that provides `log`, `ln2` and `pow`:

```dart
import 'dart:%fill%';

void main() {
  print(pow(2, 10)); // 1024
}
```
""", "math"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  print((log(1024) / ln2).round());
}
```
""", ["10", "1024", "2", "512"], "10"),

    mcq(r"""
What is the Big O of `list.length` on a Dart List?
""", ["O(1)", "O(n)", "O(log n)", "It depends on the item type"], "O(1)"),

    mcq(r"""
What is the Big O of `queue.removeFirst()` on a Dart `Queue`?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the cost of looking up a key in a `SplayTreeMap`?
""", ["O(log n) amortized", "O(1)", "O(n²)", "O(n) always"], "O(log n) amortized"),

    order(r"""
Complete the reverse email index (map comprehension):

```dart
void main() {
  final users = {'u1': 'ada@x.com', 'u2': 'bob@x.com'};
  final byEmail = {%order% (final e in users.%order%) e.%order%: e.%order%};
  print(byEmail['bob@x.com']); // u2
}
```
""", ["for", "entries", "value", "key", "keys", "while"],
        ["for", "entries", "value", "key"]),

    mcq(r"""
Which statement about dropping constants is correct?
""", [
        "O(2n) and O(n) describe the same growth rate",
        "O(2n) is twice as slow so it's a different class",
        "Constants matter more than the highest term",
        "O(n/2) is the same as O(log n)",
    ], "O(2n) and O(n) describe the same growth rate"),

    mcq(r"""
Which of these is exponential?
""", ["O(2ⁿ)", "O(n²)", "O(n log n)", "O(n¹⁰⁰)"], "O(2ⁿ)"),

    mcq(r"""
What does this print?

```dart
void main() {
  var steps = 0;
  for (var i = 0; i < 4; i++) {
    for (var j = 0; j < 4; j++) {
      steps++;
    }
  }
  print(steps);
}
```
""", ["16", "8", "4", "256"], "16"),

    mcq(r"""
What does this print?

```dart
void main() {
  var steps = 0;
  final n = 5;
  for (var i = 0; i < n; i++) {
    for (var j = i + 1; j < n; j++) {
      steps++;
    }
  }
  print(steps);
}
```
""", ["10", "25", "5", "20"], "10"),

    mcq(r"""
A nested loop where the inner loop starts at `i + 1` does n(n−1)/2 steps. What is its Big O?

```dart
for (var i = 0; i < n; i++) {
  for (var j = i + 1; j < n; j++) {
    steps++;
  }
}
```
""", ["O(n²)", "O(n)", "O(n/2)", "O(log n)"], "O(n²)"),
]
