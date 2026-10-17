# Strings as Data Structures

Imagine a **necklace of beads** 📿, where each bead is a letter.

- You can **look** at any bead by its position. ✅
- But the necklace is **glued shut**: you can't swap, add or remove a bead. 🔒
- If you want a different necklace, you have to **string a brand new one**, copying the beads you want to keep.

👉 That's a Dart `String`:

> A **String** is an **immutable sequence of UTF-16 code units**. You can read any position in O(1), but every "change" creates a **new** string.

That one fact, immutability, explains most string performance problems, and how to fix them with `StringBuffer`.

---

## 🔒 Strings Are Immutable

```dart
void main() {
  var word = 'cat';
  final original = word;

  word = word.toUpperCase(); // returns a NEW string
  print(word);     // CAT
  print(original); // cat (unchanged)

  // word[0] = 'b'; ❌ compile error: String has no []= operator

  final bat = 'b${word.substring(1)}'; // build a new one instead
  print(bat); // bAT
}
```

**🔍 What This Code Does:**

1. **New Strings Everywhere**: `toUpperCase`, `substring`, `replaceAll`, `trim` and `+` all return **new** strings.
2. **Original Untouched**: `original` still points to `'cat'`.
3. **No Index Assignment**: `String` only has `operator []` for reading, so `word[0] = 'b'` doesn't compile.
4. **Building Instead of Editing**: To "change" a character, combine pieces into a new string.

**Why immutable?** Strings are used as Map keys, Set entries and shared everywhere. If they could change, a key could silently move to the wrong hash bucket (remember **How Dart Stores Data**). Immutability makes them safe to share and lets Dart reuse identical literals.

---

## 🔢 Reading Characters: O(1) by Index

```dart
void main() {
  const s = 'Flutter';

  print(s[0]);              // F
  print(s[s.length - 1]);   // r
  print(s.length);          // 7
  print(s.codeUnitAt(0));   // 70 (UTF-16 code unit for 'F')
  print(s.indexOf('t'));    // 3
  print(s.lastIndexOf('t')); // 4
  print(s.contains('utt')); // true
}
```

**🔍 What This Code Does:**

1. **`s[i]`**: Returns a one-character String at index `i` in O(1).
2. **`length`**: Number of UTF-16 code units, stored, O(1).
3. **`codeUnitAt`**: The raw 16-bit number at that position, useful for fast comparisons.
4. **Searching**: `indexOf`, `lastIndexOf` and `contains` scan the string, so they're O(n) (more precisely, up to O(n × m) for a pattern of length m).

| Operation | Cost |
|-----------|------|
| `s[i]`, `s.codeUnitAt(i)`, `s.length` | O(1) |
| `s.substring(a, b)` | O(b − a), copies |
| `s + t`, `'$s$t'` | O(len(s) + len(t)), copies both |
| `s.contains(p)`, `s.indexOf(p)` | O(n × m) worst case |
| `s == t` | O(n), compares character by character |
| `s.split(',')` | O(n) |
| `s.toUpperCase()`, `s.trim()` | O(n) |
| `s.hashCode` | O(n) the first time, then cached by the VM |

---

## 🐢 The Concatenation Trap

Because every `+` copies both strings, building a string piece by piece in a loop gets **quadratic**.

```dart
void main() {
  const n = 20000;

  final sw1 = Stopwatch()..start();
  var slow = '';
  for (var i = 0; i < n; i++) {
    slow += 'x'; // ❌ copies the whole string every time
  }
  sw1.stop();

  final sw2 = Stopwatch()..start();
  final buffer = StringBuffer();
  for (var i = 0; i < n; i++) {
    buffer.write('x'); // ✅ appends into a growable buffer
  }
  final fast = buffer.toString();
  sw2.stop();

  print('+= : ${sw1.elapsedMilliseconds} ms, length ${slow.length}');
  print('StringBuffer: ${sw2.elapsedMilliseconds} ms, length ${fast.length}');
}
```

**🔍 What This Code Does:**

1. **Repeated Copies**: The `k`-th `+=` copies a string of length `k`. Total copying: `1 + 2 + ... + n ≈ n²/2`, so **O(n²)**.
2. **`StringBuffer`**: Collects pieces internally (like a growable list) and builds the final string **once** in `toString()`, so **O(n)** total.
3. **Same Result**: Both produce 20,000 `x` characters.
4. **Rule**: Concatenating a few strings is fine; concatenating **inside a loop** calls for `StringBuffer`.

> 💡 The Dart VM is sometimes clever about `+=` in simple loops, but you should never rely on it. `StringBuffer` is always the safe choice.

---

## 🧰 Using StringBuffer

```dart
void main() {
  final receipt = StringBuffer();

  receipt.writeln('🧾 RECEIPT');
  receipt.writeln('-' * 20);

  final items = {'Coffee': 3.5, 'Bagel': 2.25, 'Juice': 4.0};
  items.forEach((name, price) {
    receipt
      ..write(name.padRight(12))
      ..writeln('\$${price.toStringAsFixed(2)}');
  });

  final total = items.values.reduce((a, b) => a + b);
  receipt
    ..writeln('-' * 20)
    ..write('TOTAL'.padRight(12))
    ..writeln('\$${total.toStringAsFixed(2)}');

  receipt.writeAll(['Thanks', 'for', 'visiting!'], ' ');

  print(receipt.toString());
  print('Buffer length: ${receipt.length}');
}
```

**🔍 What This Code Does:**

1. **`write`**: Appends any object's `toString()`.
2. **`writeln`**: Appends followed by a newline.
3. **Cascades `..`**: Chain several writes on the same buffer.
4. **`writeAll`**: Appends every item of an iterable with a separator.
5. **`padRight`**: Pads with spaces to line up the price column.
6. **`length`**: The buffer knows its current length without building the string.

### `join`: the other O(n) builder

```dart
void main() {
  final words = ['data', 'structures', 'in', 'dart'];
  print(words.join(' '));     // data structures in dart
  print(words.join(', '));    // data, structures, in, dart

  final csvRow = [42, 'Ada', true].join(',');
  print(csvRow);              // 42,Ada,true
}
```

**🔍 What This Code Does:**

1. **`join`**: Builds one string from many pieces in O(total length).
2. **Any Objects**: Non-string items are converted with `toString()`.
3. **Idiomatic**: When you already have a list of parts, `join` is cleaner than a buffer.

---

## 🌍 Code Units, Code Points and Runes

Dart strings are **UTF-16**. Most characters fit in **one** 16-bit code unit, but emoji and many symbols need **two** (a *surrogate pair*).

```dart
void main() {
  const plain = 'hi';
  const emoji = 'hi👋';

  print(plain.length);          // 2
  print(emoji.length);          // 4  (👋 is 2 code units!)
  print(emoji.runes.length);    // 3  (3 Unicode code points)
  print(emoji.codeUnits);       // [104, 105, 55357, 56395]
  print(emoji.runes.toList());  // [104, 105, 128075]

  // ❌ Reversing by code units breaks the emoji
  print(emoji.split('').reversed.join());

  // ✅ Reversing by runes keeps it intact
  print(String.fromCharCodes(emoji.runes.toList().reversed));
}
```

**🔍 What This Code Does:**

1. **`length` Counts Code Units**: `'hi👋'` has length 4, not 3.
2. **`runes`**: Iterates over full Unicode **code points**, so 👋 counts as one.
3. **`codeUnits`**: Shows the raw UTF-16 numbers, including the surrogate pair `55357, 56395`.
4. **Broken Reversal**: Splitting into code units separates the surrogate pair, producing garbage characters.
5. **Correct Reversal**: Reverse the runes and rebuild with `String.fromCharCodes`.

| Concept | Meaning | Dart API |
|---------|---------|----------|
| **Code unit** | One 16-bit value | `s.length`, `s[i]`, `s.codeUnits` |
| **Code point (rune)** | One Unicode character number | `s.runes` |
| **Grapheme cluster** | What a human sees as one character (👨‍👩‍👧 is several code points!) | `package:characters` (`s.characters`) |

> 💡 In Flutter apps, use `package:characters` (`text.characters.length`) when counting what the **user** sees, for example in a text field's character counter.

---

## 🔁 Strings ⇄ Lists

Since strings can't change, a common pattern is: **convert to a list, edit, convert back**.

```dart
void main() {
  const word = 'listen';

  // Sort the letters (an anagram "signature")
  final letters = word.split('')..sort();
  print(letters.join()); // eilnst

  // Swap characters
  final chars = 'abcd'.split('');
  final tmp = chars[0];
  chars[0] = chars[3];
  chars[3] = tmp;
  print(chars.join()); // dbca

  // Work with code units for speed (ASCII text)
  final units = 'hello'.codeUnits.toList();
  for (var i = 0; i < units.length; i++) {
    units[i] -= 32; // lowercase ASCII → uppercase ASCII
  }
  print(String.fromCharCodes(units)); // HELLO
}
```

**🔍 What This Code Does:**

1. **`split('')`**: Turns a string into a list of one-character strings.
2. **Sorting Letters**: Two words are anagrams if their sorted letters match.
3. **Swapping**: Lists are mutable, so we can swap and then `join()`.
4. **Code Unit Math**: For ASCII, lowercase letters are exactly 32 more than uppercase (`'a'` = 97, `'A'` = 65).
5. **`String.fromCharCodes`**: Builds a string from a list of code units.

---

## 🔎 Classic String Algorithms

### Palindrome check (two pointers)

```dart
bool isPalindrome(String s) {
  final clean = s.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
  var left = 0, right = clean.length - 1;
  while (left < right) {
    if (clean[left] != clean[right]) return false;
    left++;
    right--;
  }
  return true;
}

void main() {
  print(isPalindrome('A man, a plan, a canal: Panama')); // true
  print(isPalindrome('Dart'));                           // false
}
```

**🔍 What This Code Does:**

1. **Normalize**: Lowercase and remove everything except letters and digits with a regular expression.
2. **Two Pointers**: Compare from both ends toward the middle.
3. **O(n) Time**: One pass to clean, one to compare.
4. **Raw String**: `r'...'` means backslashes and `$` aren't treated specially, which is handy for regex.

### Character frequency

```dart
Map<String, int> frequency(String s) {
  final counts = <String, int>{};
  for (final ch in s.split('')) {
    counts.update(ch, (c) => c + 1, ifAbsent: () => 1);
  }
  return counts;
}

void main() {
  print(frequency('banana')); // {b: 1, a: 3, n: 2}
}
```

**🔍 What This Code Does:**

1. **`Map.update`**: Increments an existing count, or inserts 1 with `ifAbsent`.
2. **Insertion Order**: Dart's default Map keeps keys in the order they were first added.
3. **O(n)**: One map operation per character.

### Valid anagram

```dart
bool isAnagram(String a, String b) {
  if (a.length != b.length) return false;
  final counts = <int, int>{};
  for (final c in a.codeUnits) {
    counts[c] = (counts[c] ?? 0) + 1;
  }
  for (final c in b.codeUnits) {
    final left = (counts[c] ?? 0) - 1;
    if (left < 0) return false;
    counts[c] = left;
  }
  return true;
}

void main() {
  print(isAnagram('listen', 'silent')); // true
  print(isAnagram('rat', 'car'));       // false
}
```

**🔍 What This Code Does:**

1. **Length Check First**: Different lengths can never be anagrams.
2. **Count Up, Count Down**: Add counts for `a`, subtract for `b`.
3. **Early Exit**: A count going negative means `b` has a character `a` doesn't have enough of.
4. **O(n)**: Faster than sorting both strings (O(n log n)).

### Run-length encoding

```dart
String compress(String s) {
  if (s.isEmpty) return s;
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
  final result = out.toString();
  return result.length < s.length ? result : s;
}

void main() {
  print(compress('aaabccdddd')); // a3b1c2d4
  print(compress('abc'));        // abc (compressed would be longer)
}
```

**🔍 What This Code Does:**

1. **Count Runs**: Consecutive equal characters increase `count`.
2. **Flush on Change**: When the character changes (or the string ends), write the character and its count.
3. **Loop to `<= length`**: The extra iteration flushes the final run.
4. **StringBuffer**: Avoids O(n²) concatenation.
5. **Only If Shorter**: Returns the original when compression doesn't help.

---

## 🔤 Comparing and Sorting Strings

```dart
void main() {
  print('apple'.compareTo('banana')); // negative: apple comes first
  print('b'.compareTo('a'));          // positive
  print('same'.compareTo('same'));    // 0

  final names = ['bob', 'Alice', 'carol', 'Dave'];
  names.sort();
  print(names); // [Alice, Dave, bob, carol] (uppercase sorts first!)

  names.sort((a, b) => a.toLowerCase().compareTo(b.toLowerCase()));
  print(names); // [Alice, bob, carol, Dave]

  names.sort((a, b) => a.length.compareTo(b.length));
  print(names); // [bob, Dave, Alice, carol]
}
```

**🔍 What This Code Does:**

1. **`compareTo`**: Returns negative, zero or positive, comparing code units in order.
2. **Case Sensitivity**: Uppercase letters (65–90) have smaller codes than lowercase (97–122), so `'Dave'` sorts before `'bob'`.
3. **Case-Insensitive Sort**: Compare lowercase versions with a custom comparator.
4. **Sort by Length**: Any property can drive the comparator. `Alice` and `carol` tie on length; Dart's `List.sort` is **not guaranteed to be stable**, so ties may come out in either order. Use `mergeSort` from `package:collection` when ties must keep their order.

---

## ⚠️ Common Mistakes

### 1. Concatenating in a loop

```dart
void main() {
  final parts = List.generate(5, (i) => 'line $i');

  // ❌ O(n²) for large inputs
  var text = '';
  for (final p in parts) {
    text += '$p\n';
  }

  // ✅ O(n)
  final better = parts.join('\n');
  print(better);
  print(text.length > better.length); // true (text has a trailing newline)
}
```

**🔍 What This Code Does:**

1. **Repeated Copies**: Each `+=` rebuilds the whole string.
2. **`join`**: Builds the result once.

### 2. Assuming `length` equals the visible characters

```dart
void main() {
  const name = 'Zoë 🎉';
  print(name.length);       // 6, not 5
  print(name.runes.length); // 5
}
```

**🔍 What This Code Does:**

1. **Emoji Use Two Code Units**: 🎉 adds 2 to `length`.
2. **Use Runes or Characters**: Count code points with `runes`, or graphemes with `package:characters`.

### 3. Comparing with `==` when case shouldn't matter

```dart
void main() {
  const input = 'YES';
  print(input == 'yes');               // false
  print(input.toLowerCase() == 'yes'); // true
}
```

**🔍 What This Code Does:**

1. **Exact Comparison**: `==` compares code units exactly.
2. **Normalize First**: Lowercase both sides for case-insensitive checks.

---

## 🧪 Try It Yourself

1. Write `reverseWords('data structures are fun')` → `'fun are structures data'`.
2. Write `firstUniqueChar('swiss')` → `'w'` in O(n) using a frequency map.
3. Write `capitalizeEach('hello dart world')` → `'Hello Dart World'` with a `StringBuffer`.
4. Write `longestCommonPrefix(['flower', 'flow', 'flight'])` → `'fl'`.

```dart
String reverseWords(String s) =>
    s.split(' ').where((w) => w.isNotEmpty).toList().reversed.join(' ');

void main() {
  print(reverseWords('data  structures are fun')); // fun are structures data
}
```

**🔍 What This Code Does:**

1. **Split on Spaces**: Produces words (and empty strings for double spaces).
2. **Filter Empties**: `where((w) => w.isNotEmpty)` removes them.
3. **Reverse and Join**: Builds the result in O(n).

---

## 📌 Key Takeaways

- ✅ Dart strings are **immutable** sequences of **UTF-16 code units**.
- ✅ Reading by index is **O(1)**; every "modification" creates a **new string** in O(n).
- ✅ Concatenating in a loop is **O(n²)**; use **`StringBuffer`** or **`join`** for O(n).
- ✅ `length` counts **code units**; use **`runes`** for code points and **`package:characters`** for what users see.
- ✅ Convert to a **list** (`split('')`, `codeUnits`) to edit, then rebuild.
- ✅ Frequency maps and two pointers solve most string problems in **O(n)**.

**Next up:** 👆👆 **Two Pointers & Sliding Window**, the two patterns behind a huge number of array and string problems.
