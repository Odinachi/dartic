# LRU Cache

Imagine a small **desk** next to a huge **library** 📚.

- Fetching a book from the library takes 10 minutes. Grabbing one from your desk takes 2 seconds.
- Your desk only fits **5 books**.
- When you need a 6th, something has to go back to the library. Which one? The book you **haven't touched for the longest time**: you're probably done with it.

👉 That's an **LRU cache**:

> A **cache** keeps a limited number of recently used items in fast storage. An **LRU** (**L**east **R**ecently **U**sed) cache, when full, **evicts the item that was used longest ago**. Combining a **hash map** with a **doubly linked list** makes both `get` and `put` **O(1)**.

Caches are everywhere: image caches in Flutter apps, browser caches, database buffer pools, CPU caches, DNS caches and memoization.

---

## 🧠 What an LRU Cache Must Do

| Operation | Behavior | Target cost |
|-----------|----------|-------------|
| `get(key)` | Return the value (or null) **and mark it most recently used** | O(1) |
| `put(key, value)` | Insert or update **and mark it most recently used**; if over capacity, **evict the least recently used** | O(1) |

```text
capacity = 3, most recent on the left

put(A)  → [A]
put(B)  → [B, A]
put(C)  → [C, B, A]
get(A)  → [A, C, B]        (A becomes most recent)
put(D)  → [D, A, C]        (B was least recent → evicted)
get(B)  → null
```

---

## 🐢 Naive Attempts

### List only

```dart
void main() {
  // Most recent at the end. get = remove + add: O(n) because of the search and shift.
  final order = <String>['A', 'B', 'C'];
  order.remove('A'); // O(n) search + shift
  order.add('A');
  print(order); // [B, C, A]
}
```

**🔍 What This Code Does:**

1. **Order Is Easy**: The list keeps recency order.
2. **But Lookups Are O(n)**: Finding a key means scanning, and removing from the middle shifts elements.

### Map with timestamps

Storing `key → (value, lastUsedTime)` makes `get` O(1), but **eviction** must scan every entry to find the oldest time: O(n).

> We need **O(1) lookup** (a hash map) **and** **O(1) reordering** (a doubly linked list). So we combine them.

---

## 🏗️ Hash Map + Doubly Linked List

- The **linked list** keeps items in recency order: **most recent at the front**, **least recent at the back**.
- The **hash map** points from each key **directly to its list node**, so we can find a node and **unlink it in O(1)** (see **Doubly & Circular Linked Lists**).

```text
map:  A ─┐   B ─┐   C ─┐
         ▼      ▼      ▼
head ⇄ [A] ⇄ [C] ⇄ [B] ⇄ tail
      most recent    least recent
```

```dart
class _Node<K, V> {
  K? key;
  V? value;
  _Node<K, V>? prev, next;
  _Node([this.key, this.value]);
}

class LruCache<K, V> {
  final int capacity;
  final Map<K, _Node<K, V>> _map = {};
  final _head = _Node<K, V>(); // sentinel: most recent side
  final _tail = _Node<K, V>(); // sentinel: least recent side
  int hits = 0, misses = 0;

  LruCache(this.capacity) {
    if (capacity <= 0) throw ArgumentError.value(capacity, 'capacity', 'must be > 0');
    _head.next = _tail;
    _tail.prev = _head;
  }

  int get length => _map.length;

  V? get(K key) {
    final node = _map[key];
    if (node == null) {
      misses++;
      return null;
    }
    hits++;
    _moveToFront(node);
    return node.value;
  }

  void put(K key, V value) {
    final existing = _map[key];
    if (existing != null) {
      existing.value = value;
      _moveToFront(existing);
      return;
    }
    final node = _Node<K, V>(key, value);
    _map[key] = node;
    _addFront(node);
    if (_map.length > capacity) {
      final lru = _tail.prev!; // least recently used
      _unlink(lru);
      _map.remove(lru.key);
    }
  }

  void _addFront(_Node<K, V> n) {
    n.prev = _head;
    n.next = _head.next;
    _head.next!.prev = n;
    _head.next = n;
  }

  void _unlink(_Node<K, V> n) {
    n.prev!.next = n.next;
    n.next!.prev = n.prev;
  }

  void _moveToFront(_Node<K, V> n) {
    _unlink(n);
    _addFront(n);
  }

  List<K> get keysByRecency {
    final out = <K>[];
    for (var n = _head.next!; !identical(n, _tail); n = n.next!) {
      out.add(n.key as K);
    }
    return out;
  }
}

void main() {
  final cache = LruCache<String, int>(3);
  cache.put('A', 1);
  cache.put('B', 2);
  cache.put('C', 3);
  print(cache.keysByRecency); // [C, B, A]

  print(cache.get('A'));      // 1
  print(cache.keysByRecency); // [A, C, B]

  cache.put('D', 4);          // evicts B
  print(cache.keysByRecency); // [D, A, C]
  print(cache.get('B'));      // null

  cache.put('C', 30);         // update moves C to the front
  print(cache.keysByRecency); // [C, D, A]
  print('hits=${cache.hits} misses=${cache.misses}'); // hits=1 misses=1
}
```

**🔍 What This Code Does:**

This code demonstrates **an O(1) LRU cache**:

1. **Map → Node**: `_map[key]` finds the node in O(1) average.

2. **Sentinels**: `_head` and `_tail` are dummy nodes, so adding and removing never needs null checks for the ends.

3. **`get` Moves to Front**: A hit unlinks the node and re-adds it at the front: O(1) because the node knows its neighbors.

4. **`put` Updates or Inserts**: Existing keys are updated and moved to the front; new keys are added at the front.

5. **Eviction**: When over capacity, the node just before `_tail` is the least recently used; unlink it and remove its key from the map.

6. **Node Stores Its Key**: Needed so eviction can remove the right entry from the map.

7. **Hit/Miss Counters**: Useful for measuring how effective the cache is.

---

## 🎯 The Dart Shortcut: `LinkedHashMap`

Dart's default `Map` is a `LinkedHashMap`, which remembers **insertion order**, and removing then re-inserting a key moves it to the **end**. That's enough to build a compact LRU cache.

```dart
class SimpleLru<K, V> {
  final int capacity;
  final _map = <K, V>{}; // LinkedHashMap: iteration order = insertion order

  SimpleLru(this.capacity);

  V? get(K key) {
    final value = _map.remove(key);
    if (value == null) return null;
    _map[key] = value; // re-insert → becomes the most recent (last)
    return value;
  }

  void put(K key, V value) {
    _map.remove(key);
    _map[key] = value;
    if (_map.length > capacity) {
      _map.remove(_map.keys.first); // first = least recently used
    }
  }

  @override
  String toString() => _map.toString();
}

void main() {
  final cache = SimpleLru<String, String>(2);
  cache.put('home', '🏠');
  cache.put('profile', '👤');
  cache.get('home');           // home becomes most recent
  cache.put('settings', '⚙️'); // evicts profile
  print(cache);                // {home: 🏠, settings: ⚙️}
}
```

**🔍 What This Code Does:**

1. **Order for Free**: `LinkedHashMap` internally keeps entries in a linked order alongside its hash table.
2. **Touch = Remove + Insert**: Moves the key to the end (most recent).
3. **Evict the First Key**: `keys.first` is the least recently used. Getting the first key is O(1).
4. **Caveat**: `get` treats a stored `null` value as missing; store non-null values (or use `containsKey`).

> 💡 Building it by hand (previous section) is what interviews expect and what you need in languages without an ordered hash map. In Dart apps, the `LinkedHashMap` version is perfectly practical.

---

## 🧪 Using an LRU Cache for Memoization

Expensive computations or network calls can be cached, with LRU keeping memory bounded.

```dart
class SimpleLru<K, V> {
  final int capacity;
  final _map = <K, V>{};
  SimpleLru(this.capacity);

  V? get(K key) {
    final v = _map.remove(key);
    if (v != null) _map[key] = v;
    return v;
  }

  void put(K key, V value) {
    _map
      ..remove(key)
      ..[key] = value;
    if (_map.length > capacity) _map.remove(_map.keys.first);
  }
}

var expensiveCalls = 0;

String renderThumbnail(String url) {
  expensiveCalls++; // pretend this downloads and resizes an image
  return 'thumb($url)';
}

final _cache = SimpleLru<String, String>(2);

String thumbnail(String url) {
  final cached = _cache.get(url);
  if (cached != null) return cached;
  final result = renderThumbnail(url);
  _cache.put(url, result);
  return result;
}

void main() {
  for (final url in ['a.png', 'b.png', 'a.png', 'c.png', 'a.png', 'b.png']) {
    thumbnail(url);
  }
  print('expensive calls: $expensiveCalls'); // 4
}
```

**🔍 What This Code Does:**

1. **Check the Cache First**: A hit skips the expensive work.
2. **Fill on Miss**: Compute, then store.
3. **Trace with Capacity 2**: `a` miss, `b` miss, `a` hit, `c` miss (evicts `b`), `a` hit, `b` miss (evicts `c`): 4 expensive calls instead of 6.
4. **Bounded Memory**: Unlike a plain map, the cache never grows past its capacity.

---

## ⏱️ Adding Expiration (TTL)

Real caches often also drop entries that are **too old**, even if they're used often (e.g. stale API responses).

```dart
class TtlLru<K, V> {
  final int capacity;
  final Duration ttl;
  final DateTime Function() now;
  final _map = <K, (V, DateTime)>{};

  TtlLru(this.capacity, this.ttl, {DateTime Function()? clock})
      : now = clock ?? DateTime.now;

  V? get(K key) {
    final entry = _map.remove(key);
    if (entry == null) return null;
    final (value, storedAt) = entry;
    if (now().difference(storedAt) > ttl) return null; // expired: stays removed
    _map[key] = entry; // still fresh: mark most recent
    return value;
  }

  void put(K key, V value) {
    _map
      ..remove(key)
      ..[key] = (value, now());
    if (_map.length > capacity) _map.remove(_map.keys.first);
  }
}

void main() {
  var fakeTime = DateTime(2026, 1, 1, 12, 0, 0);
  final cache = TtlLru<String, int>(10, const Duration(minutes: 5), clock: () => fakeTime);

  cache.put('price:BTC', 100);
  fakeTime = fakeTime.add(const Duration(minutes: 3));
  print(cache.get('price:BTC')); // 100 (still fresh)
  fakeTime = fakeTime.add(const Duration(minutes: 3));
  print(cache.get('price:BTC')); // null (6 minutes old → expired)
}
```

**🔍 What This Code Does:**

1. **Store Timestamps**: Each entry is a record `(value, storedAt)`.
2. **Injectable Clock**: Passing a `clock` function makes the cache testable without waiting real minutes.
3. **Expired Entries Are Dropped on Access**: Lazy expiration keeps the code simple.
4. **Two Eviction Rules**: Too old (TTL) or least recently used (capacity).

---

## 🌍 Other Cache Eviction Policies

| Policy | Evicts | Good for |
|--------|--------|----------|
| **LRU** | Least recently **used** | General purpose; recent items likely reused |
| **LFU** | Least **frequently** used | Stable popularity (some items always hot) |
| **FIFO** | Oldest **inserted** | Simplicity |
| **TTL** | Entries older than a time limit | Data that goes stale (prices, tokens) |
| **Random** | A random entry | Very cheap, surprisingly decent |

> 💡 Flutter's `ImageCache` uses an LRU-style policy with limits on both **count** and **total bytes**.

---

## ⚠️ Common Mistakes

### 1. Forgetting to move an item on `get`

A read counts as a "use". If `get` doesn't move the item to the front, the cache becomes FIFO, not LRU.

### 2. Not storing the key in the node

At eviction time you have the tail node, and you need its key to remove it from the map.

### 3. Updating an existing key without moving it

`put` on an existing key must update the value **and** mark it most recently used.

### 4. Forgetting to remove evicted keys from the map

The map would keep pointing at nodes no longer in the list, leaking memory and returning stale values.

---

## 🧪 Try It Yourself

1. Add `remove(key)` and `clear()` to `LruCache`.
2. Make the cache evict by **total size** (each value has a byte size) instead of item count.
3. Implement an **LFU cache** in O(1) (hint: a map from frequency to a linked list of keys).
4. Measure the **hit rate** of an LRU cache of size 50 on 10,000 random accesses where 80% of requests go to 20% of the keys.

---

## 📌 Key Takeaways

- ✅ An **LRU cache** keeps a limited number of items and evicts the **least recently used** when full.
- ✅ **Hash map** (key → node) gives O(1) lookup; **doubly linked list** gives O(1) reordering and eviction.
- ✅ Both `get` and `put` **mark the item as most recently used**.
- ✅ Sentinel head/tail nodes remove edge cases; nodes store their **key** for eviction.
- ✅ In Dart, a `LinkedHashMap` with **remove + re-insert** is a compact LRU cache.
- ✅ Caches trade **memory for speed**; LRU keeps that memory **bounded**.

**Next up:** 🌸 **Bloom Filters & Skip Lists**: probabilistic structures that trade certainty for speed.
