QUESTIONS = [
    mcq(r"""
What is the core trade-off behind hashing patterns?
""", ["Spend O(n) extra memory to make lookups O(1)", "Spend more time to save memory",
       "Sort the data to avoid using memory", "Use recursion to avoid loops"],
        "Spend O(n) extra memory to make lookups O(1)"),

    mcq(r"""
Which pattern answers "have I seen this before?"
""", ["A seen Set", "A frequency Map", "A grouping Map", "A prefix sum"], "A seen Set"),

    mcq(r"""
Which pattern answers "how many times does each item appear?"
""", ["A frequency Map", "A seen Set", "Two pointers", "A stack"], "A frequency Map"),

    mcq(r"""
What does this print?

```dart
bool hasDup(List<int> a) {
  final seen = <int>{};
  for (final x in a) {
    if (!seen.add(x)) return true;
  }
  return false;
}

void main() {
  print(hasDup([4, 5, 6, 5]));
}
```
""", ["true", "false", "5", "null"], "true"),

    mcq(r"""
What is the time complexity of duplicate detection with a seen set?
""", ["O(n)", "O(n²)", "O(n log n)", "O(1)"], "O(n)"),

    mcq(r"""
What does this print?

```dart
String? firstRepeat(String s) {
  final seen = <String>{};
  for (final c in s.split('')) {
    if (!seen.add(c)) return c;
  }
  return null;
}

void main() {
  print(firstRepeat('abcbad'));
}
```
""", ["b", "a", "d", "null"], "b"),

    mcq(r"""
What does this print?

```dart
int longest(List<int> nums) {
  final set = nums.toSet();
  var best = 0;
  for (final n in set) {
    if (set.contains(n - 1)) continue;
    var len = 1;
    while (set.contains(n + len)) {
      len++;
    }
    if (len > best) best = len;
  }
  return best;
}

void main() {
  print(longest([10, 5, 12, 3, 11, 4, 13]));
}
```
""", ["4", "3", "7", "2"], "4"),

    mcq(r"""
In the longest-consecutive-sequence algorithm, why skip numbers where `n - 1` exists?
""", ["They're in the middle of a run, so counting from them would repeat work",
       "They're duplicates", "They're negative", "To sort the set"],
        "They're in the middle of a run, so counting from them would repeat work"),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = <String, int>{};
  for (final w in 'red blue red green red'.split(' ')) {
    counts[w] = (counts[w] ?? 0) + 1;
  }
  print(counts['red']);
}
```
""", ["3", "1", "5", "null"], "3"),

    fill(r"""
Increment a count, starting from 0 when the key is missing:

```dart
void main() {
  final counts = <String, int>{};
  counts['a'] = (counts['a'] %fill% 0) + 1;
  print(counts); // {a: 1}
}
```
""", "??"),

    mcq(r"""
What does this print?

```dart
int? majority(List<int> a) {
  final c = <int, int>{};
  for (final x in a) {
    final n = (c[x] ?? 0) + 1;
    if (n > a.length ~/ 2) return x;
    c[x] = n;
  }
  return null;
}

void main() {
  print(majority([3, 1, 3, 3, 2]));
}
```
""", ["3", "1", "2", "null"], "3"),

    mcq(r"""
What does this print?

```dart
bool isAnagram(String a, String b) {
  if (a.length != b.length) return false;
  final c = <String, int>{};
  for (var i = 0; i < a.length; i++) {
    c[a[i]] = (c[a[i]] ?? 0) + 1;
    c[b[i]] = (c[b[i]] ?? 0) - 1;
  }
  return c.values.every((v) => v == 0);
}

void main() {
  print(isAnagram('night', 'thing'));
  print(isAnagram('aab', 'abb'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
In two-sum, what value do you look up for the current number x?
""", ["target - x", "target + x", "x * 2", "x - target"], "target - x"),

    mcq(r"""
In two-sum with a map, what does the map store?
""", ["value → index of numbers seen so far", "index → value", "pairs found so far",
       "counts of targets"], "value → index of numbers seen so far"),

    mcq(r"""
What does this print?

```dart
(int, int)? twoSum(List<int> nums, int target) {
  final idx = <int, int>{};
  for (var i = 0; i < nums.length; i++) {
    final j = idx[target - nums[i]];
    if (j != null) return (j, i);
    idx[nums[i]] = i;
  }
  return null;
}

void main() {
  print(twoSum([5, 1, 7, 3], 8));
}
```
""", ["(1, 2)", "(0, 3)", "(2, 1)", "null"], "(1, 2)"),

    mcq(r"""
Why must two-sum check for the complement BEFORE storing the current number?
""", ["So an element can't pair with itself (e.g. 3 + 3 = 6 with one 3)",
       "Maps can't store values twice", "To make it O(log n)", "It doesn't matter"],
        "So an element can't pair with itself (e.g. 3 + 3 = 6 with one 3)"),

    mcq(r"""
What does this print?

```dart
(int, int)? twoSum(List<int> nums, int target) {
  final idx = <int, int>{};
  for (var i = 0; i < nums.length; i++) {
    final j = idx[target - nums[i]];
    if (j != null) return (j, i);
    idx[nums[i]] = i;
  }
  return null;
}

void main() {
  print(twoSum([3, 3], 6));
  print(twoSum([3], 6));
}
```
""", ["(0, 1) then null", "(0, 0) then (0, 0)", "null then null", "(0, 1) then (0, 0)"],
        "(0, 1) then null"),

    mcq(r"""
Why is the hash-map two-sum better than sorting + two pointers when you need the original indexes?
""", ["Sorting rearranges elements and loses their original positions",
       "Sorting is O(n²)", "Two pointers don't work on ints", "Maps are always faster than sorting"],
        "Sorting rearranges elements and loses their original positions"),

    mcq(r"""
What is the complexity of hash-map two-sum?
""", ["O(n) time, O(n) space", "O(n²) time, O(1) space", "O(n log n) time, O(1) space",
       "O(1) time, O(n) space"], "O(n) time, O(n) space"),

    mcq(r"""
What is a canonical key?
""", ["A normalized form that's identical for items that should be grouped together",
       "The first key inserted", "A key with the smallest hash", "A random unique id"],
        "A normalized form that's identical for items that should be grouped together"),

    mcq(r"""
What canonical key groups anagrams together?
""", ["The word's letters sorted", "The word's length", "The word reversed",
       "The first letter"], "The word's letters sorted"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(('tea'.split('')..sort()).join());
}
```
""", ["aet", "tea", "eat", "tae"], "aet"),

    mcq(r"""
What does this print?

```dart
void main() {
  final groups = <String, List<String>>{};
  for (final w in ['eat', 'tea', 'tan', 'nat']) {
    final key = (w.split('')..sort()).join();
    groups.putIfAbsent(key, () => []).add(w);
  }
  print(groups.values.toList());
}
```
""", ["[[eat, tea], [tan, nat]]", "[[eat, tan], [tea, nat]]", "[[eat], [tea], [tan], [nat]]",
       "[eat, tea, tan, nat]"], "[[eat, tea], [tan, nat]]"),

    mcq(r"""
What does this print?

```dart
void main() {
  final files = ['a.dart', 'b.png', 'c.dart'];
  final byExt = <String, List<String>>{};
  for (final f in files) {
    (byExt[f.split('.').last] ??= []).add(f);
  }
  print(byExt['dart']);
}
```
""", ["[a.dart, c.dart]", "[a.dart]", "[b.png]", "null"], "[a.dart, c.dart]"),

    fill(r"""
Create the list if missing and add to it in one expression:

```dart
void main() {
  final groups = <String, List<int>>{};
  (groups['x'] %fill% []).add(1);
  print(groups); // {x: [1]}
}
```
""", "??="),

    mcq(r"""
What does this print?

```dart
void main() {
  final total = [1, 2, 3].fold<Map<String, int>>({}, (acc, n) {
    final key = n.isEven ? 'even' : 'odd';
    acc[key] = (acc[key] ?? 0) + n;
    return acc;
  });
  print(total);
}
```
""", ["{odd: 4, even: 2}", "{even: 2, odd: 4}", "{odd: 2, even: 1}", "{odd: 6}"],
        "{odd: 4, even: 2}"),

    mcq(r"""
What does this print?

```dart
int count(List<int> nums, int k) {
  final seen = <int, int>{0: 1};
  var run = 0, c = 0;
  for (final x in nums) {
    run += x;
    c += seen[run - k] ?? 0;
    seen[run] = (seen[run] ?? 0) + 1;
  }
  return c;
}

void main() {
  print(count([2, 2, 2], 4));
}
```
""", ["2", "1", "3", "0"], "2"),

    mcq(r"""
What are isomorphic strings?
""", ["Strings where characters can be consistently replaced one-to-one to get the other",
       "Strings with the same letters", "Strings of equal length", "Palindromes"],
        "Strings where characters can be consistently replaced one-to-one to get the other"),

    mcq(r"""
Why does the isomorphic check need TWO maps?
""", ["To ensure the mapping is one-to-one in both directions",
       "One map can't store strings", "To store indexes and values",
       "For speed only"], "To ensure the mapping is one-to-one in both directions"),

    mcq(r"""
Are 'ab' and 'aa' isomorphic?
""", ["No: a and b would both have to map to a", "Yes", "Only if case-insensitive",
       "It depends on hashing"], "No: a and b would both have to map to a"),

    mcq(r"""
What does this print?

```dart
bool iso(String s, String t) {
  final st = <String, String>{}, ts = <String, String>{};
  for (var i = 0; i < s.length; i++) {
    final a = s[i], b = t[i];
    if ((st[a] ?? b) != b || (ts[b] ?? a) != a) return false;
    st[a] = b;
    ts[b] = a;
  }
  return true;
}

void main() {
  print(iso('egg', 'add'));
  print(iso('foo', 'bar'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What does `map.putIfAbsent(k, f)` return when k already exists?
""", ["The existing value", "The new value from f", "null", "true"], "The existing value"),

    mcq(r"""
What does this print?

```dart
bool wordPattern(String p, String s) {
  final words = s.split(' ');
  if (words.length != p.length) return false;
  final seen = <String, String>{};
  for (var i = 0; i < words.length; i++) {
    if (seen.putIfAbsent(p[i], () => words[i]) != words[i]) return false;
  }
  return seen.values.toSet().length == seen.length;
}

void main() {
  print(wordPattern('aba', 'cat dog cat'));
  print(wordPattern('ab', 'cat cat'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
Joining n users and m orders by id with nested loops costs O(n × m). What does an index map make it?
""", ["O(n + m)", "O(n log m)", "O(1)", "O(n²)"], "O(n + m)"),

    mcq(r"""
What does this print?

```dart
void main() {
  final users = [(id: 1, name: 'Ada'), (id: 2, name: 'Bob')];
  final byId = {for (final u in users) u.id: u.name};
  print(byId[3] ?? 'unknown');
}
```
""", ["unknown", "null", "Bob", "It throws an error"], "unknown"),

    mcq(r"""
What is a hash join?
""", ["Building a map from one dataset's key, then looking up each record of the other",
       "Concatenating two lists", "Sorting both lists and merging", "Hashing two strings together"],
        "Building a map from one dataset's key, then looking up each record of the other"),

    mcq(r"""
Which hidden O(n²) pattern is fixed by converting a List to a Set?
""", ["Calling list.contains inside a loop", "Calling list.add inside a loop",
       "Reading list.length inside a loop", "Iterating with for-in"],
        "Calling list.contains inside a loop"),

    mcq(r"""
Why should you normalize keys like ' Dart ' and 'dart' before counting?
""", ["Otherwise they're treated as different keys", "Maps reject spaces",
       "To make hashing faster", "Normalization isn't needed"],
        "Otherwise they're treated as different keys"),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = <String, int>{};
  for (final w in ['Dart', ' dart', 'DART ']) {
    final k = w.trim().toLowerCase();
    counts[k] = (counts[k] ?? 0) + 1;
  }
  print(counts);
}
```
""", ["{dart: 3}", "{Dart: 1, dart: 1, DART: 1}", "{dart: 1}", "{}"], "{dart: 3}"),

    mcq(r"""
What does this print?

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
  print(isHappy(7));
  print(isHappy(4));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
In the happy-number check, what does the seen set detect?
""", ["A cycle that will never reach 1", "Duplicate digits", "Negative numbers",
       "Numbers larger than 100"], "A cycle that will never reach 1"),

    mcq(r"""
What does this print?

```dart
void main() {
  final a = [1, 2, 2, 3];
  final b = [2, 2, 4];
  final counts = <int, int>{};
  for (final x in a) {
    counts[x] = (counts[x] ?? 0) + 1;
  }
  final out = <int>[];
  for (final x in b) {
    final c = counts[x] ?? 0;
    if (c > 0) {
      out.add(x);
      counts[x] = c - 1;
    }
  }
  print(out);
}
```
""", ["[2, 2]", "[2]", "[2, 2, 4]", "[1, 2, 3, 4]"], "[2, 2]"),

    mcq(r"""
What does this print?

```dart
bool canBuild(String note, String magazine) {
  final c = <String, int>{};
  for (final ch in magazine.split('')) {
    c[ch] = (c[ch] ?? 0) + 1;
  }
  for (final ch in note.split('')) {
    final left = (c[ch] ?? 0) - 1;
    if (left < 0) return false;
    c[ch] = left;
  }
  return true;
}

void main() {
  print(canBuild('aab', 'baa'));
  print(canBuild('aa', 'ab'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    order(r"""
Complete the seen-set duplicate check:

```dart
bool hasDup(List<int> nums) {
  final seen = <int>%order%;
  for (final n in nums) {
    if (%order%seen.%order%(n)) return true;
  }
  return false;
}
```
""", ["{}", "!", "add", "[]", "contains", "remove"], ["{}", "!", "add"]),

    order(r"""
Complete the two-sum loop:

```dart
for (var i = 0; i < nums.length; i++) {
  final j = seen[target %order% nums[i]];
  if (j %order% null) return (j, i);
  seen[nums[i]] = %order%;
}
```
""", ["-", "!=", "i", "+", "==", "j"], ["-", "!=", "i"]),

    mcq(r"""
What does this print?

```dart
void main() {
  final words = ['b', 'a', 'b', 'c', 'b', 'a'];
  final counts = <String, int>{};
  for (final w in words) {
    counts[w] = (counts[w] ?? 0) + 1;
  }
  final top = counts.entries.reduce((x, y) => y.value > x.value ? y : x);
  print('${top.key} ${top.value}');
}
```
""", ["b 3", "a 2", "c 1", "b 2"], "b 3"),

    mcq(r"""
What does `values.every((v) => v == 0)` return for an empty map's values?
""", ["true", "false", "null", "It throws an error"], "true"),

    mcq(r"""
Which pattern finds "number of subarrays with sum k" when values can be negative?
""", ["Prefix sum + hash map", "Sliding window", "Seen set only", "Sorting + binary search"],
        "Prefix sum + hash map"),

    mcq(r"""
What does this print?

```dart
void main() {
  final seen = <int>{};
  final unique = [4, 1, 4, 2, 1].where(seen.add).toList();
  print(unique);
}
```
""", ["[4, 1, 2]", "[4, 1, 4, 2, 1]", "[1, 2, 4]", "[4, 1]"], "[4, 1, 2]"),

    mcq(r"""
Why does `where(seen.add)` remove duplicates while keeping order?
""", ["add returns true only the first time each value is seen",
       "where sorts the values", "Sets keep duplicates out of lists automatically",
       "add always returns true"],
        "add returns true only the first time each value is seen"),

    mcq(r"""
What does this print?

```dart
void main() {
  final first = <String, int>{};
  final s = 'loveleetcode';
  for (var i = 0; i < s.length; i++) {
    first.putIfAbsent(s[i], () => i);
  }
  print(first['e']);
}
```
""", ["1", "3", "4", "null"], "3"),

    mcq(r"""
Which of these is the best first step for "find the first unique character"?
""", ["Count every character's frequency in a map", "Sort the string",
       "Reverse the string", "Use binary search"],
        "Count every character's frequency in a map"),

    mcq(r"""
What does this print?

```dart
int firstUnique(String s) {
  final c = <String, int>{};
  for (final ch in s.split('')) {
    c[ch] = (c[ch] ?? 0) + 1;
  }
  for (var i = 0; i < s.length; i++) {
    if (c[s[i]] == 1) return i;
  }
  return -1;
}

void main() {
  print(firstUnique('aabbcdd'));
  print(firstUnique('aabb'));
}
```
""", ["4 then -1", "2 then -1", "4 then 0", "c then -1"], "4 then -1"),

    mcq(r"""
What does this print?

```dart
int pairsWithDiff(List<int> a, int k) {
  final c = <int, int>{};
  var pairs = 0;
  for (final n in a) {
    pairs += (c[n - k] ?? 0) + (c[n + k] ?? 0);
    c[n] = (c[n] ?? 0) + 1;
  }
  return pairs;
}

void main() {
  print(pairsWithDiff([1, 3, 5], 2));
}
```
""", ["2", "3", "1", "0"], "2"),
]
