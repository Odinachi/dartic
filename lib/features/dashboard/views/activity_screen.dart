import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class ActivityScreen extends StatelessWidget {
  const ActivityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final surface =
        isDark ? Colors.white.withValues(alpha: .05) : Colors.white;
    final border =
        isDark ? Colors.white.withValues(alpha: .07) : const Color(0xffEAECEF);

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new_rounded, size: 18.sp),
          onPressed: () => AppRouter.pop(),
        ),
        title: Text('Activity',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontSize: 18.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: -.2)),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.fromLTRB(20.w, 10.h, 20.w, 40.h),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // ── Streak summary ──
          _StreakRow(surface: surface, border: border, isDark: isDark),
          SizedBox(height: 28.h),

          // ── Contributions ──
          Text('Contributions',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontSize: 17.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: -.2)),
          SizedBox(height: 3.h),
          Text('142 in the last 6 months',
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(fontSize: 13.sp, color: AppColors.grey)),
          SizedBox(height: 13.h),
          _Heatmap(surface: surface, border: border, isDark: isDark),

          SizedBox(height: 30.h),

          // ── Leaderboard ──
          Row(children: [
            Text('Leaderboard',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    fontSize: 17.sp,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -.2)),
            const Spacer(),
            Text('Sep 7 – 13',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontSize: 12.sp, color: AppColors.grey)),
          ]),
          SizedBox(height: 12.h),
          _Leaderboard(surface: surface, border: border, isDark: isDark),
        ]),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  STREAK ROW
// ─────────────────────────────────────────────────────

class _StreakRow extends StatelessWidget {
  const _StreakRow({
    required this.surface,
    required this.border,
    required this.isDark,
  });
  final Color surface;
  final Color border;
  final bool isDark;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.all(18.w),
        decoration: BoxDecoration(
          color: surface,
          border: Border.all(color: border),
          borderRadius: BorderRadius.circular(12.r),
        ),
        child: Row(children: [
          Icon(Icons.local_fire_department_rounded,
              color: const Color(0xffFF6B35), size: 28.sp),
          SizedBox(width: 14.w),
          Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('7 day streak',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontSize: 18.sp,
                      fontWeight: FontWeight.w700,
                      letterSpacing: -.2)),
              SizedBox(height: 2.h),
              Text('Personal best: 18 days',
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
//  HEATMAP
// ─────────────────────────────────────────────────────

class _Heatmap extends StatelessWidget {
  const _Heatmap({
    required this.surface,
    required this.border,
    required this.isDark,
  });
  final Color surface;
  final Color border;
  final bool isDark;

  static const _months = [
    ('Jan', 4),
    ('Feb', 4),
    ('Mar', 4),
    ('Apr', 4),
    ('May', 4),
    ('Jun', 4),
    ('Jul', 5),
    ('Aug', 4),
    ('Sep', 4),
    ('Oct', 4),
    ('Nov', 4),
    ('Dec', 5),
  ];

  static final List<int> _levels = List.generate(364, (i) {
    final week = i ~/ 7;
    final day = i % 7;
    if (day == 0 || day == 6) {
      return (i * 7 + week * 3) % 5 == 0 ? 1 : 0;
    }
    final val = (i * 13 + week * 7 + day * 3) % 10;
    if (val > 7) return 4;
    if (val > 5) return 3;
    if (val > 3) return 2;
    if (val > 1) return 1;
    return 0;
  });

  Color _color(int level) => level == 0
      ? (isDark ? const Color(0xff38413F) : const Color(0xffE6E9E8))
      : const [
          Color(0xffB8D9C6),
          Color(0xff7CBB99),
          Color(0xff3A916B),
          Color(0xff075D3B),
        ][level - 1];

  @override
  Widget build(BuildContext context) {
    final cellWidth = 10.w;
    final cellHeight = 10.h;
    final spacingW = 3.w;
    final spacingH = 3.h;
    final columnWidth = cellWidth + spacingW;
    final rowHeight = cellHeight + spacingH;

    return Container(
      padding: EdgeInsets.all(14.w),
      decoration: BoxDecoration(
        color: surface,
        border: Border.all(color: border),
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: EdgeInsets.only(top: 18.h),
                child: SizedBox(
                  height: 7 * rowHeight - spacingH,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('Mon',
                          style: TextStyle(
                              fontSize: 9.sp, color: AppColors.grey)),
                      Text('Wed',
                          style: TextStyle(
                              fontSize: 9.sp, color: AppColors.grey)),
                      Text('Fri',
                          style: TextStyle(
                              fontSize: 9.sp, color: AppColors.grey)),
                    ],
                  ),
                ),
              ),
              SizedBox(width: 8.w),
              Expanded(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: _months.map((m) {
                          return SizedBox(
                            width: m.$2 * columnWidth,
                            child: Text(
                              m.$1,
                              style: TextStyle(
                                fontSize: 10.sp,
                                fontWeight: FontWeight.w500,
                                color: AppColors.grey,
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                      SizedBox(height: 6.h),
                      SizedBox(
                        width: 52 * columnWidth - spacingW,
                        height: 7 * rowHeight - spacingH,
                        child: GridView.builder(
                          scrollDirection: Axis.horizontal,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: 364,
                          gridDelegate:
                              SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 7,
                            mainAxisSpacing: spacingW,
                            crossAxisSpacing: spacingH,
                          ),
                          itemBuilder: (_, index) => DecoratedBox(
                            decoration: BoxDecoration(
                              color: _color(_levels[index]),
                              borderRadius: BorderRadius.circular(2.r),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
          SizedBox(height: 14.h),
          Row(
            children: [
              Text('Less',
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(fontSize: 11.sp, color: AppColors.grey)),
              const Spacer(),
              ...List.generate(
                5,
                (index) => Container(
                  margin: EdgeInsets.only(left: 4.w),
                  width: 9.r,
                  height: 9.r,
                  decoration: BoxDecoration(
                    color: _color(index),
                    borderRadius: BorderRadius.circular(1.r),
                  ),
                ),
              ),
              SizedBox(width: 5.w),
              Text('More',
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(fontSize: 11.sp, color: AppColors.grey)),
            ],
          ),
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  LEADERBOARD
// ─────────────────────────────────────────────────────

class _Leaderboard extends StatelessWidget {
  const _Leaderboard({
    required this.surface,
    required this.border,
    required this.isDark,
  });
  final Color surface;
  final Color border;
  final bool isDark;

  static const _entries = [
    ('Liam O.', 48, 'LO'),
    ('Amina K.', 41, 'AK'),
    ('Ethan W.', 37, 'EW'),
    ('You', 22, 'YO'),
  ];

  @override
  Widget build(BuildContext context) => Container(
        decoration: BoxDecoration(
          color: surface,
          border: Border.all(color: border),
          borderRadius: BorderRadius.circular(12.r),
        ),
        child: Column(
            children: List.generate(_entries.length, (index) {
          final entry = _entries[index];
          final isYou = entry.$1 == 'You';
          return Column(children: [
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 13.h),
              child: Row(children: [
                SizedBox(
                  width: 22.w,
                  child: Text('${index + 1}',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontSize: 13.sp,
                          fontWeight: FontWeight.w600,
                          color: AppColors.grey)),
                ),
                Container(
                  width: 30.r,
                  height: 30.r,
                  decoration: BoxDecoration(
                    color: isYou
                        ? AppColors.appBlue
                        : (isDark
                            ? Colors.white.withValues(alpha: .08)
                            : const Color(0xffF0F2F4)),
                    shape: BoxShape.circle,
                  ),
                  alignment: Alignment.center,
                  child: Text(entry.$3,
                      style: TextStyle(
                          fontSize: 10.sp,
                          color: isYou
                              ? Colors.white
                              : (isDark
                                  ? Colors.white60
                                  : AppColors.blackText),
                          fontWeight: FontWeight.w600)),
                ),
              SizedBox(width: 10.w),
                Expanded(
                  child: Text(entry.$1,
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          fontSize: 14.sp,
                          fontWeight:
                              isYou ? FontWeight.w700 : FontWeight.w500)),
                ),
                Text('${entry.$2}',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontSize: 14.sp, fontWeight: FontWeight.w700)),
                SizedBox(width: 4.w),
                Text('acts',
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(fontSize: 11.sp, color: AppColors.grey)),
              ]),
            ),
            if (index < _entries.length - 1)
              Divider(
                  height: 1,
                  indent: 15.w,
                  endIndent: 15.w,
                  color: border),
          ]);
        })),
      );
}
