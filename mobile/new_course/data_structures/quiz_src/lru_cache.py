LRU = r"""class Lru<K, V> {
  final int capacity;
  final _map = <K, V>{};
  Lru(this.capacity);

  V? get(K key) {
    final v = _map.remove(key);
    if (v == null) return null;
    _map[key] = v;
    return v;
  }

  void put(K key, V value) {
    _map.remove(key);
    _map[key] = value;
    if (_map.length > capacity) _map.remove(_map.keys.first);
  }

  List<K> get order => _map.keys.toList();
}
"""

QUESTIONS = [
    mcq(r"""
What does LRU stand for?
""", ["Least Recently Used", "Last Read Unit", "Linked Recursive Update", "Lowest Rank Usage"],
        "Least Recently Used"),

    mcq(r"""
When an LRU cache is full and a new item arrives, which item is evicted?
""", ["The one used longest ago", "The newest one", "The largest one", "A random one"],
        "The one used longest ago"),

    mcq(r"""
Which two structures together give O(1) get and put in a classic LRU cache?
""", ["A hash map and a doubly linked list", "A heap and a stack", "Two arrays",
       "A binary search tree and a queue"], "A hash map and a doubly linked list"),

    mcq(r"""
What does the hash map store in a classic LRU cache?
""", ["key → the node in the linked list", "node → key", "recency → key", "Only the values"],
        "key → the node in the linked list"),

    mcq(r"""
Why is the linked list DOUBLY linked?
""", ["So any node can be unlinked in O(1) using its prev and next", "To save memory",
       "To sort keys", "Singly linked lists can't store values"],
        "So any node can be unlinked in O(1) using its prev and next"),

    mcq(r"""
Where is the most recently used item kept in the lesson's design?
""", ["At the front (right after the head sentinel)", "At the back", "In the middle",
       "In a separate array"], "At the front (right after the head sentinel)"),

    mcq(r"""
Where is the least recently used item found?
""", ["At the back (right before the tail sentinel)", "At the front", "In the map's first key",
       "Anywhere"], "At the back (right before the tail sentinel)"),

    mcq(r"""
What must `get(key)` do on a cache hit, besides returning the value?
""", ["Move the item to the most-recently-used position", "Delete the item",
       "Move it to the least-recently-used position", "Nothing else"],
        "Move the item to the most-recently-used position"),

    mcq(r"""
What happens if `get` doesn't move accessed items?
""", ["The cache behaves like FIFO instead of LRU", "It becomes faster and still LRU",
       "It throws an error", "It evicts everything"],
        "The cache behaves like FIFO instead of LRU"),

    mcq(r"""
Why does each list node also store its key?
""", ["So the evicted tail node's key can be removed from the map", "For sorting",
       "To compute hash codes", "It doesn't need to"],
        "So the evicted tail node's key can be removed from the map"),

    mcq(r"""
What is the purpose of head and tail sentinel nodes?
""", ["They remove special cases when adding or removing at the ends", "They store the capacity",
       "They count hits", "They hold the most popular items"],
        "They remove special cases when adding or removing at the ends"),

    mcq(r"""
With capacity 3: put A, put B, put C, get A, put D. Which key is evicted?
""", ["B", "A", "C", "D"], "B"),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
void main() {
  final c = Lru<String, int>(2);
  c.put('a', 1);
  c.put('b', 2);
  c.get('a');
  c.put('c', 3);
  print(c.order);
}
```
""", ["[a, c]", "[b, c]", "[a, b]", "[c, a]"], "[a, c]"),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
void main() {
  final c = Lru<String, int>(2);
  c.put('a', 1);
  c.put('b', 2);
  c.put('c', 3);
  print(c.get('a'));
  print(c.get('c'));
}
```
""", ["null then 3", "1 then 3", "null then null", "1 then null"], "null then 3"),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
void main() {
  final c = Lru<String, int>(2);
  c.put('x', 1);
  c.put('y', 2);
  c.put('x', 10);
  c.put('z', 3);
  print(c.order);
}
```
""", ["[x, z]", "[y, z]", "[x, y]", "[z, x]"], "[x, z]"),

    mcq(r"""
Why is 'x' kept when 'z' is added after `put('x', 10)` in a capacity-2 LRU (after x, y)?
""", ["Updating x made it the most recently used, so y became the LRU", "x has a larger value",
       "Keys are evicted alphabetically", "The cache ignores updates"],
        "Updating x made it the most recently used, so y became the LRU"),

    mcq(r"""
Which Dart Map preserves insertion order and can serve as a compact LRU?
""", ["LinkedHashMap (the default {} map)", "HashMap", "SplayTreeMap", "UnmodifiableMapView"],
        "LinkedHashMap (the default {} map)"),

    mcq(r"""
In the LinkedHashMap LRU, how is an item marked as most recently used?
""", ["Remove it and re-insert it, moving it to the end", "Call sort()", "Use putIfAbsent",
       "Change its hash code"], "Remove it and re-insert it, moving it to the end"),

    mcq(r"""
In the LinkedHashMap LRU, which key is the least recently used?
""", ["keys.first", "keys.last", "The smallest key", "A random key"], "keys.first"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = {'a': 1, 'b': 2, 'c': 3};
  final v = m.remove('a')!;
  m['a'] = v;
  print(m.keys.toList());
}
```
""", ["[b, c, a]", "[a, b, c]", "[c, b, a]", "[b, a, c]"], "[b, c, a]"),

    mcq(r"""
What is a weakness of the simple LinkedHashMap LRU's `get`?
""", ["It treats a stored null value the same as a missing key", "It's O(n)",
       "It evicts on every get", "It can't be generic"],
        "It treats a stored null value the same as a missing key"),

    mcq(r"""
What is the time complexity of get and put in a correctly built LRU cache?
""", ["O(1) average", "O(log n)", "O(n)", "O(n log n)"], "O(1) average"),

    mcq(r"""
Why is "a map with lastUsed timestamps" alone not enough for O(1) LRU?
""", ["Finding the oldest entry to evict requires scanning: O(n)", "Maps can't store timestamps",
       "Timestamps are too big", "It is enough"],
        "Finding the oldest entry to evict requires scanning: O(n)"),

    mcq(r"""
Why is "a List in recency order" alone not enough for O(1) LRU?
""", ["Finding and removing a key in the middle is O(n)", "Lists can't hold strings",
       "Lists are unordered", "It is enough"], "Finding and removing a key in the middle is O(n)"),

    mcq(r"""
What does a cache trade?
""", ["Memory for speed", "Speed for memory", "Correctness for speed", "Nothing"],
        "Memory for speed"),

    mcq(r"""
What does an LRU cache guarantee about memory compared to a plain memo Map?
""", ["It never holds more than `capacity` items", "It uses no memory",
       "It holds every computed result forever", "It doubles memory"],
        "It never holds more than `capacity` items"),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
var calls = 0;
final cache = Lru<int, int>(2);

int slowSquare(int x) {
  final hit = cache.get(x);
  if (hit != null) return hit;
  calls++;
  final r = x * x;
  cache.put(x, r);
  return r;
}

void main() {
  for (final x in [2, 3, 2, 4, 2, 3]) {
    slowSquare(x);
  }
  print(calls);
}
```
""", ["4", "3", "6", "5"], "4"),

    mcq(r"""
What is the hit rate of a cache with 30 hits and 10 misses?
""", ["75%", "30%", "25%", "300%"], "75%"),

    mcq(r"""
What does a TTL (time-to-live) policy add to a cache?
""", ["Entries expire after a fixed time, even if used often", "Entries never expire",
       "Entries are sorted by time", "Entries are evicted randomly"],
        "Entries expire after a fixed time, even if used often"),

    mcq(r"""
Why does the TTL cache in the lesson take a `clock` function parameter?
""", ["So tests can control time instead of waiting real minutes", "For speed",
       "Because DateTime.now doesn't exist", "To randomize expiry"],
        "So tests can control time instead of waiting real minutes"),

    mcq(r"""
What does this print?

```dart
void main() {
  final stored = DateTime(2026, 1, 1, 12, 0);
  final now = DateTime(2026, 1, 1, 12, 6);
  print(now.difference(stored) > const Duration(minutes: 5));
}
```
""", ["true", "false", "6", "It throws an error"], "true"),

    mcq(r"""
Which policy evicts the item used the FEWEST times?
""", ["LFU (least frequently used)", "LRU", "FIFO", "TTL"], "LFU (least frequently used)"),

    mcq(r"""
Which policy evicts the item INSERTED earliest, regardless of use?
""", ["FIFO", "LRU", "LFU", "TTL"], "FIFO"),

    mcq(r"""
When is LFU better than LRU?
""", ["When some items are consistently popular over long periods",
       "When access patterns change quickly", "Always", "Never"],
        "When some items are consistently popular over long periods"),

    mcq(r"""
Which Flutter class uses an LRU-style cache with count and byte limits?
""", ["ImageCache", "StreamController", "TextEditingController", "Navigator"], "ImageCache"),

    mcq(r"""
What should `put` do when the key already exists?
""", ["Update the value AND mark it most recently used", "Ignore the new value",
       "Insert a duplicate node", "Evict it"],
        "Update the value AND mark it most recently used"),

    mcq(r"""
What bug occurs if evicted keys aren't removed from the map?
""", ["The map keeps stale nodes, leaking memory and returning evicted values",
       "Nothing", "The list gets sorted", "get becomes O(log n)"],
        "The map keeps stale nodes, leaking memory and returning evicted values"),

    mcq(r"""
To move a node to the front of a doubly linked list with a head sentinel, what are the two phases?
""", ["Unlink it from its neighbors, then insert it right after head",
       "Delete it and create a new key", "Swap it with the tail", "Sort the list"],
        "Unlink it from its neighbors, then insert it right after head"),

    order(r"""
Complete eviction in the linked-list LRU:

```dart
if (map.length > %order%) {
  final lru = tail.%order%!;
  unlink(lru);
  map.%order%(lru.key);
}
```
""", ["capacity", "prev", "remove", "next", "length", "add"], ["capacity", "prev", "remove"]),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
void main() {
  final c = Lru<int, String>(1);
  c.put(1, 'one');
  c.put(2, 'two');
  print(c.get(1));
  print(c.get(2));
}
```
""", ["null then two", "one then two", "one then null", "null then null"], "null then two"),

    mcq(r"""
What should an LRU cache constructor do with capacity 0 or negative?
""", ["Reject it (e.g. throw an ArgumentError)", "Store unlimited items",
       "Store exactly one item", "Ignore it"], "Reject it (e.g. throw an ArgumentError)"),

    mcq(r"""
Which pattern does an LRU-backed `thumbnail(url)` function implement?
""", ["Memoization with bounded memory", "Binary search", "Two pointers", "Backtracking"],
        "Memoization with bounded memory"),

    mcq(r"""
Which of these is a cache hit?
""", ["The requested key is already in the cache", "The cache is full",
       "The key had to be computed", "An item was evicted"],
        "The requested key is already in the cache"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <String, (int, DateTime)>{};
  m['k'] = (42, DateTime(2026));
  final (value, at) = m['k']!;
  print('$value ${at.year}');
}
```
""", ["42 2026", "(42, 2026)", "42 null", "It doesn't compile"], "42 2026"),

    mcq(r"""
What does `_map.keys.first` cost on a LinkedHashMap?
""", ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "O(1)"),

    mcq(r"""
In which order are keys stored in this LRU cache after the sequence put(1), put(2), get(1), put(3) with capacity 3 (least recent first)?
""", ["[2, 1, 3]", "[1, 2, 3]", "[3, 1, 2]", "[1, 3, 2]"], "[2, 1, 3]"),

    mcq(r"""
A CPU cache, a browser cache and a DNS cache all exploit which observation?
""", ["Recently used data is likely to be used again soon", "Data never changes",
       "Old data is always more important", "Every request is unique"],
        "Recently used data is likely to be used again soon"),

    mcq(r"""
What does this print?

```dart
""" + LRU + r"""
void main() {
  final c = Lru<String, int>(3);
  for (final k in ['a', 'b', 'c', 'a', 'd', 'b']) {
    if (c.get(k) == null) c.put(k, 0);
  }
  print(c.order);
}
```
""", ["[a, d, b]", "[b, c, d]", "[c, a, d]", "[a, b, c]"], "[a, d, b]"),

    fill(r"""
Remove and return a map entry's value in one step:

```dart
void main() {
  final m = {'a': 1};
  final v = m.%fill%('a');
  print(v); // 1
}
```
""", "remove"),

    mcq(r"""
What is the space complexity of an LRU cache with capacity c?
""", ["O(c)", "O(1)", "O(c²)", "Unbounded"], "O(c)"),

    mcq(r"""
Which operation in the linked-list LRU is NOT O(1)?
""", ["Listing all keys in recency order (O(n))", "get", "put", "Evicting the LRU item"],
        "Listing all keys in recency order (O(n))"),

    mcq(r"""
What does a "write-through" cache do on updates?
""", ["Writes to both the cache and the underlying storage", "Only writes to the cache",
       "Deletes the cache", "Ignores writes"], "Writes to both the cache and the underlying storage"),

    mcq(r"""
Which statement about LRU and memoization is true?
""", ["An LRU cache is a memo table that forgets the least recently used results when full",
       "LRU caches can't store function results", "Memoization always uses LRU",
       "They are unrelated"],
        "An LRU cache is a memo table that forgets the least recently used results when full"),
]
