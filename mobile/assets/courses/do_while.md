# Do-While Loops in Dart

Imagine you're at a **candy store** 🍭✨ and you want to try different candies!

You say to yourself:

> "I'll try at least ONE candy, and then I'll decide if I want more!"

So you:

1. **🍬 Try a candy first** (you always do this at least once)
2. **🤔 Check if you want more** (then decide whether to continue)
3. **🔄 Repeat if you're still hungry** (keep going if the condition is true)

👉 A **do-while loop** works exactly like this candy tasting adventure:

> It **DOES** something first, **THEN** checks **WHILE** the condition is true!

---

## 🔄 Regular While vs Do-While

### Regular While Loop (Check First, Then Do)

```dart
void main() {
  int candies = 0;

  while (candies > 0) {
    print('🍬 Eating candy #$candies');
    candies--;
  }

  print('Result: No candies eaten because we had 0 to start!');
}
```

**🔍 What This Code Does:**

This code demonstrates **condition-first execution with while loops**:

1. **Pre-Condition Check**: The `while (candies > 0)` condition is evaluated before any loop body execution occurs.

2. **Zero Execution Scenario**: Since `candies` starts at 0, the condition `0 > 0` is false from the beginning, so the loop body never executes.

3. **Skip-If-False Logic**: When the initial condition is false, the entire loop is bypassed, demonstrating while loop's "check first" behavior.

4. **No Side Effects**: No variables are modified and no actions are performed when the condition fails initially.

**Output:**

```
Result: No candies eaten because we had 0 to start!
```

### Do-While Loop (Do First, Then Check)

```dart
void main() {
  int candies = 0;

  do {
    candies++;
    print('🍬 Trying candy #$candies - it\'s delicious!');
  } while (candies < 3);

  print('🎉 Finished trying candies!');
}
```

**🔍 What This Code Does:**

This code demonstrates **action-first execution with do-while loops**:

1. **Guaranteed First Execution**: The loop body executes immediately without checking any condition first.

2. **Post-Condition Check**: The `while (candies < 3)` condition is evaluated only after the first execution completes.

3. **Minimum One Iteration**: Even if the condition would be false initially, the loop ensures at least one execution occurs.

4. **Variable Modification**: The `candies++` happens before the condition check, ensuring the loop variable changes affect the condition evaluation.

**Output:**

```
🍬 Trying candy #1 - it's delicious!
🍬 Trying candy #2 - it's delicious!
🍬 Trying candy #3 - it's delicious!
🎉 Finished trying candies!
```

**The Magic**: Do-while **always runs at least once**, even if the condition is false from the start!

---

## 🎮 Gaming Example: Player Lives

```dart
void main() {
  print('🎮 ARCADE ADVENTURE GAME 🎮\n');

  int lives = 3;
  int level = 1;

  do {
    print('💖 Starting level $level with $lives lives');
    print('🏃 Running through obstacles...');
    print('⚔️ Fighting the boss...');

    // Simulate random outcome
    bool levelCompleted = (DateTime.now().millisecond % 3) != 0;

    if (levelCompleted) {
      print('✅ Level $level completed!');
      level++;
      print('🎊 Moving to level $level!');
    } else {
      lives--;
      print('💀 Oops! Lost a life. Lives remaining: $lives');
      if (lives > 0) {
        print('🔄 Trying level $level again...');
      }
    }
    print('');

  } while (lives > 0 && level <= 5);

  if (lives == 0) {
    print('💔 Game Over! You ran out of lives.');
  } else {
    print('🏆 Congratulations! You completed all levels!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **game loop logic with compound exit conditions**:

1. **Guaranteed Game Start**: The do-while ensures the player always plays at least one level, regardless of initial conditions.

2. **Dynamic State Management**: Variables `lives` and `level` change during execution, affecting future iterations and exit conditions.

3. **Compound Exit Logic**: The loop continues while both `lives > 0` AND `level <= 5`, showing how multiple conditions control loop termination.

4. **Pseudo-Random Outcomes**: Uses `DateTime.now().millisecond % 3` to simulate random game outcomes, making each run different.

5. **Conditional Progression**: Level increases only on success, while lives decrease only on failure, modeling real game mechanics.

6. **Post-Loop Analysis**: After the loop, checks the final state to determine if the player won or lost.

---

## 🛒 Shopping Adventure

```dart
void main() {
  print('🛍️ SHOPPING MALL ADVENTURE 🛍️\n');

  double money = 100.0;
  int itemsBought = 0;
  List<String> shoppingCart = [];

  List<Map<String, dynamic>> items = [
    {'name': 'Cool T-Shirt', 'price': 25.99, 'emoji': '👕'},
    {'name': 'Sneakers', 'price': 79.99, 'emoji': '👟'},
    {'name': 'Backpack', 'price': 45.50, 'emoji': '🎒'},
    {'name': 'Sunglasses', 'price': 19.99, 'emoji': '🕶️'},
    {'name': 'Watch', 'price': 89.95, 'emoji': '⌚'},
  ];

  do {
    print('💰 Current money: \$${money.toStringAsFixed(2)}');
    print('🛒 Items in cart: ${shoppingCart.length}');
    print('');

    if (itemsBought < items.length) {
      var currentItem = items[itemsBought];
      String itemName = currentItem['name'];
      double itemPrice = currentItem['price'];
      String emoji = currentItem['emoji'];

      print('👀 Looking at: $emoji $itemName - \$${itemPrice.toStringAsFixed(2)}');

      if (money >= itemPrice) {
        money -= itemPrice;
        shoppingCart.add('$emoji $itemName');
        print('✅ Bought $itemName! Added to cart 🛒');
        print('💸 Spent \$${itemPrice.toStringAsFixed(2)}');
      } else {
        print('💸 Not enough money for $itemName');
        print('💔 Moving on to the next item...');
      }

      itemsBought++;
    } else {
      print('🏪 Visited all the stores!');
      break;
    }

    print('');

  } while (money > 0 && itemsBought < items.length);

  print('🎉 SHOPPING COMPLETE! 🎉');
  print('💰 Money left: \$${money.toStringAsFixed(2)}');
  print('🛍️ Items purchased:');

  if (shoppingCart.isEmpty) {
    print('   (No items purchased)');
  } else {
    for (int i = 0; i < shoppingCart.length; i++) {
      print('   ${i + 1}. ${shoppingCart[i]}');
    }
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **resource management with sequential processing**:

1. **Collection Processing**: Uses a List of Maps to store item data with multiple properties (name, price, emoji).

2. **Financial Transaction Logic**: Tracks money spending with precise decimal calculations using `toStringAsFixed(2)` for currency formatting.

3. **Conditional Purchasing**: Only purchases items if sufficient funds are available, demonstrating real-world shopping constraints.

4. **Dynamic Collection Building**: Builds the `shoppingCart` list progressively based on successful purchases.

5. **Index-Based Iteration**: Uses `itemsBought` as both a counter and index to process items sequentially.

6. **Multiple Exit Strategies**: Loop can end due to no money left, all items considered, or explicit break statement.

7. **State Persistence**: All changes (money, cart contents, items considered) persist across loop iterations.

---

## 🍕 Pizza Making Competition

```dart
void main() {
  print('🍕 PIZZA MAKING CHAMPIONSHIP 🍕\n');

  String playerName = 'Chef Mario';
  int pizzasMade = 0;
  int timeRemaining = 5;
  int score = 0;

  print('👨‍🍳 Welcome $playerName to the Pizza Championship!');
  print('🎯 Goal: Make as many pizzas as possible!');
  print('⏰ You have $timeRemaining rounds!\n');

  do {
    pizzasMade++;
    print('🍕 === ROUND $pizzasMade ===');
    print('👨‍🍳 $playerName is making pizza #$pizzasMade...');

    // Simulate pizza making steps
    List<String> steps = [
      '🫓 Rolling the dough...',
      '🍅 Adding tomato sauce...',
      '🧀 Sprinkling cheese...',
      '🍄 Adding toppings...',
      '🔥 Baking in the oven...'
    ];

    for (String step in steps) {
      print('   $step');
    }

    // Random pizza quality
    int quality = (DateTime.now().microsecond % 3) + 1;
    int points = 0;
    String quality_emoji = '';

    switch (quality) {
      case 1:
        points = 5;
        quality_emoji = '🙂';
        print('✅ Pizza completed! Quality: Good $quality_emoji (+$points points)');
        break;
      case 2:
        points = 8;
        quality_emoji = '😊';
        print('✅ Pizza completed! Quality: Great $quality_emoji (+$points points)');
        break;
      case 3:
        points = 10;
        quality_emoji = '🤩';
        print('✅ Pizza completed! Quality: Perfect! $quality_emoji (+$points points)');
        break;
    }

    score += points;
    timeRemaining--;

    print('📊 Current score: $score points');
    print('⏰ Rounds remaining: $timeRemaining');
    print('');

  } while (timeRemaining > 0);

  print('🏁 CHAMPIONSHIP COMPLETE! 🏁');
  print('👨‍🍳 $playerName\'s Final Results:');
  print('🍕 Pizzas made: $pizzasMade');
  print('🏆 Final score: $score points');

  if (score >= 40) {
    print('🥇 GOLD MEDAL! Amazing performance!');
  } else if (score >= 30) {
    print('🥈 SILVER MEDAL! Great job!');
  } else if (score >= 20) {
    print('🥉 BRONZE MEDAL! Nice work!');
  } else {
    print('🍕 Keep practicing, you\'ll get better!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **structured competition simulation with quality assessment**:

1. **Multi-Step Process Simulation**: Uses a List of strings to represent pizza-making steps, processed with a foreach loop.

2. **Random Quality System**: Generates pseudo-random quality ratings (1-3) using microsecond timing, creating variable outcomes.

3. **Switch-Case Scoring**: Uses switch statement to assign different point values and emojis based on quality levels.

4. **Progressive Scoring**: Accumulates score across rounds while tracking remaining rounds, simulating tournament progression.

5. **Countdown Logic**: Decrements `timeRemaining` each iteration, creating a finite competition with guaranteed end.

6. **Performance Classification**: Final scoring system categorizes performance into medal tiers based on total accumulated points.

7. **Round-Based Structure**: Each iteration represents a complete round with consistent steps but variable outcomes.

---

## 📱 User Menu System

```dart
void main() {
  print('📱 SMART PHONE SIMULATOR 📱\n');

  bool keepRunning = true;
  String currentUser = 'Alex';
  int batteryLevel = 85;

  do {
    print('📱 === PHONE MENU ===');
    print('👤 User: $currentUser');
    print('🔋 Battery: $batteryLevel%');
    print('');
    print('📋 Choose an option:');
    print('   1️⃣ Check Messages');
    print('   2️⃣ Play Music');
    print('   3️⃣ Take Photo');
    print('   4️⃣ Check Weather');
    print('   5️⃣ Power Off');
    print('');

    // Simulate user choice (random for demo)
    int userChoice = (DateTime.now().microsecond % 5) + 1;
    print('👆 You selected option $userChoice\n');

    switch (userChoice) {
      case 1:
        print('💬 CHECKING MESSAGES');
        print('📨 New message from Mom: "Don\'t forget lunch!"');
        print('📨 New message from Jake: "Want to play soccer?"');
        batteryLevel -= 2;
        break;

      case 2:
        print('🎵 PLAYING MUSIC');
        print('🎶 Now playing: "Happy Song" by The Cheerful Band');
        print('🔊 Volume: 75%');
        batteryLevel -= 5;
        break;

      case 3:
        print('📸 CAMERA MODE');
        print('📷 *Click* Photo taken!');
        print('🖼️ Saved to gallery: sunset_photo_001.jpg');
        batteryLevel -= 3;
        break;

      case 4:
        print('🌤️ WEATHER CHECK');
        print('☀️ Today: Sunny, 75°F');
        print('🌡️ Tomorrow: Partly cloudy, 72°F');
        batteryLevel -= 1;
        break;

      case 5:
        print('📴 POWERING OFF');
        print('💾 Saving data...');
        print('👋 Goodbye, $currentUser!');
        keepRunning = false;
        break;
    }

    if (keepRunning) {
      print('🔋 Battery remaining: $batteryLevel%');

      if (batteryLevel <= 10) {
        print('⚠️ LOW BATTERY WARNING!');
        print('🔌 Please charge your phone soon.');
        keepRunning = false;
      }

      print('\n⏳ Loading next menu...\n');
    }

  } while (keepRunning);

  print('\n📱 Phone session ended.');
}
```

**🔍 What This Code Does:**

This code demonstrates **interactive menu system with resource management**:

1. **Persistent Menu Display**: The do-while ensures the menu appears at least once, even if initial conditions might suggest otherwise.

2. **State-Driven Interface**: Displays current user and battery level each iteration, showing how UI updates based on changing state.

3. **Resource Consumption Modeling**: Different actions consume different amounts of battery, simulating real phone usage patterns.

4. **Multiple Exit Conditions**: Loop can end through user choice (power off) or system condition (low battery), showing flexible termination.

5. **Switch-Based Action Handling**: Uses switch statement to handle different user choices with distinct behaviors and battery impacts.

6. **Conditional Flow Control**: Uses boolean flags (`keepRunning`) to control loop continuation based on user actions or system state.

7. **Realistic Simulation**: Models actual phone behavior including battery drain, user interactions, and automatic shutdown warnings.

---

## 🎲 Dice Rolling Game

```dart
void main() {
  print('🎲 LUCKY DICE GAME 🎲\n');

  String playerName = 'Lucky Luke';
  int totalScore = 0;
  int rollCount = 0;
  bool keepPlaying = true;

  print('🎯 Goal: Roll dice until you get three 6s or decide to stop!');
  print('👤 Player: $playerName');
  print('🏁 Let\'s start rolling!\n');

  do {
    rollCount++;
    print('🎲 === ROLL #$rollCount ===');

    // Simulate rolling 3 dice
    int dice1 = (DateTime.now().microsecond % 6) + 1;
    int dice2 = ((DateTime.now().microsecond * 7) % 6) + 1;
    int dice3 = ((DateTime.now().microsecond * 13) % 6) + 1;

    print('🎲 Rolling dice...');
    print('   Dice 1: $dice1');
    print('   Dice 2: $dice2');
    print('   Dice 3: $dice3');

    int rollTotal = dice1 + dice2 + dice3;
    totalScore += rollTotal;

    print('📊 This roll: $rollTotal points');
    print('🏆 Total score: $totalScore points');

    // Check for special combinations
    if (dice1 == 6 && dice2 == 6 && dice3 == 6) {
      print('🎊 TRIPLE SIX! JACKPOT! 🎊');
      print('🏆 Bonus: +50 points!');
      totalScore += 50;
      keepPlaying = false;
    } else if (dice1 == dice2 && dice2 == dice3) {
      print('✨ Triple match! Bonus: +10 points!');
      totalScore += 10;
    } else if ((dice1 == dice2) || (dice2 == dice3) || (dice1 == dice3)) {
      print('👯 Pair found! Bonus: +5 points!');
      totalScore += 5;
    }

    // Simulate decision to continue (random for demo)
    if (keepPlaying && rollCount < 10) {
      bool wantsToContinue = (DateTime.now().microsecond % 3) != 0;
      if (wantsToContinue) {
        print('🔄 $playerName decides to roll again!');
      } else {
        print('🛑 $playerName decides to stop here.');
        keepPlaying = false;
      }
    } else if (rollCount >= 10) {
      print('🔚 Maximum rolls reached!');
      keepPlaying = false;
    }

    print('');

  } while (keepPlaying);

  print('🎮 GAME OVER! 🎮');
  print('👤 Player: $playerName');
  print('🎲 Total rolls: $rollCount');
  print('🏆 Final score: $totalScore points');

  if (totalScore >= 150) {
    print('🥇 LEGENDARY! You\'re a dice master!');
  } else if (totalScore >= 100) {
    print('🥈 EXCELLENT! Great rolling skills!');
  } else if (totalScore >= 50) {
    print('🥉 GOOD! Nice job!');
  } else {
    print('🎲 Keep practicing your dice rolling!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **complex game logic with multiple win conditions and scoring systems**:

1. **Multi-Dice Simulation**: Generates three independent random dice values using different multipliers (7, 13) to ensure variety.

2. **Pattern Recognition**: Checks for specific dice combinations (triple sixes, any triple, pairs) using logical operators and conditional chains.

3. **Tiered Scoring System**: Implements different point values for different achievements (base roll + bonus for patterns).

4. **Multiple Termination Conditions**: Game can end due to jackpot, player choice, or maximum roll limit, showing complex exit logic.

5. **Progressive Difficulty**: Uses roll count limits to prevent infinite games while maintaining player agency.

6. **Statistical Simulation**: Uses pseudo-random generation to simulate dice probability while ensuring reproducible behavior.

7. **Achievement Recognition**: Provides immediate feedback for special combinations, enhancing user engagement through reward systems.

---

## 🧠 Key Differences: While vs Do-While

### Visual Comparison

```dart
void demonstrateLoopDifference() {
  print('🔍 LOOP COMPARISON DEMO 🔍\n');

  // While loop example
  print('📋 WHILE LOOP (Check first, then do):');
  int whileCounter = 5;
  while (whileCounter < 3) {
    print('   This will never print');
    whileCounter++;
  }
  print('   While loop: Ran 0 times\n');

  // Do-while loop example
  print('📋 DO-WHILE LOOP (Do first, then check):');
  int doWhileCounter = 5;
  do {
    print('   This prints at least once!');
    doWhileCounter++;
  } while (doWhileCounter < 3);
  print('   Do-while loop: Ran 1 time\n');

  print('🎯 KEY DIFFERENCE: Do-while ALWAYS runs at least once!');
}

void main() {
  demonstrateLoopDifference();
}
```

**🔍 What This Code Does:**

This code demonstrates **the fundamental execution difference between loop types**:

1. **Condition Evaluation Timing**: Shows how while loops check conditions before execution, while do-while loops check after execution.

2. **Zero-Iteration Scenario**: Demonstrates that while loops can execute zero times when initial conditions are false.

3. **Guaranteed Execution**: Proves that do-while loops always execute at least once, regardless of initial condition values.

4. **Identical Conditions**: Uses the same false condition (`counter < 3` with counter = 5) to highlight the behavioral difference.

5. **Educational Comparison**: Provides side-by-side demonstration of when each loop type is appropriate for different scenarios.

**Output:**

```
🔍 LOOP COMPARISON DEMO 🔍

📋 WHILE LOOP (Check first, then do):
   While loop: Ran 0 times

📋 DO-WHILE LOOP (Do first, then check):
   This prints at least once!
   Do-while loop: Ran 1 time

🎯 KEY DIFFERENCE: Do-while ALWAYS runs at least once!
```

---

## 📊 Quick Reference Guide

### Do-While Syntax

```dart
do {
  // Code that runs at least once
  // This executes BEFORE checking the condition
} while (condition);  // Check condition AFTER executing
```

### When to Use Do-While

| Scenario             | Why Do-While is Perfect         |
| -------------------- | ------------------------------- |
| **User Menus**       | Always show menu at least once  |
| **Game Rounds**      | Play at least one round         |
| **Input Validation** | Ask for input at least once     |
| **Try Again Logic**  | Attempt something at least once |

### Common Patterns

```dart
// Input validation pattern
String userInput;
do {
  print('Enter your name:');
  userInput = 'SomeInput'; // Simulated input
} while (userInput.isEmpty);

// Game loop pattern
bool playAgain;
do {
  playGame();
  playAgain = askToPlayAgain();
} while (playAgain);

// Menu system pattern
int choice;
do {
  displayMenu();
  choice = getUserChoice();
  processChoice(choice);
} while (choice != 0); // 0 = exit
```

---

## 🎯 When to Use Do-While

**✅ Perfect for:**

- **User interfaces** that need to show at least once
- **Game rounds** where you play at least one game
- **Input validation** where you ask at least once
- **Menus** that should appear before checking exit condition
- **"Try again" scenarios** where you attempt at least once

**❌ Not ideal for:**

- **Counting loops** where you might not want to run (use for loops)
- **Collection processing** where the collection might be empty
- **Conditional processing** where you might skip entirely

---

## 🚀 Practice Challenges

Try creating do-while loops for these scenarios:

1. **🏦 ATM Machine**: Show menu at least once, exit on choice
2. **🎵 Music Playlist**: Play at least one song, ask to continue
3. **🎯 Dart Game**: Throw at least one dart, continue until bullseye
4. **📝 Quiz Game**: Ask at least one question, continue until wrong
5. **🍔 Restaurant Order**: Show menu at least once, order until done

---

## 🎉 Remember This!

Do-while loops are like **trying a new restaurant** 🍽️:

- **🚪 You go in at least once** (do the action first)
- **🍽️ You try the food** (execute the code)
- **🤔 Then you decide** (check the while condition)
- **🔄 You might come back** (loop continues if condition is true)

**The Magic**: Even if you're not sure you'll like it, you **try it at least once** before deciding whether to return!

That's the power of do-while - **guaranteed first execution** with **conditional repetition**! 🎪✨ 2. **🎵 Music Playlist**: Play at least one song, ask to continue 3. **🎯 Dart Game**: Throw at least one dart, continue until bullseye 4. **📝 Quiz Game**: Ask at least one question, continue until wrong 5. **🍔 Restaurant Order**: Show menu at least once, order until done

---

## 🎉 Remember This!

Do-while loops are like **trying a new restaurant** 🍽️:

- **🚪 You go in at least once** (do the action first)
- **🍽️ You try the food** (execute the code)
- **🤔 Then you decide** (check the while condition)
- **🔄 You might come back** (loop continues if condition is true)

**The Magic**: Even if you're not sure you'll like it, you **try it at least once** before deciding whether to return!

That's the power of do-while - **guaranteed first execution** with **conditional repetition**! 🎪✨
