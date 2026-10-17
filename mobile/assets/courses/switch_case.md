# Switch-Case in Dart

Imagine you're running a **magical vending machine** 🎰✨!

People walk up, press a button with a number, and get exactly what they ordered:

- Press **1** → Get a cookie 🍪
- Press **2** → Get juice 🧃
- Press **3** → Get chips 🥨
- Press anything else → "Sorry, that button doesn't work!" 😅

Instead of checking each button one by one with lots of `if-else` statements, you have a **smart system** that instantly jumps to the right choice!

👉 **Switch-case** works exactly like this magical vending machine:

> It takes one value, **instantly jumps** to the matching case, and executes that specific code!

---

## 🚫 The Problem: Too Many If-Else Statements

```dart
void processGrade(String letter) {
  // ❌ This gets messy with many options!
  if (letter == 'A') {
    print('🏆 Excellent! You got an A!');
  } else if (letter == 'B') {
    print('👍 Good job! You got a B!');
  } else if (letter == 'C') {
    print('😊 Not bad! You got a C!');
  } else if (letter == 'D') {
    print('📚 Need to study more. You got a D.');
  } else if (letter == 'F') {
    print('❌ Failed. You got an F.');
  } else {
    print('❓ Invalid grade!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **the inefficiencies and readability issues of chained if-else statements**:

1. **Repetitive Structure**: Each condition follows the same pattern of checking equality, creating verbose and repetitive code.

2. **Sequential Evaluation**: The program must check each condition in order until it finds a match, making execution slower with more conditions.

3. **Maintenance Difficulty**: Adding, removing, or modifying conditions requires careful attention to the chain structure to avoid breaking the logic.

4. **Readability Issues**: The nested structure becomes harder to scan visually as the number of conditions grows.

5. **Error-Prone**: Easy to accidentally use assignment (`=`) instead of equality (`==`) or miss an `else` keyword.

**Problems:**

- Lots of repetitive `if-else` chains! 📋
- Hard to read and maintain! 🤯
- Slow to execute with many conditions! 🐌

---

## ✅ The Solution: Switch-Case Magic

```dart
void processGrade(String letter) {
  switch (letter) {
    case 'A':
      print('🏆 Excellent! You got an A!');
      break;
    case 'B':
      print('👍 Good job! You got a B!');
      break;
    case 'C':
      print('😊 Not bad! You got a C!');
      break;
    case 'D':
      print('📚 Need to study more. You got a D.');
      break;
    case 'F':
      print('❌ Failed. You got an F.');
      break;
    default:
      print('❓ Invalid grade!');
  }
}

void main() {
  print('📊 GRADE PROCESSOR 📊\n');

  processGrade('A');
  processGrade('C');
  processGrade('F');
  processGrade('Z'); // Invalid grade
}
```

**Output:**

```
📊 GRADE PROCESSOR 📊

🏆 Excellent! You got an A!
😊 Not bad! You got a C!
❌ Failed. You got an F.
❓ Invalid grade!
```

**Perfect!** Much cleaner and easier to understand! 🎉

---

## 🍦 Ice Cream Shop Example

```dart
void orderIceCream(String flavor) {
  print('🍦 Customer orders: $flavor');

  switch (flavor.toLowerCase()) {
    case 'chocolate':
      print('🍫 Here\'s your rich chocolate ice cream!');
      print('💰 Price: \$3.50');
      break;

    case 'vanilla':
      print('🍨 Here\'s your classic vanilla ice cream!');
      print('💰 Price: \$3.00');
      break;

    case 'strawberry':
      print('🍓 Here\'s your sweet strawberry ice cream!');
      print('💰 Price: \$3.25');
      break;

    case 'mint':
      print('🌿 Here\'s your refreshing mint ice cream!');
      print('💰 Price: \$3.75');
      break;

    case 'cookies and cream':
      print('🍪 Here\'s your cookies and cream ice cream!');
      print('💰 Price: \$4.00');
      break;

    default:
      print('😢 Sorry! We don\'t have $flavor flavor.');
      print('🍦 Available flavors: Chocolate, Vanilla, Strawberry, Mint, Cookies and Cream');
  }

  print('✅ Order processed!\n');
}

void main() {
  print('🍦 MARIO\'S ICE CREAM SHOP 🍦\n');

  orderIceCream('Chocolate');
  orderIceCream('Strawberry');
  orderIceCream('Rocky Road'); // Not available
  orderIceCream('VANILLA'); // Test case-insensitive
}
```

**Output:**

```
🍦 MARIO'S ICE CREAM SHOP 🍦

🍦 Customer orders: Chocolate
🍫 Here's your rich chocolate ice cream!
💰 Price: $3.50
✅ Order processed!

🍦 Customer orders: Strawberry
🍓 Here's your sweet strawberry ice cream!
💰 Price: $3.25
✅ Order processed!

🍦 Customer orders: Rocky Road
😢 Sorry! We don't have Rocky Road flavor.
🍦 Available flavors: Chocolate, Vanilla, Strawberry, Mint, Cookies and Cream
✅ Order processed!

🍦 Customer orders: VANILLA
🍨 Here's your classic vanilla ice cream!
💰 Price: $3.00
✅ Order processed!
```

**🔍 What This Code Does:**

This code demonstrates **real-world application of switch-case with string handling**:

1. **Case Sensitivity Handling**: Uses `.toLowerCase()` to make the switch case-insensitive, improving user experience.

2. **Multiple Statements per Case**: Shows how each case can contain multiple statements before the break, allowing complex actions.

3. **Business Logic Implementation**: Each case includes both product delivery and pricing information, modeling real business operations.

4. **User-Friendly Error Handling**: The default case provides helpful feedback about available options rather than just an error message.

5. **Consistent Processing Flow**: Every path through the switch ends with the same confirmation message, ensuring consistent user feedback.

---

## 🎮 Gaming Example: Character Selection

```dart
void selectCharacter(int characterId) {
  print('🎮 Selecting character ID: $characterId\n');

  switch (characterId) {
    case 1:
      print('⚔️ WARRIOR SELECTED!');
      print('  💪 Strength: High');
      print('  🛡️ Defense: High');
      print('  ⚡ Speed: Medium');
      print('  🧠 Magic: Low');
      print('  🎯 Special: Sword Slash Attack');
      break;

    case 2:
      print('🧙‍♂️ WIZARD SELECTED!');
      print('  💪 Strength: Low');
      print('  🛡️ Defense: Low');
      print('  ⚡ Speed: Medium');
      print('  🧠 Magic: High');
      print('  🎯 Special: Fireball Spell');
      break;

    case 3:
      print('🏹 ARCHER SELECTED!');
      print('  💪 Strength: Medium');
      print('  🛡️ Defense: Medium');
      print('  ⚡ Speed: High');
      print('  🧠 Magic: Low');
      print('  🎯 Special: Multi-Arrow Shot');
      break;

    case 4:
      print('🥷 NINJA SELECTED!');
      print('  💪 Strength: Medium');
      print('  🛡️ Defense: Low');
      print('  ⚡ Speed: Very High');
      print('  🧠 Magic: Medium');
      print('  🎯 Special: Shadow Clone');
      break;

    case 5:
      print('🦸‍♀️ SUPERHERO SELECTED!');
      print('  💪 Strength: Very High');
      print('  🛡️ Defense: Very High');
      print('  ⚡ Speed: High');
      print('  🧠 Magic: High');
      print('  🎯 Special: Ultimate Power Beam');
      break;

    default:
      print('❌ INVALID CHARACTER!');
      print('🎮 Available characters:');
      print('  1️⃣ Warrior');
      print('  2️⃣ Wizard');
      print('  3️⃣ Archer');
      print('  4️⃣ Ninja');
      print('  5️⃣ Superhero');
  }

  print('\n' + '═' * 30 + '\n');
}

void main() {
  print('🎮 EPIC ADVENTURE - CHARACTER SELECT 🎮\n');

  selectCharacter(1);
  selectCharacter(3);
  selectCharacter(5);
  selectCharacter(99); // Invalid character
}
```

---

## 🌦️ Weather Response System

```dart
void checkWeather(String weather) {
  print('🌤️ Today\'s weather: $weather');

  switch (weather.toLowerCase()) {
    case 'sunny':
      print('☀️ Perfect day for outdoor activities!');
      print('🕶️ Don\'t forget sunglasses and sunscreen');
      print('🏖️ Great for: Beach, picnic, hiking');
      break;

    case 'rainy':
      print('🌧️ Stay cozy indoors today!');
      print('☂️ Take an umbrella if you go out');
      print('🏠 Great for: Reading, movies, board games');
      break;

    case 'snowy':
      print('❄️ Winter wonderland outside!');
      print('🧥 Bundle up warm with coat and gloves');
      print('⛷️ Great for: Skiing, snowman building, hot cocoa');
      break;

    case 'cloudy':
      print('☁️ Nice and mild today!');
      print('👔 Light jacket should be perfect');
      print('📷 Great for: Photography, walking, shopping');
      break;

    case 'windy':
      print('💨 Hold onto your hat!');
      print('🪁 Perfect weather for flying kites');
      print('🌊 Great for: Sailing, surfing, windmill tours');
      break;

    case 'stormy':
      print('⛈️ Stay inside and be safe!');
      print('🏠 Perfect time for indoor activities');
      print('📚 Great for: Reading, cooking, organizing');
      break;

    default:
      print('🤔 Hmm, I don\'t recognize that weather condition.');
      print('🌦️ Try: sunny, rainy, snowy, cloudy, windy, or stormy');
  }

  print('');
}

void main() {
  print('🌤️ WEATHER ASSISTANT 🌤️\n');

  checkWeather('Sunny');
  checkWeather('Rainy');
  checkWeather('Snowy');
  checkWeather('Foggy'); // Not recognized
}
```

---

## 🚦 Traffic Light Controller

```dart
void processTrafficLight(String color) {
  print('🚦 Traffic light is: $color');

  switch (color.toLowerCase()) {
    case 'red':
      print('🛑 STOP!');
      print('🚗 All vehicles must stop completely');
      print('🚶 Pedestrians can cross safely');
      print('⏰ Wait for green light');
      break;

    case 'yellow':
    case 'amber':
      print('⚠️ CAUTION!');
      print('🚗 Slow down and prepare to stop');
      print('🚶 Do not start crossing');
      print('⏰ Light will change soon');
      break;

    case 'green':
      print('✅ GO!');
      print('🚗 Vehicles may proceed safely');
      print('🚶 Do not cross - vehicles are moving');
      print('👀 Stay alert for turning vehicles');
      break;

    default:
      print('🚨 MALFUNCTION!');
      print('⚠️ Traffic light showing unknown color: $color');
      print('🛑 Treat as 4-way stop intersection');
      print('📞 Report malfunction to authorities');
  }

  print('');
}

void main() {
  print('🚦 SMART TRAFFIC CONTROLLER 🚦\n');

  processTrafficLight('Red');
  processTrafficLight('Green');
  processTrafficLight('Yellow');
  processTrafficLight('Amber'); // Same as yellow
  processTrafficLight('Purple'); // Malfunction
}
```

---

## 🏪 Restaurant Menu System

```dart
void processOrder(int menuItem) {
  print('📋 Processing order #$menuItem...\n');

  switch (menuItem) {
    case 1:
      print('🍕 MARGHERITA PIZZA');
      print('🍅 Fresh tomatoes, mozzarella, basil');
      print('💰 Price: \$12.99');
      print('⏰ Cooking time: 15 minutes');
      break;

    case 2:
      print('🍔 CLASSIC CHEESEBURGER');
      print('🥩 Beef patty, cheese, lettuce, tomato');
      print('💰 Price: \$9.99');
      print('⏰ Cooking time: 10 minutes');
      break;

    case 3:
      print('🥗 CAESAR SALAD');
      print('🥬 Romaine, croutons, parmesan, dressing');
      print('💰 Price: \$8.50');
      print('⏰ Prep time: 5 minutes');
      break;

    case 4:
      print('🍝 SPAGHETTI CARBONARA');
      print('🥓 Pasta, bacon, eggs, parmesan');
      print('💰 Price: \$13.50');
      print('⏰ Cooking time: 12 minutes');
      break;

    case 5:
      print('🐟 FISH AND CHIPS');
      print('🍟 Battered fish, french fries, tartar sauce');
      print('💰 Price: \$11.99');
      print('⏰ Cooking time: 18 minutes');
      break;

    case 6:
      print('🍰 CHOCOLATE CAKE');
      print('🍫 Rich chocolate, cream frosting');
      print('💰 Price: \$6.99');
      print('⏰ Ready immediately');
      break;

    default:
      print('❌ INVALID MENU ITEM!');
      print('📜 Our Menu:');
      print('  1️⃣ Margherita Pizza - \$12.99');
      print('  2️⃣ Classic Cheeseburger - \$9.99');
      print('  3️⃣ Caesar Salad - \$8.50');
      print('  4️⃣ Spaghetti Carbonara - \$13.50');
      print('  5️⃣ Fish and Chips - \$11.99');
      print('  6️⃣ Chocolate Cake - \$6.99');
  }

  print('\n' + '─' * 40 + '\n');
}

void main() {
  print('🍽️ WELCOME TO MARIO\'S RESTAURANT 🍽️\n');

  processOrder(1);
  processOrder(3);
  processOrder(6);
  processOrder(99); // Invalid
}
```

---

## 🎵 Music Player Controller

```dart
void handleMusicCommand(String command) {
  print('🎵 Music player received command: "$command"');

  switch (command.toLowerCase()) {
    case 'play':
      print('▶️ Playing music...');
      print('🎶 Now playing: "Awesome Song" by Cool Artist');
      break;

    case 'pause':
      print('⏸️ Music paused');
      print('🎵 Press play to continue');
      break;

    case 'stop':
      print('⏹️ Music stopped');
      print('🎵 Track returned to beginning');
      break;

    case 'next':
      print('⏭️ Skipping to next track...');
      print('🎶 Now playing: "Next Amazing Song"');
      break;

    case 'previous':
    case 'prev':
      print('⏮️ Going to previous track...');
      print('🎶 Now playing: "Previous Great Song"');
      break;

    case 'shuffle':
      print('🔀 Shuffle mode activated!');
      print('🎲 Songs will play in random order');
      break;

    case 'repeat':
      print('🔁 Repeat mode activated!');
      print('🎵 Current song will repeat');
      break;

    case 'volume up':
    case 'louder':
      print('🔊 Volume increased!');
      print('📈 Current volume: 75%');
      break;

    case 'volume down':
    case 'quieter':
      print('🔉 Volume decreased!');
      print('📉 Current volume: 25%');
      break;

    default:
      print('❓ Unknown command: "$command"');
      print('🎵 Available commands:');
      print('   ▶️ play, ⏸️ pause, ⏹️ stop');
      print('   ⏭️ next, ⏮️ previous');
      print('   🔀 shuffle, 🔁 repeat');
      print('   🔊 volume up, 🔉 volume down');
  }

  print('');
}

void main() {
  print('🎵 SMART MUSIC PLAYER 🎵\n');

  handleMusicCommand('play');
  handleMusicCommand('volume up');
  handleMusicCommand('next');
  handleMusicCommand('shuffle');
  handleMusicCommand('dance'); // Unknown command
}
```

---

## 🎯 Advanced Switch Features

### Multiple Cases for Same Action

```dart
void checkDayType(String day) {
  switch (day.toLowerCase()) {
    case 'monday':
    case 'tuesday':
    case 'wednesday':
    case 'thursday':
    case 'friday':
      print('📚 It\'s a weekday - time for work/school!');
      print('⏰ Set your alarm clock');
      break;

    case 'saturday':
    case 'sunday':
      print('🎉 It\'s the weekend - time to relax!');
      print('😴 Sleep in and have fun');
      break;

    default:
      print('❓ "$day" is not a valid day of the week');
  }
}

void main() {
  checkDayType('Monday');
  checkDayType('Saturday');
  checkDayType('Holiday'); // Invalid
}
```

**🔍 What This Code Does:**

This code demonstrates **grouping multiple cases for shared behavior**:

1. **Logical Grouping**: Groups weekdays and weekend days separately, reducing code duplication while maintaining clarity.

2. **Fall-Through Pattern**: Multiple case labels before a single action create an implicit "OR" condition.

3. **Category-Based Logic**: Models real-world scenarios where multiple inputs should trigger the same response.

4. **Maintenance Efficiency**: Adding new weekdays or weekend days only requires adding case labels, not duplicating logic.

### Switch with Numbers

```dart
void processScore(int score) {
  switch (score ~/ 10) { // Integer division to get tens digit
    case 10:
    case 9:
      print('🏆 A+ Grade! Perfect score!');
      break;
    case 8:
      print('⭐ A Grade! Excellent work!');
      break;
    case 7:
      print('👍 B Grade! Good job!');
      break;
    case 6:
      print('😊 C Grade! Not bad!');
      break;
    case 5:
      print('📚 D Grade! Need improvement');
      break;
    default:
      print('❌ F Grade! Study harder!');
  }
}

void main() {
  processScore(95);
  processScore(78);
  processScore(45);
}
```

**🔍 What This Code Does:**

This code demonstrates **mathematical preprocessing for range-based switching**:

1. **Range Conversion**: Uses integer division (`~/`) to convert continuous ranges into discrete case values.

2. **Grade Boundaries**: Models standard grading systems where score ranges map to letter grades.

3. **Mathematical Transformation**: Shows how to use switch-case for range-based logic by transforming the input.

4. **Efficient Range Handling**: Avoids complex if-else chains for range checking by preprocessing the value.

---

## 🧠 Switch vs If-Else Comparison

### When to Use Switch-Case

| **Use Switch When:**                                       | **Use If-Else When:**                    |
| ---------------------------------------------------------- | ---------------------------------------- |
| ✅ Checking **one variable** against **many exact values** | ✅ Complex **boolean conditions**        |
| ✅ Values are **constants** (strings, numbers, enums)      | ✅ **Range checks** (age > 18)           |
| ✅ **Many options** (5+ cases)                             | ✅ **Different variables** in conditions |
| ✅ Want **clean, readable** code                           | ✅ **Mathematical comparisons**          |

### Performance Example

```dart
// ✅ Good for Switch - checking exact values
void checkGrade(String letter) {
  switch (letter) {
    case 'A': print('Excellent!'); break;
    case 'B': print('Good!'); break;
    case 'C': print('Average!'); break;
    // ... more cases
  }
}

// ✅ Good for If-Else - range checking
void checkAge(int age) {
  if (age < 13) {
    print('Child');
  } else if (age < 20) {
    print('Teenager');
  } else if (age < 65) {
    print('Adult');
  } else {
    print('Senior');
  }
}
```

---

## 📚 Quick Reference Guide

### Basic Switch Syntax

```dart
switch (variable) {
  case value1:
    // Code to execute
    break;
  case value2:
    // Code to execute
    break;
  default:
    // Code if no cases match
}
```

### Important Rules

| Rule                         | Example                             | Why                              |
| ---------------------------- | ----------------------------------- | -------------------------------- |
| **Must use `break`**         | `case 'A': print('Great!'); break;` | Prevents fall-through            |
| **Values must be constants** | `case 42:` ✅ `case variable:` ❌   | Compile-time requirement         |
| **Default is optional**      | `default: print('Unknown');`        | Handles unmatched cases          |
| **Multiple cases allowed**   | `case 'Mon': case 'Tue':`           | Same action for different values |

---

## 🚀 Practice Challenges

Try creating switch statements for these scenarios:

1. **🎰 Slot Machine**: Different symbols give different rewards
2. **📱 Phone Menu**: Different numbers for different phone functions
3. **🚗 Car Gear**: Different gear positions (P, R, N, D)
4. **🎨 Art Tools**: Different brushes for different painting effects
5. **🏥 Hospital Departments**: Different departments by floor number

---

## 🎉 Remember This!

Switch-case is like having a **smart receptionist** 🏢:

- **🎯 Direct routing**: "You want accounting? Go directly to room 205!"
- **⚡ Super fast**: No need to check every single room
- **📋 Organized**: Clean, easy-to-read list of all options
- **🛡️ Safe backup**: Default case handles unexpected visitors
- **🔧 Efficient**: Perfect for exact-match scenarios

**The Magic**: Instead of checking "Is it this? Is it that? Is it this other thing?" one by one, switch-case **instantly jumps** to the right answer!

> **Think of it like**: "I have a magic elevator that goes directly to the floor you need - just tell me the floor number!" 🏗️✨

Switch-case makes your code **faster**, **cleaner**, and **easier to understand**! 🎪🚀

**Pro Tip**: Use switch-case when you're checking **one variable** against **many exact values**. Use if-else for **ranges** and **complex conditions**! 🎯
