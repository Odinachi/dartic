# Arrays & Dart Lists

Imagine a row of **school lockers** 🔐, numbered 0, 1, 2, 3...

- Every locker is the **same size** and they sit **side by side**.
- To open locker **#57**, you don't check lockers 0 to 56. You walk straight to it, because you know exactly **where** it is.
- But if you want to squeeze a new locker in at position 3, everyone from locker 3 onward has to **shift down one** 😩.

👉 That's an **array**:

> An **array** stores elements in **one contiguous block of memory**, so any element can be reached **instantly by its index**, but inserting or removing in the middle means **shifting** everything after it.

In Dart, arrays are called **`List`**. They are the most used data structure in almost every program, so understanding their costs is a superpower. 🦸

---

## 🧠 How Index Access Is O(1)

Because elements are stored side by side and every slot has the same size, the computer finds element `i` with simple math:

```text
address of list[i] = start address + i × slot size
```

One multiplication and one addition, no matter if the list has 10 items or 10 million. That's **O(1) random access**.

```dart
void main() {
  final lockers = List.generate(10000000, (i) => 'Locker $i');

  final sw = Stopwatch()..start();
  final a = lockers[3];
  final b = lockers[9999999];
  sw.stop();

  print(a); // Locker 3
  print(b); // Locker 9999999
  print('Both lookups took ${sw.elapsedMicroseconds} µs');
}
```

**🔍 What This Code Does:**

1. **Large List**: `List.generate` builds 10 million entries.
2. **Instant Access**: Reading index 3 and index 9,999,999 costs the same, a single address calculation.
3. **Microseconds**: `elapsedMicroseconds` shows both lookups are effectively instant.
4. **Zero-Based**: The first element is at index `0` and the last at `length - 1`.

---

## 📦 Fixed-Length vs Growable Lists

Dart has two flavors of List:

| | Fixed-length | Growable |
|---|-------------|----------|
| **Created with** | `List.filled(n, x)`, `List.generate(n, f, growable: false)`, `List.unmodifiable` | `[]`, `[1, 2]`, `List.empty(growable: true)`, `toList()` |
| **Can change length?** | ❌ No: `add`/`remove` throw | ✅ Yes |
| **Can change elements?** | ✅ Yes (unless unmodifiable) | ✅ Yes |
| **Like** | A classic array | A dynamic array (ArrayList, vector) |

```dart
void main() {
  // Growable: the default for literals
  final scores = <int>[90, 85];
  scores.add(77);
  print(scores); // [90, 85, 77]

  // Fixed-length: exact size, elements can still be replaced
  final seats = List<String>.filled(3, 'empty');
  seats[1] = 'Ada';
  print(seats); // [empty, Ada, empty]

  try {
    seats.add('Bob');
  } on UnsupportedError catch (e) {
    print('Fixed-length: ${e.message}');
  }

  // List.generate is growable by default
  final squares = List<int>.generate(5, (i) => i * i);
  squares.add(25);
  print(squares); // [0, 1, 4, 9, 16, 25]
}
```

**🔍 What This Code Does:**

1. **Literals Are Growable**: `[90, 85]` can `add` and `remove`.
2. **`List.filled` Is Fixed by Default**: You can replace elements with `seats[1] = ...`, but not change the length.
3. **Catching the Error**: Adding to a fixed list throws `UnsupportedError`.
4. **`List.generate`**: Growable by default, unlike `List.filled`.
5. **When to Use Fixed**: When the size is known and must not change (a game board, a buffer), it's slightly faster and documents intent.

---

## ⚙️ The Cost of Every Common Operation

| Operation | Example | Cost | Why |
|-----------|---------|------|-----|
| Read / write by index | `list[i]`, `list[i] = x` | **O(1)** | Address math |
| Length | `list.length` | **O(1)** | Stored in a field |
| Add to end | `list.add(x)` | **O(1)** amortized | Occasionally grows |
| Remove from end | `list.removeLast()` | **O(1)** | Nothing shifts |
| Insert at index | `list.insert(i, x)` | **O(n − i)** | Shift right |
| Remove at index | `list.removeAt(i)` | **O(n − i)** | Shift left |
| Insert / remove at front | `insert(0, x)`, `removeAt(0)` | **O(n)** | Everything shifts |
| Search | `contains`, `indexOf` | **O(n)** | Check one by one |
| Remove by value | `list.remove(x)` | **O(n)** | Search + shift |
| Sort | `list.sort()` | **O(n log n)** | Comparison sort |
| Copy | `toList()`, `[...list]` | **O(n)** | Every element copied |
| Sublist | `list.sublist(a, b)` | **O(b − a)** | Copies that range |

> 💡 The pattern: **the end is cheap**, **the front is expensive**, **searching is linear**.

---

## 🔀 Seeing the Shift

Let's count exactly how many elements move when inserting at different positions.

```dart
int insertAndCountShifts(List<int> list, int index, int value) {
  final shifts = list.length - index;
  list.insert(index, value);
  return shifts;
}

void main() {
  final list = List<int>.generate(1000, (i) => i);

  print('Insert at end:    ${insertAndCountShifts(list, list.length, -1)} shifts');
  print('Insert in middle: ${insertAndCountShifts(list, list.length ~/ 2, -1)} shifts');
  print('Insert at front:  ${insertAndCountShifts(list, 0, -1)} shifts');
}
```

**🔍 What This Code Does:**

1. **Counting Moves**: Every element at or after `index` has to move one slot to the right.
2. **End**: 0 shifts. Inserting at `list.length` is the same as `add`.
3. **Middle**: About 500 shifts for a list of 1,000.
4. **Front**: About 1,000 shifts, every single element moves.
5. **Lesson**: If you frequently add or remove at the front, use a `Queue` instead.

---

## 🛠️ Building Our Own Array-Backed List

To truly understand Lists, let's implement the core operations by hand using a fixed-length buffer.

```dart
class MyList<T> {
  List<T?> _data = List<T?>.filled(4, null);
  int _length = 0;

  int get length => _length;

  T operator [](int i) {
    _checkIndex(i);
    return _data[i] as T;
  }

  void operator []=(int i, T value) {
    _checkIndex(i);
    _data[i] = value;
  }

  void add(T value) {
    if (_length == _data.length) _grow();
    _data[_length++] = value;
  }

  void insert(int index, T value) {
    if (index < 0 || index > _length) {
      throw RangeError.range(index, 0, _length, 'index');
    }
    if (_length == _data.length) _grow();
    // shift right, starting from the end
    for (var i = _length; i > index; i--) {
      _data[i] = _data[i - 1];
    }
    _data[index] = value;
    _length++;
  }

  T removeAt(int index) {
    _checkIndex(index);
    final removed = _data[index] as T;
    // shift left
    for (var i = index; i < _length - 1; i++) {
      _data[i] = _data[i + 1];
    }
    _data[--_length] = null; // clear the old last slot
    return removed;
  }

  int indexOf(T value) {
    for (var i = 0; i < _length; i++) {
      if (_data[i] == value) return i;
    }
    return -1;
  }

  void _grow() {
    final bigger = List<T?>.filled(_data.length * 2, null);
    for (var i = 0; i < _length; i++) {
      bigger[i] = _data[i];
    }
    _data = bigger;
  }

  void _checkIndex(int i) {
    if (i < 0 || i >= _length) {
      throw RangeError.index(i, this, 'index', null, _length);
    }
  }

  @override
  String toString() =>
      '[${[for (var i = 0; i < _length; i++) _data[i]].join(', ')}]';
}

void main() {
  final list = MyList<String>();
  list.add('B');
  list.add('D');
  list.insert(0, 'A');
  list.insert(2, 'C');
  print(list); // [A, B, C, D]

  print(list.removeAt(1)); // B
  print(list);             // [A, C, D]
  print(list.indexOf('D')); // 2

  list[0] = 'Z';
  print(list[0]);          // Z
  print(list.length);      // 3
}
```

**🔍 What This Code Does:**

This code demonstrates **a complete dynamic array built from a fixed buffer**:

1. **Generic Type `T`**: `MyList<String>` and `MyList<int>` both work.

2. **Index Operators**: `operator []` and `operator []=` let us use `list[0]` syntax, with bounds checks.

3. **Shift Right on Insert**: The loop runs **backwards** from the end so we don't overwrite elements before moving them.

4. **Shift Left on Remove**: Elements after the removed index move down, and the old last slot is cleared to `null` so the GC can free the object.

5. **Linear Search**: `indexOf` checks each element in turn, O(n).

6. **Growth**: When full, `_grow` doubles the buffer (see **Amortized Analysis**).

---

## 🔁 Iterating Efficiently

```dart
void main() {
  final temps = [21.5, 23.0, 19.8, 25.1, 22.4];

  // 1. Classic index loop: when you need the index
  for (var i = 0; i < temps.length; i++) {
    print('Day $i: ${temps[i]}°C');
  }

  // 2. for-in: cleanest when you only need values
  var total = 0.0;
  for (final t in temps) {
    total += t;
  }
  print('Average: ${(total / temps.length).toStringAsFixed(1)}°C');

  // 3. indexed (Dart 3.x) with records
  for (final (i, t) in temps.indexed) {
    if (t > 24) print('Hot day at index $i');
  }

  // 4. Functional style
  final hotDays = temps.where((t) => t > 22).toList();
  print('Hot: $hotDays');
}
```

**🔍 What This Code Does:**

1. **Index Loop**: Gives you both the index and the element; avoid modifying the list's length inside it.
2. **for-in**: The simplest way to visit every element.
3. **`indexed`**: Yields `(index, value)` records, which we destructure with a pattern.
4. **`where`**: Lazily filters; `toList()` materializes the result. Each of these is O(n).

> ⚠️ Never `add` or `remove` while iterating with for-in over the same list; Dart throws a `ConcurrentModificationError`.

---

## 🧱 2D Arrays: Lists of Lists

Grids, game boards, images and matrices are all 2D arrays.

```dart
void main() {
  const rows = 3, cols = 4;

  // ✅ Each row is its own list
  final grid = List.generate(rows, (_) => List.filled(cols, 0));

  grid[1][2] = 7;
  grid[2][3] = 9;

  for (final row in grid) {
    print(row.join(' '));
  }

  // Sum every cell: O(rows × cols)
  var sum = 0;
  for (final row in grid) {
    for (final cell in row) {
      sum += cell;
    }
  }
  print('Sum: $sum'); // 16

  // Transpose: rows become columns
  final transposed = List.generate(
    cols,
    (c) => List.generate(rows, (r) => grid[r][c]),
  );
  print(transposed);
}
```

**🔍 What This Code Does:**

1. **Grid Creation**: `List.generate` builds a fresh row for each index (never `List.filled(rows, row)`, which shares one row).
2. **Two Indexes**: `grid[r][c]` reads row `r`, column `c`.
3. **Nested Loops**: Visiting every cell costs O(rows × cols).
4. **Transpose**: Builds a new grid where `transposed[c][r] = grid[r][c]`.

### Flattened 2D array

Some performance-sensitive code stores a grid in **one** list and computes the index:

```dart
void main() {
  const width = 4, height = 3;
  final pixels = List<int>.filled(width * height, 0);

  int index(int x, int y) => y * width + x;

  pixels[index(2, 1)] = 255;
  print(pixels[index(2, 1)]); // 255
  print(pixels.length);       // 12
}
```

**🔍 What This Code Does:**

1. **Row-Major Layout**: Row `y` starts at `y * width`, and column `x` is an offset within it.
2. **One Allocation**: A single list is more memory-friendly than many small lists.
3. **Same O(1) Access**: Still just math to find the slot.

---

## 🧰 Useful List Operations

```dart
void main() {
  final nums = [5, 3, 8, 1, 9, 2];

  print(nums.sublist(1, 4));             // [3, 8, 1]
  print(nums.getRange(1, 4).toList());   // [3, 8, 1] (lazy view)
  print(nums.reversed.toList());         // [2, 9, 1, 8, 3, 5]
  print(nums.take(2).toList());          // [5, 3]
  print(nums.skip(4).toList());          // [9, 2]

  final copy = [...nums]..sort();
  print(copy);                           // [1, 2, 3, 5, 8, 9]
  print(nums);                           // unchanged

  nums.removeRange(0, 2);
  print(nums);                           // [8, 1, 9, 2]

  nums.fillRange(0, 2, 0);
  print(nums);                           // [0, 0, 9, 2]

  print(List.filled(3, 'ab').join('-')); // ab-ab-ab
}
```

**🔍 What This Code Does:**

1. **`sublist(a, b)`**: Copies indexes `a` up to (not including) `b`.
2. **`getRange`**: A lazy view of the same range; no copy until you call `toList()`.
3. **`reversed`, `take`, `skip`**: Lazy Iterables, materialized with `toList()`.
4. **Cascade Sort**: `[...nums]..sort()` sorts a **copy**, leaving the original untouched.
5. **`removeRange` / `fillRange`**: Bulk operations on index ranges.

---

## 🔄 Classic Array Algorithms

### Reverse in place (two pointers)

```dart
void reverseInPlace(List<int> a) {
  var left = 0;
  var right = a.length - 1;
  while (left < right) {
    final tmp = a[left];
    a[left] = a[right];
    a[right] = tmp;
    left++;
    right--;
  }
}

void main() {
  final a = [1, 2, 3, 4, 5];
  reverseInPlace(a);
  print(a); // [5, 4, 3, 2, 1]
}
```

**🔍 What This Code Does:**

1. **Two Pointers**: One at each end, moving toward the middle.
2. **Swap**: A temporary variable holds one value during the swap.
3. **O(n) Time, O(1) Space**: Only n/2 swaps and no extra list.

### Rotate right by k

```dart
List<int> rotateRight(List<int> a, int k) {
  if (a.isEmpty) return a;
  k %= a.length;
  return [...a.sublist(a.length - k), ...a.sublist(0, a.length - k)];
}

void main() {
  print(rotateRight([1, 2, 3, 4, 5], 2)); // [4, 5, 1, 2, 3]
  print(rotateRight([1, 2, 3], 7));       // [3, 1, 2]
}
```

**🔍 What This Code Does:**

1. **Modulo**: Rotating by `length` returns the same list, so `k %= length` handles big `k`.
2. **Two Slices**: The last `k` elements move to the front.
3. **O(n)**: Every element is copied once.

### Remove duplicates from a sorted list (in place)

```dart
int dedupeSorted(List<int> a) {
  if (a.isEmpty) return 0;
  var write = 1;
  for (var read = 1; read < a.length; read++) {
    if (a[read] != a[write - 1]) {
      a[write++] = a[read];
    }
  }
  a.length = write; // shrink a growable list
  return write;
}

void main() {
  final a = [1, 1, 2, 3, 3, 3, 4];
  print(dedupeSorted(a)); // 4
  print(a);               // [1, 2, 3, 4]
}
```

**🔍 What This Code Does:**

1. **Read and Write Pointers**: `read` scans every element; `write` marks where the next unique value goes.
2. **Sorted Input**: Duplicates are adjacent, so comparing with the last written value is enough.
3. **Setting `length`**: For a growable list, assigning a smaller `length` truncates it.
4. **O(n) Time, O(1) Space**: One pass, no extra list.

---

## 🆚 List vs Other Structures

| Need | Best choice |
|------|-------------|
| Fast access by position | ✅ `List` |
| Add/remove at the end | ✅ `List` |
| Add/remove at the front | `Queue` / `ListQueue` |
| Fast "does it contain x?" | `Set` |
| Lookup by key | `Map` |
| Frequent insert/delete in the middle with a known node | Linked list |
| Always sorted | `SplayTreeSet` or keep a `List` sorted with binary search inserts |

---

## ⚠️ Common Mistakes

### 1. RangeError from off-by-one

```dart
void main() {
  final a = [10, 20, 30];
  try {
    print(a[a.length]); // ❌ valid indexes are 0..length-1
  } on RangeError catch (e) {
    print('RangeError: ${e.message}');
  }
  print(a[a.length - 1]); // ✅ 30
  print(a.last);          // ✅ 30
}
```

**🔍 What This Code Does:**

1. **Last Valid Index**: `length - 1`, not `length`.
2. **`last`**: A safer, clearer way to read the final element (it throws `StateError` on an empty list).

### 2. Modifying a list while iterating it

```dart
void main() {
  final nums = [1, 2, 3, 4, 5, 6];

  // ❌ for (final n in nums) { if (n.isEven) nums.remove(n); }
  //    throws ConcurrentModificationError

  // ✅ removeWhere does it safely in one O(n) pass
  nums.removeWhere((n) => n.isEven);
  print(nums); // [1, 3, 5]
}
```

**🔍 What This Code Does:**

1. **Concurrent Modification**: Changing the length during for-in breaks the iterator.
2. **`removeWhere`**: Safely removes all matching elements in a single pass.

### 3. Removing many items from the front one by one

Calling `removeAt(0)` in a loop is O(n²). Use `removeRange(0, k)`, `sublist(k)`, or a `Queue`.

---

## 🧪 Try It Yourself

1. Add `remove(T value)` and `contains(T value)` to `MyList`. What are their costs?
2. Write `moveZerosToEnd(List<int> a)` that keeps the order of non-zero numbers, in place, in O(n).
3. Write `rotateInPlace(List<int> a, int k)` using the **three reversals** trick: reverse all, reverse the first k, reverse the rest.
4. Create a 9×9 Sudoku grid and write a function that checks whether a row contains duplicates.

```dart
void moveZerosToEnd(List<int> a) {
  var write = 0;
  for (final x in a) {
    if (x != 0) a[write++] = x;
  }
  while (write < a.length) {
    a[write++] = 0;
  }
}

void main() {
  final a = [0, 1, 0, 3, 12];
  moveZerosToEnd(a);
  print(a); // [1, 3, 12, 0, 0]
}
```

**🔍 What This Code Does:**

1. **Compact Non-Zeros**: Every non-zero value is written to the next `write` slot, keeping its order.
2. **Fill the Rest**: Remaining slots are set to zero.
3. **Safe Iteration**: We only **replace** elements (no length change), so for-in is fine here.

---

## 📌 Key Takeaways

- ✅ A Dart `List` is an **array**: contiguous slots with **O(1)** access by index.
- ✅ **End operations** (`add`, `removeLast`) are cheap; **front/middle** inserts and removes are **O(n)** because of shifting.
- ✅ **Searching** (`contains`, `indexOf`, `remove(value)`) is **O(n)**.
- ✅ `List.filled` makes **fixed-length** lists; literals and `List.generate` are **growable**.
- ✅ Build grids with `List.generate`, or flatten them with `y * width + x`.
- ✅ In-place algorithms with **read/write pointers** save memory.
- ✅ Don't change a list's length while iterating it; use `removeWhere` and friends.

**Next up:** 🔤 **Strings as Data Structures**: immutability, `StringBuffer`, code units and runes.
