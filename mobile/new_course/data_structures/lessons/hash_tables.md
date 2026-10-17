# Hash Tables from Scratch

Imagine a giant **coat check** 🧥 at a concert with 1,000 hooks.

- When you hand over your coat, the attendant doesn't search for an empty hook. They look at your **ticket number**, say **#427**, and hang it on hook **427**.
- When you come back, they go **straight** to hook 427. No searching through 1,000 coats! ⚡

But what if your "ticket" is your **name**, like "Ada"? The attendant needs a rule that turns "Ada" into a hook number, the same number **every time**.

👉 That's a **hash table**:

> A **hash table** stores key–value pairs in an array of **buckets**. A **hash function** turns each key into a number, which picks the bucket. Lookups, inserts and deletes are **O(1) on average**.

Dart's `Map` and `Set` are hash tables. In this lesson we'll build one ourselves to see exactly how they work.

---

## 🧠 The Big Idea in Three Steps

```text
  key ──▶ hash function ──▶ hash code ──▶ % capacity ──▶ bucket index
 "Ada"                      2090303          % 8              7
```

1. **Hash**: Turn the key into an integer (its **hash code**).
2. **Compress**: Map that integer into the range `0 .. capacity − 1`, usually with `%`.
3. **Store**: Put the entry in that bucket. To find it later, repeat steps 1 and 2.

Because steps 1–3 take constant time, finding a key doesn't depend on how many keys are stored. That's the magic. ✨

---

## 🔢 Hash Functions

A **hash function** must be:

| Property | Why it matters |
|----------|----------------|
| **Deterministic** | The same key must always give the same hash, or we'll look in the wrong bucket |
| **Fast** | We compute it on every lookup |
| **Well distributed** | Keys should spread evenly over buckets, so buckets stay small |
| **Consistent with `==`** | Equal keys **must** have equal hashes |

### Building a simple string hash

```dart
int simpleHash(String key) {
  var hash = 0;
  for (final unit in key.codeUnits) {
    hash = (hash * 31 + unit) & 0x7fffffff; // keep it positive and bounded
  }
  return hash;
}

void main() {
  for (final name in ['Ada', 'Bob', 'ada', 'Abd', 'Dart']) {
    final h = simpleHash(name);
    print('${name.padRight(5)} hash=$h  bucket=${h % 8}');
  }
}
```

**🔍 What This Code Does:**

1. **Polynomial Rolling Hash**: Each character's code unit is mixed in, and multiplying by 31 makes **position** matter, so `'Ada'` and `'daA'` differ.
2. **Masking With `0x7fffffff`**: Keeps the hash a non-negative 31-bit number so it never overflows into negatives.
3. **Case Sensitive**: `'Ada'` and `'ada'` produce different hashes, because they are different keys.
4. **Bucket Index**: `hash % 8` maps the hash into one of 8 buckets.
5. **31 Is a Classic Choice**: An odd prime that spreads values well (Java's `String.hashCode` uses it too).

### A terrible hash function (don't do this!)

```dart
int badHash(String key) => key.length; // ❌ many keys share a length

void main() {
  final names = ['Ada', 'Bob', 'Cy', 'Dan', 'Eve', 'Fay'];
  final buckets = List.generate(8, (_) => <String>[]);
  for (final n in names) {
    buckets[badHash(n) % 8].add(n);
  }
  for (var i = 0; i < buckets.length; i++) {
    if (buckets[i].isNotEmpty) print('bucket $i: ${buckets[i]}');
  }
}
```

**🔍 What This Code Does:**

1. **Length as Hash**: Every 3-letter name lands in the same bucket.
2. **Crowded Bucket**: Bucket 3 holds 5 names while most buckets are empty.
3. **Lookups Become Linear**: Finding `'Fay'` means scanning that crowded bucket, so performance degrades toward O(n).
4. **Lesson**: Distribution is everything.

---

## 🧺 Buckets and Collisions

Two different keys can land in the **same bucket**. That's a **collision**, and it's unavoidable: there are infinitely many possible strings but only a few buckets (the **pigeonhole principle** 🐦).

The simplest fix is **separate chaining**: each bucket holds a small **list** of entries.

```text
bucket 0: []
bucket 1: [("Bob", 25)]
bucket 2: []
bucket 3: [("Ada", 36), ("Eve", 29)]   ← collision, both live here
bucket 4: []
...
```

To find `"Eve"`: hash → bucket 3 → scan the (short) list for a key that is `==` to `"Eve"`.

> 💡 The next lesson covers collisions in depth, including **open addressing**. Here we'll use chaining because it's the easiest to understand.

---

## 🏗️ Building `MyHashMap<K, V>`

```dart
class _Entry<K, V> {
  final K key;
  V value;
  _Entry(this.key, this.value);
}

class MyHashMap<K, V> {
  static const _initialCapacity = 8;
  static const _maxLoadFactor = 0.75;

  List<List<_Entry<K, V>>> _buckets =
      List.generate(_initialCapacity, (_) => <_Entry<K, V>>[]);
  int _size = 0;

  int get length => _size;
  int get capacity => _buckets.length;
  double get loadFactor => _size / _buckets.length;

  int _indexFor(K key, int capacity) =>
      (key.hashCode & 0x7fffffff) % capacity;

  List<_Entry<K, V>> _bucketFor(K key) => _buckets[_indexFor(key, capacity)];

  /// Insert or update: O(1) average
  void put(K key, V value) {
    final bucket = _bucketFor(key);
    for (final e in bucket) {
      if (e.key == key) {
        e.value = value; // key exists: update
        return;
      }
    }
    bucket.add(_Entry(key, value));
    _size++;
    if (loadFactor > _maxLoadFactor) _resize();
  }

  /// Lookup: O(1) average
  V? get(K key) {
    for (final e in _bucketFor(key)) {
      if (e.key == key) return e.value;
    }
    return null;
  }

  bool containsKey(K key) => _bucketFor(key).any((e) => e.key == key);

  /// Delete: O(1) average
  V? remove(K key) {
    final bucket = _bucketFor(key);
    for (var i = 0; i < bucket.length; i++) {
      if (bucket[i].key == key) {
        _size--;
        return bucket.removeAt(i).value;
      }
    }
    return null;
  }

  void _resize() {
    final old = _buckets;
    _buckets = List.generate(old.length * 2, (_) => <_Entry<K, V>>[]);
    for (final bucket in old) {
      for (final e in bucket) {
        _buckets[_indexFor(e.key, _buckets.length)].add(e); // rehash
      }
    }
  }

  Iterable<K> get keys => _buckets.expand((b) => b.map((e) => e.key));

  String debug() {
    final out = StringBuffer();
    for (var i = 0; i < _buckets.length; i++) {
      final items = _buckets[i].map((e) => '${e.key}=${e.value}').join(', ');
      out.writeln('[$i] $items');
    }
    return out.toString();
  }
}

void main() {
  final ages = MyHashMap<String, int>();
  ages.put('Ada', 36);
  ages.put('Linus', 54);
  ages.put('Grace', 85);
  ages.put('Ada', 37); // update, not a new entry

  print(ages.get('Ada'));          // 37
  print(ages.get('Bjarne'));       // null
  print(ages.containsKey('Grace')); // true
  print(ages.remove('Linus'));     // 54
  print(ages.length);              // 2

  for (var i = 0; i < 10; i++) {
    ages.put('user$i', i);
  }
  print('size=${ages.length} capacity=${ages.capacity} '
      'load=${ages.loadFactor.toStringAsFixed(2)}');
}
```

**🔍 What This Code Does:**

This code demonstrates **a complete hash map using separate chaining**:

1. **Buckets**: A list of lists. Each inner list holds the entries whose keys hash to that index.

2. **`_indexFor`**: Uses Dart's built-in `key.hashCode`, masks off the sign bit, and compresses with `%`.

3. **`put` Updates or Inserts**: It first scans the bucket for an equal key (`==`). If found, it updates the value; otherwise it appends a new entry.

4. **`get` and `remove`**: Hash to the bucket, then scan only that bucket.

5. **Load Factor**: `size / capacity`. When it exceeds **0.75**, `_resize` doubles the bucket count.

6. **Rehashing**: Every entry must be **re-bucketed** after resizing, because `hash % capacity` changes when capacity changes.

7. **Generic Keys**: Works for any key type whose `==` and `hashCode` are consistent: `String`, `int`, records, or your own classes.

---

## ⚖️ Load Factor: The Speed Dial

The **load factor** (α) is the average number of entries per bucket:

```text
α = number of entries / number of buckets
```

| Load factor | Average bucket size | Effect |
|-------------|---------------------|--------|
| 0.25 | Tiny | ⚡ Fast but wastes memory |
| **0.75** | **< 1** | ✅ **Good balance (common default)** |
| 2.0 | 2 | 🐢 Slower lookups |
| 10.0 | 10 | 🐌 Basically a list scan |

Keeping α below a constant means each bucket has O(1) entries **on average**, so every operation is **O(1) on average**.

### Why resizing is still O(1) amortized

A resize rehashes all `n` entries, which is O(n). But because we **double** the capacity, resizes become rarer as the table grows, exactly like `List.add` in **Amortized Analysis**. Total cost of `n` inserts: O(n), so **O(1) amortized** each.

```dart
void main() {
  var capacity = 8;
  var resizes = 0;
  var rehashed = 0;
  for (var size = 1; size <= 10000; size++) {
    if (size / capacity > 0.75) {
      rehashed += size;
      capacity *= 2;
      resizes++;
    }
  }
  print('resizes: $resizes, total rehashed: $rehashed');
  print('rehash work per insert: ${(rehashed / 10000).toStringAsFixed(2)}');
}
```

**🔍 What This Code Does:**

1. **Simulates Inserts**: Counts how often the table would resize while growing to 10,000 entries.
2. **Few Resizes**: Only about 11 resizes are needed thanks to doubling.
3. **Small Constant**: The extra rehash work per insert stays around 1.2, a constant no matter how large the table gets.

---

## 🧷 `hashCode` and `==`: The Contract Again

Our `MyHashMap` relies on two methods every Dart object has:

- `hashCode` picks the **bucket**
- `==` finds the **exact entry** inside the bucket

If `a == b` but `a.hashCode != b.hashCode`, the map looks in the **wrong bucket** and never finds the key.

```dart
class Coord {
  final int x, y;
  const Coord(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      other is Coord && other.x == x && other.y == y;

  @override
  int get hashCode => Object.hash(x, y);
}

void main() {
  final treasure = <Coord, String>{const Coord(3, 4): '💎'};
  print(treasure[Coord(3, 4)]); // 💎 (a different object, but equal)

  // Records already have value-based == and hashCode:
  final grid = <(int, int), String>{(3, 4): '💎'};
  print(grid[(3, 4)]); // 💎
}
```

**🔍 What This Code Does:**

1. **Value Equality**: Two `Coord(3, 4)` objects are `==`.
2. **Matching Hashes**: `Object.hash(x, y)` gives equal coordinates equal hash codes.
3. **Lookup Works**: The map hashes the new object to the same bucket and finds the equal key.
4. **Records Are Easier**: `(int, int)` records get correct `==` and `hashCode` automatically.

---

## 🎯 Hash Sets: A Map Without Values

A **hash set** is a hash table that stores only keys. It answers *"Is this in the collection?"* in O(1) average.

```dart
class MyHashSet<T> {
  List<List<T>> _buckets = List.generate(8, (_) => <T>[]);
  int _size = 0;

  int _index(T item, int cap) => (item.hashCode & 0x7fffffff) % cap;

  bool add(T item) {
    final bucket = _buckets[_index(item, _buckets.length)];
    if (bucket.contains(item)) return false; // already present
    bucket.add(item);
    _size++;
    if (_size > _buckets.length * 0.75) _resize();
    return true;
  }

  bool contains(T item) =>
      _buckets[_index(item, _buckets.length)].contains(item);

  bool remove(T item) {
    final removed = _buckets[_index(item, _buckets.length)].remove(item);
    if (removed) _size--;
    return removed;
  }

  int get length => _size;

  void _resize() {
    final old = _buckets;
    _buckets = List.generate(old.length * 2, (_) => <T>[]);
    for (final b in old) {
      for (final item in b) {
        _buckets[_index(item, _buckets.length)].add(item);
      }
    }
  }
}

void main() {
  final tags = MyHashSet<String>();
  print(tags.add('dart'));    // true
  print(tags.add('flutter')); // true
  print(tags.add('dart'));    // false (duplicate)
  print(tags.contains('flutter')); // true
  print(tags.remove('dart'));      // true
  print(tags.length);              // 1
}
```

**🔍 What This Code Does:**

1. **Same Bucket Logic**: Hash, compress, then look only inside one small bucket.
2. **`add` Returns a bool**: `false` means the item was already there, matching Dart's `Set.add`.
3. **Duplicates Impossible**: The bucket check prevents storing equal items twice.
4. **Resizing**: Keeps the load factor under 0.75.

---

## 📊 Complexity Summary

| Operation | Average | Worst case (everything in one bucket) |
|-----------|---------|----------------------------------------|
| `put` / `add` | **O(1)** amortized | O(n) |
| `get` / `contains` | **O(1)** | O(n) |
| `remove` | **O(1)** | O(n) |
| Iterate all entries | O(n + capacity) | O(n + capacity) |
| Memory | O(n + capacity) | O(n + capacity) |

> ⚠️ The worst case happens with a **bad hash function** or **malicious keys** chosen to collide. Real implementations use well-mixed hash functions, and some randomize hashes per program run to defend against attacks.

---

## 🌍 Where Hash Tables Shine

| Use | Example |
|-----|---------|
| Caches | Remember results of expensive calls (memoization) |
| Indexing | Find a user by ID or email |
| Counting | Word frequencies, vote tallies |
| De-duplication | Unique visitors, seen nodes in a graph |
| Grouping | Orders by customer, files by extension |
| Joins | Match records from two lists by a shared key |

```dart
void main() {
  final orders = [
    (id: 1, customer: 'ada', total: 30),
    (id: 2, customer: 'bob', total: 12),
    (id: 3, customer: 'ada', total: 18),
  ];

  // Index by id: O(1) lookups later
  final byId = {for (final o in orders) o.id: o};
  print(byId[3]?.total); // 18

  // Group by customer
  final byCustomer = <String, List<int>>{};
  for (final o in orders) {
    byCustomer.putIfAbsent(o.customer, () => []).add(o.id);
  }
  print(byCustomer); // {ada: [1, 3], bob: [2]}
}
```

**🔍 What This Code Does:**

1. **Named Records**: `(id: 1, customer: 'ada', total: 30)` creates a record with named fields.
2. **Index With a Map Comprehension**: `{for (...) o.id: o}` builds an id → order lookup in O(n).
3. **`putIfAbsent`**: Creates the list the first time a customer appears, then returns it so we can `add`.
4. **Grouping in One Pass**: O(n) total.

---

## ⚠️ Common Mistakes

### 1. Mutable keys

If a key's fields change after insertion, its `hashCode` changes, and the map can't find it anymore. Keep keys **immutable**.

### 2. Expecting order

```dart
import 'dart:collection';

void main() {
  final h = HashMap<String, int>();
  h['zebra'] = 1;
  h['apple'] = 2;
  h['mango'] = 3;
  print(h.keys); // order is NOT guaranteed

  final linked = <String, int>{'zebra': 1, 'apple': 2, 'mango': 3};
  print(linked.keys); // (zebra, apple, mango): insertion order
}
```

**🔍 What This Code Does:**

1. **`HashMap`**: A pure hash table; iteration order depends on hashes and capacity.
2. **Default `{}` Map**: A `LinkedHashMap`, which also remembers insertion order (next lessons).
3. **Rule**: Never rely on `HashMap`'s iteration order.

### 3. Searching by value

`map.containsValue(v)` is **O(n)**: hashing only helps for **keys**. If you look up by value often, keep a second map keyed by that value.

### 4. Forgetting to rehash on resize

When capacity changes, every entry's bucket index changes too. Copying buckets as-is would put entries in the wrong places.

---

## 🧪 Try It Yourself

1. Add `operator []` and `operator []=` to `MyHashMap` so you can write `map['Ada'] = 36`.
2. Add a `values` getter and an `entries` getter.
3. Print the bucket sizes of `MyHashMap` after inserting 1,000 keys. How many buckets are empty? What's the largest bucket?
4. Use the bad length-based hash from earlier with 1,000 keys and compare the largest bucket size.

```dart
void main() {
  // Starter for exercise 3: measure distribution using Dart's real hashCode
  const capacity = 1024;
  final sizes = List<int>.filled(capacity, 0);
  for (var i = 0; i < 1000; i++) {
    sizes[('key$i'.hashCode & 0x7fffffff) % capacity]++;
  }
  final empty = sizes.where((s) => s == 0).length;
  final largest = sizes.reduce((a, b) => a > b ? a : b);
  print('empty buckets: $empty, largest bucket: $largest');
}
```

**🔍 What This Code Does:**

1. **Counts per Bucket**: Simulates where 1,000 keys land among 1,024 buckets.
2. **Distribution Check**: A good hash leaves many buckets with 0 or 1 entries and keeps the largest bucket small.
3. **Experiment**: Swap in your own hash function to compare.

---

## 📌 Key Takeaways

- ✅ A **hash table** maps keys to **buckets** using `hash(key) % capacity`.
- ✅ A good **hash function** is deterministic, fast, well distributed and consistent with `==`.
- ✅ **Collisions** are unavoidable; **separate chaining** stores colliding entries in a per-bucket list.
- ✅ The **load factor** (entries ÷ buckets) controls speed; resizing with **doubling** keeps operations **O(1) amortized**.
- ✅ Resizing requires **rehashing** every entry.
- ✅ Average **O(1)** for get, put and remove; worst case **O(n)** with terrible hashing.
- ✅ Keys must have consistent **`==` and `hashCode`** and should be **immutable**.

**Next up:** 💥 **Handling Collisions**: chaining vs open addressing, probing strategies and tombstones.
