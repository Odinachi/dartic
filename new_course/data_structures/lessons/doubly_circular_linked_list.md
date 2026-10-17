# Doubly & Circular Linked Lists

Imagine the **back and forward buttons** in your web browser 🌐.

- From any page, you can go **back** ⬅️ to the previous page or **forward** ➡️ to the next one.
- If you close a page in the middle of your history, its neighbors simply **link to each other**.

Now imagine a **merry-go-round** 🎠: there's no first or last horse. After the last one comes the first one again, forever.

👉 These are the two upgrades to the singly linked list:

> A **doubly linked list** gives every node a **`next`** and a **`prev`** reference, so you can walk in **both directions** and remove any node in **O(1)** when you hold a reference to it.
>
> A **circular linked list** connects the last node back to the first, so the chain forms a **loop**.

---

## 🔗🔗 The Doubly Linked Node

```dart
class DNode<T> {
  T value;
  DNode<T>? prev;
  DNode<T>? next;
  DNode(this.value);
}

void main() {
  final a = DNode('A'), b = DNode('B'), c = DNode('C');
  a.next = b;
  b.prev = a;
  b.next = c;
  c.prev = b;

  print(b.prev?.value); // A
  print(b.next?.value); // C
  print(a.prev);        // null (a is the head)
  print(c.next);        // null (c is the tail)
}
```

**🔍 What This Code Does:**

1. **Two Links per Node**: `prev` points backward, `next` points forward.
2. **Both Directions Must Agree**: If `a.next == b`, then `b.prev` must be `a`. Every link is set **twice**.
3. **Ends Are null**: The head has no `prev`, the tail has no `next`.
4. **Cost**: One extra reference per node, in exchange for powerful new operations.

```text
        ┌──────┐     ┌──────┐     ┌──────┐
null ◀──┤  A   │◀───▶│  B   │◀───▶│  C   ├──▶ null
        └──────┘     └──────┘     └──────┘
         head                       tail
```

---

## ⚖️ Singly vs Doubly

| Operation | Singly linked | Doubly linked |
|-----------|---------------|---------------|
| Add/remove at head | O(1) | O(1) |
| Add at tail (with tail pointer) | O(1) | O(1) |
| **Remove at tail** | O(n) 🐢 | **O(1)** ⚡ |
| **Remove a node you hold** | O(n) (need its predecessor) | **O(1)** ⚡ |
| **Insert before a node you hold** | O(n) | **O(1)** ⚡ |
| Walk backward | ❌ | ✅ |
| Memory per node | value + 1 ref | value + 2 refs |
| Bug surface | Smaller | Larger (two links to keep in sync) |

> 💡 The superpower: **O(1) removal of any node** you already have a reference to. That's why LRU caches, browser history and text editors use doubly linked lists.

---

## 🏗️ Building a Doubly Linked List With Sentinels

Handling `null` at both ends creates lots of special cases. A neat trick is to use two **sentinel** nodes, a fake head and a fake tail, that are always present. Real nodes live **between** them, so every insert/remove looks the same.

```dart
class DNode<T> {
  T? value; // null only for the sentinels
  DNode<T>? prev;
  DNode<T>? next;
  DNode([this.value]);
}

class DoublyLinkedList<T> {
  final DNode<T> _head = DNode<T>(); // sentinel before the first item
  final DNode<T> _tail = DNode<T>(); // sentinel after the last item
  int _length = 0;

  DoublyLinkedList() {
    _head.next = _tail;
    _tail.prev = _head;
  }

  int get length => _length;
  bool get isEmpty => _length == 0;

  // Insert `node` between `before` and `after`: O(1)
  DNode<T> _insertBetween(T value, DNode<T> before, DNode<T> after) {
    final node = DNode<T>(value)
      ..prev = before
      ..next = after;
    before.next = node;
    after.prev = node;
    _length++;
    return node;
  }

  DNode<T> addFirst(T value) => _insertBetween(value, _head, _head.next!);
  DNode<T> addLast(T value) => _insertBetween(value, _tail.prev!, _tail);
  DNode<T> insertAfter(DNode<T> node, T value) =>
      _insertBetween(value, node, node.next!);
  DNode<T> insertBefore(DNode<T> node, T value) =>
      _insertBetween(value, node.prev!, node);

  // Remove any node in O(1)
  T unlink(DNode<T> node) {
    node.prev!.next = node.next;
    node.next!.prev = node.prev;
    node.prev = node.next = null; // help the GC, avoid stale links
    _length--;
    return node.value as T;
  }

  T removeFirst() {
    if (isEmpty) throw StateError('empty');
    return unlink(_head.next!);
  }

  T removeLast() {
    if (isEmpty) throw StateError('empty');
    return unlink(_tail.prev!);
  }

  List<T> toList() {
    final out = <T>[];
    for (var n = _head.next!; !identical(n, _tail); n = n.next!) {
      out.add(n.value as T);
    }
    return out;
  }

  List<T> toListReversed() {
    final out = <T>[];
    for (var n = _tail.prev!; !identical(n, _head); n = n.prev!) {
      out.add(n.value as T);
    }
    return out;
  }
}

void main() {
  final list = DoublyLinkedList<String>();
  list.addLast('B');
  final d = list.addLast('D');
  list.addFirst('A');
  list.insertBefore(d, 'C');
  list.addLast('E');

  print(list.toList());         // [A, B, C, D, E]
  print(list.toListReversed()); // [E, D, C, B, A]

  print(list.unlink(d));        // D (removed in O(1), no search!)
  print(list.removeLast());     // E
  print(list.removeFirst());     // A
  print(list.toList());         // [B, C]
  print(list.length);           // 2
}
```

**🔍 What This Code Does:**

This code demonstrates **a doubly linked list where every operation is O(1)**:

1. **Sentinels**: `_head` and `_tail` are permanent dummy nodes. An empty list is just `_head ⇄ _tail`.

2. **One Insert Routine**: `addFirst`, `addLast`, `insertAfter` and `insertBefore` all reuse `_insertBetween`, which sets **four** links.

3. **Returning Nodes**: Insert methods return the new node, so callers can later remove it directly.

4. **`unlink` in O(1)**: The neighbors are connected to each other, skipping the node. No traversal needed.

5. **No Null Checks for Ends**: Because sentinels always exist, `node.prev!` and `node.next!` are always valid for real nodes.

6. **Two-Way Traversal**: `toListReversed` walks backward using `prev`.

---

## 🧮 How `unlink` Works

```text
Before:   ... ⇄ P ⇄ X ⇄ N ⇄ ...

  P.next = N        (P now skips X going forward)
  N.prev = P        (N now skips X going backward)

After:    ... ⇄ P ⇄ N ⇄ ...         X is detached
```

In a **singly** linked list, we couldn't do this from `X` alone, because we don't know `P`. Having `prev` is what makes it O(1).

---

## 🌐 Real Example: Browser History

```dart
class Page {
  final String url;
  Page? back;
  Page? forward;
  Page(this.url);
}

class BrowserHistory {
  Page _current;
  BrowserHistory(String home) : _current = Page(home);

  String get current => _current.url;

  void visit(String url) {
    final page = Page(url)..back = _current;
    _current.forward = page; // drops any old forward history
    _current = page;
  }

  String goBack(int steps) {
    for (var i = 0; i < steps && _current.back != null; i++) {
      _current = _current.back!;
    }
    return _current.url;
  }

  String goForward(int steps) {
    for (var i = 0; i < steps && _current.forward != null; i++) {
      _current = _current.forward!;
    }
    return _current.url;
  }
}

void main() {
  final h = BrowserHistory('home.com');
  h.visit('news.com');
  h.visit('dart.dev');
  h.visit('pub.dev');

  print(h.goBack(2));    // news.com
  print(h.goForward(1)); // dart.dev
  h.visit('flutter.dev'); // clears pub.dev from forward history
  print(h.goForward(1)); // flutter.dev (nothing further)
  print(h.goBack(10));   // home.com (stops at the start)
}
```

**🔍 What This Code Does:**

1. **Doubly Linked Pages**: `back` and `forward` play the role of `prev` and `next`.
2. **Visiting Truncates**: A new visit replaces the forward link, just like a real browser drops "forward" pages.
3. **Bounded Steps**: The loops stop early when there's no more history.
4. **Initializer List**: `: _current = Page(home)` sets the non-nullable field before the constructor body.
5. **O(steps)** per navigation, O(1) per visit.

---

## 🎠 Circular Linked Lists

In a circular list, the last node's `next` points back to the **first** node. There's no `null` at the end, so loops must stop by **identity** (when you get back to where you started).

```dart
class CNode<T> {
  T value;
  late CNode<T> next;
  CNode(this.value) {
    next = this; // a single node points to itself
  }
}

class CircularList<T> {
  CNode<T>? _tail; // tail.next is the head

  bool get isEmpty => _tail == null;

  void add(T value) {
    final node = CNode(value);
    final tail = _tail;
    if (tail != null) {
      node.next = tail.next; // new node points to head
      tail.next = node;      // old tail points to new node
    }
    _tail = node;            // new node is the tail
  }

  // Move the head to the back: O(1)
  void rotate() {
    final tail = _tail;
    if (tail != null) _tail = tail.next;
  }

  List<T> toList() {
    final tail = _tail;
    if (tail == null) return [];
    final out = <T>[];
    var n = tail.next; // head
    do {
      out.add(n.value);
      n = n.next;
    } while (!identical(n, tail.next));
    return out;
  }
}

void main() {
  final players = CircularList<String>();
  for (final p in ['Ana', 'Ben', 'Cy', 'Dee']) {
    players.add(p);
  }
  print(players.toList()); // [Ana, Ben, Cy, Dee]
  players.rotate();
  print(players.toList()); // [Ben, Cy, Dee, Ana]
  players.rotate();
  print(players.toList()); // [Cy, Dee, Ana, Ben]
}
```

**🔍 What This Code Does:**

1. **Only a Tail Reference**: In a circular list, `tail.next` **is** the head, so one reference gives O(1) access to both ends.
2. **`late` Field**: `next` is assigned in the constructor body (to `this`), which `late` allows.
3. **Insert at the End**: The new node points to the head, the old tail points to the new node, and the new node becomes the tail.
4. **`rotate` in O(1)**: Moving `_tail` forward one step makes the old head the new tail. Great for **round-robin** turns.
5. **`do...while` + `identical`**: Visit at least once, then stop when we're back at the head.

### Round-robin scheduling & the Josephus problem

```dart
class CNode {
  final int id;
  late CNode next;
  CNode(this.id);
}

int josephus(int n, int k) {
  // Build a circle 1..n
  final first = CNode(1);
  var prev = first;
  for (var i = 2; i <= n; i++) {
    final node = CNode(i);
    prev.next = node;
    prev = node;
  }
  prev.next = first; // close the circle; prev is the last node

  var current = prev; // start "before" person 1
  while (!identical(current.next, current)) {
    for (var i = 1; i < k; i++) {
      current = current.next; // count k - 1 people
    }
    current.next = current.next.next; // eliminate the k-th
  }
  return current.id;
}

void main() {
  print(josephus(5, 2)); // 3
  print(josephus(7, 3)); // 4
}
```

**🔍 What This Code Does:**

1. **Circle of People**: Each node is a person; the last links back to the first.
2. **Count and Remove**: Step `k − 1` times, then bypass the next node to eliminate the k-th person.
3. **Natural Wraparound**: No modulo arithmetic or index juggling; the circle handles it.
4. **Stop at One**: When a node points to itself, only one person remains.
5. **O(n × k)**: n eliminations, each counting k steps.

---

## 📦 Dart's Built-in `LinkedList`

`dart:collection` provides `LinkedList<E>`, a **doubly linked list of entries**. Each element must extend `LinkedListEntry`, which stores the `next`/`previous` links **inside the element itself** (an *intrusive* list).

```dart
import 'dart:collection';

final class Song extends LinkedListEntry<Song> {
  final String title;
  Song(this.title);

  @override
  String toString() => title;
}

void main() {
  final playlist = LinkedList<Song>();
  final intro = Song('Intro');
  final hit = Song('Big Hit');
  final outro = Song('Outro');

  playlist
    ..add(intro)
    ..add(outro);
  intro.insertAfter(hit);         // O(1)
  print(playlist.toList());       // [Intro, Big Hit, Outro]

  print(hit.previous);            // Intro
  print(hit.next);                // Outro

  hit.unlink();                   // O(1) removal, no search
  print(playlist.toList());       // [Intro, Outro]
  print(playlist.length);         // 2

  playlist.addFirst(Song('Warm-up'));
  print(playlist.first);          // Warm-up
  print(playlist.last);           // Outro
}
```

**🔍 What This Code Does:**

1. **`final class ... extends LinkedListEntry<Song>`**: In Dart 3, `LinkedListEntry` is a `base` class, so subclasses must be `final`, `base` or `sealed`.
2. **Entries Know Their Neighbors**: `hit.previous` and `hit.next` work directly on the element.
3. **`insertAfter` / `insertBefore`**: O(1) insertion relative to an existing entry.
4. **`unlink()`**: Removes the entry in O(1).
5. **One List Only**: An entry can belong to **at most one** `LinkedList` at a time; adding it to another throws a `StateError`.

### `DoubleLinkedQueue`: no subclassing needed

```dart
import 'dart:collection';

void main() {
  final tasks = DoubleLinkedQueue<String>.from(['write', 'test', 'ship']);

  // Find an entry and remove it in O(1) once found
  final testEntry = tasks.firstEntry()!.nextEntry()!;
  print(testEntry.element); // test
  testEntry.append('review'); // insert after "test"
  testEntry.remove();         // remove "test"

  print(tasks.toList()); // [write, review, ship]
  tasks.addFirst('plan');
  print(tasks.removeLast()); // ship
  print(tasks);              // {plan, write, review}
}
```

**🔍 What This Code Does:**

1. **`DoubleLinkedQueue`**: A doubly linked queue that works with any element type.
2. **Entries**: `firstEntry()` and `nextEntry()` give access to the internal nodes.
3. **`append` / `prepend` / `remove`**: O(1) operations relative to an entry.
4. **Queue Operations**: `addFirst`, `addLast`, `removeFirst`, `removeLast` are all O(1).

| Dart class | Kind | Element requirement |
|------------|------|---------------------|
| `LinkedList<E>` | Doubly linked, intrusive | `E extends LinkedListEntry<E>` |
| `DoubleLinkedQueue<E>` | Doubly linked queue | Any type |
| `ListQueue<E>` (default `Queue`) | Circular array | Any type |

---

## ⚠️ Common Mistakes

### 1. Updating only one direction

```dart
class DNode<T> {
  T value;
  DNode<T>? prev, next;
  DNode(this.value);
}

void main() {
  final a = DNode(1), b = DNode(2);
  a.next = b;
  // ❌ forgot b.prev = a; walking backward from b breaks
  print(b.prev?.value); // null
  b.prev = a; // ✅
  print(b.prev?.value); // 1
}
```

**🔍 What This Code Does:**

1. **Asymmetric Links**: Forward traversal works but backward traversal doesn't.
2. **Rule**: Every insert sets **four** links; every remove fixes **two** neighbors.

### 2. Infinite loops in circular lists

A `while (node != null)` loop **never ends** on a circular list. Always stop when you return to the starting node.

### 3. Reusing an unlinked node without resetting it

After unlinking, clear `prev`/`next` (as our `unlink` does). Stale references can keep other nodes alive and cause confusing bugs if the node is reused.

### 4. Adding a `LinkedListEntry` to two lists

```dart
import 'dart:collection';

final class Item extends LinkedListEntry<Item> {}

void main() {
  final a = LinkedList<Item>(), b = LinkedList<Item>();
  final item = Item();
  a.add(item);
  try {
    b.add(item); // ❌ already in list a
  } on StateError {
    print('Unlink it from the first list before adding it elsewhere');
  }
}
```

**🔍 What This Code Does:**

1. **Intrusive Links**: The entry stores its own `next`/`previous`, so it can't be in two lists.
2. **Fix**: Call `item.unlink()` first.

---

## 🧪 Try It Yourself

1. Add `reverse()` to `DoublyLinkedList` that swaps `prev` and `next` on every node in O(n).
2. Write `moveToFront(DNode node)` that unlinks a node and re-adds it at the front, the core of an **LRU cache**.
3. Use `CircularList` to simulate a **round-robin** CPU scheduler that gives each process a time slice until all finish.
4. Implement a **text editor cursor** with a doubly linked list of characters: `insert(char)`, `backspace()`, `left()`, `right()`.

---

## 📌 Key Takeaways

- ✅ A **doubly linked list** has `prev` and `next`, allowing **two-way traversal**.
- ✅ With a node reference, you can **remove** or **insert before/after** it in **O(1)**.
- ✅ Every insert sets **four** links; every remove reconnects **two** neighbors.
- ✅ **Sentinel** head/tail nodes eliminate edge cases at the ends.
- ✅ A **circular list** links the tail back to the head; keeping only a **tail** reference gives O(1) access to both ends.
- ✅ Circular lists are perfect for **round-robin** turns and the **Josephus** problem; stop loops by **identity**, not null.
- ✅ Dart offers `LinkedList` (intrusive, `final class X extends LinkedListEntry<X>`) and `DoubleLinkedQueue`.

**Next up:** 🥞 **Stacks**: last in, first out, from undo buttons to bracket matching.
