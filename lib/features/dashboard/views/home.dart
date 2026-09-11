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
    final surface = isDark
        ? Colors.white.withValues(alpha: .05)
        : Colors.white;
    final border = isDark
        ? Colors.white.withValues(alpha: .07)
        : const Color(0xffEAECEF);

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
                      value: '$passedCount',
                      label: 'lessons',
                      isDark: isDark),
                  SizedBox(width: 8.w),
                  _StatPill(
                      value: '$dsaSolved',
                      label: 'solved',
                      isDark: isDark),
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
                                    fontSize: 12.sp,
                                    color: AppColors.grey)),
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
      'Dart compiles ahead-of-time for fast startup and just-in-time for hot reload during development.'
    ),
    (
      'Null safety',
      'Append ? to a type to mark it nullable. Sound null safety catches null errors at compile time.'
    ),
    (
      'Cascade notation',
      'Use .. to chain method calls on the same object without repeating the variable name.'
    ),
    (
      'String interpolation',
      'Use \$variable or \${expression} inside strings instead of concatenation.'
    ),
    (
      'Extension methods',
      'Add new functionality to existing classes without modifying them or creating subclasses.'
    ),
    (
      'Named parameters',
      'Wrap parameters in {} to make them named. Add required to enforce they are provided.'
    ),
    (
      'Records',
      'Dart 3 records are lightweight, immutable tuples — great for returning multiple values from a function.'
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
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    fontSize: 13.sp,
                    fontWeight: FontWeight.w600)),
            SizedBox(height: 3.h),
            Text(tip.$2,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontSize: 12.sp,
                    color: AppColors.grey,
                    height: 1.45)),
          ]),
        ),
      ]),
    );
  }
}
