QUESTIONS = [
    mcq(r"""
What ordering rule does a queue follow?
""", ["FIFO: first in, first out", "LIFO: last in, first out", "Sorted order", "Random order"],
        "FIFO: first in, first out"),

    mcq(r"""
What is a deque?
""", ["A double-ended queue: add and remove at both ends", "A queue that can't be emptied",
       "A sorted queue", "A queue of queues"],
        "A double-ended queue: add and remove at both ends"),

    mcq(r"""
Why is `List.removeAt(0)` a poor way to dequeue?
""", ["It's O(n) because every remaining element shifts", "It removes the last element",
       "It doesn't exist", "It throws on non-empty lists"],
        "It's O(n) because every remaining element shifts"),

    mcq(r"""
What is the total cost of draining n items from a List using `removeAt(0)`?
""", ["O(n²)", "O(n)", "O(n log n)", "O(1)"], "O(n²)"),

    mcq(r"""
Which library provides Dart's `Queue`?
""", ["dart:collection", "dart:core", "dart:async", "dart:io"], "dart:collection"),

    mcq(r"""
What is the default implementation created by `Queue()`?
""", ["ListQueue", "DoubleLinkedQueue", "LinkedList", "SplayTreeSet"], "ListQueue"),

    mcq(r"""
How is `ListQueue` implemented?
""", ["As a circular buffer (array)", "As a linked list", "As a binary heap",
       "As a hash table"], "As a circular buffer (array)"),

    mcq(r"""
What is the cost of `addLast` and `removeFirst` on a `ListQueue`?
""", ["O(1) amortized", "O(n)", "O(log n)", "O(n²)"], "O(1) amortized"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>();
  q.addLast(1);
  q.addLast(2);
  q.addLast(3);
  print(q.removeFirst());
  print(q);
}
```
""", ["1 then {2, 3}", "3 then {1, 2}", "1 then [2, 3]", "3 then [1, 2]"], "1 then {2, 3}"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<String>.from(['b', 'c']);
  q.addFirst('a');
  q.addLast('d');
  q.removeLast();
  print(q.toList());
}
```
""", ["[a, b, c]", "[b, c, d]", "[a, b, c, d]", "[a, c, d]"], "[a, b, c]"),

    fill(r"""
Peek at the front of the queue without removing it:

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>.from([7, 8, 9]);
  print(q.%fill%); // 7
}
```
""", "first"),

    fill(r"""
Dequeue from the front:

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>.from([7, 8, 9]);
  print(q.%fill%()); // 7
}
```
""", "removeFirst"),

    mcq(r"""
What happens when calling `removeFirst()` on an empty `Queue`?
""", ["It throws a StateError", "It returns null", "It returns 0", "Nothing"],
        "It throws a StateError"),

    mcq(r"""
Does `Queue` support `q[2]` indexing?
""", ["No, Queue has no [] operator", "Yes, in O(1)", "Yes, but it returns null",
       "Only for ListQueue"], "No, Queue has no [] operator"),

    mcq(r"""
In a circular buffer, how is an index wrapped back to the start?
""", ["Using the modulo operator: index % capacity", "By sorting the buffer",
       "By reversing the buffer", "By creating a new buffer every time"],
        "Using the modulo operator: index % capacity"),

    mcq(r"""
What does this print?

```dart
void main() {
  const capacity = 4;
  final head = 3;
  print((head + 2) % capacity);
}
```
""", ["1", "5", "2", "3"], "1"),

    mcq(r"""
In a circular buffer queue, where is the next free slot for enqueue?
""", ["(head + length) % capacity", "head - 1", "length", "capacity - 1"],
        "(head + length) % capacity"),

    mcq(r"""
What happens to `head` when you dequeue from a circular buffer?
""", ["It moves forward one position, wrapping around", "It stays the same and elements shift",
       "It resets to 0", "It moves backward"],
        "It moves forward one position, wrapping around"),

    mcq(r"""
When a circular buffer is full and grows, how are elements copied?
""", ["In queue order (front to back) into the new buffer starting at index 0",
       "In raw index order", "In reverse order", "Only the newest element is kept"],
        "In queue order (front to back) into the new buffer starting at index 0"),

    order(r"""
Complete the circular enqueue:

```dart
void enqueue(T value) {
  if (_length == _buf.length) _grow();
  final tail = (_head %order% _length) %order% _buf.length;
  _buf[tail] = value;
  _length%order%;
}
```
""", ["+", "%", "++", "-", "~/", "--"], ["+", "%", "++"]),

    mcq(r"""
Why does the lesson's `dequeue` set the old slot to null?
""", ["So the buffer doesn't keep removed objects alive", "To mark the queue as full",
       "Because Dart requires it", "To sort the buffer"],
        "So the buffer doesn't keep removed objects alive"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final recent = Queue<int>();
  for (var i = 1; i <= 5; i++) {
    if (recent.length == 3) recent.removeFirst();
    recent.addLast(i);
  }
  print(recent.toList());
}
```
""", ["[3, 4, 5]", "[1, 2, 3]", "[1, 2, 3, 4, 5]", "[5, 4, 3]"], "[3, 4, 5]"),

    mcq(r"""
Which use case suits a bounded queue that drops the oldest item when full?
""", ["\"Recently viewed\" items or the last N log lines", "Shortest paths in a weighted graph",
       "Checking balanced brackets", "Sorting a list"],
        "\"Recently viewed\" items or the last N log lines"),

    mcq(r"""
In round-robin scheduling, what happens to a job that isn't finished after its time slice?
""", ["It goes to the back of the queue", "It's discarded", "It goes to the front",
       "It runs until finished"], "It goes to the back of the queue"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<String>.from(['A', 'B', 'C']);
  for (var i = 0; i < 4; i++) {
    q.addLast(q.removeFirst());
  }
  print(q.first);
}
```
""", ["B", "A", "C", "D"], "B"),

    mcq(r"""
Which graph/tree algorithm is driven by a queue?
""", ["Breadth-first search (BFS)", "Depth-first search (DFS)", "Binary search",
       "Quick sort"], "Breadth-first search (BFS)"),

    mcq(r"""
Why does BFS on an unweighted grid find the shortest path?
""", ["It processes all cells at distance d before any at distance d + 1",
       "It always moves right first", "It sorts the cells by distance",
       "It uses recursion"],
        "It processes all cells at distance d before any at distance d + 1"),

    mcq(r"""
What happens if you replace BFS's queue with a stack?
""", ["It becomes depth-first search and no longer guarantees shortest paths",
       "It becomes faster and still finds shortest paths", "It stops working entirely",
       "Nothing changes"],
        "It becomes depth-first search and no longer guarantees shortest paths"),

    mcq(r"""
When should a BFS mark a cell as seen?
""", ["When it is enqueued", "When it is dequeued", "Never", "After the search finishes"],
        "When it is enqueued"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': <String>[],
  };
  final q = Queue<String>.from(['A']);
  final seen = {'A'};
  final order = <String>[];
  while (q.isNotEmpty) {
    final n = q.removeFirst();
    order.add(n);
    for (final m in graph[n]!) {
      if (seen.add(m)) q.addLast(m);
    }
  }
  print(order.join());
}
```
""", ["ABCD", "ABDC", "ACBD", "ADBC"], "ABCD"),

    mcq(r"""
What does this print?

```dart
void main() {
  final ((r, c), d) = ((2, 3), 7);
  print(r + c + d);
}
```
""", ["12", "7", "5", "It doesn't compile"], "12"),

    mcq(r"""
In sliding-window maximum, what does the front of the monotonic deque hold?
""", ["The index of the largest value in the current window", "The oldest index ever seen",
       "The smallest value", "The window size"],
        "The index of the largest value in the current window"),

    mcq(r"""
In sliding-window maximum, why remove smaller values from the BACK when a new value arrives?
""", ["They can never be the maximum while the new, larger value is in the window",
       "To keep the deque sorted ascending", "To save memory only", "They are duplicates"],
        "They can never be the maximum while the new, larger value is in the window"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

List<int> windowMax(List<int> a, int k) {
  final dq = ListQueue<int>();
  final res = <int>[];
  for (var i = 0; i < a.length; i++) {
    if (dq.isNotEmpty && dq.first <= i - k) dq.removeFirst();
    while (dq.isNotEmpty && a[dq.last] <= a[i]) {
      dq.removeLast();
    }
    dq.addLast(i);
    if (i >= k - 1) res.add(a[dq.first]);
  }
  return res;
}

void main() {
  print(windowMax([4, 2, 12, 3, 1], 2));
}
```
""", ["[4, 12, 12, 3]", "[4, 2, 12, 3]", "[12, 12, 12, 3]", "[2, 12, 3, 1]"],
        "[4, 12, 12, 3]"),

    mcq(r"""
What is the complexity of sliding-window maximum with a monotonic deque?
""", ["O(n)", "O(n × k)", "O(n log n)", "O(k²)"], "O(n)"),

    mcq(r"""
How can two stacks implement a queue?
""", ["Push to an inbox; when the outbox is empty, pour the inbox into it and pop from it",
       "Push to both and pop from either", "Sort both stacks after every push",
       "It's impossible"],
        "Push to an inbox; when the outbox is empty, pour the inbox into it and pop from it"),

    mcq(r"""
What is the amortized cost of dequeue in the two-stack queue?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final inbox = <int>[1, 2, 3];
  final outbox = <int>[];
  while (inbox.isNotEmpty) {
    outbox.add(inbox.removeLast());
  }
  print(outbox.removeLast());
}
```
""", ["1", "3", "2", "It throws an error"], "1"),

    mcq(r"""
Why must the two-stack queue only pour when the outbox is empty?
""", ["Pouring onto a non-empty outbox would put newer items before older ones",
       "Pouring is O(1) only when empty", "Lists can't be appended to",
       "It doesn't matter when you pour"],
        "Pouring onto a non-empty outbox would put newer items before older ones"),

    mcq(r"""
Which structure should you use to always process the MOST URGENT task, not the oldest?
""", ["A priority queue (heap)", "A Queue", "A stack", "A Set"], "A priority queue (heap)"),

    mcq(r"""
Which Dart queue lets you remove a known entry in O(1)?
""", ["DoubleLinkedQueue", "ListQueue", "List", "Set"], "DoubleLinkedQueue"),

    fill(r"""
Create a queue with an initial capacity hint:

```dart
import 'dart:collection';

void main() {
  final q = %fill%<int>(1000);
  q.add(1);
  print(q.length);
}
```
""", "ListQueue"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

class RecentCounter {
  final _t = Queue<int>();
  int ping(int t) {
    _t.addLast(t);
    while (_t.first < t - 3000) {
      _t.removeFirst();
    }
    return _t.length;
  }
}

void main() {
  final rc = RecentCounter();
  rc.ping(1);
  rc.ping(2000);
  print(rc.ping(5000));
}
```
""", ["2", "3", "1", "0"], "2"),

    mcq(r"""
What happens when you add or remove items from a Queue inside a for-in loop over that same queue?
""", ["It throws a ConcurrentModificationError", "It works normally",
       "Items are skipped silently", "The loop restarts"],
        "It throws a ConcurrentModificationError"),

    mcq(r"""
What's the safe way to process every item in a queue, including newly added ones?
""", ["while (q.isNotEmpty) { final x = q.removeFirst(); ... }", "for (final x in q) { q.add(...); }",
       "q.forEach((x) => q.add(x))", "q.toList().forEach(q.removeFirst)"],
        "while (q.isNotEmpty) { final x = q.removeFirst(); ... }"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final players = Queue<String>.from(['A', 'B', 'C', 'D']);
  while (players.length > 1) {
    players.addLast(players.removeFirst());
    players.removeFirst();
  }
  print(players.first);
}
```
""", ["A", "B", "C", "D"], "A"),

    mcq(r"""
What does `Queue.toString()` print for a queue of 1, 2, 3?
""", ["{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)", "Queue(1, 2, 3)"], "{1, 2, 3}"),

    mcq(r"""
Which async Dart tool is the natural fit for producer/consumer event queues?
""", ["Stream / StreamController", "SplayTreeMap", "StringBuffer", "Records"],
        "Stream / StreamController"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final dq = Queue<int>();
  dq.addFirst(2);
  dq.addFirst(1);
  dq.addLast(3);
  print('${dq.first} ${dq.last}');
}
```
""", ["1 3", "2 3", "3 1", "1 2"], "1 3"),

    mcq(r"""
Checking if a word is a palindrome with a deque means repeatedly:
""", ["Comparing and removing the first and last characters", "Sorting the characters",
       "Pushing all characters and popping half", "Hashing the word"],
        "Comparing and removing the first and last characters"),

    order(r"""
Complete the BFS loop skeleton:

```dart
while (queue.%order%) {
  final node = queue.%order%();
  for (final next in neighbors(node)) {
    if (seen.%order%(next)) queue.addLast(next);
  }
}
```
""", ["isNotEmpty", "removeFirst", "add", "removeLast", "isEmpty", "contains"],
        ["isNotEmpty", "removeFirst", "add"]),

    mcq(r"""
In a BFS loop, why does `if (seen.add(next)) queue.addLast(next);` only enqueue unvisited nodes?
""", ["Set.add returns true only if the item wasn't already present",
       "Set.add always returns true", "It sorts the set", "It removes duplicates from the queue"],
        "Set.add returns true only if the item wasn't already present"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>.from([5, 6, 7]);
  var sum = 0;
  while (q.isNotEmpty) {
    sum += q.removeFirst();
  }
  print('$sum ${q.isEmpty}');
}
```
""", ["18 true", "18 false", "0 true", "7 true"], "18 true"),

    mcq(r"""
Which is FIFO?
""", ["A checkout line", "A stack of plates", "Undo history", "The call stack"],
        "A checkout line"),

    mcq(r"""
In a grid BFS, what does a `seen` set of visited cells prevent?
""", ["Revisiting cells and looping forever", "Moving diagonally", "Reaching the goal",
       "Using records"], "Revisiting cells and looping forever"),
]
