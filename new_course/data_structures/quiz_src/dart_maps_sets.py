QUESTIONS = [
    mcq(r"""
Which Map class does a `{}` map literal create by default?
""", ["LinkedHashMap", "HashMap", "SplayTreeMap", "UnmodifiableMapView"], "LinkedHashMap"),

    mcq(r"""
Which Set class does `{1, 2, 3}` create by default?
""", ["LinkedHashSet", "HashSet", "SplayTreeSet", "UnmodifiableSetView"], "LinkedHashSet"),

    mcq(r"""
Which map keeps keys in INSERTION order?
""", ["LinkedHashMap", "HashMap", "SplayTreeMap", "None of them"], "LinkedHashMap"),

    mcq(r"""
Which map keeps keys SORTED?
""", ["SplayTreeMap", "LinkedHashMap", "HashMap", "Map.unmodifiable"], "SplayTreeMap"),

    mcq(r"""
Which map makes NO guarantee about iteration order?
""", ["HashMap", "LinkedHashMap", "SplayTreeMap", "A const map"], "HashMap"),

    mcq(r"""
What is the cost of lookups in a `SplayTreeMap`?
""", ["O(log n) amortized", "O(1) average", "O(n)", "O(n log n)"], "O(log n) amortized"),

    mcq(r"""
What is the cost of lookups in a `LinkedHashMap`?
""", ["O(1) average", "O(log n)", "O(n)", "O(n²)"], "O(1) average"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<String, int>.from({'pear': 1, 'apple': 2, 'fig': 3});
  print(m.keys.toList());
}
```
""", ["[apple, fig, pear]", "[pear, apple, fig]", "[fig, apple, pear]", "[pear, fig, apple]"],
        "[apple, fig, pear]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'pear': 1, 'apple': 2, 'fig': 3};
  print(m.keys.toList());
}
```
""", ["[pear, apple, fig]", "[apple, fig, pear]", "[fig, apple, pear]", "Unpredictable"],
        "[pear, apple, fig]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <String, int>{'a': 1, 'b': 2};
  m['a'] = 10;
  print(m.keys.first);
}
```
""", ["a", "b", "10", "null"], "a"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <String, int>{'a': 1, 'b': 2};
  m.remove('a');
  m['a'] = 3;
  print(m.keys.toList());
}
```
""", ["[b, a]", "[a, b]", "[a]", "[b]"], "[b, a]"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<int, String>()
    ..[30] = 'c'
    ..[10] = 'a'
    ..[20] = 'b';
  print(m.firstKey());
  print(m.lastKey());
}
```
""", ["10 then 30", "30 then 20", "10 then 20", "30 then 10"], "10 then 30"),

    fill(r"""
Find the smallest key strictly greater than 15:

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<int, String>.from({10: 'a', 20: 'b', 30: 'c'});
  print(m.%fill%(15)); // 20
}
```
""", "firstKeyAfter"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<int, String>.from({10: 'a', 20: 'b', 30: 'c'});
  print(m.firstKeyAfter(20));
  print(m.lastKeyBefore(20));
}
```
""", ["30 then 10", "20 then 20", "30 then 20", "20 then 10"], "30 then 10"),

    mcq(r"""
What does `firstKeyAfter` return when there is no larger key?
""", ["null", "The last key", "-1", "It throws an error"], "null"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<int, String>((a, b) => b.compareTo(a));
  m[1] = 'x';
  m[3] = 'y';
  m[2] = 'z';
  print(m.keys.toList());
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "[1, 3, 2]", "[2, 3, 1]"], "[3, 2, 1]"),

    mcq(r"""
In a `SplayTreeMap`, when are two keys considered the same key?
""", ["When the comparator returns 0", "When they are identical objects",
       "When their hashCodes match", "Never; all keys are distinct"],
        "When the comparator returns 0"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<String, int>(
      (a, b) => a.toLowerCase().compareTo(b.toLowerCase()));
  m['Dart'] = 1;
  m['DART'] = 2;
  print(m.length);
  print(m['dart']);
}
```
""", ["1 then 2", "2 then 1", "1 then 1", "2 then null"], "1 then 2"),

    mcq(r"""
What must SplayTreeMap keys support if no comparator is given?
""", ["Comparable (compareTo)", "Only ==", "Only hashCode", "toString"],
        "Comparable (compareTo)"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final byAge = SplayTreeMap<(String, int), String>((a, b) => a.$2.compareTo(b.$2));
  byAge[('Ana', 30)] = 'x';
  byAge[('Ben', 30)] = 'y';
  print(byAge.length);
}
```
""", ["1", "2", "0", "It throws an error"], "1"),

    mcq(r"""
How do you keep both ('Ana', 30) and ('Ben', 30) in an age-sorted SplayTreeMap?
""", ["Break ties in the comparator, e.g. compare names when ages are equal",
       "Use a HashMap instead of the comparator", "Insert them in a different order",
       "Override hashCode on the record"],
        "Break ties in the comparator, e.g. compare names when ages are equal"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(['b', 'a', 'b', 'c', 'a'].toSet());
}
```
""", ["{b, a, c}", "{a, b, c}", "[b, a, c]", "{b, a, b, c, a}"], "{b, a, c}"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  print(SplayTreeSet<String>.from(['b', 'a', 'b', 'c', 'a']));
}
```
""", ["{a, b, c}", "{b, a, c}", "[a, b, c]", "{a, a, b, b, c}"], "{a, b, c}"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = {1, 2, 3};
  final b = {2, 3, 4};
  print(a.intersection(b));
}
```
""", ["{2, 3}", "{1, 2, 3, 4}", "{1}", "{4}"], "{2, 3}"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = {1, 2, 3};
  final b = {2, 3, 4};
  print(a.difference(b));
  print(b.difference(a));
}
```
""", ["{1} then {4}", "{4} then {1}", "{1, 4} then {1, 4}", "{} then {}"], "{1} then {4}"),

    mcq(r"""
What does this print?

```dart
void main() {
  print({1, 2}.union({2, 3}));
}
```
""", ["{1, 2, 3}", "{1, 2, 2, 3}", "{2}", "{1, 3}"], "{1, 2, 3}"),

    fill(r"""
Check that a set contains every element of another collection:

```dart
void main() {
  final skills = {'dart', 'sql', 'go'};
  print(skills.%fill%({'dart', 'go'})); // true
}
```
""", "containsAll"),

    mcq(r"""
How can you compute the symmetric difference of sets a and b?
""", ["a.union(b) minus a.intersection(b)", "a.difference(b)", "a.intersection(b)",
       "a.union(b)"], "a.union(b) minus a.intersection(b)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final stock = {'apples': 5};
  stock.update('apples', (v) => v + 1);
  stock.update('kiwis', (v) => v + 1, ifAbsent: () => 1);
  print(stock);
}
```
""", ["{apples: 6, kiwis: 1}", "{apples: 5, kiwis: 1}", "{apples: 6, kiwis: 2}",
       "It throws an error"], "{apples: 6, kiwis: 1}"),

    mcq(r"""
What happens with `map.update('missing', (v) => v + 1)` and no `ifAbsent`?
""", ["It throws an ArgumentError", "It inserts 1", "It returns null", "It does nothing"],
        "It throws an ArgumentError"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'a': 0};
  final v = m.putIfAbsent('a', () => 99);
  print(v);
}
```
""", ["0", "99", "null", "It throws an error"], "0"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'a': 1, 'b': 2, 'c': 3};
  m.removeWhere((k, v) => v.isOdd);
  print(m);
}
```
""", ["{b: 2}", "{a: 1, c: 3}", "{}", "{a: 1, b: 2, c: 3}"], "{b: 2}"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'a': 1, 'b': 2};
  final out = m.map((k, v) => MapEntry(k.toUpperCase(), v * 10));
  print(out);
}
```
""", ["{A: 10, B: 20}", "{a: 10, b: 20}", "[A, B]", "It throws an error"],
        "{A: 10, B: 20}"),

    order(r"""
Destructure map entries in a for loop:

```dart
void main() {
  final m = {'x': 1, 'y': 2};
  for (final %order%(:key, :value) in m.%order%) {
    print('$key=$value');
  }
}
```
""", ["MapEntry", "entries", "Record", "keys", "values"], ["MapEntry", "entries"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = Map.fromEntries([const MapEntry('a', 1), const MapEntry('b', 2)]);
  print(m['b']);
}
```
""", ["2", "1", "null", "b"], "2"),

    mcq(r"""
What does `HashSet.identity()` compare elements by?
""", ["Object identity (identical)", "== and hashCode", "toString", "compareTo"],
        "Object identity (identical)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = 'x' * 2;
  final b = 'x' * 2;
  final byValue = <String>{a, b};
  print(byValue.length);
}
```
""", ["1", "2", "0", "It throws an error"], "1"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final ci = HashMap<String, int>(
    equals: (a, b) => a.toLowerCase() == b.toLowerCase(),
    hashCode: (a) => a.toLowerCase().hashCode,
  );
  ci['Flutter'] = 3;
  print(ci['FLUTTER']);
}
```
""", ["3", "null", "It throws an error", "0"], "3"),

    mcq(r"""
When providing custom `equals` to a HashMap, what else must you provide consistently?
""", ["A hashCode function that agrees with equals", "A comparator", "A toString",
       "Nothing else"], "A hashCode function that agrees with equals"),

    mcq(r"""
What does `Map.unmodifiable(other)` create?
""", ["A copy that can never be changed", "A view that reflects changes to other",
       "A sorted copy", "A HashMap"], "A copy that can never be changed"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final live = <int>{1};
  final view = UnmodifiableSetView(live);
  live.add(2);
  print(view.length);
}
```
""", ["2", "1", "0", "It throws an error"], "2"),

    mcq(r"""
What happens when you call `add` on an `UnmodifiableSetView`?
""", ["It throws an UnsupportedError", "It adds to the underlying set",
       "It silently ignores it", "It returns false"], "It throws an UnsupportedError"),

    mcq(r"""
Why would a class expose an `UnmodifiableMapView` of its internal map?
""", ["So callers can read the data but not change the class's internal state",
       "To make the map faster", "To sort the map", "To copy the map"],
        "So callers can read the data but not change the class's internal state"),

    mcq(r"""
Which structure answers "cheapest item over $10" fastest?
""", ["SplayTreeMap<double, String> keyed by price with firstKeyAfter",
       "HashMap<double, String>", "List<String>", "LinkedHashSet<String>"],
        "SplayTreeMap<double, String> keyed by price with firstKeyAfter"),

    mcq(r"""
Which structure gives a simple LRU cache using remove-and-reinsert?
""", ["LinkedHashMap", "HashMap", "SplayTreeMap", "Set"], "LinkedHashMap"),

    mcq(r"""
What does this print?

```dart
void main() {
  final cache = <String, int>{};
  for (final k in ['a', 'b', 'c']) {
    cache[k] = k.codeUnitAt(0);
  }
  final v = cache.remove('a')!;
  cache['a'] = v;
  print(cache.keys.first);
}
```
""", ["b", "a", "c", "null"], "b"),

    mcq(r"""
What happens when removing keys inside `for (final k in map.keys)`?
""", ["It throws a ConcurrentModificationError", "It works fine",
       "It skips every other key", "It removes all keys"],
        "It throws a ConcurrentModificationError"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <String, int>{};
  print(m['missing'] ?? -1);
}
```
""", ["-1", "null", "0", "It throws an error"], "-1"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final s = SplayTreeSet<int>.from([5, 1, 9, 3]);
  print('${s.first} ${s.last}');
}
```
""", ["1 9", "5 3", "9 1", "1 5"], "1 9"),

    mcq(r"""
What does this print?

```dart
void main() {
  final yesterday = {'u1', 'u2', 'u3'};
  final today = {'u2', 'u3', 'u4'};
  print(today.difference(yesterday));
}
```
""", ["{u4}", "{u1}", "{u2, u3}", "{u1, u4}"], "{u4}"),

    mcq(r"""
`yesterday` and `today` are sets of active user IDs. Which expression gives users who were active yesterday but not today?
""", ["yesterday.difference(today)", "today.difference(yesterday)",
       "today.intersection(yesterday)", "today.union(yesterday)"],
        "yesterday.difference(today)"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = {'a': 1};
  print(m is LinkedHashMap);
  print(m is HashMap);
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Why is a splay tree's cost described as "amortized" O(log n)?
""", ["A single operation can be slow, but any sequence averages O(log n) each",
       "It is always exactly log n", "It depends on random input",
       "It is O(1) after sorting"],
        "A single operation can be slow, but any sequence averages O(log n) each"),

    mcq(r"""
What does a splay tree do to a key when it's accessed?
""", ["Moves it toward the root so repeated access is faster", "Deletes it",
       "Moves it to a leaf", "Copies it"], "Moves it toward the root so repeated access is faster"),

    mcq(r"""
What does this print?

```dart
void main() {
  const roles = {'admin', 'user'};
  print(roles.contains('guest'));
}
```
""", ["false", "true", "null", "It throws an error"], "false"),

    mcq(r"""
Which pick is best for "fast lookups, order doesn't matter, minimal memory"?
""", ["HashMap", "SplayTreeMap", "LinkedHashMap", "List of pairs"], "HashMap"),
]
