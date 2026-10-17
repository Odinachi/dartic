# Enums in Dart

Imagine you're organizing a **pizza restaurant** 🍕!

You have different pizza sizes, but you don't want people to type random words like:

- "big" 🤔
- "huge" 🤷‍♀️
- "extra-large-supreme-mega-size" 😵

Instead, you want **exactly 3 choices**:

- Small 🍕
- Medium 🍕🍕
- Large 🍕🍕🍕

👉 An **enum** is like having a **menu with fixed choices** - no substitutions allowed!

> Enums give you a **limited set of named options** that are **safe** and **clear**!

---

## 🚫 The Problem: Random Strings

```dart
void orderPizza(String size) {
  print('Ordering a $size pizza');
}

void main() {
  orderPizza('small');      // ✅ OK
  orderPizza('medium');     // ✅ OK
  orderPizza('LARGE');      // 🤔 Different case
  orderPizza('gigantic');   // ❌ Not a real size!
  orderPizza('smal');       // ❌ Typo!
}
```

**🔍 What This Code Does:**

This code demonstrates **the problems with using strings for categorical data**:

1. **No Type Safety**: The function accepts any string value, including invalid options like "gigantic" or misspelled words like "smal".

2. **Case Sensitivity Issues**: "LARGE" vs "large" are different strings, leading to potential inconsistencies in handling.

3. **Runtime Errors**: Invalid strings only cause problems at runtime, not during compilation, making bugs harder to catch early.

4. **No IDE Support**: There's no autocomplete or IntelliSense help when typing pizza sizes, increasing the chance of typos.

5. **Maintenance Nightmare**: If you need to add or change valid sizes, you must search through all code to update string literals manually.

**Problems:**

- **Typos** cause bugs 🐛
- **Different cases** cause confusion 🤷‍♀️
- **Invalid options** are allowed 😱
- **No autocomplete** help 💭

---

## ✅ The Solution: Enums!

```dart
enum PizzaSize {
  small,
  medium,
  large
}

void orderPizza(PizzaSize size) {
  print('Ordering a ${size.name} pizza 🍕');
}

void main() {
  orderPizza(PizzaSize.small);   // ✅ Perfect!
  orderPizza(PizzaSize.medium);  // ✅ Perfect!
  orderPizza(PizzaSize.large);   // ✅ Perfect!

  // orderPizza('gigantic');     // ❌ Compiler error - can't do this!
}
```

**🔍 What This Code Does:**

This code demonstrates **the power of enum-based type safety**:

1. **Compile-Time Safety**: The enum restricts function parameters to only valid pizza sizes, preventing invalid values at compile time.

2. **IDE Integration**: Modern IDEs provide autocomplete for enum values, making development faster and reducing typos.

3. **Consistent Naming**: The `.name` property provides consistent string representation without case sensitivity issues.

4. **Code Readability**: `PizzaSize.small` is more descriptive and intention-revealing than just `'small'`.

5. **Refactoring Safety**: If you rename an enum value, IDEs can automatically update all references throughout the codebase.

6. **Documentation**: The enum declaration serves as living documentation of all valid pizza sizes in one place.

**Output:**

```
Ordering a small pizza 🍕
Ordering a medium pizza 🍕
Ordering a large pizza 🍕
```

**Amazing benefits:**

- **No typos** possible! ✨
- **Autocomplete** works perfectly 🎯
- **Only valid options** allowed 🛡️
- **Clear and readable** code 📖

---

## 🎮 Gaming Example: Player Status

```dart
enum PlayerStatus {
  idle,
  running,
  jumping,
  fighting,
  dead
}

class GamePlayer {
  String name;
  PlayerStatus status;
  int health;

  GamePlayer(this.name, this.status, this.health);

  void displayStatus() {
    String emoji = getStatusEmoji();
    String description = getStatusDescription();

    print('🎮 Player: $name');
    print('$emoji Status: ${status.name} - $description');
    print('❤️ Health: $health/100');
    print('');
  }

  String getStatusEmoji() {
    switch (status) {
      case PlayerStatus.idle:
        return '😴';
      case PlayerStatus.running:
        return '🏃‍♂️';
      case PlayerStatus.jumping:
        return '🦘';
      case PlayerStatus.fighting:
        return '⚔️';
      case PlayerStatus.dead:
        return '💀';
    }
  }

  String getStatusDescription() {
    switch (status) {
      case PlayerStatus.idle:
        return 'Standing around, waiting for action';
      case PlayerStatus.running:
        return 'Moving quickly across the battlefield';
      case PlayerStatus.jumping:
        return 'Leaping over obstacles';
      case PlayerStatus.fighting:
        return 'Engaged in combat with enemies';
      case PlayerStatus.dead:
        return 'Game over - respawn needed';
    }
  }

  void changeStatus(PlayerStatus newStatus) {
    print('🔄 ${name} changed from ${status.name} to ${newStatus.name}');
    status = newStatus;
  }
}

void main() {
  print('🎮 ADVENTURE GAME STATUS TRACKER\n');

  GamePlayer player = GamePlayer('DragonSlayer', PlayerStatus.idle, 100);

  // Show initial status
  player.displayStatus();

  // Player starts running
  player.changeStatus(PlayerStatus.running);
  player.displayStatus();

  // Player encounters obstacle
  player.changeStatus(PlayerStatus.jumping);
  player.displayStatus();

  // Battle time!
  player.changeStatus(PlayerStatus.fighting);
  player.health = 25;
  player.displayStatus();

  // Oh no!
  player.changeStatus(PlayerStatus.dead);
  player.health = 0;
  player.displayStatus();
}
```

**🔍 What This Code Does:**

This code demonstrates **enum-driven state management in object-oriented programming**:

1. **State Machine Implementation**: The `PlayerStatus` enum defines all possible player states, creating a clear state machine model.

2. **Switch-Case Pattern**: Uses comprehensive switch statements to map enum values to specific behaviors (emojis, descriptions).

3. **Type-Safe State Transitions**: The `changeStatus()` method only accepts valid `PlayerStatus` values, preventing invalid state transitions.

4. **Exhaustive Handling**: Switch statements must handle all enum cases, ensuring no status is forgotten in the implementation.

5. **Behavioral Association**: Each enum value has associated behaviors (emoji, description) that are consistently applied through methods.

6. **State History**: The system tracks state changes by displaying transitions, useful for debugging and user feedback.

7. **Object Encapsulation**: The enum works seamlessly with class properties to create cohesive object behavior.

---

## 🌤️ Weather App Example

```dart
enum WeatherCondition {
  sunny,
  cloudy,
  rainy,
  snowy,
  stormy
}

class WeatherReport {
  String city;
  WeatherCondition condition;
  int temperature;

  WeatherReport(this.city, this.condition, this.temperature);

  void displayWeather() {
    String emoji = getWeatherEmoji();
    String description = getWeatherDescription();
    String clothing = getClothingAdvice();

    print('🌍 Weather in $city:');
    print('$emoji Condition: ${condition.name} - $description');
    print('🌡️ Temperature: ${temperature}°F');
    print('👕 Clothing advice: $clothing');
    print('🎯 Activity: ${getActivitySuggestion()}');
    print('');
  }

  String getWeatherEmoji() {
    switch (condition) {
      case WeatherCondition.sunny:
        return '☀️';
      case WeatherCondition.cloudy:
        return '☁️';
      case WeatherCondition.rainy:
        return '🌧️';
      case WeatherCondition.snowy:
        return '❄️';
      case WeatherCondition.stormy:
        return '⛈️';
    }
  }

  String getWeatherDescription() {
    switch (condition) {
      case WeatherCondition.sunny:
        return 'Clear skies and bright sunshine';
      case WeatherCondition.cloudy:
        return 'Overcast with gray clouds';
      case WeatherCondition.rainy:
        return 'Steady rainfall expected';
      case WeatherCondition.snowy:
        return 'Snow falling, roads may be slippery';
      case WeatherCondition.stormy:
        return 'Thunderstorms with lightning';
    }
  }

  String getClothingAdvice() {
    switch (condition) {
      case WeatherCondition.sunny:
        return 'Light clothes, sunglasses, sunscreen';
      case WeatherCondition.cloudy:
        return 'Light jacket, comfortable clothes';
      case WeatherCondition.rainy:
        return 'Raincoat, umbrella, waterproof shoes';
      case WeatherCondition.snowy:
        return 'Heavy coat, warm boots, gloves';
      case WeatherCondition.stormy:
        return 'Stay indoors if possible!';
    }
  }

  String getActivitySuggestion() {
    switch (condition) {
      case WeatherCondition.sunny:
        return 'Perfect for outdoor sports, picnics, or beach trips';
      case WeatherCondition.cloudy:
        return 'Good for hiking, walking, or outdoor activities';
      case WeatherCondition.rainy:
        return 'Great day for indoor activities, reading, or movies';
      case WeatherCondition.snowy:
        return 'Time for snowball fights, skiing, or hot cocoa';
      case WeatherCondition.stormy:
        return 'Board games, video games, or cozy indoor time';
    }
  }
}

void main() {
  print('🌤️ WEATHER FORECAST CENTER\n');

  List<WeatherReport> forecasts = [
    WeatherReport('New York', WeatherCondition.sunny, 75),
    WeatherReport('Seattle', WeatherCondition.rainy, 58),
    WeatherReport('Chicago', WeatherCondition.stormy, 62),
    WeatherReport('Denver', WeatherCondition.snowy, 28),
    WeatherReport('Los Angeles', WeatherCondition.cloudy, 68),
  ];

  for (WeatherReport report in forecasts) {
    report.displayWeather();
  }

  print('📱 Stay safe and check weather updates regularly!');
}
```

**🔍 What This Code Does:**

This code demonstrates **domain-specific enum usage with comprehensive business logic**:

1. **Domain Modeling**: The `WeatherCondition` enum accurately models real-world weather states that are mutually exclusive.

2. **Multi-Method Integration**: The enum drives multiple related methods (emoji, description, clothing advice, activities), showing comprehensive integration.

3. **Business Rule Implementation**: Each weather condition triggers specific advice and recommendations, embedding domain knowledge in the code.

4. **Consistent User Experience**: The enum ensures consistent presentation and advice across all weather reports.

5. **Scalable Architecture**: Adding new weather conditions requires updating the enum and related switch statements, providing clear extension points.

6. **Data-Driven Presentation**: The enum values drive visual representation (emojis) and textual content (descriptions), separating data from presentation logic.

---

## 🚦 Traffic Light System

```dart
enum TrafficLight {
  red,
  yellow,
  green
}

class TrafficController {
  TrafficLight currentLight;
  int timeRemaining;

  TrafficController(this.currentLight, this.timeRemaining);

  void displayStatus() {
    String emoji = getLightEmoji();
    String instruction = getDriverInstruction();
    String nextLight = getNextLight();

    print('$emoji Current Light: ${currentLight.name.toUpperCase()}');
    print('⏰ Time remaining: ${timeRemaining} seconds');
    print('🚗 Driver instruction: $instruction');
    print('🔄 Next: $nextLight');
    print('');
  }

  String getLightEmoji() {
    switch (currentLight) {
      case TrafficLight.red:
        return '🔴';
      case TrafficLight.yellow:
        return '🟡';
      case TrafficLight.green:
        return '🟢';
    }
  }

  String getDriverInstruction() {
    switch (currentLight) {
      case TrafficLight.red:
        return 'STOP! Do not proceed';
      case TrafficLight.yellow:
        return 'CAUTION! Prepare to stop';
      case TrafficLight.green:
        return 'GO! Proceed safely';
    }
  }

  String getNextLight() {
    switch (currentLight) {
      case TrafficLight.red:
        return 'Green light coming up';
      case TrafficLight.yellow:
        return 'Red light next';
      case TrafficLight.green:
        return 'Yellow light next';
    }
  }

  void changeLight() {
    TrafficLight oldLight = currentLight;

    switch (currentLight) {
      case TrafficLight.red:
        currentLight = TrafficLight.green;
        timeRemaining = 30;
        break;
      case TrafficLight.yellow:
        currentLight = TrafficLight.red;
        timeRemaining = 45;
        break;
      case TrafficLight.green:
        currentLight = TrafficLight.yellow;
        timeRemaining = 5;
        break;
    }

    print('🔄 Light changed from ${oldLight.name} to ${currentLight.name}');
  }

  void countdown() {
    if (timeRemaining > 0) {
      timeRemaining--;
      if (timeRemaining == 0) {
        print('⏰ Time\'s up! Light is changing...');
        changeLight();
      }
    }
  }
}

void main() {
  print('🚦 SMART TRAFFIC CONTROL SYSTEM\n');

  TrafficController intersection = TrafficController(TrafficLight.red, 10);

  // Simulate traffic light cycle
  for (int second = 1; second <= 15; second++) {
    print('⏱️ === SECOND $second ===');
    intersection.displayStatus();
    intersection.countdown();
    print('');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **finite state machine implementation using enums**:

1. **Cyclic State Machine**: The enum represents a traffic light's cyclic states with defined transitions (red→green→yellow→red).

2. **State Transition Logic**: The `changeLight()` method implements specific transition rules, ensuring traffic lights follow real-world patterns.

3. **Time-Based Behavior**: Each state has associated timing (30s for green, 5s for yellow, 45s for red), modeling real traffic control systems.

4. **State History Tracking**: Captures the previous state before transitions, useful for logging and debugging state changes.

5. **Deterministic Behavior**: The enum ensures predictable state transitions that follow traffic safety protocols.

6. **Real-World Modeling**: Accurately represents actual traffic light operation with appropriate timing and sequencing.

---

## 🎵 Music Player Example

```dart
enum PlaybackState {
  stopped,
  playing,
  paused,
  loading
}

enum RepeatMode {
  off,
  one,
  all
}

class MusicPlayer {
  String currentSong;
  PlaybackState state;
  RepeatMode repeatMode;
  int volume;

  MusicPlayer(this.currentSong, this.state, this.repeatMode, this.volume);

  void displayPlayerStatus() {
    String stateEmoji = getStateEmoji();
    String repeatEmoji = getRepeatEmoji();

    print('🎵 === MUSIC PLAYER ===');
    print('🎧 Current song: $currentSong');
    print('$stateEmoji Playback: ${state.name}');
    print('$repeatEmoji Repeat: ${repeatMode.name}');
    print('🔊 Volume: $volume%');
    print('');
  }

  String getStateEmoji() {
    switch (state) {
      case PlaybackState.stopped:
        return '⏹️';
      case PlaybackState.playing:
        return '▶️';
      case PlaybackState.paused:
        return '⏸️';
      case PlaybackState.loading:
        return '⏳';
    }
  }

  String getRepeatEmoji() {
    switch (repeatMode) {
      case RepeatMode.off:
        return '➡️';
      case RepeatMode.one:
        return '🔂';
      case RepeatMode.all:
        return '🔁';
    }
  }

  void play() {
    if (state == PlaybackState.stopped || state == PlaybackState.paused) {
      state = PlaybackState.playing;
      print('▶️ Now playing: $currentSong');
    } else if (state == PlaybackState.playing) {
      print('🎵 Already playing: $currentSong');
    }
  }

  void pause() {
    if (state == PlaybackState.playing) {
      state = PlaybackState.paused;
      print('⏸️ Paused: $currentSong');
    } else {
      print('⚠️ Cannot pause - not currently playing');
    }
  }

  void toggleRepeat() {
    switch (repeatMode) {
      case RepeatMode.off:
        repeatMode = RepeatMode.one;
        print('🔂 Repeat one song enabled');
        break;
      case RepeatMode.one:
        repeatMode = RepeatMode.all;
        print('🔁 Repeat all songs enabled');
        break;
      case RepeatMode.all:
        repeatMode = RepeatMode.off;
        print('➡️ Repeat disabled');
        break;
    }
  }
}

void main() {
  print('🎵 SPOTIFY-STYLE MUSIC PLAYER\n');

  MusicPlayer player = MusicPlayer(
    'Shape of You - Ed Sheeran',
    PlaybackState.stopped,
    RepeatMode.off,
    75
  );

  player.displayPlayerStatus();

  // Test player controls
  print('🎮 TESTING PLAYER CONTROLS:');
  player.play();
  player.displayPlayerStatus();

  player.pause();
  player.displayPlayerStatus();

  player.play();
  player.toggleRepeat();
  player.toggleRepeat();
  player.toggleRepeat();

  player.stop();
  player.displayPlayerStatus();
}
```

**🔍 What This Code Does:**

This code demonstrates **multiple enum usage for complex state management**:

1. **Multiple State Dimensions**: Uses two different enums (`PlaybackState` and `RepeatMode`) to manage independent aspects of the music player.

2. **State-Dependent Operations**: Methods like `play()` and `pause()` check current state before allowing operations, preventing invalid transitions.

3. **Cyclic Enum Behavior**: The `toggleRepeat()` method cycles through repeat modes in a predictable sequence.

4. **Conditional Logic**: Operations validate current state before executing, providing user-friendly feedback for invalid actions.

5. **Independent State Management**: The two enums operate independently, showing how multiple enums can coexist in a single class.

6. **User Interface Logic**: Each state change provides immediate feedback, making the system responsive and user-friendly.

---

## 📱 Phone Battery Example

```dart
enum BatteryLevel {
  critical,  // 0-10%
  low,       // 11-25%
  medium,    // 26-50%
  good,      // 51-75%
  excellent  // 76-100%
}

enum ChargingStatus {
  notCharging,
  charging,
  fastCharging,
  wirelessCharging
}

class PhoneBattery {
  int percentage;
  ChargingStatus chargingStatus;

  PhoneBattery(this.percentage, this.chargingStatus);

  BatteryLevel get batteryLevel {
    if (percentage <= 10) return BatteryLevel.critical;
    if (percentage <= 25) return BatteryLevel.low;
    if (percentage <= 50) return BatteryLevel.medium;
    if (percentage <= 75) return BatteryLevel.good;
    return BatteryLevel.excellent;
  }

  void displayBatteryStatus() {
    String levelEmoji = getBatteryEmoji();
    String chargingEmoji = getChargingEmoji();
    String warning = getBatteryWarning();

    print('📱 === PHONE BATTERY STATUS ===');
    print('$levelEmoji Battery: $percentage% (${batteryLevel.name})');
    print('$chargingEmoji Charging: ${chargingStatus.name}');
    if (warning.isNotEmpty) {
      print('⚠️ Warning: $warning');
    }
    print('🕒 Estimated time: ${getTimeEstimate()}');
    print('');
  }

  String getBatteryEmoji() {
    switch (batteryLevel) {
      case BatteryLevel.critical:
        return '🪫';
      case BatteryLevel.low:
        return '🔋';
      case BatteryLevel.medium:
        return '🔋';
      case BatteryLevel.good:
        return '🔋';
      case BatteryLevel.excellent:
        return '🔋';
    }
  }

  String getChargingEmoji() {
    switch (chargingStatus) {
      case ChargingStatus.notCharging:
        return '🔌❌';
      case ChargingStatus.charging:
        return '🔌';
      case ChargingStatus.fastCharging:
        return '⚡';
      case ChargingStatus.wirelessCharging:
        return '🔄';
    }
  }

  String getBatteryWarning() {
    switch (batteryLevel) {
      case BatteryLevel.critical:
        return 'Phone will shut down soon! Charge immediately!';
      case BatteryLevel.low:
        return 'Low battery. Consider charging soon.';
      case BatteryLevel.medium:
      case BatteryLevel.good:
      case BatteryLevel.excellent:
        return '';
    }
  }

  String getTimeEstimate() {
    if (chargingStatus == ChargingStatus.notCharging) {
      switch (batteryLevel) {
        case BatteryLevel.critical:
          return '5-10 minutes remaining';
        case BatteryLevel.low:
          return '2-3 hours remaining';
        case BatteryLevel.medium:
          return '6-8 hours remaining';
        case BatteryLevel.good:
          return '12-15 hours remaining';
        case BatteryLevel.excellent:
          return '20+ hours remaining';
      }
    } else {
      int timeToFull = (100 - percentage) ~/ getChargingSpeed();
      return '$timeToFull minutes to full charge';
    }
  }

  int getChargingSpeed() {
    switch (chargingStatus) {
      case ChargingStatus.notCharging:
        return 0;
      case ChargingStatus.charging:
        return 2; // 2% per minute
      case ChargingStatus.fastCharging:
        return 5; // 5% per minute
      case ChargingStatus.wirelessCharging:
        return 1; // 1% per minute
    }
  }

  void simulateUsage(int minutes) {
    if (chargingStatus == ChargingStatus.notCharging) {
      percentage = (percentage - minutes).clamp(0, 100);
      print('📱 Used phone for $minutes minutes');
    } else {
      int chargeGained = minutes * getChargingSpeed();
      percentage = (percentage + chargeGained).clamp(0, 100);
      print('🔌 Charged for $minutes minutes');
    }
  }
}

void main() {
  print('📱 SMART PHONE BATTERY MONITOR\n');

  // Different battery scenarios
  List<PhoneBattery> phones = [
    PhoneBattery(8, ChargingStatus.notCharging),     // Critical
    PhoneBattery(20, ChargingStatus.charging),       // Low, charging
    PhoneBattery(45, ChargingStatus.fastCharging),   // Medium, fast charging
    PhoneBattery(65, ChargingStatus.wirelessCharging), // Good, wireless
    PhoneBattery(90, ChargingStatus.notCharging),    // Excellent
  ];

  for (int i = 0; i < phones.length; i++) {
    print('📱 PHONE ${i + 1}:');
    phones[i].displayBatteryStatus();
  }

  // Simulate charging the first phone
  print('🔌 CHARGING SIMULATION:');
  PhoneBattery chargingPhone = phones[0];
  chargingPhone.chargingStatus = ChargingStatus.fastCharging;

  for (int minute = 1; minute <= 5; minute++) {
    print('⏰ Minute $minute:');
    chargingPhone.simulateUsage(1);
    chargingPhone.displayBatteryStatus();
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **computed enum properties and complex enum interactions**:

1. **Computed Enum Values**: The `batteryLevel` getter dynamically maps numeric percentages to meaningful enum categories.

2. **Multi-Enum Logic**: Combines `BatteryLevel` and `ChargingStatus` enums to provide comprehensive battery status information.

3. **Threshold-Based Categorization**: Uses percentage ranges to automatically categorize battery levels, providing semantic meaning to raw numbers.

4. **Speed Calculations**: Different charging types have different rates, embedded as business rules in enum-driven switch statements.

5. **Time Estimation**: Combines current percentage, charging status, and charging speed to calculate realistic time estimates.

6. **Context-Aware Messaging**: Battery warnings and time estimates change based on both level and charging status, providing relevant information.

7. **Real-World Modeling**: Accurately represents actual phone battery behavior with appropriate categorization and charging characteristics.

---

## 🧠 Enum Properties and Methods

### Using .name Property

```dart
enum Color {
  red,
  green,
  blue
}

void main() {
  Color favoriteColor = Color.red;

  print('My favorite color is: ${favoriteColor.name}'); // red
  print('Uppercase: ${favoriteColor.name.toUpperCase()}'); // RED
}
```

**🔍 What This Code Does:**

This code demonstrates **enum introspection capabilities**:

1. **Built-in String Conversion**: The `.name` property provides automatic string representation of enum values without manual mapping.

2. **Dynamic String Manipulation**: Shows how enum names can be processed like regular strings (uppercase, formatting, etc.).

3. **Debugging Support**: The `.name` property is invaluable for logging, debugging, and displaying enum values to users.

4. **Consistent Naming**: Provides standardized string representation that matches the enum declaration exactly.

### Using .values Property

```dart
enum DaysOfWeek {
  monday,
  tuesday,
  wednesday,
  thursday,
  friday,
  saturday,
  sunday
}

void main() {
  print('📅 All days of the week:');

  for (DaysOfWeek day in DaysOfWeek.values) {
    String emoji = day == DaysOfWeek.saturday || day == DaysOfWeek.sunday ? '🎉' : '💼';
    print('$emoji ${day.name}');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **enum iteration and collective operations**:

1. **Complete Enumeration**: The `.values` property provides access to all enum values as a List, enabling iteration over all possibilities.

2. **Dynamic Processing**: Allows processing of all enum values without hardcoding each one, making code more maintainable.

3. **Conditional Logic**: Shows how to apply different logic to different enum values during iteration (weekend vs weekday emoji).

4. **Exhaustive Operations**: Ensures that operations consider all enum values, preventing missed cases when new values are added.

### Enhanced Enums (Advanced)

```dart
enum Planet {
  mercury(3.303e+23, 2.4397e6),
  venus(4.869e+24, 6.0518e6),
  earth(5.976e+24, 6.37814e6),
  mars(6.421e+23, 3.3972e6);

  const Planet(this.mass, this.radius);

  final double mass;       // in kilograms
  final double radius;     // in meters

  double get surfaceGravity => 6.67300E-11 * mass / (radius * radius);

  double surfaceWeight(double mass) => mass * surfaceGravity;
}

void main() {
  print('🪐 PLANETARY DATA\n');

  double earthWeight = 75; // kg

  for (Planet planet in Planet.values) {
    double weight = planet.surfaceWeight(earthWeight);
    print('${planet.name}: ${weight.toStringAsFixed(1)} kg');
  }
}
```

**🔍 What This Code Does:**

This code demonstrates **advanced enum capabilities with associated data and methods**:

1. **Parameterized Enums**: Each enum value can have associated data (mass, radius) passed through constructors.

2. **Computed Properties**: The `surfaceGravity` getter performs calculations using the associated data, providing derived values.

3. **Instance Methods**: The `surfaceWeight()` method operates on the enum's data to provide functionality beyond simple categorization.

4. **Scientific Modeling**: Demonstrates how enums can model complex real-world entities with both data and behavior.

5. **Immutable Data**: Uses `final` fields to ensure enum data cannot be modified after construction.

6. **Physics Integration**: Implements actual physics formulas (gravitational force) within the enum structure.

---

## 📊 Quick Reference Guide

### Basic Enum Syntax

```dart
enum MyEnum {
  option1,
  option2,
  option3
}
```

### Using Enums

```dart
// Create enum value
MyEnum choice = MyEnum.option1;

// Get string name
String name = choice.name; // "option1"

// Compare enum values
if (choice == MyEnum.option1) {
  print('First option selected');
}

// Switch statement
switch (choice) {
  case MyEnum.option1:
    print('Handle option 1');
    break;
  case MyEnum.option2:
    print('Handle option 2');
    break;
  case MyEnum.option3:
    print('Handle option 3');
    break;
}

// Get all values
List<MyEnum> allOptions = MyEnum.values;
```

### Common Patterns

| Use Case       | Example                     | When to Use               |
| -------------- | --------------------------- | ------------------------- |
| **States**     | `playing, paused, stopped`  | Object has limited states |
| **Options**    | `small, medium, large`      | Fixed set of choices      |
| **Categories** | `food, drinks, desserts`    | Classification system     |
| **Priorities** | `low, medium, high, urgent` | Ranking or importance     |

---

## 🎯 When to Use Enums

**✅ Perfect for:**

- **Limited options** (pizza sizes, colors, directions)
- **State management** (loading, success, error)
- **Categories** (user roles, priority levels)
- **Configuration** (themes, languages, modes)

**❌ Not ideal for:**

- **Dynamic options** that change at runtime
- **Large sets** of values (hundreds of options)
- **User-generated** content
- **Numeric ranges** (use regular numbers instead)

---

## 🚀 Practice Challenges

Try creating enums for these scenarios:

1. **🎮 Game Difficulty**: Easy, Normal, Hard, Expert
2. **🌈 Theme Colors**: Light, Dark, Auto, Custom
3. **📧 Email Status**: Unread, Read, Archived, Deleted
4. **🚗 Vehicle Types**: Car, Truck, Motorcycle, Bus
5. **🎭 User Roles**: Guest, User, Admin, SuperAdmin

---

## 🎉 Remember This!

Enums are like **restaurant menus** 🍽️:

- **📋 Fixed choices** - You can only order what's on the menu
- **🔍 Clear options** - Each dish has a specific name
- **🚫 No substitutions** - Can't make up your own items
- **✅ Safe ordering** - No confusion about what you're getting

**The Magic**: Enums prevent bugs by **limiting your choices** to only valid options - like having guard rails on a mountain road! 🛡️🏔️

**Pro Tip**: When you find yourself using strings or numbers for categories, ask "Could this be an enum instead?" Often the answer is YES! 🎯✨
