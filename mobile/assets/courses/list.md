# Lists in Dart

Imagine you're organizing a **pizza party** 🍕 for your friends!

You need to keep track of:

- 👥 **Guest list** (who's coming)
- 🍕 **Pizza flavors** (what to order)
- 🎵 **Playlist** (songs to play)
- 🎮 **Games** (fun activities)

Instead of writing each thing on separate pieces of paper, you put them all on **one organized list**!

👉 A **List** in Dart works exactly like this party planning list:

> It's a **container** that holds multiple items in a **specific order**, and you can easily **add**, **remove**, or **find** things!

---

## 🎁 The Magic of Lists

```dart
void main() {
  // Create a guest list for the party
  List<String> guests = ['Alice', 'Bob', 'Charlie', 'Diana'];

  print('🎉 Party Guest List: $guests');
  print('📊 Total guests: ${guests.length}');
  print('👋 First guest: ${guests[0]}');
  print('🎊 Last guest: ${guests[guests.length - 1]}');
}
```

**🔍 What This Code Does:**

This code demonstrates **basic list creation and access patterns**:

1. **Generic Type Declaration**: `List<String>` specifies that this list only contains String values, providing type safety.

2. **List Literal Syntax**: Square brackets `[]` with comma-separated values create a list with initial data.

3. **Length Property**: `guests.length` returns the number of items in the list, useful for bounds checking and iteration.

4. **Index-Based Access**: `guests[0]` accesses the first element using zero-based indexing, fundamental to list operations.

5. **Dynamic Length Calculation**: `guests[guests.length - 1]` safely accesses the last element by calculating its position.

6. **String Interpolation**: List contents are displayed directly in print statements using string interpolation.

---

## 🔢 Understanding List Indexes

Lists are like **hotel rooms** with **room numbers**! Each item has a specific position:

```dart
void main() {
  List<String> pizzaFlavors = ['Pepperoni', 'Hawaiian', 'Veggie', 'Margherita'];

  print('🏨 PIZZA HOTEL - Room Numbers:');
  print('');

  for (int i = 0; i < pizzaFlavors.length; i++) {
    print('🚪 Room $i: ${pizzaFlavors[i]}');
  }

  print('');
  print('📍 Quick Access:');
  print('First pizza (room 0): ${pizzaFlavors[0]}');
  print('Second pizza (room 1): ${pizzaFlavors[1]}');
  print('Last pizza: ${pizzaFlavors.last}');
}
```

**🔍 What This Code Does:**

This code demonstrates **zero-based indexing and list traversal**:

1. **Zero-Based Indexing**: Shows how list positions start at 0, not 1, which is fundamental to programming.

2. **Bounds-Safe Iteration**: `i < pizzaFlavors.length` ensures the loop doesn't exceed list boundaries.

3. **Index-Value Relationship**: Demonstrates the connection between numerical positions and actual data values.

4. **Multiple Access Patterns**: Shows both manual indexing (`[0]`, `[1]`) and convenient properties (`.last`).

5. **Visual Learning Aid**: Uses hotel room analogy to make abstract indexing concept concrete and memorable.

---

## ➕ Adding Items to Lists

### Adding to the End

```dart
void main() {
  List<String> shoppingCart = ['Apples', 'Bread'];

  print('🛒 Shopping Cart: $shoppingCart');

  // Add one item
  shoppingCart.add('Milk');
  print('➕ Added Milk: $shoppingCart');

  // Add multiple items
  shoppingCart.addAll(['Eggs', 'Cheese', 'Butter']);
  print('➕ Added dairy products: $shoppingCart');

  print('📊 Total items: ${shoppingCart.length}');
}
```

**🔍 What This Code Does:**

This code demonstrates **dynamic list modification**:

1. **Mutable Lists**: Shows that lists can be modified after creation, unlike some immutable data structures.

2. **Single Item Addition**: `add()` method appends one item to the end of the list, maintaining order.

3. **Bulk Addition**: `addAll()` method efficiently adds multiple items from another collection in one operation.

4. **State Tracking**: Demonstrates how list length automatically updates as items are added.

5. **Real-World Application**: Shopping cart example shows practical use case for dynamic list operations.

### Adding at Specific Positions

```dart
void main() {
  List<String> playlist = ['Song A', 'Song C', 'Song D'];

  print('🎵 Original Playlist: $playlist');

  // Insert at specific position (index 1)
  playlist.insert(1, 'Song B');
  print('🎶 Inserted Song B at position 1: $playlist');

  // Insert multiple songs at once
  playlist.insertAll(0, ['Intro', 'Welcome']);
  print('🎼 Added intro songs: $playlist');
}
```

**🔍 What This Code Does:**

This code demonstrates **positional insertion capabilities**:

1. **Precise Placement**: `insert()` method allows adding items at any position, not just the end.

2. **Index Shifting**: When items are inserted, existing items automatically shift to accommodate new entries.

3. **Order Preservation**: Maintains the sequence integrity of the list while allowing modifications.

4. **Batch Insertion**: `insertAll()` inserts multiple items at a specific position efficiently.

5. **Playlist Management**: Shows how ordered collections benefit from positional insertion (song ordering matters).

---

## ➖ Removing Items from Lists

```dart
void main() {
  List<String> todoList = ['Wake up', 'Brush teeth', 'Eat breakfast', 'Go to school', 'Do homework'];

  print('📝 Original Todo List: $todoList');
  print('');

  // Remove specific item
  todoList.remove('Brush teeth');
  print('✅ Completed: Brush teeth');
  print('📝 Updated list: $todoList');

  // Remove by index
  String completed = todoList.removeAt(0);
  print('✅ Completed: $completed');
  print('📝 Updated list: $todoList');

  // Remove last item
  String lastTask = todoList.removeLast();
  print('✅ Completed: $lastTask');
  print('📝 Final list: $todoList');

  // Remove multiple items
  todoList.removeRange(0, 2);
  print('✅ Completed multiple tasks');
  print('📝 Remaining: $todoList');
}
```

**🔍 What This Code Does:**

This code demonstrates **various list removal strategies**:

1. **Value-Based Removal**: `remove()` finds and removes the first occurrence of a specific value.

2. **Index-Based Removal**: `removeAt()` removes an item at a specific position and returns the removed value.

3. **Convenience Methods**: `removeLast()` provides optimized removal from the end of the list.

4. **Range Removal**: `removeRange()` efficiently removes multiple consecutive items.

5. **Return Values**: Some removal methods return the removed items, allowing for confirmation or further processing.

6. **Task Management**: Todo list example demonstrates practical use cases for different removal patterns.

---

## 🔍 Finding and Checking Items

```dart
void main() {
  List<String> students = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'];

  print('👥 Class Roster: $students\n');

  // Check if someone is in the class
  String checkStudent = 'Bob';
  if (students.contains(checkStudent)) {
    print('✅ $checkStudent is in the class!');
    print('📍 Position: ${students.indexOf(checkStudent)}');
  } else {
    print('❌ $checkStudent is not in the class');
  }

  // Find where someone sits
  print('📍 Charlie sits at position: ${students.indexOf('Charlie')}');

  // Check if list is empty
  print('📊 Class is empty: ${students.isEmpty}');
  print('📊 Class has students: ${students.isNotEmpty}');

  // Get first and last students
  print('🥇 First student: ${students.first}');
  print('🏁 Last student: ${students.last}');
}
```

**🔍 What This Code Does:**

This code demonstrates **list search and query operations**:

1. **Membership Testing**: `contains()` checks if a specific value exists in the list, returning boolean.

2. **Position Finding**: `indexOf()` returns the numerical position of an item or -1 if not found.

3. **Conditional Logic**: Combines search results with if-statements for robust error handling.

4. **State Queries**: `isEmpty` and `isNotEmpty` provide safe ways to check list state before operations.

5. **Boundary Access**: `first` and `last` properties provide convenient access to list boundaries.

6. **Classroom Management**: Student roster example shows practical applications of search operations.

---

## 🔄 Looping Through Lists

### For-Each Loop (Easiest)

```dart
void main() {
  List<String> iceCreamFlavors = ['Vanilla', 'Chocolate', 'Strawberry', 'Mint'];

  print('🍦 ICE CREAM MENU:');
  print('');

  for (String flavor in iceCreamFlavors) {
    print('🍨 Delicious $flavor ice cream!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **enhanced for-loop syntax for simple iteration**:

1. **Simplified Syntax**: `for (String flavor in iceCreamFlavors)` provides clean, readable iteration.

2. **Type Safety**: Compiler knows each `flavor` is a String, enabling autocomplete and error checking.

3. **No Index Management**: Eliminates off-by-one errors and bounds checking concerns.

4. **Value-Focused**: When you need items but not their positions, this is the most efficient approach.

5. **Readability**: Code clearly expresses intent to process each item in the collection.

### For Loop with Index

```dart
void main() {
  List<String> subjects = ['Math', 'Science', 'History', 'Art'];

  print('📚 CLASS SCHEDULE:');
  print('');

  for (int i = 0; i < subjects.length; i++) {
    print('📖 Period ${i + 1}: ${subjects[i]}');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **traditional indexed iteration**:

1. **Index Access**: Provides access to both the position (`i`) and value (`subjects[i]`) of each element.

2. **Mathematical Operations**: Can perform calculations with indices (like `i + 1` for human-readable periods).

3. **Bounds Checking**: Uses `i < subjects.length` to prevent array out-of-bounds errors.

4. **Fine Control**: Allows skipping items, reverse iteration, or custom step sizes.

5. **Numbering Systems**: Perfect when position information is needed for display or logic.

### Advanced Iteration

```dart
void main() {
  List<int> scores = [85, 92, 78, 96, 89];

  print('📊 GAME SCORES ANALYSIS:');
  print('');

  // Using forEach method
  scores.forEach((score) {
    if (score >= 90) {
      print('🏆 Excellent score: $score');
    } else if (score >= 80) {
      print('👍 Good score: $score');
    } else {
      print('📈 Keep practicing: $score');
    }
  });
}
```

**🔍 What This Code Does:**

This code demonstrates **functional programming iteration patterns**:

1. **Method-Based Iteration**: `forEach()` method takes a function that processes each element.

2. **Anonymous Functions**: Uses arrow syntax `(score) => {...}` for inline function definitions.

3. **Conditional Processing**: Shows how to apply different logic based on element values.

4. **Score Classification**: Demonstrates practical use case for value-based processing.

5. **Functional Style**: Introduces functional programming concepts in an accessible way.

---

## 🛠️ List Operations and Methods

```dart
void main() {
  List<int> numbers = [1, 2, 3, 4, 5];

  print('🔢 Original numbers: $numbers\n');

  // Reverse the list
  List<int> reversed = numbers.reversed.toList();
  print('🔄 Reversed: $reversed');

  // Sort the list (works with a copy)
  List<int> unsorted = [5, 2, 8, 1, 9, 3];
  print('🔀 Unsorted: $unsorted');
  unsorted.sort();
  print('📈 Sorted: $unsorted');

  // Get a portion of the list
  List<int> portion = numbers.sublist(1, 4);
  print('✂️ Portion (index 1-3): $portion');

  // Clear all items
  List<String> tempList = ['A', 'B', 'C'];
  print('📝 Before clear: $tempList');
  tempList.clear();
  print('🗑️ After clear: $tempList');
}
```

**🔍 What This Code Does:**

This code demonstrates **advanced list manipulation operations**:

1. **Non-Destructive Operations**: `reversed.toList()` creates a new list without modifying the original.

2. **In-Place Sorting**: `sort()` modifies the original list to arrange elements in ascending order.

3. **Sublist Extraction**: `sublist(start, end)` creates a new list containing a portion of the original.

4. **Complete Removal**: `clear()` removes all elements efficiently, resetting the list to empty state.

5. **Memory Management**: Shows both preservation (copying) and modification (in-place) approaches.

---

## 🎮 Interactive Game Example

```dart
void main() {
  List<String> playerInventory = [];
  List<String> availableItems = ['Sword', 'Shield', 'Potion', 'Key', 'Map'];

  print('🎮 ADVENTURE GAME - INVENTORY SYSTEM\n');

  // Player finds items
  print('🗡️ You found a Sword!');
  playerInventory.add('Sword');

  print('🛡️ You found a Shield!');
  playerInventory.add('Shield');

  print('🧪 You found 3 Potions!');
  for (int i = 0; i < 3; i++) {
    playerInventory.add('Potion');
  }

  // Display inventory
  print('\n🎒 YOUR INVENTORY:');
  for (int i = 0; i < playerInventory.length; i++) {
    print('  ${i + 1}. ${playerInventory[i]}');
  }

  // Count specific items
  int potionCount = 0;
  for (String item in playerInventory) {
    if (item == 'Potion') potionCount++;
  }

  print('\n📊 INVENTORY STATS:');
  print('📦 Total items: ${playerInventory.length}');
  print('🧪 Potions: $potionCount');
  print('⚔️ Weapons: ${playerInventory.contains('Sword') ? 1 : 0}');
  print('🛡️ Shields: ${playerInventory.contains('Shield') ? 1 : 0}');

  // Use a potion
  if (playerInventory.contains('Potion')) {
    print('\n💚 You used a potion to restore health!');
    playerInventory.remove('Potion');
    print('🧪 Potions remaining: ${playerInventory.where((item) => item == 'Potion').length}');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **comprehensive game inventory management system**:

1. **Dynamic Inventory**: Starts with empty list and builds inventory as items are discovered.

2. **Item Collection**: Shows realistic game progression where players collect items over time.

3. **Inventory Display**: Creates numbered list display similar to actual game interfaces.

4. **Item Counting**: Demonstrates multiple approaches to count specific items in collections.

5. **Conditional Logic**: Uses ternary operators for concise conditional value assignment.

6. **Item Usage**: Shows item consumption with immediate inventory update and feedback.

7. **Advanced Queries**: Uses `where()` method for complex filtering operations.

---

## 📚 Different Types of Lists

### String Lists

```dart
void main() {
  List<String> bookTitles = [
    'Harry Potter',
    'Lord of the Rings',
    'The Hunger Games',
    'Percy Jackson'
  ];

  print('📚 LIBRARY COLLECTION:\n');

  for (String book in bookTitles) {
    print('📖 "$book" - Available for checkout');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **string-specific list operations**:

1. **Multi-Line Declaration**: Shows how to format long lists for better readability.

2. **String Handling**: Demonstrates that strings in lists maintain their full content and formatting.

3. **Library System**: Provides practical example of string collections in real applications.

### Number Lists

```dart
void main() {
  List<int> temperatures = [72, 75, 68, 82, 77, 71, 79];

  print('🌡️ WEEKLY TEMPERATURE REPORT:\n');

  int total = 0;
  for (int temp in temperatures) {
    total += temp;
    String description = temp > 75 ? 'Warm 🌞' : temp < 70 ? 'Cool 🧥' : 'Nice 😊';
    print('📊 ${temp}°F - $description');
  }

  double average = total / temperatures.length;
  print('\n📈 Average temperature: ${average.toStringAsFixed(1)}°F');
}
```

**🔍 What This Code Does:**

This code demonstrates **numerical list processing with statistical calculations**:

1. **Accumulation Pattern**: Uses running total to sum all temperatures for average calculation.

2. **Conditional Classification**: Applies different logic based on numerical ranges for temperature categories.

3. **Mathematical Operations**: Performs division and uses `toStringAsFixed()` for formatted decimal output.

4. **Data Analysis**: Shows how lists enable statistical analysis of collected data.

### Mixed Data Lists

```dart
void main() {
  // List of Maps (like a contact book)
  List<Map<String, dynamic>> contacts = [
    {'name': 'Alice', 'age': 25, 'city': 'New York'},
    {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'},
    {'name': 'Charlie', 'age': 22, 'city': 'Chicago'},
  ];

  print('📱 CONTACT BOOK:\n');

  for (Map<String, dynamic> contact in contacts) {
    print('👤 ${contact['name']}');
    print('   🎂 Age: ${contact['age']}');
    print('   🏙️ City: ${contact['city']}\n');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **complex data structures using lists of maps**:

1. **Structured Data**: Each contact is a Map with multiple properties (name, age, city).

2. **Dynamic Typing**: `Map<String, dynamic>` allows different value types within the same structure.

3. **Data Access**: Shows how to access nested data using bracket notation for map keys.

4. **Database-Like Structure**: Demonstrates how lists can model database tables or structured records.

5. **Contact Management**: Provides practical example of complex data organization in applications.

---

## 🎯 List Best Practices

### Creating Lists

```dart
void main() {
  // Different ways to create lists

  // 1. Empty list
  List<String> emptyList = [];
  List<String> emptyList2 = <String>[];

  // 2. List with initial values
  List<int> numbers = [1, 2, 3, 4, 5];

  // 3. Fixed-length list
  List<String> fixedList = List.filled(3, 'placeholder');
  print('Fixed list: $fixedList');

  // 4. Generated list
  List<int> squares = List.generate(5, (index) => index * index);
  print('Squares: $squares');

  // 5. List from other collections
  List<String> fromSet = {'apple', 'banana', 'cherry'}.toList();
  print('From set: $fromSet');
}
```

**🔍 What This Code Does:**

This code demonstrates **various list creation patterns and factory methods**:

1. **Empty List Syntax**: Shows two equivalent ways to create empty typed lists.

2. **Literal Initialization**: Direct creation with initial values using bracket notation.

3. **Factory Constructors**: `List.filled()` creates lists with repeated values, useful for initialization.

4. **Generated Lists**: `List.generate()` uses a function to create list contents programmatically.

5. **Type Conversion**: Shows how to convert other collection types (Set) into lists.

6. **Functional Programming**: Generator functions demonstrate higher-order function usage.

### Safe List Operations

```dart
void main() {
  List<String> fruits = ['apple', 'banana', 'cherry'];

  // Safe way to access items
  int index = 1;
  if (index < fruits.length) {
    print('✅ Safe access: ${fruits[index]}');
  } else {
    print('❌ Index out of bounds!');
  }

  // Safe way to check if empty
  if (fruits.isNotEmpty) {
    print('✅ First fruit: ${fruits.first}');
    print('✅ Last fruit: ${fruits.last}');
  }

  // Safe removal
  if (fruits.contains('banana')) {
    fruits.remove('banana');
    print('✅ Removed banana: $fruits');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **defensive programming practices for list operations**:

1. **Bounds Checking**: Validates index before access to prevent runtime exceptions.

2. **Empty List Protection**: Uses `isNotEmpty` to ensure safe access to `first` and `last` properties.

3. **Existence Verification**: Checks if items exist before attempting removal operations.

4. **Error Prevention**: Shows proactive approaches to avoid common list-related runtime errors.

5. **Robust Code**: Demonstrates patterns that make applications more stable and user-friendly.

---

## 📊 Quick Reference Guide

### Essential List Methods

| Method       | Purpose                  | Example                  |
| ------------ | ------------------------ | ------------------------ |
| `add()`      | Add item to end          | `list.add('item')`       |
| `insert()`   | Add at specific position | `list.insert(0, 'item')` |
| `remove()`   | Remove specific item     | `list.remove('item')`    |
| `removeAt()` | Remove by index          | `list.removeAt(0)`       |
| `contains()` | Check if item exists     | `list.contains('item')`  |
| `indexOf()`  | Find item position       | `list.indexOf('item')`   |
| `length`     | Get list size            | `list.length`            |
| `isEmpty`    | Check if empty           | `list.isEmpty`           |
| `clear()`    | Remove all items         | `list.clear()`           |
| `sort()`     | Sort items               | `list.sort()`            |

### Common Patterns

```dart
// Loop through with index
for (int i = 0; i < list.length; i++) {
  print('${i}: ${list[i]}');
}

// Loop through items only
for (String item in list) {
  print(item);
}

// Check before accessing
if (list.isNotEmpty) {
  print(list.first);
}
```

---

## 🚀 Practice Challenges

Try creating these lists:

1. **🎵 Music Playlist**: Create a playlist, add songs, remove duplicates
2. **🛒 Shopping List**: Add items, mark as bought (remove), calculate total
3. **📝 Grade Tracker**: Store grades, calculate average, find highest/lowest
4. **👥 Friend List**: Manage friends, check if someone is a friend, sort alphabetically

---

## 🎉 Remember This!

Lists are like **organized containers** 📦:

- **📋 Ordered**: Items stay in the order you put them
- **🔢 Indexed**: Each item has a number (starting from 0)
- **📈 Dynamic**: Can grow or shrink as needed
- **🔍 Searchable**: Easy to find and check items
- **🔄 Flexible**: Add, remove, or change items anytime

**The Magic**: Lists help you organize multiple related items so you can work with them efficiently - just like organizing your room with labeled boxes! 🏠✨

**Pro Tip**: Always check if a list is empty before accessing `first` or `last` to avoid errors! 🛡️
