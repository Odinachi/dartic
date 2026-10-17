INS = r"""void insertionSort(List<int> a) {
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && a[j] > cur) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = cur;
  }
}
"""

QUESTIONS = [
    mcq(r"""
What is the worst-case time complexity of bubble, selection and insertion sort?
""", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], "O(n²)"),

    mcq(r"""
What does "in-place" mean for a sorting algorithm?
""", ["It uses only O(1) extra memory", "It never moves elements", "It sorts in O(n)",
       "It keeps equal elements in order"], "It uses only O(1) extra memory"),

    mcq(r"""
What does "stable" mean for a sorting algorithm?
""", ["Equal elements keep their original relative order", "It never crashes",
       "It always runs in O(n log n)", "It uses no extra memory"],
        "Equal elements keep their original relative order"),

    mcq(r"""
What does "adaptive" mean for a sorting algorithm?
""", ["It runs faster on input that's already partly sorted", "It changes algorithm randomly",
       "It works on any data type", "It sorts in place"],
        "It runs faster on input that's already partly sorted"),

    mcq(r"""
What is an inversion?
""", ["A pair i < j where a[i] > a[j]", "A reversed list", "A swap of two elements",
       "A pair of equal elements"], "A pair i < j where a[i] > a[j]"),

    mcq(r"""
How many inversions does a reversed list of n elements have?
""", ["n(n − 1)/2", "n", "0", "n²"], "n(n − 1)/2"),

    mcq(r"""
How does bubble sort work?
""", ["Repeatedly swaps adjacent elements that are out of order",
       "Selects the minimum and swaps it to the front", "Inserts each element into a sorted prefix",
       "Splits the list in half recursively"],
        "Repeatedly swaps adjacent elements that are out of order"),

    mcq(r"""
After the first pass of bubble sort (ascending), what is guaranteed?
""", ["The largest element is at the end", "The smallest element is at the start",
       "The list is sorted", "The middle element is correct"],
        "The largest element is at the end"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [5, 1, 4, 2, 8];
  for (var i = 0; i < a.length - 1; i++) {
    if (a[i] > a[i + 1]) {
      final t = a[i];
      a[i] = a[i + 1];
      a[i + 1] = t;
    }
  }
  print(a);
}
```
""", ["[1, 4, 2, 5, 8]", "[1, 2, 4, 5, 8]", "[5, 1, 4, 2, 8]", "[1, 5, 4, 2, 8]"],
        "[1, 4, 2, 5, 8]"),

    mcq(r"""
What does bubble sort's early-exit optimization do?
""", ["Stops if a full pass makes no swaps", "Stops after n/2 passes",
       "Skips the first element", "Stops when the minimum is found"],
        "Stops if a full pass makes no swaps"),

    mcq(r"""
What is bubble sort's best case with early exit (already sorted input)?
""", ["O(n)", "O(n²)", "O(1)", "O(log n)"], "O(n)"),

    mcq(r"""
How does selection sort work?
""", ["Finds the minimum of the unsorted part and swaps it to the front of that part",
       "Swaps adjacent out-of-order elements", "Slides each element left into place",
       "Merges sorted halves"],
        "Finds the minimum of the unsorted part and swaps it to the front of that part"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [64, 25, 12, 22, 11];
  var m = 0;
  for (var j = 1; j < a.length; j++) {
    if (a[j] < a[m]) m = j;
  }
  final t = a[0];
  a[0] = a[m];
  a[m] = t;
  print(a);
}
```
""", ["[11, 25, 12, 22, 64]", "[11, 12, 22, 25, 64]", "[25, 64, 12, 22, 11]",
       "[64, 25, 12, 22, 11]"], "[11, 25, 12, 22, 64]"),

    mcq(r"""
How many swaps does selection sort perform at most?
""", ["n − 1", "n²", "n(n − 1)/2", "log n"], "n − 1"),

    mcq(r"""
Why might selection sort be chosen despite being O(n²)?
""", ["It does the fewest writes, useful when writing is expensive", "It's stable",
       "It's O(n) on sorted data", "It's the fastest algorithm"],
        "It does the fewest writes, useful when writing is expensive"),

    mcq(r"""
Is selection sort stable?
""", ["No: long-distance swaps can reorder equal elements", "Yes", "Only for integers",
       "Only for sorted input"], "No: long-distance swaps can reorder equal elements"),

    mcq(r"""
Is selection sort adaptive?
""", ["No: it scans the whole unsorted part even on sorted input", "Yes", "Only with early exit",
       "Only for small lists"], "No: it scans the whole unsorted part even on sorted input"),

    mcq(r"""
How does insertion sort work?
""", ["Takes each element and slides it left into its place in the sorted prefix",
       "Finds the maximum and moves it to the end", "Splits the list into halves",
       "Swaps random pairs"],
        "Takes each element and slides it left into its place in the sorted prefix"),

    mcq(r"""
What does this print?

```dart
""" + INS + r"""
void main() {
  final a = [3, 1, 2];
  insertionSort(a);
  print(a);
}
```
""", ["[1, 2, 3]", "[3, 2, 1]", "[1, 3, 2]", "[2, 1, 3]"], "[1, 2, 3]"),

    order(r"""
Complete insertion sort:

```dart
for (var i = 1; i < a.length; i++) {
  final cur = a[i];
  var j = i %order% 1;
  while (j >= 0 && a[j] %order% cur) {
    a[j + 1] = a[j];
    j--;
  }
  a[j %order% 1] = cur;
}
```
""", ["-", ">", "+", ">=", "*"], ["-", ">", "+"]),

    mcq(r"""
Why does insertion sort save `cur = a[i]` before shifting?
""", ["Shifting overwrites a[i], so the value must be kept", "To sort descending",
       "To count inversions", "It isn't needed"],
        "Shifting overwrites a[i], so the value must be kept"),

    mcq(r"""
What is insertion sort's best case (already sorted input)?
""", ["O(n)", "O(n²)", "O(1)", "O(n log n)"], "O(n)"),

    mcq(r"""
How many shifts does insertion sort perform?
""", ["Exactly the number of inversions", "Always n²", "Always n", "log n"],
        "Exactly the number of inversions"),

    mcq(r"""
What does this print?

```dart
int shifts(List<int> a) {
  var s = 0;
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && a[j] > cur) {
      a[j + 1] = a[j];
      j--;
      s++;
    }
    a[j + 1] = cur;
  }
  return s;
}

void main() {
  print(shifts([1, 2, 4, 3, 5]));
  print(shifts([4, 3, 2, 1]));
}
```
""", ["1 then 6", "1 then 4", "2 then 6", "0 then 6"], "1 then 6"),

    mcq(r"""
Which elementary sort is best for small or nearly sorted lists?
""", ["Insertion sort", "Selection sort", "Bubble sort without early exit", "None"],
        "Insertion sort"),

    mcq(r"""
Why do hybrid sorts like Timsort use insertion sort for small chunks?
""", ["It's simple, cache-friendly and very fast on short or nearly sorted runs",
       "It's O(n log n)", "It uses no comparisons", "It's unstable"],
        "It's simple, cache-friendly and very fast on short or nearly sorted runs"),

    mcq(r"""
What happens if insertion sort uses `a[j] >= cur` instead of `a[j] > cur`?
""", ["Equal elements move past each other, so it's no longer stable", "It becomes faster",
       "It crashes", "Nothing"], "Equal elements move past each other, so it's no longer stable"),

    mcq(r"""
Which of the three elementary sorts are stable (in their standard form)?
""", ["Bubble and insertion", "Selection only", "All three", "None"], "Bubble and insertion"),

    mcq(r"""
What does this print?

```dart
void main() {
  final cards = [(4, 'S'), (4, 'H'), (2, 'D')];
  for (var i = 0; i < cards.length - 1; i++) {
    var m = i;
    for (var j = i + 1; j < cards.length; j++) {
      if (cards[j].$1 < cards[m].$1) m = j;
    }
    final t = cards[i];
    cards[i] = cards[m];
    cards[m] = t;
  }
  print(cards.map((c) => c.$2).join());
}
```
""", ["DHS", "DSH", "SHD", "HSD"], "DHS"),

    mcq(r"""
Selection-sorting cards [(4, S), (4, H), (2, D)] by rank produces D, H, S. What does the H/S order show?
""", ["Selection sort is not stable", "Selection sort is adaptive", "The comparator is wrong",
       "Cards can't be sorted"], "Selection sort is not stable"),

    mcq(r"""
Why does stability matter when sorting by multiple keys?
""", ["Sorting by a secondary key first, then stably by the primary key keeps ties in secondary order",
       "It makes sorting faster", "It reduces memory", "It doesn't matter"],
        "Sorting by a secondary key first, then stably by the primary key keeps ties in secondary order"),

    mcq(r"""
What does a comparator `(a, b) => b.compareTo(a)` produce?
""", ["Descending order", "Ascending order", "Random order", "An error"], "Descending order"),

    mcq(r"""
What should a comparator return when a should come BEFORE b?
""", ["A negative number", "A positive number", "0", "true"], "A negative number"),

    mcq(r"""
What does this print?

```dart
void sortBy<T>(List<T> a, int Function(T, T) cmp) {
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && cmp(a[j], cur) > 0) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = cur;
  }
}

void main() {
  final words = ['pear', 'fig', 'banana', 'kiwi'];
  sortBy<String>(words, (a, b) => a.length.compareTo(b.length));
  print(words);
}
```
""", ["[fig, pear, kiwi, banana]", "[fig, kiwi, pear, banana]", "[banana, kiwi, pear, fig]",
       "[pear, fig, banana, kiwi]"], "[fig, pear, kiwi, banana]"),

    mcq(r"""
Stable-sorting ['pear', 'fig', 'banana', 'kiwi'] by length gives fig, pear, kiwi, banana. Why does 'pear' come before 'kiwi'?
""", ["Both have length 4, and a stable sort keeps their original order",
       "Alphabetical order", "pear is shorter", "It's random"],
        "Both have length 4, and a stable sort keeps their original order"),

    mcq(r"""
Which algorithm does the fewest comparisons on already-sorted input?
""", ["Insertion sort (n − 1 comparisons)", "Selection sort", "They're all equal",
       "Bubble sort without early exit"], "Insertion sort (n − 1 comparisons)"),

    mcq(r"""
How many comparisons does selection sort make on any input of n elements?
""", ["n(n − 1)/2", "n − 1", "n log n", "It depends on the input"], "n(n − 1)/2"),

    mcq(r"""
What does this print?

```dart
void main() {
  var count = 0;
  final a = [2, 4, 1, 3, 5];
  for (var i = 0; i < a.length; i++) {
    for (var j = i + 1; j < a.length; j++) {
      if (a[i] > a[j]) count++;
    }
  }
  print(count);
}
```
""", ["3", "2", "4", "5"], "3"),

    mcq(r"""
Which sort would you use in production Dart code for 1,000,000 numbers?
""", ["List.sort() (O(n log n))", "Bubble sort", "Selection sort", "Insertion sort"],
        "List.sort() (O(n log n))"),

    mcq(r"""
What is cocktail shaker sort?
""", ["Bubble sort that alternates left-to-right and right-to-left passes",
       "Selection sort with two minimums", "Insertion sort with binary search",
       "A random shuffle"], "Bubble sort that alternates left-to-right and right-to-left passes"),

    mcq(r"""
What does binary insertion sort improve?
""", ["The number of comparisons (O(log i) to find each spot), but not the shifts",
       "The number of shifts", "Stability", "It makes it O(n log n) overall"],
        "The number of comparisons (O(log i) to find each spot), but not the shifts"),

    mcq(r"""
What does this print?

```dart
""" + INS + r"""
void main() {
  final a = [5, 4, 3, 2, 1];
  insertionSort(a);
  print('${a.first} ${a.last}');
}
```
""", ["1 5", "5 1", "1 1", "5 5"], "1 5"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, 2, 1];
  var passes = 0;
  for (var end = a.length - 1; end > 0; end--) {
    var swapped = false;
    for (var i = 0; i < end; i++) {
      if (a[i] > a[i + 1]) {
        final t = a[i];
        a[i] = a[i + 1];
        a[i + 1] = t;
        swapped = true;
      }
    }
    passes++;
    if (!swapped) break;
  }
  print('$a $passes');
}
```
""", ["[1, 2, 3] 2", "[1, 2, 3] 3", "[1, 2, 3] 1", "[3, 2, 1] 0"], "[1, 2, 3] 2"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3, 4];
  var passes = 0;
  for (var end = a.length - 1; end > 0; end--) {
    var swapped = false;
    for (var i = 0; i < end; i++) {
      if (a[i] > a[i + 1]) swapped = true;
    }
    passes++;
    if (!swapped) break;
  }
  print(passes);
}
```
""", ["1", "3", "4", "0"], "1"),

    mcq(r"""
What error occurs if bubble sort's inner loop runs `i < a.length` while comparing `a[i + 1]`?
""", ["RangeError on the last iteration", "StackOverflowError", "No error", "TypeError"],
        "RangeError on the last iteration"),

    mcq(r"""
Which elementary sort's inner loop is a `while` that may stop early?
""", ["Insertion sort", "Selection sort", "Bubble sort without early exit", "None"],
        "Insertion sort"),

    mcq(r"""
After step i of selection sort, what is true?
""", ["The first i + 1 positions hold the i + 1 smallest elements in order",
       "The last i elements are sorted", "The list is half sorted", "Nothing is guaranteed"],
        "The first i + 1 positions hold the i + 1 smallest elements in order"),

    mcq(r"""
After step i of insertion sort, what is true?
""", ["The first i + 1 elements are sorted relative to each other (but may not be final)",
       "The first i + 1 elements are the smallest overall", "The last element is the largest",
       "The list is fully sorted"],
        "The first i + 1 elements are sorted relative to each other (but may not be final)"),

    fill(r"""
Swap two list elements using a temporary variable:

```dart
void main() {
  final a = [1, 2];
  final %fill% = a[0];
  a[0] = a[1];
  a[1] = t;
  print(a); // [2, 1]
}
```
""", "t"),

    mcq(r"""
Which statement about all three elementary sorts is true?
""", ["They are all in-place comparison sorts", "They are all stable",
       "They are all O(n log n)", "They all need extra arrays"],
        "They are all in-place comparison sorts"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = ['b', 'a', 'c'];
  for (var i = 1; i < a.length; i++) {
    final cur = a[i];
    var j = i - 1;
    while (j >= 0 && a[j].compareTo(cur) > 0) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = cur;
  }
  print(a.join());
}
```
""", ["abc", "bac", "cba", "acb"], "abc"),

    mcq(r"""
If doubling the input size roughly quadruples a sort's running time, what is its complexity?
""", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], "O(n²)"),

    mcq(r"""
Which elementary sort is commonly used to teach sorting but rarely used in practice?
""", ["Bubble sort", "Insertion sort", "List.sort", "Merge sort"], "Bubble sort"),

    mcq(r"""
Sorting 2,000 random numbers, which is usually fastest?
""", ["List.sort()", "Insertion sort", "Selection sort", "Bubble sort"], "List.sort()"),
]
