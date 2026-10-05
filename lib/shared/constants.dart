import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:markdown_widget/config/configs.dart';

import '../features/courses/models/course_model.dart';

class AppData {
  static final courses = {
    "Basics": [
      CourseModel(
          title: "Introduction",
          path: "assets/courses/main.md",
          id: 0,
          quiz: "assets/jsons/quizzes/main.json",
          desc: "Introduction to Dart programming language.",
          videos: [
            "https://youtu.be/Gd97ql0gW9Q?si=qK3oJ5dE6RzfaG05",
            "https://youtu.be/XUuS82_lUTk?si=MUvf25uPgYh0n8ev",
          ]),
      CourseModel(
          title: "Variables and Data Types",
          path: "assets/courses/variables.md",
          id: 1,
          desc: "Learn about variables and data types in Dart and their usage.",
          videos: [
            "https://youtu.be/rUs7H9fZdV4?si=eHzomTSWcXNWfkbX",
            "https://youtu.be/Sqpr3HMx-I0?si=RtZYIO1Pk5WBkMWu"
          ],
          quiz: "assets/jsons/quizzes/variables.json"),
      CourseModel(
          title: "Operators",
          path: "assets/courses/operators.md",
          id: 2,
          desc: "Learn about different operators in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=JJF28iLSAQA",
            "https://youtu.be/cgiIK0VVmXM?si=fEIfGbCqvuG0iuOA"
          ],
          quiz: "assets/jsons/quizzes/operator.json"),
      CourseModel(
          title: "Comments",
          path: "assets/courses/comments.md",
          id: 3,
          desc: "Learn how to write comments in Dart code.",
          videos: [
            "https://youtu.be/8XKL78pi_Y4?si=mqDg4XmywN3yzgJs",
          ],
          quiz: "assets/jsons/quizzes/comments.json"),
      CourseModel(
          title: "Input/Output",
          path: "assets/courses/input_output.md",
          id: 4,
          canPractice: false,
          desc: "Learn how to handle input and output in Dart applications.",
          videos: ["https://youtu.be/rFP953T0lfQ?si=1N1Usu2sDOzX5SnW"],
          quiz: "assets/jsons/quizzes/input_output.json"),
      CourseModel(
        title: "Control Flow",
        path: "assets/courses/control_flow.md",
        id: 5,
        desc:
            "Understand control flow statements in Dart such as if-else and switch-case.",
        videos: [
          "https://www.youtube.com/watch?v=5udl_LBpAHk",
        ],
        quiz: "assets/jsons/quizzes/control_flow.json",
      ),
      CourseModel(
        title: "Switch case",
        path: "assets/courses/switch_case.md",
        id: 6,
        desc:
            "Learn how to use switch-case statements in Dart for multi-way branching.",
        videos: [
          "https://youtu.be/TxmO6QJ-r2o?si=L56DLpJRQ8IdauLh",
          "https://www.youtube.com/watch?v=OLo2s1em8_8"
        ],
        quiz: "assets/jsons/quizzes/switch_case.json",
      ),
      CourseModel(
        title: "For Loops",
        path: "assets/courses/for_loops.md",
        id: 7,
        desc: "Learn how to use for loops in Dart for iteration.",
        videos: [
          "https://www.youtube.com/watch?v=Q1y7u6JbDHM",
          "https://youtu.be/lDyGYxsAxTU?si=1uL4wB_Quf85fa5A"
        ],
        quiz: "assets/jsons/quizzes/for_loop.json",
      ),
      CourseModel(
          title: "While Loops",
          path: "assets/courses/while_loop.md",
          id: 8,
          desc: "Learn how to use while loops in Dart for iteration.",
          videos: [
            "https://www.youtube.com/watch?v=u4j1EAnd6RU",
            "https://www.youtube.com/watch?v=YZg_0yvueu8"
          ],
          quiz: "assets/jsons/quizzes/while_loop.json"),
      CourseModel(
          title: "Do-While Loops",
          path: "assets/courses/do_while.md",
          id: 9,
          desc: "Learn how to use do-while loops in Dart for iteration.",
          videos: [
            "https://youtu.be/pGGWQr46Ee0?si=v3LmGckwoOWyDZqc",
          ],
          quiz: "assets/jsons/quizzes/do_while.json"),
      CourseModel(
          title: "List",
          path: "assets/courses/list.md",
          id: 10,
          desc: "Learn about lists in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=sAWPh3Hzdvs",
          ],
          quiz: "assets/jsons/quizzes/list.json"),
      CourseModel(
          title: "Sets",
          path: "assets/courses/sets.md",
          id: 11,
          desc: "Learn about sets in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=AbfbANY1X2U",
          ],
          quiz: "assets/jsons/quizzes/sets.json"),
      CourseModel(
          title: "Maps",
          path: "assets/courses/map.md",
          id: 12,
          desc: "Learn about maps in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=792ek6Y9940",
            "https://www.youtube.com/watch?v=wkF28m7jZVw"
          ],
          quiz: "assets/jsons/quizzes/map.json"),
      CourseModel(
          title: "Functions",
          path: "assets/courses/functions.md",
          id: 12,
          desc: "Learn about functions in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=NsrlCADdWdw",
            "https://www.youtube.com/watch?v=EpVgqc7jy9o"
          ],
          quiz: "assets/jsons/quizzes/functions.json"),
      CourseModel(
          title: "Enums",
          path: "assets/courses/enum.md",
          id: 13,
          desc: "Learn about enums in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=r6-zUB2YVNE",
            "https://www.youtube.com/watch?v=UPrtRkBdwWk"
          ],
          quiz: "assets/jsons/quizzes/enum.json"),
      CourseModel(
          title: "Null Safety",
          path: "assets/courses/null_safe.md",
          id: 14,
          desc: "Learn about null safety in Dart and how to use it.",
          videos: [
            "https://www.youtube.com/watch?v=iYhOU9AuaFs",
            "https://www.youtube.com/watch?v=nf5eqagjw8c"
          ],
          quiz: "assets/jsons/quizzes/null_safe.json"),
    ],
    "Intermediate": [
      CourseModel(
          title: "Classes and objects",
          path: "assets/courses/classes.md",
          id: 15,
          desc: "Learn about classes and objects in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=5PZj0MXckz4",
            "https://www.youtube.com/watch?v=dKrFJojxavU"
          ],
          quiz: "assets/jsons/quizzes/classes.json"),
      CourseModel(
          title: "Inheritance",
          path: "assets/courses/inheritance.md",
          id: 16,
          desc: "Learn about inheritance in Dart and how to use it.",
          videos: [
            "https://www.youtube.com/watch?v=IPoHzLZZu08",
            "https://www.youtube.com/watch?v=m8QiP8L1T_4"
          ],
          quiz: "assets/jsons/quizzes/inheritance.json"),
      CourseModel(
          title: "Abstract Class",
          path: "assets/courses/abstract_class.md",
          id: 17,
          desc: "Learn about abstract classes in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=cTp9cV-tB_E",
            "https://www.youtube.com/watch?v=VAs7eHX-8fQ"
          ],
          quiz: "assets/jsons/quizzes/abstract_class.json"),
      CourseModel(
          title: "Mixins",
          path: "assets/courses/mixins.md",
          id: 18,
          desc: "Learn about mixins in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=VlG-K14YMe0",
            "https://www.youtube.com/watch?v=03X0QWT6zCw"
          ],
          quiz: "assets/jsons/quizzes/mixins.json"),
      CourseModel(
          title: "Getters and Setters",
          path: "assets/courses/getters_setters.md",
          id: 19,
          desc: "Learn about getters and setters in Dart and how to use them.",
          videos: ["https://www.youtube.com/watch?v=BPmqmaLY2_o"],
          quiz: "assets/jsons/quizzes/getters_setters.json"),
      CourseModel(
        title: "Anonymous Functions",
        path: "assets/courses/anonymous_functions.md",
        id: 20,
        desc: "Learn about anonymous functions in Dart and how to use them.",
        videos: [
          "https://www.youtube.com/watch?v=XTKKQdTAR0U",
        ],
        quiz: "assets/jsons/quizzes/anonymous_functions.json",
      ),
      CourseModel(
          title: "Higher-Order Functions",
          path: "assets/courses/high_order_function.md",
          id: 21,
          desc:
              "Learn about higher-order functions in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=DfZoyUDCbSg",
            "https://www.youtube.com/watch?v=nyzH2IM1bM0"
          ],
          quiz: "assets/jsons/quizzes/high_order_function.json"),
      CourseModel(
          title: "Closures",
          path: "assets/courses/closure.md",
          id: 22,
          desc: "Learn about closures in Dart and how to use them.",
          videos: ["https://www.youtube.com/watch?v=NaxyY2Rq0j8"],
          quiz: "assets/jsons/quizzes/closure.json"),
      CourseModel(
        title: "Try-Catch, finally",
        path: "assets/courses/try_catch_finally.md",
        id: 23,
        desc: "Learn about try-catch-finally in Dart and how to use it.",
        quiz: "assets/jsons/quizzes/try_catch_finally.json",
      ),
      CourseModel(
          title: "Custom Exception",
          path: "assets/courses/custom_exception.md",
          id: 24,
          desc: "Learn about custom exceptions in Dart and how to use them.",
          videos: ["https://www.youtube.com/watch?v=2uyMvzTr9xI"],
          quiz: "assets/jsons/quizzes/custom_exception.json"),
    ],
    "Advanced": [
      CourseModel(
        title: "Futures",
        path: "assets/courses/future.md",
        id: 25,
        desc: "Learn about futures in Dart and how to use them.",
        quiz: "assets/jsons/quizzes/future.json",
      ),
      CourseModel(
          title: "Async/Await",
          path: "assets/courses/async_await.md",
          id: 26,
          desc: "Learn about async/await in Dart and how to use it.",
          videos: [
            "https://www.youtube.com/watch?v=OTS-ap9_aXc&t=72s",
            "https://www.youtube.com/watch?v=i5qLpkfa8NQ"
          ],
          quiz: "assets/jsons/quizzes/async_await.json"),
      CourseModel(
          title: "Streams",
          path: "assets/courses/stream.md",
          id: 27,
          desc: "Learn about streams in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=nQBpOIHE4eE",
            "https://www.youtube.com/watch?v=tnYTHacU8Z0"
          ],
          quiz: "assets/jsons/quizzes/stream.json"),
      CourseModel(
          title: "Generics",
          path: "assets/courses/generics.md",
          id: 28,
          desc: "Learn about generics in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=8MywaeBqFmI",
            "https://www.youtube.com/watch?v=Te6M8gVqKv4"
          ],
          quiz: "assets/jsons/quizzes/generics.json"),
      CourseModel(
          title: "Extension Methods",
          path: "assets/courses/extension.md",
          id: 29,
          desc: "Learn about extension methods in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=D3j0OSfT9ZI",
            "https://www.youtube.com/watch?v=B8tjpyg7A3k"
          ],
          quiz: "assets/jsons/quizzes/extension.json"),
      CourseModel(
          title: "Sealed Classes",
          path: "assets/courses/sealed_classes.md",
          id: 30,
          desc: "Learn about sealed classes in Dart and how to use them.",
          videos: ["https://www.youtube.com/watch?v=JHbtQLPOy3o"],
          quiz: "assets/jsons/quizzes/sealed_classes.json"),
      CourseModel(
        title: "Unit Testing (Basic)",
        path: "assets/courses/unit_test.md",
        id: 31,
        desc: "Learn about unit testing in Dart and how to use it.",
        quiz: "assets/jsons/quizzes/unit_test.json",
      ),
      CourseModel(
          title: "Isolates",
          path: "assets/courses/isolates.md",
          id: 32,
          desc: "Learn about isolates in Dart and how to use them.",
          videos: [
            "https://www.youtube.com/watch?v=PPwJ75vqP_s",
            "https://www.youtube.com/watch?v=vl_AaCgudcY&t=27s"
          ],
          quiz: "assets/jsons/quizzes/isolates.json"),
      CourseModel(
        title: "Collection Methods",
        path: "assets/courses/collection_method.md",
        id: 33,
        desc: "Learn about collection methods in Dart and how to use them.",
        quiz: "assets/jsons/quizzes/collection_method.json",
      ),
    ]
  };
}

class AppButton extends StatelessWidget {
  const AppButton(
      {super.key,
      this.leftIcon,
      this.text = '',
      this.backgroundColor,
      this.textColor,
      this.onTap,
      this.borderColor});
  final Widget? leftIcon;
  final String text;
  final Color? backgroundColor;
  final Color? borderColor;
  final Color? textColor;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: double.infinity,
        height: 40.h,
        decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10.r),
            border:
                borderColor != null ? Border.all(color: borderColor!) : null,
            color: backgroundColor ?? context.colors.primary),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (leftIcon != null) leftIcon!,
            if (leftIcon != null) SizedBox(width: 10.w),
            Text(
              text,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  fontSize: 14.sp,
                  fontWeight: FontWeight.bold,
                  color: textColor ?? context.colors.onPrimary),
            )
          ],
        ),
      ),
    );
  }
}

// Reusable TextFormField widget
class AppTextFormField extends StatelessWidget {
  final TextEditingController controller;
  final String labelText;
  final String? Function(String?)? validator;

  const AppTextFormField({
    super.key,
    required this.controller,
    required this.labelText,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      textCapitalization: TextCapitalization.words,
      inputFormatters: [FilteringTextInputFormatter.allow(RegExp("[a-zA-Z]"))],
      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            fontSize: 14,
            fontWeight: FontWeight.w400,
          ),
      decoration: InputDecoration(
        labelText: labelText,
        labelStyle: Theme.of(context).textTheme.bodySmall?.copyWith(
              fontSize: 14,
              fontWeight: FontWeight.w400,
            ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: BorderSide(color: context.colors.primary, width: 2),
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: BorderSide(color: context.colors.outline),
        ),
      ),
      validator: validator ??
          (value) {
            if (value == null || value.trim().isEmpty) {
              return 'This field is required';
            }
            return null;
          },
    );
  }
}

Widget loadingWidget(BuildContext context) {
  return Container(
      height: double.infinity,
      width: double.infinity,
      color: context.colors.scrim.withValues(alpha: 0.5),
      child: Center(
        child: CircularProgressIndicator(
          color: context.colors.primary,
        ),
      ));
}

MarkdownConfig markdownConfig(BuildContext context) =>
    context.isDark ? MarkdownConfig.darkConfig : MarkdownConfig.defaultConfig;

class ShadowContainer extends StatelessWidget {
  const ShadowContainer(
      {super.key,
      this.desc,
      this.difficulty,
      this.title,
      this.onTap,
      this.completed});

  final String? title;
  final String? desc;
  final String? difficulty;
  final VoidCallback? onTap;
  final bool? completed;

  (Color, Color) _getDifficultyColors(BuildContext context, String difficulty) {
    final colors = context.colors;
    final palette = context.palette;
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return (palette.success, palette.onSuccess);
      case 'medium':
        return (palette.warning, palette.onWarning);
      case 'hard':
        return (colors.error, colors.onError);
      default:
        return (colors.outline, colors.surface);
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: EdgeInsets.only(bottom: 20.h, left: 5.w, right: 5.w),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10.r),
          color: context.colors.surfaceContainerLow,
          border: Border.all(
              color: completed == true
                  ? context.palette.success
                  : context.colors.outlineVariant),
          boxShadow: [
            BoxShadow(
              color: context.colors.shadow.withValues(alpha: .05),
              blurRadius: 8,
              spreadRadius: 2,
              offset: const Offset(0, 4),
            ),
            BoxShadow(
              color: context.colors.shadow.withValues(alpha: .01),
              blurRadius: 4,
              spreadRadius: 1,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: ListTile(
            contentPadding: EdgeInsets.zero,
            title: Text(
              title ?? 'Default',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                  ),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (desc != null)
                  Text(
                    desc!,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontSize: 12,
                        ),
                  ),
                if (difficulty != null)
                  Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: _getDifficultyColors(context, difficulty ?? "").$1,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      difficulty ?? "",
                      style: TextStyle(
                        color:
                            _getDifficultyColors(context, difficulty ?? "").$2,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
