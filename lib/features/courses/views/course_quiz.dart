import 'dart:convert';

import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/features/courses/models/quiz_model.dart';
import 'package:dartcoder/features/courses/views/question_widget.dart';
import 'package:dartcoder/features/courses/views/quiz_score_screen.dart';

import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class CourseQuiz extends StatefulWidget {
  const CourseQuiz({super.key, this.arg});
  final CourseQuizArg? arg;
  @override
  State<CourseQuiz> createState() => _CourseQuizState();
}

class _CourseQuizState extends State<CourseQuiz> {
  List<QuizModel> quizzes = [];

  void loadData(CourseModel course) async {
    await rootBundle.loadString(course.quiz ?? "").then((e) {
      List<QuizModel> allQuizzes = e == ""
          ? []
          : (json.decode(e) as List).map((e) => QuizModel.fromJson(e)).toList();

      // Select 10 random questions
      if (allQuizzes.length <= 10) {
        // If we have 10 or fewer questions, use them all
        quizzes = allQuizzes;
      } else {
        // Randomly select 10 questions
        List<QuizModel> shuffled = List.from(allQuizzes);
        shuffled.shuffle();
        quizzes = shuffled.take(10).toList();
      }

      setState(() {});
    });
  }

  @override
  void initState() {
    if (widget.arg?.course != null) loadData(widget.arg!.course!);
    super.initState();
  }

  final pageController = PageController();

  int currentQuestion = 1;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: SafeArea(
        child: Container(
          margin: EdgeInsets.only(bottom: 20.h),
          color: Colors.transparent,
          padding: EdgeInsets.symmetric(
            horizontal: 20.w,
          ),
          height: 40.h,
          child: Row(
            children: [
              InkWell(
                splashFactory: NoSplash.splashFactory,
                highlightColor: Colors.transparent,
                onTap: () {
                  if (currentQuestion > 1) {
                    pageController.previousPage(
                        duration: const Duration(milliseconds: 300),
                        curve: Curves.easeInOut);
                  } else {
                    AppRouter.showMessage(
                      "You are on the first question",
                    );
                  }
                },
                child: Container(
                  height: 40.h,
                  width: 40.h,
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10.r),
                      border: Border.all(color: context.colors.primary)),
                  child: Center(
                    child: Icon(Icons.arrow_back_ios,
                        size: 15.sp, color: context.colors.primary),
                  ),
                ),
              ),
              SizedBox(width: 10.w),
              Expanded(
                child: AppButton(
                  onTap: () {
                    if (currentQuestion == quizzes.length) {
                      AppRouter.pushReplacement(AppRouter.quizScore,
                          arg: QuizScoreScreenArgs(
                            totalQuestions: quizzes.length,
                            correctAnswers: quizzes
                                .where((e) => e.isCorrect == true)
                                .length,
                            courseId: widget.arg?.course?.id,
                          ));
                    } else {
                      pageController.nextPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut);
                    }
                  },
                  text: AppString.next,
                ),
              ),
            ],
          ),
        ),
      ),
      appBar: AppBar(
        title: Text(widget.arg?.course?.title ?? "Quiz"),
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 20.h),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("Questions $currentQuestion/${quizzes.length}",
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontSize: 13.sp, fontWeight: FontWeight.bold)),
                SizedBox(height: 5.h),
                LinearProgressIndicator(
                  value: quizzes.isEmpty ? 0 : currentQuestion / quizzes.length,
                  minHeight: 7.h,
                  borderRadius: BorderRadius.circular(50),
                ),
              ],
            ),
            SizedBox(height: 20.h),
            Expanded(
              child: PageView.builder(
                controller: pageController,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: quizzes.length,
                onPageChanged: (value) {
                  currentQuestion = value + 1;
                  setState(() {});
                  FocusScope.of(context).unfocus();
                },
                itemBuilder: (context, index) {
                  final e = quizzes[index];
                  return SingleChildScrollView(
                    child: Column(
                      key: ValueKey(e.question),
                      children: [
                        QuestionWidget(
                            onType: (index, val) {
                              if (e.type == "fill") {
                                // For fill-in-the-blank, update specific index
                                List<String> currentAnswers =
                                    List<String>.from(e.userAnswer ?? []);

                                // Ensure the list is long enough
                                while (currentAnswers.length <= index) {
                                  currentAnswers.add('');
                                }

                                currentAnswers[index] = val;
                                quizzes[quizzes.indexOf(e)] =
                                    e.copyWith(userAnswer: currentAnswers);
                              } else {
                                // For other types, keep existing behavior
                                quizzes[quizzes.indexOf(e)] =
                                    e.copyWith(userAnswer: [val]);
                              }

                              setState(() {});
                            },
                            answerType: e.type ?? "mcq",
                            userAnswer: e.userAnswer,
                            question: e.question ?? "",
                            key: ValueKey(e.question)),
                        SizedBox(height: 20.h),
                        if (e.type == "order")
                          Wrap(spacing: 10.w, runSpacing: 10.h, children: [
                            ...?(e.options)?.map((op) {
                              final selected =
                                  e.userAnswer?.contains(op) == true;
                              return InkWell(
                                highlightColor: Colors.transparent,
                                splashFactory: NoSplash.splashFactory,
                                onTap: () {
                                  if (selected) {
                                    final updatedAnswers =
                                        List<String>.from(e.userAnswer ?? []);
                                    updatedAnswers.remove(op);
                                    quizzes[index] =
                                        e.copyWith(userAnswer: updatedAnswers);
                                  } else if ((e.userAnswer?.length ?? 0) <
                                      (e.answer?.length ?? 0)) {
                                    final updatedAnswers =
                                        List<String>.from(e.userAnswer ?? []);
                                    updatedAnswers.add(op);
                                    quizzes[index] =
                                        e.copyWith(userAnswer: updatedAnswers);
                                  }

                                  setState(() {});
                                },
                                child: Container(
                                    padding: EdgeInsets.symmetric(
                                        horizontal: 10.w, vertical: 8.h),
                                    decoration: BoxDecoration(
                                      borderRadius: BorderRadius.circular(4),
                                      color: selected
                                          ? context.colors.primaryContainer
                                          : context.colors.surfaceContainerLow,
                                      border: Border.all(
                                          color: selected
                                              ? context.colors.primary
                                              : context.colors.outlineVariant),
                                      boxShadow: [
                                        BoxShadow(
                                          color: context.colors.shadow
                                              .withValues(alpha: .05),
                                          blurRadius: 8,
                                          spreadRadius: 2,
                                          offset: const Offset(0, 4),
                                        ),
                                        BoxShadow(
                                          color: context.colors.shadow
                                              .withValues(alpha: .01),
                                          blurRadius: 4,
                                          spreadRadius: 1,
                                          offset: const Offset(0, 2),
                                        ),
                                      ],
                                    ),
                                    child: Text(op)),
                              );
                            })
                          ]),
                        if (e.type == "mcq")
                          ...?e.options?.map((op) {
                            final selected = e.userAnswer?.firstOrNull == op;

                            return InkWell(
                              splashFactory: NoSplash.splashFactory,
                              highlightColor: Colors.transparent,
                              onTap: () {
                                quizzes[index] = e.copyWith(
                                    userAnswer: selected ? null : [op]);

                                setState(() {});
                              },
                              child: Container(
                                margin: EdgeInsets.only(bottom: 10.h),
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(10.r),
                                  color: selected
                                      ? context.colors.primaryContainer
                                      : context.colors.surfaceContainerLow,
                                  border: Border.all(
                                      color: selected
                                          ? context.colors.primary
                                          : context.colors.outlineVariant),
                                  boxShadow: [
                                    BoxShadow(
                                      color: context.colors.shadow
                                          .withValues(alpha: .05),
                                      blurRadius: 8,
                                      spreadRadius: 2,
                                      offset: const Offset(0, 4),
                                    ),
                                    BoxShadow(
                                      color: context.colors.shadow
                                          .withValues(alpha: .01),
                                      blurRadius: 4,
                                      spreadRadius: 1,
                                      offset: const Offset(0, 2),
                                    ),
                                  ],
                                ),
                                child: Padding(
                                  padding: EdgeInsets.symmetric(
                                      horizontal: 15.w, vertical: 10.h),
                                  child: Row(
                                    children: [
                                      Container(
                                        padding: EdgeInsets.all(1.sp),
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          border: Border.all(
                                              color: selected
                                                  ? context.colors.primary
                                                  : context.colors.outline),
                                        ),
                                        child: Icon(
                                          Icons.circle,
                                          size: 10,
                                          color: selected
                                              ? context.colors.primary
                                              : Colors.transparent,
                                        ),
                                      ),
                                      SizedBox(width: 15.w),
                                      Expanded(
                                        child: Text(
                                            op
                                                .replaceAll("\n", "\n")
                                                .replaceAll("\\n", "\n"),
                                            style: Theme.of(context)
                                                .textTheme
                                                .bodyLarge
                                                ?.copyWith(fontSize: 15)),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          }),
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class CourseQuizArg {
  final CourseModel? course;
  CourseQuizArg({this.course});
}
