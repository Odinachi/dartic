import 'package:dartcoder/features/authentication/view_model/app_cubit.dart';
import 'package:dartcoder/features/authentication/views/onboarding_screen.dart';
import 'package:dartcoder/features/courses/views/courses_list_screen.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/features/profile/views/profile_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/features/dashboard/views/home.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen>
    with TickerProviderStateMixin {
  late TabController tabController;
  @override
  void initState() {
    super.initState();

    context.read<AppCubit>().getUserProfile();
    tabController = TabController(length: 4, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomSheet: Container(
        height: 70.h,
        padding: EdgeInsets.only(bottom: 5.h),
        decoration: BoxDecoration(
          color: context.colors.surfaceContainer,
          boxShadow: [
            BoxShadow(
              color: context.colors.shadow.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, -5),
            ),
          ],
        ),
        child: SafeArea(
          child: TabBar(
            physics: const NeverScrollableScrollPhysics(),
            onTap: (value) => setState(() {}),
            controller: tabController,
            tabs: [
              navItem(
                  label: AppString.home,
                  icon: Assets.svgs.home,
                  isActive: tabController.index == 0),
              navItem(
                  label: AppString.courses,
                  icon: Assets.svgs.course,
                  isActive: tabController.index == 1),
              navItem(
                  label: AppString.editor,
                  icon: Assets.svgs.editor,
                  isActive: tabController.index == 2),
              navItem(
                  label: AppString.profile,
                  icon: Assets.svgs.person,
                  isActive: tabController.index == 3),
            ],
            indicatorColor: Colors.transparent,
            dividerColor: Colors.transparent,
            indicator: const BoxDecoration(),
          ),
        ),
      ),
      body: Padding(
        padding: EdgeInsets.only(bottom: 60.h),
        child: TabBarView(
            controller: tabController,
            physics: const NeverScrollableScrollPhysics(),
            children: [
              HomeScreen(
                onCourseTap: () {
                  tabController.index = 1;
                  setState(() {});
                },
              ),
              CoursesListScreen(),
              EditorScreen(
                arg: EditorScreenArg(isPractice: false),
              ),
              FirebaseAuth.instance.currentUser != null
                  ? ProfileScreen(
                      onDiveIn: () {
                        tabController.index = 1;
                        setState(() {});
                      },
                    )
                  : const OnboardingScreen(),
            ]),
      ),
    );
  }

  Column navItem(
      {required String label, required SvgImage icon, bool isActive = false}) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        icon.svg(
          height: 15.h,
          width: 15.w,
          color: isActive
              ? context.colors.primary
              : context.colors.onSurfaceVariant,
        ),
        Text(label,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontSize: 12.sp,
                  fontWeight: FontWeight.w500,
                  color: isActive
                      ? context.colors.primary
                      : context.colors.onSurfaceVariant,
                )),
      ],
    );
  }
}
