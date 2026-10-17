QUESTIONS = [
    mcq(r"""
What does a Dart variable of type `List<int>` actually hold?
""", ["A reference to a List object", "The list's elements directly",
       "A copy of the list", "The list's length"], "A reference to a List object"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2];
  final b = a;
  b.add(3);
  print(a);
}
```
""", ["[1, 2, 3]", "[1, 2]", "[3]", "It throws an error"], "[1, 2, 3]"),

    mcq(r"""
What does this print?

```dart
void main() {
  var a = [1, 2];
  var b = a;
  b = [9];
  print(a);
}
```
""", ["[1, 2]", "[9]", "[1, 2, 9]", "[]"], "[1, 2]"),

    mcq(r"""
What does `identical(a, b)` check?
""", ["Whether a and b refer to the exact same object", "Whether a and b have equal contents",
       "Whether a and b have the same type", "Whether a and b have the same hashCode"],
        "Whether a and b refer to the exact same object"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2];
  final b = a;
  print(identical(a, b));
}
```
""", ["true", "false", "null", "It throws an error"], "true"),

    mcq(r"""
What does this print?

```dart
void main() {
  print([1, 2] == [1, 2]);
}
```
""", ["false", "true", "null", "It doesn't compile"], "false"),

    mcq(r"""
What does this print?

```dart
void main() {
  print((1, 'a') == (1, 'a'));
}
```
""", ["true", "false", "null", "It doesn't compile"], "true"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('dart' == 'dart');
}
```
""", ["true", "false", "Depends on memory", "It throws an error"], "true"),

    mcq(r"""
What does this print?

```dart
class P {
  final int x;
  P(this.x);
}

void main() {
  print(P(1) == P(1));
}
```
""", ["false", "true", "null", "It doesn't compile"], "false"),

    mcq(r"""
Why does `P(1) == P(1)` return false here?

```dart
class P {
  final int x;
  P(this.x);
}

void main() {
  print(P(1) == P(1)); // false
}
```
""", ["The default == compares identity, and they are different objects",
       "The constructor is broken", "int fields can't be compared",
       "== is not defined for classes"],
        "The default == compares identity, and they are different objects"),

    fill(r"""
Override equality for a value class:

```dart
class P {
  final int x;
  P(this.x);

  @override
  bool %fill% ==(Object other) => other is P && other.x == x;

  @override
  int get hashCode => x.hashCode;
}
```
""", "operator"),

    mcq(r"""
What is the hashCode contract?
""", ["If a == b, then a.hashCode must equal b.hashCode",
       "If a.hashCode == b.hashCode, then a must == b",
       "hashCode must be unique for every object",
       "hashCode must never change, even for different objects"],
        "If a == b, then a.hashCode must equal b.hashCode"),

    mcq(r"""
Can two objects that are NOT equal have the same hashCode?
""", ["Yes, that's a collision and it's allowed", "No, that breaks the contract",
       "Only for strings", "Only in debug mode"], "Yes, that's a collision and it's allowed"),

    fill(r"""
Combine several fields into a hash code:

```dart
class Point {
  final int x, y;
  Point(this.x, this.y);

  @override
  int get hashCode => Object.%fill%(x, y);

  @override
  bool operator ==(Object other) =>
      other is Point && other.x == x && other.y == y;
}
```
""", "hash"),

    mcq(r"""
What does this print?

```dart
class Point {
  final int x, y;
  Point(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      other is Point && other.x == x && other.y == y;

  @override
  int get hashCode => Object.hash(x, y);
}

void main() {
  final s = {Point(1, 2)};
  print(s.contains(Point(1, 2)));
}
```
""", ["true", "false", "null", "It throws an error"], "true"),

    mcq(r"""
What usually happens if you override `==` but NOT `hashCode`, then look up an equal object in a Set?
""", ["contains usually returns false", "contains always returns true",
       "The Set throws an exception", "Dart refuses to compile"],
        "contains usually returns false"),

    mcq(r"""
Why is mutating a field used in `hashCode` after adding the object to a Set dangerous?
""", ["The object is filed under its old hash, so lookups can't find it",
       "Sets automatically delete changed objects", "Dart throws a ConcurrentModificationError",
       "It makes the Set sorted"],
        "The object is filed under its old hash, so lookups can't find it"),

    mcq(r"""
What's the best way to prevent that problem?
""", ["Make the key fields final (immutable)", "Call set.sort() after changes",
       "Use dynamic for the fields", "Never override hashCode"],
        "Make the key fields final (immutable)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <List<int>, String>{};
  m[[0, 0]] = 'start';
  print(m[[0, 0]]);
}
```
""", ["null", "start", "[0, 0]", "It throws an error"], "null"),

    mcq(r"""
What does this print?

```dart
void main() {
  final m = <(int, int), String>{};
  m[(0, 0)] = 'start';
  print(m[(0, 0)]);
}
```
""", ["start", "null", "(0, 0)", "It throws an error"], "start"),

    mcq(r"""
Which of these types are immutable in Dart?
""", ["int, String and records", "List and Map", "Set and StringBuffer",
       "Every class by default"], "int, String and records"),

    mcq(r"""
What does this print?

```dart
void main() {
  var s = 'Hi';
  final t = s;
  s += '!';
  print(t);
}
```
""", ["Hi", "Hi!", "!", "null"], "Hi"),

    mcq(r"""
What does this print?

```dart
void addOne(List<int> xs) {
  xs.add(1);
}

void main() {
  final xs = <int>[];
  addOne(xs);
  addOne(xs);
  print(xs);
}
```
""", ["[1, 1]", "[]", "[1]", "It throws an error"], "[1, 1]"),

    mcq(r"""
What does this print?

```dart
void reset(List<int> xs) {
  xs = [];
}

void main() {
  final xs = [1, 2, 3];
  reset(xs);
  print(xs);
}
```
""", ["[1, 2, 3]", "[]", "null", "It throws an error"], "[1, 2, 3]"),

    mcq(r"""
What does this print?

```dart
void bump(int x) {
  x++;
}

void main() {
  var n = 10;
  bump(n);
  print(n);
}
```
""", ["10", "11", "0", "null"], "10"),

    mcq(r"""
How does Dart pass arguments to functions?
""", ["References are passed by value", "Everything is deep-copied",
       "By pointer arithmetic", "Ints by reference, lists by value"],
        "References are passed by value"),

    mcq(r"""
What does `final` mean for `final list = [1, 2];`?
""", ["The variable can't be reassigned, but the list can still be modified",
       "The list can never be modified", "The list is a compile-time constant",
       "The list is copied every time it's used"],
        "The variable can't be reassigned, but the list can still be modified"),

    mcq(r"""
What happens here?

```dart
void main() {
  const xs = [1, 2];
  xs.add(3);
}
```
""", ["It throws an UnsupportedError at runtime", "It prints [1, 2, 3]",
       "xs becomes [3]", "Nothing happens"], "It throws an UnsupportedError at runtime"),

    fill(r"""
Create a list that can't be modified:

```dart
void main() {
  final xs = List<int>.%fill%([1, 2, 3]);
  print(xs);
}
```
""", "unmodifiable"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(null is Object);
  print(5 is Object);
}
```
""", ["false then true", "true then true", "true then false", "false then false"],
        "false then true"),

    mcq(r"""
Which type can hold any value including null?
""", ["Object?", "Object", "dynamic only", "Null"], "Object?"),

    mcq(r"""
Where do objects like lists and class instances live?
""", ["On the heap", "On the call stack", "In the CPU registers only", "In the source file"],
        "On the heap"),

    mcq(r"""
What lives in a function's stack frame?
""", ["Its parameters, local variable slots and return address",
       "Every object it creates", "The whole program's data", "Only global variables"],
        "Its parameters, local variable slots and return address"),

    mcq(r"""
When can the garbage collector free an object?
""", ["When it's no longer reachable from any live reference",
       "When the function that created it returns", "Every 5 seconds",
       "When you call delete on it"], "When it's no longer reachable from any live reference"),

    mcq(r"""
What's the most common cause of a "memory leak" in Dart?
""", ["Keeping objects reachable in long-lived collections like caches",
       "Forgetting to call free()", "Using too many local variables",
       "Using final instead of var"],
        "Keeping objects reachable in long-lived collections like caches"),

    mcq(r"""
What does this print?

```dart
void main() {
  final original = [[1], [2]];
  final copy = [...original];
  original[0].add(9);
  print(copy);
}
```
""", ["[[1, 9], [2]]", "[[1], [2]]", "[[9], [2]]", "[[1], [2], [9]]"], "[[1, 9], [2]]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final original = [[1], [2]];
  final copy = [for (final r in original) [...r]];
  original[0].add(9);
  print(copy);
}
```
""", ["[[1], [2]]", "[[1, 9], [2]]", "[[9], [2]]", "[]"], "[[1], [2]]"),

    mcq(r"""
Which of these makes a SHALLOW copy?
""", ["list.toList()", "A collection-for that copies each inner list",
       "A recursive deep copy function", "jsonDecode(jsonEncode(list))"], "list.toList()"),

    mcq(r"""
What does this print?

```dart
void main() {
  final grid = List.filled(2, [0, 0]);
  grid[0][0] = 5;
  print(grid);
}
```
""", ["[[5, 0], [5, 0]]", "[[5, 0], [0, 0]]", "[[0, 0], [0, 0]]", "It throws an error"],
        "[[5, 0], [5, 0]]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final grid = List.generate(2, (_) => [0, 0]);
  grid[0][0] = 5;
  print(grid);
}
```
""", ["[[5, 0], [0, 0]]", "[[5, 0], [5, 0]]", "[[0, 0], [0, 0]]", "It throws an error"],
        "[[5, 0], [0, 0]]"),

    fill(r"""
Build a grid with a separate row for each index:

```dart
void main() {
  final grid = List.%fill%(3, (_) => List.filled(3, 0));
  print(grid);
}
```
""", "generate"),

    mcq(r"""
In a linked list node `class Node { int value; Node? next; }`, what does `next == null` mean?
""", ["This is the last node", "The node is broken", "The value is zero",
       "The list is empty"], "This is the last node"),

    mcq(r"""
What does this print?

```dart
class Node {
  final int value;
  Node? next;
  Node(this.value);
}

void main() {
  final a = Node(1);
  a.next = Node(2);
  a.next!.next = Node(3);
  Node? n = a;
  var sum = 0;
  while (n != null) {
    sum += n.value;
    n = n.next;
  }
  print(sum);
}
```
""", ["6", "3", "1", "0"], "6"),

    mcq(r"""
Why do linked lists, trees and graphs depend on references?
""", ["Their nodes point to other node objects", "They store everything in one string",
       "They can only hold ints", "They are always immutable"],
        "Their nodes point to other node objects"),

    order(r"""
Complete the value-equality override:

```dart
class Money {
  final int cents;
  final String currency;
  Money(this.cents, this.currency);

  @override
  bool operator ==(Object other) =>
      other %order% Money && other.cents == cents && other.currency == currency;

  @override
  int get %order% => Object.%order%(cents, currency);
}
```
""", ["is", "hashCode", "hash", "as", "toString", "identical"], ["is", "hashCode", "hash"]),

    mcq(r"""
What does this print?

```dart
class Money {
  final int cents;
  Money(this.cents);

  @override
  bool operator ==(Object other) => other is Money && other.cents == cents;

  @override
  int get hashCode => cents.hashCode;
}

void main() {
  final wallet = {Money(100), Money(100), Money(50)};
  print(wallet.length);
}
```
""", ["2", "3", "1", "0"], "2"),

    mcq(r"""
What does overriding `toString` change?
""", ["How the object is printed", "How it is compared with ==", "Its hash code",
       "Whether it can be stored in a Set"], "How the object is printed"),

    mcq(r"""
What does printing an object without `toString` show?
""", ["Instance of 'ClassName'", "Its field values", "Its memory address in hex", "null"],
        "Instance of 'ClassName'"),

    mcq(r"""
Which collections compare by identity with `==`?
""", ["List, Set and Map", "String and int", "Records", "double and bool"],
        "List, Set and Map"),

    mcq(r"""
What does this print?

```dart
void main() {
  const a = [1, 2];
  const b = [1, 2];
  print(identical(a, b));
}
```
""", ["true", "false", "null", "It doesn't compile"], "true"),

    mcq(r"""
Why are identical const lists the same object?
""", ["Dart canonicalizes equal compile-time constants into one instance",
       "Lists always compare by value", "const copies the list", "It's a coincidence"],
        "Dart canonicalizes equal compile-time constants into one instance"),

    mcq(r"""
Which is the safest type of Map key?
""", ["An immutable value with proper == and hashCode, like a String or record",
       "A mutable List", "A class with mutable fields used in hashCode",
       "A StringBuffer"],
        "An immutable value with proper == and hashCode, like a String or record"),

    mcq(r"""
What error is thrown when too many objects are kept alive and memory runs out?
""", ["OutOfMemoryError", "StackOverflowError", "RangeError", "StateError"],
        "OutOfMemoryError"),

    mcq(r"""
What does this print?

```dart
void main() {
  final cache = <int, List<int>>{};
  for (var i = 0; i < 3; i++) {
    cache[i] = [i];
  }
  cache.clear();
  print(cache.length);
}
```
""", ["0", "3", "null", "It throws an error"], "0"),

    order(r"""
Make a deep copy of a map of lists:

```dart
Map<String, List<int>> deepCopy(Map<String, List<int>> m) =>
    {%order% (final e in m.%order%) e.key: [...e.%order%]};
```
""", ["for", "entries", "value", "keys", "while", "values"], ["for", "entries", "value"]),
]
