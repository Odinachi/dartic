# Getters and Setters in Dart

Imagine you have a **magical jewelry box** 💍✨ with a special lock!

The box has some **precious treasures** inside, but you can't just grab them directly. Instead, you have:

- A **special key** 🗝️ to **look inside** and see what's there (**Getter**)
- A **special door** 🚪 to **safely put new treasures** in (**Setter**)

This protects your treasures from being stolen or broken! 🛡️

👉 **Getters and Setters** work exactly like this magical jewelry box:

> They provide **safe, controlled access** to your object's private data!

---

## 🚫 The Problem: Direct Access

```dart
class BankAccount {
  double balance = 1000.0; // Anyone can access this directly!
}

void main() {
  BankAccount account = BankAccount();

  // ❌ Dangerous! Anyone can do this:
  account.balance = -500.0; // Negative balance?!
  account.balance = 999999999.0; // Unlimited money?!

  print('Balance: \$${account.balance}');
}
```

**🔍 What This Code Does:**

This code demonstrates **the security risks of direct field access**:

1. **No Data Protection**: The `balance` field is public, allowing unrestricted read and write access from anywhere in the code.

2. **Invalid State Creation**: Direct access permits setting impossible values like negative balances or unrealistic amounts.

3. **No Business Logic**: There's no validation, logging, or processing when the balance changes, bypassing important banking rules.

4. **Audit Trail Missing**: Changes to the balance happen silently without any record of who made the change or when.

5. **Breaking Encapsulation**: The internal state is exposed directly, making the class fragile and hard to maintain.

**Problems:**

- No security! 🔓
- No validation! ⚠️
- No logging of changes! 📝
- Anyone can break your data! 💥

---

## ✅ The Solution: Getters and Setters

```dart
class BankAccount {
  double _balance = 1000.0; // Private with underscore!

  // Getter - safe way to READ the balance
  double get balance {
    print('🔍 Checking account balance...');
    return _balance;
  }

  // Setter - safe way to CHANGE the balance
  set balance(double amount) {
    print('💰 Processing balance change...');

    if (amount >= 0) {
      _balance = amount;
      print('✅ Balance updated to \$${amount}');
    } else {
      print('❌ Invalid amount! Balance cannot be negative.');
    }
  }
}

void main() {
  BankAccount account = BankAccount();

  // Safe access through getters and setters
  print('Current balance: \$${account.balance}');

  account.balance = 1200.0; // This works
  account.balance = -100.0; // This is safely rejected

  print('Final balance: \$${account.balance}');
}
```

**🔍 What This Code Does:**

This code demonstrates **controlled access through getters and setters**:

1. **Data Encapsulation**: The underscore prefix `_balance` makes the field private, preventing direct external access.

2. **Controlled Reading**: The getter provides a controlled way to access the balance, with optional logging or processing.

3. **Input Validation**: The setter validates that the new balance is non-negative before allowing the change.

4. **Audit Logging**: Both getter and setter print messages, creating an audit trail of balance access and modifications.

5. **Business Rule Enforcement**: The setter enforces banking business rules by rejecting invalid transactions.

6. **Error Handling**: Invalid inputs are handled gracefully with informative error messages rather than silent failures.

---

## 🎮 Gaming Example: Player Stats

```dart
class GamePlayer {
  String _name = '';
  int _health = 100;
  int _level = 1;
  int _experience = 0;

  // Name getter and setter
  String get name => _name.isEmpty ? 'Unknown Player' : _name;

  set name(String playerName) {
    if (playerName.trim().isNotEmpty) {
      _name = playerName.trim();
      print('🎮 Player name set to: $_name');
    } else {
      print('❌ Player name cannot be empty!');
    }
  }

  // Health with validation
  int get health => _health;

  set health(int hp) {
    if (hp < 0) {
      _health = 0;
      print('💀 $name has died!');
    } else if (hp > 100) {
      _health = 100;
      print('💚 $name is at full health!');
    } else {
      _health = hp;
      print('❤️ $name\'s health: $_health/100');
    }
  }

  // Level with auto-calculation
  int get level => _level;

  // Experience with level-up logic
  int get experience => _experience;

  set experience(int xp) {
    _experience = xp;
    int newLevel = (_experience ~/ 1000) + 1; // Level up every 1000 XP

    if (newLevel > _level) {
      _level = newLevel;
      _health = 100; // Full heal on level up!
      print('🎉 LEVEL UP! $name is now level $_level!');
      print('✨ Health fully restored!');
    }

    print('⚡ $name gained experience! Total: $_experience XP');
  }

  // Read-only computed property
  int get experienceToNextLevel {
    int nextLevelXP = _level * 1000;
    return nextLevelXP - _experience;
  }

  void displayStats() {
    print('\n📊 === PLAYER STATS ===');
    print('👤 Name: $name');
    print('❤️ Health: $health/100');
    print('📈 Level: $level');
    print('⚡ Experience: $experience XP');
    print('🎯 XP to next level: $experienceToNextLevel');
    print('═' * 25);
  }
}

void main() {
  print('🎮 CREATING NEW CHARACTER\n');

  GamePlayer player = GamePlayer();

  // Set player name
  player.name = 'DragonSlayer';
  player.displayStats();

  // Battle damage
  print('\n⚔️ BATTLE SEQUENCE');
  player.health = 75; // Take damage
  player.health = 150; // Try to over-heal

  // Gain experience
  print('\n🏆 QUEST COMPLETED');
  player.experience = 800;
  player.experience = 1200; // Should level up!

  player.displayStats();

  // Test negative health
  print('\n💀 DANGEROUS BATTLE');
  player.health = -10;

  player.displayStats();
}
```

**🔍 What This Code Does:**

This code demonstrates **complex game mechanics implemented through getters and setters**:

1. **Default Value Handling**: The name getter returns a default value when no name is set, preventing empty player names.

2. **String Sanitization**: The name setter trims whitespace and validates non-empty input, ensuring clean data storage.

3. **Range Clamping**: The health setter clamps values between 0 and 100, preventing invalid health states.

4. **Automatic Level Calculation**: Experience setter automatically calculates and updates player level based on XP thresholds.

5. **Cascading Effects**: Level-up triggers multiple changes (health restoration, level increment), showing interconnected game systems.

6. **Computed Properties**: `experienceToNextLevel` calculates derived values without storing redundant data.

7. **Game Event Notification**: Setters provide immediate feedback for important game events (death, level-up, healing).

---

## 🏪 Shopping Cart Example

```dart
class ShoppingCart {
  List<String> _items = [];
  double _totalPrice = 0.0;
  String _customerName = '';

  // Customer name with formatting
  String get customerName => _customerName.isEmpty ? 'Guest' : _customerName;

  set customerName(String name) {
    _customerName = name.trim().split(' ')
      .map((word) => word.isEmpty ? '' : word[0].toUpperCase() + word.substring(1).toLowerCase())
      .join(' ');
    print('🛒 Customer set to: $_customerName');
  }

  // Items as read-only list
  List<String> get items => List.unmodifiable(_items);

  // Item count
  int get itemCount => _items.length;

  // Total price (read-only)
  double get totalPrice => _totalPrice;

  // Discount percentage with validation
  double _discountPercent = 0.0;

  double get discountPercent => _discountPercent;

  set discountPercent(double percent) {
    if (percent < 0) {
      _discountPercent = 0;
      print('❌ Discount cannot be negative!');
    } else if (percent > 50) {
      _discountPercent = 50;
      print('⚠️ Maximum discount is 50%');
    } else {
      _discountPercent = percent;
      print('🏷️ Discount set to ${_discountPercent}%');
    }
  }

  // Final price after discount (computed)
  double get finalPrice {
    double discount = _totalPrice * (_discountPercent / 100);
    return _totalPrice - discount;
  }

  // Cart capacity check
  bool get isFull => _items.length >= 10;

  bool get isEmpty => _items.isEmpty;

  void addItem(String item, double price) {
    if (isFull) {
      print('🛒 Cart is full! Cannot add more items.');
      return;
    }

    _items.add(item);
    _totalPrice += price;
    print('➕ Added $item (\$${price.toStringAsFixed(2)})');
  }

  void displayCart() {
    print('\n🛒 === SHOPPING CART ===');
    print('👤 Customer: $customerName');
    print('📦 Items (${itemCount}/10):');

    if (isEmpty) {
      print('   (Empty cart)');
    } else {
      for (int i = 0; i < _items.length; i++) {
        print('   ${i + 1}. ${_items[i]}');
      }
    }

    print('💰 Subtotal: \$${totalPrice.toStringAsFixed(2)}');
    if (_discountPercent > 0) {
      print('🏷️ Discount: ${_discountPercent}%');
      print('✨ Final Price: \$${finalPrice.toStringAsFixed(2)}');
    }
    print('═' * 25);
  }
}

void main() {
  print('🛍️ WELCOME TO DART STORE!\n');

  ShoppingCart cart = ShoppingCart();

  // Set customer name
  cart.customerName = 'sarah johnson'; // Will be formatted
  cart.displayCart();

  // Add some items
  print('\n🛒 SHOPPING SPREE');
  cart.addItem('Gaming Mouse', 49.99);
  cart.addItem('Mechanical Keyboard', 129.99);
  cart.addItem('Monitor', 299.99);

  // Apply discount
  cart.discountPercent = 15;
  cart.displayCart();

  // Try invalid discounts
  print('\n🏷️ DISCOUNT EXPERIMENTS');
  cart.discountPercent = -10; // Invalid
  cart.discountPercent = 75;  // Too high
  cart.discountPercent = 20;  // Valid

  cart.displayCart();

  // Fill up cart
  print('\n📦 FILLING CART');
  for (int i = 4; i <= 12; i++) {
    cart.addItem('Item $i', 10.0);
  }

  cart.displayCart();
}
```

**🔍 What This Code Does:**

This code demonstrates **advanced data processing and business logic in getters and setters**:

1. **String Formatting**: The customerName setter applies title case formatting to names, ensuring consistent data presentation.

2. **Immutable Collections**: The items getter returns an unmodifiable list, preventing external modification while allowing read access.

3. **Computed Properties**: Properties like `finalPrice` calculate values dynamically based on other fields without storing redundant data.

4. **Business Rule Validation**: Discount percentage is constrained to realistic business limits (0-50%).

5. **State Queries**: Boolean getters like `isFull` and `isEmpty` provide convenient ways to check object state.

6. **Data Encapsulation**: Internal collections and calculations are protected while providing controlled access through getters.

7. **Real-time Calculations**: Final price updates automatically when discount or total price changes, maintaining data consistency.

---

## 📱 Smart Phone Settings

```dart
class SmartPhone {
  String _model = '';
  int _batteryLevel = 100;
  double _brightness = 50.0;
  bool _isLocked = true;
  String _wallpaper = 'Default';

  // Model with validation
  String get model => _model.isEmpty ? 'Unknown Phone' : _model;

  set model(String phoneName) {
    if (phoneName.trim().isNotEmpty) {
      _model = phoneName.trim();
      print('📱 Phone model set to: $_model');
    }
  }

  // Battery with realistic simulation
  int get batteryLevel => _batteryLevel;

  set batteryLevel(int level) {
    if (level < 0) {
      _batteryLevel = 0;
      print('🔋 Phone has shut down - battery empty!');
    } else if (level > 100) {
      _batteryLevel = 100;
      print('🔌 Phone fully charged!');
    } else {
      _batteryLevel = level;

      if (_batteryLevel <= 10) {
        print('🪫 LOW BATTERY WARNING: $_batteryLevel%');
      } else if (_batteryLevel <= 20) {
        print('🟡 Battery getting low: $_batteryLevel%');
      } else {
        print('🔋 Battery: $_batteryLevel%');
      }
    }
  }

  // Screen brightness with validation
  double get brightness => _brightness;

  set brightness(double level) {
    if (level < 0) {
      _brightness = 0;
      print('🌑 Screen at minimum brightness');
    } else if (level > 100) {
      _brightness = 100;
      print('☀️ Screen at maximum brightness');
    } else {
      _brightness = level;

      if (level < 20) {
        print('🌘 Screen dimmed to ${_brightness.toStringAsFixed(1)}%');
      } else if (level > 80) {
        print('🌞 Screen bright at ${_brightness.toStringAsFixed(1)}%');
      } else {
        print('💡 Screen brightness: ${_brightness.toStringAsFixed(1)}%');
      }
    }
  }

  // Lock status
  bool get isLocked => _isLocked;

  set isLocked(bool locked) {
    _isLocked = locked;
    if (locked) {
      print('🔒 Phone locked for security');
    } else {
      print('🔓 Phone unlocked - welcome back!');
    }
  }

  // Wallpaper with change notification
  String get wallpaper => _wallpaper;

  set wallpaper(String image) {
    if (image.trim().isNotEmpty) {
      _wallpaper = image.trim();
      print('🖼️ Wallpaper changed to: $_wallpaper');
    }
  }

  // Computed properties
  String get batteryStatus {
    if (_batteryLevel > 80) return 'Excellent 🟢';
    if (_batteryLevel > 50) return 'Good 🟡';
    if (_batteryLevel > 20) return 'Fair 🟠';
    return 'Critical 🔴';
  }

  bool get needsCharging => _batteryLevel < 30;

  String get securityStatus => _isLocked ? 'Secure 🔒' : 'Unlocked 🔓';

  void simulateUsage(int minutes) {
    print('\n📱 Using phone for $minutes minutes...');

    // Drain battery based on brightness and usage
    int drain = minutes + (brightness ~/ 20);
    batteryLevel = batteryLevel - drain;

    print('⏰ Usage complete');
  }
}

void main() {
  print('📱 SMART PHONE SIMULATOR\n');

  SmartPhone phone = SmartPhone();
  phone.model = 'iPhone 15 Pro';

  phone.displayStatus();

  // Unlock and use phone
  print('\n🔓 UNLOCKING PHONE');
  phone.isLocked = false;

  // Adjust settings
  print('\n⚙️ ADJUSTING SETTINGS');
  phone.brightness = 75;
  phone.wallpaper = 'Sunset Beach 🌅';

  // Simulate phone usage
  phone.simulateUsage(30);
  phone.simulateUsage(45);

  phone.displayStatus();

  // Test edge cases
  print('\n🧪 TESTING LIMITS');
  phone.brightness = 150;  // Too high
  phone.brightness = -10;  // Too low
  phone.batteryLevel = 5;  // Very low

  phone.displayStatus();

  // Charge the phone
  print('\n🔌 CHARGING PHONE');
  phone.batteryLevel = 100;
  phone.isLocked = true;

  phone.displayStatus();
}
```

**🔍 What This Code Does:**

This code demonstrates **realistic device simulation with intelligent feedback systems**:

1. **Realistic Hardware Limits**: Battery and brightness values are constrained to realistic ranges (0-100) with appropriate clamping.

2. **Contextual User Feedback**: Different battery levels trigger different warning messages, simulating real device behavior.

3. **Graduated Responses**: Brightness setter provides different feedback messages based on the intensity level being set.

4. **Derived Status Information**: Computed properties like `batteryStatus` and `needsCharging` provide meaningful interpretations of raw data.

5. **Usage Simulation**: `simulateUsage()` method demonstrates how getters and setters integrate with other object behaviors.

6. **Hardware Interaction Modeling**: The relationship between brightness and battery drain shows realistic device physics simulation.

7. **User Experience Design**: Feedback messages are designed to inform users about device state changes clearly.

---

## 🧠 Different Types of Getters and Setters

### 1. **Read-Only Properties** (Getter Only)

```dart
class Circle {
  double _radius;

  Circle(this._radius);

  double get radius => _radius; // Can read

  double get area => 3.14159 * _radius * _radius; // Computed
  double get circumference => 2 * 3.14159 * _radius; // Computed

  // No setters - these are read-only!
}
```

**🔍 What This Code Does:**

This code demonstrates **immutable computed properties**:

1. **Read-Only Access**: Properties with only getters prevent external modification while allowing data access.

2. **Computed Values**: Area and circumference are calculated dynamically from the radius, ensuring they're always current.

3. **Mathematical Relationships**: Shows how getters can encapsulate mathematical formulas and derived values.

4. **Data Consistency**: Since computed values can't be set independently, they always reflect the current radius value.

### 2. **Write-Only Properties** (Setter Only)

```dart
class SecuritySystem {
  String _password = '';

  set password(String newPassword) { // Can write
    if (newPassword.length >= 8) {
      _password = newPassword;
      print('🔒 Password updated successfully!');
    } else {
      print('❌ Password must be at least 8 characters!');
    }
  }

  // No getter - password is write-only for security!

  bool checkPassword(String attempt) {
    return _password == attempt;
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **write-only properties for security**:

1. **Security by Design**: No getter prevents external code from reading the password, enhancing security.

2. **Input Validation**: Setter validates password strength requirements before accepting new values.

3. **Controlled Access**: Password verification is handled through a dedicated method rather than direct comparison.

4. **Privacy Protection**: Sensitive data can be written but not read, following security best practices.

### 3. **Computed Properties** (Dynamic Values)

```dart
class Temperature {
  double _celsius = 0;

  double get celsius => _celsius;
  set celsius(double temp) => _celsius = temp;

  // Computed getters
  double get fahrenheit => (_celsius * 9 / 5) + 32;
  double get kelvin => _celsius + 273.15;

  // Computed setters
  set fahrenheit(double temp) => _celsius = (temp - 32) * 5 / 9;
  set kelvin(double temp) => _celsius = temp - 273.15;

  String get description {
    if (_celsius < 0) return 'Freezing 🥶';
    if (_celsius < 15) return 'Cold 🧥';
    if (_celsius < 25) return 'Cool 😊';
    if (_celsius < 30) return 'Warm ☀️';
    return 'Hot 🔥';
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **unit conversion and computed properties**:

1. **Unit Conversion**: Getters and setters automatically convert between temperature scales (Celsius, Fahrenheit, Kelvin).

2. **Single Source of Truth**: All temperatures are stored in Celsius internally, with conversions calculated on demand.

3. **Bidirectional Conversion**: Both getters and setters are provided for each scale, allowing flexible input/output.

4. **Descriptive Properties**: The description getter provides human-readable interpretation of temperature values.

5. **Mathematical Accuracy**: Conversion formulas are encapsulated within the class, preventing calculation errors.

---

## 📊 Quick Reference Guide

### Basic Syntax

```dart
class MyClass {
  String _privateValue = '';

  // Getter
  String get value => _privateValue;

  // Setter
  set value(String newValue) {
    _privateValue = newValue;
  }

  // Read-only computed property
  String get uppercaseValue => _privateValue.toUpperCase();
}
```

### Common Patterns

| Pattern         | Use Case              | Example                                   |
| --------------- | --------------------- | ----------------------------------------- |
| **Validation**  | Ensure data integrity | Check age > 0, name not empty             |
| **Formatting**  | Clean up input        | Trim whitespace, capitalize names         |
| **Logging**     | Track access/changes  | Print when values are read/written        |
| **Computation** | Derived values        | Calculate area from radius                |
| **Security**    | Control access        | Hide sensitive data, validate permissions |

---

## 🎯 When to Use Getters and Setters

**✅ Great for:**

- **Private data** that needs controlled access
- **Validation** of input values
- **Computed properties** that change based on other values
- **Logging** and debugging data access
- **API compatibility** when internal structure changes

**❌ Not needed for:**

- Simple public data that doesn't need protection
- Values that never change after creation
- Performance-critical code where overhead matters

---

## 🚀 Practice Challenges

Create getters and setters for these scenarios:

1. **🏠 Smart Home**: Temperature, lights, security system
2. **🎵 Music Player**: Volume, current song, playlist
3. **🚗 Car Dashboard**: Speed, fuel, engine temperature
4. **👤 User Profile**: Email validation, password strength, avatar

---

## 🎉 Remember This!

Getters and Setters are like having **smart assistants** for your data 🤖:

- **🔍 Getters** = "Here's your data, sir/madam!" (with any processing needed)
- **✍️ Setters** = "Let me safely store that for you!" (with validation and security)
- **🛡️ Privacy** = The underscore `_` creates a secure vault
- **🧠 Computed** = Smart properties that calculate themselves

Think of them as **VIP bouncers** at a fancy club - they decide who gets in, who gets out, and they keep everything safe and organized! 🕺💃✨

**Pro Tip**: Use getters and setters when you need **control**, **validation**, or **extra processing**. For simple data, direct access is perfectly fine! 🎯
double get celsius => \_celsius;
set celsius(double temp) => \_celsius = temp;

// Computed getters
double get fahrenheit => (\_celsius \* 9 / 5) + 32;
double get kelvin => \_celsius + 273.15;

// Computed setters
set fahrenheit(double temp) => \_celsius = (temp - 32) \* 5 / 9;
set kelvin(double temp) => \_celsius = temp - 273.15;

String get description {
if (\_celsius < 0) return 'Freezing 🥶';
if (\_celsius < 15) return 'Cold 🧥';
if (\_celsius < 25) return 'Cool 😊';
if (\_celsius < 30) return 'Warm ☀️';
return 'Hot 🔥';
}
}

````

---

## 📊 Quick Reference Guide

### Basic Syntax

```dart
class MyClass {
  String _privateValue = '';

  // Getter
  String get value => _privateValue;

  // Setter
  set value(String newValue) {
    _privateValue = newValue;
  }

  // Read-only computed property
  String get uppercaseValue => _privateValue.toUpperCase();
}
````

### Common Patterns

| Pattern         | Use Case              | Example                                   |
| --------------- | --------------------- | ----------------------------------------- |
| **Validation**  | Ensure data integrity | Check age > 0, name not empty             |
| **Formatting**  | Clean up input        | Trim whitespace, capitalize names         |
| **Logging**     | Track access/changes  | Print when values are read/written        |
| **Computation** | Derived values        | Calculate area from radius                |
| **Security**    | Control access        | Hide sensitive data, validate permissions |

---

## 🎯 When to Use Getters and Setters

**✅ Great for:**

- **Private data** that needs controlled access
- **Validation** of input values
- **Computed properties** that change based on other values
- **Logging** and debugging data access
- **API compatibility** when internal structure changes

**❌ Not needed for:**

- Simple public data that doesn't need protection
- Values that never change after creation
- Performance-critical code where overhead matters

---

## 🚀 Practice Challenges

Create getters and setters for these scenarios:

1. **🏠 Smart Home**: Temperature, lights, security system
2. **🎵 Music Player**: Volume, current song, playlist
3. **🚗 Car Dashboard**: Speed, fuel, engine temperature
4. **👤 User Profile**: Email validation, password strength, avatar

---

## 🎉 Remember This!

Getters and Setters are like having **smart assistants** for your data 🤖:

- **🔍 Getters** = "Here's your data, sir/madam!" (with any processing needed)
- **✍️ Setters** = "Let me safely store that for you!" (with validation and security)
- **🛡️ Privacy** = The underscore `_` creates a secure vault
- **🧠 Computed** = Smart properties that calculate themselves

Think of them as **VIP bouncers** at a fancy club - they decide who gets in, who gets out, and they keep everything safe and organized! 🕺💃✨

**Pro Tip**: Use getters and setters when you need **control**, **validation**, or **extra processing**. For simple data, direct access is perfectly fine! 🎯
