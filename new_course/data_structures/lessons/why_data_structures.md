# Why Data Structures Matter

Imagine you've just moved into a new house 🏠 with **500 books** 📚.

You have two choices:

- 📦 **Option A:** Throw every book into one giant box.
- 🗄️ **Option B:** Put them on shelves, sorted by author, with a label on each shelf.

Both options *store* the books. But when a friend asks, *"Do you have Harry Potter?"*:

- With the **box**, you dig through every single book until you find it (or don't).
- With the **shelves**, you walk to the **R** shelf (Rowling) and grab it in seconds.

👉 That is exactly what a **data structure** is:

> A **data structure** is a way of **organizing data** so that the operations you care about (finding, adding, removing, sorting) are **fast and easy**.

The data is the same. The **organization** changes everything.

---

## 🧠 What Is a Data Structure, Really?

Every data structure answers three questions:

1. **How is the data laid out?** (side by side in memory, linked by pointers, arranged in a tree...)
2. **What operations does it support?** (add, remove, search, get by index, get smallest...)
3. **How much do those operations cost?** (in time and in memory)

You already know a few data structures from Dart:

| Dart type | What it's good at | Real-life equivalent |
|-----------|-------------------|----------------------|
| `List<T>` | Keeping items in order, grabbing item #5 instantly | A numbered row of lockers |
| `Set<T>` | Making sure there are no duplicates, fast "is it here?" checks | A guest list at a club |
| `Map<K, V>` | Looking up a value by its key | A phone book |
| `Queue<T>` | First come, first served | A line at the bank |

In this course you'll learn **how these work inside**, **when to pick each one**, and how to **build your own** (linked lists, trees, heaps, graphs and more).

---

## 🚫 The Problem: Choosing the Wrong Structure

Let's say you're building a **username checker** for a sign-up screen. Every time someone types a username, you need to check if it's already taken.

```dart
void main() {
  // 100,000 existing usernames stored in a List
  final takenUsernames = List.generate(100000, (i) => 'user$i');

  final stopwatch = Stopwatch()..start();

  // Check 1,000 new sign-ups
  var taken = 0;
  for (var i = 0; i < 1000; i++) {
    if (takenUsernames.contains('user${i * 97}')) {
      taken++;
    }
  }

  stopwatch.stop();
  print('Taken: $taken');
  print('List lookups took: ${stopwatch.elapsedMilliseconds} ms');
}
```

**🔍 What This Code Does:**

This code demonstrates **how a List performs when used for membership checks**:

1. **Linear Search**: `List.contains` checks the items **one by one**, from the start, until it finds a match or reaches the end.

2. **Worst Case Cost**: If the username isn't there, it compares against **all 100,000** names.

3. **Repeated Work**: We do this 1,000 times, so in the worst case that's up to **100 million comparisons**.

4. **Stopwatch Timing**: `Stopwatch` measures real elapsed time so we can compare approaches.

5. **Hidden Scaling Problem**: It may feel fine with 100 users, but it gets dramatically slower as the app grows.

**Problems:**

- **Every lookup scans the list** 🐢
- **Doubling the users doubles the time** of every check 📈
- **The code looks innocent**, so the problem is easy to miss 🙈

---

## ✅ The Solution: Pick a Structure Built for the Job

The question we keep asking is *"is this username in the collection?"*. A `Set` is designed exactly for that.

```dart
void main() {
  // Same 100,000 usernames, but stored in a Set
  final takenUsernames = Set<String>.from(
    List.generate(100000, (i) => 'user$i'),
  );

  final stopwatch = Stopwatch()..start();

  var taken = 0;
  for (var i = 0; i < 1000; i++) {
    if (takenUsernames.contains('user${i * 97}')) {
      taken++;
    }
  }

  stopwatch.stop();
  print('Taken: $taken');
  print('Set lookups took: ${stopwatch.elapsedMilliseconds} ms');
}
```

**🔍 What This Code Does:**

This code demonstrates **constant-time membership checks with a hash-based Set**:

1. **Hashing**: A `Set` (by default a `LinkedHashSet`) computes a **hash code** for each username and uses it to jump almost directly to where that name would be stored.

2. **No Scanning**: `contains` does **not** walk through all items; on average it checks only one or two.

3. **Same Answer, Less Work**: The result (`taken`) is identical to the List version, but the work done is a tiny fraction.

4. **Scales Gracefully**: With 10x more usernames, each lookup takes roughly the **same** time.

5. **One-Line Change**: The only change was the **type of collection**. That's the power of choosing the right data structure.

**Benefits:**

- ⚡ **Lookups stay fast** no matter how many users sign up
- 🧹 **Duplicates are impossible**, which matches the "usernames are unique" rule
- 🧠 **The code expresses intent**: a Set *means* "a collection of unique things"

---

## 📏 Measuring "Fast": Operations and Their Cost

When we compare data structures, we don't talk about milliseconds (those depend on your phone, your laptop, the weather...). We talk about **how the work grows as the data grows**.

Here's a sneak peek at the costs you'll master in this course. `n` is the number of items:

| Operation | `List` | `Set` / `Map` (hash) | Sorted tree (`SplayTreeMap`) |
|-----------|--------|----------------------|------------------------------|
| Get item at index `i` | **O(1)** ⚡ | ❌ not supported | ❌ not supported |
| Check if value exists | O(n) 🐢 | **O(1)** average ⚡ | O(log n) 🚀 |
| Add to end | **O(1)** amortized ⚡ | **O(1)** average ⚡ | O(log n) 🚀 |
| Insert at the front | O(n) 🐢 | n/a (no order by position) | n/a |
| Get items in sorted order | O(n log n) (sort first) | O(n log n) (sort first) | **O(n)** ⚡ |
| Get smallest item | O(n) 🐢 | O(n) 🐢 | O(log n) 🚀 |

Don't worry if `O(log n)` looks strange right now. The next lesson is all about **Big O**. For now, remember:

> ⚡ **O(1)** = instant, 🚀 **O(log n)** = very fast, 🐢 **O(n)** = slows down as data grows.

---

## 🍕 Pizza Shop Example: One App, Three Structures

Real apps use **several data structures at once**, each for the job it's best at.

```dart
import 'dart:collection';

void main() {
  print('🍕 PIZZA SHOP ORDER SYSTEM 🍕\n');

  // 1. Menu: look up prices by name -> Map
  final Map<String, double> menu = {
    'Margherita': 8.50,
    'Pepperoni': 9.99,
    'Veggie': 9.25,
  };

  // 2. Orders waiting to be cooked -> Queue (first in, first out)
  final Queue<String> kitchenQueue = Queue<String>();

  // 3. Customers who already got a loyalty stamp today -> Set
  final Set<String> stampedToday = {};

  void placeOrder(String customer, String pizza) {
    final price = menu[pizza];
    if (price == null) {
      print('❌ $pizza is not on the menu');
      return;
    }
    kitchenQueue.addLast('$customer: $pizza');
    final gotStamp = stampedToday.add(customer);
    print('🧾 $customer ordered $pizza (\$${price.toStringAsFixed(2)})'
        '${gotStamp ? ' ⭐ stamp added' : ''}');
  }

  placeOrder('Ada', 'Pepperoni');
  placeOrder('Linus', 'Veggie');
  placeOrder('Ada', 'Margherita');
  placeOrder('Grace', 'Hawaiian');

  print('\n👨‍🍳 Cooking in order:');
  while (kitchenQueue.isNotEmpty) {
    print('🔥 ${kitchenQueue.removeFirst()}');
  }

  print('\n⭐ Customers stamped today: $stampedToday');
}
```

**🔍 What This Code Does:**

This code demonstrates **matching each requirement to the right data structure**:

1. **Map for the Menu**: Prices are looked up **by name**, so a `Map<String, double>` gives instant lookups with `menu[pizza]`.

2. **Queue for the Kitchen**: Orders must be cooked in the **order they arrived**. `Queue.addLast` and `removeFirst` are both O(1).

3. **Set for Loyalty Stamps**: A customer gets **at most one** stamp per day. `Set.add` returns `false` if they're already in it, which handles the rule for free.

4. **Null-Safe Lookup**: `menu[pizza]` returns `null` for unknown pizzas, so we can reject them safely.

5. **Combined Design**: No single structure does everything well; the system is fast because **each part uses the right tool**.

---

## 🏥 Hospital Example: When Order Is About Priority

In a hospital emergency room, patients aren't treated first-come-first-served. The **most urgent** patient goes first.

```dart
void main() {
  print('🏥 EMERGENCY ROOM TRIAGE 🏥\n');

  // Each patient: (name, urgency) where 1 = most urgent
  final patients = <(String, int)>[
    ('Sam', 3),
    ('Rita', 1),
    ('Omar', 2),
    ('Lena', 1),
    ('Tom', 5),
  ];

  // ❌ Naive approach: search the whole list every time
  final waiting = [...patients];
  print('Treatment order (naive search):');
  while (waiting.isNotEmpty) {
    var best = 0;
    for (var i = 1; i < waiting.length; i++) {
      if (waiting[i].$2 < waiting[best].$2) best = i;
    }
    final next = waiting.removeAt(best);
    print('🩺 ${next.$1} (urgency ${next.$2})');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **a priority problem solved the slow way**:

1. **Records for Patients**: Each patient is a Dart record `(String, int)`, accessed with `.$1` (name) and `.$2` (urgency).

2. **Full Scan Every Time**: To find the most urgent patient, the loop checks **every** waiting patient.

3. **Expensive Removal**: `removeAt(best)` shifts every item after `best` one position left.

4. **Quadratic Growth**: With `n` patients we do about `n` scans of up to `n` items, roughly **n² work**.

5. **Correct but Slow**: The output is right, but this doesn't scale to a busy hospital.

> 💡 In the **Heaps & Priority Queues** lesson you'll build a structure that always hands you the most urgent patient in **O(log n)**. Same output, massively less work.

---

## 🎮 Game Example: Grid vs Map for a Huge World

Game worlds are often stored as grids. But what if your world is **1,000,000 × 1,000,000** tiles and only a few hundred tiles have something on them?

```dart
void main() {
  print('🎮 SPARSE GAME WORLD 🎮\n');

  // ❌ A full 2D grid would need 1,000,000,000,000 cells. Impossible!
  // ✅ Store only the tiles that actually contain something.
  final Map<(int, int), String> world = {};

  world[(10, 20)] = '🌳 Tree';
  world[(500000, 999)] = '💎 Diamond';
  world[(999999, 999999)] = '🏰 Castle';

  (int, int) player = (500000, 999);

  final tile = world[player] ?? '🌱 Grass';
  print('Player stands on: $tile');

  print('Stored tiles: ${world.length}');
  print('Tiles in the full world: ${1000000 * 1000000}');
}
```

**🔍 What This Code Does:**

This code demonstrates **choosing a sparse structure to save memory**:

1. **Record Keys**: Dart records like `(10, 20)` have built-in `==` and `hashCode`, so they work perfectly as Map keys.

2. **Only Store What Exists**: The Map holds **3 entries** instead of a trillion empty cells.

3. **Default Values**: `world[player] ?? '🌱 Grass'` treats every missing tile as grass.

4. **Space Complexity**: Memory grows with the number of **interesting** tiles, not the size of the world.

5. **Same Lookups**: Reading a tile is still O(1) on average, just like indexing a grid.

---

## 🧰 The Data Structure Toolbox (Your Course Map)

Here's everything you'll learn, grouped by **what kind of problem it solves**:

| Family | Structures | Typical question it answers |
|--------|-----------|-----------------------------|
| **Linear** | List, linked list, stack, queue, deque | "What comes next?" |
| **Hashing** | Hash table, `Map`, `Set` | "Have I seen this?" / "What's the value for this key?" |
| **Trees** | Binary tree, BST, heap, trie | "What's the smallest?" / "What starts with this prefix?" |
| **Graphs** | Adjacency list, adjacency matrix | "How are these things connected?" / "What's the shortest route?" |
| **Advanced** | Segment tree, LRU cache, Bloom filter | "What's the sum of this range?" / "What did I use recently?" |

And the **algorithms** that go with them: searching, sorting, traversals, shortest paths and dynamic programming.

---

## 🔍 How to Choose: Ask These Questions

Before picking a structure, ask yourself:

1. **Do I need to keep items in order?**
   - By insertion order → `List` or `Queue`
   - By sorted value → `SplayTreeMap` / `SplayTreeSet` or a sorted `List`

2. **Do I look things up by a key?**
   - Yes → `Map`

3. **Do I only care whether something exists?**
   - Yes → `Set`

4. **Do I always want the smallest/largest/most urgent item?**
   - Yes → a **heap** (priority queue)

5. **Do I add/remove mostly at the ends?**
   - Back only → `List` works as a **stack**
   - Front and back → `Queue` / `ListQueue`

6. **Are things connected to each other (friends, roads, dependencies)?**
   - Yes → a **graph**

```dart
void main() {
  print('🧭 QUICK STRUCTURE PICKER 🧭\n');

  String pick({
    bool needsKeyLookup = false,
    bool onlyMembership = false,
    bool needsPriority = false,
    bool fifo = false,
  }) {
    if (needsKeyLookup) return 'Map';
    if (onlyMembership) return 'Set';
    if (needsPriority) return 'Heap / PriorityQueue';
    if (fifo) return 'Queue';
    return 'List';
  }

  print('Phone book            -> ${pick(needsKeyLookup: true)}');
  print('Banned words          -> ${pick(onlyMembership: true)}');
  print('Task scheduler        -> ${pick(needsPriority: true)}');
  print('Print jobs            -> ${pick(fifo: true)}');
  print('Shopping cart items   -> ${pick()}');
}
```

**🔍 What This Code Does:**

This code demonstrates **turning requirements into a structure choice**:

1. **Named Parameters**: Each requirement is a `bool` flag with a default of `false`, so callers only mention what matters.

2. **Priority of Checks**: Key lookup is checked first because a Map can also answer membership questions.

3. **Default Choice**: If nothing special is needed, a `List` is the simple, safe default.

4. **Local Function**: `pick` is declared inside `main`, which is perfectly valid Dart.

5. **Mental Model**: Real choices involve trade-offs, but this decision order is a great starting point.

---

## 🔄 Same Data, Different Structures

To really feel the difference, let's store the **same** student scores three ways and answer the same questions.

```dart
import 'dart:collection';

void main() {
  print('🎓 STUDENT SCORES, THREE WAYS 🎓\n');

  final raw = {'Zoe': 88, 'Ali': 95, 'Mia': 72, 'Ben': 95, 'Kai': 60};

  // 1. List of records: keeps insertion order
  final asList = raw.entries.map((e) => (e.key, e.value)).toList();

  // 2. Map: instant lookup by name
  final asMap = Map<String, int>.from(raw);

  // 3. SplayTreeMap: always sorted by name
  final asSorted = SplayTreeMap<String, int>.from(raw);

  // Question 1: What did Mia score?
  final miaFromList = asList.firstWhere((s) => s.$1 == 'Mia').$2; // O(n)
  final miaFromMap = asMap['Mia']; // O(1)
  print('Mia (list): $miaFromList, Mia (map): $miaFromMap');

  // Question 2: Students in alphabetical order?
  print('Alphabetical: ${asSorted.keys.toList()}'); // already sorted

  // Question 3: First student alphabetically?
  print('First: ${asSorted.firstKey()}');

  // Question 4: Highest score?
  final best = asList.reduce((a, b) => a.$2 >= b.$2 ? a : b);
  print('Top scorer: ${best.$1} with ${best.$2}');
}
```

**🔍 What This Code Does:**

This code demonstrates **how the same data answers questions at different costs**:

1. **List of Records**: Finding Mia requires `firstWhere`, a linear scan, O(n).

2. **Map**: `asMap['Mia']` jumps straight to the value, O(1) on average.

3. **SplayTreeMap**: Keys are always kept **sorted**, so alphabetical order and `firstKey()` come for free.

4. **reduce for Maximum**: Finding the top score scans everything, O(n). Ties keep the first one found because of `>=`.

5. **The Lesson**: No structure is "best" at everything. Pick the one that makes your **most frequent** questions cheap.

---

## ⚠️ Common Mistakes

### 1. Using a List for frequent lookups

```dart
void main() {
  final banned = ['spam', 'scam', 'fake'];
  // ❌ O(n) per message word
  print(banned.contains('scam'));

  // ✅ O(1) average per message word
  final bannedSet = {'spam', 'scam', 'fake'};
  print(bannedSet.contains('scam'));
}
```

**🔍 What This Code Does:**

1. **Same Output**: Both print `true`.
2. **Different Cost**: The List scans; the Set hashes.
3. **Rule of Thumb**: If you call `.contains` in a loop, you probably want a `Set`.

### 2. Removing from the front of a List in a loop

```dart
import 'dart:collection';

void main() {
  final jobs = [1, 2, 3, 4, 5];
  // ❌ Each removeAt(0) shifts every remaining element
  while (jobs.isNotEmpty) {
    jobs.removeAt(0);
  }

  // ✅ Queue removes from the front in O(1)
  final queue = Queue<int>.from([1, 2, 3, 4, 5]);
  while (queue.isNotEmpty) {
    queue.removeFirst();
  }
  print('Done');
}
```

**🔍 What This Code Does:**

1. **List Front Removal**: `removeAt(0)` is O(n) because elements shift left.
2. **Queue Front Removal**: `removeFirst()` is O(1).
3. **Hidden n²**: Draining a List from the front costs O(n²) in total.

### 3. Sorting again and again

```dart
void main() {
  final scores = <int>[];
  for (final s in [50, 20, 80, 10]) {
    scores.add(s);
    scores.sort(); // ❌ Sorting after every insert
  }
  print(scores);
}
```

**🔍 What This Code Does:**

1. **Repeated Sorting**: Every `sort()` costs O(n log n).
2. **Better Options**: Sort **once** at the end, or use a `SplayTreeSet`/heap that stays ordered as you insert.
3. **Output**: `[10, 20, 50, 80]`, correct but wasteful.

---

## 🧪 Try It Yourself

1. **Duplicate Detector**: Given a list of email addresses, print the ones that appear more than once. Use a `Set` to track what you've seen.

2. **Word Counter**: Count how many times each word appears in a sentence using a `Map<String, int>`.

3. **Ticket Line**: Simulate 5 customers joining a `Queue` and being served in order.

4. **Benchmark**: Repeat the username example with 10,000, 100,000 and 1,000,000 usernames. Record the List and Set times in a table. What pattern do you see?

```dart
void main() {
  // Starter for exercise 1
  final emails = ['a@x.com', 'b@x.com', 'a@x.com', 'c@x.com', 'b@x.com'];
  final seen = <String>{};
  final duplicates = <String>{};

  for (final email in emails) {
    if (!seen.add(email)) {
      duplicates.add(email);
    }
  }

  print('Duplicates: $duplicates'); // {a@x.com, b@x.com}
}
```

**🔍 What This Code Does:**

1. **`seen.add` Returns a bool**: `false` means the email was already there.
2. **Second Set for Results**: `duplicates` is also a Set, so each duplicate is reported once even if it appears 5 times.
3. **Single Pass**: The whole check is O(n).

---

## 📌 Key Takeaways

- ✅ A **data structure** is a way to organize data so the operations you need are **efficient**.
- ✅ The **same data** can be stored in many ways; the right choice depends on **which questions you ask most**.
- ✅ `List` is great for **order and indexing**, `Set` for **uniqueness and membership**, `Map` for **key lookups**, `Queue` for **first-in-first-out**.
- ✅ We compare structures by **how their cost grows** with the amount of data (Big O), not by milliseconds.
- ✅ Real apps combine **several structures**, each doing what it's best at.
- ✅ Watch out for hidden costs: `contains` on a List, `removeAt(0)` in a loop, and repeated sorting.

**Next up:** 📏 **Big O: Time & Space**, the language we'll use to describe how fast (or slow) every structure is.
