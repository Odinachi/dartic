# Collection Methods in Dart

Imagine you're the manager of a **magical toy store** 🧸✨!

Every day, you need to:

- Transform boring toys into **colorful masterpieces** 🎨
- Sort toys by **age groups** 👶🧒👦
- Count your **total inventory** 📊
- Find **specific toys** customers want 🔍
- Check if you have **everything in stock** ✅

Instead of doing this by hand (which would take FOREVER!), you have **magical tools** that can process hundreds of toys instantly!

👉 **Collection methods** are like these magical tools for your lists, sets, and maps in Dart!

---

## 🛠️ The Magical Toolbox

Think of collection methods as **specialized machines** in your toy factory:

| Machine Name         | What It Does   | Real Example               |
| -------------------- | -------------- | -------------------------- |
| **🎨 Paint Machine** | `map()`        | Paint every toy blue       |
| **🔍 Filter Belt**   | `where()`      | Keep only stuffed animals  |
| **🧮 Calculator**    | `reduce()`     | Add up all toy prices      |
| **🚀 Finder Robot**  | `firstWhere()` | Find the first red car     |
| **✅ Inspector**     | `every()`      | Check if all toys are safe |
| **🔎 Detector**      | `any()`        | Is there any toy under $5? |

---

## 🎨 The Paint Machine: `map()`

**Transform every item in your collection!**

### Basic Example: Number Doubler

```dart
void main() {
  var prices = [5, 10, 15, 20];

  // Double every price (50% off sale!)
  var salePrices = prices.map((price) => price * 2);

  print('Original: $prices');
  print('Doubled: ${salePrices.toList()}');
}
```

**🔍 What This Code Does:**

This code demonstrates **basic transformation with map()**:

1. **Element-by-Element Processing**: The `map()` method applies the transformation function `(price) => price * 2` to each individual element in the list.

2. **Lazy Evaluation**: `map()` returns an `Iterable`, not a `List`. The transformation isn't actually performed until you call `toList()` or iterate through it.

3. **Non-Destructive**: The original `prices` list remains unchanged. `map()` creates a new collection with transformed values.

4. **Arrow Function**: Uses arrow syntax `=>` for concise transformation logic when the operation is a single expression.

5. **Type Preservation**: Since all elements are integers and the operation returns integers, the resulting collection maintains integer types.

**Output:**

```
Original: [5, 10, 15, 20]
Doubled: [10, 20, 30, 40]
```

### Real-World Example: Greeting Generator

```dart
void main() {
  var names = ['Alice', 'Bob', 'Charlie', 'Diana'];

  // Create personalized greetings
  var greetings = names.map((name) => '🎉 Welcome to our store, $name!');

  print('Customer Greetings:');
  greetings.forEach(print);
}
```

**🔍 What This Code Does:**

This code demonstrates **string transformation and template usage**:

1. **String Interpolation**: Uses `$name` to embed each name into a personalized greeting template.

2. **Type Transformation**: Converts from `List<String>` (names) to `Iterable<String>` (greetings), showing how `map()` can change content while maintaining type.

3. **Template Pattern**: Creates a reusable greeting template that can be applied to any list of names.

4. **Method Chaining**: Chains `map()` with `forEach(print)` to transform and immediately display results.

5. **Real-World Application**: Demonstrates a practical use case for personalizing communications to multiple recipients.

**Output:**

```
Customer Greetings:
🎉 Welcome to our store, Alice!
🎉 Welcome to our store, Bob!
🎉 Welcome to our store, Charlie!
🎉 Welcome to our store, Diana!
```

### Complex Example: Product Catalog

```dart
void main() {
  var toys = [
    {'name': 'Teddy Bear', 'price': 15},
    {'name': 'Race Car', 'price': 25},
    {'name': 'Puzzle', 'price': 12},
  ];

  // Create product descriptions with tax
  var descriptions = toys.map((toy) {
    double priceWithTax = (toy['price'] as int) * 1.08;
    return '${toy['name']}: \$${priceWithTax.toStringAsFixed(2)} (tax included)';
  });

  print('📋 Product Catalog:');
  descriptions.forEach(print);
}
```

**🔍 What This Code Does:**

This code demonstrates **complex data transformation with business logic**:

1. **Map Processing**: Works with `List<Map<String, dynamic>>` showing how `map()` handles complex data structures.

2. **Type Casting**: Uses `as int` to safely cast dynamic map values to specific types for calculations.

3. **Mathematical Operations**: Calculates tax (8% markup) within the transformation function.

4. **String Formatting**: Uses `toStringAsFixed(2)` to format currency values to exactly 2 decimal places.

5. **Multi-Line Functions**: Shows that `map()` can use full function blocks with multiple statements, not just arrow functions.

6. **Business Logic Integration**: Incorporates real-world business requirements (tax calculation) into data transformation.

**Output:**

```
📋 Product Catalog:
Teddy Bear: $16.20 (tax included)
Race Car: $27.00 (tax included)
Puzzle: $12.96 (tax included)
```

---

## 🔍 The Filter Belt: `where()`

**Keep only the items that match your criteria!**

### Basic Example: Age-Appropriate Toys

```dart
void main() {
  var ageRatings = [3, 8, 12, 5, 16, 2, 10];

  // Keep only toys safe for kids 10 and under
  var kidsToysAges = ageRatings.where((age) => age <= 10);

  print('All ages: $ageRatings');
  print('Kids safe: ${kidsToysAges.toList()}');
}
```

**🔍 What This Code Does:**

This code demonstrates **basic filtering with conditional logic**:

1. **Predicate Function**: The `where()` method uses a predicate function `(age) => age <= 10` that returns `true`/`false` for each element.

2. **Conditional Filtering**: Only elements that make the predicate return `true` are included in the result.

3. **Lazy Evaluation**: Like `map()`, `where()` returns an `Iterable` that doesn't execute until consumed.

4. **Boolean Logic**: Uses simple comparison operators (`<=`) to create filtering criteria.

5. **Data Safety**: Filters out potentially inappropriate content (toys for ages 12+, 16+) based on safety requirements.

**Output:**

```
All ages: [3, 8, 12, 5, 16, 2, 10]
Kids safe: [3, 8, 5, 2, 10]
```

### Real-World Example: Inventory Filter

```dart
void main() {
  var inventory = [
    {'name': 'Teddy Bear', 'price': 15, 'inStock': true, 'category': 'stuffed'},
    {'name': 'Race Car', 'price': 25, 'inStock': false, 'category': 'vehicle'},
    {'name': 'Doll', 'price': 20, 'inStock': true, 'category': 'stuffed'},
    {'name': 'Puzzle', 'price': 12, 'inStock': true, 'category': 'educational'},
    {'name': 'Truck', 'price': 30, 'inStock': true, 'category': 'vehicle'},
  ];

  // Filter available stuffed toys under $18
  var availableStuffedToys = inventory.where((toy) =>
    toy['inStock'] == true &&
    toy['category'] == 'stuffed' &&
    (toy['price'] as int) < 18
  );

  print('🧸 Available Stuffed Toys Under \$18:');
  availableStuffedToys.forEach((toy) {
    print('  • ${toy['name']}: \$${toy['price']}');
  });
}
```

**🔍 What This Code Does:**

This code demonstrates **complex filtering with multiple conditions**:

1. **Compound Conditions**: Uses logical AND (`&&`) to combine multiple filtering criteria that all must be true.

2. **Map Data Filtering**: Filters complex data structures (maps) by accessing multiple properties (`inStock`, `category`, `price`).

3. **Type Safety**: Uses `as int` to safely cast dynamic values for numeric comparisons.

4. **Business Logic**: Implements realistic business requirements (availability, category, price range).

5. **Multi-Criteria Search**: Shows how customers might search for products with multiple filters applied simultaneously.

**Output:**

```
🧸 Available Stuffed Toys Under $18:
  • Teddy Bear: $15
```

---

## 🧮 The Calculator: `reduce()`

**Combine all items into a single value!**

### Basic Example: Total Sales

```dart
void main() {
  var dailySales = [150, 200, 175, 300, 225];

  // Calculate total week sales
  var totalSales = dailySales.reduce((total, daily) => total + daily);

  print('📊 Daily sales: $dailySales');
  print('💰 Total week sales: \$${totalSales}');
}
```

**🔍 What This Code Does:**

This code demonstrates **aggregation using reduce()**:

1. **Accumulation Pattern**: `reduce()` takes two parameters - the accumulated value (`total`) and current element (`daily`).

2. **Sequential Processing**: Processes elements left-to-right: ((((150 + 200) + 175) + 300) + 225).

3. **Type Consistency**: Both input and output must be the same type - here all integers for mathematical operations.

4. **Single Value Result**: Unlike `map()` or `where()`, `reduce()` returns a single value, not a collection.

5. **Mathematical Aggregation**: Perfect for calculations like sums, finding maximums, or other accumulative operations.

**Output:**

```
📊 Daily sales: [150, 200, 175, 300, 225]
💰 Total week sales: $1050
```

### Advanced Example: Finding Best Seller

```dart
void main() {
  var products = [
    {'name': 'Teddy Bear', 'sold': 45},
    {'name': 'Race Car', 'sold': 67},
    {'name': 'Puzzle', 'sold': 23},
    {'name': 'Doll', 'sold': 56},
  ];

  // Find the product with highest sales
  var bestSeller = products.reduce((current, next) =>
    (current['sold'] as int) > (next['sold'] as int) ? current : next
  );

  print('🏆 Best Seller: ${bestSeller['name']} (${bestSeller['sold']} sold)');
}
```

**🔍 What This Code Does:**

This code demonstrates **comparative reduction for finding extremes**:

1. **Comparison Logic**: Uses ternary operator `? :` to compare and select the better of two elements.

2. **Map Comparison**: Compares complex data structures by accessing specific properties (`sold` values).

3. **Type Casting**: Uses `as int` to ensure proper numeric comparison of dynamic map values.

4. **Maximum Finding**: Implements a maximum-finding algorithm using `reduce()` instead of mathematical addition.

5. **Business Intelligence**: Provides analytical insights by identifying top-performing products.

**Output:**

```
🏆 Best Seller: Race Car (67 sold)
```

---

## 📦 The Smart Calculator: `fold()`

**Like reduce, but YOU choose the starting value!**

### Basic Example: Building a String

```dart
void main() {
  var departments = ['Toys', 'Games', 'Books', 'Art'];

  // Build store directory starting with header
  var directory = departments.fold('🏪 STORE DIRECTORY:\n', (result, dept) {
    return result + '  📁 $dept Department\n';
  });

  print(directory);
}
```

**🔍 What This Code Does:**

This code demonstrates **fold() with string accumulation**:

1. **Initial Value**: Unlike `reduce()`, `fold()` starts with a provided initial value (`'🏪 STORE DIRECTORY:\n'`).

2. **Type Flexibility**: Can start with any type - here a `String` initial value with a `List<String>` collection.

3. **Accumulation Pattern**: Each iteration adds to the growing result string, building output progressively.

4. **String Concatenation**: Uses `+` operator to combine strings, creating formatted text output.

5. **Template Building**: Creates structured text output like reports, directories, or formatted displays.

**Output:**

```
🏪 STORE DIRECTORY:
  📁 Toys Department
  📁 Games Department
  📁 Books Department
  📁 Art Department
```

### Advanced Example: Shopping Cart Total

```dart
void main() {
  var cartItems = [
    {'name': 'Teddy Bear', 'price': 15, 'quantity': 2},
    {'name': 'Race Car', 'price': 25, 'quantity': 1},
    {'name': 'Puzzle', 'price': 12, 'quantity': 3},
  ];

  // Calculate total cost starting from 0
  var totalCost = cartItems.fold(0.0, (total, item) {
    double itemTotal = (item['price'] as int) * (item['quantity'] as int);
    print('${item['name']}: \$${item['price']} x ${item['quantity']} = \$${itemTotal}');
    return total + itemTotal;
  });

  print('─' * 30);
  print('🛒 Cart Total: \$${totalCost}');
}
```

**🔍 What This Code Does:**

This code demonstrates **complex calculation with fold() and side effects**:

1. **Initial Zero**: Starts with `0.0` to ensure floating-point arithmetic for currency calculations.

2. **Side Effects**: The fold function prints line items while calculating, showing how fold can perform actions beyond just accumulation.

3. **Mathematical Operations**: Calculates item totals (price × quantity) within the fold function.

4. **Business Logic**: Implements real shopping cart functionality with itemized display and total calculation.

5. **Type Conversion**: Handles mixed types by converting integers to doubles for consistent arithmetic.

**Output:**

```
Teddy Bear: $15 x 2 = $30.0
Race Car: $25 x 1 = $25.0
Puzzle: $12 x 3 = $36.0
──────────────────────────────
🛒 Cart Total: $81.0
```

---

## 🔎 The Detector: `any()`

**Check if AT LEAST ONE item matches!**

```dart
void main() {
  var toyPrices = [15, 25, 8, 30, 12];
  var customerNames = ['Alice', 'Bob', 'Charlie'];

  // Check if there are any budget toys (under $10)
  bool hasBudgetToys = toyPrices.any((price) => price < 10);

  // Check if any customer is named 'Bob'
  bool hasBob = customerNames.any((name) => name == 'Bob');

  print('💰 Any toys under \$10? $hasBudgetToys');
  print('👤 Is Bob shopping today? $hasBob');

  if (hasBudgetToys) {
    print('✨ Great! We have budget-friendly options!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **existential quantification with any()**:

1. **Boolean Return**: `any()` returns `true` if at least one element matches the condition, `false` if none match.

2. **Short-Circuit Evaluation**: Stops checking as soon as it finds one matching element, making it efficient for large collections.

3. **Predicate Testing**: Uses predicate functions to test conditions (`price < 10`, `name == 'Bob'`).

4. **Multiple Use Cases**: Shows both numeric comparison and string equality testing in the same example.

5. **Conditional Logic**: Uses the boolean result to trigger additional business logic (showing budget-friendly message).

6. **Efficient Searching**: More efficient than filtering and checking if results exist when you only need to know if any matches exist.

**Output:**

```
💰 Any toys under $10? true
👤 Is Bob shopping today? true
✨ Great! We have budget-friendly options!
```

---

## ✅ The Inspector: `every()`

**Check if ALL items match!**

```dart
void main() {
  var safetyRatings = [5, 4, 5, 5, 4]; // Out of 5 stars
  var stockLevels = [10, 15, 0, 8, 12];

  // Check if all toys are safe (4+ stars)
  bool allSafe = safetyRatings.every((rating) => rating >= 4);

  // Check if all items are in stock
  bool allInStock = stockLevels.every((stock) => stock > 0);

  print('🛡️ All toys safety approved? $allSafe');
  print('📦 All items in stock? $allInStock');

  if (allSafe && !allInStock) {
    print('⚠️ All toys are safe, but some items need restocking!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **universal quantification with every()**:

1. **Universal Testing**: `every()` returns `true` only if ALL elements match the condition; `false` if any element fails.

2. **Quality Assurance**: Perfect for validation scenarios where all items must meet certain standards.

3. **Short-Circuit on False**: Stops checking as soon as it finds one element that doesn't match, making it efficient.

4. **Safety Validation**: Implements quality control by checking if all products meet safety standards (rating ≥ 4).

5. **Inventory Management**: Checks stock availability across all products to determine fulfillment capability.

6. **Combined Logic**: Uses boolean results in compound conditions (`allSafe && !allInStock`) for complex business decisions.

**Output:**

```
🛡️ All toys safety approved? true
📦 All items in stock? false
⚠️ All toys are safe, but some items need restocking!
```

---

## 🚀 The Finder Robot: `firstWhere()`

**Find the first item that matches!**

```dart
void main() {
  var products = [
    {'name': 'Teddy Bear', 'price': 15, 'color': 'brown'},
    {'name': 'Race Car', 'price': 25, 'color': 'red'},
    {'name': 'Doll', 'price': 20, 'color': 'pink'},
    {'name': 'Fire Truck', 'price': 30, 'color': 'red'},
  ];

  try {
    // Find first red toy
    var firstRedToy = products.firstWhere((toy) => toy['color'] == 'red');
    print('🔴 First red toy: ${firstRedToy['name']} (\$${firstRedToy['price']})');

    // Find first expensive toy (over $50) - this will throw an error!
    var expensiveToy = products.firstWhere((toy) => (toy['price'] as int) > 50);
    print('💎 Expensive toy: ${expensiveToy['name']}');

  } catch (e) {
    print('❌ No expensive toys found!');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **element retrieval with error handling**:

1. **First Match**: `firstWhere()` returns the first element that matches the predicate, not all matches.

2. **Exception Handling**: Throws `StateError` if no elements match, requiring try-catch blocks for safe usage.

3. **Early Termination**: Stops searching as soon as it finds the first match, making it efficient for large collections.

4. **Complex Object Search**: Searches through maps by accessing specific properties (`color`, `price`).

5. **Error Management**: Demonstrates proper exception handling when search criteria might not be found.

6. **Type Safety**: Uses type casting (`as int`) for safe numeric comparisons in dynamic data structures.

**Output:**

```
🔴 First red toy: Race Car ($25)
❌ No expensive toys found!
```

---

## 🍬 The Grabber: `take()`

**Take the first few items!**

```dart
void main() {
  var bestSellers = [
    'Teddy Bear', 'Race Car', 'Puzzle', 'Doll', 'Building Blocks',
    'Art Set', 'Board Game', 'Action Figure', 'Robot Toy', 'Music Box'
  ];

  // Show top 3 best sellers for promotion
  var top3 = bestSellers.take(3);

  print('🏆 TOP 3 BEST SELLERS:');
  var position = 1;
  top3.forEach((toy) {
    print('  ${position}. $toy');
    position++;
  });

  // Show first 5 for the homepage
  var homepage = bestSellers.take(5).toList();
  print('\n🌟 Homepage Featured: ${homepage.join(', ')}');
}
```

**🔍 What This Code Does:**

This code demonstrates **pagination and result limiting with take()**:

1. **Result Limiting**: `take(n)` returns only the first n elements, useful for pagination and featured content.

2. **Lazy Evaluation**: Returns an `Iterable` that can be further processed or converted to a list when needed.

3. **Top-N Selection**: Perfect for showing "top 3", "featured 5", or similar limited result sets.

4. **Position Tracking**: Uses a counter variable to add numbered rankings to the output.

5. **Multiple Uses**: Shows the same data can be used with different `take()` values for different purposes (top 3 vs homepage 5).

6. **List Conversion**: Demonstrates converting the result to a `List` with `toList()` for further processing like `join()`.

**Output:**

```
🏆 TOP 3 BEST SELLERS:
  1. Teddy Bear
  2. Race Car
  3. Puzzle

🌟 Homepage Featured: Teddy Bear, Race Car, Puzzle, Doll, Building Blocks
```

---

## 🚶 The Skipper: `skip()`

**Skip the first few items!**

```dart
void main() {
  var allProducts = [
    'Premium Toy A', 'Premium Toy B', 'Premium Toy C',  // Skip these expensive ones
    'Regular Toy 1', 'Regular Toy 2', 'Regular Toy 3',  // Show these affordable ones
    'Budget Toy X', 'Budget Toy Y', 'Budget Toy Z'
  ];

  // Skip first 3 premium toys, show the rest
  var affordableOptions = allProducts.skip(3);

  print('💰 AFFORDABLE TOY OPTIONS:');
  affordableOptions.forEach((toy) => print('  • $toy'));

  // Skip first 6 to show only budget toys
  var budgetOnly = allProducts.skip(6);
  print('\n🎯 BUDGET-FRIENDLY TOYS:');
  budgetOnly.forEach((toy) => print('  💵 $toy'));
}
```

**🔍 What This Code Does:**

This code demonstrates **offset-based data access with skip()**:

1. **Offset Processing**: `skip(n)` ignores the first n elements and returns the rest, useful for pagination.

2. **Category Filtering**: Demonstrates how ordered data can be segmented by skipping expensive categories to show affordable options.

3. **Multiple Skips**: Shows using different skip values on the same data to access different segments.

4. **Pagination Logic**: Essential for implementing "page 2", "page 3" functionality by skipping previous pages' content.

5. **Data Segmentation**: Allows access to different price tiers or categories when data is pre-sorted.

**Output:**

```
💰 AFFORDABLE TOY OPTIONS:
  • Regular Toy 1
  • Regular Toy 2
  • Regular Toy 3
  • Budget Toy X
  • Budget Toy Y
  • Budget Toy Z

🎯 BUDGET-FRIENDLY TOYS:
  💵 Budget Toy X
  💵 Budget Toy Y
  💵 Budget Toy Z
```

---

## 🎭 The Visitor: `forEach()`

**Do something with every item!**

```dart
void main() {
  var customers = [
    {'name': 'Alice', 'purchase': 45},
    {'name': 'Bob', 'purchase': 78},
    {'name': 'Charlie', 'purchase': 23},
    {'name': 'Diana', 'purchase': 156},
  ];

  print('📧 SENDING PERSONALIZED THANK YOU EMAILS:\n');

  customers.forEach((customer) {
    String customerName = customer['name'] as String;
    int purchaseAmount = customer['purchase'] as int;

    // Different messages based on purchase amount
    if (purchaseAmount > 100) {
      print('💎 Dear $customerName,');
      print('   Thank you for your premium purchase of \$$purchaseAmount!');
      print('   You\'ve earned VIP status and 20% off your next visit!');
    } else if (purchaseAmount > 50) {
      print('⭐ Dear $customerName,');
      print('   Thank you for your \$$purchaseAmount purchase!');
      print('   Enjoy 10% off your next visit!');
    } else {
      print('😊 Dear $customerName,');
      print('   Thank you for your \$$purchaseAmount purchase!');
      print('   Come back soon for new arrivals!');
    }
    print(''); // Empty line for separation
  });
}
```

**🔍 What This Code Does:**

This code demonstrates **side-effect operations with forEach()**:

1. **Side Effects Only**: `forEach()` returns `void` and is used purely for side effects like printing, saving, or sending data.

2. **Complex Logic**: Contains branching logic within the iteration to handle different customer tiers.

3. **Type Safety**: Uses explicit type casting (`as String`, `as int`) for safe access to dynamic map values.

4. **Conditional Processing**: Implements tiered customer service based on purchase amounts using if-else logic.

5. **Real-World Application**: Simulates actual business process of personalized customer communication.

6. **Multi-Line Output**: Shows how complex formatting and multiple print statements can be used within forEach.

**Output:**

```
📧 SENDING PERSONALIZED THANK YOU EMAILS:

😊 Dear Alice,
   Thank you for your $45 purchase!
   Come back soon for new arrivals!

⭐ Dear Bob,
   Thank you for your $78 purchase!
   Enjoy 10% off your next visit!

😊 Dear Charlie,
   Thank you for your $23 purchase!
   Come back soon for new arrivals!

💎 Dear Diana,
   Thank you for your premium purchase of $156!
   You've earned VIP status and 20% off your next visit!
```

---

## 🔗 Chaining Methods: The Power Combo!

**Combine multiple methods for super powers!**

```dart
void main() {
  var inventory = [
    {'name': 'Teddy Bear', 'price': 15, 'rating': 4.8, 'inStock': true},
    {'name': 'Race Car', 'price': 25, 'rating': 4.2, 'inStock': false},
    {'name': 'Puzzle', 'price': 12, 'rating': 4.9, 'inStock': true},
    {'name': 'Doll', 'price': 20, 'rating': 3.8, 'inStock': true},
    {'name': 'Robot', 'price': 35, 'rating': 4.7, 'inStock': true},
    {'name': 'Art Set', 'price': 18, 'rating': 4.5, 'inStock': false},
  ];

  print('🎯 FINDING TOP RECOMMENDATIONS:\n');

  // Chain multiple methods together!
  var recommendations = inventory
    .where((item) => item['inStock'] == true)           // Only in-stock items
    .where((item) => (item['rating'] as double) > 4.5)  // High rated (4.5+)
    .where((item) => (item['price'] as int) <= 20)      // Affordable (≤$20)
    .map((item) => '⭐ ${item['name']} - \$${item['price']} (${item['rating']}⭐)')
    .take(3);                                            // Top 3 only

  print('🏆 TOP AFFORDABLE RECOMMENDATIONS:');
  recommendations.forEach(print);

  // Another chain: Calculate average price of available toys
  var avgPrice = inventory
    .where((item) => item['inStock'] == true)
    .map((item) => item['price'] as int)
    .reduce((a, b) => a + b) /
    inventory.where((item) => item['inStock'] == true).length;

  print('\n💰 Average price of available toys: \$${avgPrice.toStringAsFixed(2)}');
}
```

**🔍 What This Code Does:**

This code demonstrates **method chaining for complex data processing pipelines**:

1. **Pipeline Processing**: Chains multiple methods to create a data processing pipeline that filters, transforms, and limits results.

2. **Multiple Filters**: Uses sequential `where()` calls to apply multiple filtering criteria (stock, rating, price).

3. **Filter-Transform-Limit**: Follows a common pattern: filter data → transform format → limit results.

4. **Fluent Interface**: Method chaining creates readable, fluent code that reads like English.

5. **Complex Business Logic**: Implements sophisticated product recommendation logic with multiple criteria.

6. **Parallel Processing**: Shows two separate chains operating on the same data for different purposes (recommendations vs. average calculation).

7. **Statistical Analysis**: Calculates average price using a combination of filtering, mapping, and reduction.

**Output:**

```
🎯 FINDING TOP RECOMMENDATIONS:

🏆 TOP AFFORDABLE RECOMMENDATIONS:
⭐ Teddy Bear - $15 (4.8⭐)
⭐ Puzzle - $12 (4.9⭐)

💰 Average price of available toys: $20.50
```

---

## 🧠 Quick Reference Guide

### The Essential Collection Methods

| Method         | Purpose                       | Returns      | Example Use Case          |
| -------------- | ----------------------------- | ------------ | ------------------------- |
| `map()`        | Transform each item           | New iterable | Convert prices to strings |
| `where()`      | Filter by condition           | New iterable | Find items on sale        |
| `reduce()`     | Combine into single value     | Same type    | Calculate total           |
| `fold()`       | Combine with start value      | Any type     | Build a string from list  |
| `any()`        | Check if at least one matches | bool         | Any item out of stock?    |
| `every()`      | Check if all match            | bool         | All items safe for kids?  |
| `firstWhere()` | Find first match              | Single item  | Find specific product     |
| `take(n)`      | Get first n items             | New iterable | Show top 5 results        |
| `skip(n)`      | Skip first n items            | New iterable | Paginate results          |
| `forEach()`    | Do action on each             | void         | Send emails to customers  |

---

## 🚀 Practice Challenges

Try these real-world scenarios:

1. **Restaurant Menu**: Filter dishes by dietary restrictions, calculate total calories
2. **Student Grades**: Find honor students, calculate class average, check if anyone failed
3. **Music Playlist**: Find songs by artist, calculate total duration, create top 10 list
4. **Weather Data**: Find hottest day, check if any day rained, calculate average temperature

---

## 🎉 Remember This!

Collection methods are like having a **team of specialized workers** 👥:

- **🎨 map()** = The Artist (transforms everything)
- **🔍 where()** = The Security Guard (only lets certain items through)
- **🧮 reduce()** = The Accountant (adds everything up)
- **🔎 any()** = The Detective (finds if something exists)
- **✅ every()** = The Quality Inspector (checks everything meets standards)

With these tools, you can process thousands of items in just a few lines of code! Your toy store (or any app) will run like magic! ✨🏪
