import 'package:dartcoder/features/authentication/views/create_profile_screen.dart';
import 'package:dartcoder/features/authentication/views/onboarding_screen.dart';
import 'package:dartcoder/features/courses/views/course_quiz.dart';
import 'package:dartcoder/features/courses/views/quiz_score_screen.dart';
import 'package:dartcoder/features/dashboard/views/dashboard_screen.dart';
import 'package:dartcoder/features/editor/views/dsa_list_screen.dart';

import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class AppRouter {
  static final navKey = GlobalKey<NavigatorState>();

  static Route generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case onboarding:
        return CupertinoPageRoute(builder: (_) => const OnboardingScreen());

      case dashboard:
        return CupertinoPageRoute(builder: (_) => const DashboardScreen());
      case courseDetails:
        return CupertinoPageRoute(
            builder: (_) =>
                CourseDetails(arg: settings.arguments as CourseDetailsArgs?));
      case editor:
        return CupertinoPageRoute(
            builder: (_) =>
                EditorScreen(arg: settings.arguments as EditorScreenArg?));
      case createProfile:
        return CupertinoPageRoute(builder: (_) => const CreateProfileScreen());
      case quiz:
        return CupertinoPageRoute(
            builder: (_) =>
                CourseQuiz(arg: settings.arguments as CourseQuizArg?));
      case dsaList:
        return CupertinoPageRoute(builder: (_) => const DsaListScreen());
      case quizScore:
        return CupertinoPageRoute(
            builder: (_) => QuizScoreScreen(
                arg: settings.arguments as QuizScoreScreenArgs?));

      default:
        return CupertinoPageRoute(builder: (_) => const OnboardingScreen());
    }
  }

  static const String onboarding = "/";
  static const String dashboard = "/dashboard";
  static const String courseDetails = "/courseDetails";
  static const String editor = "/editor";
  static const String quiz = "/quiz";
  static const String quizScore = "/quiz_score";
  static const String createProfile = "/create_profile";
  static const String dsaList = "/dsa_list";

  static Future push(String routeName, {Object? arg}) async =>
      await navKey.currentState?.pushNamed(routeName, arguments: arg);

  static void pop({Object? arg}) async => navKey.currentState?.pop(arg);
  static void pushReplacement(String routeName, {Object? arg}) async =>
      navKey.currentState?.pushReplacementNamed(routeName, arguments: arg);
  static void pushAndClear(String routeName, {Object? arg}) async => navKey
      .currentState
      ?.pushNamedAndRemoveUntil(routeName, (route) => false, arguments: arg);

  static void showMessage(String message) {
    ScaffoldMessenger.of(navKey.currentContext!).showSnackBar(SnackBar(
      elevation: 0,
      content: Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Flexible(
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 10.h),
              decoration: BoxDecoration(
                  color: Theme.of(navKey.currentContext!)
                      .colorScheme
                      .inverseSurface,
                  borderRadius: BorderRadius.circular(8)),
              child: Text(message,
                  style: Theme.of(navKey.currentContext!)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(
                          fontSize: 14.sp,
                          fontWeight: FontWeight.w400,
                          color: Theme.of(navKey.currentContext!)
                              .colorScheme
                              .onInverseSurface)),
            ),
          ),
        ],
      ),
      backgroundColor: Colors.transparent,
      margin: const EdgeInsets.all(10),
      duration: const Duration(seconds: 3),
      clipBehavior: Clip.antiAlias,
      behavior: SnackBarBehavior.floating,
    ));
  }

  static Future showConfirmation(String s,
      {required Null Function() onConfirm}) {
    return showDialog(
        context: navKey.currentContext!,
        builder: (context) {
          return AlertDialog(
            title: const Text("Confirm"),
            content: Text(s),
            actions: [
              TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: const Text("Cancel")),
              TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                    onConfirm();
                  },
                  child: const Text("Confirm")),
            ],
          );
        });
  }
}
