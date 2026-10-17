# Abstract Classes

Imagine you're designing **video game characters** 🎮.

Every character needs to:

- Have a **health bar** 💚
- Be able to **attack** ⚔️
- Have a **special move** ✨

But each character does these things **differently**:

- A **wizard** casts spells 🧙‍♂️
- A **warrior** swings a sword 🗡️
- An **archer** shoots arrows 🏹

You know **what** every character must do, but not exactly **how** they'll do it.

👉 That's what an **Abstract Class** is!

> "A blueprint that says: 'Every character must have these abilities, but YOU decide how they work!'"

---

## 🎯 Real-Life Analogy

| Real Life                                       | Dart Code                                     |
| ----------------------------------------------- | --------------------------------------------- |
| **Game character blueprint** 📋                 | `abstract class GameCharacter`                |
| **"Must have attack move"** ⚔️                  | `void attack();` (abstract method)            |
| **"Health bar works the same for everyone"** 💚 | `void showHealth() { ... }` (concrete method) |
| **Actual wizard character** 🧙‍♂️                  | `class Wizard extends GameCharacter`          |

---

## 🎮 Basic Abstract Class Example

```dart
// 'abstract' keyword means this class cannot be instantiated directly
// It serves as a blueprint for other classes
abstract class GameCharacter {
  // Property to store the character's name
  // All child classes will inherit this property
  String name;

  // Property for health with default value of 100
  // The '=' assigns a default value when object is created
  int health = 100;

  // Constructor that takes a name parameter
  // 'this.name' is shorthand for setting the name property
  GameCharacter(this.name);

  // Abstract method - declared but not implemented
  // The semicolon (;) indicates no implementation
  // All child classes MUST implement this method
  void attack();

  // Concrete method - has actual implementation
  // Child classes inherit this exact behavior
  void showHealth() {
    // String interpolation using $ to embed variables in text
    // Prints the character's name and current health
    print('$name has $health health remaining 💚');
  }
}
```

**🔍 What This Code Does:**

This code creates an **abstract class blueprint** for game characters. Here's what it accomplishes:

1. **Defines a Template**: The `GameCharacter` class serves as a template that cannot be used directly but provides structure for other classes.

2. **Shared Properties**: All characters will have a `name` (String) and `health` (integer starting at 100) - these are inherited by all child classes.

3. **Mixed Method Types**:

   - `attack()` is **abstract** - it has no implementation, forcing child classes to define their own attack behavior
   - `showHealth()` is **concrete** - it has a complete implementation that all child classes inherit unchanged

4. **Constructor Pattern**: The constructor requires a name parameter, ensuring every character must be created with a name.

5. **Enforcement**: The abstract `attack()` method creates a contract - any class extending `GameCharacter` MUST implement an attack method.

💡 **Key Points:**

- `abstract` = Cannot create objects directly from this class
- `void attack();` = Abstract method (no body, just a promise)
- `showHealth()` = Concrete method (has actual code)

---

## 🧙‍♂️ Creating Real Characters

### Wizard Character:

```dart
// 'class' defines a new class called Wizard
// 'extends' means Wizard inherits from GameCharacter
class Wizard extends GameCharacter {
  // Constructor for Wizard class
  // Takes a String parameter called 'name'
  Wizard(String name) : super(name);
  // ': super(name)' calls the parent class constructor
  // This passes the name to GameCharacter's constructor

  // '@override' annotation indicates we're implementing an abstract method
  // This is required when implementing abstract methods from parent class
  @override
  void attack() {
    // Implementation of the abstract attack method for wizards
    // String interpolation to include the wizard's name in output
    print('$name casts a fireball! 🔥');
  }

  // Additional method specific to Wizard class
  // Not inherited from GameCharacter, unique to wizards
  void castSpell() {
    // Custom behavior only wizards can do
    print('$name uses magic spell! ✨');
  }
}
```

**🔍 What This Code Does:**

This code creates a **concrete implementation** of the abstract `GameCharacter` class. Here's what it accomplishes:

1. **Inheritance**: The `Wizard` class inherits all properties (`name`, `health`) and methods (`showHealth()`) from `GameCharacter`.

2. **Constructor Chaining**: The Wizard constructor takes a name and passes it to the parent class constructor using `super(name)`, ensuring proper initialization.

3. **Abstract Method Implementation**: The `@override` annotation indicates that `attack()` fulfills the abstract method requirement from the parent class with wizard-specific behavior.

4. **Polymorphism**: The same `attack()` method signature produces different behavior - wizards cast fireballs instead of generic attacks.

5. **Class-Specific Features**: `castSpell()` is unique to wizards, showing how child classes can add their own specialized methods beyond the abstract requirements.

### Warrior Character:

```dart
// Another class extending GameCharacter
// Shows polymorphism - different implementation of same abstract method
class Warrior extends GameCharacter {
  // Constructor similar to Wizard
  // Calls parent constructor with 'super(name)'
  Warrior(String name) : super(name);

  // Required implementation of abstract attack() method
  // Different behavior than Wizard's attack
  @override
  void attack() {
    // Warrior-specific attack implementation
    print('$name swings their sword! ⚔️');
  }

  // Warrior-specific method, not in parent class
  // Demonstrates class-specific functionality
  void useShield() {
    // Behavior unique to warriors
    print('$name blocks with shield! 🛡️');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **polymorphism** through another concrete implementation:

1. **Same Structure, Different Behavior**: `Warrior` follows the same pattern as `Wizard` but implements the abstract `attack()` method differently (sword swing vs. fireball).

2. **Consistent Interface**: Both `Wizard` and `Warrior` can be treated as `GameCharacter` objects, but each has unique attack behavior.

3. **Specialized Methods**: Like `Wizard` has `castSpell()`, `Warrior` has `useShield()` - showing how each class can have unique capabilities.

4. **Contract Fulfillment**: Both classes satisfy the abstract class contract by implementing the required `attack()` method.

---

## 🎯 Using the Characters

```dart
// Main function - entry point of Dart program
void main() {
  // ❌ This line would cause a compilation error
  // Cannot instantiate abstract class directly
  // GameCharacter player = GameCharacter('Hero'); // ERROR!

  // ✅ Creating objects from concrete classes
  // 'Wizard' and 'Warrior' are concrete implementations
  Wizard merlin = Wizard('Merlin');
  // Creates a Wizard object with name 'Merlin'

  Warrior arthur = Warrior('Arthur');
  // Creates a Warrior object with name 'Arthur'

  // Calling inherited method from GameCharacter
  // Uses the concrete implementation from parent class
  merlin.showHealth();  // Output: Merlin has 100 health remaining 💚

  // Calling overridden method - uses Wizard's implementation
  merlin.attack();      // Output: Merlin casts a fireball! 🔥

  // Calling Wizard-specific method
  merlin.castSpell();   // Output: Merlin uses magic spell! ✨

  // Same pattern with Warrior object
  arthur.showHealth();  // Output: Arthur has 100 health remaining 💚
  arthur.attack();      // Output: Arthur swings their sword! ⚔️ (different implementation)
  arthur.useShield();   // Output: Arthur blocks with shield! 🛡️
}
```

**🔍 What This Code Does:**

This code demonstrates **practical usage** of abstract classes and polymorphism:

1. **Abstract Class Limitation**: Shows that you cannot directly create objects from abstract classes - the commented line would cause a compilation error.

2. **Object Creation**: Demonstrates creating objects from concrete classes (`Wizard` and `Warrior`) that implement the abstract class.

3. **Inherited Behavior**: Both objects can use `showHealth()` method inherited from the abstract parent class - same implementation for both.

4. **Polymorphic Behavior**: The same `attack()` method call produces different results:

   - `merlin.attack()` → "Merlin casts a fireball! 🔥"
   - `arthur.attack()` → "Arthur swings their sword! ⚔️"

5. **Class-Specific Methods**: Shows how each class can have unique methods (`castSpell()` for wizards, `useShield()` for warriors) beyond the abstract requirements.

6. **Code Reusability**: Both classes share common functionality (health system) while having unique behaviors (different attacks and special abilities).

---

## 🏗️ More Complex Example: Drawing Shapes

```dart
// Abstract class representing any geometric shape
abstract class Shape {
  // Property to store shape's color
  // All shapes have a color
  String color;

  // Constructor requiring a color parameter
  // Every shape must have a color when created
  Shape(this.color);

  // Abstract method - no implementation provided
  // Returns a double (decimal number) for area calculation
  // Each shape calculates area differently
  double calculateArea();

  // Another abstract method for drawing
  // Each shape draws itself differently
  void draw();

  // Concrete method - same implementation for all shapes
  // Uses abstract methods within its implementation
  void describe() {
    // String interpolation with method calls
    // Calls calculateArea() which will use child class implementation
    print('This is a $color shape with area ${calculateArea()}');
    // Calls draw() which will use child class implementation
    draw();
  }
}

// Concrete class implementing Shape abstract class
class Circle extends Shape {
  // Property specific to circles
  // 'double' type for decimal numbers (radius)
  double radius;

  // Constructor taking color and radius parameters
  // Calls parent constructor with 'super(color)'
  Circle(String color, this.radius) : super(color);

  // Implementation of abstract calculateArea method
  // '@override' shows we're implementing parent's abstract method
  @override
  double calculateArea() {
    // Mathematical formula for circle area: π × r²
    // 3.14159 is approximation of π (pi)
    // * is multiplication operator
    return 3.14159 * radius * radius;
  }

  // Implementation of abstract draw method
  @override
  void draw() {
    // Circle-specific drawing representation
    print('Drawing a circle ⭕');
  }
}

// Another concrete implementation of Shape
class Rectangle extends Shape {
  // Two properties specific to rectangles
  // 'double' allows decimal values for dimensions
  double width, height;

  // Constructor taking color, width, and height
  // Uses parameter list and calls super constructor
  Rectangle(String color, this.width, this.height) : super(color);

  // Rectangle's implementation of area calculation
  @override
  double calculateArea() {
    // Rectangle area formula: width × height
    return width * height;
  }

  // Rectangle's implementation of draw method
  @override
  void draw() {
    // Rectangle-specific drawing representation
    print('Drawing a rectangle ▭');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates a more sophisticated use of abstract classes with **multiple abstract methods**:

1. **Abstract Class Design**: `Shape` defines a common structure for all geometric shapes with:

   - Shared property (`color`) that all shapes have
   - Two abstract methods (`calculateArea()`, `draw()`) that each shape implements differently
   - One concrete method (`describe()`) that uses the abstract methods

2. **Template Method Pattern**: The `describe()` method in the abstract class calls abstract methods that will be implemented by child classes, creating a template for behavior.

3. **Concrete Implementations**:

   - `Circle` implements area calculation using π × r² formula
   - `Rectangle` implements area calculation using width × height formula
   - Each has unique drawing representation

4. **Polymorphism in Action**: The same method calls produce different results based on the object type:

   - `calculateArea()` uses different mathematical formulas
   - `draw()` displays different visual representations

5. **Code Reusability**: The `describe()` method works for all shapes without modification, demonstrating how abstract classes can provide shared functionality that leverages polymorphic behavior.

### Using the Shapes:

```dart
// Main function demonstrating polymorphism
void main() {
  // Creating Circle object with red color and radius 5.0
  Circle redCircle = Circle('red', 5.0);

  // Creating Rectangle object with blue color, width 4.0, height 6.0
  Rectangle blueRect = Rectangle('blue', 4.0, 6.0);

  // Calling describe method (from Shape class)
  // This method calls calculateArea() and draw() methods
  // Uses the specific implementations from Circle class
  redCircle.describe();
  // Output: This is a red shape with area 78.53975
  // Output: Drawing a circle ⭕

  // Same method call, but uses Rectangle implementations
  blueRect.describe();
  // Output: This is a blue shape with area 24.0
  // Output: Drawing a rectangle ▭
}
```

**🔍 What This Code Does:**

This code demonstrates **runtime polymorphism** and **template method pattern**:

1. **Object Creation**: Creates different shape objects with specific properties (color, dimensions).

2. **Polymorphic Method Calls**: The same `describe()` method call on different objects produces different results:

   - For `Circle`: uses circle's area formula and circle drawing
   - For `Rectangle`: uses rectangle's area formula and rectangle drawing

3. **Template Method in Action**: Shows how the abstract class's `describe()` method acts as a template:

   - Calls `calculateArea()` → uses implementation from specific child class
   - Calls `draw()` → uses implementation from specific child class
   - Provides consistent format but flexible content

4. **Dynamic Behavior**: At runtime, the program determines which implementation to use based on the actual object type, not the variable type.

---

## 🧠 Abstract vs Regular Classes

| **Abstract Class**                   | **Regular Class**                    |
| ------------------------------------ | ------------------------------------ |
| Cannot create objects directly       | Can create objects                   |
| Can have abstract methods (no body)  | All methods must have bodies         |
| Used as blueprints/templates         | Used to create actual objects        |
| Forces children to implement methods | Children can choose what to override |

---

## 🚦 Rules for Abstract Classes

### ✅ **What You CAN Do:**

```dart
// Abstract class demonstrating various allowed features
abstract class Vehicle {
  // ✅ Regular properties are allowed
  // Stores the vehicle brand name
  String brand;

  // ✅ Constructors are allowed in abstract classes
  // Takes brand parameter and assigns to property
  Vehicle(this.brand);

  // ✅ Abstract methods (no implementation)
  // Semicolon indicates no body - child classes must implement
  void startEngine();

  // ✅ Concrete methods (with implementation)
  // All child classes inherit this exact behavior
  void honk() {
    // Shared functionality across all vehicles
    print('Beep beep! 📯');
  }

  // ✅ Static methods are allowed
  // 'static' means method belongs to class, not instances
  // Can be called without creating object: Vehicle.info()
  static void info() {
    // Static methods can't access instance properties
    print('Vehicle information');
  }
}
```

### ❌ **What You CANNOT Do:**

```dart
void main() {
  // ❌ Cannot instantiate abstract class directly
  // This line would cause compilation error
  // Vehicle car = Vehicle('Toyota'); // ERROR!
}

// ❌ Incomplete implementation of abstract class
class Car extends Vehicle {
  // Constructor properly calling super constructor
  Car(String brand) : super(brand);

  // ❌ ERROR: Missing implementation of startEngine() method
  // All abstract methods must be implemented
  // This class would not compile without implementing startEngine()
}
```

---

## 🏆 When to Use Abstract Classes

### 1. **Common Interface + Shared Code**

```dart
// Abstract class combining shared functionality with required implementations
abstract class Animal {
  // Shared property - all animals have names
  String name;

  // Constructor initializing the name property
  Animal(this.name);

  // Abstract method - every animal makes sound differently
  // No implementation provided, child classes decide how
  void makeSound();

  // Concrete method - all animals sleep the same way
  // Shared functionality across all animal types
  void sleep() {
    // String interpolation to include animal's name
    print('$name is sleeping... 😴');
  }
}
```

### 2. **Template Method Pattern**

```dart
// Abstract class defining a process template
abstract class DataProcessor {
  // Template method - defines the complete process
  // 'final' means this method cannot be overridden by child classes
  final void process() {
    // Step 1: Load data (implementation varies by processor type)
    loadData();

    // Step 2: Validate data (implementation varies by processor type)
    validateData();

    // Step 3: Save data (implementation varies by processor type)
    saveData();

    // Step 4: Common completion message for all processors
    print('Processing complete! ✅');
  }

  // Abstract methods - child classes provide specific implementations
  // Each step can be implemented differently based on data type
  void loadData();      // How to load the data
  void validateData();  // How to validate the data
  void saveData();      // How to save the data
}

// Concrete implementation for CSV file processing
class CsvProcessor extends DataProcessor {
  // Implementation of abstract loadData method for CSV files
  @override
  void loadData() => print('Loading CSV file 📄');
  // Arrow function syntax for single-line methods

  // Implementation of abstract validateData method for CSV format
  @override
  void validateData() => print('Validating CSV format ✓');

  // Implementation of abstract saveData method for CSV data
  @override
  void saveData() => print('Saving CSV data 💾');
}
```

### 3. **Enforcing Contracts**

```dart
// Abstract class acting as a contract for payment processing
abstract class PaymentProcessor {
  // Abstract methods - every payment processor MUST implement these
  // Returns boolean to indicate if payment is valid
  bool validatePayment(double amount);

  // Processes the actual payment transaction
  void processPayment(double amount);

  // Sends receipt to customer
  void sendReceipt();

  // Concrete method - common logging for all payment methods
  // All payment processors use the same logging logic
  void logTransaction(double amount) {
    // toStringAsFixed(2) formats number to 2 decimal places
    // Ensures monetary amounts display correctly (e.g., $10.50)
    print('Transaction logged: \$${amount.toStringAsFixed(2)}');
  }
}
```

---

## 🎨 Advanced Features

### Abstract Getters and Setters:

```dart
// Abstract class with abstract properties (getters/setters)
abstract class Account {
  // Abstract getter - child classes must implement how to get balance
  // No implementation provided, just signature
  double get balance;

  // Abstract setter - child classes must implement how to set balance
  // Takes double parameter, no return value
  set balance(double amount);

  // Concrete method using abstract properties
  // Uses the abstract 'balance' getter implemented by child classes
  void displayBalance() {
    // Calls the getter implementation from child class
    // toStringAsFixed(2) formats to 2 decimal places for currency
    print('Current balance: \$${balance.toStringAsFixed(2)}');
  }
}

// Concrete implementation of Account
class SavingsAccount extends Account {
  // Private field to store actual balance value
  // Underscore (_) makes it private to this class
  double _balance = 0.0;

  // Implementation of abstract getter
  // Returns the private _balance field
  @override
  double get balance => _balance;
  // Arrow function syntax for simple getter

  // Implementation of abstract setter
  // Includes validation logic before setting
  @override
  set balance(double amount) {
    // Only set balance if amount is non-negative
    // Prevents negative account balances
    if (amount >= 0) _balance = amount;
    // If amount is negative, balance remains unchanged
  }
}
```

### Factory Constructors in Abstract Classes:

```dart
// Abstract class with factory constructor for object creation
abstract class Logger {
  // Abstract method that all logger implementations must have
  void log(String message);

  // Factory constructor - creates different types of loggers
  // 'factory' keyword indicates this doesn't create instance of Logger
  // Instead, it returns instances of concrete implementations
  factory Logger.create(String type) {
    // Switch statement to determine which logger type to create
    switch (type) {
      case 'console':
        // Return ConsoleLogger instance
        return ConsoleLogger();
      case 'file':
        // Return FileLogger instance
        return FileLogger();
      default:
        // Default case - return ConsoleLogger if type not recognized
        return ConsoleLogger();
    }
    // Factory constructors can return different concrete implementations
    // Based on parameters or conditions
  }
}

// Concrete implementation for console logging
class ConsoleLogger implements Logger {
  // Implementation of abstract log method
  // Prints messages to console with prefix
  @override
  void log(String message) => print('Console: $message');
}

// Concrete implementation for file logging
class FileLogger implements Logger {
  // Implementation of abstract log method
  // In real implementation, this would write to file
  @override
  void log(String message) => print('File: $message');
}
```

---

## 🧩 Summary

| **Concept**         | **What It Means**                                           |
| ------------------- | ----------------------------------------------------------- |
| `abstract class`    | A blueprint that cannot be instantiated directly            |
| `abstract method`   | A method without implementation (just signature)            |
| `extends`           | How concrete classes inherit from abstract classes          |
| `@override`         | Annotation showing you're implementing an abstract method   |
| **Template Method** | Abstract class defines process, children fill in details    |
| **Contract**        | Abstract class forces children to implement certain methods |

---

## 🎉 Final Thoughts

**Abstract classes are like game character templates:**

- 🎯 They define **what** every character must do
- 🎨 They let each character decide **how** to do it
- 🏗️ They provide **common code** that everyone shares
- 🚦 They **enforce rules** so nothing important is forgotten

Perfect for when you know the **structure** but want **flexibility** in implementation!

> **Remember:** Abstract = "Here's the plan, now you fill in the details!" 📋✨
