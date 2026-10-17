# Dart's Map & Set Family

Imagine three different **filing cabinets** 🗄️ for the same documents:

- 🎲 **Cabinet A:** Super fast, but documents end up in whatever drawer the system picks. Open it and the order looks random.
- 📋 **Cabinet B:** Just as fast, and it also remembers the **order** you filed things in.
- 🔤 **Cabinet C:** A little slower, but everything is always kept in **alphabetical order**, so "the first file after M" is instant to find.

👉 Dart gives you all three, for both maps and sets:

> **`HashMap` / `HashSet`**: pure hash tables, O(1) average, **no** order guarantee.
> **`LinkedHashMap` / `LinkedHashSet`**: hash tables that **remember insertion order**. This is what `{}` creates by default.
> **`SplayTreeMap` / `SplayTreeSet`**: self-balancing **trees** that keep keys **sorted**, O(log n) amortized.

Knowing which to pick, and the APIs that come with them, makes your code faster and clearer.

---

## 🗺️ The Map Family at a Glance

| Class | Order | Lookup / insert / remove | Extra powers |
|-------|-------|--------------------------|--------------|
| `HashMap` | ❌ Unspecified | O(1) average | Slightly less memory |
| `LinkedHashMap` (default `{}`) | ✅ Insertion order | O(1) average | Predictable iteration |
| `SplayTreeMap` | ✅ Sorted by key | O(log n) amortized | `firstKey`, `lastKey`, `firstKeyAfter`, `lastKeyBefore` |

All three implement the same `Map<K, V>` interface, so they're interchangeable in most code.

```dart
import 'dart:collection';

void main() {
  final entries = {'mango': 3, 'apple': 7, 'kiwi': 1, 'banana': 5};

  final hash = HashMap<String, int>.from(entries);
  final linked = LinkedHashMap<String, int>.from(entries);
  final sorted = SplayTreeMap<String, int>.from(entries);
  final literal = <String, int>{...entries};

  print('HashMap:       ${hash.keys}');    // some order, not guaranteed
  print('LinkedHashMap: ${linked.keys}');  // (mango, apple, kiwi, banana)
  print('SplayTreeMap:  ${sorted.keys}');  // (apple, banana, kiwi, mango)
  print('{} literal is a LinkedHashMap: ${literal is LinkedHashMap}'); // true
}
```

**🔍 What This Code Does:**

1. **Same Data, Three Maps**: Each class is built from the same entries with `.from`.
2. **`HashMap`**: Iteration order depends on hash codes and capacity, so never rely on it.
3. **`LinkedHashMap`**: Iterates in the order keys were first inserted.
4. **`SplayTreeMap`**: Iterates in sorted key order.
5. **Map Literals**: `{...}` creates a `LinkedHashMap`, which is why Dart maps "remember order" by default.

---

## 📋 LinkedHashMap: Order You Can Rely On

```dart
void main() {
  final scores = <String, int>{};
  scores['Zoe'] = 70;
  scores['Ali'] = 90;
  scores['Mia'] = 85;
  print(scores); // {Zoe: 70, Ali: 90, Mia: 85}

  scores['Zoe'] = 75;  // updating does NOT move the key
  print(scores.keys.first); // Zoe

  scores.remove('Zoe');
  scores['Zoe'] = 80;  // re-inserting puts it at the end
  print(scores); // {Ali: 90, Mia: 85, Zoe: 80}
}
```

**🔍 What This Code Does:**

1. **Insertion Order**: Keys appear in the order they were first added.
2. **Updates Keep Position**: Assigning a new value to an existing key leaves it where it was.
3. **Remove + Re-add Moves It**: Removing then inserting places the key at the end. (This trick is the basis of a simple LRU cache!)
4. **Same Speed as HashMap**: O(1) average for all operations, with a little extra memory to track order.

---

## 🔤 SplayTreeMap: Always Sorted

```dart
import 'dart:collection';

void main() {
  final events = SplayTreeMap<int, String>();
  events[1430] = '☕ Coffee break';
  events[900] = '🧑‍💻 Standup';
  events[1700] = '🏠 Go home';
  events[1200] = '🍔 Lunch';

  print(events.keys.toList()); // [900, 1200, 1430, 1700]
  print(events.firstKey());    // 900
  print(events.lastKey());     // 1700

  // "What's the next event after 12:30?"
  final next = events.firstKeyAfter(1230);
  print('$next → ${events[next]}'); // 1430 → ☕ Coffee break

  // "What was the last event before 12:00?"
  final prev = events.lastKeyBefore(1200);
  print('$prev → ${events[prev]}'); // 900 → 🧑‍💻 Standup
}
```

**🔍 What This Code Does:**

1. **Sorted Keys**: Keys come out in ascending order no matter how they were inserted.
2. **`firstKey` / `lastKey`**: The smallest and largest keys, O(log n).
3. **`firstKeyAfter(k)`**: The smallest key **strictly greater** than `k` (a "ceiling" query).
4. **`lastKeyBefore(k)`**: The largest key **strictly smaller** than `k` (a "floor" query).
5. **Range-Style Questions**: Things a hash map can't answer without scanning everything.

### Custom ordering with a comparator

```dart
import 'dart:collection';

void main() {
  // Descending order
  final leaderboard = SplayTreeMap<int, String>((a, b) => b.compareTo(a));
  leaderboard[120] = 'Ada';
  leaderboard[340] = 'Linus';
  leaderboard[250] = 'Grace';
  print(leaderboard); // {340: Linus, 250: Grace, 120: Ada}

  // Case-insensitive keys
  final dict = SplayTreeMap<String, String>(
      (a, b) => a.toLowerCase().compareTo(b.toLowerCase()));
  dict['banana'] = '🍌';
  dict['Apple'] = '🍎';
  dict['cherry'] = '🍒';
  print(dict.keys.toList()); // [Apple, banana, cherry]
  print(dict['APPLE']);      // 🍎 (keys equal when the comparator returns 0)
}
```

**🔍 What This Code Does:**

1. **Comparator Function**: `(a, b) => b.compareTo(a)` reverses the natural order.
2. **Equality Comes From the Comparator**: In a `SplayTreeMap`, two keys are the **same key** when `compare(a, b) == 0`, not when `==` says so.
3. **Case-Insensitive Lookup**: `'APPLE'` finds `'Apple'` because the comparator treats them as equal.
4. **Keys Must Be Comparable**: Without a comparator, keys must implement `Comparable` (like `int` and `String`).

> 💡 Why "splay"? A splay tree moves recently accessed keys toward the root, so repeated lookups of popular keys get faster. Any single operation can be slow, but sequences are **O(log n) amortized** (see **Amortized Analysis**).

---

## 🎯 The Set Family

| Class | Order | Operations | Created by |
|-------|-------|------------|------------|
| `HashSet` | ❌ Unspecified | O(1) average | `HashSet()` |
| `LinkedHashSet` | ✅ Insertion order | O(1) average | `{1, 2}`, `<T>{}`, `Set()` |
| `SplayTreeSet` | ✅ Sorted | O(log n) amortized | `SplayTreeSet()` |

```dart
import 'dart:collection';

void main() {
  final tags = ['flutter', 'dart', 'web', 'dart', 'mobile', 'flutter'];

  final ordered = tags.toSet();                     // LinkedHashSet
  final sorted = SplayTreeSet<String>.from(tags);   // sorted, unique

  print(ordered); // {flutter, dart, web, mobile}
  print(sorted);  // {dart, flutter, mobile, web}
  print(sorted.first); // dart
  print(sorted.last);  // web
}
```

**🔍 What This Code Does:**

1. **`toSet()`**: Removes duplicates and keeps first-seen order (it builds a `LinkedHashSet`).
2. **`SplayTreeSet.from`**: Removes duplicates **and** sorts.
3. **`first` / `last`**: On a sorted set, these are the smallest and largest elements.

### Set algebra

```dart
void main() {
  final aliceSkills = {'dart', 'sql', 'figma'};
  final bobSkills = {'dart', 'go', 'sql', 'docker'};

  print(aliceSkills.union(bobSkills));        // everything
  print(aliceSkills.intersection(bobSkills)); // {dart, sql}
  print(aliceSkills.difference(bobSkills));   // {figma}
  print(bobSkills.difference(aliceSkills));   // {go, docker}

  print(aliceSkills.containsAll({'dart', 'sql'})); // true

  // Symmetric difference: in one or the other, not both
  final eitherOnly = aliceSkills.union(bobSkills)
    ..removeAll(aliceSkills.intersection(bobSkills));
  print(eitherOnly); // {figma, go, docker}
}
```

**🔍 What This Code Does:**

1. **`union`**: All elements from both sets.
2. **`intersection`**: Only elements in both.
3. **`difference`**: Elements in this set that aren't in the other. Order matters!
4. **`containsAll`**: Whether every given element is present.
5. **Symmetric Difference**: Union minus intersection, built with a cascade.
6. **Cost**: Each operation is O(size of the sets involved) for hash sets.

---

## 🧰 Map API Power Tools

```dart
void main() {
  final stock = <String, int>{'apples': 5, 'pears': 0, 'plums': 12};

  // Read with a fallback
  print(stock['kiwis'] ?? 0); // 0

  // update: change an existing value (or insert with ifAbsent)
  stock.update('apples', (v) => v + 10);
  stock.update('kiwis', (v) => v + 1, ifAbsent: () => 1);

  // putIfAbsent: insert only if missing, returns the value either way
  final pears = stock.putIfAbsent('pears', () => 99);
  print(pears); // 0 (already existed)

  // removeWhere: bulk delete
  stock.removeWhere((name, qty) => qty == 0);

  // entries + records
  for (final MapEntry(:key, :value) in stock.entries) {
    print('$key: $value');
  }

  // Transform keys and values
  final upper = stock.map((k, v) => MapEntry(k.toUpperCase(), v));
  print(upper); // {APPLES: 15, PLUMS: 12, KIWIS: 1}

  // Build from entries or iterables
  final lengths = Map.fromIterable(['a', 'bb', 'ccc'], value: (s) => (s as String).length);
  final fromEntries = Map.fromEntries([const MapEntry('x', 1), const MapEntry('y', 2)]);
  print(lengths);     // {a: 1, bb: 2, ccc: 3}
  print(fromEntries); // {x: 1, y: 2}
}
```

**🔍 What This Code Does:**

1. **`??` Fallback**: `map[key]` returns `null` for missing keys.
2. **`update`**: Applies a function to an existing value; `ifAbsent` handles missing keys.
3. **`putIfAbsent`**: Doesn't overwrite existing values; perfect for grouping.
4. **`removeWhere`**: Deletes all entries matching a test, safely.
5. **`MapEntry` Pattern**: `for (final MapEntry(:key, :value) in ...)` destructures each entry.
6. **`map`**: Transforms entries into a new map.
7. **`Map.fromIterable` / `Map.fromEntries`**: Build maps from other collections.

---

## 🆔 Identity Maps and Custom Equality

Sometimes you want to compare keys **by object identity**, not by `==`, for example when tracking which exact objects you've visited.

```dart
import 'dart:collection';

class Node {
  final String name;
  Node(this.name);

  @override
  bool operator ==(Object other) => other is Node && other.name == name;

  @override
  int get hashCode => name.hashCode;
}

void main() {
  final a = Node('x');
  final b = Node('x'); // equal to a, but a different object

  final byValue = <Node>{a, b};
  print(byValue.length); // 1 (a == b)

  final byIdentity = HashSet<Node>.identity()..addAll([a, b]);
  print(byIdentity.length); // 2 (different objects)

  // Custom equality: case-insensitive string keys
  final ci = HashMap<String, int>(
    equals: (x, y) => x.toLowerCase() == y.toLowerCase(),
    hashCode: (x) => x.toLowerCase().hashCode,
  );
  ci['Dart'] = 1;
  print(ci['DART']); // 1
}
```

**🔍 What This Code Does:**

1. **Value Equality**: The normal Set treats `a` and `b` as the same element.
2. **`HashSet.identity()`**: Uses `identical` and `identityHashCode`, so distinct objects are distinct elements.
3. **Custom `equals` / `hashCode`**: `HashMap` lets you plug in your own rules without changing the key class.
4. **Consistency Still Matters**: The custom `hashCode` must agree with the custom `equals`.

---

## 🔒 Read-Only Maps and Sets

```dart
import 'dart:collection';

void main() {
  final config = Map<String, int>.unmodifiable({'timeout': 30, 'retries': 3});
  try {
    config['timeout'] = 60;
  } on UnsupportedError {
    print('config is read-only');
  }

  final live = <String>{'a'};
  final view = UnmodifiableSetView(live);
  live.add('b');      // the owner can still change it
  print(view);        // {a, b} (the view reflects changes)

  const roles = {'admin', 'user'}; // const sets are immutable too
  print(roles.contains('admin'));
}
```

**🔍 What This Code Does:**

1. **`Map.unmodifiable`**: A **copy** that can never change.
2. **`UnmodifiableSetView`**: A read-only **window** onto a set that its owner can still modify.
3. **`const` Collections**: Compile-time constant sets and maps are immutable.
4. **Design Tip**: Expose views from classes so callers can read but not modify internal state.

---

## 🧭 Choosing the Right One

| You need... | Use |
|-------------|-----|
| Fast lookups, order doesn't matter | `HashMap` / `HashSet` (or just `{}`) |
| Fast lookups **and** predictable insertion order | `{}` / `LinkedHashMap` / `LinkedHashSet` |
| Keys always sorted, min/max, "next after k" | `SplayTreeMap` / `SplayTreeSet` |
| Compare by object identity | `HashMap.identity()` / `HashSet.identity()` |
| Custom equality without changing the class | `HashMap(equals:, hashCode:)` |
| Read-only | `Map.unmodifiable`, `UnmodifiableMapView`, `const` |

```dart
import 'dart:collection';

void main() {
  // Real example: a price list where users ask "cheapest item over $10?"
  final byPrice = SplayTreeMap<double, String>()
    ..[4.99] = 'Pen'
    ..[12.50] = 'Notebook'
    ..[29.00] = 'Backpack'
    ..[10.00] = 'Mug';

  final key = byPrice.firstKeyAfter(10.0);
  print('Cheapest over \$10: ${byPrice[key]} (\$$key)'); // Notebook ($12.5)
}
```

**🔍 What This Code Does:**

1. **Cascade With Index Assignment**: `..[4.99] = 'Pen'` inserts entries in one expression.
2. **Strictly Greater**: `firstKeyAfter(10.0)` skips the $10.00 mug and finds $12.50.
3. **O(log n)**: A hash map would need to scan every price.

---

## ⚠️ Common Mistakes

### 1. Assuming `HashMap` keeps order

Only `LinkedHashMap` (the `{}` default) and `SplayTreeMap` define an iteration order.

### 2. Using `==`-based thinking with `SplayTreeMap`

Keys are deduplicated by the **comparator**. A comparator that returns 0 for different keys silently merges them.

```dart
import 'dart:collection';

void main() {
  // Sorting people by age only: two people of the same age collide!
  final byAge = SplayTreeMap<(String, int), String>((a, b) => a.$2.compareTo(b.$2));
  byAge[('Ana', 30)] = 'engineer';
  byAge[('Ben', 30)] = 'designer'; // same "key" as Ana, replaces her value
  print(byAge.length); // 1

  // ✅ Break ties with a second field
  final fixed = SplayTreeMap<(String, int), String>((a, b) {
    final byAgeCmp = a.$2.compareTo(b.$2);
    return byAgeCmp != 0 ? byAgeCmp : a.$1.compareTo(b.$1);
  });
  fixed[('Ana', 30)] = 'engineer';
  fixed[('Ben', 30)] = 'designer';
  print(fixed.length); // 2
}
```

**🔍 What This Code Does:**

1. **Comparator Equality**: Comparing only by age makes Ana and Ben "the same key".
2. **Tie-Breaker**: Comparing names when ages are equal keeps both entries.

### 3. Modifying a map while iterating it

```dart
void main() {
  final m = {'a': 1, 'b': 2, 'c': 3};
  // ❌ for (final k in m.keys) { if (m[k]! > 1) m.remove(k); }
  m.removeWhere((k, v) => v > 1); // ✅
  print(m); // {a: 1}
}
```

**🔍 What This Code Does:**

1. **Concurrent Modification**: Removing inside a loop over `keys` throws.
2. **`removeWhere`**: Does the same job safely.

### 4. Forgetting that `difference` isn't symmetric

`a.difference(b)` and `b.difference(a)` are usually different sets.

---

## 🧪 Try It Yourself

1. Build a **phone book** with `SplayTreeMap<String, String>` and print all contacts whose names start with a given letter using `firstKeyAfter`.
2. Use `LinkedHashMap` to build a tiny **LRU cache**: on every `get`, remove and re-insert the key; when over capacity, remove `keys.first`.
3. Given two lists of user IDs (yesterday and today), print **new**, **returning** and **lost** users with set operations.
4. Create a case-insensitive `HashSet<String>` of banned words.

---

## 📌 Key Takeaways

- ✅ `{}` creates a **`LinkedHashMap`** / **`LinkedHashSet`**: O(1) average **and** insertion order.
- ✅ **`HashMap` / `HashSet`** are pure hash tables with **no order guarantee**.
- ✅ **`SplayTreeMap` / `SplayTreeSet`** keep keys **sorted** with O(log n) amortized operations and support `firstKey`, `lastKey`, `firstKeyAfter`, `lastKeyBefore`.
- ✅ In sorted collections, key equality comes from the **comparator**; add tie-breakers.
- ✅ Sets support **union**, **intersection**, **difference** and **containsAll**.
- ✅ Use `update`, `putIfAbsent`, `removeWhere`, `entries` and `map` to write clean map code.
- ✅ Use **identity** collections or **custom equality** when `==` isn't what you need.

**Next up:** 🧩 **Hashing Patterns**: frequency counts, two-sum, grouping and more.
