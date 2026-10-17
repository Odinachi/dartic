NODE = r"""class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}
"""

QUESTIONS = [
    mcq(r"""
What does each node in a singly linked list hold?
""", ["A value and a reference to the next node", "A value and its index",
       "A value and references to the previous and next nodes", "Only a value"],
        "A value and a reference to the next node"),

    mcq(r"""
What does a singly linked list usually keep a reference to?
""", ["The head (first node)", "Every node in an array", "Only the middle node",
       "Nothing; it's stored in a Map"], "The head (first node)"),

    mcq(r"""
What is the `next` of the last node?
""", ["null", "The head", "Itself", "0"], "null"),

    mcq(r"""
What is the cost of accessing the i-th element of a singly linked list?
""", ["O(i)", "O(1)", "O(log n)", "O(n²)"], "O(i)"),

    mcq(r"""
What is the cost of inserting at the head of a singly linked list?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
Why is `addLast` O(1) in a list with a tail pointer?
""", ["We can link the new node directly after the known last node",
       "Linked lists are always O(1)", "The list is stored backwards",
       "Dart caches the last element automatically"],
        "We can link the new node directly after the known last node"),

    mcq(r"""
Even with a tail pointer, why is `removeLast` O(n) in a SINGLY linked list?
""", ["We must walk from the head to find the node before the tail",
       "Removing always shifts elements", "The tail is read-only",
       "It isn't; it's O(1)"],
        "We must walk from the head to find the node before the tail"),

    mcq(r"""
Which is a disadvantage of linked lists compared to arrays?
""", ["Poor cache locality and O(n) indexing", "O(n) insertion at the front",
       "They can't store objects", "They can't grow"],
        "Poor cache locality and O(n) indexing"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  final head = Node(1, Node(2, Node(3)));
  print(head.next?.next?.value);
}
```
""", ["3", "2", "null", "1"], "3"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  final head = Node(1, Node(2));
  print(head.next?.next?.value);
}
```
""", ["null", "2", "It throws an error", "0"], "null"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  final head = Node(5, Node(10, Node(15)));
  var sum = 0;
  Node<int>? n = head;
  while (n != null) {
    sum += n.value;
    n = n.next;
  }
  print(sum);
}
```
""", ["30", "15", "5", "0"], "30"),

    fill(r"""
Move the cursor forward:

```dart
""" + NODE + r"""
void main() {
  Node<int>? current = Node(1, Node(2));
  while (current != null) {
    print(current.value);
    current = current.%fill%;
  }
}
```
""", "next"),

    mcq(r"""
To insert node X after node B (B → C), which order is correct?
""", ["X.next = B.next; then B.next = X;", "B.next = X; then X.next = B.next;",
       "X.next = B; then B.next = C;", "C.next = X; then X.next = B;"],
        "X.next = B.next; then B.next = X;"),

    mcq(r"""
What goes wrong if you write `B.next = X;` and then `X.next = B.next;`?
""", ["X points to itself and the rest of the list is lost", "Nothing; both orders work",
       "B is deleted", "It throws a compile error"],
        "X points to itself and the rest of the list is lost"),

    mcq(r"""
How do you delete the node after `a` in a singly linked list?
""", ["a.next = a.next?.next;", "a.next = null;", "a = a.next;", "a.next.next = a;"],
        "a.next = a.next?.next;"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  final head = Node('A', Node('B', Node('C')));
  head.next = head.next?.next;
  final out = <String>[];
  for (Node<String>? n = head; n != null; n = n.next) {
    out.add(n.value);
  }
  print(out);
}
```
""", ["[A, C]", "[A, B, C]", "[B, C]", "[A]"], "[A, C]"),

    mcq(r"""
What happens to a node after nothing references it anymore?
""", ["The garbage collector can reclaim it", "It stays forever", "It throws an error",
       "It becomes the new head"], "The garbage collector can reclaim it"),

    order(r"""
Complete the iterative reverse:

```dart
Node<T>? reverse<T>(Node<T>? head) {
  Node<T>? prev;
  var current = head;
  while (current != null) {
    final next = current.%order%;
    current.next = %order%;
    prev = %order%;
    current = next;
  }
  return prev;
}
```
""", ["next", "prev", "current", "head", "null"], ["next", "prev", "current"]),

    mcq(r"""
In iterative reversal, what must you save BEFORE flipping `current.next`?
""", ["current.next (the rest of the list)", "The head's value", "The length",
       "Nothing"], "current.next (the rest of the list)"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
Node<T>? reverse<T>(Node<T>? head) {
  Node<T>? prev;
  var cur = head;
  while (cur != null) {
    final next = cur.next;
    cur.next = prev;
    prev = cur;
    cur = next;
  }
  return prev;
}

void main() {
  var h = reverse(Node(1, Node(2, Node(3))));
  final out = <int>[];
  for (; h != null; h = h.next) {
    out.add(h.value);
  }
  print(out);
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "[3]", "[]"], "[3, 2, 1]"),

    mcq(r"""
What is the space complexity of iterative linked-list reversal?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the space complexity of recursive linked-list reversal?
""", ["O(n) for the call stack", "O(1)", "O(log n)", "O(n²)"], "O(n) for the call stack"),

    mcq(r"""
After iterative reversal finishes, which variable holds the new head?
""", ["prev", "current", "next", "head"], "prev"),

    mcq(r"""
To find the middle node in one pass, how fast do the two pointers move?
""", ["Slow moves 1 step, fast moves 2 steps", "Both move 1 step",
       "Slow moves 2, fast moves 3", "Fast moves n steps at once"],
        "Slow moves 1 step, fast moves 2 steps"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
Node<T>? middle<T>(Node<T>? head) {
  var slow = head, fast = head;
  while (fast != null && fast.next != null) {
    slow = slow!.next;
    fast = fast.next!.next;
  }
  return slow;
}

void main() {
  print(middle(Node(1, Node(2, Node(3, Node(4, Node(5))))))?.value);
  print(middle(Node(1, Node(2)))?.value);
}
```
""", ["3 then 2", "3 then 1", "2 then 2", "5 then 2"], "3 then 2"),

    mcq(r"""
Which algorithm detects a cycle in a linked list using O(1) space?
""", ["Floyd's tortoise and hare (fast & slow pointers)", "Binary search",
       "Bubble sort", "Dijkstra's algorithm"],
        "Floyd's tortoise and hare (fast & slow pointers)"),

    mcq(r"""
In cycle detection, why compare nodes with `identical` rather than by value?
""", ["Different nodes can hold equal values", "Values can't be compared",
       "identical is faster than == for ints only", "Nodes don't have values"],
        "Different nodes can hold equal values"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
bool hasCycle<T>(Node<T>? head) {
  var slow = head, fast = head;
  while (fast != null && fast.next != null) {
    slow = slow!.next;
    fast = fast.next!.next;
    if (identical(slow, fast)) return true;
  }
  return false;
}

void main() {
  final a = Node(1), b = Node(2), c = Node(3);
  a.next = b;
  b.next = c;
  print(hasCycle(a));
  c.next = a;
  print(hasCycle(a));
}
```
""", ["false then true", "true then true", "false then false", "true then false"],
        "false then true"),

    mcq(r"""
What is an alternative cycle check that uses O(n) extra space?
""", ["Store visited nodes in a Set", "Sort the list", "Reverse the list twice",
       "Use binary search"], "Store visited nodes in a Set"),

    mcq(r"""
What is a dummy (sentinel) node used for?
""", ["Removing special cases when the head might change", "Storing the length",
       "Making the list circular", "Speeding up indexing"],
        "Removing special cases when the head might change"),

    mcq(r"""
In "remove the n-th node from the end", how far ahead does `fast` start (with a dummy)?
""", ["n + 1 steps", "n steps", "1 step", "n - 1 steps"], "n + 1 steps"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
Node<int>? removeNth(Node<int>? head, int n) {
  final dummy = Node(0, head);
  Node<int>? fast = dummy, slow = dummy;
  for (var i = 0; i <= n; i++) {
    fast = fast!.next;
  }
  while (fast != null) {
    fast = fast.next;
    slow = slow!.next;
  }
  slow!.next = slow.next?.next;
  return dummy.next;
}

void main() {
  var h = removeNth(Node(1, Node(2, Node(3))), 3);
  final out = <int>[];
  for (; h != null; h = h.next) {
    out.add(h.value);
  }
  print(out);
}
```
""", ["[2, 3]", "[1, 2]", "[1, 3]", "[1, 2, 3]"], "[2, 3]"),

    mcq(r"""
When removing the n-th node from the end, why use a dummy node before the head?

```dart
final dummy = Node(0, head);
// ... move pointers, then:
slow!.next = slow.next?.next;
return dummy.next;
```
""", ["So removing the head itself needs no special case", "Dart requires dummies",
       "To make the list circular", "To count the length"],
        "So removing the head itself needs no special case"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
Node<int>? merge(Node<int>? a, Node<int>? b) {
  final dummy = Node(0);
  var tail = dummy;
  while (a != null && b != null) {
    if (a.value <= b.value) {
      tail.next = a;
      a = a.next;
    } else {
      tail.next = b;
      b = b.next;
    }
    tail = tail.next!;
  }
  tail.next = a ?? b;
  return dummy.next;
}

void main() {
  var h = merge(Node(1, Node(5)), Node(2, Node(3, Node(9))));
  final out = <int>[];
  for (; h != null; h = h.next) {
    out.add(h.value);
  }
  print(out);
}
```
""", ["[1, 2, 3, 5, 9]", "[1, 5, 2, 3, 9]", "[1, 2, 5, 3, 9]", "[9, 5, 3, 2, 1]"],
        "[1, 2, 3, 5, 9]"),

    mcq(r"""
What is the extra space used when merging two sorted linked lists by relinking nodes?
""", ["O(1)", "O(n + m)", "O(log n)", "O(n × m)"], "O(1)"),

    fill(r"""
Attach whichever list still has nodes:

```dart
tail.next = a %fill% b;
```
""", "??"),

    mcq(r"""
What does extending `Iterable<T>` give a custom linked list?
""", ["map, where, contains, join and for-in support, once you provide an iterator",
       "O(1) indexing", "Automatic sorting", "Thread safety"],
        "map, where, contains, join and for-in support, once you provide an iterator"),

    fill(r"""
Which getter must an Iterable subclass implement?

```dart
class MyList<T> extends Iterable<T> {
  @override
  Iterator<T> get %fill% => throw UnimplementedError();
}
```
""", "iterator"),

    mcq(r"""
Which two members does an `Iterator<T>` provide?
""", ["current and moveNext()", "next and hasNext()", "first and last", "value and index"],
        "current and moveNext()"),

    mcq(r"""
What does `RangeError.checkValidIndex(index, this, 'index', length)` do?
""", ["Throws a RangeError if index is outside 0..length-1", "Returns -1 for bad indexes",
       "Clamps the index", "Sorts the list"],
        "Throws a RangeError if index is outside 0..length-1"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
Node<int>? dedupe(Node<int>? head) {
  var cur = head;
  while (cur != null && cur.next != null) {
    if (cur.value == cur.next!.value) {
      cur.next = cur.next!.next;
    } else {
      cur = cur.next;
    }
  }
  return head;
}

void main() {
  var h = dedupe(Node(1, Node(1, Node(1, Node(2)))));
  final out = <int>[];
  for (; h != null; h = h.next) {
    out.add(h.value);
  }
  print(out);
}
```
""", ["[1, 2]", "[1, 1, 2]", "[1]", "[2]"], "[1, 2]"),

    mcq(r"""
In `dedupe`, why don't we advance `cur` after removing a duplicate?
""", ["The new next node might also be a duplicate", "To avoid a null error",
       "Because the list is reversed", "It's a bug; we should advance"],
        "The new next node might also be a duplicate"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  Node<int>? head;
  for (final v in [1, 2, 3]) {
    head = Node(v, head);
  }
  final out = <int>[];
  for (var n = head; n != null; n = n.next) {
    out.add(n.value);
  }
  print(out);
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "[1]", "[3]"], "[3, 2, 1]"),

    mcq(r"""
Why does adding each value with `head = Node(v, head)` reverse the order?
""", ["Each new value becomes the new head, in front of the earlier ones",
       "Node's constructor sorts descending", "Dart iterates lists backwards",
       "It doesn't reverse the order"],
        "Each new value becomes the new head, in front of the earlier ones"),

    mcq(r"""
Which loop condition prevents a null error in fast/slow pointer loops?
""", ["fast != null && fast.next != null", "slow != null", "fast.next.next != null",
       "fast != slow"], "fast != null && fast.next != null"),

    mcq(r"""
When removing the last node of a list with a tail pointer, what must you also update?
""", ["tail (to the new last node)", "Nothing", "Every node's value", "The head's value"],
        "tail (to the new last node)"),

    mcq(r"""
What is the cost of this loop on a linked list of n nodes?

```dart
for (var i = 0; i < list.length; i++) {
  print(list.elementAtIndex(i));
}
```
""", ["O(n²)", "O(n)", "O(log n)", "O(1)"], "O(n²)"),

    mcq(r"""
What is the cost of iterating a linked list with for-in?
""", ["O(n)", "O(n²)", "O(log n)", "O(1)"], "O(n)"),

    mcq(r"""
Which application commonly uses linked lists for buckets?
""", ["Hash tables using separate chaining", "Binary search", "Merge sort's split step",
       "String interpolation"], "Hash tables using separate chaining"),

    mcq(r"""
Why can persistent (immutable) lists share tails safely?
""", ["Nodes never change, so multiple heads can point to the same tail",
       "Dart copies the tail each time", "They store everything in arrays",
       "They can't; it's unsafe"],
        "Nodes never change, so multiple heads can point to the same tail"),

    order(r"""
Complete `addFirst` for a list with head and tail:

```dart
void addFirst(T value) {
  head = Node(value, %order%);
  tail %order% head;
  _length%order%;
}
```
""", ["head", "??=", "++", "tail", "=", "--"], ["head", "??=", "++"]),

    mcq(r"""
In `addFirst`, why use `tail ??= head` instead of `tail = head`?
""", ["Only set tail when the list was empty; otherwise keep the existing tail",
       "??= is faster", "tail must always equal head", "To make tail nullable"],
        "Only set tail when the list was empty; otherwise keep the existing tail"),

    mcq(r"""
What error is thrown by `removeFirst()` on an empty list in the lesson's implementation?
""", ["StateError", "RangeError", "FormatException", "NoSuchMethodError"], "StateError"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int length(Node<int>? n) => n == null ? 0 : 1 + length(n.next);

void main() {
  print(length(Node(4, Node(5, Node(6, Node(7))))));
}
```
""", ["4", "3", "22", "0"], "4"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void main() {
  final a = Node(1);
  final x = Node(99);
  a.next = Node(2);
  x.next = a.next;
  a.next = x;
  print('${a.value} ${a.next!.value} ${a.next!.next!.value}');
}
```
""", ["1 99 2", "1 2 99", "99 1 2", "1 99 99"], "1 99 2"),

    mcq(r"""
Which data structure would you choose for a playlist where you frequently insert a song right after the current one?
""", ["A linked list (you hold the current node)", "A sorted array", "A Set",
       "A hash map keyed by index"], "A linked list (you hold the current node)"),

    mcq(r"""
Which data structure would you choose to jump directly to song #500 often?
""", ["An array (List)", "A singly linked list", "A stack", "A queue"],
        "An array (List)"),
]
