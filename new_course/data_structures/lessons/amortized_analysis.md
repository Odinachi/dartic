# Amortized Analysis

Imagine you buy a **monthly train pass** 🚆 for $60.

- On day 1, you pay **$60**. Ouch! 💸
- On days 2–30, you pay **$0**.

Is the train "expensive"? On day 1 it feels like it. But spread over the month, each ride costs about **$2**. 🎟️

👉 That's **amortized analysis**:

> **Amortized cost** is the **average cost per operation** over a long sequence of operations, even if a few individual operations are expensive.

It's how we can honestly say Dart's `List.add` is **O(1)**, even though every now and then it has to copy the entire list.

---

## 🧠 Average Case vs Amortized: Not the Same Thing!

These sound alike, but they're different promises:

| Term | What it means | Depends on luck? |
|------|---------------|------------------|
| **Average case** | Expected cost for a *random* input | ✅ Yes, a bad input can be slow |
| **Amortized** | Guaranteed average over **any** sequence of operations | ❌ No, it's a guarantee |
| **Worst case** | Cost of the single most expensive operation | ❌ No |

So "`List.add` is **O(1) amortized**" means:

> Do `n` adds in a row and the **total** work is O(n), **guaranteed**, no matter what values you add.

---

## 📦 How a Growable List Works Inside

A Dart `List` stores its elements in a contiguous block of memory (a fixed-size buffer). It keeps two numbers:

- **length**: how many elements you've added
- **capacity**: how many elements fit in the current buffer

When `length == capacity` and you `add` one more:

1. Allocate a **bigger** buffer (typically about **double** the size)
2. **Copy** every existing element into it (O(n))
3. Put the new element at the end

Let's simulate it ourselves so we can **see** the costs.

```dart
class GrowableIntList {
  List<int?> _buffer = List.filled(1, null);
  int _length = 0;
  int copies = 0; // count expensive work

  int get length => _length;
  int get capacity => _buffer.length;

  void add(int value) {
    if (_length == _buffer.length) {
      _grow();
    }
    _buffer[_length] = value;
    _length++;
  }

  void _grow() {
    final bigger = List<int?>.filled(_buffer.length * 2, null);
    for (var i = 0; i < _length; i++) {
      bigger[i] = _buffer[i];
      copies++;
    }
    _buffer = bigger;
  }

  int operator [](int index) {
    if (index < 0 || index >= _length) {
      throw RangeError.index(index, this, 'index', null, _length);
    }
    return _buffer[index]!;
  }
}

void main() {
  final list = GrowableIntList();
  for (var i = 0; i < 16; i++) {
    final before = list.capacity;
    list.add(i);
    if (list.capacity != before) {
      print('add($i): grew $before -> ${list.capacity}');
    }
  }
  print('length=${list.length}, capacity=${list.capacity}');
  print('total copies: ${list.copies}');
}
```

**🔍 What This Code Does:**

This code demonstrates **a dynamic array that doubles its capacity when full**:

1. **Fixed Buffer**: `List.filled(1, null)` creates a fixed-length buffer, like a raw array.

2. **Two Counters**: `_length` is how many items are used; `capacity` is the buffer size.

3. **Grow on Demand**: When the buffer is full, `_grow()` allocates a buffer **twice** as large and copies everything over.

4. **Counting the Cost**: `copies` tracks how many element copies happen in total.

5. **Operator Overloading**: `operator []` lets us read items with `list[3]` just like a real List, with a bounds check.

**Output:**

```text
add(1): grew 1 -> 2
add(2): grew 2 -> 4
add(4): grew 4 -> 8
add(8): grew 8 -> 16
length=16, capacity=16
total copies: 15
```

16 adds caused only **15 copies** in total. That's less than one copy per add! 🎉

---

## 🧮 Why Doubling Gives O(1) Amortized

When the list grows from capacity 1 → 2 → 4 → 8 → ... → n, the copies are:

```text
1 + 2 + 4 + 8 + ... + n/2  =  n - 1
```

This is a **geometric series**: each term is double the previous one, and the sum of all the earlier terms is always **less than the last one**.

So for `n` adds:

- **n** writes (one per add)
- fewer than **n** copies (from all the growing)
- **Total: less than 2n** → O(n) for all adds → **O(1) per add** on average

```dart
void main() {
  for (final n in [8, 64, 1024, 1000000]) {
    var capacity = 1;
    var copies = 0;
    for (var length = 0; length < n; length++) {
      if (length == capacity) {
        copies += length; // copy everything
        capacity *= 2;
      }
    }
    final perAdd = (n + copies) / n;
    print('n=$n  copies=$copies  work per add=${perAdd.toStringAsFixed(2)}');
  }
}
```

**🔍 What This Code Does:**

1. **Simulation Only**: Instead of real memory, we just count how many copies would happen.
2. **Doubling Rule**: Each time `length` reaches `capacity`, we "copy" `length` items and double the capacity.
3. **Work per Add**: `(writes + copies) / n` stays **below 2** no matter how big `n` gets.
4. **The Proof in Numbers**: Even at 1,000,000 adds, the cost per add is a small constant.

---

## ❌ What If We Grew by a Constant Instead?

What if the list grew by **+10** slots each time instead of doubling?

```dart
void main() {
  for (final n in [100, 1000, 10000, 100000]) {
    var capacity = 10;
    var copies = 0;
    for (var length = 0; length < n; length++) {
      if (length == capacity) {
        copies += length;
        capacity += 10; // grow by a constant ❌
      }
    }
    print('n=$n  copies=$copies  per add=${(copies / n).toStringAsFixed(1)}');
  }
}
```

**🔍 What This Code Does:**

1. **Constant Growth**: The buffer only gets 10 slots bigger each time it fills up.
2. **Frequent Copies**: It has to grow every 10 adds, and each grow copies everything so far.
3. **Total Copies**: About `10 + 20 + 30 + ... + n`, which is roughly `n² / 20`. That's **O(n²)** total.
4. **Per Add**: The "copies per add" number keeps **climbing** as n grows, so it's **O(n)** amortized, not O(1).

> 💡 **The key insight:** growing by a **multiplier** (×1.5, ×2) gives O(1) amortized. Growing by a **fixed amount** (+10, +100) gives O(n) amortized.

| Growth strategy | Total cost of n adds | Amortized per add |
|-----------------|----------------------|-------------------|
| ×2 (doubling) | O(n) | **O(1)** ✅ |
| ×1.5 | O(n) | **O(1)** ✅ |
| +10 | O(n²) | O(n) ❌ |
| +1 (grow every time) | O(n²) | O(n) ❌ |

---

## 🏦 The Banker's Method (Saving Coins)

Here's a friendly way to *prove* amortized costs: pretend each operation **pays coins** 🪙.

- Each `add` pays **3 coins**:
  - 🪙 1 coin to write the new item
  - 🪙 1 coin saved on the new item to pay for **its own** future copy
  - 🪙 1 coin saved to pay for copying an **older** item (one that already spent its coin)

When the list doubles from `k` to `2k`, the `k/2` items added since the last grow have saved `2 × k/2 = k` coins, exactly enough to copy all `k` items. The bank account never goes negative, so **every add costs at most 3 coins = O(1)**.

```dart
void main() {
  var capacity = 1;
  var length = 0;
  var bank = 0;

  for (var i = 0; i < 20; i++) {
    bank += 3; // each add pays 3 coins
    if (length == capacity) {
      bank -= length; // pay for copying
      capacity *= 2;
    }
    bank -= 1; // pay for writing the new item
    length++;
    if (bank < 0) print('💥 Went broke at add #$i');
  }
  print('Final bank balance: $bank coins (never negative ✅)');
}
```

**🔍 What This Code Does:**

1. **Fixed Payment**: Every add deposits exactly 3 coins.
2. **Expensive Moments**: Growing withdraws `length` coins to pay for copies.
3. **Write Cost**: Every add spends 1 coin to store its item.
4. **Never Broke**: The balance never goes below zero, which proves 3 coins (a constant) per add is always enough.

---

## 🥞 Example 2: A Stack With "Pop All"

Amortized analysis isn't just about lists. Consider a stack with a `popAll()` that removes everything.

```dart
class Stack<T> {
  final _items = <T>[];

  void push(T item) => _items.add(item); // O(1) amortized

  T pop() => _items.removeLast(); // O(1)

  int popAll() {
    var count = 0;
    while (_items.isNotEmpty) {
      _items.removeLast();
      count++;
    }
    return count; // O(k) where k = current size
  }
}

void main() {
  final s = Stack<int>();
  var work = 0;

  for (var round = 0; round < 5; round++) {
    for (var i = 0; i < 4; i++) {
      s.push(i);
      work++;
    }
    work += s.popAll();
  }

  print('Operations: 25, total work: $work');
}
```

**🔍 What This Code Does:**

1. **Push Is Cheap**: Each `push` does 1 unit of work.
2. **popAll Looks Expensive**: It removes `k` items, which is O(k) for that one call.
3. **But**: Every item can only be popped **once** after being pushed **once**.
4. **Total Work**: Over 20 pushes and 5 popAlls, total work is at most `2 × 20 = 40`, so each operation is **O(1) amortized**.
5. **Generic Class**: `Stack<T>` works for any type thanks to Dart generics.

---

## 🔢 Example 3: The Binary Counter

Incrementing a binary counter sometimes flips **many** bits (`0111 → 1000` flips 4), but usually only one.

```dart
void main() {
  final bits = List.filled(8, 0); // bits[0] is the lowest bit
  var totalFlips = 0;

  for (var n = 1; n <= 16; n++) {
    var i = 0;
    var flips = 0;
    // carry: turn trailing 1s into 0s
    while (i < bits.length && bits[i] == 1) {
      bits[i] = 0;
      i++;
      flips++;
    }
    if (i < bits.length) {
      bits[i] = 1;
      flips++;
    }
    totalFlips += flips;
    final binary = bits.reversed.join();
    print('${'$n'.padLeft(2)}: $binary  flips=$flips');
  }
  print('Total flips for 16 increments: $totalFlips');
}
```

**🔍 What This Code Does:**

1. **Carry Loop**: Every trailing `1` becomes `0`, then the next `0` becomes `1`.
2. **Uneven Costs**: Incrementing to 8 (`00000111 → 00001000`) flips 4 bits; incrementing to 9 flips just 1.
3. **Bit i Flips Every 2ⁱ Increments**: Bit 0 flips every time, bit 1 every 2nd time, bit 2 every 4th...
4. **Total**: `n + n/2 + n/4 + ... < 2n`, so **O(1) amortized** per increment. The output shows 31 flips for 16 increments.
5. **`bits.reversed.join()`**: Prints the highest bit first, the way we normally read binary.

---

## 🎯 Dart Collections and Their Amortized Costs

| Operation | Worst single call | Amortized |
|-----------|-------------------|-----------|
| `List.add` | O(n) (when growing) | **O(1)** |
| `List.removeLast` | O(1) | O(1) |
| `Map[key] = value` / `Set.add` | O(n) (when resizing) | **O(1)** (average) |
| `Queue.addLast` / `addFirst` (`ListQueue`) | O(n) (when growing) | **O(1)** |
| `SplayTreeMap` insert / lookup | O(n) | **O(log n)** |

> 💡 `SplayTreeMap` is a classic amortized structure: a single lookup can be slow, but any sequence of `m` operations costs O(m log n) in total.

---

## ⏱️ When Amortized Isn't Good Enough

Amortized O(1) is great for **throughput** (total work). But a **single** slow operation still happens. That matters for:

- 🎮 **Games** running at 60 frames per second: one big copy could drop a frame
- 🎵 **Audio** processing: a pause causes a click
- 🚗 **Real-time systems**: a deadline must never be missed

The fix is often to **reserve capacity up front**, so growth never happens during the critical part.

```dart
void main() {
  const particleCount = 10000;

  // ❌ Grows (and copies) several times while adding
  final growing = <double>[];
  for (var i = 0; i < particleCount; i++) {
    growing.add(i * 0.1);
  }

  // ✅ Fixed-length list allocated once, no growth at all
  final fixed = List<double>.filled(particleCount, 0);
  for (var i = 0; i < particleCount; i++) {
    fixed[i] = i * 0.1;
  }

  // ✅ List.generate also allocates the right size once
  final generated = List<double>.generate(particleCount, (i) => i * 0.1);

  print('${growing.length} ${fixed.length} ${generated.length}');
}
```

**🔍 What This Code Does:**

1. **Growing List**: Starts small and copies itself every time it fills up.
2. **`List.filled`**: Creates a **fixed-length** list of the exact size; there are no copies at all.
3. **`List.generate`**: Builds a list of the known size by calling a function for each index.
4. **Same Result**: All three end with 10,000 items, but the last two never pause to grow.
5. **Fixed-Length Caveat**: `List.filled(n, x)` is fixed-length by default; calling `add` on it throws. Pass `growable: true` if you need to add more later.

---

## ⚠️ Common Mistakes

### 1. Confusing amortized with average case

```dart
void main() {
  // Amortized: guaranteed over ANY sequence of adds
  final list = <int>[];
  for (var i = 0; i < 100; i++) {
    list.add(i); // total work O(100), always
  }

  // Average case: depends on the data
  // Hash lookups are O(1) on average, but a terrible hash
  // function could make every lookup O(n).
  print(list.length);
}
```

**🔍 What This Code Does:**

1. **List.add**: Its O(1) amortized bound holds for every possible sequence.
2. **Hash Lookups**: Their O(1) is an **average** that depends on a good hash function.
3. **Different Guarantees**: Amortized never depends on luck; average case does.

### 2. Calling `add` on a fixed-length list

```dart
void main() {
  final fixed = List<int>.filled(3, 0);
  try {
    fixed.add(4); // ❌ Unsupported operation
  } on UnsupportedError catch (e) {
    print('Error: ${e.message}');
  }

  final growable = List<int>.filled(3, 0, growable: true);
  growable.add(4); // ✅
  print(growable); // [0, 0, 0, 4]
}
```

**🔍 What This Code Does:**

1. **Fixed by Default**: `List.filled` without `growable: true` can't change length.
2. **UnsupportedError**: Dart throws this when you try to `add` to a fixed-length list.
3. **The Fix**: Pass `growable: true` if you need both preallocation and growth.

### 3. Thinking one slow call means the structure is slow

A single `add` that triggers a copy of 1,000,000 elements is slow, but it happened after ~500,000 cheap adds and won't happen again until ~1,000,000 more. Judge the **sequence**, not the outlier.

---

## 🧪 Try It Yourself

1. Change `GrowableIntList` to grow by **×1.5** (use `(capacity * 3) ~/ 2 + 1`). Count the copies for 1,000 adds. Is it still less than a small constant times n?

2. Add a `removeLast()` that **halves** the capacity when the list is only **¼** full. Why ¼ and not ½? *(Hint: imagine adding and removing one item repeatedly right at the boundary.)*

3. Modify the binary counter to count to 1,000 and print `totalFlips / 1000`. What number does it approach?

```dart
void main() {
  // Starter for exercise 3
  final bits = List.filled(16, 0);
  var total = 0;
  for (var n = 1; n <= 1000; n++) {
    var i = 0;
    while (bits[i] == 1) {
      bits[i] = 0;
      i++;
      total++;
    }
    bits[i] = 1;
    total++;
  }
  print('Average flips per increment: ${total / 1000}');
}
```

**🔍 What This Code Does:**

1. **16 Bits**: Enough room to count past 1,000 without overflowing.
2. **Counting Every Flip**: Both the carry flips and the final `0 → 1` flip are counted.
3. **Result**: The average approaches **2**, confirming O(1) amortized.

---

## 📌 Key Takeaways

- ✅ **Amortized cost** = total cost of a sequence ÷ number of operations, **guaranteed** for any sequence.
- ✅ `List.add` is **O(1) amortized** because the list **doubles** when full, and the total copying is less than `n`.
- ✅ Growing by a **multiplier** gives O(1) amortized; growing by a **constant** gives O(n) amortized.
- ✅ The **banker's method** proves it by "saving coins" on cheap operations to pay for expensive ones.
- ✅ **Average case** depends on the input; **amortized** does not.
- ✅ For real-time code, **preallocate** with `List.filled` or `List.generate` to avoid growth pauses.

**Next up:** 🔁 **Recursion & Iteration**, where we look at the call stack and how functions that call themselves really work.
