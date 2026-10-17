TRIE = r"""class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isWord = false;
}

class Trie {
  final root = TrieNode();

  void insert(String word) {
    var n = root;
    for (final ch in word.split('')) {
      n = n.children.putIfAbsent(ch, TrieNode.new);
    }
    n.isWord = true;
  }

  TrieNode? walk(String prefix) {
    var n = root;
    for (final ch in prefix.split('')) {
      final next = n.children[ch];
      if (next == null) return null;
      n = next;
    }
    return n;
  }

  bool contains(String w) => walk(w)?.isWord ?? false;
  bool hasPrefix(String p) => walk(p) != null;
}
"""

PIC = r"""```dart
//            (root)
//           /      \
//          c        d
//          |        |
//          a        o*
//         / \       |
//        r*  t*     g*
//       / \
//      t*  e*
// * = end of a word
```"""

QUESTIONS = [
    mcq(r"""
What is a trie?
""", ["A tree that stores strings character by character, sharing common prefixes",
       "A hash table for strings", "A sorted list of words", "A binary search tree of words"],
        "A tree that stores strings character by character, sharing common prefixes"),

    mcq(r"""
What is another name for a trie?
""", ["Prefix tree", "Heap", "Splay tree", "Hash ring"], "Prefix tree"),

    mcq(r"""
What is the cost of looking up a word of length L in a trie?
""", ["O(L)", "O(n)", "O(log n)", "O(n × L)"], "O(L)"),

    mcq(r"""
Does trie lookup time depend on how many words are stored?
""", ["No, only on the length of the word", "Yes, it's O(n)", "Yes, it's O(log n)",
       "Only for long words"], "No, only on the length of the word"),

    mcq(r"""
Which words are stored in this trie?

""" + PIC, ["car, cart, care, cat, do, dog", "c, ca, car, cat, d, do, dog",
                "cart, care, cat, dog", "car, cat, dog"], "car, cart, care, cat, do, dog"),

    mcq(r"""
In this trie, is "ca" a stored word?

""" + PIC, ["No, it's only a prefix (no end-of-word mark)", "Yes", "Only if 'car' is deleted",
                "It depends on the alphabet"], "No, it's only a prefix (no end-of-word mark)"),

    mcq(r"""
Why does a trie node need an end-of-word flag?
""", ["To distinguish complete words from prefixes of longer words",
       "To store the word's length", "To mark leaves only", "To count characters"],
        "To distinguish complete words from prefixes of longer words"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
void main() {
  final t = Trie();
  for (final w in ['tea', 'ten', 'to']) {
    t.insert(w);
  }
  print(t.contains('te'));
  print(t.hasPrefix('te'));
}
```
""", ["false then true", "true then true", "false then false", "true then false"],
        "false then true"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
void main() {
  final t = Trie()..insert('dart');
  print(t.contains('dart'));
  print(t.contains('darts'));
  print(t.hasPrefix('da'));
}
```
""", ["true then false then true", "true then true then true", "false then false then true",
       "true then false then false"], "true then false then true"),

    mcq(r"""
How many child nodes does the root have after inserting 'apple', 'apricot' and 'banana'?
""", ["2", "3", "1", "0"], "2"),

    mcq(r"""
What does `putIfAbsent(ch, TrieNode.new)` do?
""", ["Returns the existing child for ch, or creates and stores a new one",
       "Always replaces the child", "Removes the child", "Returns null if missing"],
        "Returns the existing child for ch, or creates and stores a new one"),

    mcq(r"""
What is `TrieNode.new`?
""", ["A constructor tear-off (a function that creates a TrieNode)", "A static field",
       "A keyword for allocating memory", "A deprecated syntax"],
        "A constructor tear-off (a function that creates a TrieNode)"),

    order(r"""
Complete trie insertion:

```dart
void insert(String word) {
  var n = root;
  for (final ch in word.%order%('')) {
    n = n.children.%order%(ch, TrieNode.new);
  }
  n.%order% = true;
}
```
""", ["split", "putIfAbsent", "isWord", "join", "update", "isEmpty"],
        ["split", "putIfAbsent", "isWord"]),

    mcq(r"""
How does autocomplete use a trie?
""", ["Walk to the prefix node, then collect every word in its subtree",
       "Scan every stored word", "Sort the words and binary search", "Hash the prefix"],
        "Walk to the prefix node, then collect every word in its subtree"),

    mcq(r"""
What is the cost of finding all words with prefix P (with k matching characters in total)?
""", ["O(P + output size)", "O(n)", "O(n log n)", "O(P × n)"], "O(P + output size)"),

    mcq(r"""
How can autocomplete return suggestions in alphabetical order?
""", ["Visit each node's children in sorted order during DFS", "Use a hash map",
       "Use BFS only", "Reverse the results"],
        "Visit each node's children in sorted order during DFS"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
List<String> collect(TrieNode n, String path) {
  final out = <String>[];
  if (n.isWord) out.add(path);
  final keys = n.children.keys.toList()..sort();
  for (final k in keys) {
    out.addAll(collect(n.children[k]!, path + k));
  }
  return out;
}

void main() {
  final t = Trie();
  for (final w in ['cab', 'car', 'ca', 'dog']) {
    t.insert(w);
  }
  print(collect(t.walk('ca')!, 'ca'));
}
```
""", ["[ca, cab, car]", "[cab, car]", "[car, cab, ca]", "[ca, cab, car, dog]"],
        "[ca, cab, car]"),

    mcq(r"""
How would you rank autocomplete suggestions by popularity?
""", ["Store a count or score on word nodes and pick the top ones (e.g. with a heap)",
       "Sort by word length", "Use BFS order", "Pick random words"],
        "Store a count or score on word nodes and pick the top ones (e.g. with a heap)"),

    mcq(r"""
When are array-based children (26 slots) a good choice?
""", ["For a small, fixed alphabet like lowercase a–z", "For Unicode text with emoji",
       "When memory is very limited and words are sparse", "Never"],
        "For a small, fixed alphabet like lowercase a–z"),

    mcq(r"""
What is the index of the letter 'c' in a 26-slot children array using `unit - 97`?
""", ["2", "3", "99", "-1"], "2"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('d'.codeUnitAt(0) - 97);
}
```
""", ["3", "4", "100", "97"], "3"),

    mcq(r"""
What goes wrong if a 26-slot trie receives the word 'Dart'?
""", ["'D' maps to a negative index and causes a RangeError", "It works fine",
       "It stores 'dart'", "It silently skips 'D'"],
        "'D' maps to a negative index and causes a RangeError"),

    mcq(r"""
What is a trade-off of array children vs map children?
""", ["Arrays are faster but waste memory on unused slots", "Arrays use less memory always",
       "Maps are always faster", "There is no difference"],
        "Arrays are faster but waste memory on unused slots"),

    fill(r"""
Create the child only if missing, then use it:

```dart
class Node {
  final List<Node?> next = List.filled(26, null);
}

void main() {
  final n = Node();
  final child = n.next[0] %fill% Node();
  print(identical(child, n.next[0])); // true
}
```
""", "??="),

    mcq(r"""
How can a trie answer "how many words start with P?" in O(P)?
""", ["Store a pass count on each node, incremented during insert", "Count leaves every time",
       "Use a hash map of all prefixes", "It can't"],
        "Store a pass count on each node, incremented during insert"),

    mcq(r"""
What does this print?

```dart
class Node {
  final Map<String, Node> kids = {};
  int pass = 0;
}

void main() {
  final root = Node();
  for (final w in ['app', 'apple', 'ape', 'bat']) {
    var n = root;
    for (final c in w.split('')) {
      n = n.kids.putIfAbsent(c, Node.new);
      n.pass++;
    }
  }
  print(root.kids['a']!.kids['p']!.pass);
}
```
""", ["3", "4", "2", "1"], "3"),

    mcq(r"""
When deleting a word from a trie, which nodes can be pruned?
""", ["Nodes that no longer mark a word and have no children", "All nodes of the word",
       "Only the root", "None; you only clear the flag"],
        "Nodes that no longer mark a word and have no children"),

    mcq(r"""
After inserting 'car' and 'cart' and deleting 'cart', what happens to the 'c → a → r' nodes?
""", ["They stay, because 'car' still needs them", "They're all deleted",
       "Only 'c' remains", "The trie becomes empty"],
        "They stay, because 'car' still needs them"),

    mcq(r"""
What is the longest common prefix of ['flower', 'flow', 'flight']?
""", ["fl", "flo", "f", "flow"], "fl"),

    mcq(r"""
How does a trie find the longest common prefix of all words?
""", ["Walk down while a node has exactly one child and no word ends there",
       "Find the deepest leaf", "Pick the shortest word", "Count total nodes"],
        "Walk down while a node has exactly one child and no word ends there"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
String shortestRoot(Trie t, String word) {
  var n = t.root;
  for (var i = 0; i < word.length; i++) {
    final next = n.children[word[i]];
    if (next == null) return word;
    n = next;
    if (n.isWord) return word.substring(0, i + 1);
  }
  return word;
}

void main() {
  final t = Trie()
    ..insert('cat')
    ..insert('ca');
  print(shortestRoot(t, 'cattle'));
  print(shortestRoot(t, 'dog'));
}
```
""", ["ca then dog", "cat then dog", "cattle then dog", "ca then null"], "ca then dog"),

    mcq(r"""
In a wildcard search where '.' matches any letter, what does the trie do at a '.'?
""", ["Try every child and succeed if any branch matches", "Skip the character",
       "Fail immediately", "Only try the first child"],
        "Try every child and succeed if any branch matches"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
bool match(TrieNode n, String p, [int i = 0]) {
  if (i == p.length) return n.isWord;
  if (p[i] == '.') {
    return n.children.values.any((c) => match(c, p, i + 1));
  }
  final next = n.children[p[i]];
  return next != null && match(next, p, i + 1);
}

void main() {
  final t = Trie();
  for (final w in ['bad', 'dad', 'mad']) {
    t.insert(w);
  }
  print(match(t.root, '.ad'));
  print(match(t.root, 'b..'));
  print(match(t.root, 'b.'));
}
```
""", ["true then true then false", "true then false then false", "false then true then true",
       "true then true then true"], "true then true then false"),

    mcq(r"""
Which task is a trie much better at than a hash set?
""", ["Finding all words that start with a prefix", "Checking an exact word",
       "Storing integers", "Counting total words"],
        "Finding all words that start with a prefix"),

    mcq(r"""
Why does a hash set need O(n) to answer "does any word start with 'pre'?"
""", ["Hashing works on whole keys, so it must scan every word", "Hash sets are sorted",
       "It doesn't; it's O(1)", "Hash sets can't store strings"],
        "Hashing works on whole keys, so it must scan every word"),

    mcq(r"""
What is the main downside of tries?
""", ["They can use a lot of memory (many nodes)", "Lookups are slow",
       "They can't store prefixes", "They only work for numbers"],
        "They can use a lot of memory (many nodes)"),

    mcq(r"""
What does a radix (compressed) trie do?
""", ["Merges chains of single-child nodes into one edge to save space",
       "Stores numbers in base 2", "Removes the end-of-word flag", "Sorts the children"],
        "Merges chains of single-child nodes into one edge to save space"),

    mcq(r"""
Which real-world feature is a natural fit for a trie?
""", ["Search box autocomplete", "Undo history", "Shortest driving route", "A print queue"],
        "Search box autocomplete"),

    mcq(r"""
Which of these is also a trie application?
""", ["IP routing tables (longest prefix match)", "Sorting numbers", "Matrix multiplication",
       "Counting sort"], "IP routing tables (longest prefix match)"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
int countNodes(TrieNode n) =>
    1 + n.children.values.fold(0, (s, c) => s + countNodes(c));

void main() {
  final t = Trie();
  for (final w in ['to', 'tea', 'ten']) {
    t.insert(w);
  }
  print(countNodes(t.root));
}
```
""", ["6", "8", "5", "9"], "6"),

    mcq(r"""
Inserting 'car' into a trie that already contains 'cart' does what?
""", ["Marks the existing 'r' node as a word end; no new nodes", "Creates 3 new nodes",
       "Replaces 'cart'", "Throws an error"],
        "Marks the existing 'r' node as a word end; no new nodes"),

    mcq(r"""
What does `_walk(prefix)` return when the prefix isn't in the trie?
""", ["null", "The root", "An empty node", "It throws"], "null"),

    mcq(r"""
What does `walk(word)?.isWord ?? false` evaluate to when the path doesn't exist?
""", ["false", "null", "true", "It throws"], "false"),

    mcq(r"""
What is the space complexity of a trie storing n words of average length L (worst case)?
""", ["O(n × L) nodes", "O(n)", "O(L)", "O(1)"], "O(n × L) nodes"),

    order(r"""
Complete the prefix walk:

```dart
TrieNode? walk(String prefix) {
  var n = root;
  for (final ch in prefix.split('')) {
    final next = n.%order%[ch];
    if (next %order% null) return %order%;
    n = next;
  }
  return n;
}
```
""", ["children", "==", "null", "!=", "root", "isWord"], ["children", "==", "null"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final root = <String, Map>{};
  for (final w in ['ab', 'ac']) {
    var node = root;
    for (final ch in w.split('')) {
      node = node.putIfAbsent(ch, () => <String, Map>{}) as Map<String, Map>;
    }
  }
  print(root.keys.toList());
  print((root['a'] as Map).keys.toList());
}
```
""", ["[a] then [b, c]", "[a, a] then [b, c]", "[ab, ac] then []", "[a] then [b]"],
        "[a] then [b, c]"),

    mcq(r"""
How many nodes does the path for the word 'dart' add to an empty trie (excluding the root)?
""", ["4", "5", "1", "3"], "4"),

    mcq(r"""
Which word game naturally uses a trie to prune impossible paths?
""", ["Boggle", "Sudoku", "Chess", "Tic-tac-toe"], "Boggle"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
void main() {
  final t = Trie();
  for (final w in ['a', 'ab', 'abc']) {
    t.insert(w);
  }
  var words = 0;
  var n = t.root;
  for (final ch in 'abc'.split('')) {
    n = n.children[ch]!;
    if (n.isWord) words++;
  }
  print(words);
}
```
""", ["3", "1", "2", "0"], "3"),

    mcq(r"""
Which structure is a trie most similar to in shape?
""", ["A general tree where each edge is labeled with a character", "A linked list",
       "A binary heap", "A circular buffer"],
        "A general tree where each edge is labeled with a character"),

    mcq(r"""
To support case-insensitive lookups in a trie, what should you do?
""", ["Normalize words (e.g. toLowerCase) on insert and on lookup", "Use a bigger array",
       "Store each word twice", "It's impossible"],
        "Normalize words (e.g. toLowerCase) on insert and on lookup"),

    mcq(r"""
What does this print?

```dart
""" + TRIE + r"""
void main() {
  final t = Trie();
  for (final w in ['Dart', 'dash'.toLowerCase()]) {
    t.insert(w.toLowerCase());
  }
  print(t.hasPrefix('da'));
  print(t.contains('Dart'));
}
```
""", ["true then false", "true then true", "false then false", "false then true"],
        "true then false"),
]
