# While Loops in Dart

Imagine you're a **security guard** 👮‍♀️ at a magical treasure vault!

Your job is simple but important:

- **Keep watching** the vault door 🚪
- **While** the door is unlocked, stay alert and guard it 👁️
- **Only stop** watching when the door gets locked 🔒

You don't know exactly how long you'll need to guard - maybe 5 minutes, maybe 5 hours! You just keep going **while** the condition is true.

👉 A **while loop** works exactly like this security guard:

> It keeps **repeating** an action **while** a condition remains true, and **stops automatically** when the condition becomes false!

---

## 🚫 The Problem: Unknown Repetitions

```dart
void main() {
  // ❌ What if we don't know exactly how many times to repeat?
  // For loops need us to know the exact count ahead of time!

  int health = 100;
  // How many times will the player take damage? We don't know!
  // for (int i = 0; i < ???; i++) // Can't use for loop here!
}
```

**🔍 What This Code Does:**

This code demonstrates **the limitations of for loops when the number of repetitions is unknown**:

1. **Unknown Iterations**: For loops require a known count, but many real-world scenarios depend on changing conditions.

2. **Dynamic Conditions**: The number of repetitions may depend on user input, random events, or external factors.

3. **Inflexibility**: For loops are not ideal when you can't predict how many times an action should repeat.

4. **Motivation for While Loops**: Highlights the need for a loop that continues based on a condition, not a fixed count.

**Problems:**

- We don't always know the exact number of repetitions! 🤷‍♀️
- Conditions might change during execution! 🔄
- Some tasks depend on user input or random events! 🎲

---

## ✅ The Solution: While Loops!

```dart
void main() {
  print('🏰 GUARDING THE MAGICAL TREASURE VAULT 🏰\n');

  bool doorIsLocked = false;
  int minutesGuarded = 0;

  print('👮‍♀️ Security guard starts shift...');
  print('🚪 Vault door status: ${doorIsLocked ? "LOCKED 🔒" : "UNLOCKED 🔓"}\n');

  while (!doorIsLocked) {
    minutesGuarded++;
    print('👁️ Minute $minutesGuarded: Still guarding the unlocked vault...');

    // Simulate random chance of door getting locked
    if (minutesGuarded >= 5) {
      doorIsLocked = true;
      print('🔒 *CLICK* The vault door automatically locks!');
    }
  }

  print('\n✅ Guard duty complete!');
  print('⏰ Total time guarded: $minutesGuarded minutes');
  print('🏰 The treasure is now secure!');
}
```

**🔍 What This Code Does:**

This code demonstrates **how while loops repeat actions until a condition changes**:

1. **Condition-Based Repetition**: The loop continues as long as the vault door is unlocked.

2. **Dynamic Exit**: The loop stops automatically when the condition (`!doorIsLocked`) becomes false.

3. **State Change Inside Loop**: The variable controlling the loop (`doorIsLocked`) is updated inside the loop body.

4. **Flexible Duration**: The number of repetitions is not fixed and depends on runtime events.

5. **Real-World Analogy**: Models scenarios where you keep doing something until a situation changes.

**Amazing!** The loop ran until the condition changed! 🎉

---

## 🔍 Anatomy of a While Loop

```dart
while (condition) {
//     │
//     └── This must be true for the loop to continue
    // Actions to repeat
}
```

### The Key Parts:

1. **🔍 Condition**: A true/false test that's checked before each loop
2. **🔄 Body**: The code that runs while the condition is true
3. **📈 Change**: Something inside must eventually change the condition to false

---

## 🎮 Gaming Examples

### Player Health System

```dart
void main() {
  print('⚔️ EPIC BATTLE SIMULATION ⚔️\n');

  String playerName = 'Sir Brave';
  int playerHealth = 100;
  int potions = 3;
  int battleRound = 0;

  print('🦸 $playerName enters the dungeon!');
  print('❤️ Starting health: $playerHealth HP');
  print('🧪 Potions available: $potions\n');

  while (playerHealth > 0 && potions > 0) {
    battleRound++;
    print('⚔️ === BATTLE ROUND $battleRound ===');

    // Player takes random damage (10-25 HP)
    int damage = 10 + (DateTime.now().millisecond % 16);
    playerHealth -= damage;

    print('💥 $playerName takes $damage damage!');
    print('❤️ Health remaining: ${playerHealth > 0 ? playerHealth : 0} HP');

    if (playerHealth <= 0) {
      print('💀 $playerName has been defeated!');
      break;
    }

    // Use potion if health is low
    if (playerHealth < 30 && potions > 0) {
      potions--;
      playerHealth += 40;
      if (playerHealth > 100) playerHealth = 100;

      print('🧪 Used a healing potion! (+40 HP)');
      print('✨ Health restored to: $playerHealth HP');
      print('🧪 Potions remaining: $potions');
    }

    print('');
  }

  if (potions == 0 && playerHealth > 0) {
    print('🏃‍♂️ $playerName retreats - out of potions!');
  }

  print('🏁 Battle ended after $battleRound rounds');
  print('📊 Final stats: $playerHealth HP, $potions potions remaining');
}
```

**🔍 What This Code Does:**

This code demonstrates **using while loops for unpredictable, condition-based game logic**:

1. **Multiple Conditions**: The loop continues as long as the player is alive and has potions.

2. **Random Events**: Damage taken each round is randomized, making the number of iterations unpredictable.

3. **Stateful Updates**: Player health and potion count are updated inside the loop.

4. **Conditional Actions**: Healing only occurs when health is low and potions are available.

5. **Game Simulation**: Models real game mechanics where outcomes depend on changing state and random events.

---

### Treasure Hunt Game

```dart
void main() {
  print('💎 TREASURE HUNT ADVENTURE 💎\n');

  bool treasureFound = false;
  int stepsWalked = 0;
  int cluesFound = 0;
  List<String> locations = [
    'Dark Forest', 'Mystic Cave', 'Ancient Ruins',
    'Dragon\'s Lair', 'Crystal Lake', 'Magic Castle'
  ];

  print('🗺️ Starting treasure hunt...');
  print('🎯 Goal: Find the legendary Golden Crown!\n');

  while (!treasureFound && stepsWalked < 100) {
    stepsWalked += 5;
    String currentLocation = locations[stepsWalked ~/ 20];

    print('🚶‍♀️ Step $stepsWalked: Exploring the $currentLocation...');

    // Random chance of finding clues or treasure
    int event = DateTime.now().microsecond % 4;

    switch (event) {
      case 0:
        cluesFound++;
        print('🔍 Found a clue! Total clues: $cluesFound');
        if (cluesFound >= 3) {
          treasureFound = true;
          print('💎 All clues collected! The Golden Crown appears!');
        }
        break;
      case 1:
        print('🕳️ Found an empty hole. Keep searching...');
        break;
      case 2:
        print('🐻 Encountered a friendly bear. It points you forward!');
        break;
      case 3:
        print('🌟 Beautiful scenery, but no treasure here.');
        break;
    }

    print('');
  }

  if (treasureFound) {
    print('🎉 SUCCESS! You found the Golden Crown!');
    print('👑 You are now the legendary treasure hunter!');
  } else {
    print('😓 Adventure ended without finding the treasure...');
    print('🔄 But you gained valuable experience!');
  }

  print('📊 Adventure summary:');
  print('   🚶‍♀️ Steps walked: $stepsWalked');
  print('   🔍 Clues found: $cluesFound');
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for adventure and exploration games**:

1. **Goal-Oriented Loop**: The loop continues until the treasure is found or steps run out.

2. **Randomized Events**: Each iteration simulates a different event, making the adventure unpredictable.

3. **Progress Tracking**: Variables track steps, clues, and treasure status.

4. **Dynamic Termination**: The loop can end early if the treasure is found.

5. **Replayability**: The randomness and conditions make each run unique.

---

## 🏪 Real-World Examples

### ATM Cash Withdrawal

```dart
void main() {
  print('🏦 FIRST NATIONAL BANK ATM 🏦\n');

  double accountBalance = 1250.75;
  bool transactionComplete = false;
  int attempts = 0;
  int maxAttempts = 3;

  print('💳 Welcome! Please enter your withdrawal amount.');
  print('💰 Account balance: \$${accountBalance.toStringAsFixed(2)}\n');

  // Simulate different withdrawal attempts
  List<double> withdrawalAttempts = [50.00, 1500.00, 200.00];

  while (!transactionComplete && attempts < maxAttempts) {
    attempts++;
    double requestedAmount = withdrawalAttempts[attempts - 1];

    print('💸 Attempt $attempts: Withdrawing \$${requestedAmount.toStringAsFixed(2)}...');

    if (requestedAmount <= 0) {
      print('❌ Invalid amount! Please enter a positive number.');
    } else if (requestedAmount > accountBalance) {
      print('❌ Insufficient funds!');
      print('💰 Available balance: \$${accountBalance.toStringAsFixed(2)}');
    } else if (requestedAmount > 500) {
      print('❌ Daily limit exceeded! Maximum withdrawal: \$500.00');
    } else {
      // Successful transaction
      accountBalance -= requestedAmount;
      transactionComplete = true;

      print('✅ Transaction successful!');
      print('💵 Dispensed: \$${requestedAmount.toStringAsFixed(2)}');
      print('💰 Remaining balance: \$${accountBalance.toStringAsFixed(2)}');
    }

    print('');
  }

  if (!transactionComplete) {
    print('🔒 Too many failed attempts. Card retained for security.');
    print('📞 Please contact customer service.');
  }

  print('🏦 Thank you for banking with us!');
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for transaction systems with limited attempts**:

1. **User Attempts**: The loop allows multiple withdrawal attempts up to a maximum.

2. **Multiple Exit Conditions**: The loop ends if the transaction is successful or attempts run out.

3. **Input Validation**: Checks for invalid amounts, insufficient funds, and daily limits.

4. **Stateful Updates**: Account balance and attempt count are updated inside the loop.

5. **Security Modeling**: Simulates real ATM behavior with card retention after too many failures.

---

### Download Progress Monitor

```dart
void main() {
  print('📥 FILE DOWNLOAD MANAGER 📥\n');

  String fileName = 'big_game.zip';
  double fileSizeMB = 2048.0; // 2GB file
  double downloadedMB = 0.0;
  bool downloadComplete = false;
  bool connectionStable = true;
  int seconds = 0;

  print('📁 Downloading: $fileName (${fileSizeMB.toStringAsFixed(0)}MB)');
  print('🌐 Connection status: ${connectionStable ? "Stable" : "Unstable"}\n');

  while (!downloadComplete && connectionStable) {
    seconds++;

    // Simulate download speed (varies between 1-10 MB/s)
    double downloadSpeed = 2 + (DateTime.now().millisecond % 8);
    downloadedMB += downloadSpeed;

    if (downloadedMB >= fileSizeMB) {
      downloadedMB = fileSizeMB;
      downloadComplete = true;
    }

    // Calculate progress
    double progress = (downloadedMB / fileSizeMB) * 100;
    String progressBar = createProgressBar(progress);

    print('⏰ ${seconds}s | $progressBar ${progress.toStringAsFixed(1)}%');
    print('📊 Downloaded: ${downloadedMB.toStringAsFixed(1)}MB of ${fileSizeMB.toStringAsFixed(0)}MB');
    print('🚀 Speed: ${downloadSpeed.toStringAsFixed(1)} MB/s');

    // Simulate occasional connection issues
    if (seconds > 10 && DateTime.now().millisecond % 50 == 0) {
      connectionStable = false;
      print('🔴 Connection lost!');
    }

    print('');
  }

  if (downloadComplete) {
    print('🎉 Download completed successfully!');
    print('⏱️ Total time: ${seconds} seconds');
    print('📁 File saved: $fileName');
  } else {
    print('❌ Download failed due to connection issues.');
    print('🔄 Please check your internet and try again.');
  }
}

String createProgressBar(double progress) {
  int filled = (progress / 5).round(); // 20 blocks total
  String bar = '█' * filled + '░' * (20 - filled);
  return '[$bar]';
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for monitoring and updating progress**:

1. **Continuous Monitoring**: The loop continues until the download is complete or the connection fails.

2. **Progress Calculation**: Updates and displays progress bar and download stats each iteration.

3. **Variable Speed**: Simulates fluctuating download speeds.

4. **Error Handling**: Handles connection loss and incomplete downloads.

5. **User Feedback**: Provides real-time updates and a summary at the end.

---

## 🍕 Restaurant Queue System

```dart
void main() {
  print('🍕 MARIO\'S PIZZA PALACE - ORDER QUEUE 🍕\n');

  List<String> orderQueue = [
    'Margherita Pizza', 'Pepperoni Pizza', 'Veggie Supreme',
    'Hawaiian Pizza', 'Meat Lovers', 'BBQ Chicken'
  ];

  bool restaurantOpen = true;
  int ordersCompleted = 0;
  int totalCookingTime = 0;

  print('👨‍🍳 Kitchen opens for business!');
  print('📋 Orders in queue: ${orderQueue.length}');
  print('⏰ Each pizza takes 8-12 minutes to make\n');

  while (orderQueue.isNotEmpty && restaurantOpen) {
    String currentOrder = orderQueue.removeAt(0);
    int cookingTime = 8 + (DateTime.now().millisecond % 5); // 8-12 minutes

    print('🍕 Now cooking: $currentOrder');
    print('⏱️ Estimated cooking time: $cookingTime minutes');

    // Simulate cooking process
    for (int minute = 1; minute <= cookingTime; minute++) {
      if (minute == 1) {
        print('🔥 Preheating oven and preparing dough...');
      } else if (minute == cookingTime ~/ 2) {
        print('🍅 Adding sauce and toppings...');
      } else if (minute == cookingTime - 1) {
        print('🧀 Adding final layer of cheese...');
      } else if (minute == cookingTime) {
        print('✅ $currentOrder is ready!');
      }
    }

    ordersCompleted++;
    totalCookingTime += cookingTime;

    print('📦 Boxing pizza for customer...');
    print('📋 Orders remaining: ${orderQueue.length}');
    print('📊 Completed orders: $ordersCompleted');

    // Check if it's time to close (after 60 minutes total)
    if (totalCookingTime >= 60) {
      restaurantOpen = false;
      print('🕘 Kitchen closing time! No new orders accepted.');
    }

    print('');
  }

  print('🏪 Kitchen Summary:');
  print('   ✅ Orders completed: $ordersCompleted');
  print('   ⏰ Total cooking time: $totalCookingTime minutes');
  if (orderQueue.isNotEmpty) {
    print('   📋 Orders remaining: ${orderQueue.length}');
    print('   🔄 These will be processed tomorrow.');
  }
  print('👨‍🍳 Great work today, kitchen team!');
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for queue processing and resource management**:

1. **Queue Processing**: Processes orders until the queue is empty or the restaurant closes.

2. **Simulated Timing**: Each pizza takes a variable amount of time, tracked and accumulated.

3. **Stateful Updates**: Orders are removed from the queue and stats are updated each iteration.

4. **Conditional Closure**: The restaurant closes after a certain total cooking time.

5. **Operational Reporting**: Provides a summary of completed and remaining orders.

---

## 🎯 User Input Simulation

### Password Verification System

```dart
void main() {
  print('🔐 SECURE LOGIN SYSTEM 🔐\n');

  String correctPassword = 'SuperSecret123!';
  bool accessGranted = false;
  int attempts = 0;
  int maxAttempts = 3;

  // Simulate different password attempts
  List<String> passwordAttempts = [
    'password123',
    'SuperSecret',
    'SuperSecret123!'
  ];

  print('🚪 Please enter your password to access the system.');
  print('⚠️ Maximum $maxAttempts attempts allowed.\n');

  while (!accessGranted && attempts < maxAttempts) {
    attempts++;
    String enteredPassword = passwordAttempts[attempts - 1];

    print('🔑 Attempt $attempts: Verifying password...');

    if (enteredPassword == correctPassword) {
      accessGranted = true;
      print('✅ Password correct! Access granted.');
      print('🎉 Welcome to the secure system!');
    } else {
      int remainingAttempts = maxAttempts - attempts;
      print('❌ Incorrect password!');

      if (remainingAttempts > 0) {
        print('⚠️ $remainingAttempts attempt(s) remaining.');

        // Give hints for common mistakes
        if (enteredPassword.length < correctPassword.length) {
          print('💡 Hint: Password might be longer than you think.');
        } else if (!enteredPassword.contains('!')) {
          print('💡 Hint: Don\'t forget special characters.');
        }
      } else {
        print('🔒 Account locked due to too many failed attempts.');
        print('📞 Contact administrator to unlock your account.');
      }
    }

    print('');
  }

  if (accessGranted) {
    print('🖥️ System access granted successfully!');
    print('📊 Login successful on attempt $attempts.');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for authentication and limited attempts**:

1. **Access Control**: The loop continues until the correct password is entered or attempts run out.

2. **Feedback and Hints**: Provides hints and feedback after each failed attempt.

3. **Security Enforcement**: Locks the account after too many failed attempts.

4. **Stateful Updates**: Tracks attempts and access status.

5. **User Experience**: Simulates real login systems with helpful messaging.

---

### Number Guessing Game

```dart
void main() {
  print('🎲 NUMBER GUESSING GAME 🎲\n');

  int secretNumber = 42; // The magic number
  bool numberGuessed = false;
  int guesses = 0;
  int maxGuesses = 7;

  // Simulate different guesses
  List<int> playerGuesses = [25, 60, 35, 48, 40, 43, 42];

  print('🎯 I\'m thinking of a number between 1 and 100!');
  print('🎮 You have $maxGuesses guesses to find it.\n');

  while (!numberGuessed && guesses < maxGuesses) {
    guesses++;
    int guess = playerGuesses[guesses - 1];

    print('🤔 Guess #$guesses: Is it $guess?');

    if (guess == secretNumber) {
      numberGuessed = true;
      print('🎉 CORRECT! You found the secret number!');
      print('⭐ You won in $guesses guess${guesses == 1 ? '' : 'es'}!');
    } else {
      int remaining = maxGuesses - guesses;

      if (guess < secretNumber) {
        print('📈 Too low! The number is higher than $guess.');
      } else {
        print('📉 Too high! The number is lower than $guess.');
      }

      if (remaining > 0) {
        print('🎯 $remaining guess${remaining == 1 ? '' : 'es'} remaining.');

        // Give helpful hints
        int difference = (guess - secretNumber).abs();
        if (difference <= 5) {
          print('🔥 You\'re very close!');
        } else if (difference <= 15) {
          print('🌡️ Getting warmer!');
        } else {
          print('🧊 Still cold, keep trying!');
        }
      } else {
        print('😔 Game over! The secret number was $secretNumber.');
      }
    }

    print('');
  }

  if (numberGuessed) {
    String performance = guesses <= 3 ? 'Excellent!' :
                        guesses <= 5 ? 'Good!' : 'Not bad!';
    print('🏆 Performance rating: $performance');
  } else {
    print('🎯 Better luck next time!');
    print('💡 Pro tip: Use the hints to narrow down your guesses.');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for interactive guessing games**:

1. **Unknown Iterations**: The loop continues until the correct number is guessed or guesses run out.

2. **Hint System**: Provides feedback and hints after each guess.

3. **Performance Tracking**: Tracks the number of guesses and rates performance.

4. **Replayability**: The logic supports different outcomes and user experiences.

5. **Game Over Handling**: Handles both win and loss scenarios gracefully.

---

## 🌡️ Monitoring Systems

### Smart Home Temperature Control

```dart
void main() {
  print('🏠 SMART HOME CLIMATE CONTROL 🏠\n');

  double currentTemp = 65.0; // Starting temperature
  double targetTemp = 72.0;   // Desired temperature
  bool systemRunning = true;
  int minutes = 0;
  double tolerance = 0.5; // Within 0.5°F is acceptable

  print('🌡️ Current temperature: ${currentTemp}°F');
  print('🎯 Target temperature: ${targetTemp}°F');
  print('🔧 System tolerance: ±${tolerance}°F\n');

  while (systemRunning && minutes < 60) { // Max 60 minutes
    minutes++;

    double tempDifference = targetTemp - currentTemp;

    if (tempDifference.abs() <= tolerance) {
      print('✅ Minute $minutes: Perfect temperature reached!');
      print('🌡️ Current: ${currentTemp.toStringAsFixed(1)}°F (Target: ${targetTemp}°F)');
      systemRunning = false;
    } else if (tempDifference > 0) {
      // Need to heat up
      currentTemp += 0.8; // Heating rate
      if (currentTemp > targetTemp) currentTemp = targetTemp;

      print('🔥 Minute $minutes: Heating... ${currentTemp.toStringAsFixed(1)}°F');
    } else {
      // Need to cool down
      currentTemp -= 0.6; // Cooling rate
      if (currentTemp < targetTemp) currentTemp = targetTemp;

      print('❄️ Minute $minutes: Cooling... ${currentTemp.toStringAsFixed(1)}°F');
    }

    // Simulate minor temperature fluctuations
    double fluctuation = (DateTime.now().microsecond % 3 - 1) * 0.1;
    currentTemp += fluctuation;
  }

  print('\n🏠 CLIMATE CONTROL SUMMARY:');
  if (systemRunning) {
    print('⏰ System timeout after $minutes minutes');
    print('🔧 Consider checking HVAC system maintenance');
  } else {
    print('✅ Target temperature achieved in $minutes minutes');
    print('💡 Energy efficient operation completed');
  }

  print('🌡️ Final temperature: ${currentTemp.toStringAsFixed(1)}°F');
}
```

**🔍 What This Code Does:**

This code demonstrates **while loops for automated control systems**:

1. **Continuous Adjustment**: The loop runs until the target temperature is reached or a timeout occurs.

2. **Dynamic Updates**: Temperature is adjusted up or down each iteration.

3. **Tolerance Handling**: Stops when the temperature is within an acceptable range.

4. **Efficiency Reporting**: Provides a summary of operation and energy efficiency.

5. **Safety Mechanism**: Includes a maximum time limit to prevent infinite loops.

---

## ⚠️ Important: Avoiding Infinite Loops

### The Danger Zone

```dart
void main() {
  print('⚠️ INFINITE LOOP WARNING EXAMPLES ⚠️\n');

  // ❌ BAD EXAMPLE 1: Condition never changes
  /*
  int count = 0;
  while (count < 5) {
    print('This will run forever!');
    // Missing: count++; to change the condition
  }
  */

  // ❌ BAD EXAMPLE 2: Wrong condition logic
  /*
  int lives = 3;
  while (lives > 0) {
    print('Player has $lives lives');
    lives++; // Wrong! This makes lives go UP, not down
  }
  */

  print('✅ SAFE EXAMPLES:\n');

  // ✅ GOOD: Counter that changes
  int count = 0;
  while (count < 3) {
    count++; // ← This ensures the loop will end
    print('✅ Safe count: $count');
  }

  // ✅ GOOD: Condition that can become false
  bool taskComplete = false;
  int attempts = 0;
  while (!taskComplete && attempts < 5) {
    attempts++;
    if (attempts >= 3) {
      taskComplete = true; // ← This ensures the loop can end
    }
    print('✅ Attempt $attempts, task complete: $taskComplete');
  }

  print('\n🛡️ Safety Tips:');
  print('1. Always modify the condition variable inside the loop');
  print('2. Add a maximum attempt counter as backup');
  print('3. Test your loops with simple examples first');
}
```

**🔍 What This Code Does:**

This code demonstrates **how to avoid infinite loops and ensure loop safety**:

1. **Bad Examples**: Shows common mistakes that lead to infinite loops (unchanging condition, wrong update).

2. **Good Examples**: Demonstrates safe patterns where the loop condition can become false.

3. **Safety Tips**: Provides practical advice for writing safe, terminating loops.

4. **Debugging Help**: Encourages testing with simple examples to catch logic errors early.

5. **Best Practices**: Reinforces the importance of updating the condition variable inside the loop.

---

## 🔄 While vs For Loops Comparison

### When to Use Each

```dart
void main() {
  print('🔄 WHILE vs FOR LOOP COMPARISON 🔄\n');

  print('📊 COUNTING EXAMPLE:');
  print('For loop (when you know the exact count):');
  for (int i = 1; i <= 5; i++) {
    print('   Count $i');
  }

  print('\nWhile loop (same result, different style):');
  int count = 1;
  while (count <= 5) {
    print('   Count $count');
    count++;
  }

  print('\n🎲 CONDITION-BASED EXAMPLE:');
  print('While loop (perfect for unknown repetitions):');

  bool coinIsHeads = false;
  int flips = 0;

  while (!coinIsHeads && flips < 10) {
    flips++;
    coinIsHeads = DateTime.now().millisecond % 2 == 0; // Random
    print('   Flip $flips: ${coinIsHeads ? "HEADS!" : "Tails"}');
  }

  if (coinIsHeads) {
    print('✅ Got heads after $flips flips!');
  } else {
    print('🔄 Reached maximum flips without heads.');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **the differences and appropriate use cases for while and for loops**:

1. **For Loops**: Best for known, fixed repetitions (counting, iterating over lists).

2. **While Loops**: Best for unknown or condition-based repetitions.

3. **Random Events**: Shows how while loops can handle unpredictable outcomes (coin flips).

4. **Decision Table**: Provides a quick guide for choosing the right loop type.

5. **Practical Examples**: Illustrates both loop types with real code.

---

## 🧠 Quick Reference Guide

### Basic While Loop Patterns

```dart
// Pattern 1: Counter-based
int i = 0;
while (i < 10) {
  // Do something
  i++; // Don't forget this!
}

// Pattern 2: Condition-based
bool isComplete = false;
while (!isComplete) {
  // Do something
  // Eventually set isComplete = true
}

// Pattern 3: Safe with backup counter
int attempts = 0;
while (!condition && attempts < maxAttempts) {
  // Do something
  attempts++;
}
```

**🔍 What This Code Does:**

This code demonstrates **common while loop patterns and their use cases**:

1. **Counter-Based Loops**: Repeat a fixed number of times with a counter.

2. **Condition-Based Loops**: Continue until a flag or condition changes.

3. **Backup Counters**: Use a maximum attempt counter for extra safety.

4. **Pattern Table**: Shows typical conditions and when to use them.

5. **Practical Reference**: Serves as a quick guide for writing safe and effective while loops.

---

### Common Conditions

| Pattern               | Code                      | Use Case                |
| --------------------- | ------------------------- | ----------------------- |
| **Counter**           | `while (i < 10)`          | Repeat N times          |
| **Boolean flag**      | `while (!done)`           | Until task complete     |
| **Value check**       | `while (health > 0)`      | Until threshold reached |
| **List processing**   | `while (list.isNotEmpty)` | Process all items       |
| **User continuation** | `while (playAgain)`       | Until user quits        |

---

## 🚀 Practice Challenges

Try creating while loops for these scenarios:

1. **🏧 ATM Menu**: Keep showing menu until user selects "Exit"
2. **🎯 Archery Practice**: Shoot arrows until you hit the bullseye
3. **📚 Library System**: Process book returns until queue is empty
4. **🌱 Plant Growth**: Water plant daily until it reaches full size
5. **🔐 Safe Cracking**: Try combinations until the safe opens

---

## 🎉 Remember This!

While loops are like having a **persistent assistant** 🤖:

- **🔍 Always checking**: "Is the condition still true?"
- **🔄 Never gives up**: Keeps going as long as needed
- **⚡ Stops automatically**: When the condition becomes false
- **🛡️ Needs safety**: Always ensure the condition can change
- **🎯 Perfect for unknowns**: When you don't know exactly how many times

**The Magic**: Unlike for loops that count from A to B, while loops keep going **until something specific happens** - just like waiting for a bus, cooking until it's done, or guarding until the danger passes!

> **Think of it like**: "Keep stirring the soup while it's still too cold" - you don't know exactly how long it will take, but you keep going until the condition (cold soup) changes! 🍲✨

While loops make your programs **flexible**, **responsive**, and **smart** enough to handle unpredictable situations! 🎪🚀

**Pro Tip**: Always ask yourself "What could make this condition false?" and make sure your loop can actually reach that state! 🎯
