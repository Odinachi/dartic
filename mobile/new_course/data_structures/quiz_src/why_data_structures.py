QUESTIONS = [
    mcq(r"""
What is a data structure?
""", [
        "A way of organizing data so the operations you need are efficient",
        "A special Dart keyword for storing numbers",
        "A database that runs on a server",
        "A UI widget that displays lists",
    ], "A way of organizing data so the operations you need are efficient"),

    mcq(r"""
Which Dart collection is best for checking whether a username is already taken?
""", ["Set<String>", "List<String>", "Queue<String>", "String"], "Set<String>"),

    mcq(r"""
What is the average time complexity of `contains` on a Dart `Set`?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the time complexity of `contains` on a Dart `List`?
""", ["O(n)", "O(1)", "O(log n)", "O(n log n)"], "O(n)"),

    mcq(r"""
What will this code print?

```dart
void main() {
  final seen = <String>{};
  print(seen.add('ada'));
  print(seen.add('ada'));
}
```
""", ["true then false", "true then true", "false then true", "It throws an error"],
        "true then false"),

    fill(r"""
Fill in the method that removes and returns the first item of a Queue in O(1):

```dart
import 'dart:collection';

void main() {
  final q = Queue<String>.from(['a', 'b', 'c']);
  print(q.%fill%()); // a
}
```
""", "removeFirst"),

    mcq(r"""
Which structure should you use for a menu where you look up a price by the pizza's name?
""", ["Map<String, double>", "List<double>", "Set<String>", "Queue<double>"],
        "Map<String, double>"),

    mcq(r"""
Why is calling `list.removeAt(0)` inside a loop until the list is empty slow?
""", [
        "Every call shifts all remaining elements one position left",
        "removeAt only works on sorted lists",
        "removeAt copies the whole list to a new one each time",
        "It isn't slow; removeAt(0) is always O(1)",
    ], "Every call shifts all remaining elements one position left"),

    mcq(r"""
What is the total cost of draining a List of n items using `removeAt(0)` repeatedly?
""", ["O(n²)", "O(n)", "O(log n)", "O(1)"], "O(n²)"),

    fill(r"""
Complete the code so `world` uses record keys for a sparse game map:

```dart
void main() {
  final Map<(int, int), String> world = {};
  world[(3, 4)] = 'Tree';
  print(world[(3, 4)] %fill% 'Grass');
}
```
""", "??"),

    mcq(r"""
What does this print?

```dart
void main() {
  final Map<(int, int), String> world = {(1, 2): 'Gem'};
  print(world[(9, 9)] ?? 'Grass');
}
```
""", ["Grass", "Gem", "null", "It throws an error"], "Grass"),

    mcq(r"""
Why can Dart records like `(1, 2)` be used as Map keys?
""", [
        "Records have built-in value-based == and hashCode",
        "Records are always converted to strings",
        "Map keys are compared by identity only",
        "Records are mutable so the map can update them",
    ], "Records have built-in value-based == and hashCode"),

    mcq(r"""
In the pizza shop example, why was a `Queue` used for kitchen orders?
""", [
        "Orders must be cooked in the order they arrived (FIFO)",
        "Queues automatically sort orders by price",
        "Queues remove duplicate orders",
        "Queues allow lookup by customer name",
    ], "Orders must be cooked in the order they arrived (FIFO)"),

    mcq(r"""
Which structure always keeps its keys sorted?
""", ["SplayTreeMap", "HashMap", "LinkedHashMap", "List"], "SplayTreeMap"),

    fill(r"""
Fill in the import needed to use `Queue` and `SplayTreeMap`:

```dart
import '%fill%';

void main() {
  final q = Queue<int>();
  print(q.isEmpty);
}
```
""", "dart:collection"),

    mcq(r"""
What does `SplayTreeMap.firstKey()` return?
""", ["The smallest key", "The first key inserted", "A random key", "The largest key"],
        "The smallest key"),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final m = SplayTreeMap<String, int>.from({'Zoe': 1, 'Ali': 2, 'Mia': 3});
  print(m.keys.toList());
}
```
""", ["[Ali, Mia, Zoe]", "[Zoe, Ali, Mia]", "[Zoe, Mia, Ali]", "[Mia, Ali, Zoe]"],
        "[Ali, Mia, Zoe]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final scores = {'Zoe': 88, 'Ali': 95};
  print(scores['Ali']);
}
```
""", ["95", "88", "null", "Ali"], "95"),

    mcq(r"""
Which statement about Big O is correct?
""", [
        "It describes how the work grows as the amount of data grows",
        "It measures the exact number of milliseconds a function takes",
        "It only applies to sorting algorithms",
        "It measures how much code you wrote",
    ], "It describes how the work grows as the amount of data grows"),

    mcq(r"""
Which cost grows the slowest as n gets larger?
""", ["O(1)", "O(log n)", "O(n)", "O(n²)"], "O(1)"),

    order(r"""
Arrange these costs from cheapest to most expensive as n grows:

```dart
// %order% < %order% < %order% < %order%
```
""", ["O(1)", "O(log n)", "O(n)", "O(n²)"], ["O(1)", "O(log n)", "O(n)", "O(n²)"]),

    mcq(r"""
In the emergency room example, why was the naive approach roughly O(n²)?
""", [
        "For each of the n patients, it scanned up to n patients to find the most urgent",
        "It sorted the list n times using bubble sort",
        "It used a Map, which is slow",
        "It used recursion",
    ], "For each of the n patients, it scanned up to n patients to find the most urgent"),

    mcq(r"""
Which data structure is designed to always give you the most urgent (smallest priority) item quickly?
""", ["A heap / priority queue", "A Set", "A linked list", "A String"],
        "A heap / priority queue"),

    fill(r"""
Complete the record field access to print the patient's name:

```dart
void main() {
  final patient = ('Rita', 1);
  print(patient.%fill%); // Rita
}
```
""", "$1"),

    mcq(r"""
What does this print?

```dart
void main() {
  final patient = ('Omar', 2);
  print(patient.$2);
}
```
""", ["2", "Omar", "(Omar, 2)", "It throws an error"], "2"),

    mcq(r"""
A friend list where you only care whether someone is your friend should use:
""", ["Set", "Queue", "List", "SplayTreeMap"], "Set"),

    mcq(r"""
Print jobs that must print in the order they were sent should use:
""", ["Queue", "Set", "Map", "SplayTreeSet"], "Queue"),

    mcq(r"""
Roads between cities, where you want the shortest route, are best modeled as:
""", ["A graph", "A Set", "A Queue", "A String"], "A graph"),

    mcq(r"""
Autocomplete for words that start with a given prefix is a classic use of:
""", ["A trie", "A queue", "A stack", "A hash set"], "A trie"),

    mcq(r"""
What is the time complexity of reading `list[5]` on a Dart List?
""", ["O(1)", "O(n)", "O(log n)", "O(5)"], "O(1)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final banned = {'spam', 'scam'};
  final words = ['hello', 'scam', 'world'];
  print(words.where(banned.contains).toList());
}
```
""", ["[scam]", "[hello, world]", "[]", "[spam, scam]"], "[scam]"),

    fill(r"""
Fill in the class used to measure elapsed time:

```dart
void main() {
  final sw = %fill%()..start();
  // ... do work ...
  sw.stop();
  print(sw.elapsedMilliseconds);
}
```
""", "Stopwatch"),

    mcq(r"""
Why does a Set store the 100,000 usernames as fast as a List but answer `contains` much faster?
""", [
        "It uses hash codes to jump almost directly to where the item would be",
        "It keeps a second copy of every username",
        "It sorts usernames alphabetically after every insert",
        "It stores usernames on disk instead of memory",
    ], "It uses hash codes to jump almost directly to where the item would be"),

    mcq(r"""
What does this print?

```dart
void main() {
  final emails = ['a', 'b', 'a', 'c', 'b', 'a'];
  final seen = <String>{};
  final dups = <String>{};
  for (final e in emails) {
    if (!seen.add(e)) dups.add(e);
  }
  print(dups);
}
```
""", ["{a, b}", "{a, b, a}", "{c}", "{a, b, c}"], "{a, b}"),

    mcq(r"""
What is the time complexity of this duplicate detector for n emails?

```dart
Set<String> duplicates(List<String> emails) {
  final seen = <String>{};
  final dups = <String>{};
  for (final e in emails) {
    if (!seen.add(e)) dups.add(e);
  }
  return dups;
}
```
""", ["O(n)", "O(n²)", "O(log n)", "O(1)"], "O(n)"),

    mcq(r"""
Which mistake is shown here?

```dart
void main() {
  final scores = <int>[];
  for (final s in [5, 2, 8]) {
    scores.add(s);
    scores.sort();
  }
}
```
""", [
        "Sorting after every insert instead of once at the end",
        "Using a List instead of a Map",
        "Sorting an empty list",
        "Using final for a loop variable",
    ], "Sorting after every insert instead of once at the end"),

    mcq(r"""
What does this print?

```dart
void main() {
  final scores = <int>[];
  for (final s in [50, 20, 80, 10]) {
    scores.add(s);
    scores.sort();
  }
  print(scores);
}
```
""", ["[10, 20, 50, 80]", "[50, 20, 80, 10]", "[80, 50, 20, 10]", "[10]"],
        "[10, 20, 50, 80]"),

    fill(r"""
Fill in the method that adds to the back of a Queue:

```dart
import 'dart:collection';

void main() {
  final q = Queue<String>();
  q.%fill%('order 1');
  print(q);
}
```
""", "addLast"),

    order(r"""
Complete the code that serves customers in order:

```dart
import 'dart:collection';

void main() {
  final line = Queue<String>.from(['Ana', 'Ben']);
  %order% (line.%order%) {
    print(line.%order%());
  }
}
```
""", ["while", "isNotEmpty", "removeFirst", "if", "isEmpty", "removeLast"],
        ["while", "isNotEmpty", "removeFirst"]),

    mcq(r"""
What does this print?

```dart
import 'dart:collection';

void main() {
  final q = Queue<int>.from([1, 2, 3]);
  q.addLast(4);
  q.removeFirst();
  print(q);
}
```
""", ["{2, 3, 4}", "{1, 2, 3}", "{1, 2, 3, 4}", "{4, 2, 3}"], "{2, 3, 4}"),

    mcq(r"""
Which three questions does every data structure answer?
""", [
        "How data is laid out, which operations it supports, and what they cost",
        "Its name, its author, and its version",
        "Which widget displays it, which color it uses, and its font",
        "Whether it is async, isolated, or synchronous",
    ], "How data is laid out, which operations it supports, and what they cost"),

    mcq(r"""
Why do we compare data structures using growth rates instead of milliseconds?
""", [
        "Milliseconds depend on the device; growth rates describe the algorithm itself",
        "Milliseconds are too hard to measure in Dart",
        "Growth rates are always smaller numbers",
        "Dart doesn't support timing code",
    ], "Milliseconds depend on the device; growth rates describe the algorithm itself"),

    mcq(r"""
A 1,000,000 × 1,000,000 game world with only 300 interesting tiles should be stored as:
""", [
        "A Map from coordinates to tile contents",
        "A List of 10¹² tiles",
        "A Queue of every tile",
        "A String with one character per tile",
    ], "A Map from coordinates to tile contents"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <String, int>{};
  m['a'] = 1;
  m['a'] = 2;
  print(m.length);
}
```
""", ["1", "2", "0", "It throws an error"], "1"),

    fill(r"""
Fill in the method that combines items into the maximum:

```dart
void main() {
  final nums = [3, 9, 4];
  final max = nums.%fill%((a, b) => a > b ? a : b);
  print(max); // 9
}
```
""", "reduce"),

    mcq(r"""
Which collection type in Dart is created by the literal `{'a', 'b'}`?
""", ["Set<String>", "Map<String, String>", "List<String>", "Record"], "Set<String>"),

    mcq(r"""
Which collection type in Dart is created by the literal `{'a': 1}`?
""", ["Map<String, int>", "Set<String>", "List<int>", "Record"], "Map<String, int>"),

    mcq(r"""
What kind of collection does `var x = {};` create?
""", ["Map<dynamic, dynamic>", "Set<dynamic>", "List<dynamic>", "A record"],
        "Map<dynamic, dynamic>"),

    fill(r"""
Create an empty Set of strings (not a Map):

```dart
void main() {
  final names = %fill%{};
  names.add('Ada');
  print(names);
}
```
""", "<String>"),

    mcq(r"""
What does this print?

```dart
void main() {
  final tags = {'dart', 'flutter', 'dart'};
  print(tags.length);
}
```
""", ["2", "3", "1", "It throws an error"], "2"),

    mcq(r"""
Which statement about real apps is true?
""", [
        "They usually combine several data structures, each for the job it's best at",
        "They should always use a single List for everything",
        "They should avoid Maps because they are slow",
        "They only use data structures from packages",
    ], "They usually combine several data structures, each for the job it's best at"),

    mcq(r"""
Getting the items in sorted order from a `SplayTreeMap` costs:
""", ["O(n)", "O(n²)", "O(n log n) every time", "O(1)"], "O(n)"),

    mcq(r"""
Getting the smallest key from a `SplayTreeMap` costs about:
""", ["O(log n)", "O(n²)", "O(n)", "O(n log n)"], "O(log n)"),

    order(r"""
Complete the word counter:

```dart
void main() {
  final counts = <String, int>{};
  for (final w in 'a b a'.%order%(' ')) {
    counts[w] = (counts[w] %order% 0) %order% 1;
  }
  print(counts); // {a: 2, b: 1}
}
```
""", ["split", "??", "+", "join", "?.", "-"], ["split", "??", "+"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = <String, int>{};
  for (final w in 'to be or not to be'.split(' ')) {
    counts[w] = (counts[w] ?? 0) + 1;
  }
  print(counts['be']);
}
```
""", ["2", "1", "null", "6"], "2"),

    mcq(r"""
Which operation is NOT supported efficiently (or at all) by a hash-based Set?
""", ["Get the item at index 3", "Check if an item exists", "Add an item", "Remove an item"],
        "Get the item at index 3"),

    mcq(r"""
If doubling the data doubles the time of an operation, that operation is:
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
If doubling the data makes an operation take about 4 times as long, that operation is:
""", ["O(n²)", "O(n)", "O(log n)", "O(1)"], "O(n²)"),
]
