import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class BadgeModel {
  final String emoji;
  final String title;
  final String description;
  final bool isAchieved;
  final Color accentColor;

  const BadgeModel({
    required this.emoji,
    required this.title,
    required this.description,
    required this.isAchieved,
    required this.accentColor,
  });
}

class BadgesScreen extends StatelessWidget {
  const BadgesScreen({super.key});

  static const _badges = <BadgeModel>[
    // Achieved
    BadgeModel(
      emoji: '🚀',
      title: 'First Launch',
      description: 'Complete your first lesson',
      isAchieved: true,
      accentColor: Color(0xff359EFF),
    ),
    BadgeModel(
      emoji: '🔥',
      title: 'On Fire',
      description: 'Maintain a 7-day streak',
      isAchieved: true,
      accentColor: Color(0xffFF6B35),
    ),
    BadgeModel(
      emoji: '✍️',
      title: 'Code Writer',
      description: 'Write your first program in the editor',
      isAchieved: true,
      accentColor: Color(0xff15805C),
    ),
    // Locked
    BadgeModel(
      emoji: '🏆',
      title: 'Champion',
      description: 'Finish all Dart basics lessons',
      isAchieved: false,
      accentColor: Color(0xffFFD54F),
    ),
    BadgeModel(
      emoji: '🧩',
      title: 'Problem Solver',
      description: 'Solve 10 DSA problems',
      isAchieved: false,
      accentColor: Color(0xff6C3FE8),
    ),
    BadgeModel(
      emoji: '⚡',
      title: 'Speed Demon',
      description: 'Complete 5 lessons in one day',
      isAchieved: false,
      accentColor: Color(0xffF9A825),
    ),
    BadgeModel(
      emoji: '🎯',
      title: 'Perfect Score',
      description: 'Get 100% on any quiz',
      isAchieved: false,
      accentColor: Color(0xffE91E63),
    ),
    BadgeModel(
      emoji: '🌟',
      title: 'Rising Star',
      description: 'Reach the top 3 in the weekly leaderboard',
      isAchieved: false,
      accentColor: Color(0xff00BCD4),
    ),
    BadgeModel(
      emoji: '🧠',
      title: 'Deep Thinker',
      description: 'Complete all OOP lessons',
      isAchieved: false,
      accentColor: Color(0xff9C27B0),
    ),
    BadgeModel(
      emoji: '🔁',
      title: 'Loop Master',
      description: 'Complete all loop-related lessons',
      isAchieved: false,
      accentColor: Color(0xff4CAF50),
    ),
    BadgeModel(
      emoji: '📚',
      title: 'Bookworm',
      description: 'Complete 20 lessons total',
      isAchieved: false,
      accentColor: Color(0xff795548),
    ),
    BadgeModel(
      emoji: '💎',
      title: 'Dart Master',
      description: 'Complete every lesson and quiz in the app',
      isAchieved: false,
      accentColor: Color(0xff0D6ED8),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final achieved = _badges.where((b) => b.isAchieved).toList();
    final locked = _badges.where((b) => !b.isAchieved).toList();

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new_rounded, size: 18.sp),
          onPressed: () => AppRouter.pop(),
        ),
        title: Text('Badges',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontSize: 18.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: -.2)),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.fromLTRB(20.w, 10.h, 20.w, 40.h),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // ── Summary ──
          _BadgeSummary(
            achieved: achieved.length,
            total: _badges.length,
            isDark: isDark,
          ),
          SizedBox(height: 28.h),

          // ── Achieved ──
          _SectionTitle(
              title: 'Achieved',
              count: achieved.length,
              color: const Color(0xff15805C)),
          SizedBox(height: 12.h),
          ...achieved
              .map((b) => Padding(
                    padding: EdgeInsets.only(bottom: 10.h),
                    child: _BadgeCard(badge: b, isDark: isDark),
                  )),

          SizedBox(height: 22.h),

          // ── Locked ──
          _SectionTitle(
              title: 'Locked',
              count: locked.length,
              color: AppColors.grey),
          SizedBox(height: 12.h),
          ...locked
              .map((b) => Padding(
                    padding: EdgeInsets.only(bottom: 10.h),
                    child: _BadgeCard(badge: b, isDark: isDark),
                  )),
        ]),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════
//  BADGE SUMMARY
// ═══════════════════════════════════════════════════════

class _BadgeSummary extends StatelessWidget {
  const _BadgeSummary({
    required this.achieved,
    required this.total,
    required this.isDark,
  });
  final int achieved;
  final int total;
  final bool isDark;

  @override
  Widget build(BuildContext context) {
    final progress = total > 0 ? achieved / total : 0.0;
    return Container(
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20.r),
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xff6C3FE8), Color(0xff359EFF)],
        ),
        boxShadow: [
          BoxShadow(
            color: const Color(0xff6C3FE8).withValues(alpha: .30),
            blurRadius: 24,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Row(children: [
        // Progress ring
        SizedBox(
          width: 64.r,
          height: 64.r,
          child: Stack(alignment: Alignment.center, children: [
            SizedBox(
              width: 64.r,
              height: 64.r,
              child: CircularProgressIndicator(
                value: progress,
                strokeWidth: 5,
                backgroundColor: Colors.white.withValues(alpha: .18),
                valueColor:
                    const AlwaysStoppedAnimation<Color>(Color(0xffFFD54F)),
              ),
            ),
            Text('$achieved',
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 22.sp,
                    fontWeight: FontWeight.w800)),
          ]),
        ),
        SizedBox(width: 20.w),
        Expanded(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('$achieved of $total badges',
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 18.sp,
                    fontWeight: FontWeight.w700)),
            SizedBox(height: 4.h),
            Text('Keep learning to unlock more!',
                style: TextStyle(
                    color: Colors.white.withValues(alpha: .75),
                    fontSize: 13.sp)),
          ]),
        ),
      ]),
    );
  }
}

// ═══════════════════════════════════════════════════════
//  SECTION TITLE
// ═══════════════════════════════════════════════════════

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({
    required this.title,
    required this.count,
    required this.color,
  });
  final String title;
  final int count;
  final Color color;

  @override
  Widget build(BuildContext context) => Row(children: [
        Text(title,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontSize: 17.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: -.2)),
        SizedBox(width: 8.w),
        Container(
          padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 2.h),
          decoration: BoxDecoration(
            color: color.withValues(alpha: .12),
            borderRadius: BorderRadius.circular(10.r),
          ),
          child: Text('$count',
              style: TextStyle(
                  color: color,
                  fontSize: 12.sp,
                  fontWeight: FontWeight.w700)),
        ),
      ]);
}

// ═══════════════════════════════════════════════════════
//  BADGE CARD
// ═══════════════════════════════════════════════════════

class _BadgeCard extends StatelessWidget {
  const _BadgeCard({required this.badge, required this.isDark});
  final BadgeModel badge;
  final bool isDark;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.all(16.w),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16.r),
          color: isDark
              ? Colors.white.withValues(alpha: badge.isAchieved ? .06 : .03)
              : (badge.isAchieved
                  ? Colors.white
                  : const Color(0xffFAFAFA)),
          border: Border.all(
            color: badge.isAchieved
                ? badge.accentColor.withValues(alpha: .25)
                : (isDark
                    ? Colors.white.withValues(alpha: .06)
                    : AppColors.grey.withValues(alpha: .12)),
          ),
          boxShadow: [
            if (badge.isAchieved && !isDark)
              BoxShadow(
                color: badge.accentColor.withValues(alpha: .08),
                blurRadius: 12,
                offset: const Offset(0, 4),
              ),
          ],
        ),
        child: Row(children: [
          // Emoji container
          Container(
            width: 48.r,
            height: 48.r,
            decoration: BoxDecoration(
              color: badge.isAchieved
                  ? badge.accentColor.withValues(alpha: .12)
                  : (isDark
                      ? Colors.white.withValues(alpha: .05)
                      : const Color(0xffF0F0F0)),
              borderRadius: BorderRadius.circular(14.r),
            ),
            alignment: Alignment.center,
            child: Text(badge.emoji,
                style: TextStyle(
                    fontSize: 22.sp,
                    color: badge.isAchieved ? null : AppColors.grey)),
          ),
          SizedBox(width: 14.w),
          Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(badge.title,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontSize: 15.sp,
                      fontWeight: FontWeight.w700,
                      color: badge.isAchieved
                          ? null
                          : (isDark ? Colors.white38 : AppColors.grey))),
              SizedBox(height: 2.h),
              Text(badge.description,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      fontSize: 12.sp,
                      color: badge.isAchieved
                          ? AppColors.grey
                          : (isDark
                              ? Colors.white24
                              : AppColors.grey.withValues(alpha: .5)))),
            ]),
          ),
          if (badge.isAchieved)
            Container(
              width: 28.r,
              height: 28.r,
              decoration: BoxDecoration(
                color: badge.accentColor.withValues(alpha: .12),
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.check_rounded,
                  color: badge.accentColor, size: 16.sp),
            )
          else
            Icon(Icons.lock_outline_rounded,
                color: isDark
                    ? Colors.white.withValues(alpha: .15)
                    : AppColors.grey.withValues(alpha: .3),
                size: 20.sp),
        ]),
      );
}
