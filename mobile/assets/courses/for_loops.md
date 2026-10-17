# For Loops in Dart

Imagine you're a **robot baker** 🤖👨‍🍳 in a magical bakery!

Your boss gives you instructions:

- "Bake 10 cookies, one by one" 🍪
- "Decorate 5 cupcakes in order" 🧁
- "Count down from 10 to blast off the cake rocket" 🚀

Instead of doing each task manually, you have a **special program** that can repeat actions automatically!

👉 A **for loop** is like having a **smart assistant** that counts for you and repeats tasks exactly the number of times you want!

---

## 🎯 The Problem: Repetitive Tasks

```dart
void main() {
  // ❌ This is tedious and error-prone!
  print('🍪 Baking cookie 1');
  print('🍪 Baking cookie 2');
  print('🍪 Baking cookie 3');
  print('🍪 Baking cookie 4');
  print('🍪 Baking cookie 5');
  // ... imagine doing this 100 times! 😵
}
```

**🔍 What This Code Does:**

This code demonstrates **the problems with manual repetition**:

1. **Code Duplication**: Each print statement is nearly identical, violating the DRY (Don't Repeat Yourself) principle.

2. **Maintenance Nightmare**: If you need to change the message format, you'd have to update every single line manually.

3. **Error-Prone**: Easy to make typos or skip numbers when writing repetitive code by hand.

4. **Scalability Issues**: Adding more cookies requires manually typing each new line, making it impractical for large numbers.

5. **No Dynamic Behavior**: The number of cookies is hardcoded and can't be easily changed or calculated at runtime.

**Problems:**

- Too much typing! ⌨️💥
- Easy to make mistakes 🤦‍♀️
- What if we want to bake 1000 cookies? 😱

---

## ✅ The Solution: For Loops!

```dart
void main() {
  for (int i = 1; i <= 5; i++) {
    print('🍪 Baking cookie $i');
  }
  print('🎉 All cookies are done!');
}
```

**🔍 What This Code Does:**

This code demonstrates **the power of iteration with for loops**:

1. **Automatic Counting**: The loop variable `i` automatically increments from 1 to 5, eliminating manual counting.

2. **Single Point of Control**: One loop statement controls all five iterations, making it easy to modify the count or behavior.

3. **Variable Interpolation**: Uses `$i` to dynamically insert the current loop counter into the string.

4. **Compact Code**: Replaces 5+ lines of repetitive code with just 3 lines, dramatically improving code efficiency.

5. **Scalable Solution**: Changing `<= 5` to `<= 1000` would instantly handle 1000 cookies without additional code.

**Output:**

```
🍪 Baking cookie 1
🍪 Baking cookie 2
🍪 Baking cookie 3
🍪 Baking cookie 4
🍪 Baking cookie 5
🎉 All cookies are done!
```

**Amazing!** Just 3 lines of code baked 5 cookies! 🎪

---

## 🔍 Anatomy of a For Loop

```dart
for (int i = 1; i <= 5; i++) {
//   │    │      │      │
//   │    │      │      └── Step: what to do after each loop
//   │    │      └─────────── Condition: when to stop
//   │    └────────────────── Start: where to begin counting
//   └─────────────────────── Counter: the variable that keeps track
    print('🍪 Baking cookie $i');
}
```

### The Three Parts:

1. **🏁 Start**: `int i = 1` - Begin counting at 1
2. **🔄 Condition**: `i <= 5` - Keep going while i is 5 or less
3. **📈 Step**: `i++` - Add 1 to i after each round

---

## 🧁 Bakery Examples

### Decorating Cupcakes

```dart
void main() {
  print('🧁 Welcome to Sarah\'s Cupcake Shop!\n');

  for (int cupcake = 1; cupcake <= 8; cupcake++) {
    print('🎨 Decorating cupcake #$cupcake with sprinkles ✨');
  }

  print('\n🎉 All cupcakes are beautifully decorated!');
  print('💰 Ready to sell!');
}
```

**🔍 What This Code Does:**

This code demonstrates **practical loop application in business scenarios**:

1. **Business Process Simulation**: Models a real bakery workflow where cupcakes are decorated sequentially.

2. **Professional Output**: Uses descriptive variable names (`cupcake`) and business-appropriate messaging.

3. **Progress Tracking**: Each iteration shows which specific cupcake is being processed, providing clear progress feedback.

4. **Completion Notification**: Code after the loop confirms when the batch is finished and ready for sale.

5. **Scalable Production**: Easy to adjust production volume by changing the loop limit from 8 to any number.

**Output:**

```
🧁 Welcome to Sarah's Cupcake Shop!

🎨 Decorating cupcake #1 with sprinkles ✨
🎨 Decorating cupcake #2 with sprinkles ✨
🎨 Decorating cupcake #3 with sprinkles ✨
🎨 Decorating cupcake #4 with sprinkles ✨
🎨 Decorating cupcake #5 with sprinkles ✨
🎨 Decorating cupcake #6 with sprinkles ✨
🎨 Decorating cupcake #7 with sprinkles ✨
🎨 Decorating cupcake #8 with sprinkles ✨

🎉 All cupcakes are beautifully decorated!
💰 Ready to sell!
```

### Pizza Making Assembly Line

```dart
void main() {
  print('🍕 Mario\'s Pizza Factory\n');

  for (int pizza = 1; pizza <= 6; pizza++) {
    print('👨‍🍳 Step 1: Rolling dough for pizza #$pizza');
    print('🍅 Step 2: Adding tomato sauce');
    print('🧀 Step 3: Sprinkling cheese');
    print('🔥 Step 4: Baking in the oven');
    print('✅ Pizza #$pizza is ready to serve!\n');
  }

  print('🎊 All pizzas completed! Time for lunch!');
}
```

**🔍 What This Code Does:**

This code demonstrates **complex multi-step processes within loops**:

1. **Multi-Step Workflow**: Each loop iteration contains multiple steps, showing how loops can handle complex processes.

2. **Assembly Line Modeling**: Simulates real manufacturing processes where each item goes through identical steps.

3. **Sequential Processing**: Each pizza follows the same four-step process, ensuring consistency and quality.

4. **Visual Separation**: Uses empty print statements (`\n`) to separate each pizza's production cycle for readability.

5. **Industrial Application**: Models how loops are used in manufacturing, production, and assembly line operations.

**Output:**

```
🍕 Mario's Pizza Factory

👨‍🍳 Step 1: Rolling dough for pizza #1
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #1 is ready to serve!

👨‍🍳 Step 1: Rolling dough for pizza #2
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #2 is ready to serve!

👨‍🍳 Step 1: Rolling dough for pizza #3
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #3 is ready to serve!

👨‍🍳 Step 1: Rolling dough for pizza #4
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #4 is ready to serve!

👨‍🍳 Step 1: Rolling dough for pizza #5
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #5 is ready to serve!

👨‍🍳 Step 1: Rolling dough for pizza #6
🍅 Step 2: Adding tomato sauce
🧀 Step 3: Sprinkling cheese
🔥 Step 4: Baking in the oven
✅ Pizza #6 is ready to serve!

🎊 All pizzas completed! Time for lunch!
```

---

## 🚀 Countdown Examples

### Rocket Launch Countdown

```dart
void main() {
  print('🚀 Space Mission Control\n');

  print('Preparing for rocket launch...');

  for (int countdown = 10; countdown > 0; countdown--) {
    print('⏰ T-minus $countdown seconds...');
  }

  print('🚀 BLAST OFF! 🌟');
  print('🛸 Rocket successfully launched!');
}
```

**🔍 What This Code Does:**

This code demonstrates **reverse iteration and countdown logic**:

1. **Reverse Counting**: Uses `countdown--` to decrement the counter, creating a countdown effect from 10 to 1.

2. **Greater Than Condition**: The condition `countdown > 0` ensures the loop stops before reaching 0, ending at 1.

3. **Dramatic Timing**: Simulates real countdown procedures used in rocket launches, creating suspense.

4. **Event-Driven Programming**: Shows how loops can build up to significant events (blast off) with progressive messaging.

5. **Real-World Application**: Models actual countdown timers used in aerospace, sports, and event management.

**Output:**

```
🚀 Space Mission Control

Preparing for rocket launch...
⏰ T-minus 10 seconds...
⏰ T-minus 9 seconds...
⏰ T-minus 8 seconds...
⏰ T-minus 7 seconds...
⏰ T-minus 6 seconds...
⏰ T-minus 5 seconds...
⏰ T-minus 4 seconds...
⏰ T-minus 3 seconds...
⏰ T-minus 2 seconds...
⏰ T-minus 1 seconds...
🚀 BLAST OFF! 🌟
🛸 Rocket successfully launched!
```

### New Year's Eve Countdown

```dart
void main() {
  print('🎊 NEW YEAR\'S EVE PARTY! 🎊\n');

  print('🥳 Everyone gather around!');
  print('🍾 Champagne ready!');
  print('🎆 Fireworks prepared!\n');

  for (int seconds = 5; seconds >= 1; seconds--) {
    print('🗣️ Everyone shouts: "$seconds!"');
  }

  print('🎉 HAPPY NEW YEAR! 🎉');
  print('✨ *fireworks explode* ✨');
  print('🥂 *champagne pops* 🥂');
}
```

**🔍 What This Code Does:**

This code demonstrates **countdown logic with event simulation**:

1. **Event Simulation**: Models a real-world event (New Year's Eve) where a countdown leads to a celebration.

2. **Reverse Counting**: Counts down from 5 to 1, similar to the rocket launch example, but with a different context.

3. **Thematic Messaging**: Uses emojis and festive language to create a celebratory output.

4. **Multi-Sensory Simulation**: Describes visual (fireworks), auditory (shouts), and tactile (champagne pops) elements.

5. **Cultural Event Modeling**: Represents how programming can simulate and manage real-life events and celebrations.

---

## 🎮 Gaming Examples

### Player Lives System

```dart
void main() {
  print('🎮 SUPER MARIO ADVENTURE 🎮\n');

  int totalLives = 3;

  for (int life = 1; life <= totalLives; life++) {
    print('❤️ Life $life: Mario starts the level!');
    print('🏃 Running through World 1-1...');
    print('🍄 Collected a power-up!');
    print('🏁 Level completed!\n');
  }

  print('🏆 All lives used successfully!');
  print('⭐ Mario became the champion!');
}
```

**🔍 What This Code Does:**

This code demonstrates **looping for repeated actions with game mechanics**:

1. **Life System Simulation**: Models a player life system where actions are repeated for each life.

2. **Game Progression**: Each iteration represents progressing through a level, simulating game flow.

3. **Power-Up Collection**: Demonstrates collecting items and completing levels, core mechanics in many games.

4. **Victory Condition**: Final messages celebrate the player's success, common in game design.

5. **Interactive Narrative**: Creates a mini-narrative of a game level using print statements and loops.

---

## 🌟 Different Loop Patterns

### Counting from 0 (Most Common)

```dart
void main() {
  print('📚 Reading book pages:\n');

  for (int page = 0; page < 5; page++) {
    print('📖 Reading page ${page + 1}');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **the most common loop pattern: counting from 0**:

1. **Zero-Based Indexing**: Starts counting at 0, which is common in programming, especially in array and list processing.

2. **Less Than Condition**: Uses `<` instead of `<=`, making the loop run 5 times for page numbers 0 through 4.

3. **Offset Display**: Adds 1 to the page number in the print statement to display human-readable page numbers.

4. **Common Pattern**: This is the most frequently used loop pattern, especially for iterating over arrays and collections.

5. **Foundational Concept**: Understanding this pattern is crucial for working with data structures in programming.

### Counting from 1

```dart
void main() {
  print('🎪 Circus performance:\n');

  for (int act = 1; act <= 4; act++) {
    print('🎭 Act $act: Amazing performance!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **counting from 1, often used in user-facing applications**:

1. **User-Friendly Counting**: Starts at 1, which is more natural for user-facing applications like displaying acts in a circus.

2. **Less Common in Code**: While common in user interfaces, it's less common in the underlying code, which often starts at 0.

3. **Simple Iteration**: Iterates from 1 to 4, showing each act in a performance, typical in event scheduling and display.

4. **Direct Mapping**: Each loop iteration directly maps to a real-world item (circus act), making the code easy to understand.

5. **Foundational for Events**: Useful pattern for iterating over a fixed number of events, tasks, or items.

### Counting by 2s (Even Numbers)

```dart
void main() {
  print('👥 Calling even-numbered students:\n');

  for (int student = 2; student <= 10; student += 2) {
    print('📢 Student #$student, please come forward!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **custom increment patterns**:

1. **Custom Starting Point**: Begins at 2 instead of the typical 0 or 1, showing flexibility in loop initialization.

2. **Custom Increment**: Uses `+= 2` instead of `++` to skip odd numbers and only process even values.

3. **Mathematical Patterns**: Generates the sequence 2, 4, 6, 8, 10, useful for mathematical operations and data filtering.

4. **Selective Processing**: Shows how loops can process only specific items from a sequence rather than every item.

5. **Educational Applications**: Perfect for teaching number patterns, skip counting, and mathematical sequences.

**Output:**

```
👥 Calling even-numbered students:

📢 Student #2, please come forward!
📢 Student #4, please come forward!
📢 Student #6, please come forward!
📢 Student #8, please come forward!
📢 Student #10, please come forward!
```

### Counting by 5s

```dart
void main() {
  print('💰 Counting money in $5 bills:\n');

  for (int amount = 5; amount <= 50; amount += 5) {
    print('💵 $amount dollars counted!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **counting with a custom step size**:

1. **Custom Step Size**: Increments by 5 each time, showing how to control the loop counter's growth.

2. **Range Limitation**: Stops at 50, demonstrating how to limit the range of values processed by the loop.

3. **Financial Calculations**: Simulates counting money, a practical application of loops in financial software.

4. **Efficient Counting**: Quickly counts large quantities by skipping unnecessary numbers.

5. **Real-World Application**: Models actual counting scenarios in finance, inventory, and resource management.

---

## 🏫 Educational Examples

### Multiplication Table

```dart
void main() {
  int number = 7;
  print('📊 Multiplication Table for $number:\n');

  for (int i = 1; i <= 10; i++) {
    int result = number * i;
    print('$number × $i = $result');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **mathematical computation within loops**:

1. **Variable Calculation**: Performs multiplication inside the loop, calculating `number * i` for each iteration.

2. **Educational Formatting**: Uses mathematical symbols (×, =) to present information in familiar educational format.

3. **Dynamic Results**: Each iteration produces different results based on the current loop counter value.

4. **Configurable Base**: The `number` variable can be changed to generate any multiplication table.

5. **Mathematical Learning**: Provides a practical programming example that directly supports mathematics education.

**Output:**

```
📊 Multiplication Table for 7:

7 × 1 = 7
7 × 2 = 14
7 × 3 = 21
7 × 4 = 28
7 × 5 = 35
7 × 6 = 42
7 × 7 = 49
7 × 8 = 56
7 × 9 = 63
7 × 10 = 70
```

### Grade Calculator

```dart
void main() {
  print('🎓 CLASS GRADE REPORT 🎓\n');

  List<String> students = ['Alice', 'Bob', 'Charlie', 'Diana'];
  List<int> grades = [95, 87, 92, 88];

  int totalGrades = 0;

  for (int i = 0; i < students.length; i++) {
    print('📝 ${students[i]}: ${grades[i]}% ${getGradeLetter(grades[i])}');
    totalGrades += grades[i];
  }

  double average = totalGrades / students.length;
  print('\n📊 Class Average: ${average.toStringAsFixed(1)}%');
  print('🏆 Overall Performance: ${getGradeLetter(average.round())}');
}

String getGradeLetter(int grade) {
  if (grade >= 90) return '(A)';
  if (grade >= 80) return '(B)';
  if (grade >= 70) return '(C)';
  if (grade >= 60) return '(D)';
  return '(F)';
}
```

**🔍 What This Code Does:**

This code demonstrates **data processing with accumulation and analysis**:

1. **Data Accumulation**: Uses `totalGrades += grades[i]` to sum all grades while iterating through the loop.

2. **Function Integration**: Calls `getGradeLetter()` function within the loop to convert numeric grades to letter grades.

3. **Post-Loop Calculation**: Performs average calculation after the loop completes, using accumulated data.

4. **Statistical Analysis**: Provides both individual student performance and class-wide statistics.

5. **Real-World Application**: Models actual grade reporting systems used in educational institutions.

---

## 🎨 Art and Patterns

### Drawing Stars Pattern

```dart
void main() {
  print('✨ STAR PATTERN GENERATOR ✨\n');

  for (int row = 1; row <= 5; row++) {
    String stars = '';
    for (int star = 1; star <= row; star++) {
      stars += '⭐';
    }
    print('Row $row: $stars');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **nested loops and string building**:

1. **Nested Loop Structure**: The outer loop controls rows while the inner loop builds stars for each row.

2. **Progressive Pattern**: Each row contains one more star than the previous, creating a triangular pattern.

3. **String Concatenation**: Builds the star string incrementally using `+=` operator within the inner loop.

4. **Visual Pattern Generation**: Creates ASCII art patterns that demonstrate mathematical progressions.

5. **Algorithm Foundations**: Introduces concepts used in graphics programming and pattern generation.

**Output:**

```
✨ STAR PATTERN GENERATOR ✨

Row 1: ⭐
Row 2: ⭐⭐
Row 3: ⭐⭐⭐
Row 4: ⭐⭐⭐⭐
Row 5: ⭐⭐⭐⭐⭐
```

### Christmas Tree

```dart
void main() {
  print('🎄 CHRISTMAS TREE GENERATOR 🎄\n');

  // Tree top
  for (int level = 1; level <= 4; level++) {
    // Print spaces for centering
    String spaces = ' ' * (4 - level);
    // Print stars
    String stars = '🌟' * level;
    print('$spaces$stars');
  }

  // Tree trunk
  print('   🟫'); // Trunk
  print('\n🎁 Presents under the tree! 🎁');
}
```

**🔍 What This Code Does:**

This code demonstrates **pattern generation with nested loops and string manipulation**:

1. **Hierarchical Pattern**: Creates a top-down pattern where each level of the tree is narrower than the one below.

2. **String Multiplication**: Uses string multiplication (`'🌟' * level`) to create repeated characters for each level.

3. **Dynamic Spacing**: Calculates leading spaces dynamically to center the tree shape.

4. **Visual Art Generation**: Produces a recognizable shape (Christmas tree) using simple text characters.

5. **Creative Coding**: Shows how programming can be used for creative expression, not just logical or mathematical tasks.

---

## 📱 Real App Examples

### Social Media Posts

```dart
void main() {
  print('📱 SOCIAL MEDIA FEED 📱\n');

  List<String> users = ['@sarah_coder', '@mike_designer', '@emma_artist'];
  List<String> posts = [
    'Just finished my first Dart app! 🎉',
    'New logo design for a local coffee shop ☕',
    'Painted a beautiful sunset today 🌅'
  ];

  for (int i = 0; i < users.length; i++) {
    print('👤 ${users[i]}');
    print('💬 ${posts[i]}');
    print('❤️ 24 likes  💬 5 comments  🔄 3 shares');
    print('⏰ 2 hours ago\n');
  }

  print('📲 End of feed - Pull to refresh!');
}
```

**🔍 What This Code Does:**

This code demonstrates **iterating over collections to display related data**:

1. **User Post Simulation**: Models how social media posts are displayed in a feed, with user information and post content.

2. **Multi-Array Coordination**: Uses the same index to access related data in multiple arrays (users, posts).

3. **Engagement Metrics**: Includes likes, comments, and shares to simulate real social media post engagement.

4. **Time Stamping**: Adds a time element to each post, common in social media applications.

5. **Dynamic Content Display**: Easily adaptable to display any number of posts by changing the arrays' content.

---

## 🧠 Loop Control Tips

### Early Exit with Break

```dart
void main() {
  print('🔍 Finding the first even number:\n');

  for (int number = 1; number <= 10; number++) {
    print('Checking $number...');

    if (number % 2 == 0) {
      print('✅ Found first even number: $number');
      break; // Exit the loop early
    }
  }

  print('🎯 Search completed!');
}
```

**🔍 What This Code Does:**

This code demonstrates **loop control flow with early termination**:

1. **Break Statement**: Uses `break` to immediately exit the loop when the first even number is found.

2. **Conditional Exit**: Combines if-statement with break to create search logic that stops at the first match.

3. **Efficiency Optimization**: Avoids unnecessary iterations once the desired result is found, improving performance.

4. **Search Algorithm Foundation**: Shows basic pattern used in search algorithms and data processing.

5. **Resource Conservation**: Demonstrates how to prevent loops from continuing when further processing is unnecessary.

### Skip with Continue

```dart
void main() {
  print('🎵 Playing only odd-numbered songs:\n');

  for (int song = 1; song <= 8; song++) {
    if (song % 2 == 0) {
      continue; // Skip even numbers
    }

    print('🎶 Now playing song #$song');
  }

  print('🎉 Playlist finished!');
}
```

**🔍 What This Code Does:**

This code demonstrates **selective processing with continue statement**:

1. **Continue Statement**: Uses `continue` to skip the rest of the current iteration and move to the next loop cycle.

2. **Conditional Skipping**: Combines if-statement with continue to filter out even-numbered items.

3. **Selective Processing**: Processes only items that meet specific criteria (odd numbers) while skipping others.

4. **Filtering Pattern**: Shows a common pattern for processing subsets of data within loops.

5. **Flow Control**: Demonstrates how to control execution flow without breaking out of the entire loop.

---

## 📊 Loop Comparison Guide

### Different Starting Points

| Pattern        | Code                           | Output  |
| -------------- | ------------------------------ | ------- |
| **Start at 0** | `for (int i = 0; i < 3; i++)`  | 0, 1, 2 |
| **Start at 1** | `for (int i = 1; i <= 3; i++)` | 1, 2, 3 |
| **Countdown**  | `for (int i = 3; i > 0; i--)`  | 3, 2, 1 |

### Different Step Sizes

| Pattern        | Code                               | Output            |
| -------------- | ---------------------------------- | ----------------- |
| **Count by 1** | `for (int i = 0; i < 5; i++)`      | 0, 1, 2, 3, 4     |
| **Count by 2** | `for (int i = 0; i < 10; i += 2)`  | 0, 2, 4, 6, 8     |
| **Count by 5** | `for (int i = 5; i <= 25; i += 5)` | 5, 10, 15, 20, 25 |

---

## 🚀 Practice Challenges

Try creating for loops for these scenarios:

1. **🏪 Store Inventory**: Print 15 items with prices
2. **📅 Calendar**: Show days 1-31 for a month
3. **🌡️ Temperature**: Show hourly temps for 24 hours
4. **🎲 Dice Roll**: Simulate rolling a die 10 times
5. **📚 Library**: Check out 20 books with titles

---

## 🎯 Common Patterns to Remember

### The "Less Than" Pattern (Most Popular)

```dart
for (int i = 0; i < 5; i++) {
  // Runs 5 times: 0, 1, 2, 3, 4
}
```

### The "Less Than or Equal" Pattern

```dart
for (int i = 1; i <= 5; i++) {
  // Runs 5 times: 1, 2, 3, 4, 5
}
```

### The "Countdown" Pattern

```dart
for (int i = 5; i > 0; i--) {
  // Runs 5 times: 5, 4, 3, 2, 1
}
```

---

## 🎉 Remember This!

For loops are like having a **super-efficient assistant** 🤖:

- **🏁 Start**: Tell them where to begin counting
- **🔄 Condition**: Tell them when to stop
- **📈 Step**: Tell them how to count (by 1s, 2s, backwards, etc.)
- **⚡ Action**: Tell them what to do each time

**The Magic**: Instead of doing boring repetitive work yourself, the for loop does it perfectly every time!

> **Think of it like**: "Hey computer, count from 1 to 10, and each time you count, bake me a cookie!" 🍪

And just like that - 10 cookies appear! That's the power of for loops! ✨🎪
