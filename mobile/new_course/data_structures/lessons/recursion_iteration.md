# Recursion & Iteration

Imagine you're standing in a long line at a concert 🎤 and want to know **what position you are in**. You can't see the front.

So you tap the person in front of you: *"What's your position?"*

They don't know either, so they tap the person in front of **them**... and so on, until the person at the very front says *"I'm number 1!"* 🙋

Then the answers travel back: *"I'm 2"*, *"I'm 3"*, ... until it reaches you.

👉 That's **recursion**:

> **Recursion** is when a function solves a problem by **calling itself** on a **smaller version** of the same problem, until it reaches a case simple enough to answer directly.

The alternative, walking to the front and counting people one by one, is **iteration**: repeating steps with a **loop**.

Both solve the same problems. Knowing **when** to use each, and how to convert between them, is essential for trees, graphs and many algorithms in this course.

---

## 🧱 The Two Parts of Every Recursive Function

1. **Base case** 🛑: the simplest input, answered **without** recursion. Without it, the function never stops.
2. **Recursive case** 🔁: break the problem into a smaller one, call yourself, and **combine** the result.

```dart
int positionInLine(int peopleAhead) {
  // 🛑 Base case: nobody ahead, I'm first
  if (peopleAhead == 0) return 1;

  // 🔁 Recursive case: ask the person ahead, then add 1
  return positionInLine(peopleAhead - 1) + 1;
}

void main() {
  print(positionInLine(0)); // 1
  print(positionInLine(4)); // 5
}
```

**🔍 What This Code Does:**

This code demonstrates **the basic structure of recursion**:

1. **Base Case**: When there's nobody ahead (`peopleAhead == 0`), the answer is simply `1`.

2. **Smaller Problem**: Each call passes `peopleAhead - 1`, moving one step closer to the base case.

3. **Combine**: Each call adds `1` to whatever the person ahead answered.

4. **Guaranteed to Stop**: Because the input shrinks every call and the base case catches 0, the recursion always ends.

5. **Same Answer as a Loop**: The position is just `peopleAhead + 1`; recursion is a different way of *thinking* about it.

---

## 📚 The Call Stack: What Really Happens

Every time a function is called, Dart pushes a **stack frame** 📦 onto the **call stack**. A frame holds that call's parameters, local variables and where to return to. When the function returns, its frame is **popped**.

```dart
int factorial(int n) {
  print('${'  ' * (5 - n)}→ factorial($n) called');
  if (n <= 1) {
    print('${'  ' * (5 - n)}← factorial($n) returns 1');
    return 1;
  }
  final result = n * factorial(n - 1);
  print('${'  ' * (5 - n)}← factorial($n) returns $result');
  return result;
}

void main() {
  print('Result: ${factorial(5)}');
}
```

**🔍 What This Code Does:**

1. **Indentation Shows Depth**: `'  ' * (5 - n)` indents deeper calls further, so you can *see* the stack grow.
2. **Winding Up**: Calls go `factorial(5) → 4 → 3 → 2 → 1`, each waiting for the next.
3. **Base Case**: `factorial(1)` returns `1` without calling anything.
4. **Unwinding**: Results flow back: `2 × 1 = 2`, `3 × 2 = 6`, `4 × 6 = 24`, `5 × 24 = 120`.
5. **String Repetition**: In Dart, `'ab' * 3` gives `'ababab'`.

**Output:**

```text
→ factorial(5) called
  → factorial(4) called
    → factorial(3) called
      → factorial(2) called
        → factorial(1) called
        ← factorial(1) returns 1
      ← factorial(2) returns 2
    ← factorial(3) returns 6
  ← factorial(4) returns 24
← factorial(5) returns 120
Result: 120
```

> 💡 At the deepest point, **5 frames** are on the stack at once. That's why recursion uses **O(depth)** extra memory.

---

## 💥 Stack Overflow: When Recursion Goes Too Deep

The call stack has a **limited size**. Forget the base case, or recurse too deeply, and Dart throws a `StackOverflowError`.

```dart
int countDown(int n) {
  // ❌ No base case! This never stops.
  return countDown(n - 1);
}

int sumTo(int n) => n == 0 ? 0 : n + sumTo(n - 1);

void main() {
  try {
    countDown(10);
  } on StackOverflowError {
    print('💥 Stack overflow: missing base case');
  }

  print(sumTo(1000)); // fine: 500500

  try {
    print(sumTo(10000000)); // too deep for the stack
  } on StackOverflowError {
    print('💥 Stack overflow: recursion too deep');
  }
}
```

**🔍 What This Code Does:**

1. **Missing Base Case**: `countDown` calls itself forever until the stack runs out of space.
2. **Catching It**: `on StackOverflowError` catches the error so the program can continue (for demonstration only; don't rely on this in real code).
3. **Reasonable Depth**: `sumTo(1000)` is only 1,000 frames deep, which is fine.
4. **Excessive Depth**: `sumTo(10000000)` needs 10 million frames, which overflows.
5. **Lesson**: Deep recursion on big inputs is risky. Use a loop, or an explicit stack, when depth could be large.

> ⚠️ Dart does **not** perform tail-call optimization, so even "tail recursive" functions still use one stack frame per call.

---

## 🔁 Iteration: The Loop Version

Most simple recursive functions can be written as loops that use **O(1)** extra space.

```dart
int factorialRecursive(int n) => n <= 1 ? 1 : n * factorialRecursive(n - 1);

int factorialIterative(int n) {
  var result = 1;
  for (var i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

int sumToIterative(int n) {
  var total = 0;
  for (var i = 1; i <= n; i++) {
    total += i;
  }
  return total;
}

void main() {
  print(factorialRecursive(10)); // 3628800
  print(factorialIterative(10)); // 3628800
  print(sumToIterative(10000000)); // 50000005000000, no overflow
}
```

**🔍 What This Code Does:**

1. **Same Results**: Both factorials print `3628800`.
2. **Accumulator Variable**: The loop keeps a running `result` instead of waiting on a chain of calls.
3. **Constant Space**: The iterative versions use O(1) extra memory, with no stack frames piling up.
4. **Handles Huge n**: `sumToIterative(10000000)` works where the recursive version overflowed.

| | Recursion | Iteration |
|---|-----------|-----------|
| **Readability** | Natural for self-similar problems (trees, divide & conquer) | Natural for "do this n times" |
| **Extra space** | O(depth) for the call stack | Often O(1) |
| **Risk** | Stack overflow on deep inputs | Infinite loops if the condition is wrong |
| **Speed** | Function call overhead | Usually slightly faster |

---

## 🌳 Where Recursion Shines: Self-Similar Structures

Recursion is the natural fit when a problem contains **smaller copies of itself**. A folder contains files and **more folders**. A tree node has children that are **trees**.

```dart
class FileNode {
  final String name;
  final int size; // bytes (0 for folders)
  final List<FileNode> children;

  FileNode(this.name, {this.size = 0, this.children = const []});
}

int totalSize(FileNode node) {
  var total = node.size;
  for (final child in node.children) {
    total += totalSize(child); // 🔁 same problem, smaller piece
  }
  return total;
}

void printTree(FileNode node, [int depth = 0]) {
  final icon = node.children.isEmpty && node.size > 0 ? '📄' : '📁';
  print('${'  ' * depth}$icon ${node.name}');
  for (final child in node.children) {
    printTree(child, depth + 1);
  }
}

void main() {
  final root = FileNode('project', children: [
    FileNode('README.md', size: 120),
    FileNode('lib', children: [
      FileNode('main.dart', size: 900),
      FileNode('widgets', children: [
        FileNode('button.dart', size: 400),
      ]),
    ]),
  ]);

  printTree(root);
  print('Total size: ${totalSize(root)} bytes'); // 1420
}
```

**🔍 What This Code Does:**

1. **Recursive Data**: `FileNode` contains a list of `FileNode`s, a structure defined in terms of itself.
2. **Implicit Base Case**: A file has no children, so the `for` loop doesn't run and the function just returns `node.size`.
3. **Recursive Sum**: A folder's size is its own size plus the total of each child.
4. **Depth for Indentation**: `printTree` passes `depth + 1` down so nested items are indented further.
5. **Clean Code**: A loop-only version would need you to manage a stack of folders yourself.

---

## 🔀 Multiple Recursive Calls (Tree Recursion)

When a function calls itself **more than once**, the calls form a **tree**, and the work can explode.

```dart
var calls = 0;

int fib(int n) {
  calls++;
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

void main() {
  for (final n in [10, 20, 25]) {
    calls = 0;
    final result = fib(n);
    print('fib($n) = $result using $calls calls');
  }
}
```

**🔍 What This Code Does:**

1. **Two Calls per Call**: Every `fib(n)` calls both `fib(n - 1)` and `fib(n - 2)`.
2. **Repeated Subproblems**: `fib(3)` gets computed again and again in different branches.
3. **Exploding Call Count**: `fib(25)` makes **242,785** calls just to return 75,025.
4. **Global Counter**: The top-level `calls` variable lets us count every invocation.

### ✅ Fix 1: Memoization (still recursive)

```dart
final memo = <int, int>{};

int fibMemo(int n) {
  if (n <= 1) return n;
  final cached = memo[n];
  if (cached != null) return cached;
  final result = fibMemo(n - 1) + fibMemo(n - 2);
  memo[n] = result;
  return result;
}

void main() {
  print(fibMemo(50)); // 12586269025, instantly
  print(fibMemo(90)); // 2880067194370816120
}
```

**🔍 What This Code Does:**

1. **Cache Results**: The Map remembers each `fib(n)` the first time it's computed.
2. **Skip Repeats**: Later calls return the cached value instantly.
3. **O(n) Time**: Each `n` is computed once, so the call tree collapses into a line.
4. **O(n) Space**: The memo map and the recursion depth both grow with n.

### ✅ Fix 2: Iteration (bottom-up)

```dart
int fibIterative(int n) {
  if (n <= 1) return n;
  var prev = 0, curr = 1;
  for (var i = 2; i <= n; i++) {
    final next = prev + curr;
    prev = curr;
    curr = next;
  }
  return curr;
}

void main() {
  print(fibIterative(10)); // 55
  print(fibIterative(90)); // 2880067194370816120
}
```

**🔍 What This Code Does:**

1. **Build Up From the Bottom**: Start from `fib(0)` and `fib(1)` and walk forward.
2. **Two Variables**: Only the last two values are needed, so space is **O(1)**.
3. **O(n) Time**: One pass of the loop.
4. **No Stack Risk**: Works for any `n` that fits in an `int`.

---

## 🧭 Converting Recursion to Iteration With an Explicit Stack

Any recursion can be made iterative by managing your **own** stack (a `List` used with `add` and `removeLast`). This is the trick behind iterative tree traversals and DFS.

```dart
class FileNode {
  final String name;
  final int size;
  final List<FileNode> children;
  FileNode(this.name, {this.size = 0, this.children = const []});
}

int totalSizeIterative(FileNode root) {
  var total = 0;
  final stack = <FileNode>[root]; // our own call stack

  while (stack.isNotEmpty) {
    final node = stack.removeLast(); // "pop"
    total += node.size;
    stack.addAll(node.children); // "push" the subproblems
  }
  return total;
}

void main() {
  final root = FileNode('project', children: [
    FileNode('a.txt', size: 10),
    FileNode('src', children: [
      FileNode('b.txt', size: 20),
      FileNode('c.txt', size: 30),
    ]),
  ]);
  print(totalSizeIterative(root)); // 60
}
```

**🔍 What This Code Does:**

1. **Explicit Stack**: A `List<FileNode>` replaces the call stack.
2. **Pop and Process**: `removeLast()` takes the most recently added node, the same order recursion would explore.
3. **Push Children**: `addAll(node.children)` schedules the subfolders for later.
4. **No Overflow**: The list lives on the **heap**, which is far larger than the call stack.
5. **Same Answer**: `10 + 20 + 30 = 60`, identical to the recursive version.

---

## 🧩 Classic Recursive Problems

### Reverse a string

```dart
String reverse(String s) {
  if (s.length <= 1) return s;
  return reverse(s.substring(1)) + s[0];
}

void main() {
  print(reverse('dart')); // trad
}
```

**🔍 What This Code Does:**

1. **Base Case**: Empty or one-character strings are already reversed.
2. **Recursive Step**: Reverse everything after the first character, then put the first character at the end.
3. **Cost**: `substring` and `+` copy characters each call, making this **O(n²)** time. Fine for learning, but `s.split('').reversed.join()` is O(n).

### Power (fast exponentiation)

```dart
int power(int base, int exp) {
  if (exp == 0) return 1;
  final half = power(base, exp ~/ 2);
  return exp.isEven ? half * half : half * half * base;
}

void main() {
  print(power(2, 10)); // 1024
  print(power(3, 5));  // 243
}
```

**🔍 What This Code Does:**

1. **Halving the Exponent**: `x¹⁰ = (x⁵)²`, so we solve half the problem and square it.
2. **Odd Exponents**: `x⁵ = (x²)² × x`, so multiply by `base` once more.
3. **O(log n)**: The exponent halves each call, so only about log₂(exp) calls are made.
4. **Reuse**: `half` is computed **once** and used twice; calling `power` twice would make it O(n).

### Sum of digits

```dart
int digitSum(int n) => n < 10 ? n : (n % 10) + digitSum(n ~/ 10);

void main() {
  print(digitSum(9875)); // 29
}
```

**🔍 What This Code Does:**

1. **Last Digit**: `n % 10` extracts the rightmost digit.
2. **Remove It**: `n ~/ 10` drops the rightmost digit.
3. **Base Case**: A single digit is its own sum.

### Binary search (recursive)

```dart
int search(List<int> a, int target, [int lo = 0, int? hi]) {
  hi ??= a.length - 1;
  if (lo > hi) return -1;
  final mid = (lo + hi) ~/ 2;
  if (a[mid] == target) return mid;
  return a[mid] < target
      ? search(a, target, mid + 1, hi)
      : search(a, target, lo, mid - 1);
}

void main() {
  print(search([2, 5, 8, 12, 16, 23, 38], 23)); // 5
}
```

**🔍 What This Code Does:**

1. **Optional Bounds**: `lo` defaults to 0; `hi` is nullable and filled in with `??=` on the first call.
2. **Base Case**: An empty range (`lo > hi`) means not found.
3. **One Recursive Call**: Only one half is searched, so depth is O(log n).

---

## 🔙 Backtracking: Recursion That Explores Choices

Backtracking tries a choice, recurses, then **undoes** the choice and tries the next. It's how you generate permutations, solve Sudoku or find paths in a maze.

```dart
void permutations(List<String> items, List<String> current, Set<int> used) {
  if (current.length == items.length) {
    print(current.join());
    return;
  }
  for (var i = 0; i < items.length; i++) {
    if (used.contains(i)) continue;
    used.add(i);
    current.add(items[i]);      // choose
    permutations(items, current, used); // explore
    current.removeLast();       // un-choose
    used.remove(i);
  }
}

void main() {
  permutations(['A', 'B', 'C'], [], {});
}
```

**🔍 What This Code Does:**

1. **Choose**: Add an unused item to `current` and mark its index as used.
2. **Explore**: Recurse to fill the remaining positions.
3. **Un-choose**: Remove the item and unmark it, so the next loop iteration starts clean.
4. **Base Case**: When `current` is full, print one permutation.
5. **Output**: `ABC, ACB, BAC, BCA, CAB, CBA`, all 3! = 6 orderings. Generating all permutations is O(n × n!).

---

## 🧮 Analyzing Recursive Functions

Ask two questions:

1. **How many calls are made in total?**
2. **How much work does each call do (excluding the recursive calls)?**

| Function | Calls | Work per call | Time | Space (stack depth) |
|----------|-------|---------------|------|---------------------|
| `factorial(n)` | n | O(1) | O(n) | O(n) |
| `power(b, n)` (halving) | log n | O(1) | O(log n) | O(log n) |
| Recursive binary search | log n | O(1) | O(log n) | O(log n) |
| Naive `fib(n)` | ~2ⁿ | O(1) | O(2ⁿ) | O(n) |
| `fibMemo(n)` | ~2n | O(1) | O(n) | O(n) |
| `totalSize(tree)` | one per node | O(1) + loop | O(nodes) | O(height) |

> 💡 Space is the **maximum depth**, not the total number of calls, because frames are popped as calls return.

---

## ⚠️ Common Mistakes

### 1. A base case that's never reached

```dart
int halve(int n) {
  if (n == 0) return 0;
  return halve(n - 2); // ❌ odd numbers skip 0 forever
}

int halveFixed(int n) {
  if (n <= 0) return 0; // ✅ catches both 0 and negatives
  return halveFixed(n - 2);
}

void main() {
  print(halveFixed(7)); // 0
}
```

**🔍 What This Code Does:**

1. **Skipping the Base Case**: Starting at 7, `n` goes 7, 5, 3, 1, -1, -3... and never equals 0.
2. **Use a Range Check**: `n <= 0` catches every way the input can finish.

### 2. Forgetting to return the recursive result

```dart
int sumList(List<int> xs, int i) {
  if (i == xs.length) return 0;
  return xs[i] + sumList(xs, i + 1); // ✅ the result is returned and combined
}

void main() {
  print(sumList([1, 2, 3], 0)); // 6
}
```

**🔍 What This Code Does:**

1. **Combine and Return**: Each call adds its own item to the result of the smaller problem.
2. **Common Bug**: Calling `sumList(xs, i + 1);` on its own line throws the answer away.

### 3. Recomputing the same subproblem

Calling `power(base, exp ~/ 2)` **twice** instead of storing `half` turns O(log n) into O(n). Always check whether you're repeating identical calls.

---

## 🧪 Try It Yourself

1. Write `countDigits(int n)` recursively, then iteratively.
2. Write `isPalindrome(String s)` recursively: compare the first and last characters, then recurse on the middle.
3. Write `flatten(List<Object> nested)` that turns `[1, [2, [3, 4]], 5]` into `[1, 2, 3, 4, 5]`.
4. Convert `printTree` from the folder example into an iterative version using an explicit stack of `(FileNode, int depth)` records.

```dart
List<int> flatten(List<Object> nested) {
  final out = <int>[];
  for (final item in nested) {
    if (item is int) {
      out.add(item);
    } else if (item is List<Object>) {
      out.addAll(flatten(item));
    }
  }
  return out;
}

void main() {
  print(flatten([1, [2, [3, 4]], 5])); // [1, 2, 3, 4, 5]
}
```

**🔍 What This Code Does:**

1. **Type Checks**: `is int` and `is List<Object>` decide whether to keep the item or recurse into it.
2. **Type Promotion**: After `item is int`, Dart lets us use `item` as an `int` without casting.
3. **Recursive Case**: Nested lists are flattened and their items appended with `addAll`.

---

## 📌 Key Takeaways

- ✅ Every recursive function needs a **base case** and a **recursive case** that moves toward it.
- ✅ Each call adds a **stack frame**; recursion uses **O(depth)** extra space.
- ✅ Too much depth causes a **`StackOverflowError`**; Dart has no tail-call optimization.
- ✅ Recursion shines for **self-similar** data: trees, folders, divide and conquer, backtracking.
- ✅ Iteration often uses **O(1)** space and can't overflow the stack.
- ✅ Any recursion can be converted to iteration with an **explicit stack**.
- ✅ Multiple recursive calls can explode exponentially; **memoization** or **bottom-up loops** fix repeated work.

**Next up:** 🧠 **How Dart Stores Data**: values, references, equality and hash codes.
