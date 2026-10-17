BLOOM = r"""import 'dart:typed_data';

class Bloom {
  final int m, k;
  final Uint8List bits;
  Bloom(this.m, this.k) : bits = Uint8List((m + 7) ~/ 8);

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
"""

QUESTIONS = [
    mcq(r"""
What question does a Bloom filter answer?
""", ["\"Have I possibly seen this item before?\"", "\"What is the smallest item?\"",
       "\"What is the shortest path?\"", "\"How many times has this item appeared exactly?\""],
        "\"Have I possibly seen this item before?\""),

    mcq(r"""
Can a Bloom filter return a false NEGATIVE (say \"no\" for an added item)?
""".replace('\\"', '"'), ["No, never", "Yes, often", "Only when full", "Only for strings"],
        "No, never"),

    mcq(r"""
Can a Bloom filter return a false POSITIVE?
""", ["Yes, an item never added can appear present", "No, never",
       "Only after deletion", "Only with one hash function"],
        "Yes, an item never added can appear present"),

    mcq(r"""
What does a Bloom filter store?
""", ["A bit array of m bits", "Every item in a list", "A hash map of items to counts",
       "A sorted tree of items"], "A bit array of m bits"),

    mcq(r"""
How is an item added to a Bloom filter?
""", ["Set the k bits chosen by its k hash functions", "Append it to a list",
       "Flip all bits", "Store its hash in a map"],
        "Set the k bits chosen by its k hash functions"),

    mcq(r"""
When does a Bloom filter answer "definitely not present"?
""", ["When at least one of the item's k bits is 0", "When all k bits are 1",
       "When the filter is empty only", "Never"],
        "When at least one of the item's k bits is 0"),

    mcq(r"""
When does a Bloom filter answer "probably present"?
""", ["When all of the item's k bits are 1", "When any bit is 1", "When no bits are set",
       "When the item is long"], "When all of the item's k bits are 1"),

    mcq(r"""
What is the cost of add and query in a Bloom filter with k hash functions?
""", ["O(k)", "O(n)", "O(log n)", "O(m)"], "O(k)"),

    mcq(r"""
Why can't a basic Bloom filter delete items?
""", ["Clearing a bit might erase bits shared with other items, causing false negatives",
       "Bits can't be cleared in Dart", "Deletion is too slow", "It can delete safely"],
        "Clearing a bit might erase bits shared with other items, causing false negatives"),

    mcq(r"""
Which variant supports deletion?
""", ["A counting Bloom filter (small counters instead of bits)", "A sorted Bloom filter",
       "A Bloom filter with one hash", "None"],
        "A counting Bloom filter (small counters instead of bits)"),

    mcq(r"""
Can you list the items stored in a Bloom filter?
""", ["No, only membership questions can be asked", "Yes, in insertion order",
       "Yes, sorted", "Only the last item"], "No, only membership questions can be asked"),

    mcq(r"""
What does this print?

```dart
""" + BLOOM + r"""
void main() {
  final b = Bloom(1000, 4);
  for (final w in ['red', 'green', 'blue']) {
    b.add(w);
  }
  print(b.mightContain('green'));
}
```
""", ["true", "false", "null", "It depends on luck"], "true"),

    mcq(r"""
What does this print?

```dart
""" + BLOOM + r"""
void main() {
  final b = Bloom(64, 3);
  print(b.mightContain('anything'));
}
```
""", ["false", "true", "null", "It throws an error"], "false"),

    mcq(r"""
How do false positives change as more items are added to a fixed-size Bloom filter?
""", ["They increase as more bits become 1", "They decrease", "They stay exactly the same",
       "They become false negatives"], "They increase as more bits become 1"),

    mcq(r"""
Roughly what false-positive rate do you get with about 8 bits per item and an optimal k?
""", ["About 2%", "About 50%", "About 0%", "About 25%"], "About 2%"),

    mcq(r"""
What is the approximately optimal number of hash functions k for m bits and n items?
""", ["(m / n) × ln 2", "m × n", "n / m", "Always 1"], "(m / n) × ln 2"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  print((8 * ln2).round());
}
```
""", ["6", "8", "5", "11"], "6"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  final fp = pow(1 - exp(-6 * 1000 / 8000), 6);
  print(fp.toStringAsFixed(3));
}
```
""", ["0.022", "0.006", "0.150", "0.500"], "0.022"),

    mcq(r"""
In bit arrays, what does `p >> 3` compute?
""", ["The byte index (p ~/ 8)", "The bit within the byte", "p × 8", "p − 3"],
        "The byte index (p ~/ 8)"),

    mcq(r"""
In bit arrays, what does `p & 7` compute?
""", ["The bit position within its byte (p % 8)", "The byte index", "p × 7", "Always 7"],
        "The bit position within its byte (p % 8)"),

    mcq(r"""
What does this print?

```dart
void main() {
  const p = 21;
  print('${p >> 3} ${p & 7}');
}
```
""", ["2 5", "5 2", "21 7", "3 21"], "2 5"),

    mcq(r"""
What does this print?

```dart
import 'dart:typed_data';

void main() {
  final bits = Uint8List(2);
  for (final p in [1, 3, 9]) {
    bits[p >> 3] |= 1 << (p & 7);
  }
  print(bits);
}
```
""", ["[10, 2]", "[1, 3]", "[2, 10]", "[11, 0]"], "[10, 2]"),

    fill(r"""
Set bit p in a byte array:

```dart
import 'dart:typed_data';

void main() {
  final bits = Uint8List(1);
  const p = 3;
  bits[p >> 3] %fill% 1 << (p & 7);
  print(bits[0]); // 8
}
```
""", "|="),

    mcq(r"""
How can one Bloom filter simulate k hash functions from just two base hashes?
""", ["Double hashing: position_i = h1 + i × h2", "Use k copies of the same hash",
       "Sort the hashes", "It can't"], "Double hashing: position_i = h1 + i × h2"),

    mcq(r"""
Which real systems use Bloom filters?
""", ["Databases like Cassandra/RocksDB to skip disk reads for absent keys",
       "Sorting algorithms", "Compilers for parsing", "Image compression"],
        "Databases like Cassandra/RocksDB to skip disk reads for absent keys"),

    mcq(r"""
What is the typical pattern for using a Bloom filter in an app?
""", ["Use it as a fast \"definitely not\" check before an expensive lookup",
       "Use it as the only source of truth", "Use it to sort data", "Use it to store passwords"],
        "Use it as a fast \"definitely not\" check before an expensive lookup"),

    mcq(r"""
If a Bloom filter says "probably present" for a username, what should you do?
""", ["Confirm with the real database", "Trust it and reject the username",
       "Delete the username", "Ignore the answer"], "Confirm with the real database"),

    mcq(r"""
What is a skip list?
""", ["A sorted linked list with randomized express levels for O(log n) expected search",
       "A list that skips duplicates", "An array with gaps", "A queue that skips items"],
        "A sorted linked list with randomized express levels for O(log n) expected search"),

    mcq(r"""
How is a new skip list node's level chosen?
""", ["By flipping coins: keep promoting with probability 1/2", "Always the maximum level",
       "Based on the value's size", "Round-robin"],
        "By flipping coins: keep promoting with probability 1/2"),

    mcq(r"""
About what fraction of skip list nodes reach level 3 (with p = 1/2)?
""", ["1/4", "1/2", "1/8", "All of them"], "1/4"),

    mcq(r"""
What is the expected cost of search, insert and delete in a skip list?
""", ["O(log n) expected", "O(1)", "O(n) always", "O(n log n)"], "O(log n) expected"),

    mcq(r"""
What is a skip list's WORST-case search cost (very unlucky coin flips)?
""", ["O(n)", "O(log n)", "O(1)", "O(n²)"], "O(n)"),

    mcq(r"""
How does skip list search move?
""", ["Right while the next value is smaller, then down a level", "Down first, then right",
       "Left and up", "Randomly"], "Right while the next value is smaller, then down a level"),

    mcq(r"""
In skip list insertion, what does the `update` array store?
""", ["The last node visited on each level before the insertion point",
       "The new node's values", "Every node in the list", "The coin flips"],
        "The last node visited on each level before the insertion point"),

    mcq(r"""
What does level 0 of a skip list contain?
""", ["Every element in sorted order", "Only the tallest nodes", "Only the head",
       "A random subset"], "Every element in sorted order"),

    mcq(r"""
How does a skip list keep itself balanced?
""", ["Randomness: coin flips give the right level distribution on average",
       "Rotations", "Recoloring nodes", "Periodic sorting"],
        "Randomness: coin flips give the right level distribution on average"),

    mcq(r"""
Which advantage do skip lists have over balanced BSTs?
""", ["Simpler code and easier concurrent implementations", "Guaranteed O(log n) worst case",
       "Less memory always", "They need no comparisons"],
        "Simpler code and easier concurrent implementations"),

    mcq(r"""
Which system uses skip lists for its sorted sets?
""", ["Redis", "Python dict", "Dart's HashMap", "Git"], "Redis"),

    mcq(r"""
Which Java class is a concurrent skip list?
""", ["ConcurrentSkipListMap", "HashMap", "TreeMap", "ArrayList"], "ConcurrentSkipListMap"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

void main() {
  final rnd = Random(42);
  var tall = 0;
  for (var i = 0; i < 10000; i++) {
    var lvl = 1;
    while (lvl < 16 && rnd.nextBool()) {
      lvl++;
    }
    if (lvl >= 2) tall++;
  }
  print(tall > 4500 && tall < 5500);
}
```
""", ["true", "false", "10000", "It throws an error"], "true"),

    mcq(r"""
What happens if the skip list doesn't raise its current level when a taller node is inserted?
""", ["Searches never use the new higher express links", "The node is lost",
       "It throws an error", "Nothing; it's not needed"],
        "Searches never use the new higher express links"),

    mcq(r"""
Why does the skip list head sentinel have a very small value and all levels?
""", ["So every search can start from it on any level without special cases",
       "To store the minimum element", "To count nodes", "It's required by Dart"],
        "So every search can start from it on any level without special cases"),

    mcq(r"""
How do you list all skip list values in [lo, hi]?
""", ["Search for lo, then walk level 0 until values exceed hi", "Scan every level",
       "Use binary search on an array copy", "It can't do range queries"],
        "Search for lo, then walk level 0 until values exceed hi"),

    mcq(r"""
What do Bloom filters and skip lists have in common?
""", ["Both are probabilistic data structures", "Both store items in sorted order",
       "Both guarantee exact answers", "Both are hash tables"],
        "Both are probabilistic data structures"),

    mcq(r"""
What does a Bloom filter trade for its memory savings?
""", ["Certainty: it can give false positives", "Speed", "The ability to add items",
       "Nothing"], "Certainty: it can give false positives"),

    mcq(r"""
What does a skip list trade for its simplicity?
""", ["Worst-case guarantees (its O(log n) is expected, not guaranteed)",
       "Correctness", "The ability to delete", "Sorted order"],
        "Worst-case guarantees (its O(log n) is expected, not guaranteed)"),

    mcq(r"""
Which probabilistic structure counts distinct items in very little memory?
""", ["HyperLogLog", "Skip list", "LRU cache", "Trie"], "HyperLogLog"),

    mcq(r"""
Which probabilistic structure estimates item frequencies (possibly overestimating)?
""", ["Count-min sketch", "Bloom filter", "Skip list", "Fenwick tree"], "Count-min sketch"),

    mcq(r"""
Why is a Bloom filter's memory per item independent of the item's size?
""", ["It only stores k bits per item, not the item itself", "It compresses items",
       "It stores hashes of fixed length in a list", "It isn't independent"],
        "It only stores k bits per item, not the item itself"),

    mcq(r"""
What does `Uint8List(125)` provide?
""", ["125 bytes, enough for 1,000 bits", "125 bits", "A list of 125 strings",
       "125 kilobytes"], "125 bytes, enough for 1,000 bits"),

    mcq(r"""
What does this print?

```dart
void main() {
  print((1000 + 7) ~/ 8);
}
```
""", ["125", "126", "1007", "8"], "125"),

    order(r"""
Complete the Bloom filter membership check:

```dart
bool mightContain(String s) {
  for (final p in positions(s)) {
    if (bits[p %order% 3] & (1 << (p %order% 7)) %order% 0) return false;
  }
  return true;
}
```
""", [">>", "&", "==", "<<", "|", "!="], [">>", "&", "=="]),

    order(r"""
Complete the skip list search step:

```dart
for (var i = level - 1; i %order% 0; i--) {
  while (node.next[i] != null && node.next[i]!.value %order% target) {
    node = node.next[%order%]!;
  }
}
```
""", [">=", "<", "i", ">", "0"], [">=", "<", "i"]),

    mcq(r"""
Which structure would you pick to avoid re-crawling URLs among billions, with limited memory?
""", ["A Bloom filter", "A sorted List", "A skip list of every URL", "A stack"],
        "A Bloom filter"),

    mcq(r"""
Which structure would you pick for a sorted leaderboard that many threads update concurrently?
""", ["A concurrent skip list", "A Bloom filter", "A plain List with sort()", "A Queue"],
        "A concurrent skip list"),
]
