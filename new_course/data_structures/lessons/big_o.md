# Big O: Time & Space

Imagine you're delivering party invitations 🎉 in your neighborhood.

- 📬 **Plan A:** Drop all invitations in **one** community mailbox. Takes 1 minute whether you invite 5 people or 500.
- 🚶 **Plan B:** Walk to **each** house. 5 guests = 5 stops, 500 guests = 500 stops.
- 🤝 **Plan C:** For each guest, you visit **every other guest** to ask if they get along. 5 guests = 25 visits, 500 guests = 250,000 visits! 😱

All three plans "work". But as the guest list grows, they behave **very** differently.

👉 **Big O notation** is how programmers describe this:

> **Big O** describes **how the amount of work (or memory) grows** as the size of the input grows.

- Plan A is **O(1)**: constant
- Plan B is **O(n)**: linear
- Plan C is **O(n²)**: quadratic

---

## 🤔 Why Not Just Use a Stopwatch?

You *could* time your code. But timing depends on:

- 📱 Your device (a new laptop vs an old phone)
- 🔋 Battery saver, other apps running, CPU temperature
- 🎲 The specific data you happened to test with

Big O ignores all of that and answers a more useful question:

> *"If my input becomes 10x bigger, roughly how much more work will this do?"*

| Big O | Input × 10 means work × ... | Nickname |
|-------|-----------------------------|----------|
| O(1) | × 1 | Constant ⚡ |
| O(log n) | + a little | Logarithmic 🚀 |
| O(n) | × 10 | Linear 🚶 |
| O(n log n) | × a bit more than 10 | Linearithmic 🏃 |
| O(n²) | × 100 | Quadratic 🐢 |
| O(2ⁿ) | explodes | Exponential 💥 |

---

## 📐 The Rules of Big O

Big O is about the **shape** of growth, not exact counts. Three rules make it simple:

### Rule 1: Drop constants

```dart
void printTwice(List<int> items) {
  for (final x in items) {
    print(x);
  }
  for (final x in items) {
    print(x);
  }
}

void main() {
  printTwice([1, 2, 3]);
}
```

**🔍 What This Code Does:**

1. **Two Loops**: Each loop visits all `n` items, so the total work is `2n`.
2. **Constant Dropped**: `2n` grows in a straight line just like `n`, so we call it **O(n)**.
3. **Why**: Constants depend on hardware and details; the *shape* of growth doesn't.

### Rule 2: Keep only the biggest term

```dart
void pairsAndSingles(List<int> items) {
  // n² part
  for (final a in items) {
    for (final b in items) {
      print('$a,$b');
    }
  }
  // n part
  for (final x in items) {
    print(x);
  }
}

void main() {
  pairsAndSingles([1, 2]);
}
```

**🔍 What This Code Does:**

1. **Nested Loops**: Print every pair, `n × n = n²` prints.
2. **Single Loop**: Print every item, `n` prints.
3. **Total**: `n² + n`. When `n = 1,000`, that's `1,000,000 + 1,000`. The `n` part barely matters.
4. **Result**: We call this **O(n²)**.

### Rule 3: Different inputs get different letters

```dart
void printBoth(List<String> guests, List<String> dishes) {
  for (final g in guests) {
    print('Guest: $g');
  }
  for (final d in dishes) {
    print('Dish: $d');
  }
}

void main() {
  printBoth(['Ana', 'Ben'], ['Soup', 'Cake', 'Tea']);
}
```

**🔍 What This Code Does:**

1. **Two Independent Inputs**: The guests list has `g` items, the dishes list has `d` items.
2. **Total Work**: `g + d`, written **O(g + d)**.
3. **Don't Merge**: It's *not* O(n) unless both lists are the same size; and nested loops over them would be **O(g × d)**.

---

## ⚡ O(1): Constant Time

The work is the **same** no matter how big the input is.

```dart
void main() {
  final scores = List.generate(1000000, (i) => i * 2);
  final ages = {'Ada': 36, 'Linus': 54};

  // All of these are O(1):
  print(scores[500000]);        // index access
  print(scores.length);         // length is stored, not counted
  print(ages['Ada']);           // hash map lookup (average)
  scores.add(42);               // add to end (amortized)
  print(scores.last);           // last element
}
```

**🔍 What This Code Does:**

1. **Index Access**: A List stores items side by side, so `scores[500000]` jumps straight to the right spot.
2. **Stored Length**: Dart keeps the length in a field; it doesn't count items each time.
3. **Map Lookup**: Hashing finds `'Ada'` without scanning, O(1) on average.
4. **Add to End**: Usually O(1); occasionally the list grows (covered in **Amortized Analysis**).
5. **Same Speed at Any Size**: These lines run just as fast with 10 items or 10 million.

---

## 🚶 O(n): Linear Time

The work grows **in proportion** to the input. Twice the data, twice the work.

```dart
int findMax(List<int> numbers) {
  var max = numbers.first;
  for (final n in numbers) {
    if (n > max) max = n;
  }
  return max;
}

bool containsName(List<String> names, String target) {
  for (final name in names) {
    if (name == target) return true; // may exit early
  }
  return false;
}

void main() {
  print(findMax([3, 17, 8, 42, 5])); // 42
  print(containsName(['Ana', 'Ben', 'Cy'], 'Cy')); // true
}
```

**🔍 What This Code Does:**

1. **Visit Every Item**: `findMax` must look at every number; the maximum could be anywhere.
2. **Early Exit**: `containsName` can stop early, but in the **worst case** (target is last or missing) it checks all `n` names.
3. **Big O Uses the Worst Case**: Unless we say otherwise, Big O describes the worst case, so both are **O(n)**.
4. **Built-ins Too**: `List.contains`, `indexOf`, `where`, `map(...).toList()`, `reduce` and `sum`-style loops are all O(n).

---

## 🚀 O(log n): Logarithmic Time

The work grows **very slowly**: every step **cuts the problem in half**.

Think of guessing a number between 1 and 1,000:

- "Is it bigger than 500?" → Yes → now 501–1000
- "Bigger than 750?" → No → now 501–750
- ...about **10 guesses** total, because 2¹⁰ = 1024.

```dart
int binarySearch(List<int> sorted, int target) {
  var low = 0;
  var high = sorted.length - 1;
  var steps = 0;

  while (low <= high) {
    steps++;
    final mid = (low + high) ~/ 2;
    if (sorted[mid] == target) {
      print('Found in $steps steps');
      return mid;
    } else if (sorted[mid] < target) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  print('Not found after $steps steps');
  return -1;
}

void main() {
  final million = List.generate(1000000, (i) => i);
  binarySearch(million, 765432); // about 20 steps
}
```

**🔍 What This Code Does:**

1. **Sorted Input Required**: Binary search only works because the list is sorted.
2. **Halving**: Each loop compares with the middle and throws away half of the remaining range.
3. **Integer Division**: `~/` divides and rounds down, giving a valid index.
4. **Tiny Step Count**: 1,000,000 items need at most about **20** steps, because 2²⁰ ≈ 1,000,000.
5. **Growth**: Going from 1 million to 1 billion items adds only about **10** more steps.

| n | log₂ n (max steps) |
|---|--------------------|
| 8 | 3 |
| 1,024 | 10 |
| 1,000,000 | ~20 |
| 1,000,000,000 | ~30 |

---

## 🏃 O(n log n): Linearithmic Time

You do an O(log n) amount of work **for each** of the n items. This is the speed of the **best general-purpose sorting algorithms**, including Dart's `List.sort`.

```dart
void main() {
  final names = ['Zoe', 'Ali', 'Mia', 'Ben', 'Kai'];
  names.sort(); // O(n log n)
  print(names); // [Ali, Ben, Kai, Mia, Zoe]

  // Sorting is often the first step that makes other things fast:
  final nums = [9, 4, 7, 1, 8, 2];
  nums.sort();                    // O(n log n)
  print(nums.first);              // smallest, O(1)
  print(nums.last);               // largest, O(1)
}
```

**🔍 What This Code Does:**

1. **`List.sort`**: Sorts in place in O(n log n) time.
2. **Sorting Unlocks Speed**: After sorting, the smallest and largest are at the ends, and binary search becomes possible.
3. **Trade-off**: If you only need the max once, a single O(n) scan is cheaper than sorting.

---

## 🐢 O(n²): Quadratic Time

Usually caused by a **loop inside a loop** over the same data.

```dart
bool hasDuplicateSlow(List<int> items) {
  for (var i = 0; i < items.length; i++) {
    for (var j = i + 1; j < items.length; j++) {
      if (items[i] == items[j]) return true;
    }
  }
  return false;
}

bool hasDuplicateFast(List<int> items) {
  final seen = <int>{};
  for (final x in items) {
    if (!seen.add(x)) return true;
  }
  return false;
}

void main() {
  final data = [4, 8, 15, 16, 23, 42, 8];
  print(hasDuplicateSlow(data)); // true, O(n²)
  print(hasDuplicateFast(data)); // true, O(n)
}
```

**🔍 What This Code Does:**

1. **Nested Loops**: `hasDuplicateSlow` compares every pair. For n items that's about n²/2 comparisons, which is **O(n²)**.
2. **Starting at `i + 1`**: Avoids comparing an item with itself and avoids repeating pairs, but it's still O(n²) after dropping the ½.
3. **Set to the Rescue**: `hasDuplicateFast` uses a Set; each `add` is O(1) average, so the whole thing is **O(n)**.
4. **Classic Trade**: We spend extra **memory** (the Set) to save a lot of **time**.

> 💡 **Hidden O(n²):** calling an O(n) method like `list.contains` or `list.indexOf` inside a loop is also O(n²), even though you only *see* one loop!

```dart
void main() {
  final a = [1, 2, 3, 4];
  final b = [3, 4, 5, 6];

  // ❌ Looks like one loop, but contains() is O(n) → O(n²) overall
  final common = a.where((x) => b.contains(x)).toList();
  print(common); // [3, 4]

  // ✅ Convert b to a Set first → O(n) overall
  final bSet = b.toSet();
  final commonFast = a.where(bSet.contains).toList();
  print(commonFast); // [3, 4]
}
```

**🔍 What This Code Does:**

1. **Hidden Inner Loop**: `b.contains(x)` scans `b` for every `x` in `a`.
2. **`toSet()` Costs O(n) Once**: Then every `contains` is O(1) average.
3. **Tear-off**: `bSet.contains` is passed directly as the predicate, which is a neat Dart shorthand.

---

## 💥 O(2ⁿ): Exponential Time

The work **doubles** with every extra item. These algorithms become unusable very quickly.

```dart
int fib(int n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2); // two calls per call!
}

void main() {
  final sw = Stopwatch()..start();
  print(fib(30)); // 832040
  print('Took ${sw.elapsedMilliseconds} ms');
  // fib(50) would take hours with this approach
}
```

**🔍 What This Code Does:**

1. **Two Recursive Calls**: Each call to `fib` makes two more calls, creating a tree of calls that roughly doubles at each level.
2. **Repeated Work**: `fib(28)` is computed many separate times inside `fib(30)`.
3. **Exponential Growth**: Adding 1 to `n` roughly multiplies the work by about 1.6, which is still exponential.
4. **The Fix**: Remember results you've already computed (memoization), which you'll learn in **Dynamic Programming Basics**. That makes it O(n).

---

## 📊 Seeing Growth Side by Side

```dart
import 'dart:math';

void main() {
  print('n'.padRight(8) +
      'log n'.padRight(8) +
      'n log n'.padRight(10) +
      'n²'.padRight(12) +
      '2ⁿ');
  for (final n in [1, 10, 20, 30, 100]) {
    final logn = n == 1 ? 0 : (log(n) / ln2).round();
    final pow2 = n <= 30 ? pow(2, n).toInt().toString() : 'way too big';
    print('$n'.padRight(8) +
        '$logn'.padRight(8) +
        '${n * logn}'.padRight(10) +
        '${n * n}'.padRight(12) +
        pow2);
  }
}
```

**🔍 What This Code Does:**

1. **`dart:math`**: Provides `log` (natural log), `ln2` and `pow`.
2. **log₂ Formula**: `log(n) / ln2` converts the natural log into log base 2.
3. **`padRight`**: Lines up the columns so the table is readable.
4. **The Shocking Column**: At `n = 30`, `2ⁿ` is already over a **billion** while `n²` is only 900.

---

## 💾 Space Complexity

Big O also describes **memory**. Space complexity counts the **extra** memory an algorithm needs (beyond the input itself).

```dart
// O(1) extra space: a few variables, no matter how big the list is
int sum(List<int> nums) {
  var total = 0;
  for (final n in nums) {
    total += n;
  }
  return total;
}

// O(n) extra space: builds a new list as big as the input
List<int> doubled(List<int> nums) => [for (final n in nums) n * 2];

// O(n) extra space: the call stack grows one frame per element
int sumRecursive(List<int> nums, [int i = 0]) {
  if (i == nums.length) return 0;
  return nums[i] + sumRecursive(nums, i + 1);
}

void main() {
  final nums = [1, 2, 3, 4];
  print(sum(nums));           // 10
  print(doubled(nums));       // [2, 4, 6, 8]
  print(sumRecursive(nums));  // 10
}
```

**🔍 What This Code Does:**

1. **Constant Space**: `sum` only uses `total` and the loop variable, so it's **O(1)** extra space.
2. **Linear Space**: `doubled` creates a new list with `n` items, so it's **O(n)**.
3. **Hidden Stack Space**: `sumRecursive` looks like it uses no extra variables, but each recursive call adds a **stack frame**. `n` items means `n` frames, so **O(n)** space.
4. **Optional Positional Parameter**: `[int i = 0]` lets callers skip `i`.

---

## 📈 Best, Average and Worst Case

The same algorithm can do different amounts of work depending on the input.

```dart
int linearSearch(List<int> items, int target) {
  for (var i = 0; i < items.length; i++) {
    if (items[i] == target) return i;
  }
  return -1;
}

void main() {
  final items = [7, 3, 9, 1, 5];
  print(linearSearch(items, 7)); // best case: first item, 1 check
  print(linearSearch(items, 9)); // average-ish: middle
  print(linearSearch(items, 4)); // worst case: not found, 5 checks
}
```

**🔍 What This Code Does:**

1. **Best Case O(1)**: The target is the very first item.
2. **Average Case O(n)**: On average you check about half the list, `n/2`, which is still O(n).
3. **Worst Case O(n)**: The target is last or missing; you check everything.
4. **Which One Matters?** We usually quote the **worst case**, because it's a guarantee. Some structures (like hash maps) are quoted by their **average case** because the worst case is extremely rare.

| Algorithm | Best | Average | Worst |
|-----------|------|---------|-------|
| Linear search | O(1) | O(n) | O(n) |
| Binary search | O(1) | O(log n) | O(log n) |
| Hash map lookup | O(1) | O(1) | O(n) |
| Quick sort | O(n log n) | O(n log n) | O(n²) |
| Merge sort | O(n log n) | O(n log n) | O(n log n) |

---

## 🧮 How to Analyze Code: Step by Step

1. **Identify n**: What input size does the work depend on?
2. **Count loops**: A loop over n items is O(n). Nested loops multiply.
3. **Watch hidden costs**: Built-in methods have their own costs (`contains`, `indexOf`, `insert(0, x)`, `removeAt(0)`, `sort`).
4. **Look for halving**: If each step halves the problem, think O(log n).
5. **Add sequential parts, keep the biggest**: O(n) + O(n²) = O(n²).
6. **Check recursion**: How many calls, and how much work per call?

```dart
void mystery(List<int> items) {
  items.sort();                       // O(n log n)
  for (final x in items) {            // O(n) loop...
    var k = items.length;
    while (k > 1) {                   // ...with O(log n) inside
      k ~/= 2;
    }
    print(x);
  }
  print(items.contains(99));          // O(n)
}

void main() {
  mystery([5, 3, 1, 4, 2]);
}
```

**🔍 What This Code Does:**

1. **Sort**: O(n log n).
2. **Loop With Halving Inside**: n iterations × O(log n) each = O(n log n).
3. **Final contains**: O(n).
4. **Total**: O(n log n) + O(n log n) + O(n) = **O(n log n)**.

---

## 📋 Cheat Sheet: Dart Operations

| Operation | Cost |
|-----------|------|
| `list[i]`, `list[i] = x`, `list.length` | O(1) |
| `list.add(x)` | O(1) amortized |
| `list.removeLast()` | O(1) |
| `list.insert(0, x)`, `list.removeAt(0)` | O(n) |
| `list.contains(x)`, `list.indexOf(x)` | O(n) |
| `list.sort()` | O(n log n) |
| `set.add`, `set.contains`, `set.remove` | O(1) average |
| `map[key]`, `map[key] = v`, `map.containsKey` | O(1) average |
| `map.containsValue(v)` | O(n) |
| `queue.addFirst/addLast/removeFirst/removeLast` | O(1) |
| `splayTreeMap[key]`, insert, remove | O(log n) amortized |

---

## ⚠️ Common Mistakes

### 1. Thinking "one loop" always means O(n)

```dart
void main() {
  final list = [1, 2, 3, 4, 5];
  // ❌ insert(0, ...) shifts everything, so this loop is O(n²)
  final reversed = <int>[];
  for (final x in list) {
    reversed.insert(0, x);
  }
  print(reversed); // [5, 4, 3, 2, 1]

  // ✅ O(n)
  print(list.reversed.toList());
}
```

**🔍 What This Code Does:**

1. **Insert at Front Is O(n)**: Every insert moves existing items right.
2. **n Inserts**: n × O(n) = O(n²).
3. **Better**: `list.reversed.toList()` is a single O(n) pass.

### 2. Forgetting that `containsValue` is slow

```dart
void main() {
  final users = {'u1': 'ada@x.com', 'u2': 'bob@x.com'};
  // ❌ Scans every value: O(n)
  print(users.containsValue('bob@x.com'));

  // ✅ Keep a reverse index if you look up by email often
  final byEmail = {for (final e in users.entries) e.value: e.key};
  print(byEmail.containsKey('bob@x.com')); // O(1)
}
```

**🔍 What This Code Does:**

1. **`containsValue` Is a Scan**: Maps are fast by **key**, not by value.
2. **Reverse Index**: A second map from email to id makes email lookups O(1).
3. **Map Comprehension**: `{for (...) key: value}` builds a map in one expression.

### 3. Ignoring space

Creating copies with `toList()`, `where(...).toList()` or spread `[...list]` inside a loop can quietly make memory usage O(n²) too.

---

## 🧪 Try It Yourself

1. What is the Big O of a function that prints the first 10 items of any list? *(Hint: does the work grow with n?)*
2. Write a function that returns `true` if any two numbers in a list add up to a target. First do it in O(n²), then in O(n) with a Set.
3. Count how many times the `while` loop runs for `n = 1, 2, 4, 8, 16` in:

```dart
void main() {
  for (final start in [1, 2, 4, 8, 16]) {
    var n = start;
    var count = 0;
    while (n > 1) {
      n ~/= 2;
      count++;
    }
    print('n=$start -> $count iterations');
  }
}
```

**🔍 What This Code Does:**

1. **Halving Loop**: Each iteration halves `n` with `~/= 2`.
2. **Output**: 0, 1, 2, 3, 4 iterations, which is exactly log₂ of the starting value.
3. **Pattern**: That's what O(log n) looks like in practice.

---

## 📌 Key Takeaways

- ✅ **Big O** describes how work or memory **grows** with input size, not exact times.
- ✅ **Drop constants** and **keep the biggest term**: `3n² + 5n + 7` is **O(n²)**.
- ✅ Common classes from best to worst: **O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)**.
- ✅ **Halving** each step means O(log n); **nested loops** usually mean O(n²).
- ✅ Watch for **hidden costs** in built-ins like `contains`, `insert(0, x)` and `removeAt(0)`.
- ✅ **Space complexity** counts extra memory, including the **call stack** in recursion.
- ✅ Big O usually means the **worst case**; hash maps are quoted by their **average case**.

**Next up:** 🧾 **Amortized Analysis**, or how `List.add` can be O(1) even though the list sometimes has to copy everything.
