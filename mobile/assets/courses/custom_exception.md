# Custom Exceptions in Dart

Imagine you're the **principal of a magical school** 🏫✨!

Your school has some **basic rules** that everyone knows:

- 📚 "No running in the hallways"
- 🍎 "No food fights in the cafeteria"
- 📱 "No phones during class"

But your school is **special**! You also have **unique magical rules**:

- 🪄 "No turning classmates into frogs!"
- 🔮 "Crystal balls must be returned to the library!"
- 🧙‍♀️ "Flying is only allowed in Broomstick Class!"

When students break regular rules, you give them **regular detention**. But when they break your **special magical rules**, you need **special magical consequences**!

👉 **Custom exceptions** are like creating your own **special rule violations** with **custom consequences**!

---

## 🚨 The Problem: Generic Error Messages

```dart
void checkMagicalRules(bool turningStudentsIntoFrogs) {
  if (turningStudentsIntoFrogs) {
    throw Exception('Student violated a rule!');
  }
  print('✅ All students are following the rules!');
}

void main() {
  try {
    checkMagicalRules(true);
  } catch (e) {
    print('❌ $e');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **the limitations of generic exception handling**:

1. **Vague Error Information**: The generic `Exception` provides no specific details about what rule was violated, who violated it, or what should happen next.

2. **Limited Context**: The error message "Student violated a rule!" doesn't give enough information for proper handling or user feedback.

3. **No Actionable Information**: The exception doesn't provide any guidance on how to resolve the issue or what steps should be taken.

4. **Poor User Experience**: Generic exceptions force users to guess what went wrong and how to fix it.

5. **Debugging Difficulty**: When multiple rules exist, generic exceptions make it hard to identify which specific rule was broken.

**Output:**

```
❌ Exception: Student violated a rule!
```

**Problem**: This is too vague! What rule? Which student? What should happen next?

---

## ✨ The Solution: Custom Magical Exceptions

Let's create **specific exceptions** for our magical school:

### 🐸 Frog Transformation Exception

```dart
class FrogTransformationException implements Exception {
  final String studentName;
  final String transformedBy;
  final int duration;

  FrogTransformationException(this.studentName, this.transformedBy, this.duration);

  @override
  String toString() {
    return '🐸 MAGICAL VIOLATION: $transformedBy turned $studentName into a frog for $duration minutes!';
  }

  String getReversalSpell() {
    return '✨ Reversal spell: "Ribbitus Reversus Immediatus!"';
  }

  int getDetentionHours() {
    return duration ~/ 10;
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **structured custom exception creation**:

1. **Exception Interface Implementation**: Implements `Exception` interface, making it a proper Dart exception type.

2. **Rich Data Storage**: Stores specific contextual information (student names, transformation duration) that generic exceptions can't provide.

3. **Custom toString Method**: Overrides the default string representation to provide detailed, formatted error messages.

4. **Domain-Specific Methods**: Includes methods like `getReversalSpell()` and `getDetentionHours()` that provide context-specific functionality.

5. **Business Logic Integration**: Calculates detention time based on transformation duration, embedding business rules into the exception.

6. **Immutable Properties**: Uses `final` fields to ensure exception data cannot be modified after creation.

### 📚 Library Crystal Ball Exception

```dart
class CrystalBallException implements Exception {
  final String studentName;
  final String crystalBallType;
  final bool isReturned;

  CrystalBallException(this.studentName, this.crystalBallType, {this.isReturned = false});

  @override
  String toString() {
    if (isReturned) {
      return '✅ $studentName returned the $crystalBallType crystal ball safely!';
    } else {
      return '🔮 LIBRARY VIOLATION: $studentName has not returned the $crystalBallType crystal ball!';
    }
  }

  double getLateFee() {
    return isReturned ? 0.0 : 5.50;
  }

  String getLibrarianMessage() {
    return isReturned
      ? '📚 Librarian: "Thank you for returning it safely!"'
      : '📚 Librarian: "Please return it immediately to avoid extra fees!"';
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **conditional exception behavior**:

1. **Optional Parameters**: Uses named parameter `{this.isReturned = false}` to provide default behavior while allowing customization.

2. **State-Dependent Messages**: The `toString()` method returns different messages based on the `isReturned` status, showing how exceptions can handle multiple scenarios.

3. **Conditional Logic**: Methods like `getLateFee()` return different values based on exception state, integrating business rules.

4. **Positive and Negative Cases**: Handles both violation scenarios (not returned) and success scenarios (returned), making the exception versatile.

5. **User-Friendly Messaging**: Provides contextual messages that guide user behavior based on the current situation.

### 🧹 Unauthorized Flying Exception

```dart
class UnauthorizedFlyingException implements Exception {
  final String studentName;
  final String location;
  final int altitude;
  final bool hasPermit;

  UnauthorizedFlyingException(this.studentName, this.location, this.altitude, {this.hasPermit = false});

  @override
  String toString() {
    return '🧹 FLYING VIOLATION: $studentName caught flying at ${altitude}ft in $location without proper permit!';
  }

  String getSafetyWarning() {
    if (altitude > 100) {
      return '⚠️ DANGER: Flying above 100ft without certification is extremely dangerous!';
    } else if (altitude > 50) {
      return '⚠️ WARNING: Medium altitude flying requires supervision!';
    } else {
      return 'ℹ️ Low altitude flight - still requires permit for safety!';
    }
  }

  int getSuspensionDays() {
    if (altitude > 100) return 5;
    if (altitude > 50) return 3;
    return 1;
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **severity-based exception handling**:

1. **Risk Assessment Logic**: The `getSafetyWarning()` method provides different warnings based on altitude, showing how exceptions can assess severity.

2. **Graduated Consequences**: `getSuspensionDays()` returns different penalties based on violation severity, implementing proportional response.

3. **Multiple Data Points**: Captures location, altitude, and permit status to provide comprehensive context for the violation.

4. **Safety-First Design**: Prioritizes safety messaging based on risk level, demonstrating domain-appropriate exception design.

5. **Threshold-Based Logic**: Uses altitude thresholds to categorize violations, showing how numeric data can drive exception behavior.

---

## 🏫 Complete School System

```dart
class MagicalSchoolSystem {
  List<String> currentStudents = ['Alice', 'Bob', 'Charlie', 'Diana'];
  Map<String, int> studentPoints = {
    'Alice': 50,
    'Bob': 45,
    'Charlie': 55,
    'Diana': 40
  };

  void checkFrogTransformation(String caster, String victim, int minutes) {
    print('🔍 Checking for unauthorized frog transformations...');

    if (caster != victim && minutes > 0) {
      var exception = FrogTransformationException(victim, caster, minutes);

      print('🚨 MAGICAL RULE VIOLATION DETECTED!');
      print(exception.toString());
      print(exception.getReversalSpell());

      int detentionHours = exception.getDetentionHours();
      print('⏰ Detention assigned: $detentionHours hours');

      if (studentPoints.containsKey(caster)) {
        studentPoints[caster] = (studentPoints[caster]! - 10).clamp(0, 100);
        print('📉 ${caster} loses 10 house points! New total: ${studentPoints[caster]}');
      }

      throw exception;
    }

    print('✅ No unauthorized transformations detected');
  }

  void checkCrystalBallReturn(String student, String ballType, bool returned) {
    print('🔮 Checking crystal ball returns...');

    var exception = CrystalBallException(student, ballType, isReturned: returned);

    if (!returned) {
      print('🚨 LIBRARY VIOLATION!');
      print(exception.toString());
      print('💰 Late fee: \$${exception.getLateFee()}');
      print(exception.getLibrarianMessage());
      throw exception;
    } else {
      print(exception.toString());
      print(exception.getLibrarianMessage());
    }
  }

  void checkUnauthorizedFlying(String student, String location, int altitude, bool hasPermit) {
    print('🧹 Monitoring airspace for unauthorized flying...');

    if (!hasPermit) {
      var exception = UnauthorizedFlyingException(student, location, altitude, hasPermit: hasPermit);

      print('🚨 FLYING VIOLATION!');
      print(exception.toString());
      print(exception.getSafetyWarning());

      int suspensionDays = exception.getSuspensionDays();
      print('⏰ Suspension: $suspensionDays days');

      if (studentPoints.containsKey(student)) {
        int pointsLost = altitude > 50 ? 20 : 10;
        studentPoints[student] = (studentPoints[student]! - pointsLost).clamp(0, 100);
        print('📉 $student loses $pointsLost house points! New total: ${studentPoints[student]}');
      }

      throw exception;
    }

    print('✅ All flying activities are properly authorized');
  }

  void printHousePoints() {
    print('\n🏆 CURRENT HOUSE POINTS:');
    studentPoints.forEach((student, points) {
      String emoji = points >= 50 ? '🌟' : points >= 40 ? '⭐' : '📚';
      print('  $emoji $student: $points points');
    });
    print('');
  }
}

void main() {
  var school = MagicalSchoolSystem();

  print('🏫 WELCOME TO HOGWARTS PROGRAMMING SCHOOL!');
  print('═' * 50);

  school.printHousePoints();

  print('📖 SCENARIO 1: Unauthorized Transformation');
  print('─' * 30);
  try {
    school.checkFrogTransformation('Bob', 'Alice', 30);
  } catch (e) {
    if (e is FrogTransformationException) {
      print('🎭 Resolution: Alice was quickly changed back!');
      print('📝 Incident logged in student record');
    }
  }

  print('\n📖 SCENARIO 2: Crystal Ball Check');
  print('─' * 30);
  try {
    school.checkCrystalBallReturn('Charlie', 'Future-Seeing', false);
  } catch (e) {
    if (e is CrystalBallException) {
      print('📞 Parents have been notified about the late fee');
    }
  }

  print('\n📖 SCENARIO 3: Dangerous Flying');
  print('─' * 30);
  try {
    school.checkUnauthorizedFlying('Diana', 'Great Hall', 120, false);
  } catch (e) {
    if (e is UnauthorizedFlyingException) {
      print('🚑 School nurse alerted for safety check');
      print('✉️ Flying instructor will provide remedial lessons');
    }
  }

  print('\n📖 SCENARIO 4: Good Student Behavior');
  print('─' * 30);
  try {
    school.checkCrystalBallReturn('Alice', 'Wisdom', true);
    school.checkUnauthorizedFlying('Bob', 'Quidditch Pitch', 30, true);
    print('✅ No violations - excellent behavior!');
  } catch (e) {
    print('❌ Unexpected issue: $e');
  }

  school.printHousePoints();
  print('📊 End of day report complete!');
}
```

**🔍 What This Code Does:**

This code demonstrates **comprehensive exception integration in a complete system**:

1. **System State Management**: The `MagicalSchoolSystem` class maintains state (student lists, points) that gets modified when exceptions occur.

2. **Exception-Driven Actions**: When exceptions are thrown, the system performs related actions like deducting points and assigning detention.

3. **Type-Specific Handling**: Uses `if (e is FrogTransformationException)` to handle different exception types with appropriate responses.

4. **Business Logic Integration**: Exceptions trigger real business consequences (point deduction, detention assignment) rather than just logging errors.

5. **Multiple Scenario Testing**: Demonstrates different violation scenarios and one success scenario to show comprehensive exception handling.

6. **State Persistence**: Changes made during exception handling (like point deduction) persist and affect subsequent operations.

---

## 🎮 Gaming Application: Custom Game Exceptions

```dart
class InsufficientCoinsException implements Exception {
  final int required;
  final int available;
  final String item;

  InsufficientCoinsException(this.required, this.available, this.item);

  @override
  String toString() {
    int shortage = required - available;
    return '💰 Not enough coins! Need $required for $item, but only have $available. Short by $shortage coins.';
  }

  List<String> getEarningTips() {
    return [
      '🎯 Complete daily quests for bonus coins',
      '🏆 Win battles against other players',
      '💎 Trade items you don\'t need',
      '🎰 Try your luck at the coin slots'
    ];
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **user-helpful exception design**:

1. **Detailed Financial Information**: Calculates and displays the exact shortage amount, helping users understand exactly what they need.

2. **Actionable Solutions**: The `getEarningTips()` method provides concrete ways to resolve the exception condition.

3. **Game-Specific Context**: References game mechanics (daily quests, battles, trading) that are relevant to the application domain.

4. **User Experience Focus**: Rather than just reporting failure, guides users toward success with practical suggestions.

5. **Mathematical Context**: Performs calculations (shortage = required - available) to provide precise information.

```dart
class GameSystem {
  void purchaseItem(String item, int cost, int playerCoins, int playerLevel, int requiredLevel, int inventorySlots) {
    print('🛒 Attempting to purchase: $item');

    if (playerLevel < requiredLevel) {
      var levelException = LevelTooLowException(playerLevel, requiredLevel, item);
      print('❌ ${levelException.toString()}');
      print('⚡ XP needed: ${levelException.getXPNeeded()}');
      throw levelException;
    }

    if (playerCoins < cost) {
      var coinException = InsufficientCoinsException(cost, playerCoins, item);
      print('❌ ${coinException.toString()}');
      print('💡 Ways to earn more coins:');
      coinException.getEarningTips().forEach((tip) => print('  $tip'));
      throw coinException;
    }

    if (inventorySlots >= 20) {
      var inventoryException = InventoryFullException(item, 20);
      print('❌ ${inventoryException.toString()}');
      print('🧹 Inventory management tips:');
      inventoryException.getManagementTips().forEach((tip) => print('  $tip'));
      throw inventoryException;
    }

    print('✅ Purchase successful! Enjoy your $item! 🎉');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **layered validation with multiple custom exceptions**:

1. **Sequential Validation**: Checks multiple conditions in order (level, coins, inventory) and throws appropriate exceptions for each failure.

2. **Exception-Specific Responses**: Each exception type triggers different helper information and recovery suggestions.

3. **Complete Transaction Logic**: Models a real game purchase system with multiple failure modes and one success path.

4. **Rich Error Feedback**: Provides not just error messages but also actionable guidance for each type of failure.

5. **Business Rules Enforcement**: Each exception represents a specific business rule (level requirements, payment, storage limits).

---

## 🏥 Medical App: Health Monitoring

```dart
class CriticalVitalsException implements Exception {
  final String vitalType;
  final double currentValue;
  final double normalMin;
  final double normalMax;
  final String units;

  CriticalVitalsException(this.vitalType, this.currentValue, this.normalMin, this.normalMax, this.units);

  @override
  String toString() {
    String status = currentValue < normalMin ? 'TOO LOW' : 'TOO HIGH';
    return '🚨 CRITICAL: $vitalType is $status! Current: $currentValue$units (Normal: $normalMin-$normalMax$units)';
  }

  String getUrgencyLevel() {
    double variance = currentValue < normalMin ?
      (normalMin - currentValue) / normalMin :
      (currentValue - normalMax) / normalMax;

    if (variance > 0.5) return '🔴 EMERGENCY';
    if (variance > 0.3) return '🟡 URGENT';
    return '🟠 MONITOR CLOSELY';
  }

  List<String> getRecommendations() {
    if (vitalType == 'Heart Rate') {
      return currentValue < normalMin ?
        ['💊 Check for underlying conditions', '🏃 Light exercise may help'] :
        ['😌 Rest immediately', '💧 Drink water', '🧘 Practice breathing exercises'];
    } else if (vitalType == 'Blood Pressure') {
      return currentValue < normalMin ?
        ['🧂 Increase salt intake slightly', '💧 Stay hydrated'] :
        ['🧂 Reduce sodium', '🥗 Eat more fruits and vegetables', '🚶 Light walking'];
    }
    return ['👨‍⚕️ Consult healthcare provider immediately'];
  }
}

void monitorVitals(String patientName, double heartRate, double systolic, double diastolic) {
  print('🏥 MONITORING VITALS FOR $patientName');

  try {
    if (heartRate < 60 || heartRate > 100) {
      var hrException = CriticalVitalsException('Heart Rate', heartRate, 60, 100, 'bpm');
      print(hrException.toString());
      print('⚠️ Urgency: ${hrException.getUrgencyLevel()}');
      print('📋 Recommendations:');
      hrException.getRecommendations().forEach((rec) => print('  $rec'));
      throw hrException;
    }

    if (systolic < 90 || systolic > 140) {
      var bpException = CriticalVitalsException('Blood Pressure', systolic, 90, 140, 'mmHg');
      print(bpException.toString());
      print('⚠️ Urgency: ${bpException.getUrgencyLevel()}');
      print('📋 Recommendations:');
      bpException.getRecommendations().forEach((rec) => print('  $rec'));
      throw bpException;
    }

    print('✅ All vitals are within normal range!');

  } catch (e) {
    print('\n📞 Alert sent to medical team');
    print('📱 Family members notified');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **medical domain-specific exception handling**:

1. **Clinical Precision**: Stores exact vital sign values, normal ranges, and units for medical accuracy.

2. **Severity Assessment**: The `getUrgencyLevel()` method calculates severity based on how far values deviate from normal ranges.

3. **Medical Context**: Provides condition-specific recommendations based on the type of vital sign and whether it's too high or low.

4. **Professional Response**: Automatically triggers appropriate medical responses (team alerts, family notification) when critical conditions are detected.

5. **Risk Stratification**: Uses percentage variance to categorize urgency levels, following medical triage principles.

6. **Comprehensive Monitoring**: Checks multiple vital signs and can handle different types of medical emergencies.

---

## 🧠 Key Concepts Summary

### Why Create Custom Exceptions?

| Benefit             | Description                     | Example                                             |
| ------------------- | ------------------------------- | --------------------------------------------------- |
| **🎯 Specific**     | Exact problem identification    | `InsufficientCoinsException` vs generic `Exception` |
| **📊 Informative**  | Rich context and data           | Include current/required values, suggestions        |
| **🛠️ Actionable**   | Provide solutions               | Give tips for earning coins, managing inventory     |
| **🎭 Professional** | Clean, organized error handling | Different exception types for different problems    |

### Custom Exception Structure

```dart
class YourCustomException implements Exception {
  // 📋 Properties (data about the problem)
  final String problemDetails;
  final int currentValue;
  final int expectedValue;

  // 🏗️ Constructor (how to create the exception)
  YourCustomException(this.problemDetails, this.currentValue, this.expectedValue);

  // 📝 toString (the main error message)
  @override
  String toString() {
    return 'CustomError: $problemDetails (Expected: $expectedValue, Got: $currentValue)';
  }

  // 🛠️ Helper methods (additional functionality)
  String getSolution() {
    return 'Try doing X to fix this problem';
  }
}
```

---

## 🎯 When to Create Custom Exceptions

**✅ Great for:**

- **Business rules**: Banking limits, game restrictions, medical thresholds
- **User-friendly errors**: Clear messages with helpful suggestions
- **Domain-specific problems**: Shopping cart issues, account problems
- **Rich error context**: Include relevant data and next steps

**❌ Don't need them for:**

- **Simple validation**: Use built-in exceptions
- **One-time errors**: Generic Exception is fine
- **System errors**: File not found, network issues

---

## 🚀 Practice Challenges

Create custom exceptions for these scenarios:

1. **🏪 E-commerce**: `OutOfStockException`, `InvalidCouponException`, `ShippingException`
2. **🎓 School System**: `GradeException`, `AttendanceException`, `CourseException`
3. **🏦 Banking**: `InsufficientFundsException`, `AccountFrozenException`, `DailyLimitException`
4. **🎵 Music App**: `PlaylistFullException`, `SongUnavailableException`, `SubscriptionException`

---

## 🎉 Remember This!

Custom exceptions are like having **specialized emergency responders** 🚨:

- **🔥 Fire Department**: `FireException` with water trucks and ladders
- **👮 Police**: `CrimeException` with investigation procedures
- **🚑 Ambulance**: `MedicalException` with first aid protocols
- **⚡ Electrician**: `PowerException` with safety equipment

Each one knows **exactly what went wrong** and **exactly how to help**!

Instead of just saying "Something bad happened," they say "Here's the specific problem, here's why it happened, and here's how to fix it!" 🛠️✨

**Pro Tip**: Great custom exceptions don't just report problems - they **guide users toward solutions**! 🌟
