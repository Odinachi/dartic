QUESTIONS = [
    mcq(r"""
What is a collision in a hash table?
""", ["Two different keys mapping to the same bucket or slot", "Two equal keys being inserted",
       "A hash code that's too large", "A table that is full"],
        "Two different keys mapping to the same bucket or slot"),

    mcq(r"""
What does the birthday paradox tell us about hashing?
""", ["Collisions happen much sooner than intuition suggests",
       "Collisions never happen with good hash functions",
       "Hash tables need 365 buckets", "Only dates can collide"],
        "Collisions happen much sooner than intuition suggests"),

    mcq(r"""
With 23 people, roughly what is the chance two share a birthday?
""", ["About 50%", "About 6%", "About 23%", "About 99%"], "About 50%"),

    mcq(r"""
How does separate chaining handle collisions?
""", ["Each bucket stores a list of all entries that hash to it",
       "It probes for the next free slot", "It rejects the second key",
       "It doubles the table immediately"],
        "Each bucket stores a list of all entries that hash to it"),

    mcq(r"""
How does open addressing handle collisions?
""", ["It stores entries directly in the array and probes for another free slot",
       "It stores a list in each bucket", "It throws an error", "It overwrites the old entry"],
        "It stores entries directly in the array and probes for another free slot"),

    mcq(r"""
Can the load factor exceed 1 with separate chaining?
""", ["Yes, buckets simply hold more entries", "No, never",
       "Only for String keys", "Only after a resize"], "Yes, buckets simply hold more entries"),

    mcq(r"""
Can the load factor reach or exceed 1 with open addressing?
""", ["No, there must always be empty slots", "Yes, without problems",
       "Only with linear probing", "Only with tombstones"],
        "No, there must always be empty slots"),

    mcq(r"""
What is the probe sequence for linear probing starting at slot h?
""", ["h, h+1, h+2, h+3, ...", "h, h+1, h+4, h+9, ...", "h, h+s, h+2s, ... with s from a second hash",
       "Random slots"], "h, h+1, h+2, h+3, ..."),

    mcq(r"""
What is the probe sequence for quadratic probing starting at slot h?
""", ["h, h+1, h+4, h+9, ...", "h, h+1, h+2, h+3, ...", "h, 2h, 3h, ...", "h, h-1, h-2, ..."],
        "h, h+1, h+4, h+9, ..."),

    mcq(r"""
What does double hashing use to choose the probe step size?
""", ["A second hash function", "The key's length", "A random number each time",
       "Always a step of 1"], "A second hash function"),

    mcq(r"""
What is primary clustering?
""", ["Long runs of occupied slots that grow as linear probing extends them",
       "Keys sorted into clusters by value", "Buckets in chaining getting long",
       "Two hash tables sharing memory"],
        "Long runs of occupied slots that grow as linear probing extends them"),

    mcq(r"""
Which probing method suffers most from primary clustering?
""", ["Linear probing", "Quadratic probing", "Double hashing", "Separate chaining"],
        "Linear probing"),

    mcq(r"""
Which probing method is the most cache-friendly?
""", ["Linear probing", "Double hashing", "Quadratic probing", "Random probing"],
        "Linear probing"),

    mcq(r"""
What does this print?

```dart
void main() {
  const cap = 10, home = 8;
  print([for (var j = 0; j < 4; j++) (home + j) % cap]);
}
```
""", ["[8, 9, 0, 1]", "[8, 9, 10, 11]", "[8, 9, 12, 17]", "[8, 0, 2, 4]"], "[8, 9, 0, 1]"),

    mcq(r"""
What does this print?

```dart
void main() {
  const cap = 16, home = 3;
  print([for (var j = 0; j < 4; j++) (home + j * j) % cap]);
}
```
""", ["[3, 4, 7, 12]", "[3, 4, 5, 6]", "[3, 6, 9, 12]", "[3, 4, 7, 11]"], "[3, 4, 7, 12]"),

    mcq(r"""
What does this print?

```dart
int hash2(int key) => 7 - (key % 7);

void main() {
  print(hash2(14));
  print(hash2(15));
}
```
""", ["7 then 6", "0 then 1", "7 then 1", "1 then 6"], "7 then 6"),

    mcq(r"""
Why must the double-hashing step size never be 0?
""", ["A step of 0 would probe the same slot forever", "0 is not a valid int",
       "It would skip the home slot", "It makes hashing slower"],
        "A step of 0 would probe the same slot forever"),

    mcq(r"""
Why is a prime table capacity often used with double hashing?
""", ["So every step size eventually visits every slot", "Primes are faster to divide",
       "To avoid negative indexes", "Because 0 is prime"],
        "So every step size eventually visits every slot"),

    mcq(r"""
In linear probing, when does a lookup for a missing key stop?
""", ["When it reaches an empty slot", "When it reaches a tombstone",
       "After exactly one probe", "When it reaches the end of the array"],
        "When it reaches an empty slot"),

    mcq(r"""
Why can't open addressing delete a key by simply setting its slot to empty?
""", ["Keys placed later in the same probe chain would become unreachable",
       "Dart doesn't allow null in lists", "It would make the table full",
       "It would change other keys' hash codes"],
        "Keys placed later in the same probe chain would become unreachable"),

    mcq(r"""
What is a tombstone in open addressing?
""", ["A marker for a deleted slot that lookups probe past", "An empty slot",
       "The last slot in the array", "A key that can't be deleted"],
        "A marker for a deleted slot that lookups probe past"),

    mcq(r"""
How should a lookup treat a tombstone?
""", ["Keep probing past it", "Stop and report not found", "Return its value",
       "Throw an error"], "Keep probing past it"),

    mcq(r"""
How should an insert treat a tombstone?
""", ["It may reuse the slot, after confirming the key isn't further along the chain",
       "Skip it forever", "Stop the insert", "Delete the whole chain"],
        "It may reuse the slot, after confirming the key isn't further along the chain"),

    mcq(r"""
What problem do many tombstones cause?
""", ["Longer probe chains and slower lookups, until the table is rehashed",
       "Lost keys", "Duplicate keys", "Negative load factors"],
        "Longer probe chains and slower lookups, until the table is rehashed"),

    fill(r"""
Check whether a slot holds the tombstone sentinel object:

```dart
const tombstone = Object();

bool isDeleted(Object? slot) => %fill%(slot, tombstone);
```
""", "identical"),

    mcq(r"""
What does this print?

```dart
const tomb = Object();

void main() {
  final slots = <Object?>[null, 1, 9, 17, null];
  slots[2] = tomb;
  var i = 1;
  while (slots[i] != null && slots[i] != 17) {
    i++;
  }
  print(i);
}
```
""", ["3", "2", "4", "1"], "3"),

    mcq(r"""
What does this print?

```dart
void main() {
  final slots = <int?>[null, 1, null, 17, null];
  var i = 1;
  while (slots[i] != null && slots[i] != 17) {
    i++;
  }
  print(slots[i] == 17);
}
```
""", ["false", "true", "null", "It throws an error"], "false"),

    mcq(r"""
In linear probing, keys 1, 9 and 17 share home slot 1 and sit in slots 1, 2, 3. If 9 is deleted by setting slot 2 to null, what happens when looking up 17?
""", ["The search stops at the empty slot 2 and wrongly reports 17 missing",
       "It finds 17 normally", "It throws an error", "It finds 9"],
        "The search stops at the empty slot 2 and wrongly reports 17 missing"),

    mcq(r"""
What happens with linear probing if the table becomes completely full?
""", ["A lookup for a missing key can probe forever", "Lookups become faster",
       "New keys overwrite old ones safely", "Nothing changes"],
        "A lookup for a missing key can probe forever"),

    mcq(r"""
What typical maximum load factor do open-addressing tables use?
""", ["Around 0.5 to 0.75", "Exactly 1.0", "Around 5", "No limit"], "Around 0.5 to 0.75"),

    mcq(r"""
Using Knuth's estimate ½(1 + 1/(1 − α)), what is the expected number of probes for a successful search at α = 0.5?
""", ["1.5", "2", "1", "3"], "1.5"),

    mcq(r"""
Using the same formula, roughly how many probes at α = 0.9?
""", ["5.5", "1.9", "10", "50"], "5.5"),

    mcq(r"""
What does Knuth's formula tell us about open addressing near α = 1?
""", ["Probe counts explode, so tables must resize early", "Performance stays constant",
       "It becomes faster", "Collisions stop happening"],
        "Probe counts explode, so tables must resize early"),

    mcq(r"""
Which collision strategy makes deletion easiest?
""", ["Separate chaining", "Linear probing", "Quadratic probing", "Double hashing"],
        "Separate chaining"),

    mcq(r"""
Which strategy usually has better cache performance?
""", ["Open addressing (one flat array)", "Separate chaining (lists per bucket)",
       "They are always identical", "Neither uses the cache"],
        "Open addressing (one flat array)"),

    mcq(r"""
What is a hash flooding attack?
""", ["Sending many keys chosen to collide so lookups become O(n)",
       "Filling a table with random keys", "Deleting all keys at once",
       "Using very long keys"],
        "Sending many keys chosen to collide so lookups become O(n)"),

    mcq(r"""
Which defense makes collisions hard for attackers to predict?
""", ["Randomized (seeded) hash functions", "Sorting keys", "Using smaller tables",
       "Removing the load factor limit"], "Randomized (seeded) hash functions"),

    mcq(r"""
How does Java's HashMap cap the worst case for very long chains?
""", ["It converts long chains into balanced trees (O(log n))", "It deletes old entries",
       "It refuses new keys", "It switches to linear probing"],
        "It converts long chains into balanced trees (O(log n))"),

    mcq(r"""
Two keys have the same hash code. What can you conclude?
""", ["Nothing about equality; you must still compare them with ==",
       "They are equal", "They are different", "One of them is null"],
        "Nothing about equality; you must still compare them with =="),

    mcq(r"""
What does this print?

```dart
double chance(int people, int days) {
  var none = 1.0;
  for (var i = 0; i < people; i++) {
    none *= (days - i) / days;
  }
  return 1 - none;
}

void main() {
  print(chance(2, 2));
}
```
""", ["0.5", "1.0", "0.0", "0.25"], "0.5"),

    mcq(r"""
What does `Random(42)` give you compared to `Random()`?
""", ["A repeatable sequence of random numbers", "Numbers up to 42 only",
       "A cryptographically secure generator", "Exactly 42 numbers"],
        "A repeatable sequence of random numbers"),

    order(r"""
Complete the linear probe step:

```dart
var i = home(key);
while (slots[i] %order% null) {
  if (slots[i] == key) return true;
  i = (i %order% 1) %order% slots.length;
}
return false;
```
""", ["!=", "+", "%", "==", "-", "~/"], ["!=", "+", "%"]),

    mcq(r"""
What is the average chain length in separate chaining with load factor α?
""", ["α", "1/α", "α²", "Always 1"], "α"),

    mcq(r"""
A chaining table has 3,000 entries in 1,000 buckets. What's the average chain length?
""", ["3", "0.33", "1,000", "3,000"], "3"),

    mcq(r"""
What is secondary clustering?
""", ["Keys with the same home slot following the same probe sequence",
       "Clusters inside chaining buckets", "Two tables clustering together",
       "Clusters caused by tombstones only"],
        "Keys with the same home slot following the same probe sequence"),

    mcq(r"""
Which method avoids secondary clustering by giving keys with the same home different step sizes?
""", ["Double hashing", "Quadratic probing", "Linear probing", "Separate chaining"],
        "Double hashing"),

    mcq(r"""
What is backward-shift deletion?
""", ["Moving later entries in a linear-probing cluster back into the gap, avoiding tombstones",
       "Deleting from the end of a list", "Shifting the whole table left",
       "Undoing the last insert"],
        "Moving later entries in a linear-probing cluster back into the gap, avoiding tombstones"),

    mcq(r"""
What does this print?

```dart
void main() {
  const cap = 13;
  print([5 % cap, 18 % cap, 31 % cap]);
}
```
""", ["[5, 5, 5]", "[5, 18, 31]", "[5, 5, 6]", "[0, 5, 5]"], "[5, 5, 5]"),

    mcq(r"""
What does this print?

```dart
void main() {
  const cap = 13, home = 5, step = 3;
  print([for (var j = 0; j < 4; j++) (home + j * step) % cap]);
}
```
""", ["[5, 8, 11, 1]", "[5, 8, 11, 14]", "[5, 6, 7, 8]", "[5, 8, 11, 0]"], "[5, 8, 11, 1]"),

    mcq(r"""
What happens when resizing an open-addressing table?
""", ["Every live key is re-inserted with new home slots; tombstones are dropped",
       "Keys are copied to the same indexes", "Only the first half is copied",
       "Tombstones are copied too"],
        "Every live key is re-inserted with new home slots; tombstones are dropped"),

    mcq(r"""
Which structure does Python's dict use internally?
""", ["Open addressing", "Separate chaining with linked lists", "A sorted array", "A B-tree"],
        "Open addressing"),

    mcq(r"""
What does this print?

```dart
void main() {
  final used = <int>{};
  var collisions = 0;
  for (final slot in [3, 7, 3, 1, 7, 7]) {
    if (!used.add(slot)) collisions++;
  }
  print(collisions);
}
```
""", ["3", "2", "6", "0"], "3"),

    mcq(r"""
In separate chaining, what does deleting an entry involve?
""", ["Removing it from its bucket's list", "Leaving a tombstone",
       "Shifting all buckets", "Rehashing the table"],
        "Removing it from its bucket's list"),

    mcq(r"""
Which statement about the two strategies is true?
""", ["Chaining degrades gradually at high load; open addressing degrades sharply near full",
       "Open addressing handles α > 1 better", "Chaining needs tombstones",
       "They perform identically at every load"],
        "Chaining degrades gradually at high load; open addressing degrades sharply near full"),

    mcq(r"""
In a probing insert, why keep scanning after finding a tombstone?
""", ["The key might already exist further along the chain", "Tombstones can't be reused",
       "To count the chain length", "It's not necessary"],
        "The key might already exist further along the chain"),

    fill(r"""
Remember the first reusable slot only once:

```dart
void main() {
  int? firstFree;
  for (final i in [4, 6, 9]) {
    firstFree %fill% i;
  }
  print(firstFree); // 4
}
```
""", "??="),
]
