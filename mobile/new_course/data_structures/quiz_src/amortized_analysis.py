QUESTIONS = [
    mcq(r"""
What is amortized cost?
""", [
        "The average cost per operation over a sequence of operations, guaranteed",
        "The cost of the single slowest operation",
        "The expected cost on random input",
        "The memory used by one operation",
    ], "The average cost per operation over a sequence of operations, guaranteed"),

    mcq(r"""
What is the amortized cost of `List.add` in Dart?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What is the worst-case cost of a single `List.add` call?
""", ["O(n), when the list has to grow and copy", "O(1) always", "O(log n)", "O(n²)"],
        "O(n), when the list has to grow and copy"),

    mcq(r"""
How does amortized analysis differ from average-case analysis?
""", [
        "Amortized is guaranteed for any sequence; average case depends on the input",
        "They are exactly the same thing",
        "Average case is always slower",
        "Amortized only applies to sorting",
    ], "Amortized is guaranteed for any sequence; average case depends on the input"),

    mcq(r"""
When a growable list is full, what usually happens on the next add?
""", [
        "A bigger buffer (about double) is allocated and all items are copied",
        "The new item overwrites the first item",
        "Dart throws a RangeError",
        "The list becomes a linked list",
    ], "A bigger buffer (about double) is allocated and all items are copied"),

    mcq(r"""
Starting from capacity 1 and doubling when full, how many element copies happen in total for 16 adds?
""", ["15", "16", "31", "120"], "15"),

    mcq(r"""
What is `1 + 2 + 4 + 8 + 16`?
""", ["31", "32", "16", "30"], "31"),

    mcq(r"""
Why does doubling capacity make `add` O(1) amortized?
""", [
        "The copies form a geometric series that sums to less than n",
        "Doubling avoids copying entirely",
        "Each add copies exactly one element",
        "Doubling sorts the list for free",
    ], "The copies form a geometric series that sums to less than n"),

    mcq(r"""
If a list grows by a constant +10 slots each time it's full, what is the amortized cost of add?
""", ["O(n)", "O(1)", "O(log n)", "O(10)"], "O(n)"),

    mcq(r"""
If a list grows by a constant +10 slots each time it's full, what is the total cost of n adds?
""", ["O(n²)", "O(n)", "O(n log n)", "O(10n)"], "O(n²)"),

    mcq(r"""
Which growth strategy gives O(1) amortized add?
""", ["Multiply capacity by 1.5", "Add 100 slots", "Add 1 slot", "Add 1,000 slots"],
        "Multiply capacity by 1.5"),

    mcq(r"""
What does this print?

```dart
void main() {
  var capacity = 1;
  var copies = 0;
  for (var length = 0; length < 8; length++) {
    if (length == capacity) {
      copies += length;
      capacity *= 2;
    }
  }
  print('$capacity $copies');
}
```
""", ["8 7", "8 8", "16 15", "4 3"], "8 7"),

    fill(r"""
Create a fixed-length list of 5 zeros:

```dart
void main() {
  final buf = List<int>.%fill%(5, 0);
  print(buf); // [0, 0, 0, 0, 0]
}
```
""", "filled"),

    mcq(r"""
What happens here?

```dart
void main() {
  final fixed = List<int>.filled(2, 0);
  fixed.add(1);
}
```
""", ["It throws an UnsupportedError", "It prints [0, 0, 1]", "It silently ignores the add",
       "It grows the list to 3"], "It throws an UnsupportedError"),

    fill(r"""
Allow the preallocated list to grow:

```dart
void main() {
  final list = List<int>.filled(3, 0, %fill%: true);
  list.add(9);
  print(list); // [0, 0, 0, 9]
}
```
""", "growable"),

    mcq(r"""
What does this print?

```dart
void main() {
  final list = List<int>.filled(3, 0, growable: true);
  list.add(9);
  print(list.length);
}
```
""", ["4", "3", "9", "It throws an error"], "4"),

    mcq(r"""
What does this print?

```dart
void main() {
  final squares = List<int>.generate(4, (i) => i * i);
  print(squares);
}
```
""", ["[0, 1, 4, 9]", "[1, 4, 9, 16]", "[0, 1, 2, 3]", "[0, 2, 4, 6]"], "[0, 1, 4, 9]"),

    mcq(r"""
Why might a game preallocate a list of 10,000 particles with `List.filled`?
""", [
        "To avoid a slow copy (growth pause) during gameplay",
        "Because growable lists can't hold doubles",
        "Because List.add is O(n²)",
        "To make the list sorted",
    ], "To avoid a slow copy (growth pause) during gameplay"),

    mcq(r"""
In the banker's method, how many coins does each add pay for a doubling list?
""", ["3 (a small constant)", "n", "log n", "0"], "3 (a small constant)"),

    mcq(r"""
In the banker's method, what proves the amortized bound is correct?
""", [
        "The coin balance never goes negative",
        "The coin balance is always exactly zero",
        "Every operation costs exactly the same",
        "The list never grows",
    ], "The coin balance never goes negative"),

    mcq(r"""
A stack supports `push`, `pop` and `popAll` (removes everything). What is the amortized cost of each operation over any sequence?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
Why is `popAll` cheap when amortized?
""", [
        "Each item can only be popped once after being pushed once",
        "popAll doesn't actually remove items",
        "popAll is always called on an empty stack",
        "Lists remove all items in O(1)",
    ], "Each item can only be popped once after being pushed once"),

    mcq(r"""
What does this print?

```dart
void main() {
  final items = <int>[1, 2, 3, 4];
  var count = 0;
  while (items.isNotEmpty) {
    items.removeLast();
    count++;
  }
  print(count);
}
```
""", ["4", "3", "0", "10"], "4"),

    mcq(r"""
How many bits flip when a binary counter goes from 0111 to 1000?
""", ["4", "1", "3", "8"], "4"),

    mcq(r"""
What is the amortized number of bit flips per increment of a binary counter?
""", ["O(1) (less than 2)", "O(log n)", "O(n)", "O(number of bits)"],
        "O(1) (less than 2)"),

    mcq(r"""
How often does bit i (counting from 0) flip in a binary counter?
""", ["Every 2ⁱ increments", "Every i increments", "Every increment", "Only once"],
        "Every 2ⁱ increments"),

    mcq(r"""
What does this print?

```dart
void main() {
  final bits = [1, 1, 0, 0]; // lowest bit first
  var i = 0;
  while (bits[i] == 1) {
    bits[i] = 0;
    i++;
  }
  bits[i] = 1;
  print(bits.reversed.join());
}
```
""", ["0100", "0011", "1100", "0111"], "0100"),

    fill(r"""
Print bits with the highest bit first:

```dart
void main() {
  final bits = [1, 0, 1, 0]; // lowest bit first
  print(bits.%fill%.join()); // 0101
}
```
""", "reversed"),

    mcq(r"""
Which Dart structure is a classic example of O(log n) amortized operations?
""", ["SplayTreeMap", "List", "Set", "String"], "SplayTreeMap"),

    mcq(r"""
`Map[key] = value` occasionally triggers a resize. What is its amortized (average) cost?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
When is amortized O(1) NOT good enough?
""", [
        "Real-time code where a single slow operation must never happen",
        "Batch jobs that process data overnight",
        "Adding items to a shopping cart",
        "Counting words in a file",
    ], "Real-time code where a single slow operation must never happen"),

    mcq(r"""
What does this print?

```dart
class Counter {
  int _length = 0;
  List<int?> _buf = List.filled(2, null);
  int get capacity => _buf.length;

  void add(int v) {
    if (_length == _buf.length) {
      _buf = [..._buf, ...List<int?>.filled(_buf.length, null)];
    }
    _buf[_length++] = v;
  }
}

void main() {
  final c = Counter();
  for (var i = 0; i < 5; i++) {
    c.add(i);
  }
  print(c.capacity);
}
```
""", ["8", "5", "4", "10"], "8"),

    order(r"""
Complete the grow method that doubles the buffer:

```dart
void grow() {
  final bigger = List<int?>.%order%(buffer.%order% * %order%, null);
  for (var i = 0; i < length; i++) {
    bigger[i] = buffer[i];
  }
  buffer = bigger;
}
```
""", ["filled", "length", "2", "generate", "10", "capacity"],
        ["filled", "length", "2"]),

    fill(r"""
Overload the index operator for a custom list:

```dart
class MyList {
  final _items = [10, 20, 30];
  int %fill% [](int i) => _items[i];
}

void main() {
  print(MyList()[1]); // 20
}
```
""", "operator"),

    mcq(r"""
What does this print?

```dart
class MyList {
  final _items = [10, 20, 30];
  int operator [](int i) => _items[i];
}

void main() {
  print(MyList()[2]);
}
```
""", ["30", "20", "10", "It throws an error"], "30"),

    mcq(r"""
Which error should a custom list throw for an out-of-range index, like Dart's own List?
""", ["RangeError", "FormatException", "StateError", "TypeError"], "RangeError"),

    mcq(r"""
What does this print?

```dart
void main() {
  try {
    final list = [1, 2, 3];
    print(list[5]);
  } on RangeError {
    print('out of range');
  }
}
```
""", ["out of range", "null", "3", "0"], "out of range"),

    mcq(r"""
Suppose a list halves its capacity when it becomes half full on removal. What problem can occur?
""", [
        "Alternating add/remove at the boundary causes repeated O(n) resizes",
        "The list loses data",
        "Removal becomes O(log n)",
        "Nothing; halving at half full is ideal",
    ], "Alternating add/remove at the boundary causes repeated O(n) resizes"),

    mcq(r"""
To avoid that thrashing, when should a shrinking list halve its capacity?
""", ["When it's only one quarter full", "When it's half full", "When it's 90% full",
       "Never"], "When it's only one quarter full"),

    mcq(r"""
Over a sequence of n `List.add` calls, what is the total work?
""", ["O(n)", "O(n²)", "O(n log n)", "O(1)"], "O(n)"),

    mcq(r"""
Which statement is true about a single expensive operation in an amortized structure?
""", [
        "It can still happen, but it's paid for by many cheap operations",
        "It never happens",
        "It makes the whole structure O(n) per operation",
        "It means the structure is broken",
    ], "It can still happen, but it's paid for by many cheap operations"),

    mcq(r"""
Your monthly train pass costs $60 and you ride 30 times. What's the amortized cost per ride?
""", ["$2", "$60", "$30", "$0"], "$2"),

    mcq(r"""
What does this print?

```dart
void main() {
  var total = 0;
  for (var n = 1; n <= 8; n++) {
    var x = n - 1;
    var flips = 1;
    while (x & 1 == 1) {
      flips++;
      x >>= 1;
    }
    total += flips;
  }
  print(total);
}
```
""", ["15", "8", "16", "24"], "15"),

    mcq(r"""
Which line allocates exactly the right size once (no growth)?
""", [
        "List<int>.generate(1000, (i) => i)",
        "<int>[] then add 1000 times",
        "[] then insert(0, i) 1000 times",
        "Set<int>() then add 1000 times",
    ], "List<int>.generate(1000, (i) => i)"),

    mcq(r"""
What is the type of `copies / n` in Dart when both are ints?
""", ["double", "int", "num", "String"], "double"),

    mcq(r"""
What does this print?

```dart
void main() {
  print((7 / 2).toStringAsFixed(2));
}
```
""", ["3.50", "3", "3.5", "4.00"], "3.50"),

    mcq(r"""
Which Dart queue grows like a dynamic array and has O(1) amortized addFirst/addLast?
""", ["ListQueue", "DoubleLinkedQueue", "SplayTreeSet", "HashSet"], "ListQueue"),

    order(r"""
Complete the banker's simulation:

```dart
void main() {
  var cap = 1, len = 0, bank = 0;
  for (var i = 0; i < 10; i++) {
    bank %order% 3;
    if (len == cap) {
      bank -= len;
      cap %order% 2;
    }
    bank %order% 1;
    len++;
  }
  print(bank >= 0);
}
```
""", ["+=", "*=", "-=", "/=", "~/="], ["+=", "*=", "-="]),

    mcq(r"""
What does this banker's-method simulation print?

```dart
void main() {
  var cap = 1, len = 0, bank = 0;
  for (var i = 0; i < 10; i++) {
    bank += 3;
    if (len == cap) {
      bank -= len;
      cap *= 2;
    }
    bank -= 1;
    len++;
  }
  print(bank >= 0);
}
```
""", ["true", "false", "0", "It throws an error"], "true"),

    mcq(r"""
Why is "doubling" a common growth factor rather than ×10?
""", [
        "Both are O(1) amortized, but ×10 can waste much more unused memory",
        "×10 is O(n) amortized",
        "×10 isn't allowed in Dart",
        "Doubling avoids copying",
    ], "Both are O(1) amortized, but ×10 can waste much more unused memory"),

    mcq(r"""
After doubling from capacity 8 to 16 with 9 items, how much of the buffer is unused?
""", ["7 slots", "8 slots", "9 slots", "0 slots"], "7 slots"),

    mcq(r"""
What does this print?

```dart
void main() {
  final growing = <double>[];
  for (var i = 0; i < 3; i++) {
    growing.add(i * 0.5);
  }
  print(growing);
}
```
""", ["[0.0, 0.5, 1.0]", "[0, 0.5, 1]", "[0.5, 1.0, 1.5]", "[0.0, 1.0, 2.0]"],
        "[0.0, 0.5, 1.0]"),

    mcq(r"""
Which of these has the same total cost guarantee as n `List.add` calls?
""", ["n increments of a binary counter", "n insert(0, x) calls", "n sort() calls",
       "n contains() calls on a List"], "n increments of a binary counter"),

    mcq(r"""
What is the space overhead of a doubling dynamic array in the worst case, right after it grows?
""", ["About 2× the elements stored", "Exactly the elements stored", "10× the elements stored",
       "n² slots"], "About 2× the elements stored"),

    fill(r"""
Complete the method that removes the last element in O(1):

```dart
void main() {
  final stack = [1, 2, 3];
  print(stack.%fill%()); // 3
}
```
""", "removeLast"),

    mcq(r"""
In the GrowableIntList example, what does `RangeError.index(...)` protect against?
""", ["Reading slots beyond the used length", "Adding too many items",
       "Copying null values", "Doubling too often"], "Reading slots beyond the used length"),
]
