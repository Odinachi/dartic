# Singly Linked Lists

Imagine a **treasure hunt** 🗺️.

- You start with **one clue** in your hand.
- Each clue tells you something (the treasure!) **and where to find the next clue**.
- The last clue says *"The End"*. 🏁

You can't jump straight to clue #7. You have to follow clue 1 → 2 → 3... But adding a new clue in the middle is easy: just change **one** "next location" note.

👉 That's a **singly linked list**:

> A **singly linked list** is a chain of **nodes**. Each node holds a **value** and a **reference to the next node**. The list only remembers the first node, called the **head**.

Unlike an array, the nodes are **scattered** around memory, connected only by references.

---

## 🆚 Linked List vs Array (List)

| Operation | Array (`List`) | Singly linked list |
|-----------|----------------|--------------------|
| Access by index `i` | **O(1)** ⚡ | O(i) 🐢 (walk from head) |
| Insert/remove at the **front** | O(n) 🐢 (shift) | **O(1)** ⚡ |
| Insert/remove **after a known node** | O(n) (shift) | **O(1)** ⚡ |
| Insert at the **end** | O(1) amortized | O(n), or **O(1)** with a tail pointer |
| Search for a value | O(n) | O(n) |
| Memory per element | Just the value | Value **+ a reference** |
| Cache friendliness | Excellent (contiguous) | Poor (scattered) |

> 💡 Linked lists win when you **insert and remove at the front or around nodes you already hold**. Arrays win at **random access** and raw speed.

---

## 🧱 The Node

```dart
class Node<T> {
  T value;
  Node<T>? next; // null means "end of the list"

  Node(this.value, [this.next]);

  @override
  String toString() => 'Node($value)';
}

void main() {
  // Build 1 → 2 → 3 by hand
  final third = Node(3);
  final second = Node(2, third);
  final head = Node(1, second);

  print(head);            // Node(1)
  print(head.next);       // Node(2)
  print(head.next?.next); // Node(3)
  print(third.next);      // null
}
```

**🔍 What This Code Does:**

1. **Generic Node**: `Node<T>` can hold any type of value.
2. **Nullable `next`**: `Node<T>? next` is `null` for the last node.
3. **Optional Positional Parameter**: `[this.next]` lets us create a node with or without a successor.
4. **Manual Chain**: `head → second → third → null`.
5. **Null-Aware Access**: `head.next?.next` safely follows two links.

```text
head
 │
 ▼
┌───┬───┐   ┌───┬───┐   ┌───┬──────┐
│ 1 │ ●─┼──▶│ 2 │ ●─┼──▶│ 3 │ null │
└───┴───┘   └───┴───┘   └───┴──────┘
```

---

## 🚶 Traversal: Walking the Chain

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

void main() {
  final head = Node(10, Node(20, Node(30, Node(40))));

  // Print every value
  Node<int>? current = head;
  while (current != null) {
    print(current.value);
    current = current.next;
  }

  // Count nodes
  var count = 0;
  for (Node<int>? n = head; n != null; n = n.next) {
    count++;
  }
  print('Length: $count'); // 4
}
```

**🔍 What This Code Does:**

1. **Cursor Variable**: `current` starts at the head and moves forward with `current = current.next`.
2. **Stop at null**: The loop ends after the last node.
3. **Type Promotion**: Inside `while (current != null)`, Dart knows `current` isn't null.
4. **for-loop Form**: The same walk written as a `for` with the node as the loop variable.
5. **O(n)**: Every node is visited once.

---

## 🏗️ Building a Complete `LinkedList<T>`

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

class SinglyLinkedList<T> extends Iterable<T> {
  Node<T>? head;
  Node<T>? tail;
  int _length = 0;

  @override
  int get length => _length;

  @override
  bool get isEmpty => _length == 0;

  // O(1): new node becomes the head
  void addFirst(T value) {
    head = Node(value, head);
    tail ??= head;
    _length++;
  }

  // O(1) thanks to the tail pointer
  void addLast(T value) {
    final node = Node(value);
    if (tail == null) {
      head = tail = node;
    } else {
      tail!.next = node;
      tail = node;
    }
    _length++;
  }

  // O(1)
  T removeFirst() {
    final h = head;
    if (h == null) throw StateError('List is empty');
    head = h.next;
    if (head == null) tail = null;
    _length--;
    return h.value;
  }

  // O(i): walk to the node before the position
  void insertAt(int index, T value) {
    RangeError.checkValueInInterval(index, 0, _length, 'index');
    if (index == 0) return addFirst(value);
    if (index == _length) return addLast(value);
    final prev = _nodeAt(index - 1);
    prev.next = Node(value, prev.next);
    _length++;
  }

  // O(n): find the node before the match, then bypass it
  bool remove(T value) {
    if (head == null) return false;
    if (head!.value == value) {
      removeFirst();
      return true;
    }
    var prev = head!;
    while (prev.next != null) {
      if (prev.next!.value == value) {
        if (prev.next == tail) tail = prev;
        prev.next = prev.next!.next; // skip over the removed node
        _length--;
        return true;
      }
      prev = prev.next!;
    }
    return false;
  }

  // O(i)
  T elementAtIndex(int index) => _nodeAt(index).value;

  Node<T> _nodeAt(int index) {
    RangeError.checkValidIndex(index, this, 'index', _length);
    var node = head!;
    for (var i = 0; i < index; i++) {
      node = node.next!;
    }
    return node;
  }

  @override
  Iterator<T> get iterator => _NodeIterator(head);

  @override
  String toString() => isEmpty ? '(empty)' : '${join(' → ')} → null';
}

class _NodeIterator<T> implements Iterator<T> {
  Node<T>? _next;
  T? _current;
  _NodeIterator(this._next);

  @override
  T get current => _current as T;

  @override
  bool moveNext() {
    final n = _next;
    if (n == null) return false;
    _current = n.value;
    _next = n.next;
    return true;
  }
}

void main() {
  final list = SinglyLinkedList<String>();
  list.addLast('B');
  list.addLast('C');
  list.addFirst('A');
  list.insertAt(3, 'D');
  print(list);          // A → B → C → D → null
  print(list.length);   // 4

  list.remove('C');
  print(list);          // A → B → D → null

  print(list.removeFirst()); // A
  print(list.elementAtIndex(1)); // D

  // Because it's an Iterable, all the usual methods work:
  print(list.map((s) => s.toLowerCase()).toList()); // [b, d]
  print(list.contains('B')); // true
  for (final s in list) {
    print('item: $s');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **a full singly linked list with head and tail pointers**:

1. **`addFirst`**: The new node points to the old head and becomes the new head. O(1).

2. **`addLast` With a Tail**: Without `tail` we'd walk the whole list (O(n)); keeping a reference to the last node makes it O(1).

3. **`removeFirst`**: Move `head` to `head.next`. If the list becomes empty, clear `tail` too.

4. **`insertAt`**: Walk to the node **before** the position, then splice in the new node: `prev.next = Node(value, prev.next)`.

5. **`remove(value)`**: Find the node **before** the match and make it skip over the match. Update `tail` if we removed the last node.

6. **Extending `Iterable<T>`**: By providing an `iterator`, we get `map`, `where`, `contains`, `join`, for-in loops and more for free.

7. **Bounds Checks**: `RangeError.checkValidIndex` and `checkValueInInterval` throw helpful errors for bad indexes.

---

## ✂️ Insert and Delete: Just Rewire References

The heart of linked lists is changing **one or two references**. Nothing else moves.

```text
Insert X after B:

  A → B → C            A → B   C          A → B → X → C
                ──▶          ↘ ↗    ──▶
                              X

  1) X.next = B.next   (X points to C)
  2) B.next = X        (B points to X)
```

> ⚠️ **Order matters!** If you set `B.next = X` first, you lose your only reference to `C`.

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

String show(Node<String>? n) {
  final parts = <String>[];
  for (; n != null; n = n.next) {
    parts.add(n.value);
  }
  return parts.join(' → ');
}

void main() {
  final c = Node('C');
  final b = Node('B', c);
  final a = Node('A', b);

  // Insert X after B
  final x = Node('X');
  x.next = b.next; // step 1
  b.next = x;      // step 2
  print(show(a));  // A → B → X → C

  // Delete the node after A (which is B)
  a.next = a.next?.next;
  print(show(a));  // A → X → C
}
```

**🔍 What This Code Does:**

1. **Insert in Two Steps**: Link the new node to its successor **first**, then link the predecessor to it.
2. **Delete by Bypassing**: `a.next = a.next?.next` skips B. Nothing points to B anymore, so the garbage collector frees it.
3. **O(1) Both Ways**: As long as we already have a reference to the node **before** the change point.
4. **Helper `show`**: Walks the chain and joins values for printing.

---

## 🔄 Reversing a Linked List (the classic!)

Reversal is the most famous linked-list problem. We flip every `next` arrow using **three pointers**.

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

Node<T>? reverse<T>(Node<T>? head) {
  Node<T>? prev;
  var current = head;
  while (current != null) {
    final next = current.next; // 1. remember the rest
    current.next = prev;       // 2. flip the arrow
    prev = current;            // 3. move prev forward
    current = next;            // 4. move current forward
  }
  return prev; // new head
}

Node<T>? reverseRecursive<T>(Node<T>? head) {
  if (head == null || head.next == null) return head;
  final newHead = reverseRecursive(head.next);
  head.next!.next = head; // the next node now points back to us
  head.next = null;
  return newHead;
}

String show(Node<int>? n) {
  final out = <int>[];
  for (; n != null; n = n.next) {
    out.add(n.value);
  }
  return out.join(' → ');
}

void main() {
  var head = Node(1, Node(2, Node(3, Node(4))));
  head = reverse(head)!;
  print(show(head)); // 4 → 3 → 2 → 1

  head = reverseRecursive(head)!;
  print(show(head)); // 1 → 2 → 3 → 4
}
```

**🔍 What This Code Does:**

1. **Save the Rest First**: `next` keeps a reference so we don't lose the remaining list when flipping.
2. **Flip**: `current.next = prev` points the arrow backwards.
3. **Advance Both**: `prev` and `current` step forward together.
4. **New Head**: When `current` becomes null, `prev` is the old tail, now the head.
5. **Iterative Is O(n) Time, O(1) Space**; the recursive version is O(n) space because of the call stack.

```text
prev   curr
null    1 → 2 → 3       step 1: null ← 1   2 → 3
        null ← 1 ← 2   3    ...    null ← 1 ← 2 ← 3
```

---

## 🐢🐇 Fast & Slow Pointers on Linked Lists

Two pointers moving at different speeds solve several classic problems in **one pass**.

### Find the middle node

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

Node<T>? middle<T>(Node<T>? head) {
  var slow = head;
  var fast = head;
  while (fast != null && fast.next != null) {
    slow = slow!.next;
    fast = fast.next!.next;
  }
  return slow;
}

void main() {
  final odd = Node(1, Node(2, Node(3, Node(4, Node(5)))));
  final even = Node(1, Node(2, Node(3, Node(4))));
  print(middle(odd)?.value);  // 3
  print(middle(even)?.value); // 3 (second of the two middles)
}
```

**🔍 What This Code Does:**

1. **Speeds**: `slow` moves one node per step, `fast` moves two.
2. **When Fast Finishes**: `slow` has gone exactly half as far, so it's in the middle.
3. **Even Length**: Returns the **second** middle node.
4. **One Pass, O(1) Space**: No need to count the length first.

### Detect a cycle (Floyd's tortoise and hare)

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

bool hasCycle<T>(Node<T>? head) {
  var slow = head;
  var fast = head;
  while (fast != null && fast.next != null) {
    slow = slow!.next;
    fast = fast.next!.next;
    if (identical(slow, fast)) return true; // they met inside a loop
  }
  return false;
}

void main() {
  final a = Node('a'), b = Node('b'), c = Node('c'), d = Node('d');
  a.next = b;
  b.next = c;
  c.next = d;
  print(hasCycle(a)); // false

  d.next = b; // create a loop: d → b
  print(hasCycle(a)); // true
}
```

**🔍 What This Code Does:**

1. **No Cycle**: `fast` reaches the end (null) and the function returns false.
2. **With a Cycle**: Both pointers end up circling the loop; `fast` gains one node per step, so it must eventually land on `slow`.
3. **`identical`**: Compares node **identity**, not values (two different nodes might hold equal values).
4. **O(n) Time, O(1) Space**: Better than storing visited nodes in a Set (O(n) space).

### Remove the n-th node from the end

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

Node<int>? removeNthFromEnd(Node<int>? head, int n) {
  final dummy = Node(0, head); // handles removing the head
  Node<int>? fast = dummy, slow = dummy;
  for (var i = 0; i <= n; i++) {
    fast = fast!.next; // move fast n + 1 steps ahead
  }
  while (fast != null) {
    fast = fast.next;
    slow = slow!.next;
  }
  slow!.next = slow.next?.next; // bypass the target
  return dummy.next;
}

void main() {
  var head = Node(1, Node(2, Node(3, Node(4, Node(5)))));
  head = removeNthFromEnd(head, 2)!;
  final out = <int>[];
  for (Node<int>? n = head; n != null; n = n.next) {
    out.add(n.value);
  }
  print(out); // [1, 2, 3, 5]
}
```

**🔍 What This Code Does:**

1. **Gap of n + 1**: Moving `fast` ahead first creates a fixed distance between the pointers.
2. **Move Together**: When `fast` falls off the end, `slow` is right **before** the node to remove.
3. **Dummy Node**: A fake node before the head means removing the first real node needs no special case.
4. **One Pass**: No need to compute the length first.

---

## 🧩 The Dummy (Sentinel) Node Trick

Many linked-list bugs come from special-casing the head. A **dummy node** in front of the head removes those special cases.

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

Node<int>? mergeSorted(Node<int>? a, Node<int>? b) {
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
  tail.next = a ?? b; // attach whatever is left
  return dummy.next;
}

Node<int>? removeAll(Node<int>? head, int target) {
  final dummy = Node(0, head);
  var prev = dummy;
  while (prev.next != null) {
    if (prev.next!.value == target) {
      prev.next = prev.next!.next;
    } else {
      prev = prev.next!;
    }
  }
  return dummy.next;
}

List<int> toList(Node<int>? n) {
  final out = <int>[];
  for (; n != null; n = n.next) {
    out.add(n.value);
  }
  return out;
}

void main() {
  final merged = mergeSorted(Node(1, Node(4, Node(6))), Node(2, Node(3, Node(7))));
  print(toList(merged)); // [1, 2, 3, 4, 6, 7]

  final cleaned = removeAll(Node(7, Node(1, Node(7, Node(2)))), 7);
  print(toList(cleaned)); // [1, 2]
}
```

**🔍 What This Code Does:**

1. **Merge With a Dummy**: `tail` always points to the last node of the merged list; the dummy gives it a starting point.
2. **Relinking, Not Copying**: The merge reuses the existing nodes, so it's O(1) extra space.
3. **Leftovers**: `a ?? b` attaches the remaining list in one step.
4. **Remove All Matches**: With a dummy, removing the head is the same as removing any other node.
5. **Only Advance When Not Removing**: After a removal, `prev` stays put to check the new `prev.next`.

---

## 📚 Linked Lists in Real Life

| Use | Why a linked list |
|-----|-------------------|
| **Stacks and queues** | O(1) add/remove at the ends |
| **Undo history** | Each state links to the previous one |
| **Hash table buckets** (chaining) | Small lists of colliding entries |
| **LRU caches** | O(1) move-to-front with a doubly linked list |
| **Immutable/persistent lists** in functional languages | New heads can **share** the old tail safely |

> 💡 Dart's own `dart:collection` has a `LinkedList` class for **doubly** linked lists of special entries. We'll cover it in the next lesson.

---

## ⚠️ Common Mistakes

### 1. Losing the rest of the list

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

void main() {
  final head = Node(1, Node(2, Node(3)));
  final x = Node(99);

  // ❌ Wrong order: head.next = x; x.next = head.next; (x would point to itself!)
  // ✅ Right order:
  x.next = head.next;
  head.next = x;

  final out = <int>[];
  for (Node<int>? n = head; n != null; n = n.next) {
    out.add(n.value);
  }
  print(out); // [1, 99, 2, 3]
}
```

**🔍 What This Code Does:**

1. **Save Before Overwriting**: Always connect the new node to the rest of the list first.
2. **Wrong Order Creates a Loop**: Setting `head.next = x` first and then `x.next = head.next` makes `x` point to itself.

### 2. Null pointer errors at the end

Always check `node.next != null` before using `node.next!.something`, especially in fast/slow loops (`fast != null && fast.next != null`).

### 3. Forgetting to update `tail` and `length`

When removing the last node or emptying the list, `tail` must be updated. When adding or removing, `length` must change. Missing either causes subtle bugs later.

### 4. Using a linked list for random access

`elementAtIndex(i)` is O(i). Looping `for (i...) list.elementAtIndex(i)` is O(n²). Iterate with the iterator instead.

---

## 🧪 Try It Yourself

1. Add `removeLast()` to `SinglyLinkedList`. Why is it O(n) even with a tail pointer?
2. Write `isPalindrome(Node<int>? head)` in O(n) time and O(1) space. *(Hint: find the middle, reverse the second half, compare.)*
3. Write `intersection(Node a, Node b)` that returns the node where two lists merge (by identity), or null.
4. Write `rotateRight(head, k)` that rotates a linked list right by k places.

```dart
class Node<T> {
  T value;
  Node<T>? next;
  Node(this.value, [this.next]);
}

Node<int>? deleteDuplicatesSorted(Node<int>? head) {
  var current = head;
  while (current != null && current.next != null) {
    if (current.value == current.next!.value) {
      current.next = current.next!.next; // skip the duplicate
    } else {
      current = current.next;
    }
  }
  return head;
}

void main() {
  var head = deleteDuplicatesSorted(Node(1, Node(1, Node(2, Node(3, Node(3))))));
  final out = <int>[];
  for (; head != null; head = head.next) {
    out.add(head.value);
  }
  print(out); // [1, 2, 3]
}
```

**🔍 What This Code Does:**

1. **Sorted Input**: Duplicates sit next to each other.
2. **Skip Instead of Advance**: When the next node is a duplicate, bypass it and check again.
3. **O(n) Time, O(1) Space**: Each node is visited once.

---

## 📌 Key Takeaways

- ✅ A **singly linked list** is a chain of nodes, each with a **value** and a **`next`** reference; the last `next` is **null**.
- ✅ **Insert/remove at the head** and **after a known node** are **O(1)**; **indexing** and **searching** are **O(n)**.
- ✅ A **tail pointer** makes `addLast` O(1), but `removeLast` is still O(n) in a singly linked list.
- ✅ When rewiring, **connect the new node first**, then the predecessor.
- ✅ **Reversal** uses three pointers: `prev`, `current`, `next`.
- ✅ **Fast & slow pointers** find the middle, detect cycles and find the n-th from the end in one pass.
- ✅ A **dummy node** removes special cases around the head.

**Next up:** 🔗🔗 **Doubly & Circular Linked Lists**: two-way links, O(1) removal anywhere, and Dart's `LinkedList`.
