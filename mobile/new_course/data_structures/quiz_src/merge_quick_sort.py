MERGE = r"""List<int> merge(List<int> l, List<int> r) {
  final out = <int>[];
  var i = 0, j = 0;
  while (i < l.length && j < r.length) {
    out.add(l[i] <= r[j] ? l[i++] : r[j++]);
  }
  return out
    ..addAll(l.sublist(i))
    ..addAll(r.sublist(j));
}

List<int> mergeSort(List<int> a) {
  if (a.length <= 1) return a;
  final mid = a.length ~/ 2;
  return merge(mergeSort(a.sublist(0, mid)), mergeSort(a.sublist(mid)));
}
"""

PART = r"""int partition(List<int> a, int lo, int hi) {
  final pivot = a[hi];
  var store = lo;
  for (var i = lo; i < hi; i++) {
    if (a[i] < pivot) {
      final t = a[i];
      a[i] = a[store];
      a[store] = t;
      store++;
    }
  }
  final t = a[store];
  a[store] = a[hi];
  a[hi] = t;
  return store;
}
"""

QUESTIONS = [
    mcq(r"""
What are the three steps of divide and conquer?
""", ["Divide, conquer (recurse), combine", "Sort, search, return", "Push, pop, peek",
       "Hash, bucket, compare"], "Divide, conquer (recurse), combine"),

    mcq(r"""
In merge sort, where does most of the work happen?
""", ["In the merge (combine) step", "In the split step", "In choosing a pivot",
       "In the base case"], "In the merge (combine) step"),

    mcq(r"""
In quick sort, where does most of the work happen?
""", ["In the partition (divide) step", "In the combine step", "In the base case",
       "After recursion finishes"], "In the partition (divide) step"),

    mcq(r"""
What is merge sort's time complexity in the worst case?
""", ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "O(n log n)"),

    mcq(r"""
What is quick sort's worst-case time complexity?
""", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], "O(n²)"),

    mcq(r"""
What is quick sort's average time complexity?
""", ["O(n log n)", "O(n²)", "O(n)", "O(n³)"], "O(n log n)"),

    mcq(r"""
How much extra memory does a typical merge sort use?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
How much extra memory does quick sort use on average?
""", ["O(log n) for the recursion stack", "O(n)", "O(n²)", "None at all"],
        "O(log n) for the recursion stack"),

    mcq(r"""
Which of the two is stable?
""", ["Merge sort", "Quick sort", "Both", "Neither"], "Merge sort"),

    mcq(r"""
Which of the two sorts in place?
""", ["Quick sort", "Merge sort", "Both", "Neither"], "Quick sort"),

    mcq(r"""
What does this print?

```dart
""" + MERGE + r"""
void main() {
  print(merge([1, 5, 9], [2, 3, 10]));
}
```
""", ["[1, 2, 3, 5, 9, 10]", "[1, 5, 9, 2, 3, 10]", "[2, 3, 10, 1, 5, 9]", "[1, 2, 5, 3, 9, 10]"],
        "[1, 2, 3, 5, 9, 10]"),

    mcq(r"""
What does this print?

```dart
""" + MERGE + r"""
void main() {
  print(mergeSort([38, 27, 43, 3, 9]));
}
```
""", ["[3, 9, 27, 38, 43]", "[38, 27, 43, 3, 9]", "[43, 38, 27, 9, 3]", "[3, 27, 9, 38, 43]"],
        "[3, 9, 27, 38, 43]"),

    mcq(r"""
Why does merge use `<=` rather than `<` when comparing fronts?
""", ["On ties, the left element goes first, keeping the sort stable", "It's faster",
       "To avoid an infinite loop", "It doesn't matter"],
        "On ties, the left element goes first, keeping the sort stable"),

    mcq(r"""
What is the base case of recursive merge sort?
""", ["A list of 0 or 1 elements is already sorted", "A list of 2 elements",
       "An empty list only", "When the pivot is found"],
        "A list of 0 or 1 elements is already sorted"),

    mcq(r"""
How many levels of splitting does merge sort have for n elements?
""", ["About log₂ n", "n", "n / 2", "√n"], "About log₂ n"),

    mcq(r"""
Why is merge sort O(n log n)?
""", ["log n levels, each doing O(n) merging work", "n levels of O(log n) work each, only by luck",
       "It compares each pair once", "It uses hashing"],
        "log n levels, each doing O(n) merging work"),

    order(r"""
Complete recursive merge sort:

```dart
List<int> mergeSort(List<int> a) {
  if (a.length %order% 1) return a;
  final mid = a.length %order% 2;
  final left = mergeSort(a.%order%(0, mid));
  final right = mergeSort(a.sublist(mid));
  return merge(left, right);
}
```
""", ["<=", "~/", "sublist", ">=", "/", "getRange"], ["<=", "~/", "sublist"]),

    mcq(r"""
What does bottom-up merge sort do instead of recursion?
""", ["Merges runs of width 1, 2, 4, 8, ... iteratively", "Picks pivots in a loop",
       "Uses insertion sort only", "Sorts from right to left"],
        "Merges runs of width 1, 2, 4, 8, ... iteratively"),

    mcq(r"""
Which sort is the natural choice for sorting a linked list?
""", ["Merge sort", "Quick sort", "Selection sort", "Counting sort"], "Merge sort"),

    mcq(r"""
Which sort is used for "external sorting" of files too big for memory?
""", ["Merge sort (sort chunks, then merge them)", "Quick sort", "Bubble sort", "Heap sort"],
        "Merge sort (sort chunks, then merge them)"),

    mcq(r"""
What does partitioning do in quick sort?
""", ["Places the pivot in its final position with smaller elements left and larger right",
       "Splits the list exactly in half", "Merges two sorted lists", "Sorts the whole list"],
        "Places the pivot in its final position with smaller elements left and larger right"),

    mcq(r"""
What does this print?

```dart
""" + PART + r"""
void main() {
  final a = [7, 2, 9, 4, 3, 8, 5];
  final p = partition(a, 0, a.length - 1);
  print('$p ${a[p]}');
}
```
""", ["3 5", "6 5", "0 7", "3 4"], "3 5"),

    mcq(r"""
What does this print?

```dart
""" + PART + r"""
void main() {
  final a = [4, 1, 3, 2];
  partition(a, 0, 3);
  print(a);
}
```
""", ["[1, 2, 3, 4]", "[4, 1, 3, 2]", "[1, 3, 2, 4]", "[2, 1, 3, 4]"], "[1, 2, 3, 4]"),

    mcq(r"""
In Lomuto partition, which element is used as the pivot?
""", ["The last element of the range", "The first element", "The middle element",
       "The maximum"], "The last element of the range"),

    mcq(r"""
After partitioning around a pivot at index p, which ranges does quick sort recurse on?
""", ["lo..p − 1 and p + 1..hi", "lo..p and p..hi", "lo..hi twice", "Only lo..p − 1"],
        "lo..p − 1 and p + 1..hi"),

    mcq(r"""
Why can always choosing the first element as pivot be disastrous?
""", ["On already sorted input every split is maximally unbalanced, giving O(n²)",
       "It throws an error", "It makes the sort unstable only", "It uses too much memory"],
        "On already sorted input every split is maximally unbalanced, giving O(n²)"),

    mcq(r"""
How many comparisons does first-element-pivot quick sort make on 1,000 already sorted numbers?
""", ["499,500", "About 10,000", "1,000", "About 20"], "499,500"),

    mcq(r"""
Which pivot strategies avoid the worst case on sorted input?
""", ["Random pivot or median-of-three", "Always the first element", "Always the last element",
       "Always the smallest element"], "Random pivot or median-of-three"),

    mcq(r"""
What is three-way partitioning useful for?
""", ["Lists with many duplicate values", "Lists with no duplicates", "Linked lists",
       "Very small lists only"], "Lists with many duplicate values"),

    mcq(r"""
What are the three regions in three-way partitioning?
""", ["Less than, equal to, and greater than the pivot", "Small, medium and large lists",
       "Left half, middle, right half by index", "Sorted, unsorted, unknown"],
        "Less than, equal to, and greater than the pivot"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [2, 1, 2, 3, 2];
  final pivot = 2;
  final less = a.where((x) => x < pivot).toList();
  final equal = a.where((x) => x == pivot).toList();
  final greater = a.where((x) => x > pivot).toList();
  print([...less, ...equal, ...greater]);
}
```
""", ["[1, 2, 2, 2, 3]", "[2, 2, 2, 1, 3]", "[1, 3, 2, 2, 2]", "[2, 1, 2, 3, 2]"],
        "[1, 2, 2, 2, 3]"),

    mcq(r"""
Is Dart's `List.sort` guaranteed to be stable?
""", ["No", "Yes", "Only for ints", "Only for strings"], "No"),

    mcq(r"""
How can you make a sort's result independent of stability?
""", ["Add an explicit tie-breaker to the comparator", "Sort twice", "Use toSet first",
       "Reverse the list"], "Add an explicit tie-breaker to the comparator"),

    mcq(r"""
Which package provides a stable `mergeSort` for Dart lists?
""", ["package:collection", "dart:core", "dart:math", "package:path"], "package:collection"),

    mcq(r"""
What does this print?

```dart
void main() {
  final tasks = [(2, 'b'), (1, 'z'), (1, 'a')];
  tasks.sort((x, y) {
    final c = x.$1.compareTo(y.$1);
    return c != 0 ? c : x.$2.compareTo(y.$2);
  });
  print(tasks.map((t) => t.$2).join());
}
```
""", ["azb", "zab", "bza", "abz"], "azb"),

    mcq(r"""
What does this print?

```dart
void main() {
  final dates = [DateTime(2026, 3, 9), DateTime(2026, 3, 2), DateTime(2026, 3, 5)];
  dates.sort();
  print(dates.first.day);
}
```
""", ["2", "9", "5", "3"], "2"),

    mcq(r"""
What is the lower bound on worst-case comparisons for any comparison sort?
""", ["Ω(n log n)", "Ω(n)", "Ω(log n)", "Ω(n²)"], "Ω(n log n)"),

    mcq(r"""
Why can't a comparison sort beat n log n in the worst case?
""", ["There are n! orderings and each comparison only halves the possibilities",
       "Computers are too slow", "Because of memory limits", "It can, with hashing"],
        "There are n! orderings and each comparison only halves the possibilities"),

    mcq(r"""
How does merge sort count inversions in O(n log n)?
""", ["When a right-half element is taken during merge, it forms inversions with all remaining left elements",
       "By comparing every pair", "By counting swaps in partition", "It can't"],
        "When a right-half element is taken during merge, it forms inversions with all remaining left elements"),

    mcq(r"""
During a merge, left = [5, 7, 9] (all remaining) and right[j] = 4 is taken. How many cross inversions are added?
""", ["3", "1", "0", "4"], "3"),

    mcq(r"""
What does this print?

```dart
(List<int>, int) sortCount(List<int> a) {
  if (a.length <= 1) return (a, 0);
  final mid = a.length ~/ 2;
  final (l, x) = sortCount(a.sublist(0, mid));
  final (r, y) = sortCount(a.sublist(mid));
  final out = <int>[];
  var i = 0, j = 0, c = 0;
  while (i < l.length && j < r.length) {
    if (l[i] <= r[j]) {
      out.add(l[i++]);
    } else {
      c += l.length - i;
      out.add(r[j++]);
    }
  }
  out
    ..addAll(l.sublist(i))
    ..addAll(r.sublist(j));
  return (out, x + y + c);
}

void main() {
  print(sortCount([3, 1, 2]).$2);
}
```
""", ["2", "1", "3", "0"], "2"),

    mcq(r"""
What does quickselect find?
""", ["The k-th smallest element in O(n) average time", "The median in O(1)",
       "All duplicates", "The sorted order"], "The k-th smallest element in O(n) average time"),

    mcq(r"""
Why is quickselect O(n) on average instead of O(n log n)?
""", ["It recurses into only one side after partitioning", "It skips partitioning",
       "It uses hashing", "It sorts only half the list"],
        "It recurses into only one side after partitioning"),

    mcq(r"""
Which algorithm does Dart's `List.sort` use internally?
""", ["A dual-pivot quicksort with insertion sort for small ranges", "Bubble sort",
       "Pure merge sort", "Counting sort"],
        "A dual-pivot quicksort with insertion sort for small ranges"),

    mcq(r"""
Which has better cache behavior in practice?
""", ["Quick sort, because it works in place", "Merge sort, because it copies",
       "They're identical", "Neither uses the cache"],
        "Quick sort, because it works in place"),

    mcq(r"""
What happens if quick sort recurses on lo..p and p..hi (including the pivot again)?
""", ["It can recurse forever on the same range", "It sorts faster", "Nothing changes",
       "It becomes stable"], "It can recurse forever on the same range"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(5.clamp(0, 3));
  print((-2).clamp(0, 3));
}
```
""", ["3 then 0", "5 then -2", "3 then -2", "0 then 3"], "3 then 0"),

    mcq(r"""
What does `a.setAll(0, src)` do?
""", ["Overwrites a's elements starting at index 0 with src's elements", "Appends src to a",
       "Sorts a", "Clears a"], "Overwrites a's elements starting at index 0 with src's elements"),

    fill(r"""
Split a list at index mid (copying the second half):

```dart
void main() {
  final a = [1, 2, 3, 4];
  final right = a.%fill%(2);
  print(right); // [3, 4]
}
```
""", "sublist"),

    mcq(r"""
What does this print?

```dart
""" + MERGE + r"""
void main() {
  final a = [3, 1, 2];
  final b = mergeSort(a);
  print('$a $b');
}
```
""", ["[3, 1, 2] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]", "[3, 1, 2] [3, 1, 2]", "[1, 2, 3] [3, 1, 2]"],
        "[3, 1, 2] [1, 2, 3]"),

    mcq(r"""
A merge sort that uses `sublist` and a `merge` returning a new list leaves the input list unchanged. Why?
""", ["It builds new lists with sublist and merge instead of modifying the input",
       "Dart copies lists on every call", "It's sorted in place then restored",
       "It isn't unchanged"],
        "It builds new lists with sublist and merge instead of modifying the input"),

    mcq(r"""
If you need a guaranteed O(n log n) sort that's also stable, which do you choose?
""", ["Merge sort", "Quick sort", "Selection sort", "Quick sort with a fixed first pivot"],
        "Merge sort"),

    mcq(r"""
If memory is tight and average speed matters most, which do you choose?
""", ["Quick sort (with random pivots)", "Merge sort", "Bubble sort", "Counting sort with huge ranges"],
        "Quick sort (with random pivots)"),

    order(r"""
Complete the quick sort recursion:

```dart
void quickSort(List<int> a, int lo, int hi) {
  if (lo %order% hi) return;
  final p = partition(a, lo, hi);
  quickSort(a, lo, p %order% 1);
  quickSort(a, p %order% 1, hi);
}
```
""", [">=", "-", "+", "<", "*"], [">=", "-", "+"]),
]
