HEAP = r"""class MinHeap {
  final d = <int>[];

  void add(int v) {
    d.add(v);
    var i = d.length - 1;
    while (i > 0) {
      final p = (i - 1) ~/ 2;
      if (d[p] <= d[i]) break;
      final t = d[p];
      d[p] = d[i];
      d[i] = t;
      i = p;
    }
  }

  int removeMin() {
    final top = d.first, last = d.removeLast();
    if (d.isNotEmpty) {
      d[0] = last;
      var i = 0;
      while (true) {
        final l = 2 * i + 1, r = l + 1;
        var m = i;
        if (l < d.length && d[l] < d[m]) m = l;
        if (r < d.length && d[r] < d[m]) m = r;
        if (m == i) break;
        final t = d[i];
        d[i] = d[m];
        d[m] = t;
        i = m;
      }
    }
    return top;
  }
}
"""

QUESTIONS = [
    mcq(r"""
What does a priority queue always let you remove?
""", ["The item with the highest priority (e.g. the smallest value)", "The oldest item",
       "The newest item", "A random item"],
        "The item with the highest priority (e.g. the smallest value)"),

    mcq(r"""
What is the min-heap property?
""", ["Every parent is ≤ its children", "Every left child is < its right sibling",
       "The array is sorted", "Every leaf is at the same depth"],
        "Every parent is ≤ its children"),

    mcq(r"""
Where is the smallest element in a min-heap?
""", ["At the root (index 0)", "At the last index", "In the leftmost leaf",
       "It could be anywhere"], "At the root (index 0)"),

    mcq(r"""
Is the array behind a heap sorted?
""", ["No, only the root is guaranteed to be the min (or max)", "Yes, always ascending",
       "Yes, always descending", "Only after every insert"],
        "No, only the root is guaranteed to be the min (or max)"),

    mcq(r"""
What shape is a binary heap always?
""", ["A complete binary tree", "A degenerate tree", "A perfect tree only",
       "A BST"], "A complete binary tree"),

    mcq(r"""
In a 0-based heap array, what is the left child index of node i?
""", ["2i + 1", "2i", "i + 1", "(i - 1) ~/ 2"], "2i + 1"),

    mcq(r"""
In a 0-based heap array, what is the right child index of node i?
""", ["2i + 2", "2i + 1", "2i", "i + 2"], "2i + 2"),

    mcq(r"""
In a 0-based heap array, what is the parent index of node i?
""", ["(i - 1) ~/ 2", "i ~/ 2", "2i + 1", "i - 1"], "(i - 1) ~/ 2"),

    mcq(r"""
What does this print?

```dart
void main() {
  final heap = [2, 5, 3, 9, 6, 4];
  const i = 1;
  print('${heap[2 * i + 1]} ${heap[2 * i + 2]} ${heap[(i - 1) ~/ 2]}');
}
```
""", ["9 6 2", "5 3 2", "9 6 5", "3 9 2"], "9 6 2"),

    mcq(r"""
Why can heaps be stored in a plain array without gaps?
""", ["They are complete trees, filled level by level, left to right", "They are sorted",
       "They only store ints", "They have no leaves"],
        "They are complete trees, filled level by level, left to right"),

    mcq(r"""
What is the cost of peeking at the minimum of a min-heap?
""", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "O(1)"),

    mcq(r"""
What is the cost of inserting into a binary heap?
""", ["O(log n)", "O(1)", "O(n)", "O(n log n)"], "O(log n)"),

    mcq(r"""
What is the cost of removing the minimum from a binary heap?
""", ["O(log n)", "O(1)", "O(n)", "O(n²)"], "O(log n)"),

    mcq(r"""
What is the cost of searching a heap for an arbitrary value?
""", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "O(n)"),

    mcq(r"""
How does insertion work in a min-heap?
""", ["Add at the end, then swap with the parent while smaller (sift up)",
       "Add at the root, then sift down", "Insert in sorted position",
       "Add anywhere and re-sort"],
        "Add at the end, then swap with the parent while smaller (sift up)"),

    mcq(r"""
How does removeMin work in a min-heap?
""", ["Move the last element to the root, then sift down toward the smaller child",
       "Remove index 0 and shift everything left", "Remove the last element",
       "Sort and remove the first"],
        "Move the last element to the root, then sift down toward the smaller child"),

    mcq(r"""
When sifting down in a min-heap, which child do you swap with?
""", ["The smaller child", "The larger child", "Always the left child", "Always the right child"],
        "The smaller child"),

    mcq(r"""
What does this print?

```dart
""" + HEAP + r"""
void main() {
  final h = MinHeap();
  for (final x in [7, 3, 5, 1]) {
    h.add(x);
  }
  print(h.d.first);
}
```
""", ["1", "7", "3", "5"], "1"),

    mcq(r"""
What does this print?

```dart
""" + HEAP + r"""
void main() {
  final h = MinHeap();
  for (final x in [7, 3, 5, 1]) {
    h.add(x);
  }
  print(h.d);
}
```
""", ["[1, 3, 5, 7]", "[1, 7, 5, 3]", "[7, 3, 5, 1]", "[1, 5, 3, 7]"], "[1, 3, 5, 7]"),

    mcq(r"""
What does this print?

```dart
""" + HEAP + r"""
void main() {
  final h = MinHeap();
  for (final x in [4, 9, 2, 8, 1]) {
    h.add(x);
  }
  final out = <int>[];
  while (h.d.isNotEmpty) {
    out.add(h.removeMin());
  }
  print(out);
}
```
""", ["[1, 2, 4, 8, 9]", "[4, 9, 2, 8, 1]", "[9, 8, 4, 2, 1]", "[1, 4, 2, 8, 9]"],
        "[1, 2, 4, 8, 9]"),

    mcq(r"""
What does this print?

```dart
""" + HEAP + r"""
void main() {
  final h = MinHeap();
  for (final x in [5, 3, 8]) {
    h.add(x);
  }
  h.removeMin();
  print(h.d.first);
}
```
""", ["5", "3", "8", "It throws an error"], "5"),

    mcq(r"""
How do you turn a min-heap with a comparator into a max-heap?
""", ["Reverse the comparator, e.g. (a, b) => b.compareTo(a)", "Sort the array descending",
       "Use removeLast instead", "It's impossible"],
        "Reverse the comparator, e.g. (a, b) => b.compareTo(a)"),

    mcq(r"""
Where is the largest element in a max-heap?
""", ["At the root", "At the last index", "In a leaf", "Anywhere"], "At the root"),

    mcq(r"""
What is "heapify"?
""", ["Building a heap from an existing array in O(n)", "Inserting one item",
       "Sorting a heap", "Converting a heap into a BST"],
        "Building a heap from an existing array in O(n)"),

    mcq(r"""
Where does bottom-up heapify start sifting down?
""", ["At index length ~/ 2 - 1 (the last non-leaf), moving back to 0",
       "At index 0, moving forward", "At the last index", "At the middle only"],
        "At index length ~/ 2 - 1 (the last non-leaf), moving back to 0"),

    mcq(r"""
Why is bottom-up heapify O(n) instead of O(n log n)?
""", ["Most nodes are near the bottom and only sift down a short distance",
       "It skips half the elements", "It uses a hash map", "It doesn't compare elements"],
        "Most nodes are near the bottom and only sift down a short distance"),

    mcq(r"""
What does this print?

```dart
void siftDown(List<int> a, int i, int n) {
  while (true) {
    final l = 2 * i + 1, r = l + 1;
    var m = i;
    if (l < n && a[l] < a[m]) m = l;
    if (r < n && a[r] < a[m]) m = r;
    if (m == i) return;
    final t = a[i];
    a[i] = a[m];
    a[m] = t;
    i = m;
  }
}

void main() {
  final a = [5, 4, 3, 2, 1];
  for (var i = a.length ~/ 2 - 1; i >= 0; i--) {
    siftDown(a, i, a.length);
  }
  print(a[0]);
}
```
""", ["1", "5", "2", "3"], "1"),

    mcq(r"""
What is the time complexity of heap sort?
""", ["O(n log n)", "O(n)", "O(n²)", "O(log n)"], "O(n log n)"),

    mcq(r"""
Which property does heap sort have?
""", ["In place, but not stable", "Stable, but uses O(n) extra space",
       "O(n) time", "Only works on strings"], "In place, but not stable"),

    mcq(r"""
In ascending heap sort, which kind of heap is built first?
""", ["A max-heap", "A min-heap", "A BST", "No heap"], "A max-heap"),

    mcq(r"""
To find the k LARGEST elements in a stream, which heap do you keep?
""", ["A min-heap of size k", "A max-heap of all elements", "A max-heap of size k",
       "A min-heap of all elements"], "A min-heap of size k"),

    mcq(r"""
Why use a min-heap (not a max-heap) of size k to track the k largest?
""", ["Its root is the smallest of the current top k, which is the one to evict",
       "Min-heaps are faster", "Max-heaps can't hold k items", "It doesn't matter"],
        "Its root is the smallest of the current top k, which is the one to evict"),

    mcq(r"""
What is the complexity of top-k with a size-k heap over n items?
""", ["O(n log k)", "O(n log n)", "O(k log n)", "O(n²)"], "O(n log k)"),

    mcq(r"""
What does this print?

```dart
""" + HEAP + r"""
List<int> topK(List<int> xs, int k) {
  final h = MinHeap();
  for (final x in xs) {
    if (h.d.length < k) {
      h.add(x);
    } else if (x > h.d.first) {
      h.removeMin();
      h.add(x);
    }
  }
  return h.d..sort();
}

void main() {
  print(topK([4, 1, 7, 3, 9, 2], 2));
}
```
""", ["[7, 9]", "[1, 2]", "[9, 7]", "[4, 7]"], "[7, 9]"),

    mcq(r"""
What is the k-th largest element, using a size-k min-heap after processing all items?
""", ["The heap's root", "The heap's last element", "The maximum in the heap",
       "It can't be found"], "The heap's root"),

    mcq(r"""
How many items are in the heap at a time when merging k sorted lists?
""", ["At most k (one candidate per list)", "All N items", "Exactly 1", "2k"],
        "At most k (one candidate per list)"),

    mcq(r"""
What is the complexity of merging k sorted lists with N total items using a heap?
""", ["O(N log k)", "O(N log N)", "O(N k)", "O(k log N)"], "O(N log k)"),

    mcq(r"""
Which Dart package provides a ready-made `PriorityQueue`?
""", ["package:collection", "dart:collection", "dart:core", "package:path"],
        "package:collection"),

    mcq(r"""
Which famous algorithm relies on a min-heap of distances?
""", ["Dijkstra's shortest path", "Binary search", "Bubble sort", "Kadane's algorithm"],
        "Dijkstra's shortest path"),

    mcq(r"""
How can you maintain the median of a stream efficiently?
""", ["Two heaps: a max-heap for the lower half and a min-heap for the upper half",
       "One sorted list", "A hash map of counts", "A stack"],
        "Two heaps: a max-heap for the lower half and a min-heap for the upper half"),

    mcq(r"""
In an emergency room priority queue, what does a two-level comparator (urgency, then arrival) achieve?
""", ["Equally urgent patients are served in arrival order", "Faster inserts",
       "Patients are sorted alphabetically", "It removes duplicates"],
        "Equally urgent patients are served in arrival order"),

    mcq(r"""
What does this print?

```dart
void main() {
  int cmp((int, int) a, (int, int) b) {
    final c = a.$1.compareTo(b.$1);
    return c != 0 ? c : a.$2.compareTo(b.$2);
  }

  final items = [(2, 1), (1, 5), (1, 2)]..sort(cmp);
  print(items.first);
}
```
""", ["(1, 2)", "(1, 5)", "(2, 1)", "It throws an error"], "(1, 2)"),

    mcq(r"""
What happens if you change an item's priority while it's inside a heap?
""", ["The heap property can break; remove and re-add it instead", "The heap re-sorts itself",
       "Nothing; heaps track changes", "It throws immediately"],
        "The heap property can break; remove and re-add it instead"),

    mcq(r"""
What is "lazy deletion" in priority queues?
""", ["Pushing a new entry and skipping stale ones when they're popped later",
       "Never removing anything", "Deleting the root only", "Deleting in a background isolate"],
        "Pushing a new entry and skipping stale ones when they're popped later"),

    mcq(r"""
Which structure gives O(1) min AND O(log n) arbitrary lookup by key?
""", ["None of these alone: a heap gives O(1) min but O(n) lookup", "A min-heap",
       "A FIFO queue", "A stack"],
        "None of these alone: a heap gives O(1) min but O(n) lookup"),

    mcq(r"""
In a 1-based heap array, what are the children of i?
""", ["2i and 2i + 1", "2i + 1 and 2i + 2", "i + 1 and i + 2", "i ~/ 2"], "2i and 2i + 1"),

    mcq(r"""
How many levels does a binary heap with 1,000,000 elements have, roughly?
""", ["About 20", "About 1,000", "About 500,000", "About 2"], "About 20"),

    order(r"""
Complete sift-up for a min-heap:

```dart
void siftUp(List<int> d, int i) {
  while (i > 0) {
    final p = (i %order% 1) %order% 2;
    if (d[p] <= d[i]) break;
    final t = d[p];
    d[p] = d[i];
    d[i] = t;
    i = %order%;
  }
}
```
""", ["-", "~/", "p", "+", "%", "i"], ["-", "~/", "p"]),

    order(r"""
Complete the child index computation in sift-down:

```dart
final left = %order% * i + 1;
final right = %order% + 1;
```
""", ["2", "left", "i", "right"], ["2", "left"]),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final pq = SplayTreeSet<(int, String)>((a, b) {
    final c = a.$1.compareTo(b.$1);
    return c != 0 ? c : a.$2.compareTo(b.$2);
  });
  pq
    ..add((3, 'c'))
    ..add((1, 'a'))
    ..add((2, 'b'));
  final first = pq.first;
  pq.remove(first);
  print('${first.$2} ${pq.first.$2}');
}
```
""", ["a b", "c b", "a c", "b a"], "a b"),

    mcq(r"""
Why include tie-breakers in a SplayTreeSet comparator used as a priority queue?
""", ["Otherwise items with equal priority are treated as duplicates and dropped",
       "For faster sorting", "To make it a max-heap", "It's not needed"],
        "Otherwise items with equal priority are treated as duplicates and dropped"),

    mcq(r"""
Which use case is NOT a good fit for a heap?
""", ["Iterating all items in sorted order repeatedly", "Getting the next scheduled event",
       "Finding the top 10 scores", "Dijkstra's algorithm"],
        "Iterating all items in sorted order repeatedly"),

    mcq(r"""
What does this print?

```dart
void main() {
  final heap = [1, 3, 2, 7, 4];
  var ok = true;
  for (var i = 1; i < heap.length; i++) {
    if (heap[(i - 1) ~/ 2] > heap[i]) ok = false;
  }
  print(ok);
}
```
""", ["true", "false", "1", "It throws an error"], "true"),

    mcq(r"""
Which typedef line gives a record type a readable name?
""", ["typedef Patient = ({String name, int urgency});", "class Patient = (String, int);",
       "record Patient(String name, int urgency);", "alias Patient = (String, int);"],
        "typedef Patient = ({String name, int urgency});"),

    mcq(r"""
Adding n items to a heap one at a time costs O(n log n). What does heapify cost to build a heap from n items already in an array?
""", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "O(n)"),
]
