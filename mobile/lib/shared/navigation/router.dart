import 'dart:async';

import 'package:dartcoder/features/authetication/views/create_profile_screen.dart';
import 'package:dartcoder/features/authetication/views/onboarding_screen.dart';
import 'package:dartcoder/features/courses/views/course_quiz.dart';
import 'package:dartcoder/features/courses/views/quiz_score_screen.dart';
import 'package:dartcoder/features/dashboard/views/activity_screen.dart';
import 'package:dartcoder/features/dashboard/views/dashboard_screen.dart';
import 'package:dartcoder/features/editor/views/dsa_list_screen.dart';
import 'package:dartcoder/features/profile/views/badges_screen.dart';
import 'package:dartcoder/features/courses/views/courses_list_screen.dart';
import 'package:dartcoder/features/courses/views/dsa_course_screen.dart';

import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class AppRouter {
  static final navKey = GlobalKey<NavigatorState>();

  /// Routes that require a signed-in Firebase user. Guests are sent to
  /// onboarding instead (Firestore rules also reject unauthenticated reads).
  static const _authRequired = {dsaCourse, dsaCourseDetails};

  static Route generateRoute(RouteSettings settings) {
    if (_authRequired.contains(settings.name) &&
        FirebaseAuth.instance.currentUser == null) {
      return CupertinoPageRoute(builder: (_) => const OnboardingScreen());
    }
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
      case activity:
        return CupertinoPageRoute(builder: (_) => const ActivityScreen());
      case badges:
        return CupertinoPageRoute(builder: (_) => const BadgesScreen());
      case quizScore:
        return CupertinoPageRoute(
            builder: (_) => QuizScoreScreen(
                arg: settings.arguments as QuizScoreScreenArgs?));
      case coursesList:
        return CupertinoPageRoute(builder: (_) => const CoursesListScreen());
      case dsaCourse:
        return CupertinoPageRoute(builder: (_) => const DsaCourseListScreen());
      case dsaCourseDetails:
        return CupertinoPageRoute(
            builder: (_) => DsaCourseDetailsScreen(
                arg: settings.arguments as DsaCourseDetailsArgs));

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
  static const String activity = "/activity";
  static const String badges = "/badges";
  static const String coursesList = "/courses_list";
  static const String dsaCourse = "/dsa_course";
  static const String dsaCourseDetails = "/dsa_course_details";

  static Future push(String routeName, {Object? arg}) async =>
      await navKey.currentState?.pushNamed(routeName, arguments: arg);

  static void pop({Object? arg}) async => navKey.currentState?.pop(arg);
  static void pushReplacement(String routeName, {Object? arg}) async =>
      navKey.currentState?.pushReplacementNamed(routeName, arguments: arg);
  static void pushAndClear(String routeName, {Object? arg}) async => navKey
      .currentState
      ?.pushNamedAndRemoveUntil(routeName, (route) => false, arguments: arg);

  static OverlayEntry? _toast;

  /// Shows a short message as a toast above the keyboard and bottom insets.
  ///
  /// Drawn in the navigator's overlay rather than as a floating SnackBar, so a
  /// tall FloatingActionButton (e.g. the editor's run/test buttons) or an open
  /// keyboard can't push it off screen. A new message replaces the old one.
  static void showMessage(String message) {
    final overlay = navKey.currentState?.overlay;
    if (overlay == null) return;
    _toast?.remove();
    late final OverlayEntry entry;
    entry = OverlayEntry(
      builder: (_) => _Toast(
        message: message,
        onDismissed: () {
          if (_toast == entry) _toast = null;
          if (entry.mounted) entry.remove();
        },
      ),
    );
    _toast = entry;
    overlay.insert(entry);
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

class _Toast extends StatefulWidget {
  const _Toast({required this.message, required this.onDismissed});

  final String message;
  final VoidCallback onDismissed;

  @override
  State<_Toast> createState() => _ToastState();
}

class _ToastState extends State<_Toast> with SingleTickerProviderStateMixin {
  late final _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 220),
      reverseDuration: const Duration(milliseconds: 180))
    ..forward();
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer(const Duration(seconds: 3), () async {
      if (!mounted) return;
      await _controller.reverse();
      widget.onDismissed();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final media = MediaQuery.of(context);
    final bottom = media.viewInsets.bottom + media.padding.bottom + 24;
    final curve =
        CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic);
    return Positioned(
      left: 16,
      right: 16,
      bottom: bottom,
      child: IgnorePointer(
        child: FadeTransition(
          opacity: curve,
          child: SlideTransition(
            position: Tween(begin: const Offset(0, .3), end: Offset.zero)
                .animate(curve),
            child: Center(
              child: Material(
                color: Colors.transparent,
                child: Container(
                  padding:
                      EdgeInsets.symmetric(horizontal: 15.w, vertical: 10.h),
                  decoration: BoxDecoration(
                      color: AppColors.black,
                      borderRadius: BorderRadius.circular(8)),
                  child: Text(widget.message,
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontSize: 14.sp,
                          fontWeight: FontWeight.w400,
                          color: AppColors.white)),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
