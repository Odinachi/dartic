# Stacks

Imagine a **stack of pancakes** 🥞 on your plate.

- You put each new pancake **on top**.
- You eat from the **top** too (unless you want a syrupy mess).
- The **last** pancake added is the **first** one eaten.

👉 That's a **stack**:

> A **stack** is a collection where you can only add (**push**) and remove (**pop**) at **one end**, the **top**. It follows **LIFO**: **L**ast **I**n, **F**irst **O**ut.

Stacks are everywhere: the **undo** button ↩️, the **back** button 🔙, the function **call stack** 📚, matching **brackets** `{[()]}` and evaluating **expressions** `3 + 4 * 2`.

---

## 🧰 Stack Operations

| Operation | What it does | Cost |
|-----------|--------------|------|
| `push(x)` | Put `x` on top | O(1) amortized |
| `pop()` | Remove and return the top | O(1) |
| `peek()` / `top` | Look at the top without removing | O(1) |
| `isEmpty` | Is the stack empty? | O(1) |
| `length` | How many items | O(1) |

Notice what's **missing**: there's no "get the 5th item" or "search". A stack deliberately restricts access to make its purpose clear and its operations fast.

---

## 🧱 A Dart List Is Already a Stack

The **end** of a `List` is cheap to add and remove from, so it makes a perfect stack.

```dart
void main() {
  final stack = <String>[];

  stack.add('🥞 1');  // push
  stack.add('🥞 2');  // push
  stack.add('🥞 3');  // push
  print(stack);       // [🥞 1, 🥞 2, 🥞 3]  (top is on the right)

  print(stack.last);  // 🥞 3 (peek)

  print(stack.removeLast()); // 🥞 3 (pop)
  print(stack.removeLast()); // 🥞 2 (pop)
  print(stack);              // [🥞 1]
  print(stack.isEmpty);      // false
}
```

**🔍 What This Code Does:**

1. **Push = `add`**: Appends to the end in O(1) amortized.
2. **Peek = `last`**: Reads the end in O(1).
3. **Pop = `removeLast`**: Removes from the end in O(1); nothing shifts.
4. **LIFO in Action**: Items come out in the reverse order they went in.

> ⚠️ Don't use the **front** of a List as the top (`insert(0, x)`, `removeAt(0)`): those are O(n).

---

## 🏗️ A Proper `Stack<T>` Class

Wrapping a List hides operations that would break the "top only" rule, and gives clear names and error messages.

```dart
class Stack<T> {
  final List<T> _items = [];

  void push(T item) => _items.add(item);

  T pop() {
    if (_items.isEmpty) throw StateError('Cannot pop from an empty stack');
    return _items.removeLast();
  }

  T peek() {
    if (_items.isEmpty) throw StateError('Cannot peek an empty stack');
    return _items.last;
  }

  T? tryPop() => _items.isEmpty ? null : _items.removeLast();

  bool get isEmpty => _items.isEmpty;
  bool get isNotEmpty => _items.isNotEmpty;
  int get length => _items.length;

  @override
  String toString() => 'Stack(${_items.join(', ')} ← top)';
}

void main() {
  final books = Stack<String>()
    ..push('Dart Basics')
    ..push('Flutter in Action')
    ..push('Algorithms');

  print(books);          // Stack(Dart Basics, Flutter in Action, Algorithms ← top)
  print(books.peek());   // Algorithms
  print(books.pop());    // Algorithms
  print(books.length);   // 2

  final empty = Stack<int>();
  print(empty.tryPop()); // null
  try {
    empty.pop();
  } on StateError catch (e) {
    print(e.message);    // Cannot pop from an empty stack
  }
}
```

**🔍 What This Code Does:**

1. **Private Storage**: `_items` is private, so users can only use stack operations.
2. **Clear Errors**: Popping an empty stack throws a `StateError` with a helpful message.
3. **Safe Variant**: `tryPop` returns `null` instead of throwing.
4. **Cascades**: `..push(...)` chains pushes on the same object.
5. **All O(1)**: Every operation touches only the end of the list.

### Linked-list stack

A stack can also be built from a singly linked list, pushing and popping at the **head**:

```dart
class _Node<T> {
  final T value;
  final _Node<T>? next;
  _Node(this.value, this.next);
}

class LinkedStack<T> {
  _Node<T>? _top;
  int _length = 0;

  void push(T value) {
    _top = _Node(value, _top);
    _length++;
  }

  T pop() {
    final top = _top ?? (throw StateError('empty'));
    _top = top.next;
    _length--;
    return top.value;
  }

  T peek() => (_top ?? (throw StateError('empty'))).value;
  bool get isEmpty => _top == null;
  int get length => _length;
}

void main() {
  final s = LinkedStack<int>()
    ..push(1)
    ..push(2)
    ..push(3);
  print(s.pop());  // 3
  print(s.peek()); // 2
  print(s.length); // 2
}
```

**🔍 What This Code Does:**

1. **Head = Top**: Pushing creates a new head; popping moves the head forward. Both O(1), with no amortization.
2. **Immutable Nodes**: `final next` works because we never change a node after creating it.
3. **Throw as an Expression**: `_top ?? (throw ...)` throws when the stack is empty.
4. **Trade-off**: An extra object per item, versus the List version's occasional resize.

---

## ✅ Classic Problem: Balanced Brackets

Every opening bracket must be closed by the **matching** bracket in the **right order**. The most recently opened bracket must close first: that's LIFO!

```dart
bool isBalanced(String code) {
  const pairs = {')': '(', ']': '[', '}': '{'};
  final stack = <String>[];

  for (final ch in code.split('')) {
    if (ch == '(' || ch == '[' || ch == '{') {
      stack.add(ch);                       // opener: push
    } else if (pairs.containsKey(ch)) {
      if (stack.isEmpty || stack.removeLast() != pairs[ch]) {
        return false;                      // nothing to match, or wrong type
      }
    }
  }
  return stack.isEmpty;                    // leftovers mean unclosed openers
}

void main() {
  print(isBalanced('{[()]}'));                 // true
  print(isBalanced('void main() { print([1, 2]); }')); // true
  print(isBalanced('([)]'));                   // false (wrong order)
  print(isBalanced('(()'));                    // false (unclosed)
  print(isBalanced('())'));                    // false (extra closer)
}
```

**🔍 What This Code Does:**

1. **Push Openers**: Every `(`, `[` or `{` goes on the stack.
2. **Match Closers**: A closer must match the **top** opener; the map `pairs` says which opener each closer needs.
3. **Three Failure Modes**: Wrong type (`([)]`), extra closer (`())`), or leftover openers (`(()`).
4. **Ignores Other Characters**: Letters and symbols in real code are skipped.
5. **O(n) Time, O(n) Space**: One pass, the stack holds at most n openers.

---

## ↩️ Undo / Redo With Two Stacks

```dart
class TextEditor {
  String text = '';
  final _undo = <String>[];
  final _redo = <String>[];

  void type(String s) {
    _undo.add(text); // save the state before changing it
    text += s;
    _redo.clear();   // a new action invalidates the redo history
  }

  void undo() {
    if (_undo.isEmpty) return;
    _redo.add(text);
    text = _undo.removeLast();
  }

  void redo() {
    if (_redo.isEmpty) return;
    _undo.add(text);
    text = _redo.removeLast();
  }
}

void main() {
  final editor = TextEditor()
    ..type('Hello')
    ..type(', Dart')
    ..type('!');
  print(editor.text); // Hello, Dart!

  editor.undo();
  print(editor.text); // Hello, Dart
  editor.undo();
  print(editor.text); // Hello

  editor.redo();
  print(editor.text); // Hello, Dart

  editor.type(' rocks');
  editor.redo();      // nothing to redo now
  print(editor.text); // Hello, Dart rocks
}
```

**🔍 What This Code Does:**

1. **Undo Stack**: Holds previous states; the most recent change is undone first (LIFO).
2. **Redo Stack**: Holds states we've undone, so we can step forward again.
3. **Moving Between Stacks**: Undo pops from `_undo` and pushes onto `_redo`, and vice versa.
4. **New Action Clears Redo**: Typing after an undo starts a new timeline.
5. **Real Apps**: Store **commands** (what changed) instead of whole text snapshots to save memory.

---

## 🧮 Evaluating Expressions: Reverse Polish Notation

In **postfix** notation (RPN), operators come **after** their operands: `3 4 +` means `3 + 4`. There are no parentheses and no precedence rules, and a stack evaluates it in one pass.

```dart
int evalRpn(List<String> tokens) {
  final stack = <int>[];
  for (final t in tokens) {
    switch (t) {
      case '+' || '-' || '*' || '/':
        final b = stack.removeLast(); // right operand (pushed last)
        final a = stack.removeLast(); // left operand
        stack.add(switch (t) {
          '+' => a + b,
          '-' => a - b,
          '*' => a * b,
          _ => a ~/ b,
        });
      default:
        stack.add(int.parse(t));
    }
  }
  return stack.single;
}

void main() {
  // (3 + 4) * 2
  print(evalRpn(['3', '4', '+', '2', '*'])); // 14
  // 5 - (6 / 3)
  print(evalRpn(['5', '6', '3', '/', '-'])); // 3
}
```

**🔍 What This Code Does:**

1. **Numbers Are Pushed**: `int.parse` turns each number token into an int.
2. **Operators Pop Two**: The **first** pop is the **right** operand, because it was pushed last. Order matters for `-` and `/`.
3. **Push the Result**: The answer becomes an operand for later operators.
4. **Dart 3 Patterns**: `case '+' || '-' ...` matches any operator; the `switch` **expression** picks the calculation.
5. **`stack.single`**: A valid expression leaves exactly one value; `single` throws otherwise.

### From infix to postfix: the Shunting-Yard algorithm

How do calculators turn `3 + 4 * 2` into RPN? With **two** structures: an output list and an operator **stack**.

```dart
List<String> toRpn(List<String> tokens) {
  const precedence = {'+': 1, '-': 1, '*': 2, '/': 2};
  final output = <String>[];
  final ops = <String>[];

  for (final t in tokens) {
    if (precedence.containsKey(t)) {
      // pop operators with higher or equal precedence (left-associative)
      while (ops.isNotEmpty &&
          ops.last != '(' &&
          precedence[ops.last]! >= precedence[t]!) {
        output.add(ops.removeLast());
      }
      ops.add(t);
    } else if (t == '(') {
      ops.add(t);
    } else if (t == ')') {
      while (ops.last != '(') {
        output.add(ops.removeLast());
      }
      ops.removeLast(); // discard '('
    } else {
      output.add(t); // number
    }
  }
  while (ops.isNotEmpty) {
    output.add(ops.removeLast());
  }
  return output;
}

void main() {
  print(toRpn('3 + 4 * 2'.split(' ')).join(' '));         // 3 4 2 * +
  print(toRpn('( 3 + 4 ) * 2'.split(' ')).join(' '));     // 3 4 + 2 *
  print(toRpn('10 - 2 - 3'.split(' ')).join(' '));        // 10 2 - 3 -
}
```

**🔍 What This Code Does:**

1. **Numbers Go Straight to Output**.
2. **Operators Wait on the Stack**: Before pushing, pop any operator that should be applied **first** (higher or equal precedence).
3. **Parentheses**: `(` is a wall on the stack; `)` pops everything back to the matching `(`.
4. **Flush at the End**: Remaining operators are appended.
5. **Left-Associativity**: `>=` makes `10 - 2 - 3` evaluate as `(10 - 2) - 3`.

---

## 📉 The Monotonic Stack

A **monotonic stack** keeps its elements in sorted order (always increasing or always decreasing). When a new element would break the order, we **pop** until it fits, and each pop answers a question about the popped element.

### Next greater element

For each number, find the first number to its **right** that is bigger.

```dart
List<int> nextGreater(List<int> nums) {
  final result = List<int>.filled(nums.length, -1);
  final stack = <int>[]; // indexes; their values are decreasing

  for (var i = 0; i < nums.length; i++) {
    while (stack.isNotEmpty && nums[stack.last] < nums[i]) {
      result[stack.removeLast()] = nums[i]; // nums[i] is their answer
    }
    stack.add(i);
  }
  return result; // anything left on the stack has no greater element
}

void main() {
  print(nextGreater([2, 1, 2, 4, 3])); // [4, 2, 4, -1, -1]
}
```

**🔍 What This Code Does:**

1. **Stack of Waiting Indexes**: Each index waits until a bigger number shows up.
2. **Resolve on Arrival**: When `nums[i]` is bigger than the top, the top's answer is `nums[i]`; pop and repeat.
3. **Decreasing Stack**: After the `while`, everything on the stack is ≥ `nums[i]`, so pushing keeps it decreasing.
4. **Default −1**: Indexes never resolved have no greater element.
5. **O(n)**: Each index is pushed once and popped at most once, even though there's a nested `while`.

### Daily temperatures: how many days until warmer?

```dart
List<int> daysUntilWarmer(List<int> temps) {
  final answer = List<int>.filled(temps.length, 0);
  final stack = <int>[];
  for (var day = 0; day < temps.length; day++) {
    while (stack.isNotEmpty && temps[stack.last] < temps[day]) {
      final prev = stack.removeLast();
      answer[prev] = day - prev;
    }
    stack.add(day);
  }
  return answer;
}

void main() {
  print(daysUntilWarmer([73, 74, 75, 71, 69, 72, 76, 73]));
  // [1, 1, 4, 2, 1, 1, 0, 0]
}
```

**🔍 What This Code Does:**

1. **Same Pattern**: Store indexes, resolve them when a warmer day arrives.
2. **Distance Instead of Value**: The answer is `day - prev`, the number of days waited.
3. **O(n)**: A brute force double loop would be O(n²).

### Largest rectangle in a histogram (the boss level 🏆)

```dart
import 'dart:math';

int largestRectangle(List<int> heights) {
  final stack = <int>[]; // indexes with increasing heights
  var best = 0;
  for (var i = 0; i <= heights.length; i++) {
    final h = i == heights.length ? 0 : heights[i]; // sentinel 0 flushes the stack
    while (stack.isNotEmpty && heights[stack.last] > h) {
      final height = heights[stack.removeLast()];
      final left = stack.isEmpty ? -1 : stack.last;
      best = max(best, height * (i - left - 1));
    }
    stack.add(i);
  }
  return best;
}

void main() {
  print(largestRectangle([2, 1, 5, 6, 2, 3])); // 10
}
```

**🔍 What This Code Does:**

1. **Increasing Stack**: Bars are kept in increasing height order.
2. **Pop When a Shorter Bar Arrives**: The popped bar can't extend further right, so its rectangle ends here.
3. **Width**: From just after the new stack top (`left`) up to `i − 1`.
4. **Sentinel Height 0**: An extra iteration flushes every remaining bar.
5. **O(n)**: Each bar is pushed and popped once.

---

## 📚 The Call Stack Is a Stack

Every function call **pushes** a frame; every return **pops** it. That's why recursion can be converted into a loop with an explicit stack (see **Recursion & Iteration**), and why infinite recursion causes a **stack** overflow.

```dart
void main() {
  // Depth-first traversal of a folder tree with an explicit stack
  final tree = {
    'root': ['src', 'test'],
    'src': ['main.dart', 'utils.dart'],
    'test': ['main_test.dart'],
  };

  final stack = ['root'];
  while (stack.isNotEmpty) {
    final node = stack.removeLast();
    print(node);
    final children = tree[node] ?? const [];
    // push in reverse so the first child is processed first
    stack.addAll(children.reversed);
  }
}
```

**🔍 What This Code Does:**

1. **Explicit Stack**: Replaces recursive calls.
2. **Pop, Visit, Push Children**: The classic depth-first loop.
3. **Reverse Push**: Because the stack is LIFO, pushing children in reverse makes them come out in their original order.
4. **Output**: `root, src, main.dart, utils.dart, test, main_test.dart`.

---

## ⚠️ Common Mistakes

### 1. Popping an empty stack

```dart
void main() {
  final stack = <int>[];
  // stack.removeLast(); ❌ throws RangeError
  final top = stack.isEmpty ? null : stack.removeLast(); // ✅
  print(top); // null
}
```

**🔍 What This Code Does:**

1. **Always Check First**: `removeLast` on an empty List throws.
2. **Safe Pop**: Return `null` (or a default) when empty.

### 2. Wrong operand order

In RPN and similar problems, the **first** pop is the **right-hand** operand. `a - b` with `b` popped first; swapping them gives wrong answers for `-` and `/`.

### 3. Using the front of a List as the top

`insert(0, x)` and `removeAt(0)` are O(n). Always use the **end**.

### 4. Forgetting leftovers

In bracket matching, a non-empty stack at the end means unclosed openers. In monotonic stack problems, leftover indexes need a default answer.

---

## 🧪 Try It Yourself

1. **Min stack**: support `push`, `pop`, `top` and `getMin()` all in O(1). *(Hint: a second stack of current minimums.)*
2. **Simplify a path**: `'/a/./b/../../c/'` → `'/c'` using a stack of folder names.
3. **Decode a string**: `'3[a2[c]]'` → `'accaccacc'`.
4. **Remove adjacent duplicates**: `'abbaca'` → `'ca'`.

```dart
class MinStack {
  final _items = <int>[];
  final _mins = <int>[];

  void push(int x) {
    _items.add(x);
    _mins.add(_mins.isEmpty || x < _mins.last ? x : _mins.last);
  }

  int pop() {
    _mins.removeLast();
    return _items.removeLast();
  }

  int get top => _items.last;
  int get min => _mins.last;
}

void main() {
  final s = MinStack()
    ..push(5)
    ..push(2)
    ..push(8);
  print(s.min); // 2
  s.pop();
  s.pop();
  print(s.min); // 5
}
```

**🔍 What This Code Does:**

1. **Parallel Stacks**: `_mins` stores the minimum **at each depth**.
2. **Push**: The new minimum is the smaller of `x` and the previous minimum.
3. **Pop Both**: Keeps the two stacks in sync, so `min` is always correct in O(1).

---

## 📌 Key Takeaways

- ✅ A **stack** is **LIFO**: push and pop at the **top** only.
- ✅ In Dart, use a `List` with `add` / `removeLast` / `last`; all O(1).
- ✅ Stacks solve **matching** problems (brackets, tags), **undo/redo**, and **expression evaluation** (RPN, Shunting-Yard).
- ✅ A **monotonic stack** answers "next greater/smaller" questions in **O(n)**.
- ✅ The **call stack** is a stack; any recursion can use an explicit stack instead.
- ✅ Always handle the **empty** case and the **operand order**.

**Next up:** 🚶‍♀️🚶🚶‍♂️ **Queues & Deques**: first in, first out.
