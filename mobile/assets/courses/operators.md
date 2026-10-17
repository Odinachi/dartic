# Operators in Dart

Imagine you're the **captain of a magical calculator spaceship** 🚀🧮!

Your spaceship has different **control buttons** that can:

- ➕ **Add** fuel tanks together
- ➖ **Remove** damaged parts
- ✖️ **Multiply** your speed boost
- ➗ **Split** treasure equally among crew
- 🔍 **Compare** distances to planets
- 🎯 **Make decisions** about which route to take

👉 **Operators** are exactly like those magical control buttons:

> They tell Dart **what action to perform** on your data - like a remote control for your code!

---

## 🧮 Arithmetic Operators: The Math Wizards

### Basic Math Operations

```dart
void main() {
  print('🧮 MAGICAL CALCULATOR SPACESHIP 🧮\n');

  // Fuel calculations
  int fuelTank1 = 150;
  int fuelTank2 = 200;
  int totalFuel = fuelTank1 + fuelTank2;

  print('⛽ Tank 1: $fuelTank1 units');
  print('⛽ Tank 2: $fuelTank2 units');
  print('🚀 Total fuel: $totalFuel units');

  // Distance traveled
  double speed = 25.5;
  double time = 4.0;
  double distance = speed * time;

  print('\n🌌 Journey Report:');
  print('⚡ Speed: $speed units/hour');
  print('⏰ Time: $time hours');
  print('📏 Distance traveled: $distance units');

  // Sharing treasure
  int treasureCoins = 1000;
  int crewMembers = 4;
  int coinsPerPerson = treasureCoins ~/ crewMembers; // Integer division
  int leftoverCoins = treasureCoins % crewMembers;   // Remainder

  print('\n💰 Treasure Distribution:');
  print('🪙 Total coins: $treasureCoins');
  print('👥 Crew members: $crewMembers');
  print('💎 Coins per person: $coinsPerPerson');
  print('🎁 Leftover coins: $leftoverCoins');
}
```

**🔍 What This Code Does:**

This code demonstrates **practical applications of arithmetic operators in real-world scenarios**:

1. **Addition for Aggregation**: Uses `+` to combine fuel from multiple tanks, showing how addition accumulates quantities.

2. **Multiplication for Calculations**: Demonstrates `*` operator for computing distance using the physics formula `distance = speed × time`.

3. **Integer Division for Fair Distribution**: Uses `~/` to divide treasure equally among crew members, ensuring whole number results.

4. **Modulo for Remainders**: Uses `%` operator to find leftover coins that can't be divided evenly, useful in distribution problems.

5. **Mixed Data Types**: Shows how arithmetic works with both integers and doubles, with Dart handling type conversions automatically.

---

### All Arithmetic Operators

```dart
void main() {
  print('🎪 ARITHMETIC OPERATORS CIRCUS 🎪\n');

  int a = 17;
  int b = 5;

  print('🎭 Our magical numbers: a = $a, b = $b\n');

  print('➕ Addition: $a + $b = ${a + b}');
  print('➖ Subtraction: $a - $b = ${a - b}');
  print('✖️ Multiplication: $a * $b = ${a * b}');
  print('➗ Division: $a / $b = ${a / b}');
  print('🔢 Integer Division: $a ~/ $b = ${a ~/ b}');
  print('📦 Modulo (Remainder): $a % $b = ${a % b}');

  print('\n🎯 Special Cases:');
  print('🤖 Increment: a++ makes a become ${++a}');
  print('⬇️ Decrement: a-- makes a become ${--a}');
}
```

**🔍 What This Code Does:**

This code demonstrates **the complete set of arithmetic operators with concrete examples**:

1. **Operator Comparison**: Shows all arithmetic operators applied to the same values (17 and 5) for easy comparison.

2. **Division Types**: Illustrates the difference between regular division (`/`) which returns a double, and integer division (`~/`) which returns an integer.

3. **Modulo Understanding**: Demonstrates how modulo (`%`) returns the remainder after division (17 ÷ 5 = 3 remainder 2).

4. **Increment/Decrement**: Shows pre-increment (`++a`) and pre-decrement (`--a`) operators that modify variables in place.

5. **Type Awareness**: Demonstrates how different operators produce different result types (int vs double).

---

## 🔍 Comparison Operators: The Decision Makers

```dart
void main() {
  print('⚖️ SPACE TRAFFIC CONTROL ⚖️\n');

  int spaceshipSpeed = 75;
  int speedLimit = 60;
  int minimumSpeed = 30;

  print('🚀 Spaceship speed: $spaceshipSpeed mph');
  print('🚦 Speed limit: $speedLimit mph');
  print('🐌 Minimum speed: $minimumSpeed mph\n');

  // Comparison checks
  print('🔍 SPEED ANALYSIS:');
  print('Is speeding? ${spaceshipSpeed > speedLimit}');
  print('Within limit? ${spaceshipSpeed <= speedLimit}');
  print('Too slow? ${spaceshipSpeed < minimumSpeed}');
  print('Exactly at limit? ${spaceshipSpeed == speedLimit}');
  print('Different from limit? ${spaceshipSpeed != speedLimit}');
  print('Fast enough? ${spaceshipSpeed >= minimumSpeed}');

  // Traffic decision
  print('\n🚨 TRAFFIC CONTROL DECISION:');
  if (spaceshipSpeed > speedLimit) {
    print('⚠️ SLOW DOWN! You are speeding!');
  } else if (spaceshipSpeed < minimumSpeed) {
    print('📢 SPEED UP! You are too slow!');
  } else {
    print('✅ Perfect speed! Safe travels!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **comparison operators in a traffic control system**:

1. **Range Checking**: Uses `>` and `<` to determine if values fall outside acceptable ranges (speed limits).

2. **Boundary Testing**: Uses `<=` and `>=` to include boundary values in range checks.

3. **Equality Testing**: Uses `==` to check for exact matches and `!=` to check for differences.

4. **Boolean Results**: All comparison operations return boolean values that can be used in conditional statements.

5. **Real-World Logic**: Models actual traffic control decisions based on speed comparisons.

6. **Conditional Flow**: Shows how comparison results drive program flow through if-else statements.

---

## 🧠 Logical Operators: The Smart Decision System

```dart
void main() {
  print('🎮 ADVENTURE GAME QUEST SYSTEM 🎮\n');

  // Player stats
  int playerLevel = 15;
  bool hasKey = true;
  bool hasMap = false;
  int goldCoins = 250;

  // Quest requirements
  int requiredLevel = 10;
  int questCost = 200;

  print('👤 PLAYER STATUS:');
  print('📊 Level: $playerLevel');
  print('🗝️ Has key: $hasKey');
  print('🗺️ Has map: $hasMap');
  print('💰 Gold coins: $goldCoins\n');

  // Logical operations
  print('🧠 QUEST ELIGIBILITY CHECKS:');

  // AND operator
  bool canEnterDungeon = hasKey && (playerLevel >= requiredLevel);
  print('🏰 Can enter dungeon: $canEnterDungeon');
  print('   (Needs key AND level $requiredLevel+)');

  // OR operator
  bool hasNavigationTool = hasKey || hasMap;
  print('🧭 Has navigation tool: $hasNavigationTool');
  print('   (Has key OR map)');

  // NOT operator
  bool needsMap = !hasMap;
  print('🗺️ Needs to buy map: $needsMap');
  print('   (Does NOT have map)');

  // Complex logical expression
  bool canStartEpicQuest = (playerLevel >= requiredLevel) &&
                          (hasKey || hasMap) &&
                          (goldCoins >= questCost);
  print('⚔️ Can start epic quest: $canStartEpicQuest');
  print('   (High level AND navigation tool AND enough gold)');

  // Quest recommendations
  print('\n🎯 QUEST RECOMMENDATIONS:');
  if (canStartEpicQuest) {
    print('🌟 Ready for the EPIC QUEST! Good luck, hero!');
  } else {
    print('📋 Complete these tasks first:');
    if (playerLevel < requiredLevel) {
      print('   📈 Gain ${requiredLevel - playerLevel} more levels');
    }
    if (!hasKey && !hasMap) {
      print('   🗝️ Find a key OR 🗺️ buy a map');
    }
    if (goldCoins < questCost) {
      print('   💰 Earn ${questCost - goldCoins} more gold coins');
    }
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **complex logical decision-making using boolean operators**:

1. **AND Logic (`&&`)**: Requires ALL conditions to be true, used for mandatory requirements like having both a key AND sufficient level.

2. **OR Logic (`||`)**: Requires ANY condition to be true, used for alternative requirements like having EITHER a key OR a map.

3. **NOT Logic (`!`)**: Inverts boolean values, useful for checking what's missing or opposite conditions.

4. **Complex Expressions**: Combines multiple logical operators with parentheses to create sophisticated eligibility rules.

5. **Real Game Logic**: Models actual game mechanics where players must meet multiple criteria to access content.

6. **Readable Code**: Uses descriptive variable names and comments to make complex logical expressions understandable.

---

## ⚡ Assignment Operators: The Power-Up System

```dart
void main() {
  print('⚡ SUPERHERO POWER-UP SYSTEM ⚡\n');

  int strength = 50;
  int speed = 30;
  int intelligence = 40;

  print('🦸‍♀️ INITIAL HERO STATS:');
  print('💪 Strength: $strength');
  print('⚡ Speed: $speed');
  print('🧠 Intelligence: $intelligence\n');

  print('🔋 APPLYING POWER-UPS:\n');

  // Basic assignment
  int energy = 100;
  print('⚡ Energy charged to: $energy');

  // Add and assign
  strength += 20;  // Same as: strength = strength + 20
  print('💪 Strength boosted by 20! New strength: $strength');

  // Subtract and assign
  energy -= 30;   // Same as: energy = energy - 30
  print('⚡ Energy consumed (-30)! Remaining: $energy');

  // Multiply and assign
  speed *= 2;     // Same as: speed = speed * 2
  print('🏃 Speed doubled! New speed: $speed');

  // Divide and assign
  intelligence ~/= 2;  // Integer division and assign
  print('🧠 Intelligence halved (thinking too hard)! New intelligence: $intelligence');

  // Modulo and assign
  int lives = 7;
  lives %= 3;     // Same as: lives = lives % 3
  print('❤️ Lives after modulo: $lives');

  print('\n🎊 FINAL HERO STATS:');
  print('💪 Final Strength: $strength');
  print('⚡ Final Speed: $speed');
  print('🧠 Final Intelligence: $intelligence');
  print('⚡ Final Energy: $energy');
  print('❤️ Final Lives: $lives');

  // Power level calculation
  int totalPower = strength + speed + intelligence;
  print('\n🌟 TOTAL POWER LEVEL: $totalPower');

  if (totalPower >= 150) {
    print('🏆 LEGENDARY HERO STATUS ACHIEVED!');
  } else if (totalPower >= 100) {
    print('⭐ SUPER HERO STATUS!');
  } else {
    print('📈 Keep training to become stronger!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **assignment operators as shortcuts for common update patterns**:

1. **Compound Assignment**: Shows how `+=`, `-=`, `*=`, etc. are shorthand for longer expressions that modify variables.

2. **Code Efficiency**: Demonstrates cleaner, more readable code compared to writing `variable = variable + value`.

3. **Different Operations**: Shows compound assignment works with all arithmetic operators (`+`, `-`, `*`, `/`, `~/`, `%`).

4. **Progressive Changes**: Models how game characters' stats evolve over time through various power-ups and events.

5. **Integer Division Assignment**: Uses `~/=` to show compound assignment with integer division, useful for calculations that need whole numbers.

6. **Practical Applications**: Each example represents real scenarios like consuming energy, gaining experience, or applying effects.

---

## 🛒 Real-World Example: Smart Shopping Cart

```dart
void main() {
  print('🛒 SMART SHOPPING CART SYSTEM 🛒\n');

  // Item prices
  double laptopPrice = 999.99;
  double mousePrice = 29.99;
  double keyboardPrice = 79.99;

  // Shopping cart
  int laptopQuantity = 1;
  int mouseQuantity = 2;
  int keyboardQuantity = 1;

  // Customer info
  double customerBudget = 1200.00;
  bool hasPremiumMembership = true;
  bool hasFreShippingCoupon = false;

  print('🛍️ CART CONTENTS:');
  print('💻 Laptop: $laptopQuantity × \$${laptopPrice} = \$${laptopQuantity * laptopPrice}');
  print('🖱️ Mouse: $mouseQuantity × \$${mousePrice} = \$${mouseQuantity * mousePrice}');
  print('⌨️ Keyboard: $keyboardQuantity × \$${keyboardPrice} = \$${keyboardQuantity * keyboardPrice}');

  // Calculate totals
  double subtotal = (laptopQuantity * laptopPrice) +
                   (mouseQuantity * mousePrice) +
                   (keyboardQuantity * keyboardPrice);

  print('\n💰 PRICE BREAKDOWN:');
  print('Subtotal: \$${subtotal.toStringAsFixed(2)}');

  // Apply discounts
  double discountRate = 0.0;
  if (hasPremiumMembership && subtotal >= 1000) {
    discountRate = 0.10; // 10% premium discount
  } else if (hasPremiumMembership) {
    discountRate = 0.05; // 5% premium discount
  }

  double discountAmount = subtotal * discountRate;
  double afterDiscount = subtotal - discountAmount;

  if (discountAmount > 0) {
    print('🎟️ Premium discount (${(discountRate * 100).toStringAsFixed(0)}%): -\$${discountAmount.toStringAsFixed(2)}');
    print('💵 After discount: \$${afterDiscount.toStringAsFixed(2)}');
  }

  // Calculate shipping
  double shippingCost = 0.0;
  if (!hasFreShippingCoupon && afterDiscount < 500) {
    shippingCost = 25.00;
  }

  double finalTotal = afterDiscount + shippingCost;

  if (shippingCost > 0) {
    print('🚚 Shipping cost: \$${shippingCost.toStringAsFixed(2)}');
  } else {
    print('🚚 Shipping: FREE! 🎉');
  }

  print('💳 FINAL TOTAL: \$${finalTotal.toStringAsFixed(2)}');

  // Check affordability
  print('\n💰 BUDGET CHECK:');
  print('Customer budget: \$${customerBudget.toStringAsFixed(2)}');
  print('Final total: \$${finalTotal.toStringAsFixed(2)}');

  bool canAfford = finalTotal <= customerBudget;
  double difference = (customerBudget - finalTotal).abs();

  if (canAfford) {
    print('✅ Purchase approved!');
    print('💰 Money remaining: \$${difference.toStringAsFixed(2)}');

    // Loyalty points calculation
    int loyaltyPoints = (finalTotal / 10).floor(); // 1 point per $10
    if (hasPremiumMembership) {
      loyaltyPoints *= 2; // Double points for premium members
    }
    print('⭐ Loyalty points earned: $loyaltyPoints');
  } else {
    print('❌ Insufficient funds!');
    print('💸 Need \$${difference.toStringAsFixed(2)} more');

    // Suggest removing items
    if (keyboardQuantity > 0) {
      double newTotal = finalTotal - keyboardPrice;
      if (newTotal <= customerBudget) {
        print('💡 Suggestion: Remove keyboard to afford the rest!');
      }
    }
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **comprehensive e-commerce calculations using multiple operator types**:

1. **Financial Calculations**: Uses arithmetic operators for subtotals, discounts, and shipping calculations common in e-commerce.

2. **Conditional Logic**: Combines logical operators to determine discount eligibility based on membership and purchase amount.

3. **Tiered Pricing**: Shows how comparison operators implement business rules like minimum purchase amounts for free shipping.

4. **Error Prevention**: Uses `.abs()` method and careful comparisons to handle edge cases in financial calculations.

5. **Loyalty Programs**: Demonstrates compound assignment (`*= 2`) for bonus calculations in customer reward systems.

6. **Business Intelligence**: Shows how operators enable complex business logic like suggesting alternative purchases when budgets are exceeded.

---

## 🎲 Gaming Example: Dice Combat System

```dart
void main() {
  print('⚔️ EPIC DICE COMBAT SYSTEM ⚔️\n');

  // Player stats
  String playerName = 'Sir Dartington';
  int playerHealth = 100;
  int playerAttack = 25;
  int playerDefense = 15;

  // Enemy stats
  String enemyName = 'Code Dragon';
  int enemyHealth = 120;
  int enemyAttack = 30;
  int enemyDefense = 10;

  print('🏟️ BATTLE ARENA');
  print('👤 $playerName: ❤️$playerHealth ⚔️$playerAttack 🛡️$playerDefense');
  print('🐉 $enemyName: ❤️$enemyHealth ⚔️$enemyAttack 🛡️$enemyDefense\n');

  int round = 1;

  while (playerHealth > 0 && enemyHealth > 0) {
    print('⚡ === ROUND $round ===');

    // Player attacks (simulate dice roll with modulo)
    int playerDiceRoll = (DateTime.now().millisecondsSinceEpoch % 6) + 1;
    int playerDamage = (playerAttack + playerDiceRoll) - enemyDefense;
    playerDamage = playerDamage > 0 ? playerDamage : 1; // Minimum 1 damage

    enemyHealth -= playerDamage;
    enemyHealth = enemyHealth < 0 ? 0 : enemyHealth; // Don't go below 0

    print('🎲 $playerName rolls: $playerDiceRoll');
    print('⚔️ $playerName deals $playerDamage damage to $enemyName!');
    print('🐉 $enemyName health: $enemyHealth');

    if (enemyHealth <= 0) {
      print('🏆 $playerName WINS! 🎉');
      break;
    }

    // Enemy counter-attacks
    int enemyDiceRoll = (DateTime.now().microsecondsSinceEpoch % 6) + 1;
    int enemyDamage = (enemyAttack + enemyDiceRoll) - playerDefense;
    enemyDamage = enemyDamage > 0 ? enemyDamage : 1;

    playerHealth -= enemyDamage;
    playerHealth = playerHealth < 0 ? 0 : playerHealth;

    print('🎲 $enemyName rolls: $enemyDiceRoll');
    print('🐉 $enemyName deals $enemyDamage damage to $playerName!');
    print('👤 $playerName health: $playerHealth');

    if (playerHealth <= 0) {
      print('💀 $enemyName WINS! Game Over!');
      break;
    }

    // Health status
    if (playerHealth <= 25) {
      print('🚨 $playerName is critically wounded!');
    } else if (playerHealth <= 50) {
      print('⚠️ $playerName is badly hurt!');
    }

    if (enemyHealth <= 30) {
      print('🔥 $enemyName is nearly defeated!');
    } else if (enemyHealth <= 60) {
      print('⚡ $enemyName is weakening!');
    }

    round++;
    print('');
  }

  print('\n📊 BATTLE SUMMARY:');
  print('⚡ Total rounds: ${round - 1}');
  print('👤 $playerName final health: $playerHealth');
  print('🐉 $enemyName final health: $enemyHealth');

  if (playerHealth > enemyHealth) {
    int experienceGained = 150 + (round * 10);
    int goldEarned = 75 + (round * 5);
    print('🎁 Rewards: ${experienceGained}XP, ${goldEarned} gold!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **complex game mechanics using various operator combinations**:

1. **Random Number Generation**: Uses modulo operator with timestamps to simulate dice rolls (random 1-6 values).

2. **Combat Calculations**: Combines arithmetic operators for damage calculation (attack + dice - defense).

3. **Boundary Enforcement**: Uses comparison and conditional operators to enforce minimum damage and prevent negative health.

4. **Loop Control**: Uses logical AND (`&&`) in while loop to continue combat until one character is defeated.

5. **Progressive Feedback**: Uses comparison operators to provide dynamic status updates based on current health levels.

6. **Game State Management**: Shows how operators maintain and update complex game state through multiple rounds of combat.

---

## 📊 Operator Precedence: The Order of Operations

```dart
void main() {
  print('🎯 OPERATOR PRECEDENCE DEMO 🎯\n');

  // Order matters!
  print('🧮 Mathematical expressions:');
  print('2 + 3 * 4 = ${2 + 3 * 4}');          // Multiplication first: 2 + 12 = 14
  print('(2 + 3) * 4 = ${(2 + 3) * 4}');      // Parentheses first: 5 * 4 = 20
  print('10 / 2 + 3 = ${10 / 2 + 3}');        // Division first: 5 + 3 = 8
  print('10 / (2 + 3) = ${10 / (2 + 3)}');    // Parentheses first: 10 / 5 = 2

  print('\n🔍 Comparison and logical:');
  bool result1 = 5 > 3 && 2 < 4;              // Comparisons first, then AND
  bool result2 = true || false && false;       // AND before OR
  bool result3 = (true || false) && false;     // Parentheses change the order

  print('5 > 3 && 2 < 4 = $result1');
  print('true || false && false = $result2');
  print('(true || false) && false = $result3');

  print('\n📋 Precedence order (highest to lowest):');
  print('1. () Parentheses');
  print('2. * / ~/ % Multiplication, Division, Modulo');
  print('3. + - Addition, Subtraction');
  print('4. < > <= >= Comparison');
  print('5. == != Equality');
  print('6. && Logical AND');
  print('7. || Logical OR');
  print('8. = += -= Assignment');
}
```

**🔍 What This Code Does:**

This code demonstrates **the critical importance of operator precedence in programming**:

1. **Mathematical Order**: Shows how multiplication and division execute before addition and subtraction, following mathematical conventions.

2. **Parentheses Override**: Demonstrates how parentheses can change execution order, just like in mathematics.

3. **Logical Precedence**: Shows that AND (`&&`) has higher precedence than OR (`||`), affecting boolean expression evaluation.

4. **Common Pitfalls**: Highlights expressions where precedence might cause unexpected results if not understood properly.

5. **Best Practices**: Implicitly suggests using parentheses for clarity even when not strictly necessary.

---

## 📚 String Operators: Text Magic

```dart
void main() {
  print('✨ STRING MAGIC OPERATORS ✨\n');

  String firstName = 'Harry';
  String lastName = 'Potter';
  String house = 'Gryffindor';

  // String concatenation
  String fullName = firstName + ' ' + lastName;
  print('🧙‍♂️ Full name: $fullName');

  // String interpolation (better way)
  String introduction = 'Hello, I am $firstName $lastName from $house house!';
  print('💬 Introduction: $introduction');

  // String multiplication (repeat)
  String spell = 'Abra' * 3;
  print('🪄 Magic spell: ${spell}cadabra!');

  // String comparison
  String password = 'Alohomora';
  String userInput = 'alohomora';

  print('\n🔐 Password check:');
  print('Password: "$password"');
  print('User input: "$userInput"');
  print('Match (case-sensitive): ${password == userInput}');
  print('Match (case-insensitive): ${password.toLowerCase() == userInput.toLowerCase()}');

  // String length comparison
  String shortSpell = 'Lumos';
  String longSpell = 'Expelliarmus';

  print('\n📏 Spell length comparison:');
  print('$shortSpell length: ${shortSpell.length}');
  print('$longSpell length: ${longSpell.length}');
  print('$shortSpell is shorter: ${shortSpell.length < longSpell.length}');

  // Contains check
  String favoriteSpell = 'Expecto Patronum';
  print('\n🔍 Spell analysis:');
  print('Favorite spell: "$favoriteSpell"');
  print('Contains "Patronum": ${favoriteSpell.contains("Patronum")}');
  print('Starts with "Expecto": ${favoriteSpell.startsWith("Expecto")}');
}
```

**🔍 What This Code Does:**

This code demonstrates **string manipulation using operators and methods**:

1. **String Concatenation**: Uses `+` operator to combine multiple strings, though string interpolation is generally preferred.

2. **String Interpolation**: Shows `$variable` syntax for embedding variables in strings, which is more readable and efficient.

3. **String Multiplication**: Demonstrates the `*` operator for repeating strings, useful for creating patterns or padding.

4. **Case-Sensitive Comparison**: Shows how string equality (`==`) is case-sensitive and how to handle case-insensitive comparisons.

5. **String Properties**: Uses `.length` property with comparison operators to compare string sizes.

6. **String Methods**: Demonstrates `.contains()`, `.startsWith()`, and other string analysis methods for text processing.

---

## 🧠 Quick Reference Guide

### All Operators at a Glance

| Category       | Operator | Name             | Example           | Result          |
| -------------- | -------- | ---------------- | ----------------- | --------------- |
| **Arithmetic** | `+`      | Addition         | `5 + 3`           | `8`             |
|                | `-`      | Subtraction      | `5 - 3`           | `2`             |
|                | `*`      | Multiplication   | `5 * 3`           | `15`            |
|                | `/`      | Division         | `5 / 2`           | `2.5`           |
|                | `~/`     | Integer Division | `5 ~/ 2`          | `2`             |
|                | `%`      | Modulo           | `5 % 2`           | `1`             |
|                | `++`     | Increment        | `x++`             | `x + 1`         |
|                | `--`     | Decrement        | `x--`             | `x - 1`         |
| **Comparison** | `==`     | Equal            | `5 == 5`          | `true`          |
|                | `!=`     | Not equal        | `5 != 3`          | `true`          |
|                | `>`      | Greater than     | `5 > 3`           | `true`          |
|                | `<`      | Less than        | `5 < 3`           | `false`         |
|                | `>=`     | Greater or equal | `5 >= 5`          | `true`          |
|                | `<=`     | Less or equal    | `5 <= 3`          | `false`         |
| **Logical**    | `&&`     | AND              | `true && false`   | `false`         |
|                | `\|\|`   | OR               | `true \|\| false` | `true`          |
|                | `!`      | NOT              | `!true`           | `false`         |
| **Assignment** | `=`      | Assign           | `x = 5`           | `x` becomes `5` |
|                | `+=`     | Add assign       | `x += 3`          | `x = x + 3`     |
|                | `-=`     | Subtract assign  | `x -= 3`          | `x = x - 3`     |
|                | `*=`     | Multiply assign  | `x *= 3`          | `x = x * 3`     |
|                | `/=`     | Divide assign    | `x /= 3`          | `x = x / 3`     |

---

## 🎯 Common Use Cases

### Age Verification System

```dart
void checkAgeEligibility(int age) {
  bool canVote = age >= 18;
  bool canDrink = age >= 21;
  bool isMinor = age < 18;

  print('👤 Age: $age');
  print('🗳️ Can vote: $canVote');
  print('🍺 Can drink: $canDrink');
  print('👶 Is minor: $isMinor');
}

void main() {
  checkAgeEligibility(16);
  print('');
  checkAgeEligibility(20);
  print('');
  checkAgeEligibility(25);
}
```

### Grade Calculator

```dart
void calculateGrade(int score) {
  String grade;

  if (score >= 90) {
    grade = 'A';
  } else if (score >= 80) {
    grade = 'B';
  } else if (score >= 70) {
    grade = 'C';
  } else if (score >= 60) {
    grade = 'D';
  } else {
    grade = 'F';
  }

  bool isPassing = score >= 60;
  bool isHonorRoll = score >= 90;

  print('📝 Score: $score');
  print('🎓 Grade: $grade');
  print('✅ Passing: $isPassing');
  print('🌟 Honor roll: $isHonorRoll');
}
```

---

## 🚀 Practice Challenges

Try using operators in these scenarios:

1. **🏪 Store Calculator**: Calculate total with tax and discount
2. **🎮 Game Score**: Add points, multiply bonuses, compare high scores
3. **⏰ Time Converter**: Convert hours to minutes using multiplication
4. **🍕 Pizza Splitter**: Divide pizzas equally among friends using modulo
5. **🎯 Target Practice**: Compare player scores and determine winners

---

## 🎉 Remember This!

Operators are like **tools in a magical toolbox** 🧰✨:

- **🧮 Arithmetic**: Your calculator for number crunching
- **⚖️ Comparison**: Your scale for weighing options
- **🧠 Logical**: Your brain for making smart decisions
- **⚡ Assignment**: Your magic wand for changing values

**The Magic**: Operators turn your data into **actions** and **decisions** - they're the verbs in your code's story!

> **Think of it like**: "Numbers are the ingredients, operators are the cooking instructions!" 👨‍🍳

Without operators, you'd have ingredients but no recipe - operators tell Dart exactly what to **do** with your data! 🎪🚀
