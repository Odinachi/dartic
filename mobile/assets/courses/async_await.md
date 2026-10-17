# async/await in Dart

Imagine you ordered pizza 🍕 for dinner, but it takes 30 minutes to arrive.

Do you just sit by the door staring at it for 30 minutes? **NO WAY!**

Instead, you:

- Keep watching TV 📺
- Text your friends 📱
- Maybe tidy up a bit 🧹
- **Then** answer the door when the pizza arrives!

👉 That's exactly what `async/await` does in programming:

> It lets your app **keep working** while waiting for slow things to finish, then handles the result when it's ready!

---

## 🎯 The Problem Without async/await

```dart
void badExample() {
  print('Ordering pizza...');
  print('Pizza arrived!');
}
```

**🔍 What This Code Does:**

This code demonstrates the **problem with synchronous execution**:

1. **Immediate Execution**: Both print statements execute instantly one after another with no delay.

2. **No Real Waiting**: In reality, ordering pizza takes time, but this code doesn't represent that waiting period.

3. **Blocking Behavior**: If there was actual waiting logic here (like a loop), it would freeze the entire application.

4. **Unrealistic Simulation**: Real-world operations (network calls, file reading, user input) take time that needs to be handled properly.

5. **User Experience Issue**: In a real app, this would make the interface unresponsive during long operations.

**Problem**: The entire app stops working while waiting!

---

## ✅ The Solution: async/await

```dart
Future<String> orderPizza() async {
  print('📞 Calling pizza place...');
  await Future.delayed(Duration(seconds: 2));
  return '🍕 Pizza delivered!';
}

void main() async {
  print('🏠 I\'m hungry, ordering food...');

  String result = await orderPizza();

  print(result);
  print('😋 Time to eat!');
}
```

**🔍 What This Code Does:**

This code demonstrates **proper asynchronous programming** with async/await:

1. **Async Function Declaration**: `orderPizza()` is marked with `async`, indicating it performs asynchronous operations.

2. **Future Return Type**: `Future<String>` means this function will eventually return a String, but not immediately.

3. **Simulated Delay**: `Future.delayed(Duration(seconds: 2))` simulates a 2-second wait (like network call or file operation).

4. **Await Keyword**: `await` pauses execution at that line until the Future completes, but doesn't block the entire program.

5. **Sequential Execution**: Code after `await` runs only after the awaited operation completes.

6. **Main Function**: `main()` is also marked `async` because it uses `await` to wait for `orderPizza()`.

7. **Non-blocking**: While waiting, other parts of the program can continue running (though not visible in this simple example).

**Output:**

```
🏠 I'm hungry, ordering food...
📞 Calling pizza place...
🍕 Pizza delivered!
😋 Time to eat!
```

---

## 🔍 Understanding the Keywords

### `async`

- Put this on functions that might take time
- Like putting a "⏰ SLOW" warning sign on a function
- **Must use this** if your function has `await` inside

```dart
// ✅ Correct
Future<void> slowFunction() async {
  await Future.delayed(Duration(seconds: 1));
}

// ❌ Wrong - missing async
Future<void> brokenFunction() {
  await Future.delayed(Duration(seconds: 1)); // ERROR!
}
```

### `await`

- Means "stop here and wait for this to finish"
- Like pressing pause ⏸️ until something is ready
- **Can only be used** inside `async` functions

```dart
void main() async {
  print('Starting...');
  await Future.delayed(Duration(seconds: 1)); // Wait 1 second
  print('1 second later!');
}
```

### `Future<T>`

- A promise to give you something later
- `Future<String>` = "I'll give you text later"
- `Future<int>` = "I'll give you a number later"

---

## 🏃‍♀️ Step-by-Step Example

Let's watch someone get ready for school:

```dart
Future<void> brushTeeth() async {
  print('🦷 Brushing teeth...');
  await Future.delayed(Duration(seconds: 2));
  print('✨ Teeth are clean!');
}

Future<void> eatBreakfast() async {
  print('🥞 Making breakfast...');
  await Future.delayed(Duration(seconds: 3));
  print('😋 Breakfast eaten!');
}

Future<void> packBag() async {
  print('🎒 Packing school bag...');
  await Future.delayed(Duration(seconds: 1));
  print('📚 Bag is ready!');
}

void main() async {
  print('⏰ Getting ready for school!\n');

  await brushTeeth();
  print('');

  await eatBreakfast();
  print('');

  await packBag();
  print('');

  print('🚌 Ready for the school bus!');
}
```

**🔍 What This Code Does:**

This code demonstrates **sequential asynchronous operations** representing a morning routine:

1. **Multiple Async Functions**: Three separate async functions represent different morning tasks, each taking different amounts of time.

2. **Sequential Execution**: Tasks are performed one after another using `await`, ensuring each completes before the next begins.

3. **Different Durations**: Each task has a different delay (2s, 3s, 1s) simulating real-world task variations.

4. **Return Type `void`**: `Future<void>` indicates these functions don't return a value, just perform actions.

5. **Structured Workflow**: The main function orchestrates the entire morning routine in a logical order.

6. **Progress Feedback**: Each function prints start and completion messages, providing user feedback during long operations.

7. **Total Time**: The entire routine takes 6 seconds (2+3+1), but is handled asynchronously without blocking.

**Output:**

```
⏰ Getting ready for school!

🦷 Brushing teeth...
✨ Teeth are clean!

🥞 Making breakfast...
😋 Breakfast eaten!

🎒 Packing school bag...
📚 Bag is ready!

🚌 Ready for the school bus!
```

---

## 🕐 Different Wait Times

```dart
Future<String> fastTask() async {
  await Future.delayed(Duration(milliseconds: 500));
  return '⚡ Fast task done!';
}

Future<String> mediumTask() async {
  await Future.delayed(Duration(seconds: 2));
  return '🚶 Medium task done!';
}

Future<String> slowTask() async {
  await Future.delayed(Duration(seconds: 4));
  return '🐌 Slow task done!';
}

void main() async {
  print('Starting all tasks...\n');

  String result1 = await fastTask();
  print(result1);

  String result2 = await mediumTask();
  print(result2);

  String result3 = await slowTask();
  print(result3);

  print('\n🎉 All done!');
}
```

**🔍 What This Code Does:**

This code demonstrates **varying execution times** and their impact on program flow:

1. **Different Time Units**: Shows milliseconds (500ms) vs seconds (2s, 4s) for different operation speeds.

2. **Return Values**: Each function returns a descriptive string indicating completion, demonstrating how async functions can return data.

3. **Sequential Processing**: Tasks execute in order - fast, then medium, then slow - each waiting for the previous to complete.

4. **Cumulative Time**: Total execution time is 6.5 seconds (0.5 + 2 + 4), but handled smoothly without blocking.

5. **Progress Indication**: Users see immediate feedback when each task completes, rather than waiting for everything to finish.

6. **Real-World Simulation**: Represents scenarios where different operations have vastly different completion times (database queries vs API calls vs file uploads).

---

## 🎮 Interactive Game Example

```dart
Future<int> rollDice() async {
  print('🎲 Rolling dice...');
  await Future.delayed(Duration(seconds: 1));

  int result = DateTime.now().millisecond % 6 + 1;
  return result;
}

Future<String> playTurn(String playerName) async {
  print('\n🎯 $playerName\'s turn!');

  int roll = await rollDice();
  print('🎲 $playerName rolled: $roll');

  if (roll == 6) {
    return '$playerName wins! 🏆';
  } else if (roll >= 4) {
    return '$playerName did pretty good! 😊';
  } else {
    return '$playerName needs more practice! 😅';
  }
}

void main() async {
  print('🎮 Welcome to the Dice Game!');

  String result1 = await playTurn('Alice');
  print(result1);

  String result2 = await playTurn('Bob');
  print(result2);

  String result3 = await playTurn('Charlie');
  print(result3);

  print('\n🎉 Game Over!');
}
```

**🔍 What This Code Does:**

This code demonstrates **interactive async programming** with game simulation:

1. **Nested Async Operations**: `playTurn()` calls `rollDice()`, showing how async functions can call other async functions.

2. **Random Number Generation**: Uses `DateTime.now().millisecond % 6 + 1` to generate pseudo-random numbers 1-6.

3. **Conditional Logic**: Different outcomes based on dice roll values, demonstrating business logic within async functions.

4. **Player Simulation**: Each player gets a turn sequentially, simulating real game flow where players wait for their turn.

5. **Realistic Delays**: 1-second delay for dice rolling simulates physical dice rolling or network-based random number generation.

6. **Return Value Processing**: Each turn returns a result string that gets printed, showing data flow in async operations.

7. **Game Flow Control**: The main function orchestrates the entire game, managing turn order and final completion.

**Sample Output:**

```
🎮 Welcome to the Dice Game!

🎯 Alice's turn!
🎲 Rolling dice...
🎲 Alice rolled: 4
Alice did pretty good! 😊

🎯 Bob's turn!
🎲 Rolling dice...
🎲 Bob rolled: 6
Bob wins! 🏆

🎯 Charlie's turn!
🎲 Rolling dice...
🎲 Charlie rolled: 2
Charlie needs more practice! 😅

🎉 Game Over!
```

---

## 📱 Real App Example: Loading User Info

```dart
Future<String> loadUserName() async {
  print('👤 Loading user name...');
  await Future.delayed(Duration(seconds: 1));
  return 'Sarah Johnson';
}

Future<int> loadUserAge() async {
  print('🎂 Loading user age...');
  await Future.delayed(Duration(seconds: 1));
  return 25;
}

Future<String> loadUserCity() async {
  print('🏙️ Loading user city...');
  await Future.delayed(Duration(seconds: 1));
  return 'New York';
}

Future<void> displayUserProfile() async {
  print('📱 Opening user profile...\n');

  String name = await loadUserName();
  print('✅ Name: $name\n');

  int age = await loadUserAge();
  print('✅ Age: $age\n');

  String city = await loadUserCity();
  print('✅ City: $city\n');

  print('🎉 Profile loaded completely!');
  print('📋 Summary: $name, age $age, lives in $city');
}

void main() async {
  await displayUserProfile();
}
```

**🔍 What This Code Does:**

This code demonstrates **real-world application patterns** for loading user data:

1. **Modular Data Loading**: Separates data loading into distinct functions (name, age, city), representing different API endpoints or database queries.

2. **Progressive Loading**: Loads and displays each piece of information as it becomes available, improving perceived performance.

3. **Type Safety**: Different return types (`String`, `int`) demonstrate how async functions can return various data types.

4. **User Feedback**: Provides loading messages for each operation, keeping users informed during potentially slow network operations.

5. **Data Aggregation**: Combines loaded data into a final summary, showing how async operations can build up complex data structures.

6. **Real-world Simulation**: 1-second delays simulate actual network latency when fetching user data from servers.

7. **Error-Free Flow**: Demonstrates successful data loading scenario (error handling would be added in production).

**Output:**

```
📱 Opening user profile...

👤 Loading user name...
✅ Name: Sarah Johnson

🎂 Loading user age...
✅ Age: 25

🏙️ Loading user city...
✅ City: New York

🎉 Profile loaded completely!
📋 Summary: Sarah Johnson, age 25, lives in New York
```

---

## ⚠️ Common Mistakes

### Mistake 1: Forgetting `async`

```dart
// ❌ WRONG - This will cause an error!
void brokenFunction() {
  await Future.delayed(Duration(seconds: 1)); // ERROR!
}

// ✅ CORRECT - Add async
Future<void> fixedFunction() async {
  await Future.delayed(Duration(seconds: 1)); // Works!
}
```

**🔍 What This Code Shows:**

This demonstrates the **most common async/await error**:

1. **Syntax Rule Violation**: Using `await` without `async` violates Dart's syntax rules and causes compilation errors.

2. **Function Signature**: The correct version shows that async functions must return `Future<T>` types.

3. **Keyword Dependency**: `await` can only exist inside `async` functions - they're a paired concept.

4. **Compiler Protection**: Dart prevents this mistake at compile-time, not runtime, making it easy to catch.

### Mistake 2: Forgetting `await`

```dart
Future<String> getMessage() async {
  await Future.delayed(Duration(seconds: 1));
  return 'Hello!';
}

void main() async {
  // ❌ WRONG - This doesn't wait!
  String message = getMessage(); // This gives you a Future, not a String!

  // ✅ CORRECT - Use await
  String message = await getMessage(); // This gives you the actual String
  print(message);
}
```

**🔍 What This Code Shows:**

This demonstrates the **Future vs actual value confusion**:

1. **Type Mismatch**: Without `await`, you get a `Future<String>` instead of a `String`, causing type errors.

2. **Premature Execution**: The code continues immediately without waiting for the async operation to complete.

3. **Data Access Issue**: You can't use the data from a Future directly - you need to await it first.

4. **Common Beginner Error**: New async programmers often forget that async functions return Futures that must be awaited.

5. **Correct Pattern**: Always use `await` when you need the actual value from an async function call.

---

## 🧠 Quick Reference

### Basic Pattern

```dart
Future<ReturnType> functionName() async {
  // Do some work
  await somethingThatTakesTime();
  // Do more work
  return result;
}
```

### Using It

```dart
void main() async {
  ReturnType result = await functionName();
  print(result);
}
```

### Key Rules

1. ✅ Functions with `await` inside **must** be marked `async`
2. ✅ Use `await` when you need to **wait** for something to finish
3. ✅ `await` can **only** be used inside `async` functions
4. ✅ `async` functions **always** return a `Future`

---

## 🎉 Remember This!

`async/await` is like **ordering food delivery** 🥡:

1. **`async`** = "This restaurant takes orders that take time"
2. **`await`** = "I'll wait here until my food arrives"
3. **While waiting**, the restaurant keeps taking other orders
4. **When ready**, you get exactly what you ordered!

Your code stays **smooth** and **responsive** instead of freezing up! 🎯
