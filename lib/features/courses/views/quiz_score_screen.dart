import 'package:confetti/confetti.dart';
import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:flutter_screenutil/flutter_screenutil.dart';

class QuizScoreScreen extends StatefulWidget {
  const QuizScoreScreen({super.key, this.arg});
  final QuizScoreScreenArgs? arg;

  @override
  State<QuizScoreScreen> createState() => _QuizScoreScreenState();
}

class _QuizScoreScreenState extends State<QuizScoreScreen> {
  late ConfettiController _controller;

  @override
  void initState() {
    _controller = ConfettiController(duration: const Duration(seconds: 10));
    final percentage = ((widget.arg?.correctAnswers ?? 0) /
        (widget.arg?.totalQuestions ?? 1) *
        100);

    if (percentage >= 80 && widget.arg?.trackProgress != false) {
      context.read<AppCubit>().updatePassedCourses(widget.arg?.courseId ?? 0);
    }
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final percentage = ((widget.arg?.correctAnswers ?? 0) /
        (widget.arg?.totalQuestions ?? 1) *
        100);

    return Scaffold(
        bottomNavigationBar: SafeArea(
          child: Container(
            margin: EdgeInsets.only(bottom: 20.h),
            color: Colors.transparent,
            padding: EdgeInsets.symmetric(
              horizontal: 20.w,
            ),
            height: 40.h,
            child: AppButton(
              onTap: () {
                if (widget.arg?.trackProgress == false) {
                  AppRouter.pop();
                } else if (widget.arg?.courseId == 33) {
                  AppRouter.pushAndClear(AppRouter.dashboard);
                } else {
                  final item = AppData.courses.values
                      .toList()
                      .reduce((value, element) => value + element)
                      .where((e) => e.id == ((widget.arg?.courseId ?? 0) + 1))
                      .firstOrNull;
                  if (item != null) {
                    AppRouter.pushReplacement(AppRouter.courseDetails,
                        arg: CourseDetailsArgs(course: item));
                  }
                }
              },
              textColor: AppColors.white,
              text: widget.arg?.trackProgress == false
                  ? "Back to lesson"
                  : widget.arg?.courseId == 33
                      ? "Home"
                      : AppString.next,
            ),
          ),
        ),
        body: SafeArea(
            child: Stack(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Assets.json.trophy.lottie(
                    height: 150.h,
                    width: 150.w,
                    fit: BoxFit.contain,
                    onLoaded: (composition) {
                      if (percentage >= 80) {
                        _controller.play();
                      }
                    }),
                SizedBox(height: 20.h),
                Text(
                  percentage >= 80 ? "Congratulations!" : "Quiz Completed!",
                  textAlign: TextAlign.center,
                  style: Theme.of(context)
                      .textTheme
                      .bodyLarge
                      ?.copyWith(fontSize: 25.sp, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 10.h),
                Text(
                  "You have scored ${percentage.toStringAsFixed(0)}%",
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontSize: 16.sp,
                        fontWeight: FontWeight.w400,
                      ),
                ),
              ],
            ),
            if (percentage >= 80)
              Positioned(
                top: 0,
                left: 0,
                child: ConfettiWidget(
                  confettiController: _controller,
                  blastDirectionality: BlastDirectionality.explosive,

                  // blastDirection: pi / 2,

                  // maxBlastForce: 5, // set a lower max blast force
                  // minBlastForce: 2, // set a lower min blast force
                  // emissionFrequency: 0.05,
                  // numberOfParticles: 50, // a lot of particles at once
                  // gravity: 1,
                ),
              ),
          ],
        )));
  }

  @override
  void dispose() {
    _controller.dispose();

    super.dispose();
  }
}

class QuizScoreScreenArgs {
  final num? totalQuestions;
  final num? correctAnswers;
  final num? courseId;

  /// False for quizzes outside the bundled Dart course, which have no
  /// numeric course id to record or advance to.
  final bool trackProgress;

  QuizScoreScreenArgs({
    this.totalQuestions,
    this.correctAnswers,
    this.courseId,
    this.trackProgress = true,
  });
}
