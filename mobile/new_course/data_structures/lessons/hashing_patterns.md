# Hashing Patterns

Imagine you're a **detective** 🕵️ with a notebook.

- Every time you meet someone, you jot their name down. Later, *"Have I met this person before?"* takes one glance. 📒
- You tally how many times each suspect was spotted near the scene. 📊
- You group clues by the day they were found. 🗂️

The notebook doesn't solve the case by itself, but it turns slow questions into instant ones.

👉 That's the idea behind **hashing patterns**:

> Use a **Set** or **Map** to remember what you've already seen, so each new question about the past costs **O(1)** instead of a scan. This turns many **O(n²)** brute-force solutions into **O(n)**.

This lesson collects the patterns you'll use again and again.

---

## 🧭 The Pattern Menu

| Pattern | Structure | Typical question |
|---------|-----------|------------------|
| 👀 **Seen set** | `Set<T>` | "Have I seen this before?" |
| 📊 **Frequency count** | `Map<T, int>` | "How many times does each thing appear?" |
| 🔍 **Complement lookup** | `Map<T, int>` (value → index) | "Is there an earlier item that pairs with this one?" |
| 🗂️ **Grouping** | `Map<K, List<T>>` | "Which items share a property?" |
| 🧮 **Prefix + map** | `Map<int, int>` | "How many subarrays sum to k?" |
| 🪞 **Canonical key** | `Map<String, ...>` | "Are these the same thing in a different form?" |
| 🔗 **Index map** | `Map<K, T>` | "Find the record with this id instantly" |

---

## 👀 Pattern 1: The Seen Set

### Contains duplicate

```dart
bool hasDuplicate(List<int> nums) {
  final seen = <int>{};
  for (final n in nums) {
    if (!seen.add(n)) return true; // add returns false if already present
  }
  return false;
}

void main() {
  print(hasDuplicate([1, 2, 3, 1])); // true
  print(hasDuplicate([1, 2, 3, 4])); // false
}
```

**🔍 What This Code Does:**

1. **One Pass**: Each number is checked against everything seen so far.
2. **`Set.add` Doubles as a Check**: It returns `false` when the item was already present.
3. **Early Exit**: Stops at the first duplicate.
4. **O(n) Time, O(n) Space**: Versus O(n²) comparing every pair.

### First repeated character

```dart
String? firstRepeat(String s) {
  final seen = <String>{};
  for (final ch in s.split('')) {
    if (!seen.add(ch)) return ch;
  }
  return null;
}

void main() {
  print(firstRepeat('swiss')); // s
  print(firstRepeat('dart'));  // null
}
```

**🔍 What This Code Does:**

1. **Order Matters**: The first character whose second occurrence appears earliest is returned.
2. **Nullable Return**: `String?` signals "no repeat found".

### Longest consecutive sequence

```dart
int longestConsecutive(List<int> nums) {
  final set = nums.toSet();
  var best = 0;
  for (final n in set) {
    if (set.contains(n - 1)) continue; // only start counting at a sequence's beginning
    var length = 1;
    while (set.contains(n + length)) {
      length++;
    }
    if (length > best) best = length;
  }
  return best;
}

void main() {
  print(longestConsecutive([100, 4, 200, 1, 3, 2])); // 4 (1, 2, 3, 4)
}
```

**🔍 What This Code Does:**

1. **Set for O(1) Membership**: Every "is n+1 present?" check is instant.
2. **Only Start at Beginnings**: If `n − 1` exists, `n` is in the middle of a run; skip it.
3. **Count Upward**: From each beginning, walk up while the next number exists.
4. **O(n) Overall**: Each number is part of exactly one upward walk, even though there's a nested loop. Sorting would cost O(n log n).

---

## 📊 Pattern 2: Frequency Counting

```dart
Map<String, int> countWords(String text) {
  final counts = <String, int>{};
  for (final word in text.toLowerCase().split(RegExp(r'\W+'))) {
    if (word.isEmpty) continue;
    counts[word] = (counts[word] ?? 0) + 1;
  }
  return counts;
}

void main() {
  final counts = countWords('The cat and the hat. The END!');
  print(counts); // {the: 3, cat: 1, and: 1, hat: 1, end: 1}

  // Top 2 most common words
  final top = counts.entries.toList()
    ..sort((a, b) => b.value.compareTo(a.value));
  print(top.take(2).map((e) => '${e.key}=${e.value}').toList()); // [the=3, cat=1]
}
```

**🔍 What This Code Does:**

1. **Normalize**: Lowercase the text and split on non-word characters (`\W+`).
2. **Count**: `(counts[word] ?? 0) + 1` starts new words at 1.
3. **Rank**: Sort the entries by count, descending.
4. **O(n)** to count, plus O(u log u) to sort `u` unique words.

### Majority element

```dart
int? majority(List<int> nums) {
  final counts = <int, int>{};
  for (final n in nums) {
    final c = (counts[n] ?? 0) + 1;
    if (c > nums.length ~/ 2) return n; // appears more than half the time
    counts[n] = c;
  }
  return null;
}

void main() {
  print(majority([2, 2, 1, 1, 1, 2, 2])); // 2
  print(majority([1, 2, 3]));             // null
}
```

**🔍 What This Code Does:**

1. **Running Counts**: Update each number's count as we go.
2. **Early Answer**: Once a count passes half the length, that number is the majority.
3. **O(n)**: One pass with a map.

### Valid anagram with one map

```dart
bool isAnagram(String a, String b) {
  if (a.length != b.length) return false;
  final counts = <String, int>{};
  for (var i = 0; i < a.length; i++) {
    counts[a[i]] = (counts[a[i]] ?? 0) + 1;
    counts[b[i]] = (counts[b[i]] ?? 0) - 1;
  }
  return counts.values.every((c) => c == 0);
}

void main() {
  print(isAnagram('listen', 'silent')); // true
  print(isAnagram('apple', 'papel'));   // true
  print(isAnagram('rat', 'tar!'));      // false
}
```

**🔍 What This Code Does:**

1. **Add and Subtract Together**: Characters from `a` add 1, from `b` subtract 1.
2. **Balanced = Anagram**: Every count must end at zero.
3. **`every`**: Returns true only if the test passes for all values.

---

## 🔍 Pattern 3: Complement Lookup (Two Sum)

**Problem:** Return the indexes of two numbers that add up to `target`. The list is **not** sorted.

```dart
(int, int)? twoSum(List<int> nums, int target) {
  final indexOf = <int, int>{}; // value → index
  for (var i = 0; i < nums.length; i++) {
    final need = target - nums[i];
    final j = indexOf[need];
    if (j != null) return (j, i);
    indexOf[nums[i]] = i; // store AFTER checking, so we don't pair i with itself
  }
  return null;
}

void main() {
  print(twoSum([2, 7, 11, 15], 9)); // (0, 1)
  print(twoSum([3, 2, 4], 6));      // (1, 2)
  print(twoSum([3, 3], 6));         // (0, 1)
  print(twoSum([1, 2], 10));        // null
}
```

**🔍 What This Code Does:**

1. **The Complement**: For each number `x`, the partner we need is `target − x`.
2. **Look Back With a Map**: If that partner appeared earlier, its index is in `indexOf`.
3. **Check Before Storing**: Storing after the check stops `3 + 3 = 6` from pairing an element with itself, while still handling two different 3s.
4. **O(n)**: Versus O(n²) checking every pair, or O(n log n) sorting + two pointers (which loses the original indexes).

### Count pairs with a given difference

```dart
int pairsWithDiff(List<int> nums, int k) {
  final counts = <int, int>{};
  var pairs = 0;
  for (final n in nums) {
    pairs += (counts[n - k] ?? 0) + (k == 0 ? 0 : counts[n + k] ?? 0);
    counts[n] = (counts[n] ?? 0) + 1;
  }
  return pairs;
}

void main() {
  print(pairsWithDiff([1, 5, 3, 4, 2], 2)); // 3: (1,3), (5,3), (4,2)
}
```

**🔍 What This Code Does:**

1. **Two Possible Partners**: A partner of `n` with difference `k` is either `n − k` or `n + k`.
2. **Count, Then Record**: Each pair is counted once, when its second element arrives.
3. **Special Case `k == 0`**: Avoids counting the same partner twice.

---

## 🗂️ Pattern 4: Grouping

### Group anagrams with a canonical key

```dart
List<List<String>> groupAnagrams(List<String> words) {
  final groups = <String, List<String>>{};
  for (final w in words) {
    final key = (w.split('')..sort()).join(); // canonical form
    groups.putIfAbsent(key, () => []).add(w);
  }
  return groups.values.toList();
}

void main() {
  print(groupAnagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat']));
  // [[eat, tea, ate], [tan, nat], [bat]]
}
```

**🔍 What This Code Does:**

1. **Canonical Key**: Sorting a word's letters gives the same key for all its anagrams (`'eat'`, `'tea'`, `'ate'` → `'aet'`).
2. **Group by Key**: `putIfAbsent` creates each group's list the first time.
3. **Insertion Order**: Groups appear in the order their first word appeared.
4. **O(n × L log L)** for `n` words of length `L`.

### Group by a property with `fold`

```dart
void main() {
  final files = ['main.dart', 'logo.png', 'app.dart', 'readme.md', 'icon.png'];

  final byExt = files.fold<Map<String, List<String>>>({}, (acc, f) {
    final ext = f.split('.').last;
    (acc[ext] ??= []).add(f);
    return acc;
  });

  print(byExt); // {dart: [main.dart, app.dart], png: [logo.png, icon.png], md: [readme.md]}
}
```

**🔍 What This Code Does:**

1. **`fold` With a Map Accumulator**: Builds the grouping in one expression.
2. **`??=` Shortcut**: `(acc[ext] ??= [])` creates the list if missing and returns it.
3. **Any Property Works**: Group users by country, orders by status, logs by level.

---

## 🧮 Pattern 5: Prefix Sum + Map

From **Prefix Sums**: count subarrays with sum `k`, even with negative numbers.

```dart
int countSubarrays(List<int> nums, int k) {
  final seen = <int, int>{0: 1};
  var running = 0, count = 0;
  for (final x in nums) {
    running += x;
    count += seen[running - k] ?? 0;
    seen[running] = (seen[running] ?? 0) + 1;
  }
  return count;
}

void main() {
  print(countSubarrays([1, 2, 1, -1, 2], 3)); // 3: [1, 2], [2, 1], [1, 2, 1, -1]
}
```

**🔍 What This Code Does:**

1. **Running Prefix**: The sum of everything up to the current position.
2. **Complement of a Prefix**: A subarray ending here sums to `k` if an earlier prefix equals `running − k`.
3. **Counts, Not Indexes**: The map stores how many times each prefix value appeared.

---

## 🪞 Pattern 6: Canonical Forms and Bijections

### Isomorphic strings

Two strings are isomorphic if characters in one can be consistently replaced to get the other (`'egg'` ↔ `'add'`).

```dart
bool isIsomorphic(String s, String t) {
  if (s.length != t.length) return false;
  final sToT = <String, String>{};
  final tToS = <String, String>{};
  for (var i = 0; i < s.length; i++) {
    final a = s[i], b = t[i];
    if ((sToT[a] ?? b) != b || (tToS[b] ?? a) != a) return false;
    sToT[a] = b;
    tToS[b] = a;
  }
  return true;
}

void main() {
  print(isIsomorphic('egg', 'add'));     // true
  print(isIsomorphic('foo', 'bar'));     // false
  print(isIsomorphic('paper', 'title')); // true
  print(isIsomorphic('ab', 'aa'));       // false
}
```

**🔍 What This Code Does:**

1. **Two Maps**: One for each direction, ensuring the mapping is one-to-one.
2. **Consistency Check**: If a character was mapped before, it must map to the same partner again.
3. **Why Two?**: With only `sToT`, `'ab'` → `'aa'` would wrongly pass (both `a` and `b` map to `a`).

### Word pattern

```dart
bool wordPattern(String pattern, String sentence) {
  final words = sentence.split(' ');
  if (words.length != pattern.length) return false;
  final seen = <String, String>{};
  for (var i = 0; i < words.length; i++) {
    final existing = seen.putIfAbsent(pattern[i], () => words[i]);
    if (existing != words[i]) return false;
  }
  return seen.values.toSet().length == seen.length; // no two letters share a word
}

void main() {
  print(wordPattern('abba', 'dog cat cat dog')); // true
  print(wordPattern('abba', 'dog dog dog dog')); // false
}
```

**🔍 What This Code Does:**

1. **`putIfAbsent` Returns the Existing Value**: Lets us check consistency in one line.
2. **Uniqueness Check**: Different letters must map to different words.

---

## 🔗 Pattern 7: Index Maps for Fast Joins

Joining two lists by a shared key with nested loops is O(n × m). A map makes it O(n + m).

```dart
void main() {
  final users = [
    (id: 1, name: 'Ada'),
    (id: 2, name: 'Linus'),
    (id: 3, name: 'Grace'),
  ];
  final orders = [
    (userId: 2, item: 'Keyboard'),
    (userId: 1, item: 'Mouse'),
    (userId: 2, item: 'Monitor'),
    (userId: 9, item: 'Lamp'),
  ];

  final nameById = {for (final u in users) u.id: u.name}; // O(n)

  for (final o in orders) {                               // O(m)
    final name = nameById[o.userId] ?? 'unknown user';
    print('$name bought ${o.item}');
  }
}
```

**🔍 What This Code Does:**

1. **Build an Index Once**: A map from id to name in O(n).
2. **Look Up Per Order**: Each order finds its user in O(1).
3. **Handles Missing Keys**: `?? 'unknown user'` covers orders whose user doesn't exist.
4. **This Is a Hash Join**: The same idea databases use to join tables.

---

## 🧠 How to Spot a Hashing Pattern

Ask yourself:

1. Am I scanning the list **inside** another loop to find something? → Build a Set/Map first.
2. Am I asking **"have I seen X?"** → Seen set.
3. Am I asking **"how many X?"** → Frequency map.
4. Am I looking for a **partner** that satisfies an equation? → Complement map.
5. Do several items **belong together**? → Grouping map with a canonical key.

> 💡 The trade-off is always the same: spend **O(n) memory** to save **time**.

---

## ⚠️ Common Mistakes

### 1. Storing before checking in two-sum

```dart
void main() {
  final nums = [3, 4];
  const target = 6;
  final seen = <int, int>{};
  for (var i = 0; i < nums.length; i++) {
    seen[nums[i]] = i; // ❌ stored first
    final j = seen[target - nums[i]];
    if (j != null) {
      print('pair: ($j, $i)'); // wrongly pairs index 0 with itself: (0, 0)
      break;
    }
  }
}
```

**🔍 What This Code Does:**

1. **The Bug**: `3` is stored, then `6 − 3 = 3` is found: the element pairs with itself.
2. **The Fix**: Check for the complement **before** storing the current value.

### 2. Using a List where a Set belongs

`list.contains` inside a loop is a hidden O(n²). Convert to a Set first with `toSet()`.

### 3. Forgetting to normalize keys

`'Dart'`, `'dart'` and `' dart '` are three different keys. Trim and lowercase when they should count as the same.

### 4. Iterating a HashMap and expecting order

If the output must be ordered, use the default `{}` map (insertion order) or sort the entries.

---

## 🧪 Try It Yourself

1. **Intersection of two arrays** (with duplicates): `[1, 2, 2, 1]` and `[2, 2]` → `[2, 2]`.
2. **First unique character index** in a string, or −1.
3. **Ransom note**: can `note` be built from the letters in `magazine` (each letter used once)?
4. **Happy number**: repeatedly replace a number with the sum of the squares of its digits; detect a loop with a seen set.

```dart
bool isHappy(int n) {
  final seen = <int>{};
  while (n != 1 && seen.add(n)) {
    var next = 0;
    while (n > 0) {
      final d = n % 10;
      next += d * d;
      n ~/= 10;
    }
    n = next;
  }
  return n == 1;
}

void main() {
  print(isHappy(19)); // true: 19 → 82 → 68 → 100 → 1
  print(isHappy(2));  // false: falls into a loop
}
```

**🔍 What This Code Does:**

1. **Seen Set Detects Loops**: If a number repeats, we're in a cycle that never reaches 1.
2. **`seen.add(n)` in the Condition**: Records the number and stops when it was already seen.
3. **Digit Squares**: `n % 10` and `n ~/= 10` peel off digits.

---

## 📌 Key Takeaways

- ✅ **Seen sets** answer "have I seen this?" in O(1), turning duplicate checks into O(n).
- ✅ **Frequency maps** count occurrences in one pass; use them for anagrams, majority and top-k.
- ✅ **Complement maps** solve two-sum style problems in O(n): **check before storing**.
- ✅ **Grouping maps** with a **canonical key** collect related items (anagrams, extensions).
- ✅ **Prefix sum + map** counts subarrays with a target sum, even with negatives.
- ✅ **Two maps** enforce one-to-one mappings (isomorphic strings, word patterns).
- ✅ **Index maps** turn O(n × m) joins into O(n + m) hash joins.
- ✅ The universal trade-off: **memory for speed**.

**Next up:** 🌳 **Module 4: Tree Fundamentals**: roots, leaves, depth and height.
