# Anonymous Functions in Dart

Imagine you're at a pizza party 🍕 and someone shouts:

> "Hey! Whoever finishes their slice first, grab more napkins from the kitchen!"

Nobody gets assigned this task by name — it's just a job that needs doing. The first person done just does it!

👉 That's exactly what an **anonymous function** is: a **function without a name** that just gets the job done when needed!

---

## 🏷️ Regular Functions (With Names)

These are like having assigned chores with your name on them:

```dart
double calculateTip(double bill) {
  return bill * 0.15;
}

void greetCustomer(String name) {
  print('Welcome, $name! Enjoy your meal!');
}

void main() {
  double tip = calculateTip(50.0);
  greetCustomer('Sarah');
  print('Tip: \$${tip}');
}
```

**🔍 What This Code Does:**

This code demonstrates **traditional named functions** with clear identifiers:

1. **Function Declaration**: `calculateTip` and `greetCustomer` are declared with specific names that describe their purpose.

2. **Reusability**: These named functions can be called multiple times throughout the program from any scope where they're accessible.

3. **Type Safety**: Each function specifies parameter types (`double`, `String`) and return types, providing compile-time error checking.

4. **Clear Intent**: Function names make the code self-documenting - `calculateTip(50.0)` immediately tells you what's happening.

5. **Memory Storage**: Named functions are stored in memory with their identifiers and can be referenced throughout the program's execution.

**Output:**

```
Welcome, Sarah! Enjoy your meal!
Tip: $7.5
```

---

## 👤 Anonymous Functions (No Names)

These are like spontaneous helpers — no name tags needed!

### Basic Anonymous Function

```dart
void main() {
  var makeSound = () {
    print('🔊 Beep beep!');
  };

  makeSound(); // Output: 🔊 Beep beep!
}
```

**🔍 What This Code Does:**

This code demonstrates **basic anonymous function creation and usage**:

1. **Anonymous Declaration**: The function `() { print('🔊 Beep beep!'); }` has no name - it's defined inline without an identifier.

2. **Variable Storage**: The anonymous function is stored in the variable `makeSound`, which acts as a reference to the function.

3. **Type Inference**: Dart automatically determines that `makeSound` is of type `Function` based on the assigned value.

4. **Immediate Usability**: Once stored in a variable, the anonymous function can be called just like a named function using parentheses.

5. **Scope Limitation**: This function only exists within the scope where it's defined (inside `main()` in this case).

### Anonymous Function with Parameters

```dart
void main() {
  var multiplyByTwo = (int number) {
    return number * 2;
  };

  print(multiplyByTwo(7)); // Output: 14
  print(multiplyByTwo(25)); // Output: 50
}
```

**🔍 What This Code Does:**

This code shows **anonymous functions with parameters and return values**:

1. **Parameter Definition**: `(int number)` defines that this function accepts one integer parameter named `number`.

2. **Return Value**: The function calculates and returns the input multiplied by 2, demonstrating that anonymous functions can return values.

3. **Variable Assignment**: The anonymous function is stored in `multiplyByTwo` variable for later use.

4. **Multiple Calls**: Shows how the same anonymous function can be called multiple times with different arguments (7 and 25).

5. **Type Safety**: The parameter type `int` ensures only integers can be passed to this function.

### Arrow Function Syntax (Super Short!)

```dart
void main() {
  var addFive = (int x) => x + 5;
  var isEven = (int num) => num % 2 == 0;

  print(addFive(10));    // Output: 15
  print(isEven(8));      // Output: true
  print(isEven(7));      // Output: false
}
```

**🔍 What This Code Does:**

This code demonstrates **arrow function syntax** for concise anonymous functions:

1. **Arrow Syntax**: The `=>` operator provides a shorthand for simple functions that return a single expression.

2. **Expression Evaluation**: `x + 5` is automatically returned without needing an explicit `return` statement.

3. **Boolean Logic**: `isEven` uses modulo operator (`%`) to determine if a number is even by checking if remainder is 0.

4. **Concise Code**: Arrow functions reduce boilerplate code for simple operations, making code more readable.

5. **Implicit Return**: The expression after `=>` is automatically returned, eliminating the need for curly braces and return statements.

---

## 🚀 Immediately Invoked Functions

Sometimes you want to run a function right away, just once:

```dart
void main() {
  print('Starting app...');

  () {
    print('🎉 App initialized!');
    print('Ready for users!');
  }();

  print('App is running...');
}
```

**🔍 What This Code Does:**

This code demonstrates **immediately invoked function expressions (IIFE)**:

1. **Immediate Execution**: The `()` at the end of the function definition executes it immediately upon creation.

2. **One-Time Use**: This function runs once and cannot be called again since it's not stored in a variable.

3. **Isolation**: Creates a temporary scope for initialization code that doesn't pollute the main function scope.

4. **Sequential Execution**: The function executes in order with the surrounding code, useful for setup tasks.

5. **No Storage**: Unlike stored anonymous functions, this executes and disappears immediately.

**Output:**

```
Starting app...
🎉 App initialized!
Ready for users!
App is running...
```

---

## 📝 Real-World Example: Processing Lists

### Scenario: Restaurant Order Processing

```dart
void main() {
  var orders = ['Pizza', 'Burger', 'Salad', 'Pasta', 'Tacos'];
  var prices = [12.99, 8.50, 7.25, 11.00, 9.75];

  print('=== RESTAURANT ORDERS ===');

  orders.forEach((order) {
    print('✅ Preparing: $order');
  });

  print('\n=== PRICE CALCULATION ===');

  var pricesWithTax = prices.map((price) {
    return price * 1.08;
  }).toList();

  for (int i = 0; i < orders.length; i++) {
    print('${orders[i]}: \$${prices[i]} → \$${pricesWithTax[i].toStringAsFixed(2)} (with tax)');
  }

  var total = pricesWithTax.reduce((sum, price) => sum + price);
  print('\n💰 Total bill: \$${total.toStringAsFixed(2)}');
}
```

**🔍 What This Code Does:**

This code demonstrates **practical applications of anonymous functions** in data processing:

1. **forEach with Anonymous Function**: `orders.forEach((order) {...})` applies an anonymous function to each item in the list, printing each order.

2. **Map Transformation**: `prices.map((price) {...})` transforms each price by applying 8% tax using an anonymous function, creating a new list.

3. **Functional Programming**: Shows how anonymous functions enable functional programming paradigms for data transformation.

4. **Reduce Operation**: `reduce((sum, price) => sum + price)` uses an arrow function to accumulate all prices into a total sum.

5. **List Processing Pipeline**: Demonstrates chaining operations (map, toList, reduce) with anonymous functions for data processing workflows.

6. **Real-World Application**: Simulates actual restaurant billing system with tax calculation and total computation.

**Output:**

```
=== RESTAURANT ORDERS ===
✅ Preparing: Pizza
✅ Preparing: Burger
✅ Preparing: Salad
✅ Preparing: Pasta
✅ Preparing: Tacos

=== PRICE CALCULATION ===
Pizza: $12.99 → $14.03 (with tax)
Burger: $8.50 → $9.18 (with tax)
Salad: $7.25 → $7.83 (with tax)
Pasta: $11.00 → $11.88 (with tax)
Tacos: $9.75 → $10.53 (with tax)

💰 Total bill: $53.45
```

---

## 🎮 Interactive Example: Game Score Processing

```dart
void main() {
  var playerScores = [
    {'name': 'Alex', 'score': 1250},
    {'name': 'Sam', 'score': 890},
    {'name': 'Jordan', 'score': 1450},
    {'name': 'Casey', 'score': 720},
  ];

  print('🎮 GAME LEADERBOARD 🎮\n');

  var getRankEmoji = (int score) {
    if (score > 1400) return '🏆';
    if (score > 1000) return '🥈';
    if (score > 800) return '🥉';
    return '🎯';
  };

  playerScores.forEach((player) {
    String emoji = getRankEmoji(player['score'] as int);
    print('$emoji ${player['name']}: ${player['score']} points');
  });

  var winner = playerScores.reduce((a, b) =>
    (a['score'] as int) > (b['score'] as int) ? a : b
  );

  print('\n🎊 Winner: ${winner['name']} with ${winner['score']} points!');
}
```

**🔍 What This Code Does:**

This code demonstrates **complex anonymous function applications** with conditional logic:

1. **Conditional Anonymous Function**: `getRankEmoji` uses conditional statements to return different emojis based on score ranges.

2. **Map Data Processing**: Works with List of Maps (representing player data) showing how anonymous functions handle complex data structures.

3. **Type Casting**: Uses `as int` to safely cast dynamic map values to integers for comparison operations.

4. **Nested Function Calls**: Combines `forEach` with custom anonymous function calls, showing function composition.

5. **Comparison Logic**: The `reduce` operation uses ternary operator in arrow function to find the highest scoring player.

6. **Dynamic Content**: Anonymous functions generate dynamic content (emojis, formatting) based on data values.

**Output:**

```
🎮 GAME LEADERBOARD 🎮

🏆 Jordan: 1450 points
🥈 Alex: 1250 points
🥉 Sam: 890 points
🎯 Casey: 720 points

🎊 Winner: Jordan with 1450 points!
```

---

## 🛠️ Practical Use Cases

### 1. Event Handlers

```dart
void main() {
  var buttons = ['Save', 'Cancel', 'Delete'];

  buttons.forEach((buttonName) {
    var handleClick = () {
      switch(buttonName) {
        case 'Save': print('💾 Data saved successfully!'); break;
        case 'Cancel': print('❌ Operation cancelled'); break;
        case 'Delete': print('🗑️ Item deleted'); break;
      }
    };

    print('Clicking $buttonName button...');
    handleClick();
  });
}
```

**🔍 What This Code Does:**

This code demonstrates **event handler simulation** using anonymous functions:

1. **Dynamic Event Handlers**: Creates different anonymous functions for each button based on the button name.

2. **Closure Behavior**: Each anonymous function captures the `buttonName` variable from its surrounding scope (closure).

3. **Switch Logic**: Uses switch statements within anonymous functions to handle different button behaviors.

4. **Event Simulation**: Simulates clicking each button and executing its corresponding handler function.

5. **Modular Design**: Each button gets its own handler function, demonstrating how anonymous functions can encapsulate specific behaviors.

### 2. Data Filtering

```dart
void main() {
  var students = [
    {'name': 'Emma', 'grade': 85},
    {'name': 'Liam', 'grade': 92},
    {'name': 'Olivia', 'grade': 78},
    {'name': 'Noah', 'grade': 96},
  ];

  var honorStudents = students.where((student) {
    return (student['grade'] as int) > 90;
  }).toList();

  print('🎓 Honor Students:');
  honorStudents.forEach((student) {
    print('⭐ ${student['name']}: ${student['grade']}%');
  });
}
```

**🔍 What This Code Does:**

This code demonstrates **data filtering** with anonymous functions:

1. **Filtering Logic**: `where()` method uses an anonymous function to test each student against a condition (grade > 90).

2. **Predicate Function**: The anonymous function acts as a predicate, returning true/false to determine if items should be included.

3. **Method Chaining**: Chains `where()` and `toList()` methods to filter and convert the result back to a list.

4. **Dynamic Filtering**: The filter condition is defined inline, making it easy to modify without creating separate named functions.

5. **Result Processing**: Uses `forEach` with another anonymous function to display the filtered results with formatting.

---

## 📊 Comparison Table

| Feature      | Named Function                      | Anonymous Function                |
| ------------ | ----------------------------------- | --------------------------------- |
| **Has Name** | ✅ `void myFunction()`              | ❌ `() { ... }`                   |
| **Reusable** | ✅ Call anywhere                    | 🔶 Only where defined             |
| **Memory**   | Stored globally                     | 🔶 Stored in variable/used inline |
| **Best For** | Repeated tasks                      | One-time or callback tasks        |
| **Example**  | `double calculateTax(double price)` | `prices.map((p) => p * 1.08)`     |

---

## 🧠 Quick Reference

### Syntax Patterns

```dart
() { print('Hello!'); }

(String name) { print('Hi $name!'); }

(int x) => x * 2

(() { print('Run now!'); })();

var myFunc = (int a, int b) => a + b;
```

### Common Uses

- **Lists**: `list.forEach((item) => print(item))`
- **Filtering**: `list.where((item) => item > 10)`
- **Mapping**: `list.map((item) => item * 2)`
- **Event handling**: Button clicks, form submissions
- **Callbacks**: Functions passed to other functions

---

## 🎉 Remember This!

Anonymous functions are like **helpful strangers** at a party 🎉

- They show up when needed
- Do their job perfectly
- Don't need formal introductions
- Disappear when done
- Make your code cleaner and more flexible!

**Pro Tip**: Use anonymous functions when you need a quick, one-time helper. Use named functions when you'll need the same logic multiple times throughout your app!
