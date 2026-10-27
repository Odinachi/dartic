import 'dart:io' show Platform;

import 'package:dartcoder/features/authetication/models/user_model.dart';
import 'package:dartcoder/features/authetication/models/user_progress.dart';
import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:dartcoder/features/wallet/view_model/wallet_cubit.dart';
import 'package:dartcoder/features/wallet/views/gem_widgets.dart';
import 'package:dartcoder/main.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:url_launcher/url_launcher.dart';

const _appStoreUrl = 'https://apps.apple.com/app/id6744124202';
const _playStoreUrl =
    'https://play.google.com/store/apps/details?id=com.odibillz.dartcoder';
const _supportEmail = 'odinachidavid@yahoo.com';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key, this.onDiveIn});

  /// Opens the course list (used by the "start learning" prompts).
  final VoidCallback? onDiveIn;

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  void initState() {
    super.initState();
    if (FirebaseAuth.instance.currentUser != null) {
      final wallet = context.read<WalletCubit>();
      if (wallet.state.wallet == null) wallet.load();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isGuest = FirebaseAuth.instance.currentUser == null;

    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          centerTitle: false,
          title: Text(AppString.profile,
              style: context.text.titleLarge?.copyWith(
                  fontSize: 22.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: -.4)),
        ),
        body: BlocBuilder<AppCubit, AppState>(builder: (context, _) {
          final cubit = context.read<AppCubit>();
          final progress = _Progress.from(cubit.userProgress);

          return ListView(
            padding: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 32.h),
            children: [
              FadeSlideIn(
                child: isGuest
                    ? const _GuestCard()
                    : _Header(user: cubit.profile, email: FirebaseAuth.instance.currentUser?.email),
              ),
              if (!isGuest) ...[
                SizedBox(height: 14.h),
                FadeSlideIn(
                    delay: FadeSlideIn.stagger(1), child: const _GemsCard()),
              ],
              SizedBox(height: 14.h),
              FadeSlideIn(
                delay: FadeSlideIn.stagger(2),
                child: _ContinueCard(progress: progress, onBrowse: widget.onDiveIn),
              ),
              _SectionTitle('Your progress'),
              FadeSlideIn(
                  delay: FadeSlideIn.stagger(3),
                  child: _ProgressCard(progress: progress)),
              _SectionTitle('Milestones'),
              FadeSlideIn(
                  delay: FadeSlideIn.stagger(4),
                  child: _Milestones(progress: progress)),
              _SectionTitle('Settings'),
              const _SettingsCard(),
              _SectionTitle('Help & about'),
              const _AboutCard(),
              if (!isGuest) ...[
                _SectionTitle('Account'),
                const _AccountCard(),
              ],
              SizedBox(height: 18.h),
              Center(
                child: Text('Dartic · Learn Dart by writing it',
                    style: context.text.bodySmall?.copyWith(
                        fontSize: 11.5.sp, color: context.palette.textMuted)),
              ),
            ],
          );
        }),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  PROGRESS DATA (all real, from the user's progress doc)
// ─────────────────────────────────────────────────────

class _Progress {
  _Progress({
    required this.sections,
    required this.lessonsDone,
    required this.lessonsTotal,
    required this.problemsSolved,
    required this.current,
    required this.next,
  });

  /// Dart course modules: name, lessons passed, lessons in module.
  final List<({String name, int done, int total})> sections;
  final int lessonsDone;
  final int lessonsTotal;
  final int problemsSolved;
  final CourseModel? current;
  final CourseModel? next;

  factory _Progress.from(UserProgressModel? p) {
    final passed = {...?p?.passedCourses};
    final sections = [
      for (final entry in AppData.courses.entries)
        (
          name: entry.key,
          done: entry.value.where((c) => passed.contains(c.id)).length,
          total: entry.value.length,
        ),
    ];
    final all = AppData.courses.values.expand((c) => c).toList();
    final current = all.where((c) => c.id == p?.currentCourse).firstOrNull;
    final next = current == null
        ? null
        : all.where((c) => c.id == (current.id ?? 0) + 1).firstOrNull;
    return _Progress(
      sections: sections,
      lessonsDone: all.where((c) => passed.contains(c.id)).length,
      lessonsTotal: all.length,
      problemsSolved: p?.passedDsa?.length ?? 0,
      current: current,
      next: next,
    );
  }
}

// ─────────────────────────────────────────────────────
//  HEADER
// ─────────────────────────────────────────────────────

class _Header extends StatelessWidget {
  const _Header({required this.user, this.email});
  final UserModel? user;
  final String? email;

  static const _months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final name =
        '${user?.firstName ?? ''} ${user?.lastName ?? ''}'.trim();
    final joined = user?.createdAt;

    return AppCard(
      padding: EdgeInsets.all(18.w),
      child: Row(
        children: [
          _Avatar(name: name, photoUrl: user?.photoUrl),
          SizedBox(width: 14.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name.isEmpty ? 'Dart learner' : name,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: context.text.titleLarge?.copyWith(
                        fontSize: 19.sp,
                        fontWeight: FontWeight.w700,
                        letterSpacing: -.3)),
                SizedBox(height: 2.h),
                Text(
                  user?.username?.isNotEmpty == true
                      ? '@${user!.username}'
                      : (email ?? ''),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: context.text.bodyMedium?.copyWith(
                      fontSize: 13.5.sp, color: palette.textMuted),
                ),
                SizedBox(height: 10.h),
                Wrap(
                  spacing: 6.w,
                  runSpacing: 6.h,
                  children: [
                    if (user?.currentLevel?.isNotEmpty == true)
                      _Chip(
                          icon: Icons.school_rounded,
                          label: user!.currentLevel!,
                          color: AppColors.appBlue),
                    if (joined != null)
                      _Chip(
                          icon: Icons.calendar_today_rounded,
                          label:
                              'Since ${_months[joined.month - 1]} ${joined.year}',
                          color: palette.textMuted),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Avatar extends StatelessWidget {
  const _Avatar({required this.name, this.photoUrl});
  final String name;
  final String? photoUrl;

  @override
  Widget build(BuildContext context) {
    final initials = name
        .split(RegExp(r'\s+'))
        .where((p) => p.isNotEmpty)
        .take(2)
        .map((p) => p[0].toUpperCase())
        .join();
    final size = 64.w;
    return Container(
      width: size,
      height: size,
      padding: const EdgeInsets.all(2.5),
      decoration: const BoxDecoration(
          shape: BoxShape.circle, gradient: AppColors.primaryGradient),
      child: ClipOval(
        child: Container(
          color: context.palette.surfaceAlt,
          alignment: Alignment.center,
          child: photoUrl?.isNotEmpty == true
              ? Image.network(photoUrl!,
                  width: size,
                  height: size,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => _initials(context, initials))
              : _initials(context, initials),
        ),
      ),
    );
  }

  Widget _initials(BuildContext context, String initials) => Text(
        initials.isEmpty ? 'D' : initials,
        style: context.text.titleLarge
            ?.copyWith(fontSize: 22.sp, fontWeight: FontWeight.w700),
      );
}

class _Chip extends StatelessWidget {
  const _Chip({required this.icon, required this.label, required this.color});
  final IconData icon;
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) => Container(
        padding: EdgeInsets.symmetric(horizontal: 9.w, vertical: 4.h),
        decoration: BoxDecoration(
          color: color.withValues(alpha: .12),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 12.sp, color: color),
            SizedBox(width: 4.w),
            Text(label,
                style: context.text.bodySmall?.copyWith(
                    fontSize: 11.5.sp,
                    fontWeight: FontWeight.w600,
                    color: color)),
          ],
        ),
      );
}

class _GuestCard extends StatelessWidget {
  const _GuestCard();

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return AppCard(
      padding: EdgeInsets.all(18.w),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const _Avatar(name: ''),
              SizedBox(width: 14.w),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Learning as a guest',
                        style: context.text.titleLarge?.copyWith(
                            fontSize: 18.sp, fontWeight: FontWeight.w700)),
                    SizedBox(height: 3.h),
                    Text('Progress stays on this device only.',
                        style: context.text.bodyMedium?.copyWith(
                            fontSize: 13.sp, color: palette.textMuted)),
                  ],
                ),
              ),
            ],
          ),
          SizedBox(height: 14.h),
          Text(
            'Sign in to sync progress across devices, unlock the data structures '
            'course and algorithm practice, and get ${GemRules.welcomeBonus} free gems.',
            style: context.text.bodyMedium
                ?.copyWith(fontSize: 13.5.sp, height: 1.45),
          ),
          SizedBox(height: 14.h),
          _PrimaryButton(
            label: 'Sign in',
            onTap: () => AppRouter.pushAndClear(AppRouter.onboarding),
          ),
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  GEMS
// ─────────────────────────────────────────────────────

class _GemsCard extends StatelessWidget {
  const _GemsCard();

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return BlocBuilder<WalletCubit, WalletState>(builder: (context, state) {
      final wallet = state.wallet;
      return AppCard(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 44.w,
                  height: 44.w,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: const Color(0xff8B7CFF).withValues(alpha: .14),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: GemIcon(size: 24.sp),
                ),
                SizedBox(width: 12.w),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        wallet == null ? '–' : '${wallet.gems}',
                        style: context.text.titleLarge?.copyWith(
                            fontSize: 24.sp,
                            fontWeight: FontWeight.w700,
                            height: 1.1),
                      ),
                      Text(
                        wallet?.gems == 1 ? 'gem' : 'gems',
                        style: context.text.bodySmall?.copyWith(
                            fontSize: 12.5.sp, color: palette.textMuted),
                      ),
                    ],
                  ),
                ),
                if (wallet != null)
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('${wallet.unlocked.length}',
                          style: context.text.titleMedium?.copyWith(
                              fontWeight: FontWeight.w700)),
                      Text('solutions unlocked',
                          style: context.text.bodySmall?.copyWith(
                              fontSize: 11.5.sp, color: palette.textMuted)),
                    ],
                  ),
              ],
            ),
            SizedBox(height: 12.h),
            Text(
              'Spend ${GemRules.solutionCost} gem to unlock a solution. '
              'Unlocked solutions stay unlocked.',
              style: context.text.bodySmall?.copyWith(
                  fontSize: 12.5.sp, height: 1.4, color: palette.textMuted),
            ),
            SizedBox(height: 12.h),
            Row(
              children: [
                if (gemStore.isAvailable) ...[
                  Expanded(
                    child: _PrimaryButton(
                        label: 'Get gems', onTap: () => showGemStore(context)),
                  ),
                  SizedBox(width: 10.w),
                ],
                Expanded(
                  child: _SecondaryButton(
                      label: 'How gems work',
                      onTap: () => showGemInfoSheet(context)),
                ),
              ],
            ),
          ],
        ),
      );
    });
  }
}

// ─────────────────────────────────────────────────────
//  CONTINUE LEARNING
// ─────────────────────────────────────────────────────

class _ContinueCard extends StatelessWidget {
  const _ContinueCard({required this.progress, this.onBrowse});
  final _Progress progress;
  final VoidCallback? onBrowse;

  @override
  Widget build(BuildContext context) {
    final current = progress.current;
    if (current == null) {
      return AppCard(
        padding: EdgeInsets.all(16.w),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Start your first lesson',
                      style: context.text.titleMedium
                          ?.copyWith(fontWeight: FontWeight.w700)),
                  SizedBox(height: 3.h),
                  Text('Your next lesson will show up here.',
                      style: context.text.bodySmall?.copyWith(
                          fontSize: 12.5.sp, color: context.palette.textMuted)),
                ],
              ),
            ),
            SizedBox(width: 12.w),
            SizedBox(
                width: 110.w,
                child: _PrimaryButton(label: 'Browse', onTap: onBrowse)),
          ],
        ),
      );
    }
    void open(CourseModel c) => AppRouter.push(AppRouter.courseDetails,
        arg: CourseDetailsArgs(course: c));

    return AppCard(
      padding: EdgeInsets.zero,
      child: Column(
        children: [
          _LessonTile(
              label: 'Continue',
              course: current,
              highlight: true,
              onTap: () => open(current)),
          if (progress.next != null) ...[
            Divider(height: 1, color: context.palette.border),
            _LessonTile(
                label: 'Up next',
                course: progress.next!,
                onTap: () => open(progress.next!)),
          ],
        ],
      ),
    );
  }
}

class _LessonTile extends StatelessWidget {
  const _LessonTile(
      {required this.label,
      required this.course,
      required this.onTap,
      this.highlight = false});
  final String label;
  final CourseModel course;
  final VoidCallback onTap;
  final bool highlight;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return Pressable(
      onTap: onTap,
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 14.h),
        child: Row(
          children: [
            Container(
              width: 38.w,
              height: 38.w,
              decoration: BoxDecoration(
                gradient: highlight ? AppColors.primaryGradient : null,
                color: highlight ? null : palette.surfaceAlt,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                highlight ? Icons.play_arrow_rounded : Icons.menu_book_rounded,
                size: 20.sp,
                color: highlight ? AppColors.white : palette.textMuted,
              ),
            ),
            SizedBox(width: 12.w),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(label.toUpperCase(),
                      style: context.text.bodySmall?.copyWith(
                          fontSize: 10.5.sp,
                          letterSpacing: .6,
                          fontWeight: FontWeight.w600,
                          color: palette.textMuted)),
                  SizedBox(height: 2.h),
                  Text(course.title ?? '',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: context.text.titleMedium?.copyWith(
                          fontSize: 15.sp, fontWeight: FontWeight.w600)),
                ],
              ),
            ),
            Icon(Icons.chevron_right_rounded,
                size: 20.sp, color: palette.textMuted),
          ],
        ),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  PROGRESS
// ─────────────────────────────────────────────────────

class _ProgressCard extends StatelessWidget {
  const _ProgressCard({required this.progress});
  final _Progress progress;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final pct = progress.lessonsTotal == 0
        ? 0
        : (progress.lessonsDone * 100 / progress.lessonsTotal).round();
    return AppCard(
      padding: EdgeInsets.all(16.w),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: _Stat(
                    value: '${progress.lessonsDone}/${progress.lessonsTotal}',
                    label: 'Dart lessons'),
              ),
              Container(width: 1, height: 34.h, color: palette.border),
              Expanded(
                child: _Stat(
                    value: '${progress.problemsSolved}',
                    label: 'Problems solved'),
              ),
              Container(width: 1, height: 34.h, color: palette.border),
              Expanded(child: _Stat(value: '$pct%', label: 'Course done')),
            ],
          ),
          SizedBox(height: 16.h),
          for (final s in progress.sections) ...[
            _SectionBar(name: s.name, done: s.done, total: s.total),
            if (s != progress.sections.last) SizedBox(height: 12.h),
          ],
        ],
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat({required this.value, required this.label});
  final String value;
  final String label;

  @override
  Widget build(BuildContext context) => Column(
        children: [
          Text(value,
              style: context.text.titleLarge
                  ?.copyWith(fontSize: 18.sp, fontWeight: FontWeight.w700)),
          SizedBox(height: 2.h),
          Text(label,
              textAlign: TextAlign.center,
              style: context.text.bodySmall?.copyWith(
                  fontSize: 11.sp, color: context.palette.textMuted)),
        ],
      );
}

class _SectionBar extends StatelessWidget {
  const _SectionBar(
      {required this.name, required this.done, required this.total});
  final String name;
  final int done;
  final int total;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final value = total == 0 ? 0.0 : done / total;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Text(name,
                style: context.text.bodyMedium
                    ?.copyWith(fontSize: 13.5.sp, fontWeight: FontWeight.w600)),
            const Spacer(),
            Text(done == total && total > 0 ? 'Complete' : '$done of $total',
                style: context.text.bodySmall?.copyWith(
                    fontSize: 12.sp,
                    fontWeight: done == total && total > 0
                        ? FontWeight.w700
                        : null,
                    color: done == total && total > 0
                        ? AppColors.success
                        : palette.textMuted)),
          ],
        ),
        SizedBox(height: 6.h),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: TweenAnimationBuilder<double>(
            tween: Tween(begin: 0, end: value),
            duration: const Duration(milliseconds: 700),
            curve: Curves.easeOutCubic,
            builder: (_, v, __) => LinearProgressIndicator(
              value: v,
              minHeight: 7.h,
              backgroundColor: palette.surfaceAlt,
              valueColor: const AlwaysStoppedAnimation(AppColors.appBlue),
            ),
          ),
        ),
      ],
    );
  }
}

// ─────────────────────────────────────────────────────
//  MILESTONES (computed from real progress)
// ─────────────────────────────────────────────────────

class _Milestones extends StatelessWidget {
  const _Milestones({required this.progress});
  final _Progress progress;

  @override
  Widget build(BuildContext context) {
    final basics = progress.sections.firstOrNull;
    final items = <({IconData icon, String title, int value, int goal, Color color})>[
      (icon: Icons.flag_rounded, title: 'First lesson', value: progress.lessonsDone, goal: 1, color: AppColors.appBlue),
      (icon: Icons.local_library_rounded, title: '10 lessons', value: progress.lessonsDone, goal: 10, color: AppColors.violet),
      if (basics != null)
        (icon: Icons.foundation_rounded, title: '${basics.name} done', value: basics.done, goal: basics.total, color: AppColors.teal),
      (icon: Icons.bolt_rounded, title: 'First solve', value: progress.problemsSolved, goal: 1, color: AppColors.orange),
      (icon: Icons.psychology_rounded, title: '10 solves', value: progress.problemsSolved, goal: 10, color: AppColors.amber),
      (icon: Icons.emoji_events_rounded, title: 'Dart graduate', value: progress.lessonsDone, goal: progress.lessonsTotal, color: AppColors.success),
    ];
    items.sort((a, b) {
      final aDone = a.value >= a.goal, bDone = b.value >= b.goal;
      return aDone == bDone ? 0 : (aDone ? -1 : 1);
    });

    return SizedBox(
      height: 128.h,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        clipBehavior: Clip.none,
        itemCount: items.length,
        separatorBuilder: (_, __) => SizedBox(width: 10.w),
        itemBuilder: (context, i) {
          final m = items[i];
          final earned = m.goal > 0 && m.value >= m.goal;
          final palette = context.palette;
          return Container(
            width: 116.w,
            padding: EdgeInsets.all(12.w),
            decoration: BoxDecoration(
              color: palette.surface,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                  color: earned ? m.color.withValues(alpha: .5) : palette.border),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 34.w,
                  height: 34.w,
                  decoration: BoxDecoration(
                    color: earned
                        ? m.color.withValues(alpha: .16)
                        : palette.surfaceAlt,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(earned ? m.icon : Icons.lock_rounded,
                      size: 18.sp,
                      color: earned ? m.color : palette.textMuted),
                ),
                const Spacer(),
                Text(m.title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: context.text.bodyMedium?.copyWith(
                        fontSize: 13.sp,
                        fontWeight: FontWeight.w700,
                        color: earned ? null : palette.textMuted)),
                SizedBox(height: 2.h),
                Text(
                  earned
                      ? 'Earned'
                      : '${m.value.clamp(0, m.goal)} / ${m.goal}',
                  style: context.text.bodySmall?.copyWith(
                      fontSize: 11.5.sp,
                      color: earned ? m.color : palette.textMuted,
                      fontWeight: earned ? FontWeight.w600 : null),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

// ─────────────────────────────────────────────────────
//  SETTINGS, HELP, ACCOUNT
// ─────────────────────────────────────────────────────

class _SettingsCard extends StatelessWidget {
  const _SettingsCard();

  @override
  Widget build(BuildContext context) {
    return _Group(children: [
      ValueListenableBuilder<bool>(
        valueListenable: isDarkTheme,
        builder: (context, dark, _) => _Tile(
          icon: dark ? Icons.dark_mode_rounded : Icons.light_mode_rounded,
          title: 'Dark mode',
          onTap: () => isDarkTheme.value = !dark,
          trailing: Switch.adaptive(
            value: dark,
            activeTrackColor: AppColors.appBlue,
            onChanged: (v) => isDarkTheme.value = v,
          ),
        ),
      ),
    ]);
  }
}

class _AboutCard extends StatelessWidget {
  const _AboutCard();

  Future<void> _open(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    return _Group(children: [
      _Tile(
        icon: Icons.mail_outline_rounded,
        title: 'Contact support',
        subtitle: 'Questions, bugs or ideas',
        onTap: () => _open('mailto:$_supportEmail?subject=Dartic%20support'),
      ),
      _Tile(
        icon: Icons.star_outline_rounded,
        title: 'Rate Dartic',
        subtitle: 'It really helps',
        onTap: () => _open(Platform.isIOS ? _appStoreUrl : _playStoreUrl),
      ),
      _Tile(
        icon: Icons.privacy_tip_outlined,
        title: 'Privacy policy',
        onTap: () => _open(AppLinks.privacy),
      ),
      _Tile(
        icon: Icons.description_outlined,
        title: 'Terms of service',
        onTap: () => _open(AppLinks.terms),
      ),
    ]);
  }
}

class _AccountCard extends StatelessWidget {
  const _AccountCard();

  @override
  Widget build(BuildContext context) {
    return _Group(children: [
      _Tile(
        icon: Icons.logout_rounded,
        title: 'Sign out',
        onTap: () => AppRouter.showConfirmation(
          'Sign out of Dartic? Your progress and gems stay safe in your account.',
          onConfirm: () {
            context.read<AppCubit>().signOut();
          },
        ),
      ),
      _Tile(
        icon: Icons.delete_outline_rounded,
        title: 'Delete account',
        subtitle: 'Permanently removes your account and gems',
        destructive: true,
        onTap: () => AppRouter.showConfirmation(
          'Delete your account? Your profile and gems will be permanently '
          'deleted, including unlocked solutions and any gems you bought. '
          'This can\'t be undone.',
          onConfirm: () {
            context.read<AppCubit>().deleteAccount();
          },
        ),
      ),
    ]);
  }
}

class _Group extends StatelessWidget {
  const _Group({required this.children});
  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return AppCard(
      padding: EdgeInsets.zero,
      child: Column(
        children: [
          for (var i = 0; i < children.length; i++) ...[
            children[i],
            if (i < children.length - 1)
              Divider(
                  height: 1,
                  indent: 56.w,
                  color: context.palette.border),
          ],
        ],
      ),
    );
  }
}

class _Tile extends StatelessWidget {
  const _Tile({
    required this.icon,
    required this.title,
    required this.onTap,
    this.subtitle,
    this.trailing,
    this.destructive = false,
  });

  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback onTap;
  final Widget? trailing;
  final bool destructive;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final color = destructive ? AppColors.red : palette.textPrimary;
    return Pressable(
      onTap: onTap,
      scale: .99,
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 12.h),
        child: Row(
          children: [
            Container(
              width: 30.w,
              height: 30.w,
              decoration: BoxDecoration(
                color: (destructive ? AppColors.red : AppColors.appBlue)
                    .withValues(alpha: .1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon,
                  size: 17.sp,
                  color: destructive ? AppColors.red : AppColors.appBlue),
            ),
            SizedBox(width: 12.w),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title,
                      style: context.text.bodyLarge?.copyWith(
                          fontSize: 15.sp,
                          fontWeight: FontWeight.w600,
                          color: color)),
                  if (subtitle != null)
                    Text(subtitle!,
                        style: context.text.bodySmall?.copyWith(
                            fontSize: 12.sp, color: palette.textMuted)),
                ],
              ),
            ),
            trailing ??
                Icon(Icons.chevron_right_rounded,
                    size: 20.sp, color: palette.textMuted),
          ],
        ),
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
        padding: EdgeInsets.fromLTRB(4.w, 26.h, 4.w, 10.h),
        child: Text(text,
            style: context.text.titleMedium?.copyWith(
                fontSize: 16.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: -.2)),
      );
}

class _PrimaryButton extends StatelessWidget {
  const _PrimaryButton({required this.label, this.onTap});
  final String label;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Pressable(
        onTap: onTap,
        child: Container(
          height: 42.h,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            gradient: AppColors.primaryGradient,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(label,
              style: context.text.bodyMedium?.copyWith(
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w700,
                  color: AppColors.white)),
        ),
      );
}

class _SecondaryButton extends StatelessWidget {
  const _SecondaryButton({required this.label, this.onTap});
  final String label;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Pressable(
        onTap: onTap,
        child: Container(
          height: 42.h,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: context.palette.surfaceAlt,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(label,
              style: context.text.bodyMedium?.copyWith(
                  fontSize: 14.sp, fontWeight: FontWeight.w600)),
        ),
      );
}
