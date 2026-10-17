QUESTIONS = [
    mcq(r"""
What makes counting, radix and bucket sort "non-comparison" sorts?
""", ["They place elements using their key values instead of comparing pairs",
       "They never move elements", "They only sort strings", "They use recursion"],
        "They place elements using their key values instead of comparing pairs"),

    mcq(r"""
How can non-comparison sorts beat the O(n log n) lower bound?
""", ["That bound only applies to algorithms that learn order solely by comparisons",
       "They cheat by skipping elements", "They are actually O(n log n)",
       "They only work on sorted data"],
        "That bound only applies to algorithms that learn order solely by comparisons"),

    mcq(r"""
What is the time complexity of counting sort with n items and key range k?
""", ["O(n + k)", "O(n log n)", "O(n × k)", "O(k log n)"], "O(n + k)"),

    mcq(r"""
When is counting sort a good choice?
""", ["When keys are integers in a small range", "When keys are arbitrary strings",
       "When the key range is huge", "When data is already sorted"],
        "When keys are integers in a small range"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, 1, 2, 3, 0];
  final counts = List<int>.filled(4, 0);
  for (final x in a) {
    counts[x]++;
  }
  print(counts);
}
```
""", ["[1, 1, 1, 2]", "[0, 1, 2, 3]", "[3, 1, 2, 3]", "[1, 2, 1, 1]"], "[1, 1, 1, 2]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [4, 2, 2, 0, 4];
  final counts = List<int>.filled(5, 0);
  for (final x in a) {
    counts[x]++;
  }
  final out = [
    for (var v = 0; v < 5; v++)
      for (var c = 0; c < counts[v]; c++) v,
  ];
  print(out);
}
```
""", ["[0, 2, 2, 4, 4]", "[4, 4, 2, 2, 0]", "[0, 2, 4]", "[4, 2, 2, 0, 4]"], "[0, 2, 2, 4, 4]"),

    mcq(r"""
Why does a stable counting sort compute prefix sums of the counts?
""", ["To find the starting output position for each key", "To count inversions",
       "To find the maximum key", "To remove duplicates"],
        "To find the starting output position for each key"),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = [2, 1, 2];
  var total = 0;
  for (var k = 0; k < counts.length; k++) {
    final c = counts[k];
    counts[k] = total;
    total += c;
  }
  print(counts);
}
```
""", ["[0, 2, 3]", "[2, 3, 5]", "[0, 1, 2]", "[2, 1, 2]"], "[0, 2, 3]"),

    mcq(r"""
What makes the record-based counting sort stable?
""", ["Items are placed by walking the input in order, so equal keys keep their order",
       "It compares names on ties", "It sorts twice", "It uses a Set"],
        "Items are placed by walking the input in order, so equal keys keep their order"),

    mcq(r"""
What does this print?

```dart
void main() {
  final items = [(3, 'Zoe'), (1, 'Ali'), (3, 'Mia'), (1, 'Kai')];
  final counts = List<int>.filled(4, 0);
  for (final (k, _) in items) {
    counts[k]++;
  }
  var total = 0;
  for (var k = 0; k < 4; k++) {
    final c = counts[k];
    counts[k] = total;
    total += c;
  }
  final out = List<String>.filled(items.length, '');
  for (final (k, name) in items) {
    out[counts[k]++] = name;
  }
  print(out.join(' '));
}
```
""", ["Ali Kai Zoe Mia", "Kai Ali Mia Zoe", "Ali Kai Mia Zoe", "Zoe Mia Ali Kai"],
        "Ali Kai Zoe Mia"),

    mcq(r"""
How does counting sort handle negative numbers?
""", ["Offset every key by the minimum so the smallest maps to index 0",
       "It can't, ever", "It takes absolute values", "It sorts them separately with bubble sort"],
        "Offset every key by the minimum so the smallest maps to index 0"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, -2, 0, -2];
  final lo = a.reduce((x, y) => x < y ? x : y);
  print([for (final x in a) x - lo]);
}
```
""", ["[5, 0, 2, 0]", "[3, -2, 0, -2]", "[1, 0, 0, 0]", "[5, 2, 0, 2]"], "[5, 0, 2, 0]"),

    mcq(r"""
Why is counting sort a bad choice for `[1, 1000000000]`?
""", ["The count array would need a billion slots for two numbers", "It can't sort two numbers",
       "The numbers are too small", "It isn't stable"],
        "The count array would need a billion slots for two numbers"),

    mcq(r"""
What does radix sort do?
""", ["Sorts keys one digit at a time with a stable sort per digit",
       "Picks a radix pivot and partitions", "Hashes keys into buckets randomly",
       "Compares the first digits only"],
        "Sorts keys one digit at a time with a stable sort per digit"),

    mcq(r"""
In LSD radix sort, which digit is processed first?
""", ["The least significant digit (ones)", "The most significant digit",
       "The middle digit", "A random digit"], "The least significant digit (ones)"),

    mcq(r"""
Why must each radix sort pass be stable?
""", ["So the order established by less significant digits is kept for ties",
       "To make it faster", "Because digits are unique", "It doesn't need to be"],
        "So the order established by less significant digits is kept for ties"),

    mcq(r"""
What does `(x ~/ exp) % 10` extract when x = 802 and exp = 10?
""", ["0", "2", "8", "80"], "0"),

    mcq(r"""
What does this print?

```dart
void main() {
  const x = 4729;
  print([for (var exp = 1; exp <= 1000; exp *= 10) (x ~/ exp) % 10]);
}
```
""", ["[9, 2, 7, 4]", "[4, 7, 2, 9]", "[4729, 472, 47, 4]", "[9, 29, 729, 4729]"],
        "[9, 2, 7, 4]"),

    mcq(r"""
What is the time complexity of radix sort with d digits in base b?
""", ["O(d × (n + b))", "O(n log n)", "O(n × b × d²)", "O(b^d)"], "O(d × (n + b))"),

    mcq(r"""
How many passes does base-10 radix sort need for numbers up to 802?
""", ["3", "2", "10", "802"], "3"),

    mcq(r"""
How many passes does base-256 radix sort need for 32-bit integers?
""", ["4", "32", "256", "8"], "4"),

    mcq(r"""
What does this print?

```dart
List<int> passByDigit(List<int> a, int exp) {
  final buckets = List.generate(10, (_) => <int>[]);
  for (final x in a) {
    buckets[(x ~/ exp) % 10].add(x);
  }
  return [for (final b in buckets) ...b];
}

void main() {
  print(passByDigit([170, 45, 75, 90, 802, 24, 2, 66], 1));
}
```
""", ["[170, 90, 802, 2, 24, 45, 75, 66]", "[2, 24, 45, 66, 75, 90, 170, 802]",
       "[802, 2, 24, 45, 66, 170, 75, 90]", "[170, 45, 75, 90, 802, 24, 2, 66]"],
        "[170, 90, 802, 2, 24, 45, 75, 66]"),

    mcq(r"""
What does this print?

```dart
List<int> radix(List<int> a) {
  var cur = [...a];
  final mx = cur.reduce((x, y) => x > y ? x : y);
  for (var exp = 1; mx ~/ exp > 0; exp *= 10) {
    final b = List.generate(10, (_) => <int>[]);
    for (final x in cur) {
      b[(x ~/ exp) % 10].add(x);
    }
    cur = [for (final bucket in b) ...bucket];
  }
  return cur;
}

void main() {
  print(radix([329, 457, 657, 839, 436, 720, 355]));
}
```
""", ["[329, 355, 436, 457, 657, 720, 839]", "[720, 355, 436, 457, 657, 329, 839]",
       "[839, 720, 657, 457, 436, 355, 329]", "[329, 457, 657, 839, 436, 720, 355]"],
        "[329, 355, 436, 457, 657, 720, 839]"),

    mcq(r"""
How does LSD radix sort handle fixed-length strings?
""", ["Bucket by character from the last position to the first", "Sort by length first only",
       "Hash each string", "It can't"], "Bucket by character from the last position to the first"),

    mcq(r"""
Why can LSD radix sort struggle with variable-length strings?
""", ["It assumes all keys have the same number of positions; shorter strings need padding",
       "It's unstable on strings", "Strings can't be bucketed", "It only works on digits"],
        "It assumes all keys have the same number of positions; shorter strings need padding"),

    mcq(r"""
What does this print?

```dart
void main() {
  var words = ['ba', 'ab', 'aa', 'bb'];
  for (var pos = 1; pos >= 0; pos--) {
    final b = List.generate(128, (_) => <String>[]);
    for (final w in words) {
      b[w.codeUnitAt(pos)].add(w);
    }
    words = [for (final x in b) ...x];
  }
  print(words);
}
```
""", ["[aa, ab, ba, bb]", "[ba, ab, aa, bb]", "[bb, ba, ab, aa]", "[aa, ba, ab, bb]"],
        "[aa, ab, ba, bb]"),

    mcq(r"""
What does bucket sort assume about the data?
""", ["Values are spread fairly evenly over a known range", "Values are all integers",
       "Values are already sorted", "Values are strings"],
        "Values are spread fairly evenly over a known range"),

    mcq(r"""
What is bucket sort's average time complexity with evenly spread data?
""", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
What happens to bucket sort if all values land in one bucket?
""", ["It degrades to the cost of sorting that one bucket", "It becomes O(1)",
       "It throws an error", "Nothing changes"],
        "It degrades to the cost of sorting that one bucket"),

    mcq(r"""
For n values in [0, 1), which bucket does value x go into?
""", ["floor(x × n)", "x % n", "round(x)", "n − x"], "floor(x × n)"),

    mcq(r"""
What does this print?

```dart
void main() {
  const n = 10;
  print([0.78, 0.17, 0.05].map((x) => (x * n).floor()).toList());
}
```
""", ["[7, 1, 0]", "[8, 2, 1]", "[78, 17, 5]", "[0, 1, 7]"], "[7, 1, 0]"),

    mcq(r"""
Which sort is best for 1,000,000 ages between 0 and 120?
""", ["Counting sort", "Bubble sort", "Bucket sort with 1 bucket", "Radix sort in base 1,000,000"],
        "Counting sort"),

    mcq(r"""
Which sort is best for 1,000,000 random 9-digit IDs?
""", ["Radix sort (or List.sort)", "Counting sort with a billion slots",
       "Bubble sort", "Selection sort"], "Radix sort (or List.sort)"),

    mcq(r"""
Which sort is best for general objects with a custom comparator and unknown key range?
""", ["List.sort (a comparison sort)", "Counting sort", "Radix sort", "Bucket sort"],
        "List.sort (a comparison sort)"),

    mcq(r"""
What does the "Dutch national flag" algorithm sort?
""", ["A list containing only three distinct values (e.g. 0, 1, 2) in one pass",
       "Strings by color", "Any integers", "Floating-point numbers"],
        "A list containing only three distinct values (e.g. 0, 1, 2) in one pass"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [2, 0, 1, 2, 0];
  var lo = 0, mid = 0, hi = a.length - 1;
  while (mid <= hi) {
    if (a[mid] == 0) {
      final t = a[lo];
      a[lo++] = a[mid];
      a[mid++] = t;
    } else if (a[mid] == 2) {
      final t = a[hi];
      a[hi--] = a[mid];
      a[mid] = t;
    } else {
      mid++;
    }
  }
  print(a);
}
```
""", ["[0, 0, 1, 2, 2]", "[2, 2, 1, 0, 0]", "[0, 1, 2, 0, 2]", "[2, 0, 1, 2, 0]"],
        "[0, 0, 1, 2, 2]"),

    mcq(r"""
In the Dutch flag algorithm, why isn't `mid` advanced after swapping a 2 to the end?
""", ["The value swapped in from the end hasn't been examined yet", "It's a bug",
       "2s must be checked twice", "To keep it stable"],
        "The value swapped in from the end hasn't been examined yet"),

    mcq(r"""
What does this print?

```dart
void main() {
  final ratings = [5, 3, 5, 4, 5];
  final counts = List<int>.filled(6, 0);
  for (final r in ratings) {
    counts[r]++;
  }
  print('${counts[5]} ${'*' * counts[4]}');
}
```
""", ["3 *", "3 ***", "1 *", "5 *"], "3 *"),

    mcq(r"""
Which non-comparison sort uses about 10 buckets per pass in base 10?
""", ["Radix sort", "Counting sort with k = 10⁹", "Bucket sort with n buckets", "Quick sort"],
        "Radix sort"),

    mcq(r"""
Is counting sort (the stable, prefix-sum version) stable?
""", ["Yes", "No", "Only for negative numbers", "Only when k < n"], "Yes"),

    mcq(r"""
What extra space does counting sort use?
""", ["O(n + k)", "O(1)", "O(log n)", "O(n²)"], "O(n + k)"),

    mcq(r"""
Which statement is true about counting sort vs merge sort for scores 0–100?
""", ["Counting sort is O(n + 101), merge sort is O(n log n)", "Merge sort is always faster",
       "Both are O(n²)", "Counting sort can't handle duplicates"],
        "Counting sort is O(n + 101), merge sort is O(n log n)"),

    mcq(r"""
What does `List<Student?>.filled(n, null)` followed by `.cast<Student>()` achieve?
""", ["Pre-sizes an output list, then exposes it as non-nullable after it's fully filled",
       "Sorts the students", "Removes null students", "Copies the list twice"],
        "Pre-sizes an output list, then exposes it as non-nullable after it's fully filled"),

    fill(r"""
Extract the digit at position `exp` (1, 10, 100, ...):

```dart
void main() {
  const x = 4729, exp = 100;
  print((x ~/ exp) %fill% 10); // 7
}
```
""", "%"),

    order(r"""
Complete the counting step of counting sort:

```dart
final counts = List<int>.%order%(maxValue %order% 1, 0);
for (final x in a) {
  counts[x]%order%;
}
```
""", ["filled", "+", "++", "generate", "-", "--"], ["filled", "+", "++"]),

    order(r"""
Complete the stable placement step:

```dart
for (final item in items) {
  out[counts[item.%order%]%order%] = %order%;
}
```
""", ["key", "++", "item", "value", "--", "counts"], ["key", "++", "item"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final grades = ['B', 'A', 'C', 'A'];
  final buckets = {'A': <String>[], 'B': <String>[], 'C': <String>[]};
  for (final g in grades) {
    buckets[g]!.add(g);
  }
  print(buckets.values.expand((b) => b).join());
}
```
""", ["AABC", "BACA", "CBAA", "ABC"], "AABC"),

    mcq(r"""
What does the h-index measure, and how can counting help compute it?
""", ["Largest h with h papers having ≥ h citations; count papers per citation level",
       "Average citations; sort descending", "Total papers; use a set",
       "Maximum citations; use a heap"],
        "Largest h with h papers having ≥ h citations; count papers per citation level"),

    mcq(r"""
Which sort would you NOT use for a list of 50 small integers in an app?
""", ["A custom radix sort in base 256 (overkill; List.sort is fine)", "List.sort",
       "Insertion sort", "Counting sort if values are tiny"],
        "A custom radix sort in base 256 (overkill; List.sort is fine)"),

    mcq(r"""
What does MSD radix sort do differently from LSD?
""", ["Processes the most significant digit first, recursing into buckets",
       "Uses comparisons", "Only works on negative numbers", "Isn't a radix sort"],
        "Processes the most significant digit first, recursing into buckets"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, 1, 3, 2];
  final maxV = a.reduce((x, y) => x > y ? x : y);
  print(maxV + 1);
}
```
""", ["4", "3", "2", "10"], "4"),

    mcq(r"""
Which key property is needed for counting sort keys?
""", ["They must map to small non-negative integer indexes (possibly after offsetting)",
       "They must be strings", "They must be unique", "They must be sorted already"],
        "They must map to small non-negative integer indexes (possibly after offsetting)"),

    mcq(r"""
What is the space cost of base-10 radix sort's buckets per pass?
""", ["O(n + 10)", "O(10ⁿ)", "O(1)", "O(n²)"], "O(n + 10)"),
]
