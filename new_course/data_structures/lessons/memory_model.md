# How Dart Stores Data

Imagine you and your friend both want to visit the same **house** 🏡.

- 📝 You could each have a **copy of the address** on a sticky note.
- 🏠 There's still only **one house**.

If your friend paints the front door red 🔴 and you visit later, you'll see a red door too, because you both point to the **same house**.

But if your friend **crosses out the address on their note** and writes a new one, your note doesn't change at all.

👉 That's how Dart stores objects:

> Variables don't hold objects directly. They hold **references** (like addresses) to objects that live in memory. Several variables can refer to the **same** object.

Understanding this is crucial for data structures: linked lists, trees and graphs are all built from objects **pointing to other objects**.

---

## 🧠 Everything Is an Object

In Dart, **every value is an object**, even numbers, booleans and `null`.

```dart
void main() {
  int age = 30;
  double price = 9.99;
  bool isOpen = true;
  String name = 'Dart';
  List<int> nums = [1, 2, 3];

  print(age is Object);    // true
  print(price is Object);  // true
  print(isOpen is Object); // true
  print(name is Object);   // true
  print(nums is Object);   // true
  print(null is Object);   // false (null is the only non-Object value)
}
```

**🔍 What This Code Does:**

1. **Uniform Model**: `int`, `double`, `bool`, `String` and `List` are all subtypes of `Object`.
2. **`is` Operator**: Checks whether a value is an instance of a type.
3. **Null Is Special**: With sound null safety, `null` has its own type `Null` and is **not** an `Object`. That's why `Object` excludes null and `Object?` includes it.
4. **No Primitives**: Unlike Java or C, Dart has no separate primitive types; the VM optimizes small ints and doubles behind the scenes.

---

## 🔗 Variables Hold References

When you assign one variable to another, Dart copies the **reference**, not the object.

```dart
void main() {
  final cart = ['🍎 Apple', '🍞 Bread'];
  final sameCart = cart; // copies the reference

  sameCart.add('🧀 Cheese');

  print(cart);     // [🍎 Apple, 🍞 Bread, 🧀 Cheese]
  print(sameCart); // [🍎 Apple, 🍞 Bread, 🧀 Cheese]
  print(identical(cart, sameCart)); // true
}
```

**🔍 What This Code Does:**

1. **One List, Two Names**: `cart` and `sameCart` point to the **same** list object.
2. **Mutation Is Shared**: Adding through `sameCart` changes what `cart` sees too.
3. **`identical`**: Returns `true` only when both references point to the exact same object in memory.
4. **`final` Doesn't Freeze the Object**: `final` means the *variable* can't be reassigned; the list itself can still be modified.

### Reassigning vs mutating

```dart
void main() {
  var a = [1, 2, 3];
  var b = a;

  b.add(4);        // mutate the shared object
  print(a);        // [1, 2, 3, 4]

  b = [9, 9];      // reassign b to a NEW object
  print(a);        // [1, 2, 3, 4] (unchanged)
  print(b);        // [9, 9]
}
```

**🔍 What This Code Does:**

1. **Mutation**: `b.add(4)` changes the object both variables point to.
2. **Reassignment**: `b = [9, 9]` only changes where `b` points. `a` still points to the original list.
3. **Sticky Note Analogy**: Painting the door (mutation) affects everyone; rewriting your note (reassignment) only affects you.

---

## 📦 Passing Objects to Functions

Dart passes **references by value**. The function gets its own copy of the reference, pointing to the same object.

```dart
void addBonus(List<int> scores) {
  scores.add(100); // ✅ visible to the caller: same list
}

void replace(List<int> scores) {
  scores = [0, 0, 0]; // ❌ only changes the local parameter
}

void increment(int x) {
  x = x + 1; // ❌ ints are immutable; only the local copy changes
}

void main() {
  final scores = [70, 80];
  addBonus(scores);
  print(scores); // [70, 80, 100]

  replace(scores);
  print(scores); // [70, 80, 100] (unchanged)

  var n = 5;
  increment(n);
  print(n); // 5
}
```

**🔍 What This Code Does:**

1. **Mutating a Parameter**: `scores.add(100)` modifies the caller's list because both references point to it.
2. **Reassigning a Parameter**: `scores = [...]` only redirects the function's local copy of the reference.
3. **Immutable Values**: `int` objects can't change, so `x = x + 1` creates a new int for the local variable only.
4. **Rule of Thumb**: Functions can **change the contents** of objects you pass in, but can never make **your variable** point somewhere else.

---

## 🧊 Mutable vs Immutable Objects

Some objects can change after creation (**mutable**), others can't (**immutable**).

| Immutable ❄️ | Mutable 🔧 |
|-------------|-----------|
| `int`, `double`, `bool`, `String`, `null` | `List`, `Set`, `Map` (unless unmodifiable) |
| Records like `(1, 'a')` | Most classes with non-final fields |
| `const` objects | `StringBuffer` |

```dart
void main() {
  var greeting = 'Hello';
  final other = greeting;
  greeting += ' World'; // creates a NEW string

  print(greeting); // Hello World
  print(other);    // Hello (original string unchanged)

  final frozen = List<int>.unmodifiable([1, 2, 3]);
  try {
    frozen.add(4);
  } on UnsupportedError {
    print('Cannot modify an unmodifiable list');
  }

  const fixed = [1, 2, 3];
  try {
    fixed.add(4);
  } on UnsupportedError {
    print('Cannot modify a const list');
  }
}
```

**🔍 What This Code Does:**

1. **Strings Are Immutable**: `+=` builds a brand new String; `other` still points to `'Hello'`.
2. **`List.unmodifiable`**: Creates a list whose contents can't change; `add` throws `UnsupportedError`.
3. **`const` Collections**: Compile-time constant lists are deeply immutable.
4. **Why It Matters**: Immutable objects are safe to share; nobody can change them behind your back.

---

## ⚖️ Equality: `==` vs `identical`

Dart has two ways to compare objects:

- **`identical(a, b)`**: are they the **same object** in memory? (identity)
- **`a == b`**: are they **equal** according to the class's rules? (equality)

By default, `==` for your own classes is **identity**. Built-in types like `int`, `String` and records override it to compare **values**.

```dart
class Point {
  final int x;
  final int y;
  Point(this.x, this.y);
}

void main() {
  final p1 = Point(1, 2);
  final p2 = Point(1, 2);
  final p3 = p1;

  print(p1 == p2);          // false: different objects, default == is identity
  print(identical(p1, p3)); // true: same object

  print('dart' == 'dart');  // true: String compares characters
  print((1, 2) == (1, 2));  // true: records compare fields
  print([1, 2] == [1, 2]);  // false: Lists use identity!
}
```

**🔍 What This Code Does:**

1. **Default Equality Is Identity**: Two `Point(1, 2)` objects are different objects, so `==` returns `false`.
2. **Strings and Records**: These override `==` to compare their contents.
3. **Lists Don't**: `[1, 2] == [1, 2]` is `false` because each literal creates a separate list and `List` doesn't override `==`.
4. **Surprise Factor**: This often surprises beginners who expect lists to compare by contents.

> 💡 To compare collection contents, use `listEquals`, `setEquals` and `mapEquals` from `package:flutter/foundation.dart`, or `ListEquality` from `package:collection`.

---

## #️⃣ Overriding `==` and `hashCode`

For value-like classes (points, money, coordinates), you usually want `==` to compare **fields**. When you override `==`, you **must** also override `hashCode`.

```dart
class Point {
  final int x;
  final int y;
  const Point(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      other is Point && other.x == x && other.y == y;

  @override
  int get hashCode => Object.hash(x, y);

  @override
  String toString() => 'Point($x, $y)';
}

void main() {
  final a = Point(1, 2);
  final b = Point(1, 2);

  print(a == b);                     // true
  print(a.hashCode == b.hashCode);   // true

  final visited = {a};
  print(visited.contains(b));        // true: found via hashCode + ==

  final labels = {Point(0, 0): 'origin'};
  print(labels[const Point(0, 0)]);  // origin
}
```

**🔍 What This Code Does:**

1. **Custom `==`**: Two points are equal when both coordinates match. `other is Point` also promotes `other` so we can read its fields.
2. **`Object.hash`**: Combines several fields into one well-distributed hash code.
3. **Sets and Maps Work**: `visited.contains(b)` finds `a` because they have the same hash code **and** are `==`.
4. **`toString`**: Makes printing readable instead of `Instance of 'Point'`.
5. **`const` Constructor**: Allows compile-time constant points like `const Point(0, 0)`.

### 🚨 The hashCode contract

> If `a == b`, then `a.hashCode` **must** equal `b.hashCode`.

Break it, and hash-based collections silently stop working:

```dart
class BadPoint {
  final int x;
  final int y;
  BadPoint(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      other is BadPoint && other.x == x && other.y == y;
  // ❌ hashCode NOT overridden: still identity-based
}

void main() {
  final set = {BadPoint(1, 2)};
  print(BadPoint(1, 2) == BadPoint(1, 2)); // true
  print(set.contains(BadPoint(1, 2)));     // false (almost always) 😱
}
```

**🔍 What This Code Does:**

1. **Equal but Different Hashes**: The two points are `==`, but their default hash codes are based on identity, so they differ.
2. **Wrong Bucket**: The Set looks in the bucket for the new point's hash, which is not where the original was stored.
3. **Silent Bug**: No error is thrown; `contains` just returns the wrong answer.
4. **The Fix**: Always override `hashCode` together with `==`.

---

## 🔒 Don't Mutate Keys Inside a Set or Map

Hash collections store an object based on its hash code **at the time it was added**. If you change a field used in `hashCode` afterwards, the collection can no longer find it.

```dart
class Tag {
  String name;
  Tag(this.name);

  @override
  bool operator ==(Object other) => other is Tag && other.name == name;

  @override
  int get hashCode => name.hashCode;
}

void main() {
  final tag = Tag('dart');
  final tags = {tag};

  tag.name = 'flutter'; // ❌ mutating a key after inserting it

  print(tags.contains(tag));         // false: wrong bucket now
  print(tags.contains(Tag('dart'))); // false: name no longer matches
  print(tags.length);                // 1: it's still in there, lost!
}
```

**🔍 What This Code Does:**

1. **Hash Changes**: Changing `name` changes `hashCode`.
2. **Lost Entry**: The set still holds the object, but it's filed under the **old** hash, so lookups fail.
3. **Best Practice**: Make key fields `final` (immutable) so this can't happen.

---

## 🧠 Stack vs Heap (Conceptually)

You'll hear these two words a lot:

| | Call stack 📚 | Heap 🗄️ |
|---|---------------|----------|
| **Holds** | Function frames: parameters, local variable slots, return addresses | Objects: lists, maps, class instances, strings |
| **Lifetime** | Freed automatically when the function returns | Freed by the **garbage collector** when no longer reachable |
| **Size** | Small, limited | Large |
| **Overflow** | `StackOverflowError` (deep recursion) | `OutOfMemoryError` (too many live objects) |

```dart
class Node {
  final int value;
  Node? next; // a reference to another object on the heap
  Node(this.value);
}

Node buildChain(int length) {
  final head = Node(0);      // `head` (a reference) lives in this frame
  var current = head;        // the Node objects live on the heap
  for (var i = 1; i < length; i++) {
    current.next = Node(i);
    current = current.next!;
  }
  return head; // frame disappears, but the nodes survive on the heap
}

void main() {
  final chain = buildChain(4);
  Node? n = chain;
  while (n != null) {
    print(n.value);
    n = n.next;
  }
}
```

**🔍 What This Code Does:**

1. **Objects on the Heap**: Each `Node(...)` is allocated on the heap and outlives the function that created it.
2. **References in Frames**: `head` and `current` are slots in `buildChain`'s stack frame; they disappear when it returns.
3. **Returning a Reference**: We return `head`, so the caller can still reach the whole chain.
4. **Nullable Links**: `Node? next` is `null` at the end of the chain, which ends the `while` loop.
5. **Preview**: This is exactly a **singly linked list**, which you'll build properly later in the course.

---

## ♻️ Garbage Collection

You never free memory manually in Dart. The **garbage collector (GC)** finds objects that are no longer **reachable** from any variable and reclaims them.

```dart
class Big {
  final List<int> data = List.filled(1000000, 0);
}

void main() {
  var big = Big(); // reachable via `big`
  print(big.data.length);

  big = Big(); // the first Big is now unreachable → eligible for GC
  print(big.data.length);

  final cache = <int, Big>{};
  for (var i = 0; i < 3; i++) {
    cache[i] = Big(); // ❌ kept reachable forever by the map
  }
  cache.clear(); // ✅ now they can be collected
  print('cache size: ${cache.length}');
}
```

**🔍 What This Code Does:**

1. **Reachability**: An object stays alive as long as something can still reach it.
2. **Dropping References**: Reassigning `big` makes the first object unreachable, so the GC can free it.
3. **Accidental Retention**: Objects stored in long-lived collections (caches, static lists, listeners) stay in memory until removed. This is the most common kind of "memory leak" in Dart.
4. **`clear()`**: Removing entries lets the GC reclaim them.

---

## 📋 Copying: Shallow vs Deep

```dart
void main() {
  final original = [
    [1, 2],
    [3, 4],
  ];

  final shallow = [...original]; // new outer list, same inner lists
  final deep = [for (final row in original) [...row]]; // copies inner lists too

  original[0].add(99);

  print(original); // [[1, 2, 99], [3, 4]]
  print(shallow);  // [[1, 2, 99], [3, 4]] (inner list shared)
  print(deep);     // [[1, 2], [3, 4]] (fully independent)

  print(identical(original, shallow));       // false
  print(identical(original[0], shallow[0])); // true
}
```

**🔍 What This Code Does:**

1. **Shallow Copy**: The spread `[...original]` creates a new outer list, but its elements are the **same** inner list objects.
2. **Deep Copy**: The collection-for builds a new inner list for every row.
3. **Shared Mutation**: Adding `99` to `original[0]` shows up in `shallow` but not `deep`.
4. **Other Shallow Copies**: `List.of`, `List.from`, `toList()`, `Map.of` and `{...map}` are all shallow.

---

## 🎯 Why This Matters for Data Structures

| Concept | Where you'll use it |
|---------|---------------------|
| References | Every linked list, tree and graph node points to other nodes |
| `null` references | Marking the end of a list, missing children in a tree |
| `==` and `hashCode` | Storing your own objects in `Set`/`Map`, visited sets in graph search |
| Immutability | Safe keys, memoization caches, records as compound keys |
| Stack vs heap | Recursion depth limits; explicit stacks for deep traversals |
| Shallow vs deep copy | Snapshots of state, undo/redo, backtracking |

---

## ⚠️ Common Mistakes

### 1. Expecting lists to compare by value

```dart
void main() {
  print([1, 2, 3] == [1, 2, 3]); // false
  // ✅ compare contents yourself (or use package:collection)
  bool sameItems(List<int> a, List<int> b) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (a[i] != b[i]) return false;
    }
    return true;
  }
  print(sameItems([1, 2, 3], [1, 2, 3])); // true
}
```

**🔍 What This Code Does:**

1. **Identity Comparison**: Two separate list literals are never `==`.
2. **Element-by-Element**: Comparing length and each item gives value equality in O(n).

### 2. Using a list as a Map key

```dart
void main() {
  final scores = <List<int>, String>{};
  scores[[0, 0]] = 'start';
  print(scores[[0, 0]]); // null: a different list object!

  // ✅ Use a record instead
  final better = <(int, int), String>{};
  better[(0, 0)] = 'start';
  print(better[(0, 0)]); // start
}
```

**🔍 What This Code Does:**

1. **List Keys Use Identity**: The second `[0, 0]` is a new object, so the lookup misses.
2. **Records Use Values**: `(0, 0)` compares by fields and has a matching `hashCode`.

### 3. Sharing one mutable default

```dart
void main() {
  final row = <int>[0, 0, 0];
  final grid = List.filled(3, row); // ❌ same list 3 times
  grid[0][0] = 1;
  print(grid); // [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

  final fixed = List.generate(3, (_) => [0, 0, 0]); // ✅ 3 separate lists
  fixed[0][0] = 1;
  print(fixed); // [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
}
```

**🔍 What This Code Does:**

1. **`List.filled` Reuses the Value**: Every slot holds a reference to the **same** `row`.
2. **`List.generate` Calls the Function Each Time**: Each row is a fresh list.

---

## 🧪 Try It Yourself

1. Create a `Money` class with `amount` and `currency`, override `==` and `hashCode`, and put several in a `Set`. Check that duplicates are removed.
2. Write a function `deepCopy(Map<String, List<int>> m)` that returns a fully independent copy.
3. Build a 3×3 grid with `List.filled` and with `List.generate`, then change one cell in each. Explain the difference.

---

## 📌 Key Takeaways

- ✅ Every value in Dart is an object; variables hold **references** to them.
- ✅ Assigning or passing a variable copies the **reference**, so mutations are shared.
- ✅ `identical` checks **same object**; `==` checks **equality**, which defaults to identity for your own classes.
- ✅ `int`, `String` and records compare by **value**; `List`, `Set` and `Map` compare by **identity**.
- ✅ Override `==` **and** `hashCode` together, and keep key fields **immutable**.
- ✅ Objects live on the **heap** and are freed by the **garbage collector** when unreachable.
- ✅ Spread and `toList()` make **shallow** copies; nested data needs a **deep** copy.

**Next up:** 📏 **Module 2: Arrays & Dart Lists**, where we look inside the most important data structure of all.
