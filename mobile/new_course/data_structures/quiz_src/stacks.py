QUESTIONS = [
    mcq(r"""
What ordering rule does a stack follow?
""", ["LIFO: last in, first out", "FIFO: first in, first out",
       "Sorted order", "Random order"], "LIFO: last in, first out"),

    mcq(r"""
Which Dart List methods make it behave like a stack?
""", ["add, removeLast and last", "insert(0, x) and removeAt(0)",
       "add and removeAt(0)", "sort and first"], "add, removeLast and last"),

    mcq(r"""
What is the cost of push and pop on a List-based stack?
""", ["O(1) (push is amortized)", "O(n)", "O(log n)", "O(n²)"],
        "O(1) (push is amortized)"),

    mcq(r"""
Why shouldn't you use the front of a List as the top of a stack?
""", ["insert(0, x) and removeAt(0) are O(n)", "The front can't be read",
       "Lists don't have a front", "It reverses LIFO into FIFO"],
        "insert(0, x) and removeAt(0) are O(n)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = <int>[];
  s.add(1);
  s.add(2);
  s.add(3);
  s.removeLast();
  s.add(4);
  print(s.last);
}
```
""", ["4", "3", "1", "2"], "4"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = ['a', 'b', 'c'];
  final out = <String>[];
  while (s.isNotEmpty) {
    out.add(s.removeLast());
  }
  print(out.join());
}
```
""", ["cba", "abc", "a", "c"], "cba"),

    fill(r"""
Peek at the top of a List-based stack without removing it:

```dart
void main() {
  final stack = [1, 2, 3];
  print(stack.%fill%); // 3
}
```
""", "last"),

    mcq(r"""
What happens when calling `removeLast()` on an empty List?
""", ["It throws a RangeError", "It returns null", "It returns 0", "Nothing happens"],
        "It throws a RangeError"),

    mcq(r"""
In a linked-list stack, which end acts as the top?
""", ["The head", "The tail", "The middle", "A random node"], "The head"),

    mcq(r"""
What does this print?

```dart
class Node {
  final int v;
  final Node? next;
  Node(this.v, this.next);
}

void main() {
  Node? top;
  for (final x in [1, 2, 3]) {
    top = Node(x, top);
  }
  top = top!.next;
  print(top!.v);
}
```
""", ["2", "3", "1", "null"], "2"),

    mcq(r"""
Which problem is a classic use of a stack?
""", ["Checking balanced brackets", "Finding the shortest path in a weighted graph",
       "Serving customers in arrival order", "Counting word frequencies"],
        "Checking balanced brackets"),

    mcq(r"""
Why does bracket matching use a stack?
""", ["The most recently opened bracket must be closed first (LIFO)",
       "Brackets must be sorted", "Brackets are unique", "It needs O(1) indexing"],
        "The most recently opened bracket must be closed first (LIFO)"),

    mcq(r"""
What does this print?

```dart
bool balanced(String s) {
  const pairs = {')': '(', ']': '[', '}': '{'};
  final stack = <String>[];
  for (final c in s.split('')) {
    if ('([{'.contains(c)) {
      stack.add(c);
    } else if (pairs.containsKey(c)) {
      if (stack.isEmpty || stack.removeLast() != pairs[c]) return false;
    }
  }
  return stack.isEmpty;
}

void main() {
  print(balanced('{[]()}'));
  print(balanced('{[(])}'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Why does `balanced('(()')` return false?
""", ["An opener is left on the stack at the end", "The closer doesn't match",
       "The stack is empty when a closer arrives", "Parentheses aren't supported"],
        "An opener is left on the stack at the end"),

    mcq(r"""
Why does `balanced('())')` return false?
""", ["A closer arrives when the stack is empty", "An opener is left over",
       "The types don't match", "It has an odd length"],
        "A closer arrives when the stack is empty"),

    mcq(r"""
What are the time and space complexities of bracket matching on n characters?
""", ["O(n) time, O(n) space", "O(n²) time, O(1) space", "O(n log n) time, O(n) space",
       "O(1) time, O(1) space"], "O(n) time, O(n) space"),

    mcq(r"""
How many stacks does a simple undo/redo system use?
""", ["Two: one for undo, one for redo", "One", "Three", "None; it uses a queue"],
        "Two: one for undo, one for redo"),

    mcq(r"""
What should happen to the redo stack when the user performs a NEW action after undoing?
""", ["It should be cleared", "It should be reversed", "It should be merged into undo",
       "Nothing"], "It should be cleared"),

    mcq(r"""
What does this print?

```dart
void main() {
  var text = '';
  final undo = <String>[];
  for (final s in ['a', 'b', 'c']) {
    undo.add(text);
    text += s;
  }
  text = undo.removeLast();
  text = undo.removeLast();
  print(text);
}
```
""", ["a", "ab", "abc", "''"], "a"),

    mcq(r"""
What is `3 4 + 2 *` in Reverse Polish Notation equal to?
""", ["14", "11", "10", "24"], "14"),

    mcq(r"""
When evaluating RPN, an operator pops two values. Which one is the RIGHT operand?
""", ["The first one popped", "The second one popped", "Either; order never matters",
       "The bottom of the stack"], "The first one popped"),

    mcq(r"""
What does this print?

```dart
int eval(List<String> tokens) {
  final s = <int>[];
  for (final t in tokens) {
    if (t == '-') {
      final b = s.removeLast();
      final a = s.removeLast();
      s.add(a - b);
    } else {
      s.add(int.parse(t));
    }
  }
  return s.single;
}

void main() {
  print(eval(['10', '3', '-']));
}
```
""", ["7", "-7", "13", "3"], "7"),

    mcq(r"""
What does this print?

```dart
int evalRpn(List<String> tokens) {
  final s = <int>[];
  for (final t in tokens) {
    switch (t) {
      case '+' || '*':
        final b = s.removeLast(), a = s.removeLast();
        s.add(t == '+' ? a + b : a * b);
      default:
        s.add(int.parse(t));
    }
  }
  return s.single;
}

void main() {
  print(evalRpn(['2', '3', '4', '*', '+']));
}
```
""", ["14", "20", "24", "9"], "14"),

    fill(r"""
Get the only remaining element (throws if there isn't exactly one):

```dart
void main() {
  final stack = [42];
  print(stack.%fill%); // 42
}
```
""", "single"),

    mcq(r"""
What does the Shunting-Yard algorithm do?
""", ["Converts infix expressions to postfix (RPN)", "Sorts numbers",
       "Finds shortest paths", "Balances binary trees"],
        "Converts infix expressions to postfix (RPN)"),

    mcq(r"""
What is `3 + 4 * 2` in postfix notation?
""", ["3 4 2 * +", "3 4 + 2 *", "+ 3 * 4 2", "3 4 2 + *"], "3 4 2 * +"),

    mcq(r"""
What is `(3 + 4) * 2` in postfix notation?
""", ["3 4 + 2 *", "3 4 2 * +", "* + 3 4 2", "3 + 4 2 *"], "3 4 + 2 *"),

    mcq(r"""
In Shunting-Yard, what happens when a `)` is read?
""", ["Pop operators to the output until the matching ( is found", "Push it onto the stack",
       "Add it to the output", "Clear the whole stack"],
        "Pop operators to the output until the matching ( is found"),

    mcq(r"""
Why does Shunting-Yard pop operators with EQUAL precedence before pushing a new one?
""", ["To make operators like - and / left-associative", "To sort operators",
       "To remove duplicates", "It never does"],
        "To make operators like - and / left-associative"),

    mcq(r"""
What is a monotonic stack?
""", ["A stack whose elements are kept in increasing or decreasing order",
       "A stack with only one element", "A stack that can't be popped",
       "A stack of sorted strings only"],
        "A stack whose elements are kept in increasing or decreasing order"),

    mcq(r"""
What does this print?

```dart
List<int> nextGreater(List<int> a) {
  final res = List<int>.filled(a.length, -1);
  final s = <int>[];
  for (var i = 0; i < a.length; i++) {
    while (s.isNotEmpty && a[s.last] < a[i]) {
      res[s.removeLast()] = a[i];
    }
    s.add(i);
  }
  return res;
}

void main() {
  print(nextGreater([4, 5, 2, 25]));
}
```
""", ["[5, 25, 25, -1]", "[5, 25, 25, 25]", "[-1, 5, 25, -1]", "[5, -1, 25, -1]"],
        "[5, 25, 25, -1]"),

    mcq(r"""
Why is the "next greater element" monotonic stack algorithm O(n) despite a nested while?
""", ["Each index is pushed once and popped at most once", "The while loop runs once",
       "Dart optimizes it", "It isn't; it's O(n²)"],
        "Each index is pushed once and popped at most once"),

    mcq(r"""
What does this print?

```dart
List<int> warmer(List<int> t) {
  final ans = List<int>.filled(t.length, 0);
  final s = <int>[];
  for (var d = 0; d < t.length; d++) {
    while (s.isNotEmpty && t[s.last] < t[d]) {
      final p = s.removeLast();
      ans[p] = d - p;
    }
    s.add(d);
  }
  return ans;
}

void main() {
  print(warmer([30, 40, 50, 60]));
}
```
""", ["[1, 1, 1, 0]", "[3, 2, 1, 0]", "[0, 0, 0, 0]", "[1, 1, 1, 1]"], "[1, 1, 1, 0]"),

    mcq(r"""
In "daily temperatures", what do leftover indexes on the stack mean?
""", ["No warmer day ever comes, so their answer stays 0", "They are errors",
       "They are the warmest days so far and get answer 1", "They must be re-processed"],
        "No warmer day ever comes, so their answer stays 0"),

    mcq(r"""
What is the largest rectangle area in the histogram `[2, 1, 5, 6, 2, 3]`?
""", ["10", "12", "6", "8"], "10"),

    mcq(r"""
In the histogram algorithm, why process an extra bar of height 0 at the end?
""", ["To flush every remaining bar from the stack", "To avoid an empty list",
       "To make the stack increasing", "It's not needed"],
        "To flush every remaining bar from the stack"),

    mcq(r"""
What causes a StackOverflowError?
""", ["Too many nested function calls filling the call stack", "Popping an empty List",
       "Pushing too many items onto a List", "Using recursion at all"],
        "Too many nested function calls filling the call stack"),

    mcq(r"""
In iterative DFS with an explicit stack, why push children in reverse?
""", ["So the first child is popped (processed) first", "To sort the children",
       "To save memory", "Because Lists are reversed"],
        "So the first child is popped (processed) first"),

    mcq(r"""
What does this print?

```dart
void main() {
  final tree = {'r': ['a', 'b'], 'a': ['c']};
  final stack = ['r'];
  final out = <String>[];
  while (stack.isNotEmpty) {
    final n = stack.removeLast();
    out.add(n);
    stack.addAll((tree[n] ?? const []).reversed);
  }
  print(out.join());
}
```
""", ["racb", "rabc", "rbac", "rcab"], "racb"),

    mcq(r"""
How does a MinStack return the minimum in O(1)?
""", ["It keeps a second stack of the minimum at each depth", "It sorts on every push",
       "It scans the stack on each call", "It stores only the minimum"],
        "It keeps a second stack of the minimum at each depth"),

    mcq(r"""
What does this print?

```dart
void main() {
  final items = <int>[], mins = <int>[];
  void push(int x) {
    items.add(x);
    mins.add(mins.isEmpty || x < mins.last ? x : mins.last);
  }

  push(3);
  push(1);
  push(4);
  print(mins.last);
  items.removeLast();
  mins.removeLast();
  items.removeLast();
  mins.removeLast();
  print(mins.last);
}
```
""", ["1 then 3", "1 then 1", "3 then 3", "4 then 3"], "1 then 3"),

    mcq(r"""
What does this print?

```dart
String removeAdjacentDups(String s) {
  final st = <String>[];
  for (final c in s.split('')) {
    if (st.isNotEmpty && st.last == c) {
      st.removeLast();
    } else {
      st.add(c);
    }
  }
  return st.join();
}

void main() {
  print(removeAdjacentDups('abbaca'));
}
```
""", ["ca", "aca", "abca", "a"], "ca"),

    mcq(r"""
What does this print?

```dart
String simplify(String path) {
  final st = <String>[];
  for (final part in path.split('/')) {
    if (part.isEmpty || part == '.') continue;
    if (part == '..') {
      if (st.isNotEmpty) st.removeLast();
    } else {
      st.add(part);
    }
  }
  return '/${st.join('/')}';
}

void main() {
  print(simplify('/a/./b/../../c/'));
}
```
""", ["/c", "/a/c", "/a/b/c", "/"], "/c"),

    order(r"""
Complete the safe pop:

```dart
T? tryPop<T>(List<T> stack) =>
    stack.%order% ? %order% : stack.%order%();
```
""", ["isEmpty", "null", "removeLast", "isNotEmpty", "removeAt", "first"],
        ["isEmpty", "null", "removeLast"]),

    mcq(r"""
What does a well-designed `Stack<T>` class hide by keeping its List private?
""", ["Operations that break the top-only rule, like inserting in the middle",
       "The push method", "The length", "The type parameter"],
        "Operations that break the top-only rule, like inserting in the middle"),

    mcq(r"""
What error type does the lesson's `Stack.pop()` throw on an empty stack?
""", ["StateError", "RangeError", "ArgumentError", "FormatException"], "StateError"),

    fill(r"""
Throw an error as an expression when the stack is empty:

```dart
T pop<T>(List<T> stack) {
  if (stack.isEmpty) %fill% StateError('empty');
  return stack.removeLast();
}
```
""", "throw"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = <int>[1, 2, 3];
  s.add(s.removeLast() + s.removeLast());
  print(s);
}
```
""", ["[1, 5]", "[1, 2, 5]", "[6]", "[3, 3]"], "[1, 5]"),

    mcq(r"""
Which of these is NOT naturally a stack?
""", ["A printer queue serving jobs in arrival order", "Undo history",
       "The function call stack", "Browser back button history"],
        "A printer queue serving jobs in arrival order"),

    mcq(r"""
What does this print?

```dart
void main() {
  final st = <String>[];
  for (final w in 'to be or not'.split(' ')) {
    st.add(w);
  }
  final out = <String>[];
  while (st.isNotEmpty) {
    out.add(st.removeLast());
  }
  print(out.join(' '));
}
```
""", ["not or be to", "to be or not", "ton ro eb ot", "not"], "not or be to"),

    mcq(r"""
Which Dart 3 pattern matches any of several string constants in a switch case?
""", ["case '+' || '-':", "case '+', '-':", "case ['+', '-']:", "case in ['+', '-']:"],
        "case '+' || '-':"),

    mcq(r"""
What does this print?

```dart
void main() {
  const t = '*';
  final r = switch (t) {
    '+' => 1 + 2,
    '*' => 1 * 2,
    _ => 0,
  };
  print(r);
}
```
""", ["2", "3", "0", "It doesn't compile"], "2"),

    mcq(r"""
What's the maximum size a stack reaches when checking `((((()))))` for balance?
""", ["5", "10", "1", "0"], "5"),

    mcq(r"""
Which structure would you use to reverse the order of items with only push/pop?
""", ["A stack", "A queue", "A set", "A map"], "A stack"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = <int>[];
  for (var i = 1; i <= 3; i++) {
    s.add(i * 10);
  }
  print(s.removeLast() - s.removeLast());
}
```
""", ["10", "-10", "20", "30"], "10"),
]
