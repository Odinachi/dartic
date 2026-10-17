# Inheritance in Dart

Imagine your **dad is a superhero** 🦸‍♂️!

He can **fly**, he's super **strong**, and he **saves people**.

Now imagine **you're his child** 👧 — and you also get some of his powers!

But here's the cool part: **you can also learn new powers** that your dad doesn't have, and you can even do some of his powers **in your own special way**!

👉 That's exactly what **Inheritance** is in Dart:

> It's when **one class (the child)** gets all the abilities from **another class (the parent)**, can add new abilities, and can customize existing ones!

---

## 🦸‍♂️ Parent Class: The Original Superhero

Let's create our superhero dad:

```dart
class SuperDad {
  String name;
  int age;
  String superpower;

  SuperDad(this.name, this.age, this.superpower);

  void fly() {
    print('$name is flying high in the sky! ☁️✈️');
  }

  void savePeople() {
    print('$name is saving people from danger! 🛡️🦸‍♂️');
  }

  void displayInfo() {
    print('👤 Name: $name');
    print('🎂 Age: $age');
    print('⚡ Superpower: $superpower');
  }

  void rest() {
    print('$name is taking a well-deserved break 😴');
  }
}

void main() {
  SuperDad dad = SuperDad('Captain Amazing', 45, 'Super Strength');

  dad.displayInfo();
  dad.fly();
  dad.savePeople();
  dad.rest();
}
```

**Output:**

```
👤 Name: Captain Amazing
🎂 Age: 45
⚡ Superpower: Super Strength
Captain Amazing is flying high in the sky! ☁️✈️
Captain Amazing is saving people from danger! 🛡️🦸‍♂️
Captain Amazing is taking a well-deserved break 😴
```

**🔍 What This Code Does:**

This code demonstrates **the foundation of inheritance with a base parent class**:

1. **Base Class Definition**: `SuperDad` serves as the parent class that defines common superhero characteristics and behaviors.

2. **Property Encapsulation**: Contains fundamental properties (`name`, `age`, `superpower`) that all superheroes would need.

3. **Behavioral Methods**: Implements core superhero abilities (`fly()`, `savePeople()`) that can be inherited by child classes.

4. **Information Display**: Provides a standard way to display superhero information that child classes can use or override.

5. **Constructor Pattern**: Uses a straightforward constructor that accepts all necessary parameters for superhero initialization.

6. **Method Consistency**: All methods follow consistent naming and output patterns that child classes can build upon.

---

## 👧 Child Class: The Next Generation

Now let's create a superhero kid who **inherits** from SuperDad:

```dart
class SuperKid extends SuperDad {
  String school;
  String favoriteToy;

  SuperKid(String name, int age, String superpower, this.school, this.favoriteToy)
    : super(name, age, superpower);

  // New ability that only SuperKid has
  void playWithToys() {
    print('$name is playing with $favoriteToy! 🧸🎮');
  }

  void goToSchool() {
    print('$name is going to $school for superhero training! 🏫📚');
  }

  // Override parent's rest method with kid-specific behavior
  @override
  void rest() {
    print('$name is taking a nap with favorite teddy bear! 🧸😴');
  }
}

void main() {
  SuperKid kid = SuperKid('Wonder Kid', 8, 'Lightning Speed', 'Hero Elementary', 'Robot Toy');

  print('🌟 SUPERHERO KID PROFILE 🌟\n');

  kid.displayInfo(); // Inherited from SuperDad
  print('🏫 School: ${kid.school}');
  print('🧸 Favorite Toy: ${kid.favoriteToy}\n');

  print('=== INHERITED ABILITIES ===');
  kid.fly();        // From SuperDad
  kid.savePeople(); // From SuperDad

  print('\n=== NEW KID ABILITIES ===');
  kid.playWithToys(); // SuperKid's own method
  kid.goToSchool();   // SuperKid's own method

  print('\n=== CUSTOMIZED ABILITY ===');
  kid.rest(); // SuperKid's version (overridden)
}
```

**Output:**

```
🌟 SUPERHERO KID PROFILE 🌟

👤 Name: Wonder Kid
🎂 Age: 8
⚡ Superpower: Lightning Speed
🏫 School: Hero Elementary
🧸 Favorite Toy: Robot Toy

=== INHERITED ABILITIES ===
Wonder Kid is flying high in the sky! ☁️✈️
Wonder Kid is saving people from danger! 🛡️🦸‍♂️

=== NEW KID ABILITIES ===
Wonder Kid is playing with Robot Toy! 🧸🎮
Wonder Kid is going to Hero Elementary for superhero training! 🏫📚

=== CUSTOMIZED ABILITY ===
Wonder Kid is taking a nap with favorite teddy bear! 🧸😴
```

**Amazing!** SuperKid can do everything SuperDad can do, plus has their own special abilities!

**🔍 What This Code Does:**

This code demonstrates **inheritance with extension and method overriding**:

1. **Class Extension**: `extends SuperDad` establishes inheritance, giving `SuperKid` access to all parent methods and properties.

2. **Constructor Delegation**: Uses `super(name, age, superpower)` to call the parent constructor, ensuring proper initialization of inherited properties.

3. **Property Extension**: Adds new properties (`school`, `favoriteToy`) specific to the child class, extending the parent's data model.

4. **Method Addition**: Implements new methods (`playWithToys()`, `goToSchool()`) that are unique to the child class.

5. **Method Override**: Uses `@override` annotation to replace the parent's `rest()` method with child-specific behavior.

6. **Behavioral Specialization**: Child class maintains the parent's interface while providing specialized implementations appropriate for a kid superhero.

---

## 🐕 Animal Kingdom Example

Let's create a more complex inheritance example with animals:

```dart
class Animal {
  String name;
  String species;
  int age;
  String habitat;

  Animal(this.name, this.species, this.age, this.habitat);

  void eat() {
    print('$name the $species is eating 🍽️');
  }

  void sleep() {
    print('$name is sleeping in the $habitat 😴');
  }

  void makeSound() {
    print('$name makes a sound! 🔊');
  }

  void displayInfo() {
    print('📋 Animal Info:');
    print('  👤 Name: $name');
    print('  🐾 Species: $species');
    print('  🎂 Age: $age years');
    print('  🏠 Habitat: $habitat');
  }
}

class Dog extends Animal {
  String breed;
  String ownerName;

  Dog(String name, this.breed, int age, this.ownerName)
    : super(name, 'Dog', age, 'House');

  @override
  void makeSound() {
    print('$name says: Woof! Woof! 🐕');
  }

  void wagTail() {
    print('$name is wagging tail happily! 🐕💕');
  }

  void fetch() {
    print('$name is playing fetch with $ownerName! 🎾');
  }

  void guard() {
    print('$name is guarding the house! 🏠🛡️');
  }
}

class Cat extends Animal {
  String furColor;
  bool isIndoor;

  Cat(String name, this.furColor, int age, this.isIndoor)
    : super(name, 'Cat', age, isIndoor ? 'House' : 'Outdoors');

  @override
  void makeSound() {
    print('$name says: Meow! Purr! 🐱');
  }

  void climb() {
    print('$name is climbing up high! 🐱🌳');
  }

  void hunt() {
    if (!isIndoor) {
      print('$name is hunting for mice! 🐱🐭');
    } else {
      print('$name is hunting for toy mice! 🐱🧸');
    }
  }

  void purr() {
    print('$name is purring contentedly! 🐱💤');
  }
}

class Bird extends Animal {
  double wingspan;
  bool canFly;

  Bird(String name, String species, int age, this.wingspan, this.canFly)
    : super(name, species, age, 'Sky');

  @override
  void makeSound() {
    print('$name says: Tweet! Chirp! 🐦');
  }

  void fly() {
    if (canFly) {
      print('$name is soaring through the sky with ${wingspan}ft wingspan! 🐦✈️');
    } else {
      print('$name cannot fly but is running fast! 🐦💨');
    }
  }

  void buildNest() {
    print('$name is building a cozy nest! 🐦🏠');
  }
}

void main() {
  print('🐾 WELCOME TO THE ANIMAL KINGDOM! 🐾\n');

  // Create different animals
  Dog buddy = Dog('Buddy', 'Golden Retriever', 3, 'Sarah');
  Cat whiskers = Cat('Whiskers', 'Orange', 2, true);
  Bird eagle = Bird('Ace', 'Eagle', 5, 6.5, true);

  List<Animal> animals = [buddy, whiskers, eagle];

  for (Animal animal in animals) {
    print('=' * 50);
    animal.displayInfo();

    // All animals can do these basic things
    animal.eat();
    animal.sleep();
    animal.makeSound(); // Each has their own version!

    // Check specific animal types and call their unique methods
    if (animal is Dog) {
      print('\n🐕 DOG SPECIAL ABILITIES:');
      animal.wagTail();
      animal.fetch();
      animal.guard();
    } else if (animal is Cat) {
      print('\n🐱 CAT SPECIAL ABILITIES:');
      animal.climb();
      animal.hunt();
      animal.purr();
    } else if (animal is Bird) {
      print('\n🐦 BIRD SPECIAL ABILITIES:');
      animal.fly();
      animal.buildNest();
    }

    print('');
  }
}
```

**Output:**

```
🐾 WELCOME TO THE ANIMAL KINGDOM! 🐾

==================================================
📋 Animal Info:
  👤 Name: Buddy
  🐾 Species: Dog
  🎂 Age: 3 years
  🏠 Habitat: House
Buddy the Dog is eating 🍽️
Buddy is sleeping in the House 😴
Buddy says: Woof! Woof! 🐕

🐕 DOG SPECIAL ABILITIES:
Buddy is wagging tail happily! 🐕💕
Buddy is playing fetch with Sarah! 🎾
Buddy is guarding the house! 🏠🛡️

==================================================
📋 Animal Info:
  👤 Name: Whiskers
  🐾 Species: Cat
  🎂 Age: 2 years
  🏠 Habitat: House
Whiskers the Cat is eating 🍽️
Whiskers is sleeping in the House 😴
Whiskers says: Meow! Purr! 🐱

🐱 CAT SPECIAL ABILITIES:
Whiskers is climbing up high! 🐱🌳
Whiskers is hunting for toy mice! 🐱🧸
Whiskers is purring contentedly! 🐱💤

==================================================
📋 Animal Info:
  👤 Name: Ace
  🐾 Species: Eagle
  🎂 Age: 5 years
  🏠 Habitat: Sky
Ace the Eagle is eating 🍽️
Ace is sleeping in the Sky 😴
Ace says: Tweet! Chirp! 🐦

🐦 BIRD SPECIAL ABILITIES:
Ace is soaring through the sky with 6.5ft wingspan! 🐦✈️
Ace is building a cozy nest! 🐦🏠
```

**🔍 What This Code Does:**

This code demonstrates **polymorphism and specialized inheritance in a class hierarchy**:

1. **Polymorphic Design**: All animals share the same base interface (`eat()`, `sleep()`, `makeSound()`, `displayInfo()`) enabling polymorphic treatment.

2. **Method Overriding**: Each animal class overrides `makeSound()` with species-specific implementations, demonstrating behavioral polymorphism.

3. **Smart Constructor Logic**: Child constructors intelligently set parent properties (e.g., Cat sets habitat based on `isIndoor` boolean).

4. **Conditional Behavior**: Methods like `hunt()` and `fly()` demonstrate how object properties affect method behavior within inheritance.

5. **Type Checking**: Uses `is` operator to determine specific animal types, allowing access to specialized methods not available in the base class.

6. **Collection Polymorphism**: Shows how different animal types can be stored in a single `List<Animal>` while maintaining their unique behaviors.

---

## 🚗 Vehicle Inheritance Hierarchy

```dart
class Vehicle {
  String brand;
  String model;
  int year;
  String color;
  int maxSpeed;

  Vehicle(this.brand, this.model, this.year, this.color, this.maxSpeed);

  void start() {
    print('$color $year $brand $model is starting up! 🔥');
  }

  void stop() {
    print('$brand $model has stopped 🛑');
  }

  void honk() {
    print('$brand $model: BEEP BEEP! 📯');
  }

  void displaySpecs() {
    print('🚗 Vehicle Specifications:');
    print('  🏷️ Brand: $brand');
    print('  📋 Model: $model');
    print('  📅 Year: $year');
    print('  🎨 Color: $color');
    print('  💨 Max Speed: ${maxSpeed} mph');
  }
}

class Car extends Vehicle {
  int doors;
  String fuelType;
  bool hasAirConditioning;

  Car(String brand, String model, int year, String color, int maxSpeed,
      this.doors, this.fuelType, this.hasAirConditioning)
    : super(brand, model, year, color, maxSpeed);

  void openTrunk() {
    print('$model trunk is now open! 🧳');
  }

  void playMusic() {
    print('$model is playing your favorite music! 🎵');
  }

  @override
  void start() {
    print('$color $brand $model engine purring to life! 🚗💨');
    if (hasAirConditioning) {
      print('Air conditioning is cooling the cabin! ❄️');
    }
  }
}

class Motorcycle extends Vehicle {
  String bikeType;
  bool hasSidecar;

  Motorcycle(String brand, String model, int year, String color, int maxSpeed,
             this.bikeType, this.hasSidecar)
    : super(brand, model, year, color, maxSpeed);

  void wheelie() {
    print('$model is doing an awesome wheelie! 🏍️🤸‍♂️');
  }

  void leanIntoTurn() {
    print('$model is leaning smoothly into the turn! 🏍️💨');
  }

  @override
  void start() {
    print('$color $brand $model roars to life! 🏍️🔥');
  }

  @override
  void honk() {
    print('$brand $model: VROOM VROOM! 🏍️💨');
  }
}

class Truck extends Vehicle {
  int cargoCapacity;
  int wheels;
  bool hasTrailer;

  Truck(String brand, String model, int year, String color, int maxSpeed,
        this.cargoCapacity, this.wheels, this.hasTrailer)
    : super(brand, model, year, color, maxSpeed);

  void loadCargo() {
    print('$model is loading ${cargoCapacity} tons of cargo! 📦🚛');
  }

  void unloadCargo() {
    print('$model finished unloading at the destination! 📦✅');
  }

  @override
  void start() {
    print('$color $brand $model diesel engine rumbling! 🚛💪');
  }

  @override
  void honk() {
    print('$brand $model: HOOOOOOONK! 🚛📯');
  }
}

void main() {
  print('🚗 VEHICLE SHOWROOM 🚗\n');

  // Create different vehicles
  Car sedan = Car('Toyota', 'Camry', 2023, 'Blue', 120, 4, 'Gasoline', true);
  Motorcycle sportsBike = Motorcycle('Yamaha', 'YZF-R1', 2024, 'Red', 186, 'Sport', false);
  Truck deliveryTruck = Truck('Ford', 'F-150', 2022, 'White', 100, 5, 6, false);

  List<Vehicle> vehicles = [sedan, sportsBike, deliveryTruck];

  for (Vehicle vehicle in vehicles) {
    print('=' * 60);
    vehicle.displaySpecs();
    print('');

    // All vehicles can do these basic things
    vehicle.start();
    vehicle.honk();

    // Specific vehicle behaviors
    if (vehicle is Car) {
      print('\n🚗 CAR FEATURES:');
      print('  🚪 Doors: ${vehicle.doors}');
      print('  ⛽ Fuel Type: ${vehicle.fuelType}');
      print('  ❄️ AC: ${vehicle.hasAirConditioning ? "Yes" : "No"}');
      vehicle.openTrunk();
      vehicle.playMusic();
    } else if (vehicle is Motorcycle) {
      print('\n🏍️ MOTORCYCLE FEATURES:');
      print('  🏍️ Type: ${vehicle.bikeType}');
      print('  👥 Sidecar: ${vehicle.hasSidecar ? "Yes" : "No"}');
      vehicle.wheelie();
      vehicle.leanIntoTurn();
    } else if (vehicle is Truck) {
      print('\n🚛 TRUCK FEATURES:');
      print('  📦 Cargo Capacity: ${vehicle.cargoCapacity} tons');
      print('  🛞 Wheels: ${vehicle.wheels}');
      print('  🚚 Trailer: ${vehicle.hasTrailer ? "Yes" : "No"}');
      vehicle.loadCargo();
      vehicle.unloadCargo();
    }

    vehicle.stop();
    print('');
  }
}
```

**Output:**

```
🚗 VEHICLE SHOWROOM 🚗

============================================================
🚗 Vehicle Specifications:
  🏷️ Brand: Toyota
  📋 Model: Camry
  📅 Year: 2023
  🎨 Color: Blue
  💨 Max Speed: 120 mph

Blue 2023 Toyota Camry is starting up! 🔥
Toyota Camry: BEEP BEEP! 📯

🚗 CAR FEATURES:
  🚪 Doors: 4
  ⛽ Fuel Type: Gasoline
  ❄️ AC: Yes
Camry trunk is now open! 🧳
Camry is playing your favorite music! 🎵
Toyota Camry has stopped 🛑

============================================================
🚗 Vehicle Specifications:
  🏷️ Brand: Yamaha
  📋 Model: YZF-R1
  📅 Year: 2024
  🎨 Color: Red
  💨 Max Speed: 186 mph

Red 2024 Yamaha YZF-R1 is starting up! 🔥
Yamaha YZF-R1: BEEP BEEP! 📯

🏍️ MOTORCYCLE FEATURES:
  🏍️ Type: Sport
  👥 Sidecar: No
YZF-R1 is doing an awesome wheelie! 🏍️🤸‍♂️
YZF-R1 is leaning smoothly into the turn! 🏍️💨
Yamaha YZF-R1 has stopped 🛑

============================================================
🚗 Vehicle Specifications:
  🏷️ Brand: Ford
  📋 Model: F-150
  📅 Year: 2022
  🎨 Color: White
  💨 Max Speed: 100 mph

White 2022 Ford F-150 is starting up! 🔥
Ford F-150: BEEP BEEP! 📯

🚛 TRUCK FEATURES:
  📦 Cargo Capacity: 5 tons
  🛞 Wheels: 6
  🚚 Trailer: No
F-150 is loading 5 tons of cargo! 📦🚛
F-150 finished unloading at the destination! 📦✅
Ford F-150 has stopped 🛑
```

**🔍 What This Code Does:**

This code demonstrates **inheritance with vehicle-specific specialization**:

1. **Common Vehicle Properties**: Base class contains universal vehicle attributes (brand, model, year, color, maxSpeed) shared across all vehicle types.

2. **Specialized Properties**: Each vehicle type adds unique properties (car doors, motorcycle sidecar, truck cargo capacity) specific to that vehicle category.

3. **Method Enhancement**: Overridden methods like `start()` maintain the base interface while adding type-specific behavior (air conditioning for cars, engine sounds).

4. **Behavioral Differentiation**: Each vehicle type has unique methods (`wheelie()` for motorcycles, `loadCargo()` for trucks) that reflect real-world capabilities.

5. **Sound Customization**: Different `honk()` implementations show how the same action can vary dramatically between vehicle types.

6. **Constructor Chaining**: Demonstrates proper constructor delegation while adding type-specific parameter handling.

---

## 🎮 Gaming Character Hierarchy

```dart
class GameCharacter {
  String name;
  int level;
  int health;
  int maxHealth;
  int experience;

  GameCharacter(this.name, this.level, this.health, this.experience) {
    maxHealth = health;
  }

  void levelUp() {
    level++;
    maxHealth += 20;
    health = maxHealth; // Full heal on level up
    print('🎉 $name leveled up to $level! Max health: $maxHealth');
  }

  void takeDamage(int damage) {
    health -= damage;
    if (health < 0) health = 0;
    print('💥 $name took $damage damage! Health: $health/$maxHealth');
    if (health == 0) {
      print('💀 $name has been defeated!');
    }
  }

  void heal(int amount) {
    health += amount;
    if (health > maxHealth) health = maxHealth;
    print('💚 $name healed for $amount! Health: $health/$maxHealth');
  }

  void displayStats() {
    print('📊 $name\'s Stats:');
    print('  📈 Level: $level');
    print('  ❤️ Health: $health/$maxHealth');
    print('  ⭐ Experience: $experience');
  }

  void basicAttack() {
    print('⚔️ $name performs a basic attack!');
  }
}

class Warrior extends GameCharacter {
  int armor;
  String weaponType;

  Warrior(String name, int level, int health, int experience, this.armor, this.weaponType)
    : super(name, level, health, experience);

  @override
  void basicAttack() {
    print('⚔️ $name swings their $weaponType with mighty force!');
  }

  void shieldBlock() {
    print('🛡️ $name raises their shield and blocks the attack!');
  }

  void berserkerRage() {
    print('😤 $name enters berserker rage! Attack power doubled!');
  }

  void chargeAttack() {
    print('🏃‍♂️ $name charges forward with $weaponType ready!');
  }
}

class Mage extends GameCharacter {
  int mana;
  int maxMana;
  String magicSchool;

  Mage(String name, int level, int health, int experience, this.mana, this.magicSchool)
    : super(name, level, health, experience) {
    maxMana = mana;
  }

  @override
  void basicAttack() {
    if (mana >= 10) {
      mana -= 10;
      print('🔮 $name casts a $magicSchool spell! Mana: $mana/$maxMana');
    } else {
      print('💫 $name is out of mana and uses staff attack!');
    }
  }

  void castFireball() {
    if (mana >= 25) {
      mana -= 25;
      print('🔥 $name hurls a blazing fireball! Mana: $mana/$maxMana');
    } else {
      print('❌ Not enough mana for fireball!');
    }
  }

  void teleport() {
    if (mana >= 15) {
      mana -= 15;
      print('✨ $name teleports to safety! Mana: $mana/$maxMana');
    } else {
      print('❌ Not enough mana to teleport!');
    }
  }

  void restoreMana() {
    mana = maxMana;
    print('🧙‍♂️ $name meditates and restores full mana!');
  }
}

class Archer extends GameCharacter {
  int arrows;
  String bowType;
  int accuracy;

  Archer(String name, int level, int health, int experience, this.arrows, this.bowType, this.accuracy)
    : super(name, level, health, experience);

  @override
  void basicAttack() {
    if (arrows > 0) {
      arrows--;
      print('🏹 $name shoots an arrow with $bowType! Arrows left: $arrows');
    } else {
      print('🗡️ $name is out of arrows and uses melee attack!');
    }
  }

  void multiShot() {
    if (arrows >= 3) {
      arrows -= 3;
      print('🏹🏹🏹 $name shoots multiple arrows at once! Arrows left: $arrows');
    } else {
      print('❌ Not enough arrows for multi-shot!');
    }
  }

  void precisionShot() {
    if (arrows > 0) {
      arrows--;
      print('🎯 $name takes careful aim and shoots with ${accuracy}% accuracy!');
    } else {
      print('❌ No arrows left for precision shot!');
    }
  }

  void craftArrows() {
    arrows += 10;
    print('🪓 $name crafted 10 new arrows! Total arrows: $arrows');
  }
}

void main() {
  print('⚔️ EPIC FANTASY ADVENTURE ⚔️\n');

  // Create party of adventurers
  Warrior tank = Warrior('Sir Braveheart', 5, 120, 2400, 25, 'Battle Axe');
  Mage wizard = Mage('Mystic Luna', 4, 80, 1800, 100, 'Elemental');
  Archer ranger = Archer('Swift Arrow', 4, 90, 1900, 30, 'Elven Longbow', 95);

  List<GameCharacter> party = [tank, wizard, ranger];

  print('🎭 PARTY ASSEMBLY:');
  for (GameCharacter character in party) {
    character.displayStats();
    print('');
  }

  print('⚔️ BATTLE BEGINS!');
  print('=' * 50);

  // Battle simulation
  print('\n🌊 ROUND 1: Party attacks!');
  for (GameCharacter character in party) {
    character.basicAttack();

    // Use special abilities
    if (character is Warrior) {
      character.shieldBlock();
      character.berserkerRage();
    } else if (character is Mage) {
      character.castFireball();
      character.teleport();
    } else if (character is Archer) {
      character.precisionShot();
      character.multiShot();
    }
    print('');
  }

  print('💥 ROUND 2: Enemy counterattack!');
  for (GameCharacter character in party) {
    character.takeDamage(30);
  }

  print('\n💚 ROUND 3: Recovery time!');
  for (GameCharacter character in party) {
    character.heal(15);

    if (character is Mage) {
      character.restoreMana();
    } else if (character is Archer) {
      character.craftArrows();
    } else if (character is Warrior) {
      character.chargeAttack();
    }
  }

  print('\n🎊 FINAL STATS:');
  for (GameCharacter character in party) {
    character.displayStats();
    print('');
  }
}
```

**Output:**

```
⚔️ EPIC FANTASY ADVENTURE ⚔️

🎭 PARTY ASSEMBLY:
📊 Sir Braveheart's Stats:
  📈 Level: 5
  ❤️ Health: 120/140
  ⭐ Experience: 2400

📊 Mystic Luna's Stats:
  📈 Level: 4
  ❤️ Health: 80/100
  ⭐ Experience: 1800

📊 Swift Arrow's Stats:
  📈 Level: 4
  ❤️ Health: 90/110
  ⭐ Experience: 1900

⚔️ BATTLE BEGINS!
==================================================

🌊 ROUND 1: Party attacks!
⚔️ Sir Braveheart performs a basic attack!
🛡️ Sir Braveheart raises their shield and blocks the attack!
😤 Sir Braveheart enters berserker rage! Attack power doubled!
🏃‍♂️ Sir Braveheart charges forward with Battle Axe ready!

⚔️ Mystic Luna performs a basic attack!
🔮 Mystic Luna casts a Elemental spell! Mana: 90/100
✨ Mystic Luna teleports to safety! Mana: 75/100

⚔️ Swift Arrow performs a basic attack!
🎯 Swift Arrow takes careful aim and shoots with 95% accuracy!
🏹 Swift Arrow shoots an arrow with Elven Longbow! Arrows left: 29
🏹🏹🏹 Swift Arrow shoots multiple arrows at once! Arrows left: 26

==================================================
💥 ROUND 2: Enemy counterattack!
💥 Sir Braveheart took 30 damage! Health: 90/140
💥 Mystic Luna took 30 damage! Health: 50/100
💥 Swift Arrow took 30 damage! Health: 60/110

==================================================

💚 ROUND 3: Recovery time!
💚 Sir Braveheart healed for 15! Health: 105/140
🧙‍♂️ Mystic Luna meditates and restores full mana!
🪓 Swift Arrow crafted 10 new arrows! Total arrows: 36

🎊 FINAL STATS:
📊 Sir Braveheart's Stats:
  📈 Level: 5
  ❤️ Health: 105/140
  ⭐ Experience: 2400

📊 Mystic Luna's Stats:
  📈 Level: 4
  ❤️ Health: 50/100
  ⭐ Experience: 1800

📊 Swift Arrow's Stats:
  📈 Level: 4
  ❤️ Health: 60/110
  ⭐ Experience: 1900
```

**🔍 What This Code Does:**

This code demonstrates **game development patterns using inheritance with resource management**:

1. **Base Game Mechanics**: `GameCharacter` provides fundamental RPG mechanics (leveling, health, damage) that all character types need.

2. **Resource Management**: Different classes manage different resources (Warrior uses armor, Mage uses mana, Archer uses arrows) showing specialized resource systems.

3. **Conditional Abilities**: Methods check resource availability before executing (mana for spells, arrows for shots), implementing game balance mechanics.

4. **Class-Specific Combat**: Each class overrides `basicAttack()` with unique implementations that reflect their combat style and resource usage.

5. **Fallback Behaviors**: When resources are depleted, classes provide alternative actions (staff attack when out of mana, melee when out of arrows).

6. **Character Progression**: Demonstrates how inheritance can model character advancement systems in games while maintaining class-specific abilities.

---

## 🧠 Key Concepts Summary

### Inheritance Terminology

| Term             | Meaning                                   | Example                      |
| ---------------- | ----------------------------------------- | ---------------------------- |
| **Parent Class** | The original class (base class)           | `Animal`                     |
| **Child Class**  | The class that inherits (derived class)   | `Dog extends Animal`         |
| **`extends`**    | Keyword to create inheritance             | `class Dog extends Animal`   |
| **`super`**      | Refers to the parent class                | `super(name, age)`           |
| **`@override`**  | Marks methods that replace parent methods | `@override void makeSound()` |

### What Child Classes Get:

```dart
class Child extends Parent {
  // ✅ All parent properties
  // ✅ All parent methods
  // ✅ Can add new properties
  // ✅ Can add new methods
  // ✅ Can override parent methods
  // ✅ Can call parent methods with super
}
```

---

## 🎯 Types of Inheritance Relationships

### 1. **"Is-A" Relationship**

```dart
// Dog IS-A Animal
class Dog extends Animal { }

// Car IS-A Vehicle
class Car extends Vehicle { }
```

### 2. **Method Overriding**

```dart
class Parent {
  void greet() => print('Hello from Parent');
}

class Child extends Parent {
  @override
  void greet() => print('Hi from Child!'); // Different behavior
}
```

### 3. **Using Super Constructor**

```dart
class Parent {
  String name;
  Parent(this.name);
}

class Child extends Parent {
  int age;
  Child(String name, this.age) : super(name); // Call parent constructor
}
```

---

## 🚀 Benefits of Inheritance

**✅ Code Reusability:**

- Write common functionality once in parent class
- All children automatically get these features

**✅ Logical Organization:**

- Group related classes in hierarchies
- Easy to understand relationships

**✅ Polymorphism Support:**

- Treat different objects the same way
- `List<Animal>` can hold Dogs, Cats, Birds

**✅ Easy Maintenance:**

- Change parent class → all children updated
- Add new features in one place

---

## ⚠️ When NOT to Use Inheritance

**❌ Avoid inheritance when:**

- Classes aren't truly related ("is-a" doesn't make sense)
- You only need a few methods from another class
- The relationship is more "uses-a" than "is-a"

**🔄 Use composition instead:**

```dart
// ❌ Bad: Rectangle extends Color (Rectangle is NOT a Color)
class Rectangle extends Color { }

// ✅ Good: Rectangle has a Color
class Rectangle {
  Color color;
  Rectangle(this.color);
}
```

---

## 🎮 Practice Challenges

Try creating inheritance hierarchies for these scenarios:

1. **🏫 School System**: Person → Student, Teacher, Principal
2. **📱 Electronics**: Device → Phone, Laptop, Tablet
3. **🎵 Media**: MediaFile → AudioFile, VideoFile, ImageFile
4. **🏪 E-commerce**: Product → Book, Clothing, Electronics

---

## 🎉 Remember This!

Inheritance is like a **family tree** 🌳:

- **👴 Grandparents** (base classes) pass traits to **👨‍👩‍👧‍👦 Parents** (intermediate classes)
- **Parents** pass traits to **👧👦 Children** (derived classes)
- Each generation can **add new traits** and **modify inherited ones**
- **Family resemblance** shows through shared methods and properties

**The Magic**: You get all the **good stuff** from your parents, can **add your own special abilities**, and can **do some things your own way**!

Just like real families, programming inheritance creates **related groups** of classes that **share common features** while having their **own unique personalities**! 🎪✨

**Pro Tip**: Use inheritance when you have a **clear "is-a" relationship** - if you can say "Child IS-A Parent" and it makes sense, inheritance is perfect! 🎯
