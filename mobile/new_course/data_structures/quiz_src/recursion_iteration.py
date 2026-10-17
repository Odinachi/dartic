QUESTIONS = [
    mcq(r"""
What is recursion?
""", [
        "A function solving a problem by calling itself on a smaller version of it",
        "A loop that runs forever",
        "A function that returns another function",
        "Running two functions at the same time",
    ], "A function solving a problem by calling itself on a smaller version of it"),

    mcq(r"""
What are the two essential parts of a recursive function?
""", ["A base case and a recursive case", "A loop and a counter",
       "A try and a catch", "An async and an await"], "A base case and a recursive case"),

    mcq(r"""
What happens if a recursive function has no reachable base case?
""", ["It eventually throws a StackOverflowError", "It returns null",
       "Dart automatically stops it after 100 calls", "It becomes a loop"],
        "It eventually throws a StackOverflowError"),

    mcq(r"""
What does this print?

```dart
int factorial(int n) => n <= 1 ? 1 : n * factorial(n - 1);

void main() {
  print(factorial(5));
}
```
""", ["120", "24", "15", "720"], "120"),

    fill(r"""
Complete the base case:

```dart
int factorial(int n) {
  if (n %fill% 1) return 1;
  return n * factorial(n - 1);
}
```
""", "<="),

    mcq(r"""
What is pushed onto the call stack each time a function is called?
""", ["A stack frame with its parameters, locals and return address",
       "A copy of the entire program", "A new isolate", "A Future"],
        "A stack frame with its parameters, locals and return address"),

    mcq(r"""
What is the extra space complexity of `factorial(n)` implemented recursively?
""", ["O(n)", "O(1)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the extra space complexity of this iterative factorial?

```dart
int factorial(int n) {
  var result = 1;
  for (var i = 2; i <= n; i++) result *= i;
  return result;
}
```
""", ["O(1)", "O(n)", "O(log n)", "O(n²)"], "O(1)"),

    mcq(r"""
Does Dart perform tail-call optimization?
""", ["No, every recursive call uses a stack frame", "Yes, always",
       "Only in release mode", "Only for functions named tail"],
        "No, every recursive call uses a stack frame"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('ab' * 3);
}
```
""", ["ababab", "ab3", "aaabbb", "It throws an error"], "ababab"),

    mcq(r"""
What does this print?

```dart
int sumTo(int n) => n == 0 ? 0 : n + sumTo(n - 1);

void main() {
  print(sumTo(100));
}
```
""", ["5050", "100", "4950", "10000"], "5050"),

    mcq(r"""
Which error does Dart throw when recursion goes too deep?
""", ["StackOverflowError", "OutOfMemoryError", "RangeError", "RecursionError"],
        "StackOverflowError"),

    fill(r"""
Catch the error caused by runaway recursion:

```dart
int forever(int n) => forever(n + 1);

void main() {
  try {
    forever(0);
  } on %fill% {
    print('too deep');
  }
}
```
""", "StackOverflowError"),

    mcq(r"""
Why does the iterative version handle `sumTo(10000000)` while the recursive one crashes?
""", ["The loop uses O(1) space instead of 10 million stack frames",
       "Loops are compiled to native code but recursion isn't",
       "The recursive version has a bug in its base case",
       "Dart limits recursion to 1,000 calls"],
        "The loop uses O(1) space instead of 10 million stack frames"),

    mcq(r"""
How many calls does naive `fib(n)` (two recursive calls per call) make, roughly?
""", ["Exponential in n", "Exactly n", "n log n", "n²"], "Exponential in n"),

    mcq(r"""
What does this print?

```dart
var calls = 0;

int fib(int n) {
  calls++;
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

void main() {
  fib(5);
  print(calls);
}
```
""", ["15", "5", "8", "10"], "15"),

    mcq(r"""
What does memoization do?
""", ["Caches results of calls so repeated subproblems aren't recomputed",
       "Converts recursion into a loop automatically",
       "Reduces stack depth to O(1)", "Sorts the inputs first"],
        "Caches results of calls so repeated subproblems aren't recomputed"),

    fill(r"""
Complete the memoized Fibonacci:

```dart
final memo = <int, int>{};

int fib(int n) {
  if (n <= 1) return n;
  return memo[n] %fill%= fib(n - 1) + fib(n - 2);
}
```
""", "??"),

    mcq(r"""
What does this print?

```dart
final memo = <int, int>{};

int fib(int n) {
  if (n <= 1) return n;
  return memo[n] ??= fib(n - 1) + fib(n - 2);
}

void main() {
  print(fib(40));
}
```
""", ["102334155", "63245986", "165580141", "40"], "102334155"),

    mcq(r"""
What is the time complexity of memoized Fibonacci?
""", ["O(n)", "O(2ⁿ)", "O(log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the space complexity of the two-variable iterative Fibonacci?
""", ["O(1)", "O(n)", "O(log n)", "O(2ⁿ)"], "O(1)"),

    order(r"""
Complete the iterative Fibonacci:

```dart
int fib(int n) {
  if (n <= 1) return n;
  var prev = 0, curr = 1;
  for (var i = 2; i <= n; i++) {
    final next = %order% + curr;
    prev = %order%;
    curr = %order%;
  }
  return curr;
}
```
""", ["prev", "curr", "next", "i"], ["prev", "curr", "next"]),

    mcq(r"""
How can any recursive algorithm be made iterative?
""", ["By managing your own explicit stack", "By adding async", "By using a Set",
       "It can't; some recursion can never be iterative"],
        "By managing your own explicit stack"),

    fill(r"""
Complete the "pop" step of an explicit stack:

```dart
void main() {
  final stack = <int>[1, 2, 3];
  while (stack.isNotEmpty) {
    final top = stack.%fill%();
    print(top);
  }
}
```
""", "removeLast"),

    mcq(r"""
What does this print?

```dart
void main() {
  final stack = <int>[1, 2, 3];
  final out = <int>[];
  while (stack.isNotEmpty) {
    out.add(stack.removeLast());
  }
  print(out);
}
```
""", ["[3, 2, 1]", "[1, 2, 3]", "[1, 3, 2]", "[]"], "[3, 2, 1]"),

    mcq(r"""
Why does an explicit stack avoid stack overflow?
""", ["It lives on the heap, which is much larger than the call stack",
       "Lists can't hold more than 1,000 items", "It runs in a separate isolate",
       "It uses tail calls"], "It lives on the heap, which is much larger than the call stack"),

    mcq(r"""
What does this print?

```dart
String reverse(String s) {
  if (s.length <= 1) return s;
  return reverse(s.substring(1)) + s[0];
}

void main() {
  print(reverse('flutter'));
}
```
""", ["rettulf", "flutter", "rettulF", "fluttre"], "rettulf"),

    mcq(r"""
What does this print?

```dart
int power(int base, int exp) {
  if (exp == 0) return 1;
  final half = power(base, exp ~/ 2);
  return exp.isEven ? half * half : half * half * base;
}

void main() {
  print(power(2, 13));
}
```
""", ["8192", "4096", "26", "16384"], "8192"),

    mcq(r"""
What is the time complexity of this `power` function?

```dart
int power(int base, int exp) {
  if (exp == 0) return 1;
  final half = power(base, exp ~/ 2);
  return exp.isEven ? half * half : half * half * base;
}
```
""", ["O(log exp)", "O(exp)", "O(exp²)", "O(1)"], "O(log exp)"),

    mcq(r"""
What happens to `power`'s complexity if it calls `power(base, exp ~/ 2)` twice instead of storing `half`?
""", ["It becomes O(exp)", "It stays O(log exp)", "It becomes O(1)", "It becomes O(2^exp)"],
        "It becomes O(exp)"),

    mcq(r"""
What does this print?

```dart
int digitSum(int n) => n < 10 ? n : (n % 10) + digitSum(n ~/ 10);

void main() {
  print(digitSum(4321));
}
```
""", ["10", "4321", "1234", "4"], "10"),

    fill(r"""
Get the last digit of a number:

```dart
void main() {
  final n = 987;
  print(n %fill% 10); // 7
}
```
""", "%"),

    mcq(r"""
What does `987 ~/ 10` evaluate to?
""", ["98", "98.7", "7", "99"], "98"),

    mcq(r"""
What does this print?

```dart
int search(List<int> a, int t, [int lo = 0, int? hi]) {
  hi ??= a.length - 1;
  if (lo > hi) return -1;
  final mid = (lo + hi) ~/ 2;
  if (a[mid] == t) return mid;
  return a[mid] < t ? search(a, t, mid + 1, hi) : search(a, t, lo, mid - 1);
}

void main() {
  print(search([1, 4, 9, 16, 25], 16));
}
```
""", ["3", "4", "2", "-1"], "3"),

    mcq(r"""
What is the stack depth of recursive binary search on n items?
""", ["O(log n)", "O(n)", "O(1)", "O(n log n)"], "O(log n)"),

    mcq(r"""
What are the three steps of backtracking?
""", ["Choose, explore, un-choose", "Sort, search, return", "Push, pop, peek",
       "Hash, bucket, compare"], "Choose, explore, un-choose"),

    mcq(r"""
How many permutations does `['A', 'B', 'C', 'D']` have?
""", ["24", "12", "16", "4"], "24"),

    mcq(r"""
In the permutation example, why do we call `current.removeLast()` after the recursive call?
""", ["To undo the choice so the next option starts from a clean state",
       "To free memory", "To sort the result", "To stop the recursion"],
        "To undo the choice so the next option starts from a clean state"),

    mcq(r"""
What does this print?

```dart
void perms(List<String> items, List<String> cur, Set<int> used, List<String> out) {
  if (cur.length == items.length) {
    out.add(cur.join());
    return;
  }
  for (var i = 0; i < items.length; i++) {
    if (used.contains(i)) continue;
    used.add(i);
    cur.add(items[i]);
    perms(items, cur, used, out);
    cur.removeLast();
    used.remove(i);
  }
}

void main() {
  final out = <String>[];
  perms(['x', 'y'], [], {}, out);
  print(out);
}
```
""", ["[xy, yx]", "[xy]", "[x, y]", "[yx, xy]"], "[xy, yx]"),

    mcq(r"""
For recursive functions, space complexity is determined by:
""", ["The maximum depth of the call stack", "The total number of calls ever made",
       "The number of base cases", "The number of parameters"],
        "The maximum depth of the call stack"),

    mcq(r"""
What is wrong with this function?

```dart
int halve(int n) {
  if (n == 0) return 0;
  return halve(n - 2);
}
```
""", ["Odd inputs skip 0 and never reach the base case", "It returns the wrong type",
       "n - 2 is not allowed in Dart", "Nothing; it always works"],
        "Odd inputs skip 0 and never reach the base case"),

    mcq(r"""
Which base case fixes `halve` for all integers?
""", ["if (n <= 0) return 0;", "if (n == 1) return 0;", "if (n == 2) return 0;",
       "if (n > 0) return 0;"], "if (n <= 0) return 0;"),

    mcq(r"""
What does this print?

```dart
int count(int n) {
  if (n == 0) return 0;
  count(n - 1);
  return 1;
}

void main() {
  print(count(5));
}
```
""", ["1", "5", "0", "15"], "1"),

    mcq(r"""
Why does `count(5)` return 1 instead of 5?

```dart
int count(int n) {
  if (n == 0) return 0;
  count(n - 1);
  return 1;
}
```
""", ["The recursive result is ignored instead of being added",
       "The base case is wrong", "count is called with the wrong argument",
       "Dart caches the first result"],
        "The recursive result is ignored instead of being added"),

    mcq(r"""
What does this print?

```dart
class Node {
  final int size;
  final List<Node> kids;
  Node(this.size, [this.kids = const []]);
}

int total(Node n) {
  var t = n.size;
  for (final k in n.kids) t += total(k);
  return t;
}

void main() {
  final tree = Node(1, [Node(2), Node(3, [Node(4)])]);
  print(total(tree));
}
```
""", ["10", "6", "4", "1"], "10"),

    mcq(r"""
In the file-size example, what acts as the base case?
""", ["A node with no children, where the loop doesn't run", "A node with size 0",
       "The root node", "There is no base case"],
        "A node with no children, where the loop doesn't run"),

    mcq(r"""
Which kinds of problems are naturally recursive?
""", ["Self-similar ones like trees, folders and divide-and-conquer",
       "Adding two numbers", "Printing a single line", "Reading one variable"],
        "Self-similar ones like trees, folders and divide-and-conquer"),

    mcq(r"""
What does this print?

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
  print(flatten([1, [2, [3]], [4, 5]]));
}
```
""", ["[1, 2, 3, 4, 5]", "[1, [2, [3]], [4, 5]]", "[1, 4, 5]", "[[1], [2], [3], [4], [5]]"],
        "[1, 2, 3, 4, 5]"),

    fill(r"""
Check whether an Object is an int:

```dart
void main() {
  Object item = 42;
  if (item %fill% int) {
    print(item + 1);
  }
}
```
""", "is"),

    mcq(r"""
Why can this code use `item + 1` without a cast?

```dart
void main() {
  Object item = 42;
  if (item is int) {
    print(item + 1);
  }
}
```
""", ["Type promotion after the `is int` check", "Object supports +",
       "Dart ignores types at runtime", "item is declared as int"],
        "Type promotion after the `is int` check"),

    mcq(r"""
What does this print?

```dart
bool isPalindrome(String s) {
  if (s.length <= 1) return true;
  if (s[0] != s[s.length - 1]) return false;
  return isPalindrome(s.substring(1, s.length - 1));
}

void main() {
  print(isPalindrome('racecar'));
  print(isPalindrome('dart'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    order(r"""
Complete the recursive palindrome check:

```dart
bool isPal(String s) {
  if (s.length %order% 1) return true;
  if (s[0] %order% s[s.length - 1]) return false;
  return isPal(s.%order%(1, s.length - 1));
}
```
""", ["<=", "!=", "substring", "==", ">=", "split"], ["<=", "!=", "substring"]),

    mcq(r"""
Which is usually true about recursion vs iteration speed?
""", ["Iteration is usually slightly faster because it avoids function call overhead",
       "Recursion is always faster", "They are always identical",
       "Iteration is always O(n²)"],
        "Iteration is usually slightly faster because it avoids function call overhead"),

    mcq(r"""
What does this print?

```dart
void countdown(int n) {
  if (n < 0) return;
  print(n);
  countdown(n - 1);
}

void main() {
  countdown(2);
}
```
""", ["2 1 0", "0 1 2", "2 1", "1 2"], "2 1 0"),

    mcq(r"""
What does this print?

```dart
void countup(int n) {
  if (n < 0) return;
  countup(n - 1);
  print(n);
}

void main() {
  countup(2);
}
```
""", ["0 1 2", "2 1 0", "1 2", "2 1"], "0 1 2"),

    mcq(r"""
Why does `countup` print in increasing order?
""", ["The print happens after the recursive call returns (while unwinding)",
       "Dart sorts printed output", "The base case prints everything",
       "n is incremented each call"],
        "The print happens after the recursive call returns (while unwinding)"),
]
