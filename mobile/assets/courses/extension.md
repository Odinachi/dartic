# Extension Methods in Dart

Imagine you have a favorite **toy robot** 🤖.

But one day, you say:

> "I wish my robot could **sing songs** too!"

Instead of buying a new robot, you just give it **new powers** — like adding a button for singing! 🎵

👉 That's what **extension methods** do in Dart:

> They let you **add new abilities** (functions) to existing classes, **without changing the original**!

---

## 🎁 Real-Life Analogy

| Real Life                       | Dart Code                             |
| ------------------------------- | ------------------------------------- |
| Adding a new button to a toy 🧸 | Add a method to a class via extension |
| Giving your shoes wings 🪽👟     | Give extra features to existing class |
| Superpowers without surgery 🦸‍♂️  | Keep class the same, but do more!     |

---

## 🚫 The Problem: Limited Built-in Methods

```dart
void main() {
  String name = 'sarah johnson';

  print(name.toUpperCase()); // SARAH JOHNSON
  print(name.toLowerCase()); // sarah johnson

}
```

**🔍 What This Code Does:**

This code demonstrates **the limitations of built-in class methods**:

1. **Limited Functionality**: Built-in classes like `String` only provide basic methods (`toUpperCase()`, `toLowerCase()`), leaving many common operations unsupported.

2. **Missing Common Operations**: Everyday tasks like capitalizing each word, adding exclamation marks, or checking palindromes require custom implementations.

3. **Repetitive Code**: Without extensions, you'd need to write the same utility functions repeatedly across different files and projects.

4. **Poor Developer Experience**: Lack of method chaining and fluent APIs makes code less readable and harder to maintain.

5. **Utility Class Proliferation**: Developers often create separate utility classes to handle these operations, leading to scattered functionality.

**Problems:**

- Built-in classes don't have every method we need 😔
- We can't modify String, int, List classes directly 🚫
- Repetitive code when we need the same functionality 📝

---

## ✅ The Solution: Extension Methods

Let's teach all strings how to **shout** and **capitalize properly**:

```dart
extension StringMagic on String {
  String shout() {
    return toUpperCase() + '!!!';
  }

  String capitalizeWords() {
    return split(' ')
        .map((word) => word.isEmpty ? '' :
             word[0].toUpperCase() + word.substring(1).toLowerCase())
        .join(' ');
  }

  String reverse() {
    return split('').reversed.join('');
  }

  bool get isPalindrome {
    String cleaned = toLowerCase().replaceAll(' ', '');
    return cleaned == cleaned.split('').reversed.join('');
  }
}

void main() {
  String name = 'sarah johnson';

  print('Original: $name');
  print('Shouting: ${name.shout()}');
  print('Capitalized: ${name.capitalizeWords()}');
  print('Reversed: ${name.reverse()}');

  String palindrome = 'racecar';
  print('Is "$palindrome" a palindrome? ${palindrome.isPalindrome}');
}
```

**🔍 What This Code Does:**

This code demonstrates **extension method creation and usage**:

1. **Extension Declaration**: `extension StringMagic on String` adds new methods to the existing `String` class without modifying its source code.

2. **Method Addition**: New methods like `shout()`, `capitalizeWords()`, and `reverse()` become available on all String instances.

3. **Getter Extension**: The `isPalindrome` getter demonstrates how to add computed properties using the `get` keyword.

4. **Method Chaining**: Extensions enable fluent method chaining by operating on and returning String values.

5. **Complex Logic**: The `capitalizeWords()` method shows how extensions can contain sophisticated logic involving multiple operations (split, map, join).

6. **Non-Destructive**: Original strings remain unchanged; extensions return new values, maintaining immutability.

7. **Universal Availability**: Once defined, these methods work on any String instance throughout the application.

**Output:**

```
Original: sarah johnson
Shouting: SARAH JOHNSON!!!
Capitalized: Sarah Johnson
Reversed: noshoj haras
Is "racecar" a palindrome? true
```

---

## 🧮 Number Magic Extensions

```dart
extension NumberMagic on int {
  int get square => this * this;
  int get cube => this * this * this;

  bool get isEven => this % 2 == 0;
  bool get isOdd => this % 2 != 0;

  String get ordinal {
    if (this >= 11 && this <= 13) return '${this}th';
    switch (this % 10) {
      case 1: return '${this}st';
      case 2: return '${this}nd';
      case 3: return '${this}rd';
      default: return '${this}th';
    }
  }

  List<int> get factors {
    List<int> result = [];
    for (int i = 1; i <= this; i++) {
      if (this % i == 0) result.add(i);
    }
    return result;
  }

  String toEmoji() {
    const numberEmojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'];
    return toString().split('').map((digit) =>
      numberEmojis[int.parse(digit)]).join('');
  }
}

void main() {
  int number = 12;

  print('🔢 Number Magic with $number:');
  print('Square: ${number.square}');
  print('Cube: ${number.cube}');
  print('Is even: ${number.isEven}');
  print('Is odd: ${number.isOdd}');
  print('Ordinal: ${number.ordinal}');
  print('Factors: ${number.factors}');
  print('As emoji: ${number.toEmoji()}');

  print('\n🎯 Testing different numbers:');
  for (int i = 1; i <= 5; i++) {
    print('${i.ordinal} place winner! ${i.toEmoji()}');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **mathematical and utility extensions for integers**:

1. **Mathematical Operations**: `square` and `cube` getters provide quick access to common mathematical operations without external functions.

2. **Boolean Properties**: `isEven` and `isOdd` getters encapsulate common number classification logic in readable properties.

3. **String Formatting**: The `ordinal` getter implements complex business logic for converting numbers to ordinal forms (1st, 2nd, 3rd, etc.).

4. **Mathematical Analysis**: The `factors` getter performs mathematical computation to find all divisors of a number.

5. **Visual Representation**: `toEmoji()` method demonstrates string manipulation and mapping for creative number display.

6. **Edge Case Handling**: The ordinal logic handles special cases (11th, 12th, 13th) that don't follow standard patterns.

---

## 📅 DateTime Adventures

```dart
extension DateTimeMagic on DateTime {
  String get friendlyDate {
    DateTime now = DateTime.now();
    Duration difference = now.difference(this);

    if (difference.inDays == 0) {
      if (difference.inHours == 0) {
        if (difference.inMinutes < 1) return 'Just now';
        return '${difference.inMinutes} minutes ago';
      }
      return '${difference.inHours} hours ago';
    } else if (difference.inDays == 1) {
      return 'Yesterday';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} days ago';
    } else {
      return '${day}/${month}/${year}';
    }
  }

  bool get isWeekend => weekday == DateTime.saturday || weekday == DateTime.sunday;

  bool get isToday {
    DateTime now = DateTime.now();
    return year == now.year && month == now.month && day == now.day;
  }

  String get seasonEmoji {
    int month = this.month;
    if (month >= 3 && month <= 5) return '🌸'; // Spring
    if (month >= 6 && month <= 8) return '☀️'; // Summer
    if (month >= 9 && month <= 11) return '🍂'; // Fall
    return '❄️'; // Winter
  }

  String get zodiacSign {
    int month = this.month;
    int day = this.day;

    if ((month == 3 && day >= 21) || (month == 4 && day <= 19)) return 'Aries ♈';
    if ((month == 4 && day >= 20) || (month == 5 && day <= 20)) return 'Taurus ♉';
    if ((month == 5 && day >= 21) || (month == 6 && day <= 20)) return 'Gemini ♊';
    if ((month == 6 && day >= 21) || (month == 7 && day <= 22)) return 'Cancer ♋';
    if ((month == 7 && day >= 23) || (month == 8 && day <= 22)) return 'Leo ♌';
    if ((month == 8 && day >= 23) || (month == 9 && day <= 22)) return 'Virgo ♍';
    if ((month == 9 && day >= 23) || (month == 10 && day <= 22)) return 'Libra ♎';
    if ((month == 10 && day >= 23) || (month == 11 && day <= 21)) return 'Scorpio ♏';
    if ((month == 11 && day >= 22) || (month == 12 && day <= 21)) return 'Sagittarius ♐';
    if ((month == 12 && day >= 22) || (month == 1 && day <= 19)) return 'Capricorn ♑';
    if ((month == 1 && day >= 20) || (month == 2 && day <= 18)) return 'Aquarius ♒';
    return 'Pisces ♓';
  }
}

void main() {
  DateTime now = DateTime.now();
  DateTime birthday = DateTime(2010, 5, 15);
  DateTime yesterday = now.subtract(Duration(days: 1));
  DateTime lastWeek = now.subtract(Duration(days: 5));

  print('📅 DateTime Magic:');
  print('Today: ${now.friendlyDate}');
  print('Yesterday: ${yesterday.friendlyDate}');
  print('Last week: ${lastWeek.friendlyDate}');
  print('My birthday: ${birthday.friendlyDate}');

  print('\n🎉 Birthday Info:');
  print('Season: ${birthday.seasonEmoji}');
  print('Zodiac: ${birthday.zodiacSign}');
  print('Is weekend: ${birthday.isWeekend}');

  print('\n📊 Today\'s Info:');
  print('Is today: ${now.isToday}');
  print('Is weekend: ${now.isWeekend}');
  print('Current season: ${now.seasonEmoji}');
}
```

**🔍 What This Code Does:**

This code demonstrates **complex date/time manipulation and user-friendly formatting**:

1. **Relative Time Calculation**: The `friendlyDate` getter calculates time differences and presents them in human-readable format.

2. **Hierarchical Time Logic**: Uses nested conditions to handle different time scales (minutes, hours, days, weeks) with appropriate messaging.

3. **Real-Time Comparison**: Dynamically compares against the current time using `DateTime.now()` for accurate relative calculations.

4. **Weekend Detection**: `isWeekend` getter encapsulates weekend logic using built-in `weekday` constants.

5. **Date Comparison**: `isToday` getter demonstrates precise date matching by comparing year, month, and day components.

6. **Fallback Formatting**: When dates are too old for relative formatting, falls back to standard date format.

---

## 📚 List SuperPowers

```dart
extension ListMagic<T> on List<T> {
  T? get secondOrNull => length >= 2 ? this[1] : null;
  T? get thirdOrNull => length >= 3 ? this[2] : null;
  T? get lastOrNull => isNotEmpty ? last : null;
  T? get penultimateOrNull => length >= 2 ? this[length - 2] : null;

  List<T> get shuffled {
    List<T> newList = List.from(this);
    newList.shuffle();
    return newList;
  }

  Map<T, int> get frequency {
    Map<T, int> freq = {};
    for (T item in this) {
      freq[item] = (freq[item] ?? 0) + 1;
    }
    return freq;
  }

  List<List<T>> chunk(int size) {
    List<List<T>> chunks = [];
    for (int i = 0; i < length; i += size) {
      chunks.add(sublist(i, (i + size > length) ? length : i + size));
    }
    return chunks;
  }
}

extension ListStringMagic on List<String> {
  String get longestWord {
    if (isEmpty) return '';
    return reduce((a, b) => a.length > b.length ? a : b);
  }

  String get shortestWord {
    if (isEmpty) return '';
    return reduce((a, b) => a.length < b.length ? a : b);
  }

  List<String> get capitalized {
    return map((word) => word.isEmpty ? '' :
           word[0].toUpperCase() + word.substring(1).toLowerCase()).toList();
  }
}

void main() {
  List<String> fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry'];
  List<int> numbers = [1, 2, 3, 4, 5, 2, 3, 1];

  print('🍎 Fruit List Magic:');
  print('Original: $fruits');
  print('Second fruit: ${fruits.secondOrNull}');
  print('Last fruit: ${fruits.lastOrNull}');
  print('Penultimate: ${fruits.penultimateOrNull}');
  print('Shuffled: ${fruits.shuffled}');
  print('Longest word: ${fruits.longestWord}');
  print('Shortest word: ${fruits.shortestWord}');
  print('Capitalized: ${fruits.capitalized}');

  print('\n🔢 Number List Magic:');
  print('Numbers: $numbers');
  print('Frequency: ${numbers.frequency}');
  print('Chunks of 3: ${numbers.chunk(3)}');

  List<String> colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange'];
  print('\n🌈 Color chunks: ${colors.chunk(2)}');
}
```

**🔍 What This Code Does:**

This code demonstrates **generic extensions and specialized type extensions**:

1. **Generic Extension**: `ListMagic<T>` works with any type of List, providing type-safe operations regardless of element type.

2. **Safe Access Patterns**: Methods like `secondOrNull`, `lastOrNull` prevent index out-of-bounds errors by returning null for invalid positions.

3. **Non-Destructive Operations**: `shuffled` creates a new list copy before shuffling, preserving the original list.

4. **Statistical Analysis**: `frequency` method counts occurrences of each element, useful for data analysis and reporting.

5. **Data Partitioning**: `chunk()` method divides lists into smaller sublists of specified size, handling remainder elements gracefully.

6. **Specialized Extensions**: `ListStringMagic` specifically targets `List<String>`, providing string-specific operations like length comparison.

7. **Functional Programming**: Uses `reduce()` and `map()` for elegant data transformation and analysis.

---

## 🎮 Gaming Extensions

```dart
extension PlayerStats on Map<String, dynamic> {
  int get level => this['level'] ?? 1;
  int get health => this['health'] ?? 100;
  int get experience => this['experience'] ?? 0;
  String get name => this['name'] ?? 'Unknown Player';

  int get experienceToNextLevel => (level * 1000) - experience;

  bool get canLevelUp => experience >= (level * 1000);

  String get healthStatus {
    double percentage = health / 100.0;
    if (percentage > 0.8) return 'Excellent 💚';
    if (percentage > 0.6) return 'Good 💛';
    if (percentage > 0.4) return 'Fair 🧡';
    if (percentage > 0.2) return 'Poor ❤️';
    return 'Critical 💀';
  }

  String get playerCard {
    return '''
🎮 === PLAYER CARD ===
👤 $name
📊 Level $level
❤️ Health: $health/100 (${healthStatus})
⚡ XP: $experience/${level * 1000}
🎯 XP to next level: $experienceToNextLevel
${canLevelUp ? '🎉 Ready to level up!' : ''}
═══════════════════════''';
  }

  void levelUp() {
    if (canLevelUp) {
      this['level'] = level + 1;
      this['health'] = 100; // Full heal on level up
      print('🎉 ${name} leveled up to ${level}!');
    }
  }
}

extension ScoreBoard on List<Map<String, dynamic>> {
  List<Map<String, dynamic>> get topPlayers {
    List<Map<String, dynamic>> sorted = List.from(this);
    sorted.sort((a, b) => (b['score'] ?? 0).compareTo(a['score'] ?? 0));
    return sorted;
  }

  Map<String, dynamic>? get highestScorer {
    if (isEmpty) return null;
    return reduce((a, b) => (a['score'] ?? 0) > (b['score'] ?? 0) ? a : b);
  }

  double get averageScore {
    if (isEmpty) return 0;
    int total = fold(0, (sum, player) => sum + (player['score'] ?? 0));
    return total / length;
  }

  void displayLeaderboard() {
    print('🏆 LEADERBOARD 🏆');
    print('═' * 30);
    List<Map<String, dynamic>> sorted = topPlayers;
    for (int i = 0; i < sorted.length; i++) {
      String medal = i == 0 ? '🥇' : i == 1 ? '🥈' : i == 2 ? '🥉' : '🏅';
      print('$medal ${i + 1}. ${sorted[i]['name']}: ${sorted[i]['score']} pts');
    }
    print('📊 Average Score: ${averageScore.toStringAsFixed(1)}');
  }
}

void main() {
  // Player stats
  Map<String, dynamic> player = {
    'name': 'DragonSlayer',
    'level': 5,
    'health': 75,
    'experience': 4800,
  };

  print(player.playerCard);

  if (player.canLevelUp) {
    player.levelUp();
    print('\n' + player.playerCard);
  }

  // Leaderboard
  List<Map<String, dynamic>> players = [
    {'name': 'Alice', 'score': 1250},
    {'name': 'Bob', 'score': 980},
    {'name': 'Charlie', 'score': 1400},
    {'name': 'Diana', 'score': 750},
  ];

  print('\n');
  players.displayLeaderboard();

  print('\n🏆 Champion: ${players.highestScorer!['name']}');
}
```

**🔍 What This Code Does:**

This code demonstrates **extending built-in collection types for domain-specific functionality**:

1. **Map Extension**: Extends `Map<String, dynamic>` to create a player statistics system using key-value pairs.

2. **Safe Property Access**: Getters use null coalescing (`??`) to provide default values when map keys don't exist.

3. **Computed Properties**: Properties like `experienceToNextLevel` and `canLevelUp` derive values from existing data.

4. **Business Logic Integration**: Implements game-specific rules (leveling system, health status calculation) within the extension.

5. **Multi-Line String Formatting**: `playerCard` getter demonstrates complex string templating for data presentation.

6. **Conditional Display**: Uses conditional expressions to show different content based on player state.

7. **Mutable Operations**: `levelUp()` method modifies the map data, showing how extensions can perform state changes.

---

## 🌐 Web & API Extensions

```dart
extension UrlMagic on String {
  bool get isValidUrl {
    try {
      Uri.parse(this);
      return startsWith('http://') || startsWith('https://');
    } catch (e) {
      return false;
    }
  }

  String get domain {
    if (!isValidUrl) return '';
    Uri uri = Uri.parse(this);
    return uri.host;
  }

  bool get isSecure => startsWith('https://');

  String addQueryParam(String key, String value) {
    String separator = contains('?') ? '&' : '?';
    return '$this$separator$key=${Uri.encodeComponent(value)}';
  }
}

extension ApiResponse on Map<String, dynamic> {
  bool get isSuccess => this['success'] == true || this['status'] == 'ok';
  String get message => this['message'] ?? 'No message';
  dynamic get data => this['data'];
  int get statusCode => this['statusCode'] ?? 200;

  void printResponse() {
    String emoji = isSuccess ? '✅' : '❌';
    print('$emoji API Response:');
    print('Status: ${statusCode}');
    print('Message: ${message}');
    if (data != null) print('Data: $data');
  }
}

void main() {
  // URL Magic
  print('🌐 URL Magic:');
  String url1 = 'https://api.example.com/users';
  String url2 = 'not-a-url';

  print('URL: $url1');
  print('Valid: ${url1.isValidUrl}');
  print('Domain: ${url1.domain}');
  print('Secure: ${url1.isSecure}');
  print('With param: ${url1.addQueryParam('limit', '10')}');

  print('\nURL: $url2');
  print('Valid: ${url2.isValidUrl}');

  // API Response Magic
  print('\n📡 API Response Magic:');

  Map<String, dynamic> successResponse = {
    'success': true,
    'message': 'Data retrieved successfully',
    'data': {'users': ['Alice', 'Bob', 'Charlie']},
    'statusCode': 200,
  };

  Map<String, dynamic> errorResponse = {
    'success': false,
    'message': 'User not found',
    'statusCode': 404,
  };

  successResponse.printResponse();
  print('');
  errorResponse.printResponse();
}
```

**🔍 What This Code Does:**

This code demonstrates **web development and API-focused extensions**:

1. **URL Validation**: `isValidUrl` getter uses try-catch exception handling to safely parse URLs and validate format.

2. **URL Parsing**: `domain` getter leverages Dart's `Uri` class to extract hostname from valid URLs.

3. **Security Checking**: `isSecure` getter provides quick HTTPS protocol detection for security validation.

4. **Query Parameter Building**: `addQueryParam()` method handles URL query string construction with proper encoding and separators.

5. **API Response Handling**: Extends Map to create a standardized interface for API response processing.

6. **Flexible Success Detection**: `isSuccess` getter handles multiple success indicators common in different API designs.

7. **Formatted Output**: `printResponse()` method provides consistent, user-friendly API response display.

---

## 🔧 Advanced Extension Patterns

### Multiple Extensions on Same Type

```dart
extension StringValidation on String {
  bool get isValidEmail => RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  bool get isValidPhone => RegExp(r'^\d{3}-\d{3}-\d{4}$').hasMatch(this);
  bool get isStrongPassword => length >= 8 && RegExp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)').hasMatch(this);
}

extension StringFormatting on String {
  String get phoneFormat {
    String digits = replaceAll(RegExp(r'\D'), '');
    if (digits.length == 10) {
      return '${digits.substring(0, 3)}-${digits.substring(3, 6)}-${digits.substring(6)}';
    }
    return this;
  }

  String get titleCase => split(' ')
      .map((word) => word.isEmpty ? '' : word[0].toUpperCase() + word.substring(1).toLowerCase())
      .join(' ');
}

void main() {
  String email = 'user@example.com';
  String phone = '1234567890';
  String password = 'MyPass123';
  String name = 'john doe';

  print('📧 Email Validation:');
  print('Email: $email - Valid: ${email.isValidEmail}');

  print('\n📞 Phone Formatting:');
  print('Phone: $phone - Formatted: ${phone.phoneFormat}');
  print('Phone valid: ${phone.phoneFormat.isValidPhone}');

  print('\n🔐 Password Strength:');
  print('Password: $password - Strong: ${password.isStrongPassword}');

  print('\n📝 Text Formatting:');
  print('Name: $name - Title Case: ${name.titleCase}');
}
```

**🔍 What This Code Does:**

This code demonstrates **multiple extensions on the same type for separation of concerns**:

1. **Logical Grouping**: Separates validation logic (`StringValidation`) from formatting logic (`StringFormatting`) for better organization.

2. **Regular Expression Patterns**: Uses regex patterns to validate complex string formats like email addresses and phone numbers.

3. **Password Strength**: Combines length checking with regex patterns to validate password complexity requirements.

4. **Data Cleaning**: `phoneFormat` getter removes non-digit characters before reformatting, handling messy input data.

5. **Conditional Formatting**: Only applies phone formatting when exactly 10 digits are present, maintaining data integrity.

6. **Consistent Naming**: Both extensions follow consistent naming conventions while serving different purposes.

7. **Reusable Patterns**: These extensions can be imported and used across multiple files and projects.

---

## 🧠 Quick Reference Guide

### Basic Extension Syntax

```dart
extension ExtensionName on TargetType {
  // Methods
  ReturnType methodName() {
    return /* some value */;
  }

  // Getters
  ReturnType get propertyName => /* computed value */;

  // Setters (only for mutable types)
  set propertyName(value) {
    // set logic
  }
}
```

### Usage Patterns

| Pattern         | Use Case          | Example                                |
| --------------- | ----------------- | -------------------------------------- |
| **Convenience** | Common operations | `string.capitalize()`, `number.square` |
| **Validation**  | Check data format | `email.isValid`, `phone.isFormatted`   |
| **Conversion**  | Transform data    | `date.friendlyFormat`, `list.toMap`    |
| **Computation** | Calculate values  | `rectangle.area`, `student.gpa`        |

---

## 🎯 When to Use Extensions

**✅ Perfect for:**

- Adding utility methods to built-in types (String, int, DateTime)
- Creating domain-specific operations
- Improving code readability with fluent APIs
- Avoiding utility classes for simple operations

**❌ Avoid when:**

- The functionality should be part of the original class
- You need to store additional state
- The operation is too complex or specialized
- You're working with interfaces that might change

---

## 🚀 Practice Challenges

Try creating these extensions:

1. **🎯 ScoreExtension on int**: Convert scores to letter grades, percentage bars
2. **🕐 TimeExtension on Duration**: Human-readable formats, time comparisons
3. **🗺️ MapExtension**: Safe getters, key transformations, filtering
4. **📊 DataExtension**: Statistical operations, data validation

---

## 🎉 Remember This!

Extension methods are like **superhero power-ups** 🦸‍♀️:

- **🔧 No Surgery Required**: Don't modify the original class
- **⚡ Instant Powers**: Add abilities right where you need them
- **🎯 Targeted**: Each extension focuses on specific functionality
- **📦 Reusable**: Once defined, use anywhere in your project
- **🧹 Clean Code**: No more utility classes cluttering your codebase

**The Magic**: You can make ANY type in Dart smarter without touching the source code!

> **Think of it like**: "Hey String, you're cool, but here are some extra tricks I taught you!" 🎪✨

Extensions make your code more **expressive**, **readable**, and **fun** to work with! 🚀
