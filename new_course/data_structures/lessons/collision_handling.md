# Handling Collisions

Imagine a **cinema** 🎬 where every ticket has an assigned seat. But the box office made a mistake: **two people** got tickets for seat **H7**! 🎟️🎟️

There are two classic ways to sort this out:

- 🪑 **Option 1, chaining:** Bring a **folding chair** and put it next to H7. Seat H7 now holds a little group of people. To find someone, go to H7 and check the group.
- 🚶 **Option 2, open addressing:** The second person walks to the **next empty seat** (H8, H9...) using an agreed rule. To find them later, start at H7 and follow the same rule until you find them.

👉 Hash tables face exactly this problem:

> A **collision** happens when two different keys hash to the **same bucket**. **Separate chaining** stores colliding entries together in that bucket. **Open addressing** stores every entry directly in the array and **probes** for another free slot.

The strategy you pick changes memory use, speed and how deletion works.

---

## 💥 Collisions Are Inevitable

Even with a perfect hash function, collisions happen surprisingly early. This is the **birthday paradox** 🎂: with just **23** people in a room, there's a better than 50% chance two share a birthday (365 "buckets").

```dart
import 'dart:math';

double collisionChance(int people, int days) {
  var noCollision = 1.0;
  for (var i = 0; i < people; i++) {
    noCollision *= (days - i) / days;
  }
  return 1 - noCollision;
}

void main() {
  for (final n in [10, 23, 50, 70]) {
    final p = collisionChance(n, 365);
    print('$n people: ${(p * 100).toStringAsFixed(1)}% chance of a shared birthday');
  }

  // Simulate hashing 100 random keys into 1,000 buckets
  final rnd = Random(42);
  final used = <int>{};
  var collisions = 0;
  for (var i = 0; i < 100; i++) {
    if (!used.add(rnd.nextInt(1000))) collisions++;
  }
  print('Collisions with 100 keys in 1000 buckets: $collisions');
}
```

**🔍 What This Code Does:**

1. **Probability of No Collision**: Each new person must avoid every birthday already taken: `365/365 × 364/365 × 363/365 × ...`.
2. **Complement**: `1 − noCollision` is the chance of **at least one** shared birthday.
3. **Surprising Result**: 23 people already give about 50.7%; 70 people give over 99.9%.
4. **Simulation**: Even when only 10% of the buckets are used, a few collisions appear.
5. **Seeded Random**: `Random(42)` makes the simulation repeatable.

> 💡 Since collisions **will** happen, the question is never "how do I avoid them?" but "how do I handle them efficiently?"

---

## 🪑 Strategy 1: Separate Chaining

Each bucket holds a **collection** (usually a list or linked list) of all entries that hash there.

```text
index:  0       1                 2      3
      [ ]  [Ada→36, Eve→29]     [ ]  [Bob→25]
```

You built this in the previous lesson. Its properties:

| Aspect | Separate chaining |
|--------|-------------------|
| Load factor can exceed 1? | ✅ Yes, buckets just get longer |
| Deletion | ✅ Easy: remove from the bucket's list |
| Memory | Extra list/node objects per bucket |
| Cache friendliness | Weaker: entries are scattered in memory |
| Performance at high load | Degrades gracefully: average chain length = α |

```dart
void main() {
  // Expected average chain length = load factor α
  const buckets = 1000;
  for (final entries in [500, 1000, 3000]) {
    final chains = List<int>.filled(buckets, 0);
    for (var i = 0; i < entries; i++) {
      chains[('key$i'.hashCode & 0x7fffffff) % buckets]++;
    }
    final longest = chains.reduce((a, b) => a > b ? a : b);
    print('α=${(entries / buckets).toStringAsFixed(1)}  longest chain=$longest');
  }
}
```

**🔍 What This Code Does:**

1. **Counts Chain Lengths**: Hashes `entries` keys into 1,000 buckets.
2. **Average = α**: With 3,000 entries, each chain holds 3 entries on average.
3. **Longest Chain**: Stays small with a good hash function, even when α > 1.

---

## 🚶 Strategy 2: Open Addressing

All entries live **directly in one array**, with no lists. On a collision, we **probe** a sequence of other slots until we find a free one. Lookups follow the **same** probe sequence.

### Linear probing

Try the next slot, then the next: `i, i+1, i+2, ...` (wrapping around).

```dart
class LinearProbingMap<K, V> {
  List<K?> _keys = List.filled(8, null);
  List<V?> _values = List.filled(8, null);
  int _size = 0;

  int get length => _size;
  int _home(K key, int cap) => (key.hashCode & 0x7fffffff) % cap;

  void put(K key, V value) {
    if ((_size + 1) / _keys.length > 0.5) _resize(); // keep α ≤ 0.5
    var i = _home(key, _keys.length);
    while (_keys[i] != null) {
      if (_keys[i] == key) {
        _values[i] = value; // update existing key
        return;
      }
      i = (i + 1) % _keys.length; // probe the next slot
    }
    _keys[i] = key;
    _values[i] = value;
    _size++;
  }

  V? get(K key) {
    var i = _home(key, _keys.length);
    while (_keys[i] != null) { // an empty slot ends the search
      if (_keys[i] == key) return _values[i];
      i = (i + 1) % _keys.length;
    }
    return null;
  }

  void _resize() {
    final oldKeys = _keys, oldValues = _values;
    _keys = List.filled(oldKeys.length * 2, null);
    _values = List.filled(oldKeys.length * 2, null);
    _size = 0;
    for (var i = 0; i < oldKeys.length; i++) {
      final k = oldKeys[i];
      if (k != null) put(k, oldValues[i] as V);
    }
  }
}

void main() {
  final m = LinearProbingMap<int, String>();
  // On the Dart VM, 1, 9 and 17 all hash to slot 1 when capacity is 8
  m.put(1, 'one');
  m.put(9, 'nine');
  m.put(17, 'seventeen');
  print(m.get(9));  // nine
  print(m.get(17)); // seventeen
  print(m.get(25)); // null
  print(m.length);  // 3
}
```

**🔍 What This Code Does:**

This code demonstrates **open addressing with linear probing**:

1. **Two Parallel Arrays**: `_keys[i]` and `_values[i]` hold one entry; `null` means "empty slot".

2. **Home Slot**: The hash tells us where the key **would** go if there were no collisions.

3. **Probe on Collision**: If the slot is taken by a different key, try `i + 1`, wrapping with `%`.

4. **Lookup Follows the Same Path**: Start at the home slot and walk forward until we find the key or hit an **empty** slot, which proves the key isn't present.

5. **Low Load Factor**: Open addressing needs `α < 1` (there must be empty slots!) and works best around 0.5–0.7.

6. **Resize Re-Inserts**: Every key gets a new home slot in the bigger array.

```text
capacity 8, keys 1, 9, 17 (all hash to slot 1):

slot:   0    1    2    3    4 ...
      [   |  1 |  9 | 17 |   ]
            home  +1   +2
```

### The problem: primary clustering 🧱

Linear probing creates **clusters**: long runs of filled slots. Any key hashing into a cluster has to walk to its end, and then **extends** it, making the cluster even longer.

```dart
void main() {
  const cap = 20;
  final slots = List<int?>.filled(cap, null);
  var totalProbes = 0;

  // Insert keys whose home slots crowd around 5..7
  for (final key in [5, 6, 5, 7, 6, 5, 8, 5]) {
    var i = key % cap;
    var probes = 1;
    while (slots[i] != null) {
      i = (i + 1) % cap;
      probes++;
    }
    slots[i] = key;
    totalProbes += probes;
    print('insert $key → slot $i after $probes probe(s)');
  }
  print('cluster: ${slots.sublist(4, 14)}');
  print('average probes: ${totalProbes / 8}');
}
```

**🔍 What This Code Does:**

1. **Neighboring Homes**: Several keys want slots 5–8.
2. **Growing Run**: Each collision pushes the key further right, extending one continuous cluster.
3. **Rising Cost**: Later inserts need more and more probes.
4. **Lesson**: Linear probing is cache-friendly and simple, but sensitive to clustering at high load.

### Quadratic probing

Jump by growing squares: `i, i+1, i+4, i+9, ...`. This spreads colliding keys out and avoids primary clustering.

```dart
void main() {
  const cap = 16;
  const home = 3;
  final linear = [for (var j = 0; j < 6; j++) (home + j) % cap];
  final quadratic = [for (var j = 0; j < 6; j++) (home + j * j) % cap];
  print('linear probes:    $linear');    // [3, 4, 5, 6, 7, 8]
  print('quadratic probes: $quadratic'); // [3, 4, 7, 12, 3, 12]
}
```

**🔍 What This Code Does:**

1. **Linear**: Visits neighbors one by one, which is how clusters form.
2. **Quadratic**: Leaps further each time, scattering keys.
3. **Catch**: Quadratic probing may **revisit** slots (`3` and `12` repeat here) and miss empty ones unless the capacity and load factor are chosen carefully (for example, a prime capacity with α ≤ 0.5).

### Double hashing

Use a **second hash function** to choose the step size: `i, i+s, i+2s, ...` where `s = hash2(key)`. Keys with the same home slot usually get **different** step sizes, so their probe paths split apart.

```dart
int hash1(int key, int cap) => key % cap;
int hash2(int key) => 7 - (key % 7); // never 0

void main() {
  const cap = 13; // prime capacity
  for (final key in [5, 18, 31]) {
    final step = hash2(key);
    final probes = [for (var j = 0; j < 4; j++) (hash1(key, cap) + j * step) % cap];
    print('key $key: home ${hash1(key, cap)}, step $step, probes $probes');
  }
}
```

**🔍 What This Code Does:**

1. **Same Home Slot**: 5, 18 and 31 all hash to slot 5 with capacity 13.
2. **Different Steps**: `hash2` gives each key its own stride, so they spread out instead of piling up.
3. **Never Zero**: A step of 0 would probe the same slot forever, so `hash2` returns 1–7.
4. **Prime Capacity**: Ensures every step size eventually visits every slot.

| Probing | Sequence | Clustering | Cache-friendly |
|---------|----------|------------|----------------|
| Linear | `h, h+1, h+2...` | Primary clustering 😬 | ✅ Best |
| Quadratic | `h, h+1, h+4, h+9...` | Secondary clustering only | 🟡 OK |
| Double hashing | `h, h+s, h+2s...` | Minimal | ❌ Worst |

---

## 🪦 Deleting With Open Addressing: Tombstones

Deletion is the tricky part. If we simply set a slot back to `null`, we **break** the probe chain for keys that were placed **after** it.

```text
Insert 1, 9, 17 (all home slot 1):   [ _ | 1 | 9 | 17 | _ ]
Delete 9 by setting null:             [ _ | 1 | _ | 17 | _ ]
Look up 17: start at 1 → occupied, not 17 → slot 2 is EMPTY → stop. ❌ "not found"!
```

The fix is a **tombstone** 🪦: a special marker meaning "something used to be here, keep probing".

```dart
const _tombstone = Object();

class ProbingSet {
  List<Object?> _slots = List.filled(8, null);
  int _size = 0;

  int get length => _size;
  int _home(int key) => key % _slots.length;

  bool add(int key) {
    var i = _home(key);
    int? firstFree;
    while (_slots[i] != null) {
      if (_slots[i] == key) return false;            // already present
      if (identical(_slots[i], _tombstone)) firstFree ??= i; // reusable
      i = (i + 1) % _slots.length;
    }
    _slots[firstFree ?? i] = key;
    _size++;
    return true;
  }

  bool contains(int key) {
    var i = _home(key);
    while (_slots[i] != null) {              // tombstones do NOT stop the search
      if (_slots[i] == key) return true;
      i = (i + 1) % _slots.length;
    }
    return false;
  }

  bool remove(int key) {
    var i = _home(key);
    while (_slots[i] != null) {
      if (_slots[i] == key) {
        _slots[i] = _tombstone;               // mark, don't empty
        _size--;
        return true;
      }
      i = (i + 1) % _slots.length;
    }
    return false;
  }

  String debug() => _slots
      .map((s) => s == null ? '_' : identical(s, _tombstone) ? '🪦' : '$s')
      .join(' ');
}

void main() {
  final set = ProbingSet();
  set
    ..add(1)
    ..add(9)
    ..add(17);
  print(set.debug());        // _ 1 9 17 _ _ _ _
  set.remove(9);
  print(set.debug());        // _ 1 🪦 17 _ _ _ _
  print(set.contains(17));   // true (probing continues past the tombstone)
  set.add(25);               // reuses the tombstone slot
  print(set.debug());        // _ 1 25 17 _ _ _ _
}
```

**🔍 What This Code Does:**

1. **Unique Marker**: `const _tombstone = Object()` is a sentinel no real key can equal; we check it with `identical`.
2. **Remove Leaves a Tombstone**: The slot isn't empty, so later lookups keep probing past it.
3. **Lookups Skip Tombstones**: Only a truly empty (`null`) slot ends a search.
4. **Inserts Reuse Tombstones**: `firstFree` remembers the first tombstone seen, but we still scan to the end of the chain to make sure the key isn't already present.
5. **Cleanup**: Too many tombstones slow lookups down, so real implementations **rehash** periodically to clear them.

---

## ⚖️ Chaining vs Open Addressing

| | Separate chaining | Open addressing |
|---|-------------------|-----------------|
| Storage | Array of buckets + lists/nodes | One flat array |
| Max load factor | Can exceed 1 | Must stay < 1 (often ≤ 0.7) |
| Memory overhead | Per-entry node/list objects | Empty slots |
| Cache performance | Weaker | ✅ Better (especially linear probing) |
| Deletion | ✅ Simple | Needs tombstones (or backward-shift deletion) |
| Degradation at high load | Gradual | Sharp: probes explode near α = 1 |
| Used by | Java's `HashMap`, many textbooks | Python `dict`, Rust `HashMap`, Dart VM's maps (an open-addressing index table) |

```dart
void main() {
  // Expected probes for a successful search with linear probing ≈ ½(1 + 1/(1 − α))
  for (final a in [0.25, 0.5, 0.75, 0.9, 0.99]) {
    final probes = 0.5 * (1 + 1 / (1 - a));
    print('α=$a  expected probes ≈ ${probes.toStringAsFixed(1)}');
  }
}
```

**🔍 What This Code Does:**

1. **Knuth's Formula**: Gives the expected probe count for linear probing at load factor α.
2. **Fine at Moderate Load**: About 1.5 probes at α = 0.5.
3. **Explodes Near Full**: About 50 probes at α = 0.99, which is why open-addressing tables resize early.

---

## 🛡️ Hash Flooding Attacks

If an attacker knows your hash function, they can send thousands of keys that **all collide**, turning every O(1) lookup into O(n) and freezing a server. Defenses:

- 🎲 **Randomized (seeded) hashing**: a secret random seed per process, so attackers can't predict collisions.
- 🌳 **Tree-ified buckets**: Java's `HashMap` converts long chains into balanced trees, capping the worst case at O(log n).
- 🔒 **Limits**: cap the number of keys accepted in a request.

---

## ⚠️ Common Mistakes

### 1. Emptying a slot on delete in open addressing

Always use a tombstone (or shift later entries back). Setting `null` silently "loses" keys further down the probe chain.

### 2. Letting an open-addressing table get full

With no empty slots, a lookup for a missing key would probe **forever**. Resize well before α reaches 1.

### 3. A second hash that can return 0

In double hashing, a step of 0 means probing the same slot endlessly. Design `hash2` to always return at least 1.

### 4. Comparing hashes instead of keys

```dart
void main() {
  // Two different keys CAN share a hash code. Always confirm with ==.
  const a = 'Aa', b = 'BB';
  print('${a.hashCode == b.hashCode ? 'same' : 'different'} hash codes');
  print(a == b); // false: hash equality alone never proves key equality
}
```

**🔍 What This Code Does:**

1. **Hashes Can Match by Chance**: Collisions mean equal hash codes don't imply equal keys.
2. **`==` Is the Final Word**: Every bucket or probe check must compare the keys themselves.

---

## 🧪 Try It Yourself

1. Add `remove` to `LinearProbingMap` using tombstones, and make `put` reuse them.
2. Count the average number of probes for 1,000 random inserts at α = 0.5, 0.7 and 0.9. Compare with Knuth's formula.
3. Implement **backward-shift deletion** for linear probing: after removing, move later entries in the same cluster back into the gap, so no tombstones are needed.
4. Modify the clustering demo to use quadratic probing and compare the probe counts.

---

## 📌 Key Takeaways

- ✅ **Collisions** are unavoidable (birthday paradox); good tables handle them efficiently.
- ✅ **Separate chaining** keeps a list per bucket; simple deletion, load factor can exceed 1.
- ✅ **Open addressing** stores entries in one array and **probes** for free slots: **linear**, **quadratic** or **double hashing**.
- ✅ **Linear probing** is cache-friendly but suffers **primary clustering**.
- ✅ Open addressing needs **tombstones** for deletion, and must resize well before it's full.
- ✅ Equal hash codes never prove equal keys; always confirm with **`==`**.
- ✅ **Randomized hashing** and **tree-ified buckets** defend against hash-flooding attacks.

**Next up:** 🗂️ **Dart's Map & Set Family**: `HashMap`, `LinkedHashMap`, `SplayTreeMap` and when to use each.
