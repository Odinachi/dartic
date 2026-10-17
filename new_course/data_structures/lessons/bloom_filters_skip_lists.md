# Bloom Filters & Skip Lists

Imagine a **nightclub bouncer** 🕶️ with a terrible memory but a clever trick. Instead of remembering every banned person's face, he remembers a few **features** for each: hat color, shoe brand, eye color.

- If someone has **any** feature that's never been seen on a banned person, they're **definitely not** banned. ✅
- If **all** their features match banned people's features, they **might** be banned, so he checks the full list. 🤔

He never wrongly lets in a banned person, but occasionally double-checks an innocent one. And he needs almost no memory.

👉 That's a **Bloom filter**. And its cousin, the **skip list**, is like adding **express lanes** to a linked list.

> A **Bloom filter** is a tiny bit array that answers *"have I seen this?"* with **no false negatives** but some **false positives**, using a fraction of the memory of a set.
> A **skip list** is a linked list with randomized **express layers** that give **O(log n)** expected search, insert and delete, a simpler alternative to balanced trees.

Both are **probabilistic** data structures: they use **randomness** or **approximation** to gain speed and simplicity.

---

## 🌸 Part 1: Bloom Filters

### How it works

- A bit array of **m** bits, all starting at 0.
- **k** different hash functions, each mapping an item to a position in `0..m−1`.
- **Add** an item: set the k bits it hashes to.
- **Query** an item: if **any** of its k bits is 0 → **definitely not present**. If **all** are 1 → **probably present**.

```text
m = 16 bits, k = 3 hash functions

add("cat") → bits 2, 7, 11
add("dog") → bits 4, 7, 13

bits: 0 0 1 0 1 0 0 1 0 0 0 1 0 1 0 0
          ↑   ↑     ↑       ↑   ↑

query("cow") → bits 2, 9, 13 → bit 9 is 0 → definitely NOT present ✅
query("eel") → bits 4, 11, 13 → all 1 → "probably present" (false positive! 😬)
```

### Building one in Dart

```dart
import 'dart:typed_data';

class BloomFilter {
  final int m; // number of bits
  final int k; // number of hash functions
  final Uint8List _bits;

  BloomFilter(this.m, this.k) : _bits = Uint8List((m + 7) ~/ 8);

  // Derive k positions from two base hashes (double hashing)
  Iterable<int> _positions(String item) sync* {
    final h1 = _fnv1a(item);
    final h2 = _fnv1a('salt:$item') | 1; // odd, so steps cover all bits
    for (var i = 0; i < k; i++) {
      yield (h1 + i * h2) % m;
    }
  }

  static int _fnv1a(String s) {
    var hash = 0x811c9dc5;
    for (final unit in s.codeUnits) {
      hash ^= unit;
      hash = (hash * 0x01000193) & 0xffffffff; // keep it 32-bit
    }
    return hash;
  }

  void add(String item) {
    for (final p in _positions(item)) {
      _bits[p >> 3] |= 1 << (p & 7); // set bit p
    }
  }

  bool mightContain(String item) {
    for (final p in _positions(item)) {
      if (_bits[p >> 3] & (1 << (p & 7)) == 0) return false; // definitely absent
    }
    return true; // probably present
  }
}

void main() {
  final seen = BloomFilter(1000, 5);
  for (final url in ['dart.dev', 'flutter.dev', 'pub.dev']) {
    seen.add(url);
  }
  print(seen.mightContain('dart.dev'));    // true (really added)
  print(seen.mightContain('flutter.dev')); // true
  print(seen.mightContain('example.com')); // false (almost certainly)
}
```

**🔍 What This Code Does:**

This code demonstrates **a Bloom filter backed by a compact bit array**:

1. **`Uint8List` Bit Array**: Each byte holds 8 bits, so 1,000 bits need only 125 bytes.

2. **Bit Tricks**: `p >> 3` finds the byte (`p ~/ 8`), `p & 7` finds the bit within it (`p % 8`), and `1 << (p & 7)` is a mask for that bit.

3. **FNV-1a Hash**: A simple, fast string hash; masking with `0xffffffff` keeps it 32-bit.

4. **Double Hashing**: Positions `h1 + i·h2` simulate k independent hash functions from just two.

5. **No False Negatives**: Anything added has all its bits set, so `mightContain` always returns `true` for it.

6. **Possible False Positives**: Unrelated items can find all their bits already set by others.

### Measuring false positives

```dart
import 'dart:math';
import 'dart:typed_data';

class BloomFilter {
  final int m, k;
  final Uint8List bits;
  BloomFilter(this.m, this.k) : bits = Uint8List((m + 7) ~/ 8);

  int _h(String s, int seed) {
    var h = 0x811c9dc5 ^ seed;
    for (final u in s.codeUnits) {
      h = ((h ^ u) * 0x01000193) & 0xffffffff;
    }
    return h;
  }

  void add(String s) {
    for (var i = 0; i < k; i++) {
      final p = _h(s, i) % m;
      bits[p >> 3] |= 1 << (p & 7);
    }
  }

  bool mightContain(String s) {
    for (var i = 0; i < k; i++) {
      final p = _h(s, i) % m;
      if (bits[p >> 3] & (1 << (p & 7)) == 0) return false;
    }
    return true;
  }
}

void main() {
  const n = 1000; // items to insert
  for (final bitsPerItem in [4, 8, 16]) {
    final m = n * bitsPerItem;
    final k = max(1, (bitsPerItem * ln2).round()); // optimal k ≈ (m/n)·ln 2
    final f = BloomFilter(m, k);
    for (var i = 0; i < n; i++) {
      f.add('user$i');
    }
    var falsePositives = 0;
    for (var i = 0; i < 10000; i++) {
      if (f.mightContain('stranger$i')) falsePositives++;
    }
    final rate = falsePositives / 10000 * 100;
    print('$bitsPerItem bits/item, k=$k → ${rate.toStringAsFixed(2)}% false positives');
  }
}
```

**🔍 What This Code Does:**

1. **Seeded Hashes**: Mixing a different seed into the hash gives k independent-looking functions.
2. **Optimal k**: About `(m / n) × ln 2` hash functions minimizes false positives.
3. **Experiment**: Tests 10,000 items that were **never** added.
4. **Typical Results**: Roughly 15% at 4 bits/item, 2–3% at 8 bits/item, and about 0.1% at 16 bits/item.
5. **Memory Win**: Storing 1,000 strings in a `Set` takes kilobytes; 8 bits/item is just **1 KB**.

| Bits per item | Approx. false-positive rate |
|---------------|-----------------------------|
| 4 | ~15% |
| 8 | ~2% |
| 10 | ~1% |
| 16 | ~0.05–0.1% |

### Bloom filter properties

| Property | Bloom filter |
|----------|--------------|
| Add | O(k) |
| Query | O(k) |
| False negatives | ❌ Never |
| False positives | ✅ Possible (tunable) |
| Delete | ❌ Not supported (clearing a bit could erase other items) |
| Memory | A few bits per item, regardless of item size |
| List stored items | ❌ Impossible |

### Real-world uses

- 🌐 **Browsers** checking URLs against a malicious-site list before doing a slower full lookup
- 🗄️ **Databases** (Cassandra, RocksDB, Bigtable) skipping disk reads for keys that definitely aren't in a file
- 📧 **Spam filters** and **"have I already crawled this page?"** in web crawlers
- 🔑 Checking if a **username** is "probably taken" before hitting the database

```dart
// The typical pattern: a cheap filter in front of an expensive lookup
Future<bool> isTaken(String username, bool Function(String) bloomMightContain,
    Future<bool> Function(String) databaseLookup) async {
  if (!bloomMightContain(username)) return false; // fast, certain "no"
  return databaseLookup(username);                // rare, slow "maybe" check
}

void main() async {
  final taken = {'ada', 'linus'};
  var dbCalls = 0;
  Future<bool> db(String u) async {
    dbCalls++;
    return taken.contains(u);
  }

  bool bloom(String u) => u.length <= 5; // stand-in filter for the demo

  print(await isTaken('ada', bloom, db));            // true
  print(await isTaken('grace_hopper', bloom, db));   // false (no DB call)
  print('database calls: $dbCalls');                 // 1
}
```

**🔍 What This Code Does:**

1. **Filter First**: A "definitely not" answer skips the database entirely.
2. **Database Only on "Maybe"**: The rare positive answer is confirmed by the authoritative source.
3. **Function Parameters**: The filter and database lookup are injected, which keeps the demo testable.
4. **`async`/`await`**: The database check is asynchronous, like a real network call.

---

## ⏩ Part 2: Skip Lists

### The idea: express lanes

A sorted linked list has O(n) search: you must walk node by node. What if some nodes also had links that **skip ahead**?

```text
Level 3: head ─────────────────────────────▶ 50 ─────────────────▶ nil
Level 2: head ──────────▶ 20 ──────────────▶ 50 ─────────▶ 70 ───▶ nil
Level 1: head ──▶ 10 ──▶ 20 ──▶ 30 ──▶ 40 ──▶ 50 ──▶ 60 ──▶ 70 ──▶ nil

search(60): L3: 50 (≤60) → next is nil, drop down
            L2: 50 → 70 is too far, drop down
            L1: 50 → 60 ✅
```

- Every node is on level 1 (the full sorted list).
- Each node is **randomly promoted** to higher levels: with probability ½ it reaches level 2, ¼ level 3, and so on.
- Search starts at the top-left and moves **right** while the next value is small enough, then **drops down** a level.

With random promotion, the expected height is **O(log n)** and each search takes **O(log n)** expected steps, without any rotations or rebalancing.

### Building a skip list

```dart
import 'dart:math';

class _SkipNode {
  final int value;
  final List<_SkipNode?> next; // next[i] = successor on level i
  _SkipNode(this.value, int levels) : next = List.filled(levels, null);
}

class SkipList {
  static const maxLevel = 16;
  final _head = _SkipNode(-1 << 62, maxLevel); // sentinel smaller than everything
  final Random _rnd;
  int _level = 1; // levels currently in use
  int length = 0;

  SkipList([int seed = 42]) : _rnd = Random(seed);

  int _randomLevel() {
    var lvl = 1;
    while (lvl < maxLevel && _rnd.nextBool()) {
      lvl++; // coin flip: promote with probability 1/2
    }
    return lvl;
  }

  bool contains(int value) {
    var node = _head;
    for (var i = _level - 1; i >= 0; i--) {
      while (node.next[i] != null && node.next[i]!.value < value) {
        node = node.next[i]!; // move right on this level
      }
    }                         // then drop down
    final candidate = node.next[0];
    return candidate != null && candidate.value == value;
  }

  void insert(int value) {
    final update = List<_SkipNode>.filled(maxLevel, _head);
    var node = _head;
    for (var i = _level - 1; i >= 0; i--) {
      while (node.next[i] != null && node.next[i]!.value < value) {
        node = node.next[i]!;
      }
      update[i] = node; // last node before `value` on level i
    }
    final lvl = _randomLevel();
    if (lvl > _level) _level = lvl;
    final fresh = _SkipNode(value, lvl);
    for (var i = 0; i < lvl; i++) {
      fresh.next[i] = update[i].next[i]; // splice in on each level
      update[i].next[i] = fresh;
    }
    length++;
  }

  bool remove(int value) {
    final update = List<_SkipNode>.filled(maxLevel, _head);
    var node = _head;
    for (var i = _level - 1; i >= 0; i--) {
      while (node.next[i] != null && node.next[i]!.value < value) {
        node = node.next[i]!;
      }
      update[i] = node;
    }
    final target = node.next[0];
    if (target == null || target.value != value) return false;
    for (var i = 0; i < target.next.length; i++) {
      update[i].next[i] = target.next[i]; // bypass on every level it appears
    }
    length--;
    return true;
  }

  List<int> toList() {
    final out = <int>[];
    for (var n = _head.next[0]; n != null; n = n.next[0]) {
      out.add(n.value);
    }
    return out;
  }
}

void main() {
  final list = SkipList();
  for (final v in [30, 10, 50, 20, 70, 40, 60]) {
    list.insert(v);
  }
  print(list.toList());       // [10, 20, 30, 40, 50, 60, 70]
  print(list.contains(40));   // true
  print(list.contains(45));   // false
  print(list.remove(30));     // true
  print(list.toList());       // [10, 20, 40, 50, 60, 70]
  print(list.length);         // 6
}
```

**🔍 What This Code Does:**

This code demonstrates **a skip list with randomized levels**:

1. **Multi-Level Nodes**: `next[i]` is the successor on level `i`; level 0 links every node in sorted order.

2. **Coin Flips**: `_randomLevel` keeps promoting while `nextBool()` is true, so about half the nodes reach level 2, a quarter reach level 3, and so on.

3. **Search**: From the highest level, move right while the next value is smaller; then drop a level. Ends just before the target on level 0.

4. **`update` Array**: Remembers the last node visited on each level, which is exactly where the new node must be spliced in (or the old one bypassed).

5. **Sentinel Head**: A node with a tiny value and all levels simplifies every loop.

6. **Seeded Random**: Makes the structure reproducible for testing.

### Skip list vs balanced BST

| | Skip list | Balanced BST (AVL / red-black) |
|---|-----------|--------------------------------|
| Search / insert / delete | O(log n) **expected** | O(log n) **worst case** |
| Balancing | Randomness (coin flips) | Rotations and recoloring |
| Code complexity | ✅ Simple | Tricky |
| Range scans | ✅ Walk level 0 in order | In-order traversal |
| Concurrency | ✅ Easier to make lock-free | Harder |
| Used in | Redis sorted sets, LevelDB/RocksDB memtables, Java's `ConcurrentSkipListMap` | `TreeMap`, `std::map` |

---

## 🎲 Probabilistic vs Deterministic

| Structure | What it trades | What it gains |
|-----------|----------------|---------------|
| **Bloom filter** | Certainty (false positives) | Huge memory savings |
| **Skip list** | Worst-case guarantees | Simplicity, concurrency |
| **Count-min sketch** | Exact counts (overestimates) | Tiny memory for frequency counts |
| **HyperLogLog** | Exact distinct counts | Counting billions of uniques in kilobytes |

> 💡 Probabilistic structures shine at **massive scale**: when exact answers would need too much memory or too much coordination, "almost always right" is often good enough.

---

## ⚠️ Common Mistakes

### 1. Trusting a Bloom filter "yes"

A positive answer means **maybe**. Always confirm with the real data source when correctness matters.

### 2. Removing items from a Bloom filter

Clearing bits can erase **other** items' bits, causing false negatives. Use a **counting Bloom filter** (small counters instead of bits) if you need deletes.

### 3. Sizing a Bloom filter too small

False positives rise quickly as the filter fills up. Size `m` for the expected number of items and the error rate you can accept.

### 4. Forgetting to raise the skip list's current level

If a new node is taller than the current level, the search must start from the new top level, or the new express links are never used.

---

## 🧪 Try It Yourself

1. Add a `falsePositiveEstimate(n)` method to `BloomFilter` using `(1 − e^(−k·n/m))^k`.
2. Build a **counting Bloom filter** that supports `remove`.
3. Add `range(lo, hi)` to `SkipList` returning all values in `[lo, hi]` in sorted order.
4. Insert 100,000 numbers into a `SkipList` and measure the average number of steps per `contains`. Compare with log₂(100,000) ≈ 17.

```dart
import 'dart:math';

double falsePositiveRate(int m, int k, int n) => pow(1 - exp(-k * n / m), k).toDouble();

void main() {
  print(falsePositiveRate(8000, 6, 1000).toStringAsFixed(4)); // ≈ 0.0216
}
```

**🔍 What This Code Does:**

1. **Probability a Bit Is Still 0**: About `e^(−k·n/m)` after n insertions.
2. **False Positive**: All k bits of a new item happen to be 1: `(1 − e^(−k·n/m))^k`.
3. **8 Bits per Item, k = 6**: About **2%**, matching the experiment above.

---

## 📌 Key Takeaways

- ✅ A **Bloom filter** uses a bit array and k hash functions to test membership with **no false negatives** and tunable **false positives**.
- ✅ Bloom filters use only a few **bits per item**, can't **delete** (without counting variants) and can't **list** their items.
- ✅ Use them as a **fast "definitely not" filter** in front of expensive lookups.
- ✅ A **skip list** adds randomly promoted **express levels** to a sorted linked list, giving **O(log n) expected** operations.
- ✅ Skip lists are **simpler** than balanced trees and great for **range scans** and **concurrency**.
- ✅ **Probabilistic** structures trade certainty or worst-case guarantees for **memory**, **speed** and **simplicity**.

**Next up:** 🧩 **Dynamic Programming Basics**: memoization and tabulation for overlapping subproblems.
