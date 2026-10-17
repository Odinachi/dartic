# Generics in Dart

Imagine you're running a **magical storage facility** 🏪✨!

You have different types of containers:

- A **cookie jar** 🍪 that should only hold cookies
- A **toy chest** 🧸 that should only hold toys
- A **book shelf** 📚 that should only hold books

But what if you had ONE **smart container** that could safely hold ANY type of item, but once you decide what goes in it, it ONLY accepts that type?

👉 That's exactly what **Generics** do in Dart:

> They let you create **flexible, reusable code** that works with different types while keeping everything **type-safe**!

---

## 🚫 The Problem: Unsafe Storage

```dart
class UnsafeBox {
  dynamic item; // Can hold ANYTHING!

  void store(dynamic something) {
    item = something;
  }

  dynamic retrieve() {
    return item;
  }
}

void main() {
  UnsafeBox box = UnsafeBox();

  box.store('Cookie'); // Store a string
  String cookie = box.retrieve(); // ❌ Might crash if wrong type!

  box.store(42); // Now it has a number
  String number = box.retrieve(); // ❌ CRASH! Expected string, got int
}
```

**🔍 What This Code Does:**

This code demonstrates **the dangers of using dynamic typing without constraints**:

1. **Type Erasure**: Using `dynamic` removes all compile-time type checking, making the code unsafe and prone to runtime errors.

2. **Runtime Type Errors**: The code compiles successfully but crashes at runtime when trying to assign an `int` to a `String` variable.

3. **No IDE Support**: IDEs cannot provide autocomplete, refactoring, or error detection because the type is unknown at compile time.

4. **Maintenance Nightmares**: Developers must manually track what types are stored in the box, leading to bugs and confusion.

5. **Silent Failures**: Type mismatches only become apparent when the code runs, making debugging difficult and expensive.

**Problems:**

- No type safety! 💥
- Runtime crashes! 😱
- Hard to debug! 🐛
- No IDE help! 🤷‍♀️

---

## ✅ The Solution: Generic Magic Box

```dart
class MagicBox<T> {
  T? item;

  void store(T something) {
    item = something;
    print('📦 Stored ${something.runtimeType}: $something');
  }

  T? retrieve() {
    if (item != null) {
      print('📤 Retrieved: $item');
      return item;
    }
    print('📭 Box is empty!');
    return null;
  }

  bool get isEmpty => item == null;
  bool get isNotEmpty => item != null;
}

void main() {
  // Create boxes for specific types
  MagicBox<String> cookieBox = MagicBox<String>();
  MagicBox<int> numberBox = MagicBox<int>();

  cookieBox.store('Chocolate Chip Cookie');
  numberBox.store(42);

  String? cookie = cookieBox.retrieve(); // ✅ Type-safe!
  int? number = numberBox.retrieve();     // ✅ Type-safe!

  print('🍪 Cookie: $cookie');
  print('🔢 Number: $number');

  // cookieBox.store(123); // ❌ Compiler error - can't store int in String box!
}
```

**🔍 What This Code Does:**

This code demonstrates **the power of generics for type safety**:

1. **Parameterized Types**: `<T>` creates a type parameter that can be replaced with any concrete type when instantiating the class.

2. **Compile-Time Safety**: The compiler enforces type constraints, preventing `cookieBox.store(123)` from compiling.

3. **Type Specialization**: `MagicBox<String>` and `MagicBox<int>` are specialized versions that only work with their specific types.

4. **Null Safety Integration**: Uses nullable types (`T?`) to handle empty states safely within Dart's null safety system.

5. **Runtime Type Information**: `something.runtimeType` shows how generic types maintain type information at runtime.

6. **IDE Intelligence**: IDEs can provide autocomplete and error detection because the types are known at compile time.

---

## 🎮 Gaming Example: Inventory System

```dart
class GameInventory<T> {
  List<T> _items = [];
  int maxCapacity;

  GameInventory(this.maxCapacity);

  bool addItem(T item) {
    if (_items.length < maxCapacity) {
      _items.add(item);
      print('✅ Added ${item.toString()} to inventory');
      return true;
    } else {
      print('❌ Inventory full! Cannot add ${item.toString()}');
      return false;
    }
  }

  T? removeItem(int index) {
    if (index >= 0 && index < _items.length) {
      T item = _items.removeAt(index);
      print('🗑️ Removed ${item.toString()} from inventory');
      return item;
    }
    print('❌ Invalid index: $index');
    return null;
  }

  void displayInventory() {
    print('\n🎒 INVENTORY (${_items.length}/$maxCapacity):');
    if (_items.isEmpty) {
      print('   📭 Empty inventory');
    } else {
      for (int i = 0; i < _items.length; i++) {
        print('   ${i + 1}. ${_items[i]}');
      }
    }
    print('');
  }

  List<T> get items => List.unmodifiable(_items);
  int get count => _items.length;
  bool get isFull => _items.length >= maxCapacity;
  bool get isEmpty => _items.isEmpty;
}

// Different item types
class Weapon {
  String name;
  int damage;

  Weapon(this.name, this.damage);

  @override
  String toString() => '$name (⚔️ $damage dmg)';
}

class Potion {
  String name;
  int healing;

  Potion(this.name, this.healing);

  @override
  String toString() => '$name (💚 +$healing HP)';
}

void main() {
  print('🎮 RPG INVENTORY SYSTEM\n');

  // Create different inventories for different item types
  GameInventory<Weapon> weaponInventory = GameInventory<Weapon>(3);
  GameInventory<Potion> potionInventory = GameInventory<Potion>(5);

  // Add weapons
  print('=== WEAPON INVENTORY ===');
  weaponInventory.addItem(Weapon('Iron Sword', 25));
  weaponInventory.addItem(Weapon('Magic Staff', 35));
  weaponInventory.addItem(Weapon('Silver Bow', 30));
  weaponInventory.addItem(Weapon('Dragon Blade', 50)); // Should fail - inventory full

  weaponInventory.displayInventory();

  // Add potions
  print('=== POTION INVENTORY ===');
  potionInventory.addItem(Potion('Health Potion', 50));
  potionInventory.addItem(Potion('Mana Potion', 30));
  potionInventory.addItem(Potion('Super Healing', 100));

  potionInventory.displayInventory();

  // Use items
  print('=== USING ITEMS ===');
  Weapon? weapon = weaponInventory.removeItem(0);
  Potion? potion = potionInventory.removeItem(1);

  if (weapon != null) {
    print('⚔️ Equipped: ${weapon.name}');
  }
  if (potion != null) {
    print('🧪 Drank: ${potion.name}');
  }

  weaponInventory.displayInventory();
  potionInventory.displayInventory();
}
```

**🔍 What This Code Does:**

This code demonstrates **practical generic implementation in game development**:

1. **Generic Container**: `GameInventory<T>` can hold any type of item while maintaining type safety for specific inventories.

2. **Capacity Management**: Implements real game mechanics like inventory limits and full/empty state checking.

3. **Type Specialization**: Separate inventories for `Weapon` and `Potion` types ensure items can't be accidentally mixed or mishandled.

4. **Polymorphic Behavior**: Both `Weapon` and `Potion` classes override `toString()` to provide meaningful representations.

5. **Collection Encapsulation**: Uses private `_items` list with public getter returning unmodifiable view for data protection.

6. **Business Logic Integration**: Generic type system integrates seamlessly with game-specific logic like damage values and healing amounts.

7. **Index-Based Operations**: Safe item removal with bounds checking demonstrates defensive programming with generics.

---

## 🏪 Shopping Cart with Multiple Types

```dart
class ShoppingCart<T> {
  List<CartItem<T>> _items = [];

  void addItem(T product, int quantity, double price) {
    // Check if item already exists
    int existingIndex = _items.indexWhere((item) =>
      item.product.toString() == product.toString());

    if (existingIndex != -1) {
      _items[existingIndex].quantity += quantity;
      print('📦 Updated ${product.toString()}: +$quantity (total: ${_items[existingIndex].quantity})');
    } else {
      _items.add(CartItem<T>(product, quantity, price));
      print('🛒 Added ${product.toString()}: $quantity × \$${price.toStringAsFixed(2)}');
    }
  }

  void removeItem(T product) {
    int index = _items.indexWhere((item) =>
      item.product.toString() == product.toString());

    if (index != -1) {
      CartItem<T> removed = _items.removeAt(index);
      print('🗑️ Removed ${removed.product.toString()} from cart');
    } else {
      print('❌ ${product.toString()} not found in cart');
    }
  }

  double get totalPrice {
    return _items.fold(0.0, (sum, item) => sum + item.totalPrice);
  }

  int get totalItems {
    return _items.fold(0, (sum, item) => sum + item.quantity);
  }

  void displayCart() {
    print('\n🛒 SHOPPING CART:');
    if (_items.isEmpty) {
      print('   📭 Cart is empty');
    } else {
      for (int i = 0; i < _items.length; i++) {
        CartItem<T> item = _items[i];
        print('   ${i + 1}. ${item.product} x${item.quantity} = \$${item.totalPrice.toStringAsFixed(2)}');
      }
      print('   ─' * 30);
      print('   📊 Total Items: $totalItems');
      print('   💰 Total Price: \$${totalPrice.toStringAsFixed(2)}');
    }
    print('');
  }
}

class CartItem<T> {
  T product;
  int quantity;
  double pricePerUnit;

  CartItem(this.product, this.quantity, this.pricePerUnit);

  double get totalPrice => quantity * pricePerUnit;
}

// Product classes
class Electronics {
  String name;
  String brand;

  Electronics(this.name, this.brand);

  @override
  String toString() => '$brand $name';
}

class Clothing {
  String name;
  String size;
  String color;

  Clothing(this.name, this.size, this.color);

  @override
  String toString() => '$color $name ($size)';
}

class Food {
  String name;
  DateTime expiry;

  Food(this.name, this.expiry);

  @override
  String toString() => '$name (exp: ${expiry.day}/${expiry.month})';
}

void main() {
  print('🛍️ MULTI-CATEGORY SHOPPING\n');

  // Create different carts for different product types
  ShoppingCart<Electronics> electronicsCart = ShoppingCart<Electronics>();
  ShoppingCart<Clothing> clothingCart = ShoppingCart<Clothing>();
  ShoppingCart<Food> foodCart = ShoppingCart<Food>();

  // Electronics shopping
  print('=== ELECTRONICS STORE ===');
  electronicsCart.addItem(Electronics('iPhone 15', 'Apple'), 1, 999.99);
  electronicsCart.addItem(Electronics('AirPods', 'Apple'), 2, 179.99);
  electronicsCart.addItem(Electronics('Gaming Mouse', 'Logitech'), 1, 49.99);
  electronicsCart.displayCart();

  // Clothing shopping
  print('=== CLOTHING STORE ===');
  clothingCart.addItem(Clothing('T-Shirt', 'M', 'Blue'), 3, 19.99);
  clothingCart.addItem(Clothing('Jeans', 'L', 'Black'), 1, 59.99);
  clothingCart.addItem(Clothing('Sneakers', '10', 'White'), 1, 89.99);
  clothingCart.displayCart();

  // Food shopping
  print('=== GROCERY STORE ===');
  DateTime nextWeek = DateTime.now().add(Duration(days: 7));
  DateTime nextMonth = DateTime.now().add(Duration(days: 30));

  foodCart.addItem(Food('Milk', nextWeek), 2, 3.99);
  foodCart.addItem(Food('Bread', DateTime(2024, 2, 15)), 1, 2.49);
  foodCart.addItem(Food('Apples', nextMonth), 5, 0.99);
  foodCart.displayCart();

  // Calculate grand total
  double grandTotal = electronicsCart.totalPrice +
                     clothingCart.totalPrice +
                     foodCart.totalPrice;

  print('🧾 GRAND TOTAL ACROSS ALL STORES: \$${grandTotal.toStringAsFixed(2)}');
}
```

**🔍 What This Code Does:**

This code demonstrates **complex e-commerce logic with nested generics**:

1. **Nested Generic Types**: `CartItem<T>` is itself a generic class used within the generic `ShoppingCart<T>` class.

2. **Quantity Management**: Automatically updates quantities for existing items instead of creating duplicates.

3. **Financial Calculations**: Uses `fold()` to aggregate totals across all cart items with proper decimal handling.

4. **Product Comparison**: Uses `toString()` for product comparison, allowing flexible equality checking.

5. **Type-Safe E-commerce**: Each cart specializes in one product type, preventing mixing incompatible products.

6. **Immutable Operations**: Cart modifications return feedback but don't expose internal state directly.

---

## 🏥 Generic Data Structures

### Stack Implementation

```dart
class Stack<T> {
  List<T> _items = [];

  void push(T item) {
    _items.add(item);
    print('📚 Pushed: $item (Stack size: ${_items.length})');
  }

  T? pop() {
    if (_items.isEmpty) {
      print('❌ Cannot pop from empty stack');
      return null;
    }
    T item = _items.removeLast();
    print('📖 Popped: $item (Stack size: ${_items.length})');
    return item;
  }

  T? peek() {
    if (_items.isEmpty) {
      print('👀 Stack is empty');
      return null;
    }
    return _items.last;
  }

  bool get isEmpty => _items.isEmpty;
  bool get isNotEmpty => _items.isNotEmpty;
  int get size => _items.length;

  void display() {
    print('\n📚 STACK CONTENTS (top to bottom):');
    if (_items.isEmpty) {
      print('   📭 Stack is empty');
    } else {
      for (int i = _items.length - 1; i >= 0; i--) {
        String indicator = i == _items.length - 1 ? ' ← top' : '';
        print('   ${_items[i]}$indicator');
      }
    }
    print('');
  }
}

void main() {
  print('📚 GENERIC STACK DEMO\n');

  // String stack for web pages
  Stack<String> browserHistory = Stack<String>();

  print('=== BROWSER HISTORY ===');
  browserHistory.push('google.com');
  browserHistory.push('youtube.com');
  browserHistory.push('github.com');
  browserHistory.display();

  print('Going back...');
  browserHistory.pop();
  browserHistory.pop();
  browserHistory.display();

  // Number stack for calculations
  Stack<int> calculatorStack = Stack<int>();

  print('=== CALCULATOR STACK ===');
  calculatorStack.push(10);
  calculatorStack.push(5);
  calculatorStack.push(3);
  calculatorStack.display();

  print('Performing operations...');
  int? b = calculatorStack.pop();
  int? a = calculatorStack.pop();
  if (a != null && b != null) {
    int result = a + b;
    calculatorStack.push(result);
    print('🧮 Calculated: $a + $b = $result');
  }
  calculatorStack.display();
}
```

**🔍 What This Code Does:**

This code demonstrates **implementing classic data structures with generics**:

1. **LIFO Principle**: Implements Last-In-First-Out behavior with `push()` adding to end and `pop()` removing from end.

2. **Safe Operations**: All operations check for empty state and return nullable types to prevent crashes.

3. **Generic Flexibility**: The same stack implementation works for any type (`String` for browser history, `int` for calculations).

4. **State Visibility**: Provides multiple ways to inspect stack state (`peek()`, `isEmpty`, `size`, `display()`).

5. **Visual Representation**: `display()` method shows stack contents with clear indication of the top element.

6. **Real-World Applications**: Demonstrates browser history and calculator use cases that utilize stack behavior.

### Queue Implementation

```dart
class Queue<T> {
  List<T> _items = [];

  void enqueue(T item) {
    _items.add(item);
    print('➡️ Enqueued: $item (Queue size: ${_items.length})');
  }

  T? dequeue() {
    if (_items.isEmpty) {
      print('❌ Cannot dequeue from empty queue');
      return null;
    }
    T item = _items.removeAt(0);
    print('⬅️ Dequeued: $item (Queue size: ${_items.length})');
    return item;
  }

  T? front() {
    return _items.isEmpty ? null : _items.first;
  }

  T? rear() {
    return _items.isEmpty ? null : _items.last;
  }

  bool get isEmpty => _items.isEmpty;
  int get size => _items.length;

  void display() {
    print('\n🚶 QUEUE CONTENTS (front to rear):');
    if (_items.isEmpty) {
      print('   📭 Queue is empty');
    } else {
      for (int i = 0; i < _items.length; i++) {
        String indicator = i == 0 ? ' ← front' : i == _items.length - 1 ? ' ← rear' : '';
        print('   ${_items[i]}$indicator');
      }
    }
    print('');
  }
}

void main() {
  print('🚶 CUSTOMER SERVICE QUEUE\n');

  Queue<String> customerQueue = Queue<String>();

  // Customers arrive
  customerQueue.enqueue('Alice (Account Issue)');
  customerQueue.enqueue('Bob (Billing Question)');
  customerQueue.enqueue('Charlie (Technical Support)');
  customerQueue.enqueue('Diana (Product Information)');

  customerQueue.display();

  // Serve customers
  print('=== SERVING CUSTOMERS ===');
  while (customerQueue.isNotEmpty) {
    String? customer = customerQueue.dequeue();
    if (customer != null) {
      print('👨‍💼 Now serving: $customer');
      if (customerQueue.isNotEmpty) {
        print('👥 Next in line: ${customerQueue.front()}');
      }
    }
    print('');
  }

  print('✅ All customers served!');
}
```

**🔍 What This Code Does:**

This code demonstrates **FIFO queue implementation with generics**:

1. **FIFO Principle**: Implements First-In-First-Out behavior with `enqueue()` adding to end and `dequeue()` removing from beginning.

2. **Customer Service Model**: Perfect example of real-world queue usage where customers are served in arrival order.

3. **Position Tracking**: `front()` and `rear()` methods allow inspection of queue endpoints without modification.

4. **Service Simulation**: Main function demonstrates complete customer service workflow using the queue.

5. **Generic Type Safety**: Ensures queue only contains the specified type (String for customer names in this case).

---

## 🔧 Generic Functions and Methods

```dart
// Generic function to find maximum
T findMax<T extends Comparable<T>>(List<T> items) {
  if (items.isEmpty) {
    throw ArgumentError('Cannot find max of empty list');
  }

  T max = items[0];
  for (T item in items) {
    if (item.compareTo(max) > 0) {
      max = item;
    }
  }
  return max;
}

// Generic function to swap elements
void swap<T>(List<T> list, int index1, int index2) {
  if (index1 < 0 || index1 >= list.length || index2 < 0 || index2 >= list.length) {
    throw RangeError('Invalid indices');
  }

  T temp = list[index1];
  list[index1] = list[index2];
  list[index2] = temp;

  print('🔄 Swapped positions $index1 and $index2');
}

// Generic function to filter items
List<T> filterItems<T>(List<T> items, bool Function(T) predicate) {
  List<T> filtered = [];
  for (T item in items) {
    if (predicate(item)) {
      filtered.add(item);
    }
  }
  return filtered;
}

// Generic function to transform items
List<R> transformItems<T, R>(List<T> items, R Function(T) transformer) {
  List<R> transformed = [];
  for (T item in items) {
    transformed.add(transformer(item));
  }
  return transformed;
}

void main() {
  print('🔧 GENERIC FUNCTIONS DEMO\n');

  // Find max with different types
  print('=== FINDING MAXIMUM VALUES ===');
  List<int> numbers = [3, 7, 2, 9, 1, 8];
  List<String> words = ['apple', 'zebra', 'banana', 'orange'];

  print('Numbers: $numbers');
  print('Max number: ${findMax(numbers)}');

  print('Words: $words');
  print('Max word (alphabetically): ${findMax(words)}');

  // Swap elements
  print('\n=== SWAPPING ELEMENTS ===');
  List<String> colors = ['red', 'blue', 'green', 'yellow'];
  print('Before swap: $colors');
  swap(colors, 0, 2);
  print('After swap: $colors');

  // Filter items
  print('\n=== FILTERING ITEMS ===');
  List<int> allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  List<int> evenNumbers = filterItems(allNumbers, (n) => n % 2 == 0);
  print('All numbers: $allNumbers');
  print('Even numbers: $evenNumbers');

  List<String> allWords = ['hello', 'world', 'dart', 'programming', 'fun'];
  List<String> longWords = filterItems(allWords, (word) => word.length > 4);
  print('All words: $allWords');
  print('Long words: $longWords');

  // Transform items
  print('\n=== TRANSFORMING ITEMS ===');
  List<int> lengths = transformItems(allWords, (word) => word.length);
  print('Words: $allWords');
  print('Lengths: $lengths');

  List<String> upperCaseWords = transformItems(allWords, (word) => word.toUpperCase());
  print('Uppercase: $upperCaseWords');
}
```

**🔍 What This Code Does:**

This code demonstrates **generic functions and advanced type constraints**:

1. **Bounded Generics**: `T extends Comparable<T>` constrains the type parameter to only types that can be compared.

2. **Algorithm Generalization**: `findMax()` works with any comparable type (numbers, strings, dates) using the same algorithm.

3. **Type-Safe Operations**: `swap()` can swap elements of any type while maintaining type safety and bounds checking.

4. **Higher-Order Functions**: `filterItems()` and `transformItems()` accept function parameters, enabling functional programming patterns.

5. **Multiple Type Parameters**: `transformItems<T, R>()` uses two type parameters for input and output types, enabling type transformations.

6. **Function Type Annotations**: Uses proper function type syntax like `bool Function(T)` for type-safe callbacks.

---

## 🎯 Generic Constraints

```dart
// Constraint: T must implement Comparable
class SortedList<T extends Comparable<T>> {
  List<T> _items = [];

  void add(T item) {
    _items.add(item);
    _items.sort(); // This works because T implements Comparable
    print('➕ Added $item. Sorted list: $_items');
  }

  T? get smallest => _items.isEmpty ? null : _items.first;
  T? get largest => _items.isEmpty ? null : _items.last;
}

// Constraint: T must extend a specific class
abstract class Animal {
  String name;
  Animal(this.name);
  void makeSound();
}

class Dog extends Animal {
  Dog(String name) : super(name);
  @override
  void makeSound() => print('$name says: Woof! 🐕');
}

class Cat extends Animal {
  Cat(String name) : super(name);
  @override
  void makeSound() => print('$name says: Meow! 🐱');
}

class AnimalShelter<T extends Animal> {
  List<T> animals = [];

  void addAnimal(T animal) {
    animals.add(animal);
    print('🏠 Added ${animal.name} to the shelter');
  }

  void makeAllSounds() {
    print('🔊 All animals making sounds:');
    for (T animal in animals) {
      animal.makeSound(); // This works because T extends Animal
    }
  }
}

void main() {
  print('🎯 GENERIC CONSTRAINTS DEMO\n');

  // Sorted list demo
  print('=== SORTED LIST ===');
  SortedList<int> sortedNumbers = SortedList<int>();
  sortedNumbers.add(5);
  sortedNumbers.add(2);
  sortedNumbers.add(8);
  sortedNumbers.add(1);

  print('Smallest: ${sortedNumbers.smallest}');
  print('Largest: ${sortedNumbers.largest}');

  // Animal shelter demo
  print('\n=== ANIMAL SHELTER ===');
  AnimalShelter<Dog> dogShelter = AnimalShelter<Dog>();
  dogShelter.addAnimal(Dog('Buddy'));
  dogShelter.addAnimal(Dog('Max'));
  dogShelter.makeAllSounds();

  AnimalShelter<Cat> catShelter = AnimalShelter<Cat>();
  catShelter.addAnimal(Cat('Whiskers'));
  catShelter.addAnimal(Cat('Luna'));
  catShelter.makeAllSounds();
}
```

**🔍 What This Code Does:**

This code demonstrates **generic constraints for enhanced type safety**:

1. **Interface Constraints**: `T extends Comparable<T>` ensures only sortable types can be used in `SortedList`.

2. **Automatic Sorting**: Because of the constraint, `_items.sort()` is guaranteed to work without runtime type checking.

3. **Class Hierarchy Constraints**: `T extends Animal` ensures `AnimalShelter` only accepts animal subtypes.

4. **Method Availability**: Constraints guarantee certain methods (like `makeSound()`) are available on the generic type.

5. **Type Specialization**: `AnimalShelter<Dog>` and `AnimalShelter<Cat>` create specialized shelters while maintaining common behavior.

6. **Compile-Time Validation**: Constraints are checked at compile time, preventing invalid type usage before runtime.

---

## 🧠 Built-in Generic Collections

```dart
void main() {
  print('📦 BUILT-IN GENERIC COLLECTIONS\n');

  // Lists
  List<String> fruits = ['apple', 'banana', 'orange'];
  List<int> scores = [95, 87, 92, 78];

  print('🍎 Fruits: $fruits');
  print('📊 Scores: $scores');

  // Sets (no duplicates)
  Set<String> uniqueColors = {'red', 'blue', 'green', 'red'}; // 'red' appears only once
  print('🎨 Unique colors: $uniqueColors');

  // Maps (key-value pairs)
  Map<String, int> ages = {
    'Alice': 25,
    'Bob': 30,
    'Charlie': 22
  };
  print('👥 Ages: $ages');

  // Nested generics
  List<Map<String, dynamic>> students = [
    {'name': 'Alice', 'grade': 'A', 'age': 20},
    {'name': 'Bob', 'grade': 'B', 'age': 21},
  ];
  print('🎓 Students: $students');

  // Generic methods on collections
  print('\n=== GENERIC COLLECTION METHODS ===');

  // Where (filter)
  List<int> evenScores = scores.where((score) => score % 2 == 0).toList();
  print('Even scores: $evenScores');

  // Map (transform)
  List<String> fruitLengths = fruits.map((fruit) => '${fruit.length} chars').toList();
  print('Fruit lengths: $fruitLengths');

  // Reduce
  int totalScore = scores.reduce((a, b) => a + b);
  print('Total score: $totalScore');

  // Fold
  String allFruits = fruits.fold('Fruits: ', (prev, fruit) => prev + fruit + ' ');
  print(allFruits);
}
```

**🔍 What This Code Does:**

This code demonstrates **Dart's built-in generic collection types and methods**:

1. **Type-Safe Collections**: Each collection (`List<String>`, `Set<String>`, `Map<String, int>`) enforces type constraints.

2. **Automatic Deduplication**: `Set<String>` automatically removes duplicate 'red' entries, showing set behavior.

3. **Nested Generic Types**: `List<Map<String, dynamic>>` shows how generics can be nested for complex data structures.

4. **Functional Methods**: `where()`, `map()`, `reduce()`, and `fold()` demonstrate generic functional programming methods.

5. **Type Inference**: Dart can often infer generic types from context, reducing boilerplate code.

6. **Collection Transformations**: Shows how to transform data while maintaining type safety throughout the pipeline.

---

## 📊 Quick Reference Guide

### Generic Syntax

```dart
// Generic class
class Container<T> {
  T item;
  Container(this.item);
}

// Generic function
T identity<T>(T value) => value;

// Generic with constraints
class NumberContainer<T extends num> {
  T number;
  NumberContainer(this.number);
}

// Multiple type parameters
class Pair<K, V> {
  K key;
  V value;
  Pair(this.key, this.value);
}
```

### Common Generic Types

| Type          | Description        | Example                   |
| ------------- | ------------------ | ------------------------- |
| `List<T>`     | Ordered collection | `List<String> names`      |
| `Set<T>`      | Unique items       | `Set<int> uniqueNumbers`  |
| `Map<K, V>`   | Key-value pairs    | `Map<String, int> ages`   |
| `Iterable<T>` | Sequence of items  | `Iterable<double> values` |
| `Future<T>`   | Async result       | `Future<String> data`     |
| `Stream<T>`   | Async sequence     | `Stream<int> numbers`     |

---

## 🎯 When to Use Generics

**✅ Perfect for:**

- **Collections** that hold items of the same type
- **Reusable code** that works with multiple types
- **Type-safe APIs** that prevent runtime errors
- **Data structures** like stacks, queues, trees

**❌ Not needed for:**

- **Simple functions** that don't work with types
- **One-time use** code that won't be reused
- **Dynamic content** where type changes frequently

---

## 🚀 Practice Challenges

Try creating these generic classes:

1. **🎯 GenericPair**: Hold two values of potentially different types
2. **📊 Statistics**: Calculate averages, min, max for any numeric type
3. **🔄 CircularBuffer**: Fixed-size buffer that overwrites old data
4. **🌳 BinaryTree**: Tree structure that works with comparable types

---

## 🎉 Remember This!

Generics are like **smart molds** 🏭:

- **🔧 Flexible**: One mold, many shapes
- **🛡️ Safe**: Only the right type fits
- **♻️ Reusable**: Use the same code for different types
- **⚡ Efficient**: No boxing/unboxing, no type checking at runtime

**The Magic**: You write the code once, but it works safely with many different types!

> **Think of it like**: "I'm making a cookie cutter that can cut ANY shape, but once I tell it to cut stars, it ONLY cuts perfect stars!" ⭐🍪

Generics make your code **flexible** AND **safe** at the same time! 🎪✨
