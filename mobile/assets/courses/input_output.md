# Input and Output

Imagine you're at a candy shop 🍭. The shopkeeper asks, "What candy do you want?" and you say "Chocolate!"

That’s **input** — you’re **giving information** to the program.

---

## 📢 What is Output?

Now imagine the shopkeeper gives you the chocolate and says, "Here you go!" — that’s **output** — the program **shows
something** to you.

---

## 🖨️ Output in Dart: `print()`

To **show something**, we use `print()`:

```dart
void main() {
  print('Hello, friend!'); // Output: Hello, friend!
}
```

**🔍 What This Code Does:**

This code demonstrates **basic output functionality in Dart**:

1. **Console Output**: The `print()` function displays text in the console/terminal where the Dart program is running.

2. **String Literals**: The text `'Hello, friend!'` is a string literal enclosed in single quotes, which gets displayed exactly as written.

3. **Immediate Execution**: When the program runs, this message appears instantly without waiting for any user interaction.

4. **Program Entry Point**: The `main()` function is where Dart programs begin execution, making this the first thing users see.

5. **Simple Communication**: This is the most basic form of program-to-user communication in console applications.

Dart prints that message for you to see.

---

## 🎤 Input in Dart (in Console Apps)

To **ask the user something**, we can use Dart's `stdin.readLineSync()` — but we need to import `dart:io` first.

```dart
import 'dart:io';

void main() {
  print('What is your name?');
  String? name = stdin.readLineSync();
  print('Hello, $name!');
}
```

**🔍 What This Code Does:**

This code demonstrates **interactive console input and output**:

1. **Library Import**: `import 'dart:io';` gives access to input/output functionality that's not available by default in Dart core.

2. **User Prompting**: `print('What is your name?');` displays a question to guide the user on what input is expected.

3. **Input Reading**: `stdin.readLineSync()` pauses program execution and waits for the user to type something and press Enter.

4. **Nullable String Handling**: `String? name` indicates that the input might be null, following Dart's null safety requirements.

5. **String Interpolation**: `$name` embeds the user's input directly into the output string, creating personalized responses.

6. **Synchronous Operation**: The program waits at the input line until the user provides input before continuing to the next line.

- `import 'dart:io';` tells Dart we want to use input features.
- `stdin.readLineSync()` waits for the user to type something.
- We store the input in a variable (`name`) and use it later!

---

## 🧁 Real-Life Example

You: 🗣️ “I want cookies!”
Dart: 👂 (listens)
Dart: 🗣️ “Hello, I heard you want cookies!”

In code:

```dart
import 'dart:io';

void main() {
  print('What do you want?');
  String? snack = stdin.readLineSync();
  print('Yum! I heard you want $snack!');
}
```

**🔍 What This Code Does:**

This code demonstrates **a complete input-output conversation flow**:

1. **Conversational Programming**: Creates a natural dialogue between the program and user, simulating a real conversation.

2. **Variable Naming**: Uses descriptive variable name `snack` that clearly indicates what type of input is expected.

3. **Response Generation**: The program acknowledges the user's input by incorporating it into an enthusiastic response.

4. **User Experience**: Provides immediate feedback that confirms the program understood and processed the user's input correctly.

5. **Interactive Flow**: Shows the complete cycle of prompt → input → acknowledgment that forms the basis of interactive programs.

6. **Emotional Programming**: Uses words like "Yum!" to make the interaction feel more engaging and human-like.

---

## 🧠 Note

In mobile apps, we don't use `stdin` — instead we use buttons, text fields, etc. But for learning Dart in a console,
this is how input/output works.

---

## 💡 Summary

- `print()` is how Dart **talks** to you (output).
- `stdin.readLineSync()` is how Dart **listens** to you (input).
- It's like a fun chat between you and Dart!

So remember: **Input is you talking to Dart, and Output is Dart talking back!** 🗣️👂🎉
