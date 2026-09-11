import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, this.onCourseTap});
  final VoidCallback? onCourseTap;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final surface = isDark ? Colors.white.withValues(alpha: .05) : Colors.white;
    final border =
        isDark ? Colors.white.withValues(alpha: .07) : const Color(0xffEAECEF);

    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        centerTitle: false,
        title: Text('Dartic',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontSize: 21.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: -.3)),
        actions: [
          IconButton(
            onPressed: () {},
            icon: Icon(Icons.notifications_none_rounded,
                size: 22.sp,
                color: isDark ? Colors.white60 : AppColors.blackText),
          ),
          SizedBox(width: 4.w),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.fromLTRB(20.w, 10.h, 20.w, 30.h),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // ── Streak bar ──
          BlocBuilder<AppCubit, AppState>(builder: (context, _) {
            final progress = context.read<AppCubit>().userProgress;
            final passedCount = progress?.passedCourses?.length ?? 0;
            final dsaSolved = progress?.passedDsa?.length ?? 0;
            return GestureDetector(
              onTap: () => AppRouter.push(AppRouter.activity),
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 14.h),
                decoration: BoxDecoration(
                  color: surface,
                  border: Border.all(color: border),
                  borderRadius: BorderRadius.circular(12.r),
                ),
                child: Row(children: [
                  Icon(Icons.local_fire_department_rounded,
                      color: const Color(0xffFF6B35), size: 20.sp),
                  SizedBox(width: 8.w),
                  Text('7 day streak',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          fontSize: 14.sp, fontWeight: FontWeight.w600)),
                  const Spacer(),
                  _StatPill(
                      value: '$passedCount', label: 'lessons', isDark: isDark),
                  SizedBox(width: 8.w),
                  _StatPill(
                      value: '$dsaSolved', label: 'solved', isDark: isDark),
                  SizedBox(width: 8.w),
                  Icon(Icons.chevron_right_rounded,
                      size: 18.sp, color: AppColors.grey),
                ]),
              ),
            );
          }),

          SizedBox(height: 24.h),

          // ── Paths ──
          Text('Paths',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontSize: 17.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: -.2)),
          SizedBox(height: 12.h),

          _PathCard(
            title: 'Dart fundamentals',
            subtitle: '30 lessons · Beginner',
            image: Assets.images.dart,
            accentColor: AppColors.appBlue,
            surface: surface,
            border: border,
            isDark: isDark,
            onTap: onCourseTap,
          ),

          SizedBox(height: 10.h),

          _PathCard(
            title: 'Algorithm practice',
            subtitle: 'Problem sets · Intermediate',
            image: Assets.images.dsa,
            accentColor: const Color(0xff15805C),
            surface: surface,
            border: border,
            isDark: isDark,
            onTap: () {
              FirebaseAuth.instance.currentUser == null
                  ? AppRouter.pushAndClear(AppRouter.onboarding)
                  : AppRouter.push(AppRouter.dsaList);
            },
          ),

          SizedBox(height: 28.h),

          // ── Quick tip ──
          _QuickTip(isDark: isDark, surface: surface, border: border),
        ]),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  STAT PILL — compact "3 lessons" badge
// ─────────────────────────────────────────────────────

class _StatPill extends StatelessWidget {
  const _StatPill({
    required this.value,
    required this.label,
    required this.isDark,
  });
  final String value;
  final String label;
  final bool isDark;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 4.h),
        decoration: BoxDecoration(
          color: isDark
              ? Colors.white.withValues(alpha: .07)
              : const Color(0xffF4F5F7),
          borderRadius: BorderRadius.circular(6.r),
        ),
        child: Text('$value $label',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                fontSize: 11.sp,
                fontWeight: FontWeight.w600,
                color: isDark ? Colors.white60 : const Color(0xff5A6069))),
      );
}

// ─────────────────────────────────────────────────────
//  PATH CARD
// ─────────────────────────────────────────────────────

class _PathCard extends StatelessWidget {
  const _PathCard({
    required this.title,
    required this.subtitle,
    required this.image,
    required this.accentColor,
    required this.surface,
    required this.border,
    required this.isDark,
    required this.onTap,
  });
  final String title;
  final String subtitle;
  final AppAssetImage image;
  final Color accentColor;
  final Color surface;
  final Color border;
  final bool isDark;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12.r),
          child: Container(
            decoration: BoxDecoration(
              color: surface,
              border: Border.all(color: border),
              borderRadius: BorderRadius.circular(12.r),
            ),
            child: Row(children: [
              // Thumbnail
              ClipRRect(
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(11.r),
                    bottomLeft: Radius.circular(11.r)),
                child: SizedBox(
                    width: 88.w,
                    height: 88.h,
                    child: image.image(fit: BoxFit.cover)),
              ),
              // Content
              Expanded(
                child: Padding(
                  padding:
                      EdgeInsets.symmetric(horizontal: 14.w, vertical: 14.h),
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(title,
                            style: Theme.of(context)
                                .textTheme
                                .bodyLarge
                                ?.copyWith(
                                    fontSize: 15.sp,
                                    fontWeight: FontWeight.w600,
                                    letterSpacing: -.15)),
                        SizedBox(height: 4.h),
                        Text(subtitle,
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                    fontSize: 12.sp, color: AppColors.grey)),
                      ]),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(right: 14.w),
                child: Icon(Icons.chevron_right_rounded,
                    size: 20.sp, color: AppColors.grey),
              ),
            ]),
          ),
        ),
      );
}

// ─────────────────────────────────────────────────────
//  QUICK TIP
// ─────────────────────────────────────────────────────

class _QuickTip extends StatelessWidget {
  const _QuickTip({
    required this.isDark,
    required this.surface,
    required this.border,
  });
  final bool isDark;
  final Color surface;
  final Color border;

  static const _tips = [
    (
      'AOT + JIT',
      'Dart uses both ahead-of-time (AOT) and just-in-time (JIT) compilation. AOT compilation produces fast native code for production, while JIT compilation enables features such as hot reload during development.'
    ),
    (
      'Null Safety',
      'Dart uses sound null safety to help prevent null reference errors. A type such as String cannot contain null unless you explicitly mark it as nullable with String?.'
    ),
    (
      'Cascade Notation',
      'Cascade notation lets you perform multiple operations on the same object without repeatedly writing its variable name. Use .. for non-nullable objects and ?.. when the object may be null.'
    ),
    (
      'String Interpolation',
      'String interpolation lets you insert variables and expressions directly into a string. Use \$variable for simple values or \${expression} when an expression needs to be evaluated.'
    ),
    (
      'Extension Methods',
      'Extension methods let you add functionality to an existing type without changing its original source code or creating a subclass. They are useful for adding convenient helper methods to types you do not own.'
    ),
    (
      'Named Parameters',
      'Named parameters make function calls easier to read by identifying arguments by name. Place them inside {} and use required when the caller must provide the argument.'
    ),
    (
      'Records',
      'Records are anonymous, immutable structures that let you group multiple values into a single object. They are especially useful when a function needs to return multiple values without creating a separate class.'
    ),
    (
      'Arrow Functions',
      'Arrow functions provide a concise syntax for functions that contain a single expression. For example, int square(int x) => x * x; returns the result of the expression directly.'
    ),
    (
      'Final Variables',
      'A final variable can only be assigned once. Unlike const, its value does not need to be known at compile time and can be determined while the program is running.'
    ),
    (
      'Constant Values',
      'The const keyword creates compile-time constants. A const value must be known before the program runs and cannot be changed after it has been created.'
    ),
    (
      'Late Variables',
      'The late keyword tells Dart that a non-nullable variable will be initialized later. It allows you to declare the variable first and assign its value before accessing it.'
    ),
    (
      'Variable Type Inference',
      'Using var allows Dart to determine a variable’s type from the value assigned to it. The variable remains strongly typed even though you did not explicitly write the type.'
    ),
    (
      'Dynamic Type',
      'The dynamic type tells Dart to allow a value to behave as any type. Static type checking is reduced for dynamic values, so incorrect operations may only be detected when the program runs.'
    ),
    (
      'Object Type',
      'Object is the base type for Dart objects. Unlike dynamic, using Object keeps static type checking in place, making it safer when you do not know the exact type of a value.'
    ),
    (
      'Never Type',
      'Never represents a type for values that can never successfully exist. It is commonly used by functions that always throw an exception or never complete normally.'
    ),
    (
      'First-Class Functions',
      'Functions are objects in Dart, which means you can store them in variables, pass them as arguments, return them from other functions, and place them inside collections.'
    ),
    (
      'Anonymous Functions',
      'An anonymous function is a function without a name. They are commonly used when passing short pieces of behavior directly to methods such as map(), where(), and forEach().'
    ),
    (
      'Closures',
      'A closure is a function that remembers variables from the surrounding scope where it was created. This allows the function to continue accessing those variables later.'
    ),
    (
      'Optional Parameters',
      'Optional parameters allow a function to be called without providing every argument. Use [] for optional positional parameters and {} for optional named parameters.'
    ),
    (
      'Default Parameters',
      'Optional parameters can have default values. The default value is automatically used when the caller does not provide an argument.'
    ),
    (
      'Required Parameters',
      'The required keyword makes a named parameter mandatory. The parameter remains named, but Dart reports an error if the caller does not provide it.'
    ),
    (
      'Generics',
      'Generics allow classes, functions, and collections to work with different types while maintaining type safety. For example, List<String> represents a list that should contain strings.'
    ),
    (
      'Typedefs',
      'A typedef gives a function type or another type a reusable name. This can make complex function signatures easier to read and use throughout a Dart project.'
    ),
    (
      'Getters',
      'A getter allows a class to expose a value using property-style syntax while calculating or controlling how that value is obtained. Getters are accessed without parentheses.'
    ),
    (
      'Setters',
      'A setter lets you control what happens when a value is assigned to a property. Setters are useful when a class needs to validate or transform a value before storing it.'
    ),
    (
      'Constructors',
      'Constructors are special methods used to create and initialize objects. They can receive parameters, assign fields, and perform setup when an object is created.'
    ),
    (
      'Named Constructors',
      'Named constructors provide additional ways to create an instance of a class. They are useful when objects can be initialized from different sources, such as User.fromJson().'
    ),
    (
      'Factory Constructors',
      'A factory constructor does not necessarily create a new object every time it is called. It can return an existing instance, a cached object, or an instance of a subclass.'
    ),
    (
      'Constant Constructors',
      'A const constructor allows instances of a class to be created as compile-time constants. All values used to create the object must also be suitable for compile-time evaluation.'
    ),
    (
      'Abstract Classes',
      'An abstract class provides a blueprint for other classes and cannot be instantiated directly. It can contain both implemented methods and abstract methods that subclasses must implement.'
    ),
    (
      'Interfaces',
      'Every Dart class defines an interface containing its public members. Another class can implement that interface to provide its own implementation of those members.'
    ),
    (
      'Inheritance',
      'Inheritance allows a class to reuse and extend the behavior of another class. Use the extends keyword to create a subclass that inherits members from a superclass.'
    ),
    (
      'Mixins',
      'Mixins provide a way to reuse methods and properties across multiple classes without requiring those classes to share the same superclass.'
    ),
    (
      'Enums',
      'Enums represent a fixed set of related values. They are useful when a variable should only contain one value from a predefined collection of choices.'
    ),
    (
      'Sealed Classes',
      'Sealed classes restrict which classes can extend a class. This allows Dart to know the possible subclasses and helps the compiler check whether pattern matching is exhaustive.'
    ),
    (
      'Pattern Matching',
      'Patterns allow Dart to inspect, match, and extract values from objects. They can be used with switch statements, switch expressions, variable declarations, and assignments.'
    ),
    (
      'Switch Expressions',
      'A switch expression evaluates a value and returns a result. Unlike a traditional switch statement, it can be directly assigned to a variable or returned from a function.'
    ),
    (
      'Destructuring',
      'Destructuring allows you to unpack values from structured data such as records into individual variables, making it easier to work with multiple values.'
    ),
    (
      'Lists',
      'A List is an ordered collection of values. Each element has an index starting from zero, and a List can contain duplicate values.'
    ),
    (
      'Sets',
      'A Set is a collection that stores unique values. Adding the same value multiple times does not create duplicate elements.'
    ),
    (
      'Maps',
      'A Map stores data as key-value pairs. Each key is associated with a value, allowing you to retrieve information using the key.'
    ),
    (
      'Iterables',
      'An Iterable represents a sequence of values that can be processed one at a time. Dart provides methods such as map(), where(), reduce(), and fold() for working with iterables.'
    ),
    (
      'Map Method',
      'The map() method transforms every element in an iterable into another value. It returns a new iterable containing the transformed results.'
    ),
    (
      'Where Method',
      'The where() method filters an iterable based on a condition. Only elements for which the provided function returns true are included in the resulting iterable.'
    ),
    (
      'Reduce Method',
      'The reduce() method combines the elements of an iterable into a single value. It uses the first element as the initial value and repeatedly applies the provided function.'
    ),
    (
      'Fold Method',
      'The fold() method combines all elements of an iterable into one value while allowing you to provide the initial value yourself.'
    ),
    (
      'Spread Operator',
      'The spread operator (...) inserts all elements from one collection into another collection. It is useful when building lists, sets, and other collection literals.'
    ),
    (
      'Collection If',
      'A collection if lets you conditionally add an element to a List, Set, or Map directly inside the collection literal.'
    ),
    (
      'Collection For',
      'A collection for lets you generate multiple elements inside a collection literal by iterating over another iterable.'
    ),
    (
      'Null-Aware Operators',
      'Dart provides several operators for working safely with nullable values. Use ?. for safe access, ?? for fallback values, and ??= to assign only when a value is null.'
    ),
    (
      'Type Checking',
      'The is operator checks whether an object is an instance of a particular type. It can also help Dart promote a variable to a more specific type after the check.'
    ),
    (
      'Type Casting',
      'The as operator explicitly treats an object as a particular type. If the object is not compatible with that type, a runtime error occurs.'
    ),
    (
      'Exceptions',
      'Exceptions represent errors or unexpected conditions that occur while a program is running. Use throw to create an exception and try-catch to handle it.'
    ),
    (
      'Rethrow',
      'The rethrow keyword lets you pass an exception from a catch block to another error handler. It preserves the original exception and stack trace.'
    ),
    (
      'Future',
      'A Future represents a value that will become available later. Futures are commonly used for asynchronous operations such as network requests, file operations, and database queries.'
    ),
    (
      'Async and Await',
      'The async keyword marks a function as asynchronous, while await pauses execution within that function until a Future completes without blocking the entire program.'
    ),
    (
      'Streams',
      'A Stream represents a sequence of asynchronous values that arrive over time. Streams are useful for events, real-time data, and other operations that produce multiple values.'
    ),
    (
      'Yield',
      'The yield keyword produces a value from a generator function. Unlike return, yield can produce multiple values over time.'
    ),
    (
      'Synchronous Generators',
      'A function marked with sync* creates a synchronous generator. It uses yield to lazily produce values through an Iterable.'
    ),
    (
      'Asynchronous Generators',
      'A function marked with async* creates an asynchronous generator. It uses yield to produce values over time through a Stream.'
    ),
    (
      'Lazy Evaluation',
      'Lazy evaluation delays calculating a value until it is actually needed. Dart uses lazy evaluation with features such as Iterables and generators to avoid unnecessary work.'
    ),
    (
      'Isolates',
      'Isolates allow Dart programs to perform concurrent work using separate memory and execution contexts. Isolates communicate by sending messages rather than sharing memory directly.'
    ),
    (
      'Event Loop',
      'Dart uses an event loop to process asynchronous events and callbacks. It allows the program to handle tasks such as timers and I/O without blocking normal execution.'
    ),
    (
      'Microtasks',
      'A microtask is a high-priority asynchronous task that is processed before the event queue continues. Dart uses a microtask queue for short pieces of deferred work.'
    ),
    (
      'Timers',
      'The Timer class schedules code to run after a specified duration. A timer can execute once or repeatedly at a fixed interval.'
    ),
    (
      'Libraries',
      'Dart libraries organize code into reusable units. A library can contain classes, functions, variables, and other declarations that can be imported by other Dart files.'
    ),
    (
      'Imports',
      'The import keyword makes declarations from another Dart library available in the current file. Imports help split large programs into smaller, reusable pieces.'
    ),
    (
      'Show and Hide',
      'The show and hide keywords control which declarations are imported from a library. This helps avoid naming conflicts and keeps the imported API focused.'
    ),
    (
      'Part Files',
      'The part and part of keywords allow multiple files to form a single Dart library. They are available for specific library organization needs, although normal imports are often preferred.'
    ),
    (
      'Pubspec YAML',
      'The pubspec.yaml file contains important Dart project configuration such as the project name, dependencies, SDK constraints, assets, and package metadata.'
    ),
    (
      'Dart Packages',
      'Dart packages are reusable collections of Dart code that can be shared between projects. Dependencies are typically managed through pubspec.yaml.'
    ),
    (
      'Dart Formatter',
      'dart format automatically formats Dart source code according to Dart’s standard formatting conventions, making code more consistent and readable.'
    ),
    (
      'Dart Analyzer',
      'The Dart analyzer examines your code before it runs and reports problems such as type errors, undefined identifiers, warnings, and other issues.'
    ),
    (
      'Assertions',
      'The assert statement checks that a condition is true during development. It is useful for detecting incorrect assumptions while writing and testing code.'
    ),
    (
      'Equality',
      'The == operator checks whether two values are equal. When creating value-based classes, == and hashCode should normally be overridden together.'
    ),
    (
      'Operator Overloading',
      'Dart allows classes to define how operators such as +, -, ==, [], and > behave for their objects. This can make custom types work naturally with operators.'
    ),
    (
      'Callable Classes',
      'A class becomes callable like a function when it defines a call() method. This allows an object to be invoked using parentheses.'
    ),
    (
      'Lexical Scope',
      'Lexical scope determines where a variable can be accessed based on where it was declared in the source code. Inner scopes can access variables from their surrounding scopes.'
    ),
    (
      'Private Members',
      'A Dart identifier beginning with an underscore (_) is private to its library. This convention is commonly used to hide implementation details from other libraries.'
    ),
  ];
  @override
  Widget build(BuildContext context) {
    final tip = _tips[DateTime.now().day % _tips.length];
    return Container(
      padding: EdgeInsets.all(16.w),
      decoration: BoxDecoration(
        color: surface,
        border: Border.all(color: border),
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          width: 32.r,
          height: 32.r,
          decoration: BoxDecoration(
            color: isDark
                ? const Color(0xffF9A825).withValues(alpha: .12)
                : const Color(0xffFFF8E1),
            borderRadius: BorderRadius.circular(8.r),
          ),
          child: Icon(Icons.lightbulb_outline_rounded,
              size: 16.sp, color: const Color(0xffF9A825)),
        ),
        SizedBox(width: 12.w),
        Expanded(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(tip.$1,
                style: Theme.of(context)
                    .textTheme
                    .bodyLarge
                    ?.copyWith(fontSize: 13.sp, fontWeight: FontWeight.w600)),
            SizedBox(height: 3.h),
            Text(tip.$2,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontSize: 12.sp, color: AppColors.grey, height: 1.45)),
          ]),
        ),
      ]),
    );
  }
}
