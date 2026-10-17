# Queues & Deques

Imagine the line at your favorite **coffee shop** ☕.

- New customers join at the **back** of the line.
- The barista serves whoever is at the **front**.
- Nobody cuts in line (hopefully 😅).

The **first** person who arrived is the **first** one served.

👉 That's a **queue**:

> A **queue** adds items at the **back** (**enqueue**) and removes them from the **front** (**dequeue**). It follows **FIFO**: **F**irst **I**n, **F**irst **O**ut.

And if the coffee shop also lets VIPs jump to the front, or lets people leave from the back of the line, you have a **deque** (double-ended queue): add and remove at **both** ends.

Queues power task schedulers, message processing, print spoolers, breadth-first search, event loops, and rate limiters.

---

## 🧰 Queue Operations

| Operation | Meaning | Ideal cost |
|-----------|---------|------------|
| `enqueue(x)` / `addLast(x)` | Join at the back | O(1) |
| `dequeue()` / `removeFirst()` | Leave from the front | O(1) |
| `peek()` / `first` | Look at the front | O(1) |
| `isEmpty`, `length` | Size checks | O(1) |

A **deque** adds `addFirst` and `removeLast`, also O(1).

---

## ❌ Why Not Just Use a List?

```dart
void main() {
  final line = <String>[];
  line.add('Ana');   // enqueue: O(1) ✅
  line.add('Ben');
  line.add('Cy');

  final served = line.removeAt(0); // dequeue: O(n) ❌ shifts everyone forward
  print(served); // Ana
  print(line);   // [Ben, Cy]
}
```

**🔍 What This Code Does:**

1. **Adding at the End Is Cheap**: `add` is O(1) amortized.
2. **Removing at the Front Is Expensive**: `removeAt(0)` shifts every remaining element left, O(n).
3. **Draining n Items Costs O(n²)**: Fine for 10 customers, terrible for a million messages.

We need a structure that's cheap at **both** ends.

---

## ✅ Dart's `Queue` (a `ListQueue`)

`dart:collection` provides `Queue<E>`. Its default implementation, **`ListQueue`**, is a **circular buffer**: O(1) amortized at both ends.

```dart
import 'dart:collection';

void main() {
  final orders = Queue<String>();

  orders.addLast('☕ Latte');      // enqueue
  orders.addLast('🍵 Matcha');
  orders.addLast('🧋 Bubble tea');
  print(orders);                    // {☕ Latte, 🍵 Matcha, 🧋 Bubble tea}

  print(orders.first);              // ☕ Latte (peek)
  print(orders.removeFirst());      // ☕ Latte (dequeue)
  print(orders.length);             // 2

  // Deque powers: both ends
  orders.addFirst('⭐ VIP espresso');
  print(orders.removeLast());       // 🧋 Bubble tea
  print(orders.toList());           // [⭐ VIP espresso, 🍵 Matcha]

  // Iterable goodies still work
  print(orders.contains('🍵 Matcha')); // true (O(n))
}
```

**🔍 What This Code Does:**

1. **`addLast` / `removeFirst`**: Standard FIFO queue operations, both O(1).
2. **`addFirst` / `removeLast`**: Deque operations, also O(1).
3. **`first` / `last`**: Peek at either end without removing.
4. **Prints With Braces**: `Queue.toString()` uses `{...}`; `toList()` gives a normal list.
5. **No Indexing**: `Queue` has no `[]` operator; it's not meant for random access. (`elementAt(i)` exists from Iterable but is O(i) for some implementations.)

| Dart class | How it's built | Notes |
|------------|----------------|-------|
| `Queue()` → `ListQueue` | Circular array | Fast and memory-friendly; the default choice |
| `ListQueue` | Circular array | Use directly to set an initial capacity |
| `DoubleLinkedQueue` | Doubly linked list | O(1) removal of a known entry |

---

## 🔄 How a Circular Buffer Works

A circular buffer is an array where the **front** and **back** indexes **wrap around** to the beginning, so removing from the front never shifts anything.

```dart
class CircularQueue<T> {
  List<T?> _buf;
  int _head = 0; // index of the front element
  int _length = 0;

  CircularQueue([int capacity = 4]) : _buf = List<T?>.filled(capacity, null);

  int get length => _length;
  bool get isEmpty => _length == 0;

  void enqueue(T value) {
    if (_length == _buf.length) _grow();
    final tail = (_head + _length) % _buf.length; // wrap around
    _buf[tail] = value;
    _length++;
  }

  T dequeue() {
    if (isEmpty) throw StateError('Queue is empty');
    final value = _buf[_head] as T;
    _buf[_head] = null;                  // let the GC reclaim it
    _head = (_head + 1) % _buf.length;   // move front forward, wrapping
    _length--;
    return value;
  }

  T get front {
    if (isEmpty) throw StateError('Queue is empty');
    return _buf[_head] as T;
  }

  void _grow() {
    final bigger = List<T?>.filled(_buf.length * 2, null);
    for (var i = 0; i < _length; i++) {
      bigger[i] = _buf[(_head + i) % _buf.length]; // unroll in order
    }
    _buf = bigger;
    _head = 0;
  }

  String debug() => 'buf=$_buf head=$_head length=$_length';
}

void main() {
  final q = CircularQueue<int>(4);
  q.enqueue(1);
  q.enqueue(2);
  q.enqueue(3);
  print(q.dequeue()); // 1
  print(q.dequeue()); // 2
  q.enqueue(4);
  q.enqueue(5); // wraps around to index 0
  print(q.debug()); // buf=[5, null, 3, 4] head=2 length=3

  q.enqueue(6);
  q.enqueue(7); // full → grows and unrolls
  print(q.debug()); // buf=[3, 4, 5, 6, 7, null, null, null] head=0 length=5

  final out = <int>[];
  while (!q.isEmpty) {
    out.add(q.dequeue());
  }
  print(out); // [3, 4, 5, 6, 7]
}
```

**🔍 What This Code Does:**

This code demonstrates **a growable circular buffer queue**:

1. **Modulo Wraparound**: `(index) % capacity` sends an index past the end back to 0, so the buffer is used like a ring.

2. **Tail Position**: The next free slot is `_head + _length`, wrapped.

3. **Dequeue Moves the Head**: Instead of shifting elements, we just advance `_head`. O(1).

4. **Clearing Slots**: Setting the old slot to `null` avoids holding references to removed objects.

5. **Growing**: When full, copy elements **in queue order** into a bigger buffer starting at index 0. O(n) occasionally, O(1) amortized.

```text
capacity 4, after dequeuing 1 and 2, then enqueueing 4 and 5:

index:  0    1    2    3
      [ 5 | -- | 3  | 4 ]
              head↑
order: 3 → 4 → 5   (wraps from index 3 to index 0)
```

---

## 🧺 Fixed-Size Ring Buffer: Keep Only the Latest N

Sometimes you only care about the **most recent** items: the last 100 log lines, the last 5 sensor readings. A fixed-size buffer **overwrites** the oldest item when full.

```dart
import 'dart:collection';

class RecentItems<T> {
  final int capacity;
  final Queue<T> _items = Queue<T>();
  RecentItems(this.capacity);

  void add(T item) {
    if (_items.length == capacity) {
      _items.removeFirst(); // drop the oldest
    }
    _items.addLast(item);
  }

  List<T> get items => _items.toList();
}

void main() {
  final recent = RecentItems<String>(3);
  for (final page in ['home', 'search', 'item/42', 'cart', 'checkout']) {
    recent.add(page);
  }
  print(recent.items); // [item/42, cart, checkout]
}
```

**🔍 What This Code Does:**

1. **Bounded Size**: The queue never grows beyond `capacity`.
2. **Evict Oldest**: When full, `removeFirst` drops the item that arrived first.
3. **O(1) per Add**: Perfect for "recently viewed" lists, log tails and moving averages.

---

## 📬 Example: Processing Tasks in Order

```dart
import 'dart:collection';

class Job {
  final int id;
  final String name;
  int remaining; // time units still needed
  Job(this.id, this.name, this.remaining);
}

void main() {
  // Round-robin scheduler: each job runs for at most `slice` units,
  // then goes to the back of the queue if it isn't finished.
  final ready = Queue<Job>.from([
    Job(1, 'compile', 5),
    Job(2, 'test', 2),
    Job(3, 'deploy', 3),
  ]);
  const slice = 2;
  var clock = 0;

  while (ready.isNotEmpty) {
    final job = ready.removeFirst();
    final run = job.remaining < slice ? job.remaining : slice;
    clock += run;
    job.remaining -= run;
    if (job.remaining > 0) {
      ready.addLast(job); // back of the line
    } else {
      print('t=$clock: ${job.name} finished');
    }
  }
}
```

**🔍 What This Code Does:**

1. **FIFO Fairness**: Jobs run in the order they're waiting.
2. **Time Slices**: Each job runs at most `slice` units per turn.
3. **Re-queue Unfinished Jobs**: `addLast` sends them to the back, so every job gets a fair turn.
4. **Output**: `test` finishes at t=4, `deploy` at t=9, and `compile` at t=10.
5. **Real World**: Operating systems use this "round robin" idea to share the CPU.

---

## 🌊 Queues and Breadth-First Search

Queues explore things **level by level**: everything 1 step away, then 2 steps away, and so on. This is **breadth-first search (BFS)**, which you'll use heavily for trees and graphs.

```dart
import 'dart:collection';

int shortestSteps(List<String> grid, (int, int) start, (int, int) goal) {
  final rows = grid.length, cols = grid[0].length;
  final queue = Queue<((int, int), int)>(); // (position, distance)
  final seen = <(int, int)>{start};
  queue.add((start, 0));

  const moves = [(1, 0), (-1, 0), (0, 1), (0, -1)];
  while (queue.isNotEmpty) {
    final ((r, c), dist) = queue.removeFirst();
    if ((r, c) == goal) return dist;
    for (final (dr, dc) in moves) {
      final next = (r + dr, c + dc);
      final (nr, nc) = next;
      if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
      if (grid[nr][nc] == '#' || seen.contains(next)) continue;
      seen.add(next);
      queue.add((next, dist + 1));
    }
  }
  return -1;
}

void main() {
  final maze = [
    'S..#',
    '.#..',
    '...G',
  ];
  print(shortestSteps(maze, (0, 0), (2, 3))); // 5
}
```

**🔍 What This Code Does:**

1. **Queue of (Position, Distance)**: Nested records store each cell with how far it is from the start.
2. **Level by Level**: Because it's FIFO, all cells at distance `d` are processed before any at `d + 1`.
3. **First Arrival Is Shortest**: The first time we dequeue the goal, its distance is the minimum.
4. **`seen` Set**: Prevents revisiting cells and looping forever.
5. **Record Patterns**: `final ((r, c), dist) = ...` destructures the nested record in one line.

> 💡 Swap the **queue** for a **stack** and the same loop becomes depth-first search, which does **not** find shortest paths.

---

## 🪟 Deque Power: Sliding Window Maximum

A **monotonic deque** keeps candidates for the maximum of a moving window. Indexes enter at the back and leave from **both** ends.

```dart
import 'dart:collection';

List<int> windowMax(List<int> nums, int k) {
  final dq = ListQueue<int>(); // indexes; their values are decreasing
  final result = <int>[];

  for (var i = 0; i < nums.length; i++) {
    // 1. Drop the front if it slid out of the window
    if (dq.isNotEmpty && dq.first <= i - k) dq.removeFirst();
    // 2. Drop smaller values from the back: they can never be the max
    while (dq.isNotEmpty && nums[dq.last] <= nums[i]) {
      dq.removeLast();
    }
    dq.addLast(i);
    // 3. Record the max once the first full window is formed
    if (i >= k - 1) result.add(nums[dq.first]);
  }
  return result;
}

void main() {
  print(windowMax([1, 3, -1, -3, 5, 3, 6, 7], 3)); // [3, 3, 5, 5, 6, 7]
}
```

**🔍 What This Code Does:**

1. **Front = Current Max**: The deque's front always holds the index of the largest value in the window.
2. **Expire From the Front**: Indexes older than the window are removed with `removeFirst`.
3. **Prune From the Back**: Smaller values behind a new bigger value can never win, so `removeLast` discards them.
4. **O(n)**: Each index is added once and removed at most once. A brute force approach is O(n × k).

---

## 🥞🥞 Building a Queue From Two Stacks

A classic interview puzzle: implement a FIFO queue using only two LIFO stacks.

```dart
class StackQueue<T> {
  final _inbox = <T>[];  // receives new items
  final _outbox = <T>[]; // serves items in FIFO order

  void enqueue(T x) => _inbox.add(x);

  T dequeue() {
    if (_outbox.isEmpty) {
      while (_inbox.isNotEmpty) {
        _outbox.add(_inbox.removeLast()); // reverse the order once
      }
    }
    if (_outbox.isEmpty) throw StateError('empty');
    return _outbox.removeLast();
  }
}

void main() {
  final q = StackQueue<int>()
    ..enqueue(1)
    ..enqueue(2)
    ..enqueue(3);
  print(q.dequeue()); // 1
  q.enqueue(4);
  print(q.dequeue()); // 2
  print(q.dequeue()); // 3
  print(q.dequeue()); // 4
}
```

**🔍 What This Code Does:**

1. **Two Stacks Reverse Twice**: Pouring the inbox into the outbox reverses the order, turning LIFO into FIFO.
2. **Only Pour When Empty**: Moving items only when the outbox is empty keeps the order correct.
3. **Amortized O(1)**: Each item is moved from inbox to outbox **once**, so n operations cost O(n) total.

---

## 🧭 Choosing the Right Queue

| Need | Use |
|------|-----|
| FIFO processing, BFS | `Queue` (`ListQueue`) |
| Add/remove at both ends | `Queue` (it's already a deque) |
| Keep only the latest N items | `Queue` + evict with `removeFirst` |
| Always process the **most urgent** item | **Priority queue / heap** (Module 4) |
| Remove an arbitrary known entry in O(1) | `DoubleLinkedQueue` |
| Async producer/consumer | `Stream` / `StreamController` |

---

## ⚠️ Common Mistakes

### 1. Using `removeAt(0)` as a queue

O(n) per dequeue. Use `Queue.removeFirst()`.

### 2. Removing from an empty queue

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>();
  // q.removeFirst(); ❌ throws StateError: No element
  if (q.isNotEmpty) {
    print(q.removeFirst());
  } else {
    print('Nothing to process'); // ✅
  }
}
```

**🔍 What This Code Does:**

1. **Empty Check**: `removeFirst` on an empty `Queue` throws a `StateError`.
2. **Guard First**: Check `isNotEmpty` before dequeuing.

### 3. Marking BFS nodes as seen too late

Mark a node as **seen when you enqueue it**, not when you dequeue it. Otherwise the same node can be enqueued many times, wasting time and memory.

### 4. Modifying a queue while iterating it

Like Lists, changing a `Queue` inside a for-in over the same queue throws a `ConcurrentModificationError`. Use a `while (q.isNotEmpty)` loop with `removeFirst()` instead.

---

## 🧪 Try It Yourself

1. **Hot potato**: n players pass a potato; every k-th pass eliminates the holder. Use a `Queue` with `removeFirst`/`addLast`.
2. **Recent counter**: `ping(t)` returns how many pings happened in the last 3000 ms. *(Hint: evict old timestamps from the front.)*
3. **Palindrome check with a deque**: compare and remove characters from both ends.
4. **Stack from two queues**: the reverse puzzle. Which operation becomes O(n)?

```dart
import 'dart:collection';

class RecentCounter {
  final _times = Queue<int>();

  int ping(int t) {
    _times.addLast(t);
    while (_times.first < t - 3000) {
      _times.removeFirst();
    }
    return _times.length;
  }
}

void main() {
  final rc = RecentCounter();
  print(rc.ping(1));    // 1
  print(rc.ping(100));  // 2
  print(rc.ping(3001)); // 3
  print(rc.ping(3002)); // 3 (ping at t=1 expired)
}
```

**🔍 What This Code Does:**

1. **Timestamps in Arrival Order**: New pings go to the back.
2. **Evict Expired From the Front**: Anything older than `t − 3000` falls out of the window.
3. **Length = Answer**: The queue holds exactly the pings in the window.
4. **O(1) Amortized**: Each timestamp is added and removed once.

---

## 📌 Key Takeaways

- ✅ A **queue** is **FIFO**: add at the back, remove from the front.
- ✅ Don't use `List.removeAt(0)` as dequeue; it's **O(n)**.
- ✅ Dart's `Queue` (a **`ListQueue`** circular buffer) gives **O(1)** amortized operations at **both ends**, so it's also a **deque**.
- ✅ A **circular buffer** wraps indexes with `%` so nothing ever shifts.
- ✅ Queues drive **BFS**, schedulers and "latest N" buffers; a **monotonic deque** solves sliding-window maximum in O(n).
- ✅ Two stacks can simulate a queue with **amortized O(1)** operations.

**Next up:** #️⃣ **Module 3: Hash Tables from Scratch**: how `Map` and `Set` find things in O(1).
