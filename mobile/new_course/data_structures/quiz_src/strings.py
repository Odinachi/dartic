QUESTIONS = [
    mcq(r"""
What does it mean that Dart strings are immutable?
""", ["Once created, a string's characters can never change",
       "Strings can't be stored in variables", "Strings are always constants",
       "Strings can't be compared"], "Once created, a string's characters can never change"),

    mcq(r"""
What does this print?

```dart
void main() {
  var s = 'dart';
  final t = s;
  s = s.toUpperCase();
  print(t);
}
```
""", ["dart", "DART", "null", "It throws an error"], "dart"),

    mcq(r"""
What happens with `word[0] = 'b';` when `word` is a String?
""", ["It doesn't compile: String has no []= operator", "It replaces the first letter",
       "It throws at runtime", "It appends 'b'"],
        "It doesn't compile: String has no []= operator"),

    mcq(r"""
What is the cost of reading `s[i]`?
""", ["O(1)", "O(n)", "O(log n)", "O(i)"], "O(1)"),

    mcq(r"""
What is the cost of `s.substring(a, b)`?
""", ["O(b − a), because it copies", "O(1), it's a view", "O(n²)", "O(log n)"],
        "O(b − a), because it copies"),

    mcq(r"""
What is the total cost of building a string of length n with `+=` one character at a time?
""", ["O(n²)", "O(n)", "O(n log n)", "O(1)"], "O(n²)"),

    mcq(r"""
Which class builds strings efficiently piece by piece?
""", ["StringBuffer", "StringBuilder", "List<String>", "Runes"], "StringBuffer"),

    fill(r"""
Append to a StringBuffer:

```dart
void main() {
  final sb = StringBuffer();
  sb.%fill%('Hello');
  sb.write(' Dart');
  print(sb.toString());
}
```
""", "write"),

    mcq(r"""
What does this print?

```dart
void main() {
  final sb = StringBuffer();
  sb
    ..write('a')
    ..write(1)
    ..write(true);
  print(sb);
}
```
""", ["a1true", "a 1 true", "[a, 1, true]", "It throws an error"], "a1true"),

    mcq(r"""
What does this print?

```dart
void main() {
  final sb = StringBuffer();
  sb.writeAll(['x', 'y', 'z'], '-');
  print(sb.toString());
}
```
""", ["x-y-z", "xyz", "x-y-z-", "[x, y, z]"], "x-y-z"),

    mcq(r"""
What does `writeln` do?
""", ["Writes the value followed by a newline", "Writes a line number",
       "Writes and immediately prints", "Clears the buffer"],
        "Writes the value followed by a newline"),

    mcq(r"""
What does this print?

```dart
void main() {
  print(['a', 'b', 'c'].join(', '));
}
```
""", ["a, b, c", "abc", "[a, b, c]", "a,b,c"], "a, b, c"),

    mcq(r"""
What does this print?

```dart
void main() {
  print([1, true, 'x'].join('|'));
}
```
""", ["1|true|x", "1truex", "It throws an error", "[1, true, x]"], "1|true|x"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('hi👋'.length);
}
```
""", ["4", "3", "2", "5"], "4"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('hi👋'.runes.length);
}
```
""", ["3", "4", "2", "1"], "3"),

    mcq(r"""
What does `String.length` count?
""", ["UTF-16 code units", "Unicode code points", "Visible characters (graphemes)", "Bytes in UTF-8"],
        "UTF-16 code units"),

    mcq(r"""
Which API iterates over Unicode code points?
""", ["runes", "codeUnits", "split('')", "characters (dart:core)"], "runes"),

    mcq(r"""
Which package correctly counts user-visible characters like 👨‍👩‍👧?
""", ["package:characters", "dart:math", "dart:collection", "package:path"],
        "package:characters"),

    mcq(r"""
Why does `'hi👋'.split('').reversed.join()` produce garbage?
""", ["It splits the emoji's surrogate pair into two halves",
       "reversed doesn't work on strings", "join adds spaces", "split('') throws on emoji"],
        "It splits the emoji's surrogate pair into two halves"),

    fill(r"""
Build a string from code units or runes:

```dart
void main() {
  final s = String.%fill%([72, 105]);
  print(s); // Hi
}
```
""", "fromCharCodes"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('A'.codeUnitAt(0));
  print('a'.codeUnitAt(0));
}
```
""", ["65 then 97", "97 then 65", "1 then 1", "65 then 66"], "65 then 97"),

    mcq(r"""
What does this print?

```dart
void main() {
  final units = 'abc'.codeUnits.toList();
  for (var i = 0; i < units.length; i++) {
    units[i] -= 32;
  }
  print(String.fromCharCodes(units));
}
```
""", ["ABC", "abc", "[65, 66, 67]", "It throws an error"], "ABC"),

    mcq(r"""
What does this print?

```dart
void main() {
  final letters = 'dcba'.split('')..sort();
  print(letters.join());
}
```
""", ["abcd", "dcba", "[a, b, c, d]", "a,b,c,d"], "abcd"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('banana'.indexOf('an'));
  print('banana'.lastIndexOf('an'));
}
```
""", ["1 then 3", "1 then 1", "3 then 1", "2 then 4"], "1 then 3"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('Flutter'.contains('utt'));
}
```
""", ["true", "false", "2", "It throws an error"], "true"),

    mcq(r"""
What does this print?

```dart
bool isPal(String s) {
  var l = 0, r = s.length - 1;
  while (l < r) {
    if (s[l] != s[r]) return false;
    l++;
    r--;
  }
  return true;
}

void main() {
  print(isPal('level'));
  print(isPal('levels'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    fill(r"""
Remove every non-alphanumeric character with a regular expression:

```dart
void main() {
  final clean = 'A, b!'.toLowerCase().%fill%(RegExp(r'[^a-z0-9]'), '');
  print(clean); // ab
}
```
""", "replaceAll"),

    mcq(r"""
What does the `r` prefix in `r'\d+'` mean?
""", ["A raw string: backslashes and $ aren't treated specially", "A regex literal",
       "A reversed string", "A rune string"],
        "A raw string: backslashes and $ aren't treated specially"),

    mcq(r"""
What does this print?

```dart
void main() {
  final counts = <String, int>{};
  for (final ch in 'hello'.split('')) {
    counts.update(ch, (c) => c + 1, ifAbsent: () => 1);
  }
  print(counts['l']);
}
```
""", ["2", "1", "3", "null"], "2"),

    fill(r"""
Insert a default when the key is missing:

```dart
void main() {
  final counts = <String, int>{};
  counts.update('a', (c) => c + 1, %fill%: () => 1);
  print(counts); // {a: 1}
}
```
""", "ifAbsent"),

    mcq(r"""
What does this print?

```dart
bool isAnagram(String a, String b) {
  if (a.length != b.length) return false;
  final counts = <int, int>{};
  for (final c in a.codeUnits) counts[c] = (counts[c] ?? 0) + 1;
  for (final c in b.codeUnits) {
    final left = (counts[c] ?? 0) - 1;
    if (left < 0) return false;
    counts[c] = left;
  }
  return true;
}

void main() {
  print(isAnagram('evil', 'vile'));
  print(isAnagram('evil', 'veil!'));
}
```
""", ["true then false", "false then true", "true then true", "false then false"],
        "true then false"),

    mcq(r"""
What is the time complexity of the counting anagram check?
""", ["O(n)", "O(n log n)", "O(n²)", "O(1)"], "O(n)"),

    mcq(r"""
What is the time complexity of checking anagrams by sorting both strings?
""", ["O(n log n)", "O(n)", "O(n²)", "O(1)"], "O(n log n)"),

    mcq(r"""
What does this print?

```dart
String compress(String s) {
  final out = StringBuffer();
  var count = 1;
  for (var i = 1; i <= s.length; i++) {
    if (i < s.length && s[i] == s[i - 1]) {
      count++;
    } else {
      out
        ..write(s[i - 1])
        ..write(count);
      count = 1;
    }
  }
  return out.toString();
}

void main() {
  print(compress('aabbbc'));
}
```
""", ["a2b3c1", "a2b3c", "abc", "a1a1b1b1b1c1"], "a2b3c1"),

    mcq(r"""
What does `'apple'.compareTo('banana')` return?
""", ["A negative number", "A positive number", "0", "true"], "A negative number"),

    mcq(r"""
What does this print?

```dart
void main() {
  final names = ['bob', 'Alice'];
  names.sort();
  print(names);
}
```
""", ["[Alice, bob]", "[bob, Alice]", "[alice, bob]", "It throws an error"], "[Alice, bob]"),

    mcq(r"""
Why does `'Zed'` sort before `'apple'` with the default `sort()`?
""", ["Uppercase letters have smaller code units than lowercase",
       "Shorter strings always come first", "Z is a special character",
       "Dart sorts in reverse by default"],
        "Uppercase letters have smaller code units than lowercase"),

    order(r"""
Sort names case-insensitively:

```dart
void main() {
  final names = ['bob', 'Alice', 'carol'];
  names.%order%((a, b) => a.%order%().%order%(b.toLowerCase()));
  print(names);
}
```
""", ["sort", "toLowerCase", "compareTo", "reversed", "toUpperCase", "equals"],
        ["sort", "toLowerCase", "compareTo"]),

    mcq(r"""
Is Dart's `List.sort` guaranteed to be stable?
""", ["No", "Yes", "Only for strings", "Only in release mode"], "No"),

    mcq(r"""
What does this print?

```dart
void main() {
  const input = 'Yes';
  print(input == 'yes');
  print(input.toLowerCase() == 'yes');
}
```
""", ["false then true", "true then true", "true then false", "false then false"],
        "false then true"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('ab' * 3);
}
```
""", ["ababab", "ab3", "aabbb", "It throws an error"], "ababab"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('7'.padLeft(3, '0'));
}
```
""", ["007", "700", "7", "  7"], "007"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('  hi  '.trim().length);
}
```
""", ["2", "6", "4", "0"], "2"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('a,b,,c'.split(','));
}
```
""", ["[a, b, , c]", "[a, b, c]", "[a,b,,c]", "It throws an error"], "[a, b, , c]"),

    mcq(r"""
What does this print?

```dart
String reverseWords(String s) =>
    s.split(' ').where((w) => w.isNotEmpty).toList().reversed.join(' ');

void main() {
  print(reverseWords('one  two three'));
}
```
""", ["three two one", "eerht owt eno", "three  two one", "one two three"],
        "three two one"),

    mcq(r"""
Why are strings safe to use as Map keys?
""", ["They are immutable with value-based == and hashCode",
       "They are always short", "Maps convert them to ints", "They are stored on the stack"],
        "They are immutable with value-based == and hashCode"),

    mcq(r"""
What is the cost of comparing two strings of length n with `==`?
""", ["O(n) in the worst case", "O(1) always", "O(n²)", "O(log n)"],
        "O(n) in the worst case"),

    order(r"""
Find the first non-repeating character:

```dart
String? firstUnique(String s) {
  final counts = <String, int>{};
  for (final c in s.%order%('')) {
    counts[c] = (counts[c] %order% 0) + 1;
  }
  for (final c in s.split('')) {
    if (counts[c] %order% 1) return c;
  }
  return null;
}
```
""", ["split", "??", "==", "join", "!=", "?."], ["split", "??", "=="]),

    mcq(r"""
What does `firstUnique('swiss')` return?
""", ["w", "s", "i", "null"], "w"),

    mcq(r"""
What does this print?

```dart
void main() {
  final s = 'Dart';
  final chars = s.split('');
  chars[0] = 'K';
  print(chars.join());
  print(s);
}
```
""", ["Kart then Dart", "Kart then Kart", "Dart then Dart", "It throws an error"],
        "Kart then Dart"),

    mcq(r"""
What does this print?

```dart
void main() {
  final sb = StringBuffer('ab');
  sb.write('cd');
  print(sb.length);
}
```
""", ["4", "2", "1", "0"], "4"),

    mcq(r"""
Which is the cleanest way to combine an existing `List<String>` into one string with newlines?
""", ["list.join('\\n')", "A for loop with +=", "list.toString()", "list.reduce((a, b) => a + b)"],
        "list.join('\\n')"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('Dart'.toUpperCase().toLowerCase() == 'dart');
}
```
""", ["true", "false", "DART", "dart"], "true"),

    fill(r"""
Get the last character safely:

```dart
void main() {
  const s = 'Flutter';
  print(s[s.%fill% - 1]); // r
}
```
""", "length"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('abc'.codeUnits);
}
```
""", ["[97, 98, 99]", "[a, b, c]", "abc", "[65, 66, 67]"], "[97, 98, 99]"),

    mcq(r"""
What does this print?

```dart
void main() {
  print('ab'.compareTo('ab'));
}
```
""", ["0", "1", "-1", "true"], "0"),
]
