# Tries

Imagine typing **"flu"** into a search box and instantly seeing suggestions: **flutter**, **fluent**, **flute**, **fluffy**. 🔎

How does the app find every word starting with "flu" so fast, out of hundreds of thousands of words? It doesn't scan them all. It walks down a path: **f → l → u**, and everything **below** that point starts with "flu".

👉 That's a **trie** (pronounced "try", from re**trie**val), also called a **prefix tree**:

> A **trie** stores strings character by character along paths from the root. Words that share a **prefix** share the **same path**. Looking up a word or prefix of length **L** takes **O(L)**, no matter how many words are stored.

---

## 🌳 What a Trie Looks Like

Words: `car`, `cart`, `care`, `cat`, `dog`, `do`

```text
             (root)
            /      \
           c        d
           |        |
           a        o ✓        ← "do" ends here
          / \       |
         r ✓  t ✓    g ✓       ← "car", "cat", "dog"
        / \
       t ✓  e ✓                ← "cart", "care"

✓ = a word ends at this node
```

- Each **edge** is one character.
- Each **node** represents the prefix spelled by the path from the root.
- A node is marked **✓ (end of word)** if a stored word ends there. `car` is a word, but `ca` is not.
- `car`, `cart` and `care` share the nodes for `c → a → r`.

---

## 🏗️ Building a Trie in Dart

```dart
class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isWord = false;
}

class Trie {
  final _root = TrieNode();
  int _words = 0;

  int get length => _words;

  void insert(String word) {
    var node = _root;
    for (final ch in word.split('')) {
      node = node.children.putIfAbsent(ch, TrieNode.new);
    }
    if (!node.isWord) {
      node.isWord = true;
      _words++;
    }
  }

  TrieNode? _walk(String prefix) {
    var node = _root;
    for (final ch in prefix.split('')) {
      final next = node.children[ch];
      if (next == null) return null; // path breaks: no such prefix
      node = next;
    }
    return node;
  }

  bool contains(String word) => _walk(word)?.isWord ?? false;

  bool hasPrefix(String prefix) => _walk(prefix) != null;
}

void main() {
  final trie = Trie();
  for (final w in ['car', 'cart', 'care', 'cat', 'dog', 'do']) {
    trie.insert(w);
  }

  print(trie.contains('car'));  // true
  print(trie.contains('ca'));   // false (a prefix, not a word)
  print(trie.hasPrefix('ca'));  // true
  print(trie.contains('cars')); // false
  print(trie.hasPrefix('z'));   // false
  print(trie.length);           // 6
}
```

**🔍 What This Code Does:**

This code demonstrates **a map-based trie with insert, search and prefix checks**:

1. **Children Map**: Each node maps a character to the child node, so any alphabet (including emoji and accents) works.

2. **`putIfAbsent(ch, TrieNode.new)`**: Reuses the existing child or creates one. `TrieNode.new` is a **constructor tear-off**.

3. **End-of-Word Flag**: `isWord` distinguishes complete words from mere prefixes.

4. **Shared Walk**: `contains` and `hasPrefix` both follow characters from the root; they differ only in whether the final node must be a word.

5. **O(L) Operations**: Cost depends only on the length of the word, not on how many words are stored.

---

## ✍️ Autocomplete: Collect Every Word Below a Prefix

```dart
class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isWord = false;
}

class Trie {
  final _root = TrieNode();

  void insert(String word) {
    var node = _root;
    for (final ch in word.split('')) {
      node = node.children.putIfAbsent(ch, TrieNode.new);
    }
    node.isWord = true;
  }

  List<String> suggest(String prefix, {int limit = 10}) {
    var node = _root;
    for (final ch in prefix.split('')) {
      final next = node.children[ch];
      if (next == null) return [];
      node = next;
    }
    final results = <String>[];
    void collect(TrieNode n, StringBuffer path) {
      if (results.length >= limit) return;
      if (n.isWord) results.add(path.toString());
      final keys = n.children.keys.toList()..sort(); // alphabetical suggestions
      for (final ch in keys) {
        path.write(ch);
        collect(n.children[ch]!, path);
        // backtrack: remove the last character
        final s = path.toString();
        path
          ..clear()
          ..write(s.substring(0, s.length - 1));
      }
    }

    collect(node, StringBuffer(prefix));
    return results;
  }
}

void main() {
  final trie = Trie();
  for (final w in ['flutter', 'fluent', 'flute', 'fluffy', 'flow', 'dart', 'flu']) {
    trie.insert(w);
  }
  print(trie.suggest('flu'));           // [flu, fluent, fluffy, flute, flutter]
  print(trie.suggest('flu', limit: 2)); // [flu, fluent]
  print(trie.suggest('fl'));            // [flow, flu, fluent, fluffy, flute, flutter]
  print(trie.suggest('x'));             // []
}
```

**🔍 What This Code Does:**

1. **Walk to the Prefix Node**: O(P) for a prefix of length P.
2. **DFS Below It**: Every word in that subtree starts with the prefix.
3. **Sorted Children**: Visiting children alphabetically gives alphabetical suggestions.
4. **Backtracking**: After exploring a child, remove its character from `path`.
5. **Limit**: Stops early once enough suggestions are found, so huge subtrees don't slow down the UI.

> 💡 Real autocomplete also ranks results by **popularity**: store a count or score at each word node and pick the top suggestions with a **heap**.

---

## ⚡ Array-Based Children for Speed

When the alphabet is small and fixed (like lowercase `a`–`z`), a fixed-size list of 26 children is faster than a map.

```dart
class Node {
  final List<Node?> next = List.filled(26, null);
  bool isWord = false;
  int passCount = 0; // how many words pass through this node
}

class LowercaseTrie {
  final _root = Node();

  void insert(String word) {
    var n = _root;
    for (final unit in word.codeUnits) {
      final i = unit - 97; // 'a' is 97
      n = n.next[i] ??= Node();
      n.passCount++;
    }
    n.isWord = true;
  }

  int countWithPrefix(String prefix) {
    var n = _root;
    for (final unit in prefix.codeUnits) {
      final child = n.next[unit - 97];
      if (child == null) return 0;
      n = child;
    }
    return n.passCount;
  }
}

void main() {
  final t = LowercaseTrie();
  for (final w in ['apple', 'app', 'apply', 'ape', 'bat']) {
    t.insert(w);
  }
  print(t.countWithPrefix('ap'));  // 4
  print(t.countWithPrefix('app')); // 3
  print(t.countWithPrefix('b'));   // 1
  print(t.countWithPrefix('c'));   // 0
}
```

**🔍 What This Code Does:**

1. **Index by Letter**: `unit - 97` maps `'a'..'z'` to `0..25`.
2. **`??=` to Create Children**: `n.next[i] ??= Node()` creates the child only if missing, then returns it.
3. **Prefix Counts**: `passCount` records how many inserted words go through each node, so "how many words start with X" is O(L).
4. **Trade-off**: Fast and simple, but each node reserves 26 slots even if it uses one. Maps are more memory-efficient for sparse or large alphabets.

---

## 🗑️ Deleting Words

Deleting must unmark the word, and optionally **prune** nodes that no longer lead to any word.

```dart
class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isWord = false;
}

void insert(TrieNode root, String w) {
  var n = root;
  for (final ch in w.split('')) {
    n = n.children.putIfAbsent(ch, TrieNode.new);
  }
  n.isWord = true;
}

/// Returns true if `node` can be removed by its parent.
bool delete(TrieNode node, String word, int depth) {
  if (depth == word.length) {
    if (!node.isWord) return false; // word not present
    node.isWord = false;
    return node.children.isEmpty;
  }
  final ch = word[depth];
  final child = node.children[ch];
  if (child == null) return false;
  if (delete(child, word, depth + 1)) {
    node.children.remove(ch); // prune the empty branch
    return !node.isWord && node.children.isEmpty;
  }
  return false;
}

bool contains(TrieNode root, String w) {
  var n = root;
  for (final ch in w.split('')) {
    final next = n.children[ch];
    if (next == null) return false;
    n = next;
  }
  return n.isWord;
}

void main() {
  final root = TrieNode();
  for (final w in ['car', 'cart']) {
    insert(root, w);
  }
  delete(root, 'cart', 0);
  print(contains(root, 'cart')); // false
  print(contains(root, 'car'));  // true (the shared prefix survives)

  delete(root, 'car', 0);
  print(root.children.isEmpty);  // true (everything was pruned)
}
```

**🔍 What This Code Does:**

1. **Recursive Delete**: Walk down to the end of the word and clear `isWord`.
2. **Prune on the Way Back Up**: A child is removed only if it marks no word and has no children left.
3. **Shared Prefixes Survive**: Deleting `cart` keeps `c → a → r` because `car` still needs it.

---

## 🔤 Classic Trie Problems

### Longest common prefix

```dart
String longestCommonPrefix(List<String> words) {
  if (words.isEmpty) return '';
  final root = <String, Map>{};
  for (final w in words) {
    var node = root;
    for (final ch in w.split('')) {
      node = node.putIfAbsent(ch, () => <String, Map>{}) as Map<String, Map>;
    }
    node['\$'] = {}; // end marker
  }
  final prefix = StringBuffer();
  var node = root;
  while (node.length == 1 && !node.containsKey('\$')) {
    final ch = node.keys.first;
    prefix.write(ch);
    node = node[ch] as Map<String, Map>;
  }
  return prefix.toString();
}

void main() {
  print(longestCommonPrefix(['flower', 'flow', 'flight'])); // fl
  print(longestCommonPrefix(['dart', 'darts', 'dartboard'])); // dart
  print(longestCommonPrefix(['dog', 'cat']));               // (empty)
}
```

**🔍 What This Code Does:**

1. **Nested Maps as a Trie**: A quick trie without a node class; `'$'` marks word ends.
2. **Walk While There's One Path**: As long as a node has exactly one child and no word ends there, all words agree on that character.
3. **Stop at a Branch or Word End**: That's where the common prefix ends.

### Replace words with their shortest root

```dart
class Node {
  final Map<String, Node> kids = {};
  bool end = false;
}

String replaceWithRoots(List<String> roots, String sentence) {
  final trie = Node();
  for (final r in roots) {
    var n = trie;
    for (final ch in r.split('')) {
      n = n.kids.putIfAbsent(ch, Node.new);
    }
    n.end = true;
  }

  String shortestRoot(String word) {
    var n = trie;
    for (var i = 0; i < word.length; i++) {
      final next = n.kids[word[i]];
      if (next == null) return word;
      n = next;
      if (n.end) return word.substring(0, i + 1);
    }
    return word;
  }

  return sentence.split(' ').map(shortestRoot).join(' ');
}

void main() {
  print(replaceWithRoots(['cat', 'bat', 'rat'], 'the cattle was rattled by the battery'));
  // the cat was rat by the bat
}
```

**🔍 What This Code Does:**

1. **Insert the Roots**: Each root marks its end node.
2. **Stop at the First Root**: Walking a word, the first `end` node gives the **shortest** matching root.
3. **No Match**: Words with no root prefix are kept unchanged.

---

## 📊 Trie vs Other Structures

| Task | Trie | Hash set | Sorted list + binary search |
|------|------|----------|-----------------------------|
| Exact lookup | O(L) | O(L) average (hashing reads every char) | O(L log n) |
| "Any word starts with P?" | **O(P)** | ❌ O(n × P) scan | O(P log n) |
| List all words with prefix P | **O(P + output)** | ❌ scan all | O(P log n + output) |
| Count words with prefix | **O(P)** with counts | ❌ | O(P log n) |
| Memory | Can be large (many nodes) | Compact | Compact |

> 💡 Use a trie when **prefixes** matter: autocomplete, spell checkers, IP routing tables, word games (Boggle, Scrabble), and T9-style keypads.

---

## ⚠️ Common Mistakes

### 1. Forgetting the end-of-word flag

Without `isWord`, inserting `cart` would make `car` look like a stored word, because its path exists.

### 2. Using `contains` when you meant `hasPrefix`

`contains('ca')` is false (not a word) while `hasPrefix('ca')` is true. Pick the right one for the question.

### 3. Array children with unexpected characters

A 26-slot node crashes (RangeError) on uppercase letters, digits or spaces. Normalize input (`toLowerCase()`, filter) or use a map.

### 4. Ignoring memory

A trie of a million long, dissimilar words can have tens of millions of nodes. **Compressed tries** (radix trees) merge chains of single-child nodes into one edge to save space.

---

## 🧪 Try It Yourself

1. Add `remove(String word)` to the `Trie` class using the pruning approach.
2. Add a `frequency` field and make `suggest` return the **top 3 most popular** words for a prefix.
3. **Word search with wildcards**: support `.` matching any single letter (e.g. `c.t` matches `cat` and `cut`).
4. Build a **T9 keypad** helper: map digits to letters and find all dictionary words for `228` (`bat`, `cat`, `act`).

```dart
class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isWord = false;
}

bool matches(TrieNode node, String pattern, [int i = 0]) {
  if (i == pattern.length) return node.isWord;
  final ch = pattern[i];
  if (ch == '.') {
    return node.children.values.any((child) => matches(child, pattern, i + 1));
  }
  final next = node.children[ch];
  return next != null && matches(next, pattern, i + 1);
}

void main() {
  final root = TrieNode();
  for (final w in ['cat', 'cut', 'cot', 'car']) {
    var n = root;
    for (final c in w.split('')) {
      n = n.children.putIfAbsent(c, TrieNode.new);
    }
    n.isWord = true;
  }
  print(matches(root, 'c.t')); // true
  print(matches(root, '..r')); // true
  print(matches(root, 'c.p')); // false
}
```

**🔍 What This Code Does:**

1. **Normal Characters**: Follow exactly one child.
2. **Wildcard `.`**: Try **every** child; `any` returns true if one branch matches.
3. **Word End Check**: The pattern only matches if it ends exactly on a word node.

---

## 📌 Key Takeaways

- ✅ A **trie** stores strings as paths of characters; shared prefixes share nodes.
- ✅ Each node has **children** (a map or a fixed array) and an **end-of-word** flag.
- ✅ Insert, search and prefix checks cost **O(L)**, independent of the number of words.
- ✅ **Autocomplete** = walk to the prefix node, then DFS to collect words (limit and rank them).
- ✅ Store **counts** in nodes to answer "how many words start with P?" in O(P).
- ✅ Deletion can **prune** branches that no longer lead to words.
- ✅ Tries trade **memory** for powerful **prefix** queries; radix trees compress them.

**Next up:** 🕸️ **Module 5: Representing Graphs**: when things connect in any direction, not just parent to child.
