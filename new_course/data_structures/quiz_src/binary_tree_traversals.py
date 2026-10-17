NODE = r"""class Node {
  final int v;
  final Node? left, right;
  const Node(this.v, [this.left, this.right]);
}
"""

PIC = r"""```dart
//        1
//       / \
//      2   3
//     / \   \
//    4   5   6
```"""

QUESTIONS = [
    mcq(r"""
What is the order of a pre-order traversal?
""", ["node → left → right", "left → node → right", "left → right → node", "level by level"],
        "node → left → right"),

    mcq(r"""
What is the order of an in-order traversal?
""", ["left → node → right", "node → left → right", "left → right → node", "right → node → left"],
        "left → node → right"),

    mcq(r"""
What is the order of a post-order traversal?
""", ["left → right → node", "node → left → right", "left → node → right", "node → right → left"],
        "left → right → node"),

    mcq(r"""
What is the pre-order traversal of this tree?

""" + PIC, ["1 2 4 5 3 6", "4 2 5 1 3 6", "4 5 2 6 3 1", "1 2 3 4 5 6"], "1 2 4 5 3 6"),

    mcq(r"""
What is the in-order traversal of this tree?

""" + PIC, ["4 2 5 1 3 6", "1 2 4 5 3 6", "4 5 2 6 3 1", "1 2 3 4 5 6"], "4 2 5 1 3 6"),

    mcq(r"""
What is the post-order traversal of this tree?

""" + PIC, ["4 5 2 6 3 1", "4 2 5 1 3 6", "1 2 4 5 3 6", "6 5 4 3 2 1"], "4 5 2 6 3 1"),

    mcq(r"""
Which traversal of a binary search tree produces values in sorted order?
""", ["In-order", "Pre-order", "Post-order", "None of them"], "In-order"),

    mcq(r"""
Which traversal is best for evaluating an expression tree?
""", ["Post-order (children before the operator)", "Pre-order", "In-order",
       "Level-order"], "Post-order (children before the operator)"),

    mcq(r"""
Which traversal is natural for copying or serializing a tree?
""", ["Pre-order", "Post-order", "In-order", "Random order"], "Pre-order"),

    mcq(r"""
Which traversal is natural for deleting/freeing every node safely?
""", ["Post-order (children before parent)", "Pre-order", "In-order", "Level-order"],
        "Post-order (children before parent)"),

    mcq(r"""
What is the time complexity of any of the three depth-first traversals?
""", ["O(n)", "O(log n)", "O(n log n)", "O(n²)"], "O(n)"),

    mcq(r"""
What is the extra space used by a recursive traversal?
""", ["O(h), where h is the tree height", "O(1)", "O(n²)", "O(log n) always"],
        "O(h), where h is the tree height"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void pre(Node? n, List<int> out) {
  if (n == null) return;
  out.add(n.v);
  pre(n.left, out);
  pre(n.right, out);
}

void main() {
  final out = <int>[];
  pre(const Node(1, Node(2, Node(4)), Node(3)), out);
  print(out);
}
```
""", ["[1, 2, 4, 3]", "[4, 2, 1, 3]", "[4, 2, 3, 1]", "[1, 2, 3, 4]"], "[1, 2, 4, 3]"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void inOrder(Node? n, List<int> out) {
  if (n == null) return;
  inOrder(n.left, out);
  out.add(n.v);
  inOrder(n.right, out);
}

void main() {
  final out = <int>[];
  inOrder(const Node(8, Node(3, Node(1), Node(6)), Node(10)), out);
  print(out);
}
```
""", ["[1, 3, 6, 8, 10]", "[8, 3, 1, 6, 10]", "[1, 6, 3, 10, 8]", "[10, 8, 6, 3, 1]"],
        "[1, 3, 6, 8, 10]"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void post(Node? n, List<int> out) {
  if (n == null) return;
  post(n.left, out);
  post(n.right, out);
  out.add(n.v);
}

void main() {
  final out = <int>[];
  post(const Node(1, Node(2), Node(3, Node(4))), out);
  print(out);
}
```
""", ["[2, 4, 3, 1]", "[1, 2, 3, 4]", "[2, 1, 4, 3]", "[4, 3, 2, 1]"], "[2, 4, 3, 1]"),

    order(r"""
Complete the in-order traversal:

```dart
void inOrder(Node? n, List<int> out) {
  if (n == null) return;
  inOrder(n.%order%, out);
  out.add(n.%order%);
  inOrder(n.%order%, out);
}
```
""", ["left", "v", "right", "next", "value"], ["left", "v", "right"]),

    mcq(r"""
In iterative pre-order with a stack, which child do you push first?
""", ["Right, so that left is popped first", "Left, so that it's popped first",
       "Either; order doesn't matter", "Neither; use a queue"],
        "Right, so that left is popped first"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<int> preIter(Node? root) {
  final out = <int>[];
  if (root == null) return out;
  final st = <Node>[root];
  while (st.isNotEmpty) {
    final n = st.removeLast();
    out.add(n.v);
    if (n.right != null) st.add(n.right!);
    if (n.left != null) st.add(n.left!);
  }
  return out;
}

void main() {
  print(preIter(const Node(1, Node(2, Node(4), Node(5)), Node(3))));
}
```
""", ["[1, 2, 4, 5, 3]", "[1, 3, 2, 5, 4]", "[4, 5, 2, 3, 1]", "[1, 2, 3, 4, 5]"],
        "[1, 2, 4, 5, 3]"),

    mcq(r"""
What happens in iterative pre-order if you push left BEFORE right?
""", ["You get node → right → left order", "It's still correct pre-order",
       "It becomes in-order", "It crashes"], "You get node → right → left order"),

    mcq(r"""
In iterative in-order traversal, what is the first step at each node?
""", ["Push nodes while going as far left as possible", "Visit the node immediately",
       "Push the right child", "Pop everything from the stack"],
        "Push nodes while going as far left as possible"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
List<int> inIter(Node? root) {
  final out = <int>[], st = <Node>[];
  var cur = root;
  while (cur != null || st.isNotEmpty) {
    while (cur != null) {
      st.add(cur);
      cur = cur.left;
    }
    final n = st.removeLast();
    out.add(n.v);
    cur = n.right;
  }
  return out;
}

void main() {
  print(inIter(const Node(4, Node(2, Node(1), Node(3)), Node(5))));
}
```
""", ["[1, 2, 3, 4, 5]", "[4, 2, 1, 3, 5]", "[1, 3, 2, 5, 4]", "[5, 4, 3, 2, 1]"],
        "[1, 2, 3, 4, 5]"),

    mcq(r"""
How does the two-stack trick produce post-order iteratively?
""", ["Traverse node → right → left, then reverse the result", "Traverse in-order and reverse",
       "Traverse pre-order twice", "Use a queue instead of a stack"],
        "Traverse node → right → left, then reverse the result"),

    mcq(r"""
What is the reverse of "node → right → left" order?
""", ["left → right → node (post-order)", "left → node → right (in-order)",
       "node → left → right (pre-order)", "right → left → node"],
        "left → right → node (post-order)"),

    mcq(r"""
Why might you prefer an iterative traversal over a recursive one?
""", ["To avoid stack overflow on very deep trees", "It's always shorter code",
       "It visits fewer nodes", "Recursion doesn't work on trees"],
        "To avoid stack overflow on very deep trees"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
String ser(Node? n) => n == null ? '#' : '${n.v},${ser(n.left)},${ser(n.right)}';

void main() {
  print(ser(const Node(1, Node(2), null)));
}
```
""", ["1,2,#,#,#", "1,2,#", "2,1,#", "1,#,2,#,#"], "1,2,#,#,#"),

    mcq(r"""
Why does tree serialization include `#` markers for null children?
""", ["So the exact shape can be rebuilt unambiguously", "To save space",
       "Because Dart can't print null", "To sort the values"],
        "So the exact shape can be rebuilt unambiguously"),

    mcq(r"""
What does this print?

```dart
sealed class E {}

class Num extends E {
  final int v;
  Num(this.v);
}

class Add extends E {
  final E l, r;
  Add(this.l, this.r);
}

class Mul extends E {
  final E l, r;
  Mul(this.l, this.r);
}

int eval(E e) => switch (e) {
      Num(:final v) => v,
      Add(:final l, :final r) => eval(l) + eval(r),
      Mul(:final l, :final r) => eval(l) * eval(r),
    };

void main() {
  print(eval(Mul(Add(Num(2), Num(3)), Num(4))));
}
```
""", ["20", "14", "24", "9"], "20"),

    mcq(r"""
In the expression evaluator with a `sealed` class, what does `sealed` give you?
""", ["Exhaustiveness checking in switch: every subtype must be handled",
       "Faster evaluation", "Immutability", "Automatic toString"],
        "Exhaustiveness checking in switch: every subtype must be handled"),

    mcq(r"""
What is the pattern `Op(:final symbol, :final left)` called?
""", ["An object pattern that destructures fields by name", "A record literal",
       "A constructor call", "A type cast"],
        "An object pattern that destructures fields by name"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int maxDepth(Node? n) {
  if (n == null) return 0;
  final l = maxDepth(n.left), r = maxDepth(n.right);
  return 1 + (l > r ? l : r);
}

void main() {
  print(maxDepth(const Node(1, Node(2, Node(3, Node(4))), Node(5))));
}
```
""", ["4", "3", "5", "2"], "4"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void sums(Node? n, int so, List<int> out) {
  if (n == null) return;
  final t = so + n.v;
  if (n.left == null && n.right == null) {
    out.add(t);
    return;
  }
  sums(n.left, t, out);
  sums(n.right, t, out);
}

void main() {
  final out = <int>[];
  sums(const Node(1, Node(2, Node(4)), Node(3)), 0, out);
  print(out);
}
```
""", ["[7, 4]", "[3, 4]", "[1, 3, 7]", "[10]"], "[7, 4]"),

    mcq(r"""
In path-sum problems, how does the running total move?
""", ["Down from parent to children as a parameter", "Up from leaves as a return value",
       "Through a global stack only", "It's recomputed at each leaf from scratch"],
        "Down from parent to children as a parameter"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
bool same(Node? a, Node? b) {
  if (a == null || b == null) return a == b;
  return a.v == b.v && same(a.left, b.left) && same(a.right, b.right);
}

void main() {
  print(same(const Node(1, Node(2)), const Node(1, Node(2))));
  print(same(const Node(1, Node(2)), const Node(1, null, Node(2))));
}
```
""", ["true then false", "true then true", "false then false", "false then true"],
        "true then false"),

    mcq(r"""
In `same(a, b)`, what does `if (a == null || b == null) return a == b;` handle?
""", ["Both null → true; exactly one null → false", "Both null → false",
       "It compares values", "It throws on null"],
        "Both null → true; exactly one null → false"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void leaves(Node? n, List<int> out) {
  if (n == null) return;
  if (n.left == null && n.right == null) out.add(n.v);
  leaves(n.left, out);
  leaves(n.right, out);
}

void main() {
  final out = <int>[];
  leaves(const Node(1, Node(2, Node(4), Node(5)), Node(3, null, Node(6))), out);
  print(out);
}
```
""", ["[4, 5, 6]", "[4, 5, 3, 6]", "[1, 2, 3]", "[6, 5, 4]"], "[4, 5, 6]"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void inOrder(Node? n, void Function(int) visit) {
  if (n == null) return;
  inOrder(n.left, visit);
  visit(n.v);
  inOrder(n.right, visit);
}

void main() {
  final sb = StringBuffer();
  inOrder(const Node(2, Node(1), Node(3)), sb.write);
  print(sb);
}
```
""", ["123", "213", "132", "321"], "123"),

    mcq(r"""
What is a "tear-off" like `sb.write` passed as a callback?
""", ["A method reference used as a function value", "A copy of the StringBuffer",
       "A call that runs immediately", "A deprecated syntax"],
        "A method reference used as a function value"),

    mcq(r"""
What does Morris traversal achieve?
""", ["In-order traversal in O(1) extra space by temporarily threading pointers",
       "O(log n) traversal time", "Traversal without visiting leaves",
       "Sorting a tree"],
        "In-order traversal in O(1) extra space by temporarily threading pointers"),

    mcq(r"""
In Morris traversal, what is the "predecessor" of a node?
""", ["The rightmost node of its left subtree", "Its parent", "Its left child",
       "The root"], "The rightmost node of its left subtree"),

    mcq(r"""
Does Morris traversal leave the tree modified when it finishes?
""", ["No, it removes the temporary threads", "Yes, all right pointers change",
       "Yes, the tree becomes a linked list", "It deletes the leaves"],
        "No, it removes the temporary threads"),

    mcq(r"""
Given pre-order `A B D E C` and in-order `D B E A C`, what is the root?
""", ["A", "D", "B", "C"], "A"),

    mcq(r"""
Given pre-order `A B D E C` and in-order `D B E A C`, which nodes are in A's left subtree?
""", ["D, B, E", "C", "B only", "D and C"], "D, B, E"),

    mcq(r"""
Which pair of traversals uniquely identifies a binary tree with unique values?
""", ["Pre-order and in-order", "Pre-order and post-order (always)", "Only in-order",
       "Only post-order"], "Pre-order and in-order"),

    fill(r"""
Advance an iterator to the next token:

```dart
void main() {
  final it = 'a,b'.split(',').iterator;
  it.%fill%();
  print(it.current); // a
}
```
""", "moveNext"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int countNodes(Node? n) => n == null ? 0 : 1 + countNodes(n.left) + countNodes(n.right);

void main() {
  print(countNodes(const Node(1, Node(2, Node(3)), Node(4, null, Node(5)))));
}
```
""", ["5", "4", "3", "6"], "5"),

    mcq(r"""
Which traversal visits a node BEFORE any of its descendants?
""", ["Pre-order", "Post-order", "In-order", "Reverse in-order"], "Pre-order"),

    mcq(r"""
Which traversal visits a node AFTER all of its descendants?
""", ["Post-order", "Pre-order", "In-order", "Level-order"], "Post-order"),

    mcq(r"""
What is "reverse in-order" (right → node → left) on a BST useful for?
""", ["Getting values in descending order", "Getting values in ascending order",
       "Serializing the tree", "Deleting the tree"], "Getting values in descending order"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
void rev(Node? n, List<int> out) {
  if (n == null) return;
  rev(n.right, out);
  out.add(n.v);
  rev(n.left, out);
}

void main() {
  final out = <int>[];
  rev(const Node(5, Node(3, Node(1)), Node(8)), out);
  print(out);
}
```
""", ["[8, 5, 3, 1]", "[1, 3, 5, 8]", "[5, 3, 1, 8]", "[8, 1, 3, 5]"], "[8, 5, 3, 1]"),

    mcq(r"""
To find the k-th smallest value in a BST, which traversal do you use?
""", ["In-order, stopping after k visits", "Pre-order", "Post-order", "Level-order"],
        "In-order, stopping after k visits"),

    mcq(r"""
What does this print?

```dart
""" + NODE + r"""
int? kth(Node? root, int k) {
  final st = <Node>[];
  var cur = root;
  while (cur != null || st.isNotEmpty) {
    while (cur != null) {
      st.add(cur);
      cur = cur.left;
    }
    final n = st.removeLast();
    if (--k == 0) return n.v;
    cur = n.right;
  }
  return null;
}

void main() {
  print(kth(const Node(5, Node(3, Node(2), Node(4)), Node(7)), 3));
}
```
""", ["4", "3", "5", "2"], "4"),

    order(r"""
Complete the iterative pre-order loop:

```dart
while (stack.isNotEmpty) {
  final n = stack.%order%();
  out.add(n.v);
  if (n.%order% != null) stack.add(n.right!);
  if (n.%order% != null) stack.add(n.left!);
}
```
""", ["removeLast", "right", "left", "removeFirst", "first"], ["removeLast", "right", "left"]),

    mcq(r"""
What does `const Node(1, Node(2))` require of the Node class?
""", ["A const constructor and only final fields", "A factory constructor",
       "Mutable fields", "A static method"], "A const constructor and only final fields"),

    mcq(r"""
What is the maximum number of nodes on the explicit stack during iterative in-order traversal?
""", ["About the height of the tree", "Always n", "Always 1", "n²"],
        "About the height of the tree"),
]
