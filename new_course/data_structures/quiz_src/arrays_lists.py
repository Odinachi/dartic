QUESTIONS = [
    mcq(r"""
Why is reading `list[i]` O(1)?
""", ["Elements are contiguous, so the address is start + i × slot size",
       "Dart caches every element in a Map", "The list is always sorted",
       "Dart scans from the end"],
        "Elements are contiguous, so the address is start + i × slot size"),

    mcq(r"""
What is the cost of `list.insert(0, x)` on a list of n elements?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the cost of `list.removeLast()`?
""", ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "O(1)"),

    mcq(r"""
What is the cost of `list.indexOf(x)`?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the cost of `list.remove(x)` (remove by value)?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
How many elements shift when inserting at index 2 in a list of length 10?
""", ["8", "2", "10", "0"], "8"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [10, 20, 30];
  a.insert(1, 15);
  print(a);
}
```
""", ["[10, 15, 20, 30]", "[15, 10, 20, 30]", "[10, 20, 15, 30]", "[10, 15, 30]"],
        "[10, 15, 20, 30]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = ['a', 'b', 'c', 'd'];
  print(a.removeAt(1));
  print(a);
}
```
""", ["b then [a, c, d]", "a then [b, c, d]", "[a, c, d] then b", "c then [a, b, d]"],
        "b then [a, c, d]"),

    mcq(r"""
What happens here?

```dart
void main() {
  final seats = List<String>.filled(3, '');
  seats.add('x');
}
```
""", ["It throws an UnsupportedError", "seats becomes length 4", "Nothing happens",
       "It doesn't compile"], "It throws an UnsupportedError"),

    mcq(r"""
Is a list created with `List.generate(3, (i) => i)` growable by default?
""", ["Yes", "No", "Only in release mode", "Only for ints"], "Yes"),

    mcq(r"""
What does this print?

```dart
void main() {
  final seats = List<String>.filled(3, '-');
  seats[1] = 'Ada';
  print(seats);
}
```
""", ["[-, Ada, -]", "[Ada, -, -]", "[-, -, Ada]", "It throws an error"], "[-, Ada, -]"),

    fill(r"""
Get the number of elements in O(1):

```dart
void main() {
  final a = [4, 5, 6];
  print(a.%fill%); // 3
}
```
""", "length"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [10, 20, 30];
  print(a[a.length - 1]);
}
```
""", ["30", "20", "It throws a RangeError", "3"], "30"),

    mcq(r"""
What happens with `a[a.length]` on a non-empty list?
""", ["It throws a RangeError", "It returns null", "It returns the last element",
       "It returns 0"], "It throws a RangeError"),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [5, 3, 8, 1, 9];
  print(nums.sublist(1, 3));
}
```
""", ["[3, 8]", "[3, 8, 1]", "[5, 3]", "[8, 1]"], "[3, 8]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [1, 2, 3, 4, 5];
  print(nums.take(2).toList());
  print(nums.skip(3).toList());
}
```
""", ["[1, 2] then [4, 5]", "[1, 2] then [3, 4, 5]", "[4, 5] then [1, 2]", "[2] then [5]"],
        "[1, 2] then [4, 5]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final nums = [3, 1, 2];
  final sorted = [...nums]..sort();
  print(nums);
  print(sorted);
}
```
""", ["[3, 1, 2] then [1, 2, 3]", "[1, 2, 3] then [1, 2, 3]", "[3, 1, 2] then [3, 1, 2]",
       "null then [1, 2, 3]"], "[3, 1, 2] then [1, 2, 3]"),

    fill(r"""
Use a cascade to sort a copy and return it in one expression:

```dart
void main() {
  final nums = [3, 1, 2];
  final sorted = [...nums]%fill%sort();
  print(sorted);
}
```
""", ".."),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3, 4, 5];
  a.removeRange(1, 3);
  print(a);
}
```
""", ["[1, 4, 5]", "[1, 2, 5]", "[4, 5]", "[1, 3, 4, 5]"], "[1, 4, 5]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3, 4];
  a.fillRange(1, 3, 0);
  print(a);
}
```
""", ["[1, 0, 0, 4]", "[0, 0, 3, 4]", "[1, 0, 0, 0]", "[1, 2, 0, 4]"], "[1, 0, 0, 4]"),

    mcq(r"""
What happens here?

```dart
void main() {
  final nums = [1, 2, 3, 4];
  for (final n in nums) {
    if (n.isEven) nums.remove(n);
  }
}
```
""", ["It throws a ConcurrentModificationError", "nums becomes [1, 3]",
       "nums becomes [1, 2, 3, 4]", "It doesn't compile"],
        "It throws a ConcurrentModificationError"),

    fill(r"""
Safely remove all even numbers in one pass:

```dart
void main() {
  final nums = [1, 2, 3, 4];
  nums.%fill%((n) => n.isEven);
  print(nums); // [1, 3]
}
```
""", "removeWhere"),

    mcq(r"""
What does this print?

```dart
void main() {
  final temps = [20, 25, 30];
  for (final (i, t) in temps.indexed) {
    if (t > 22) print(i);
  }
}
```
""", ["1 then 2", "0", "25 then 30", "2"], "1 then 2"),

    mcq(r"""
What is the cost of visiting every cell of a grid with r rows and c columns?
""", ["O(r × c)", "O(r + c)", "O(r)", "O(1)"], "O(r × c)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final grid = List.generate(2, (_) => List.filled(3, 0));
  grid[1][2] = 7;
  print(grid);
}
```
""", ["[[0, 0, 0], [0, 0, 7]]", "[[0, 0, 7], [0, 0, 7]]", "[[0, 7, 0], [0, 0, 0]]",
       "[[7, 0, 0], [0, 0, 0]]"], "[[0, 0, 0], [0, 0, 7]]"),

    mcq(r"""
In a row-major flattened grid of width w, what index stores cell (x, y)?
""", ["y * w + x", "x * w + y", "x + y", "w * x * y"], "y * w + x"),

    mcq(r"""
What does this print?

```dart
void main() {
  const width = 5;
  int index(int x, int y) => y * width + x;
  print(index(3, 2));
}
```
""", ["13", "17", "10", "5"], "13"),

    order(r"""
Complete the in-place reverse:

```dart
void reverse(List<int> a) {
  var left = 0, right = a.length - 1;
  while (left %order% right) {
    final tmp = a[left];
    a[left] = a[%order%];
    a[right] = %order%;
    left++;
    right--;
  }
}
```
""", ["<", "right", "tmp", "<=", "left", ">"], ["<", "right", "tmp"]),

    mcq(r"""
What is the space complexity of reversing a list in place with two pointers?
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
What does this print?

```dart
List<int> rotateRight(List<int> a, int k) {
  k %= a.length;
  return [...a.sublist(a.length - k), ...a.sublist(0, a.length - k)];
}

void main() {
  print(rotateRight([1, 2, 3, 4, 5], 1));
}
```
""", ["[5, 1, 2, 3, 4]", "[2, 3, 4, 5, 1]", "[1, 2, 3, 4, 5]", "[4, 5, 1, 2, 3]"],
        "[5, 1, 2, 3, 4]"),

    mcq(r"""
Why does `rotateRight` use `k %= a.length`?
""", ["Rotating by the length returns the same list, so large k can be reduced",
       "To make k negative", "To sort the list", "It's required for sublist to work"],
        "Rotating by the length returns the same list, so large k can be reduced"),

    mcq(r"""
What does this print?

```dart
int dedupe(List<int> a) {
  var write = 1;
  for (var read = 1; read < a.length; read++) {
    if (a[read] != a[write - 1]) a[write++] = a[read];
  }
  a.length = write;
  return write;
}

void main() {
  final a = [2, 2, 2, 5, 7, 7];
  dedupe(a);
  print(a);
}
```
""", ["[2, 5, 7]", "[2, 2, 5, 7]", "[2, 5, 7, 7]", "[5, 7]"], "[2, 5, 7]"),

    mcq(r"""
Why does the in-place dedupe require a sorted list?
""", ["Duplicates must be adjacent to be detected by comparing neighbors",
       "Unsorted lists can't be modified", "Sorting makes it O(1)",
       "It doesn't; it works on any list"],
        "Duplicates must be adjacent to be detected by comparing neighbors"),

    fill(r"""
Truncate a growable list to its first 3 elements:

```dart
void main() {
  final a = [1, 2, 3, 4, 5];
  a.%fill% = 3;
  print(a); // [1, 2, 3]
}
```
""", "length"),

    mcq(r"""
In `MyList.insert`, why does the shifting loop run backwards from the end?
""", ["So elements are moved before they get overwritten",
       "Because Dart loops can't count upwards", "To sort the list",
       "To make it O(1)"], "So elements are moved before they get overwritten"),

    mcq(r"""
Why does `MyList.removeAt` set the old last slot to null?
""", ["So the removed reference doesn't keep the object alive (lets the GC free it)",
       "To mark the list as sorted", "Because Dart requires it",
       "To make removeAt O(1)"],
        "So the removed reference doesn't keep the object alive (lets the GC free it)"),

    fill(r"""
Declare an index-assignment operator:

```dart
class Box {
  final _items = [0, 0];
  void operator %fill%(int i, int v) => _items[i] = v;
}
```
""", "[]="),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [3, 6, 9];
  print(a.contains(6));
  print(a.indexOf(9));
}
```
""", ["true then 2", "true then 3", "false then 2", "6 then 9"], "true then 2"),

    mcq(r"""
What does `indexOf` return when the value isn't found?
""", ["-1", "null", "0", "It throws an error"], "-1"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3];
  print(a.reversed.toList());
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "(3, 2, 1)", "[3]"], "[3, 2, 1]"),

    mcq(r"""
Which method returns a lazy view of a range without copying it?
""", ["getRange", "sublist", "toList", "removeRange"], "getRange"),

    mcq(r"""
What is the cost of `list.sublist(a, b)`?
""", ["O(b − a)", "O(1)", "O(n²)", "O(log n)"], "O(b − a)"),

    mcq(r"""
What does this print?

```dart
void moveZeros(List<int> a) {
  var w = 0;
  for (final x in a) {
    if (x != 0) a[w++] = x;
  }
  while (w < a.length) {
    a[w++] = 0;
  }
}

void main() {
  final a = [0, 4, 0, 5, 6];
  moveZeros(a);
  print(a);
}
```
""", ["[4, 5, 6, 0, 0]", "[0, 0, 4, 5, 6]", "[4, 0, 5, 0, 6]", "[6, 5, 4, 0, 0]"],
        "[4, 5, 6, 0, 0]"),

    mcq(r"""
Why is replacing elements during for-in OK in `moveZeros`, but removing isn't?
""", ["Replacing doesn't change the length; removing does",
       "for-in copies the list first", "Replacing is O(n)",
       "Dart doesn't allow removing at all"],
        "Replacing doesn't change the length; removing does"),

    mcq(r"""
Which structure should you use if you add and remove at the FRONT often?
""", ["Queue / ListQueue", "List", "SplayTreeSet", "String"], "Queue / ListQueue"),

    mcq(r"""
Which structure should you use for frequent "does it contain x?" checks?
""", ["Set", "List", "Queue", "StringBuffer"], "Set"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = <int>[];
  print(a.isEmpty);
  a.add(1);
  print(a.first == a.last);
}
```
""", ["true then true", "true then false", "false then true", "It throws an error"],
        "true then true"),

    mcq(r"""
What happens when calling `.first` on an empty list?
""", ["It throws a StateError", "It returns null", "It returns 0", "It returns -1"],
        "It throws a StateError"),

    order(r"""
Transpose a grid:

```dart
List<List<int>> transpose(List<List<int>> g) => List.%order%(
      g[0].%order%,
      (c) => List.generate(g.length, (r) => g[%order%][%order%]),
    );
```
""", ["generate", "length", "r", "c", "filled", "first"], ["generate", "length", "r", "c"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final g = [
    [1, 2, 3],
    [4, 5, 6],
  ];
  final t = List.generate(3, (c) => List.generate(2, (r) => g[r][c]));
  print(t);
}
```
""", ["[[1, 4], [2, 5], [3, 6]]", "[[1, 2, 3], [4, 5, 6]]", "[[4, 1], [5, 2], [6, 3]]",
       "[[1, 2], [3, 4], [5, 6]]"], "[[1, 4], [2, 5], [3, 6]]"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(List.filled(3, 'hi').join('-'));
}
```
""", ["hi-hi-hi", "hihihi", "[hi, hi, hi]", "hi-hi-hi-"], "hi-hi-hi"),

    mcq(r"""
What is the cost of `list.add(x)` on a growable list?
""", ["O(1) amortized", "O(n) always", "O(log n)", "O(n²)"], "O(1) amortized"),

    mcq(r"""
Inserting at index `list.length` is equivalent to:
""", ["add", "insert(0, x)", "removeLast", "It throws a RangeError"], "add"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 3];
  a.insert(a.length, 4);
  print(a);
}
```
""", ["[1, 2, 3, 4]", "[4, 1, 2, 3]", "It throws a RangeError", "[1, 2, 4, 3]"],
        "[1, 2, 3, 4]"),

    mcq(r"""
What is the total cost of calling `removeAt(0)` until a list of n items is empty?
""", ["O(n²)", "O(n)", "O(n log n)", "O(1)"], "O(n²)"),

    mcq(r"""
Which operation on a List is O(n log n)?
""", ["sort()", "add()", "removeLast()", "operator []"], "sort()"),

    mcq(r"""
What does this print?

```dart
void main() {
  final temps = [21.0, 23.0, 25.0];
  var total = 0.0;
  for (final t in temps) {
    total += t;
  }
  print((total / temps.length).toStringAsFixed(1));
}
```
""", ["23.0", "23", "69.0", "22.5"], "23.0"),
]
