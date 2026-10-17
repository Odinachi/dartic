QUESTIONS = [
    mcq(r"""
What does a hash function do in a hash table?
""", ["Turns a key into an integer used to pick a bucket", "Sorts the keys",
       "Encrypts the values", "Counts the entries"],
        "Turns a key into an integer used to pick a bucket"),

    mcq(r"""
How is a hash code usually turned into a bucket index?
""", ["hash % capacity", "hash * capacity", "hash ~/ 2", "capacity - hash"],
        "hash % capacity"),

    mcq(r"""
What is the average cost of get, put and remove in a hash table?
""", ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "O(1)"),

    mcq(r"""
What is the worst-case cost of a hash table lookup?
""", ["O(n), when every key lands in the same bucket", "O(1) always", "O(log n)", "O(n²)"],
        "O(n), when every key lands in the same bucket"),

    mcq(r"""
Which property is REQUIRED of a hash function?
""", ["Equal keys must produce equal hashes", "Every key must have a unique hash",
       "It must be slow to compute", "It must return a String"],
        "Equal keys must produce equal hashes"),

    mcq(r"""
What is a collision?
""", ["Two different keys mapping to the same bucket", "Two equal keys in one map",
       "A hash code that is negative", "A map running out of memory"],
        "Two different keys mapping to the same bucket"),

    mcq(r"""
Why are collisions unavoidable?
""", ["There are more possible keys than buckets (pigeonhole principle)",
       "Hash functions are random", "Dart's hashCode is broken", "Buckets are always full"],
        "There are more possible keys than buckets (pigeonhole principle)"),

    mcq(r"""
What is separate chaining?
""", ["Each bucket holds a list of the entries that hash to it",
       "Storing keys and values in two separate maps", "Linking maps together",
       "Moving to the next empty bucket"],
        "Each bucket holds a list of the entries that hash to it"),

    mcq(r"""
What does this print?

```dart
int simpleHash(String key) {
  var hash = 0;
  for (final u in key.codeUnits) {
    hash = (hash * 31 + u) & 0x7fffffff;
  }
  return hash;
}

void main() {
  print(simpleHash('a'));
  print(simpleHash('ab'));
}
```
""", ["97 then 3105", "97 then 98", "1 then 2", "97 then 195"], "97 then 3105"),

    mcq(r"""
Why does a good string hash multiply by a constant like 31 at each step?
""", ["So the position of each character affects the hash", "To make it slower",
       "To keep the hash small", "To sort characters"],
        "So the position of each character affects the hash"),

    mcq(r"""
What is wrong with using `key.length` as a hash function?
""", ["Many different keys share a length, so they all collide", "length can be negative",
       "It isn't deterministic", "It's too slow"],
        "Many different keys share a length, so they all collide"),

    fill(r"""
Mask off the sign bit so the hash is non-negative:

```dart
void main() {
  final h = 'Ada'.hashCode %fill% 0x7fffffff;
  print(h >= 0); // true
}
```
""", "&"),

    mcq(r"""
What is the load factor of a hash table?
""", ["Number of entries ÷ number of buckets", "Number of buckets ÷ number of entries",
       "The size of the largest bucket", "The time to resize"],
        "Number of entries ÷ number of buckets"),

    mcq(r"""
A table has 12 entries and 16 buckets. What is its load factor?
""", ["0.75", "1.33", "0.5", "12"], "0.75"),

    mcq(r"""
What is a common maximum load factor before resizing?
""", ["0.75", "10", "0.01", "100"], "0.75"),

    mcq(r"""
What happens when the load factor gets too high?
""", ["Buckets get longer and lookups slow down", "The table throws an error",
       "Keys are deleted", "Nothing; load factor doesn't matter"],
        "Buckets get longer and lookups slow down"),

    mcq(r"""
Why must every entry be rehashed when a hash table resizes?
""", ["The bucket index hash % capacity changes when capacity changes",
       "Hash codes expire", "Resizing sorts the keys", "To delete duplicates"],
        "The bucket index hash % capacity changes when capacity changes"),

    mcq(r"""
Why is put still O(1) amortized even though resizing is O(n)?
""", ["Doubling the capacity makes resizes rare, like a growable list",
       "Resizing happens in the background", "Resizing only copies one bucket",
       "It isn't; put is O(n)"],
        "Doubling the capacity makes resizes rare, like a growable list"),

    mcq(r"""
In a chaining hash map, `put` with an existing key should:
""", ["Update the existing entry's value", "Add a second entry with the same key",
       "Throw an error", "Ignore the new value"], "Update the existing entry's value"),

    mcq(r"""
Inside a bucket, which method finds the exact matching key?
""", ["== (equality)", "hashCode", "toString", "compareTo"], "== (equality)"),

    mcq(r"""
What do `hashCode` and `==` each do during a lookup?
""", ["hashCode picks the bucket; == finds the exact entry in it",
       "hashCode finds the entry; == picks the bucket", "Both pick the bucket",
       "Neither is used"], "hashCode picks the bucket; == finds the exact entry in it"),

    mcq(r"""
What does this print?

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
  final m = {const Coord(1, 2): 'gem'};
  print(m[Coord(1, 2)]);
}
```
""", ["gem", "null", "It throws an error", "Coord(1, 2)"], "gem"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <(int, int), String>{(0, 1): 'start'};
  print(m[(0, 1)]);
}
```
""", ["start", "null", "(0, 1)", "It throws an error"], "start"),

    mcq(r"""
Which key types work correctly in a hash map without extra code?
""", ["String, int and records", "Lists", "Any class without == override when compared by value",
       "StringBuffer"], "String, int and records"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <List<int>, String>{[1]: 'one'};
  print(m[[1]]);
}
```
""", ["null", "one", "[1]", "It throws an error"], "null"),

    mcq(r"""
What is a hash set?
""", ["A hash table that stores only keys", "A sorted list", "A map of maps",
       "A set that can contain duplicates"], "A hash table that stores only keys"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = <String>{};
  print(s.add('x'));
  print(s.add('x'));
}
```
""", ["true then false", "true then true", "false then true", "false then false"],
        "true then false"),

    mcq(r"""
What is the cost of `map.containsValue(v)`?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
Why is `containsValue` slow but `containsKey` fast?
""", ["Hashing only organizes entries by key", "Values are stored on disk",
       "containsValue sorts first", "They are the same speed"],
        "Hashing only organizes entries by key"),

    mcq(r"""
What does this print?

```dart
void main() {
  final orders = [(id: 1, who: 'ada'), (id: 2, who: 'bob'), (id: 3, who: 'ada')];
  final byWho = <String, List<int>>{};
  for (final o in orders) {
    byWho.putIfAbsent(o.who, () => []).add(o.id);
  }
  print(byWho['ada']);
}
```
""", ["[1, 3]", "[1]", "[3]", "null"], "[1, 3]"),

    fill(r"""
Create the list only the first time a key appears:

```dart
void main() {
  final groups = <String, List<int>>{};
  groups.%fill%('a', () => []).add(1);
  print(groups); // {a: [1]}
}
```
""", "putIfAbsent"),

    mcq(r"""
What does this print?

```dart
void main() {
  final users = [(id: 7, name: 'Ada'), (id: 9, name: 'Bob')];
  final byId = {for (final u in users) u.id: u.name};
  print(byId[9]);
}
```
""", ["Bob", "Ada", "null", "9"], "Bob"),

    mcq(r"""
How do you access a named record field like `(id: 1, who: 'ada')`?
""", ["record.id", "record.$1", "record['id']", "record.get('id')"], "record.id"),

    mcq(r"""
Is iteration order guaranteed for `HashMap` from `dart:collection`?
""", ["No", "Yes, insertion order", "Yes, sorted by key", "Yes, reverse insertion order"],
        "No"),

    mcq(r"""
Which map does the literal `{}` (with keys and values) create by default?
""", ["LinkedHashMap (keeps insertion order)", "HashMap (no order)",
       "SplayTreeMap (sorted)", "An unmodifiable map"],
        "LinkedHashMap (keeps insertion order)"),

    mcq(r"""
What goes wrong if you change a key object's fields (used in hashCode) after inserting it?
""", ["The map looks in the wrong bucket and can't find it", "The map re-sorts itself",
       "Dart throws immediately", "Nothing"],
        "The map looks in the wrong bucket and can't find it"),

    mcq(r"""
Why do some hash table implementations randomize hashing per program run?
""", ["To defend against attackers who choose keys that all collide",
       "To make lookups faster", "To save memory", "To keep keys sorted"],
        "To defend against attackers who choose keys that all collide"),

    order(r"""
Complete the bucket index calculation:

```dart
int indexFor(Object key, int capacity) =>
    (key.%order% & 0x7fffffff) %order% capacity;
```
""", ["hashCode", "%", "~/", "toString", "*"], ["hashCode", "%"]),

    order(r"""
Complete the chaining `get`:

```dart
V? get(K key) {
  %order% (final e in _bucketFor(key)) {
    if (e.key %order% key) return e.%order%;
  }
  return null;
}
```
""", ["for", "==", "value", "while", "!=", "key"], ["for", "==", "value"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final buckets = List.generate(4, (_) => <int>[]);
  for (final x in [1, 5, 9, 2]) {
    buckets[x % 4].add(x);
  }
  print(buckets[1]);
}
```
""", ["[1, 5, 9]", "[1]", "[2]", "[]"], "[1, 5, 9]"),

    mcq(r"""
Keys `[1, 5, 9, 2]` go into 4 buckets using `x % 4`. Which bucket is most crowded?
""", ["Bucket 1", "Bucket 0", "Bucket 2", "Bucket 3"], "Bucket 1"),

    mcq(r"""
What does this print?

```dart
void main() {
  var capacity = 8, size = 0;
  for (var i = 0; i < 7; i++) {
    size++;
    if (size / capacity > 0.75) capacity *= 2;
  }
  print(capacity);
}
```
""", ["16", "8", "32", "7"], "16"),

    mcq(r"""
Which use case is a natural fit for a hash map?
""", ["Counting word frequencies", "Keeping items in sorted order",
       "Finding the smallest item repeatedly", "Undo history"],
        "Counting word frequencies"),

    mcq(r"""
Which use case is a natural fit for a hash set?
""", ["Tracking visited nodes in a graph search", "Storing a leaderboard in rank order",
       "A FIFO print queue", "Reversing a string"],
        "Tracking visited nodes in a graph search"),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = <String, int>{};
  for (final w in 'a b a c a'.split(' ')) {
    counts[w] = (counts[w] ?? 0) + 1;
  }
  print(counts);
}
```
""", ["{a: 3, b: 1, c: 1}", "{a: 1, b: 1, c: 1}", "{c: 1, b: 1, a: 3}", "[a, b, c]"],
        "{a: 3, b: 1, c: 1}"),

    mcq(r"""
What is `Object.hash(x, y)` used for?
""", ["Combining several fields into one well-distributed hash code",
       "Encrypting objects", "Comparing two objects", "Converting objects to strings"],
        "Combining several fields into one well-distributed hash code"),

    mcq(r"""
What does iterating every entry of a chaining hash table cost?
""", ["O(n + capacity)", "O(1)", "O(log n)", "O(n²)"], "O(n + capacity)"),

    mcq(r"""
Which of these would make a hash map degrade to O(n) lookups?
""", ["A hashCode that returns the same value for every key",
       "A load factor of 0.5", "Using String keys", "Resizing by doubling"],
        "A hashCode that returns the same value for every key"),

    mcq(r"""
What does this print?

```dart
class Bad {
  final int v;
  Bad(this.v);
  @override
  bool operator ==(Object o) => o is Bad && o.v == v;
  @override
  int get hashCode => 1;
}

void main() {
  final s = {Bad(1), Bad(2), Bad(1)};
  print(s.length);
}
```
""", ["2", "3", "1", "It throws an error"], "2"),

    mcq(r"""
A class's `hashCode` always returns 1 but `==` is correct. Sets of it still behave correctly. What's the problem?
""", ["All items share one bucket, so operations become O(n)", "It allows duplicates",
       "It loses items", "It doesn't compile"],
        "All items share one bucket, so operations become O(n)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'a': 1};
  m['a'] = 2;
  m['b'] = 3;
  print('${m.length} ${m['a']}');
}
```
""", ["2 2", "3 2", "2 1", "3 1"], "2 2"),

    mcq(r"""
What does `map.remove(key)` return when the key isn't present?
""", ["null", "false", "-1", "It throws an error"], "null"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'x': 10};
  print(m.remove('x'));
  print(m.remove('x'));
}
```
""", ["10 then null", "true then false", "10 then 10", "null then null"], "10 then null"),

    mcq(r"""
What is the space complexity of a hash table with n entries and c buckets?
""", ["O(n + c)", "O(1)", "O(n²)", "O(log n)"], "O(n + c)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final seen = <int>{};
  final dups = [3, 1, 3, 2, 1].where((x) => !seen.add(x)).toList();
  print(dups);
}
```
""", ["[3, 1]", "[1, 2, 3]", "[3, 1, 2]", "[]"], "[3, 1]"),

    mcq(r"""
Which statement about two UNEQUAL keys is true?
""", ["They may have the same hash code (a collision)", "They must have different hash codes",
       "They can't be in the same map", "They always go to different buckets"],
        "They may have the same hash code (a collision)"),
]
