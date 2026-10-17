DNODE = r"""class DNode<T> {
  T value;
  DNode<T>? prev;
  DNode<T>? next;
  DNode(this.value);
}
"""

QUESTIONS = [
    mcq(r"""
What extra reference does a doubly linked node have compared to a singly linked node?
""", ["prev (a link to the previous node)", "index", "tail", "length"],
        "prev (a link to the previous node)"),

    mcq(r"""
What is the cost of removing a node you already hold a reference to in a doubly linked list?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
Why is removing a held node O(n) in a singly linked list but O(1) in a doubly linked one?
""", ["Singly lists must search for the predecessor; doubly lists have prev",
       "Doubly lists are stored in arrays", "Singly lists can't remove nodes",
       "Doubly lists skip the garbage collector"],
        "Singly lists must search for the predecessor; doubly lists have prev"),

    mcq(r"""
What is the cost of `removeLast` in a doubly linked list with a tail pointer?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What's the main cost of a doubly linked list compared to a singly linked one?
""", ["One extra reference per node and more links to keep in sync",
       "O(n) insertion at the head", "No backward traversal", "It can't store generics"],
        "One extra reference per node and more links to keep in sync"),

    mcq(r"""
How many links are set when inserting a node between two existing nodes in a doubly linked list?
""", ["4", "2", "1", "3"], "4"),

    mcq(r"""
How many neighbor links must be fixed when unlinking a node from a doubly linked list?
""", ["2", "4", "1", "0"], "2"),

    order(r"""
Complete `unlink`:

```dart
void unlink(DNode<int> node) {
  node.prev!.%order% = node.next;
  node.next!.%order% = node.prev;
}
```
""", ["next", "prev", "value", "head"], ["next", "prev"]),

    mcq(r"""
What does this print?

```dart
""" + DNODE + r"""
void main() {
  final a = DNode(1), b = DNode(2), c = DNode(3);
  a.next = b;
  b.prev = a;
  b.next = c;
  c.prev = b;
  print(c.prev?.prev?.value);
}
```
""", ["1", "2", "3", "null"], "1"),

    mcq(r"""
What does this print?

```dart
""" + DNODE + r"""
void main() {
  final a = DNode(1), b = DNode(2);
  a.next = b;
  print(b.prev?.value);
}
```
""", ["null", "1", "2", "It throws an error"], "null"),

    mcq(r"""
What's the bug here?

```dart
""" + DNODE + r"""
void main() {
  final a = DNode(1), b = DNode(2);
  a.next = b;
  print(b.prev?.value); // null
}
```
""", ["b.prev was never set, so the backward link is missing", "a.next should be null",
       "DNode can't hold ints", "There is no bug"],
        "b.prev was never set, so the backward link is missing"),

    mcq(r"""
What is a sentinel node in a doubly linked list?
""", ["A permanent dummy head or tail that removes edge cases",
       "The node with the smallest value", "A node that stores the length",
       "A node that is always null"],
        "A permanent dummy head or tail that removes edge cases"),

    mcq(r"""
In a list with head and tail sentinels, what does an empty list look like?
""", ["head.next == tail and tail.prev == head", "head == null", "tail.next == head",
       "head.prev == tail"], "head.next == tail and tail.prev == head"),

    mcq(r"""
Why can sentinel-based code use `node.prev!` safely for real nodes?
""", ["Every real node always has a neighbor (possibly a sentinel) on both sides",
       "The ! operator ignores null", "prev is never used", "Dart initializes prev to the head"],
        "Every real node always has a neighbor (possibly a sentinel) on both sides"),

    mcq(r"""
What does this print?

```dart
""" + DNODE + r"""
void main() {
  final a = DNode('A'), b = DNode('B'), c = DNode('C');
  a.next = b; b.prev = a;
  b.next = c; c.prev = b;

  b.prev!.next = b.next;
  b.next!.prev = b.prev;

  print('${a.next!.value} ${c.prev!.value}');
}
```
""", ["C A", "B B", "A C", "C C"], "C A"),

    mcq(r"""
Which real-world feature naturally uses a doubly linked structure?
""", ["Browser back/forward history", "A dictionary lookup", "Binary search",
       "Counting words"], "Browser back/forward history"),

    mcq(r"""
In the browser history example, what happens to forward history when you visit a new page?
""", ["It's replaced (dropped)", "It's kept and merged", "It's moved to back history",
       "It throws an error"], "It's replaced (dropped)"),

    mcq(r"""
What does this print?

```dart
class Page {
  final String url;
  Page? back, forward;
  Page(this.url);
}

void main() {
  var cur = Page('a');
  for (final u in ['b', 'c']) {
    final p = Page(u)..back = cur;
    cur.forward = p;
    cur = p;
  }
  cur = cur.back!;
  print(cur.url);
  print(cur.forward!.url);
}
```
""", ["b then c", "a then b", "c then c", "b then a"], "b then c"),

    mcq(r"""
In a circular linked list, what does the last node's `next` point to?
""", ["The first node", "null", "Itself always", "The middle node"], "The first node"),

    mcq(r"""
Why do circular lists often store only a tail reference?
""", ["tail.next is the head, so both ends are reachable in O(1)",
       "The head can't be stored", "Tails are faster to read",
       "Circular lists have no head"],
        "tail.next is the head, so both ends are reachable in O(1)"),

    mcq(r"""
What happens if you traverse a circular list with `while (node != null)`?
""", ["It loops forever", "It visits each node once", "It throws an error", "It stops at the tail"],
        "It loops forever"),

    mcq(r"""
How should a traversal of a circular list stop?
""", ["When it returns to the starting node (compare by identity)",
       "When node == null", "After 100 steps", "When the value is 0"],
        "When it returns to the starting node (compare by identity)"),

    fill(r"""
Loop that runs at least once, then checks the condition:

```dart
void main() {
  var i = 10;
  %fill% {
    print(i);
    i++;
  } while (i < 3);
}
```
""", "do"),

    mcq(r"""
What does this print?

```dart
void main() {
  var i = 10;
  do {
    print(i);
    i++;
  } while (i < 3);
}
```
""", ["10", "Nothing", "10 11 12", "0 1 2"], "10"),

    mcq(r"""
What does `late CNode<T> next;` allow?
""", ["Assigning the non-nullable field later, e.g. in the constructor body",
       "Making next nullable", "Making next constant", "Lazy deletion"],
        "Assigning the non-nullable field later, e.g. in the constructor body"),

    mcq(r"""
In a circular list with a tail reference, how do you "rotate" so the head moves to the back?
""", ["tail = tail.next", "head = null", "tail = tail.prev", "Reverse the list"],
        "tail = tail.next"),

    mcq(r"""
What does this print?

```dart
class C {
  final int v;
  late C next;
  C(this.v);
}

void main() {
  final a = C(1), b = C(2), c = C(3);
  a.next = b;
  b.next = c;
  c.next = a;
  var n = a;
  for (var i = 0; i < 5; i++) {
    n = n.next;
  }
  print(n.v);
}
```
""", ["3", "1", "2", "It throws an error"], "3"),

    mcq(r"""
Which classic problem is naturally solved with a circular linked list?
""", ["The Josephus problem", "Binary search", "Matrix multiplication", "Prefix sums"],
        "The Josephus problem"),

    mcq(r"""
What does this print?

```dart
class N {
  final int id;
  late N next;
  N(this.id);
}

int josephus(int n, int k) {
  final first = N(1);
  var prev = first;
  for (var i = 2; i <= n; i++) {
    final node = N(i);
    prev.next = node;
    prev = node;
  }
  prev.next = first;
  var cur = prev;
  while (!identical(cur.next, cur)) {
    for (var i = 1; i < k; i++) {
      cur = cur.next;
    }
    cur.next = cur.next.next;
  }
  return cur.id;
}

void main() {
  print(josephus(4, 2));
}
```
""", ["1", "2", "3", "4"], "1"),

    mcq(r"""
Which scheduling strategy maps naturally onto a circular list?
""", ["Round-robin", "Shortest job first", "Priority scheduling", "First-fit"],
        "Round-robin"),

    mcq(r"""
Which library provides Dart's `LinkedList` class?
""", ["dart:collection", "dart:core", "dart:async", "dart:math"], "dart:collection"),

    mcq(r"""
What must elements of a Dart `LinkedList<E>` extend?
""", ["LinkedListEntry<E>", "Comparable<E>", "Iterable<E>", "Object only"],
        "LinkedListEntry<E>"),

    fill(r"""
Declare an entry class for Dart's LinkedList (Dart 3):

```dart
import 'dart:collection';

%fill% class Task extends LinkedListEntry<Task> {
  final String name;
  Task(this.name);
}
```
""", "final"),

    mcq(r"""
Why must subclasses of `LinkedListEntry` be `final`, `base` or `sealed` in Dart 3?
""", ["LinkedListEntry is declared as a base class", "It's a style rule only",
       "Because it's abstract", "Because entries are immutable"],
        "LinkedListEntry is declared as a base class"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

final class S extends LinkedListEntry<S> {
  final String t;
  S(this.t);
  @override
  String toString() => t;
}

void main() {
  final list = LinkedList<S>();
  final a = S('a'), c = S('c');
  list
    ..add(a)
    ..add(c);
  a.insertAfter(S('b'));
  print(list.toList());
}
```
""", ["[a, b, c]", "[a, c, b]", "[b, a, c]", "[a, c]"], "[a, b, c]"),

    mcq(r"""
What does `entry.unlink()` do?
""", ["Removes the entry from its LinkedList in O(1)", "Deletes the whole list",
       "Moves the entry to the end", "Clears the entry's value"],
        "Removes the entry from its LinkedList in O(1)"),

    mcq(r"""
What happens if you add a `LinkedListEntry` that's already in one LinkedList to another?
""", ["It throws a StateError", "It's moved automatically", "It's copied",
       "Both lists share it"], "It throws a StateError"),

    mcq(r"""
Why can an entry only be in one `LinkedList` at a time?
""", ["Its next/previous links are stored inside the entry itself (intrusive list)",
       "Dart limits object references", "LinkedList copies entries",
       "Entries are immutable"],
        "Its next/previous links are stored inside the entry itself (intrusive list)"),

    mcq(r"""
Which Dart class is a doubly linked queue that accepts ANY element type?
""", ["DoubleLinkedQueue", "LinkedList", "SplayTreeSet", "HashSet"], "DoubleLinkedQueue"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = DoubleLinkedQueue<int>.from([1, 2, 3]);
  q.firstEntry()!.nextEntry()!.remove();
  print(q.toList());
}
```
""", ["[1, 3]", "[2, 3]", "[1, 2]", "[1, 2, 3]"], "[1, 3]"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = DoubleLinkedQueue<String>.from(['x', 'z']);
  q.firstEntry()!.append('y');
  print(q.toList());
}
```
""", ["[x, y, z]", "[y, x, z]", "[x, z, y]", "[x, z]"], "[x, y, z]"),

    mcq(r"""
What is the default implementation behind Dart's `Queue()` constructor?
""", ["ListQueue (a circular array)", "DoubleLinkedQueue", "LinkedList", "SplayTreeMap"],
        "ListQueue (a circular array)"),

    mcq(r"""
Why does the lesson's `unlink` set `node.prev = node.next = null` at the end?
""", ["To avoid stale references that keep other nodes alive or cause bugs",
       "Because Dart requires it", "To make the list circular", "To sort the list"],
        "To avoid stale references that keep other nodes alive or cause bugs"),

    mcq(r"""
What does this print?

```dart
void main() {
  int? a, b;
  a = b = 5;
  print('$a $b');
}
```
""", ["5 5", "null 5", "5 null", "It doesn't compile"], "5 5"),

    mcq(r"""
Which structure combination powers an O(1) LRU cache?
""", ["Hash map + doubly linked list", "Array + binary search", "Two stacks",
       "Set + queue"], "Hash map + doubly linked list"),

    mcq(r"""
In an LRU cache, what operation does the doubly linked list make O(1)?
""", ["Moving an accessed item to the front", "Finding an item by key",
       "Sorting items by key", "Counting items"], "Moving an accessed item to the front"),

    mcq(r"""
What does this print?

```dart
""" + DNODE + r"""
void main() {
  final a = DNode(1), b = DNode(2), c = DNode(3);
  a.next = b; b.prev = a;
  b.next = c; c.prev = b;
  final out = <int>[];
  for (DNode<int>? n = c; n != null; n = n.prev) {
    out.add(n.value);
  }
  print(out);
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "[3]", "[]"], "[3, 2, 1]"),

    mcq(r"""
Which traversal is only possible in a doubly linked list?
""", ["Walking backward from the tail", "Walking forward from the head",
       "Counting nodes", "Finding the maximum"], "Walking backward from the tail"),

    order(r"""
Insert `node` between `before` and `after`:

```dart
node.prev = %order%;
node.next = %order%;
before.next = %order%;
after.prev = node;
```
""", ["before", "after", "node", "null", "head"], ["before", "after", "node"]),

    mcq(r"""
In the sentinel-based list, what does `addFirst` call?
""", ["_insertBetween(value, _head, _head.next!)", "_insertBetween(value, _tail, _head)",
       "_insertBetween(value, _tail.prev!, _tail)", "unlink(_head)"],
        "_insertBetween(value, _head, _head.next!)"),

    mcq(r"""
In the sentinel-based list, what does `addLast` call?
""", ["_insertBetween(value, _tail.prev!, _tail)", "_insertBetween(value, _head, _head.next!)",
       "_insertBetween(value, _tail, _head)", "unlink(_tail)"],
        "_insertBetween(value, _tail.prev!, _tail)"),

    mcq(r"""
Why do the lesson's insert methods return the new node?
""", ["So callers can later remove it in O(1) without searching",
       "Because Dart functions must return something", "To print it",
       "To make the list immutable"],
        "So callers can later remove it in O(1) without searching"),

    mcq(r"""
A text editor stores characters in a doubly linked list with a cursor node. Which operation is O(1)?
""", ["Inserting a character at the cursor", "Jumping to the 10,000th character",
       "Sorting the text", "Counting words"], "Inserting a character at the cursor"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = DoubleLinkedQueue<int>();
  q.addLast(2);
  q.addFirst(1);
  q.addLast(3);
  print(q.removeLast());
  print(q);
}
```
""", ["3 then {1, 2}", "1 then {2, 3}", "3 then [1, 2]", "2 then {1, 3}"], "3 then {1, 2}"),

    mcq(r"""
Which statement about memory is true?
""", ["Doubly linked nodes use more memory than singly linked ones",
       "Doubly linked nodes use less memory", "They use the same memory",
       "Linked lists use less memory than arrays for ints"],
        "Doubly linked nodes use more memory than singly linked ones"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

final class E extends LinkedListEntry<E> {
  final int v;
  E(this.v);
}

void main() {
  final list = LinkedList<E>();
  final e1 = E(1), e2 = E(2), e3 = E(3);
  list.addAll([e1, e2, e3]);
  e2.unlink();
  print(list.length);
  print(e1.next?.v);
}
```
""", ["2 then 3", "3 then 2", "2 then 2", "2 then null"], "2 then 3"),
]
