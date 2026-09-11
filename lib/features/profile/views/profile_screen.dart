import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:dartcoder/main.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key, this.onDiveIn});
  final VoidCallback? onDiveIn;

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final courseList = AppData.courses.values.toList();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final surface = isDark ? Colors.white.withValues(alpha: .05) : Colors.white;
    final border =
        isDark ? Colors.white.withValues(alpha: .07) : const Color(0xffEAECEF);

    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
            automaticallyImplyLeading: false,
            centerTitle: false,
            title: Text(AppString.profile,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    fontSize: 20.sp,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -.2)),
            actions: [_settingsMenu()]),
        body: BlocBuilder<AppCubit, AppState>(builder: (_, __) {
          final user = context.read<AppCubit>().profile;
          final progress = context.read<AppCubit>().userProgress;
          final allCourses = courseList.expand((courses) => courses).toList();
          final currentCourse = allCourses
              .where((course) =>
                  course.id ==
                  context.read<AppCubit>().userProgress?.currentCourse)
              .firstOrNull;
          final nextCourse = currentCourse == null
              ? null
              : allCourses
                  .where((course) => course.id == (currentCourse.id ?? 0) + 1)
                  .firstOrNull;
          final fullName =
              '${user?.firstName ?? ''} ${user?.lastName ?? ''}'.trim();
          final lessonsCompleted = progress?.passedCourses?.length ?? 0;
          final problemsSolved = progress?.passedDsa?.length ?? 0;

          return SingleChildScrollView(
            padding: EdgeInsets.fromLTRB(20.w, 17.h, 20.w, 30.h),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              // ── Identity ──
              _ProfileHeader(
                name: fullName.isEmpty ? 'Dart learner' : fullName,
                username: user?.username,
                year: user?.createdAt?.year,
                isDark: isDark,
                surface: surface,
                border: border,
              ),

              SizedBox(height: 18.h),

              // ── Stats ──
              _StatsRow(
                lessonsCompleted: lessonsCompleted,
                problemsSolved: problemsSolved,
                surface: surface,
                border: border,
              ),

              SizedBox(height: 18.h),

              // ── Badges ──
              _BadgesRow(
                surface: surface,
                border: border,
                isDark: isDark,
              ),

              SizedBox(height: 28.h),

              // ── Course Progress ──
              Text(AppString.courseProgress,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontSize: 17.sp,
                      fontWeight: FontWeight.w700,
                      letterSpacing: -.2)),
              SizedBox(height: 12.h),
              if (currentCourse != null) ...[
                _CourseRow(
                    course: currentCourse,
                    label: 'Currently learning',
                    surface: surface,
                    border: border,
                    onTap: () => AppRouter.push(AppRouter.courseDetails,
                        arg: CourseDetailsArgs(course: currentCourse))),
                if (nextCourse != null) ...[
                  SizedBox(height: 9.h),
                  _CourseRow(
                      course: nextCourse,
                      label: 'Up next',
                      surface: surface,
                      border: border,
                      onTap: () => AppRouter.push(AppRouter.courseDetails,
                          arg: CourseDetailsArgs(course: nextCourse)))
                ],
              ] else
                _EmptyState(
                    onTap: widget.onDiveIn, surface: surface, border: border),
            ]),
          );
        }),
      ),
    );
  }

  Widget _settingsMenu() => PopupMenuButton<String>(
        icon: Icon(Icons.more_horiz_rounded, size: 23.sp),
        onSelected: (value) {
          if (value == 'theme') {
            isDarkTheme.value = !isDarkTheme.value;
          }
          if (value == 'logout') {
            context.read<AppCubit>().signOut();
          }
          if (value == 'delete') {
            AppRouter.showConfirmation(
                'Are you sure you want to delete your account? This action is irreversible.',
                onConfirm: () {
              context.read<AppCubit>().deleteAccount();
            });
          }
        },
        itemBuilder: (context) => [
          PopupMenuItem(
              value: 'theme',
              child: Text(
                  isDarkTheme.value ? 'Use light theme' : 'Use dark theme')),
          const PopupMenuItem(value: 'logout', child: Text('Log out')),
          const PopupMenuItem(
              value: 'delete',
              child: Text('Delete account',
                  style: TextStyle(color: AppColors.red)))
        ],
      );
}

// ─────────────────────────────────────────────────────
//  PROFILE HEADER
// ─────────────────────────────────────────────────────

class _ProfileHeader extends StatelessWidget {
  const _ProfileHeader({
    required this.name,
    required this.username,
    required this.year,
    required this.isDark,
    required this.surface,
    required this.border,
  });
  final String name;
  final String? username;
  final int? year;
  final bool isDark;
  final Color surface;
  final Color border;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.all(18.w),
        decoration: BoxDecoration(
          color: surface,
          border: Border.all(color: border),
          borderRadius: BorderRadius.circular(12.r),
        ),
        child: Row(children: [
          Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(name,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontSize: 17.sp,
                      fontWeight: FontWeight.w700,
                      letterSpacing: -.2)),
              SizedBox(height: 2.h),
              Text(
                  [
                    if (username?.isNotEmpty == true) '@$username',
                    'Joined ${year ?? 2023}',
                  ].join(' · '),
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(fontSize: 13.sp, color: AppColors.grey)),
            ]),
          ),
        ]),
      );
}

// ─────────────────────────────────────────────────────
//  STATS ROW
// ─────────────────────────────────────────────────────

class _StatsRow extends StatelessWidget {
  const _StatsRow({
    required this.lessonsCompleted,
    required this.problemsSolved,
    required this.surface,
    required this.border,
  });
  final int lessonsCompleted;
  final int problemsSolved;
  final Color surface;
  final Color border;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.symmetric(horizontal: 0, vertical: 14.h),
        decoration: BoxDecoration(
          color: surface,
          border: Border.all(color: border),
          borderRadius: BorderRadius.circular(12.r),
        ),
        child: IntrinsicHeight(
          child: Row(children: [
            _statCell(
                value: '7',
                label: 'Day streak',
                context: context,
                onTap: () => AppRouter.push(AppRouter.activity)),
            VerticalDivider(width: 1, thickness: 1, color: border),
            _statCell(
                value: '$lessonsCompleted', label: 'Lessons', context: context),
            VerticalDivider(width: 1, thickness: 1, color: border),
            _statCell(
                value: '$problemsSolved', label: 'Solved', context: context),
          ]),
        ),
      );

  Widget _statCell({
    required String value,
    required String label,
    required BuildContext context,
    VoidCallback? onTap,
  }) =>
      Expanded(
        child: GestureDetector(
          onTap: onTap,
          behavior: HitTestBehavior.opaque,
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            Text(value,
                style: Theme.of(context)
                    .textTheme
                    .bodyLarge
                    ?.copyWith(fontSize: 18.sp, fontWeight: FontWeight.w700)),
            SizedBox(height: 2.h),
            Text(label,
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(fontSize: 11.sp, color: AppColors.grey)),
          ]),
        ),
      );
}

// ─────────────────────────────────────────────────────
//  BADGES ROW
// ─────────────────────────────────────────────────────

class _BadgesRow extends StatelessWidget {
  const _BadgesRow({
    required this.surface,
    required this.border,
    required this.isDark,
  });
  final Color surface;
  final Color border;
  final bool isDark;

  @override
  Widget build(BuildContext context) => Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => AppRouter.push(AppRouter.badges),
          borderRadius: BorderRadius.circular(12.r),
          child: Container(
            padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 14.h),
            decoration: BoxDecoration(
              color: surface,
              border: Border.all(color: border),
              borderRadius: BorderRadius.circular(12.r),
            ),
            child: Row(children: [
              Icon(Icons.workspace_premium_rounded,
                  size: 20.sp,
                  color: isDark ? Colors.white60 : const Color(0xff5A6069)),
              SizedBox(width: 10.w),
              Text('Badges',
                  style: Theme.of(context)
                      .textTheme
                      .bodyLarge
                      ?.copyWith(fontSize: 14.sp, fontWeight: FontWeight.w600)),
              SizedBox(width: 8.w),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 3.h),
                decoration: BoxDecoration(
                  color: isDark
                      ? Colors.white.withValues(alpha: .07)
                      : const Color(0xffF4F5F7),
                  borderRadius: BorderRadius.circular(6.r),
                ),
                child: Text('3 / 12',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontSize: 11.sp,
                        fontWeight: FontWeight.w600,
                        color: AppColors.grey)),
              ),
              const Spacer(),
              Icon(Icons.chevron_right_rounded,
                  size: 18.sp, color: AppColors.grey),
            ]),
          ),
        ),
      );
}

// ─────────────────────────────────────────────────────
//  COURSE ROW
// ─────────────────────────────────────────────────────

class _CourseRow extends StatelessWidget {
  const _CourseRow({
    required this.course,
    required this.label,
    required this.onTap,
    required this.surface,
    required this.border,
  });
  final CourseModel course;
  final String label;
  final VoidCallback onTap;
  final Color surface;
  final Color border;

  @override
  Widget build(BuildContext context) => Material(
      color: Colors.transparent,
      child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12.r),
          child: Container(
              padding: EdgeInsets.all(15.w),
              decoration: BoxDecoration(
                color: surface,
                border: Border.all(color: border),
                borderRadius: BorderRadius.circular(12.r),
              ),
              child: Row(children: [
                Expanded(
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                      Text(label,
                          style: Theme.of(context)
                              .textTheme
                              .bodyMedium
                              ?.copyWith(
                                  fontSize: 11.sp,
                                  color: AppColors.grey,
                                  fontWeight: FontWeight.w500)),
                      SizedBox(height: 3.h),
                      Text(course.title ?? '',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context)
                              .textTheme
                              .bodyLarge
                              ?.copyWith(
                                  fontSize: 14.sp, fontWeight: FontWeight.w600))
                    ])),
                Icon(Icons.chevron_right_rounded,
                    size: 18.sp, color: AppColors.grey),
              ]))));
}

// ─────────────────────────────────────────────────────
//  EMPTY STATE
// ─────────────────────────────────────────────────────

class _EmptyState extends StatelessWidget {
  const _EmptyState({
    this.onTap,
    required this.surface,
    required this.border,
  });
  final VoidCallback? onTap;
  final Color surface;
  final Color border;

  @override
  Widget build(BuildContext context) => Container(
      padding: EdgeInsets.all(17.w),
      decoration: BoxDecoration(
        color: surface,
        border: Border.all(color: border),
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('No courses started yet',
            style: Theme.of(context)
                .textTheme
                .bodyLarge
                ?.copyWith(fontSize: 14.sp, fontWeight: FontWeight.w600)),
        SizedBox(height: 4.h),
        Text('Pick a course to begin tracking progress.',
            style: Theme.of(context)
                .textTheme
                .bodyMedium
                ?.copyWith(fontSize: 12.sp, color: AppColors.grey)),
        SizedBox(height: 14.h),
        SizedBox(
          width: double.infinity,
          child: TextButton(
              onPressed: onTap,
              style: TextButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: AppColors.appBlue,
                padding: EdgeInsets.symmetric(vertical: 12.h),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.r)),
              ),
              child: const Text('Browse courses',
                  style: TextStyle(fontWeight: FontWeight.w600))),
        ),
      ]));
}
