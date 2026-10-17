import 'dart:async';

import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:url_launcher/url_launcher.dart';

const _mono = TextStyle(
  fontFamily: 'Menlo',
  fontFamilyFallback: ['Courier', 'monospace'],
);

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  Future<void> _open(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final text = Theme.of(context).textTheme;

    return Scaffold(
      body: BlocBuilder<AppCubit, AppState>(builder: (context, state) {
        return Stack(
          children: [
            SafeArea(
              child: LayoutBuilder(
                builder: (context, constraints) => SingleChildScrollView(
                  padding: EdgeInsets.symmetric(horizontal: 24.w),
                  child: ConstrainedBox(
                    constraints:
                        BoxConstraints(minHeight: constraints.maxHeight),
                    child: IntrinsicHeight(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(height: 8.h),
                          FadeSlideIn(
                            child: Row(
                              children: [
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(9),
                                  child: Assets.images.appImg
                                      .image(width: 34, height: 34),
                                ),
                                const SizedBox(width: 10),
                                Text('Dartic',
                                    style: text.titleLarge?.copyWith(
                                        fontSize: 20,
                                        fontWeight: FontWeight.w700,
                                        letterSpacing: -0.4)),
                              ],
                            ),
                          ),
                          const Spacer(flex: 2),
                          SizedBox(height: 16.h),
                          FadeSlideIn(
                            delay: FadeSlideIn.stagger(1, stepMs: 90),
                            child: const _TypingEditor(),
                          ),
                          SizedBox(height: 22.h),
                          FadeSlideIn(
                            delay: FadeSlideIn.stagger(2, stepMs: 90),
                            child: Text.rich(
                              TextSpan(children: [
                                const TextSpan(text: 'Learn Dart\nby '),
                                TextSpan(
                                    text: 'writing',
                                    style: TextStyle(
                                        color: isDark
                                            ? AppColors.appBlue
                                            : AppColors.appBlueDeep)),
                                const TextSpan(text: ' it.'),
                              ]),
                              style: text.headlineLarge?.copyWith(
                                fontSize: 36.sp,
                                height: 1.02,
                                fontWeight: FontWeight.w700,
                                letterSpacing: -1.6,
                                color: palette.textPrimary,
                              ),
                            ),
                          ),
                          SizedBox(height: 10.h),
                          FadeSlideIn(
                            delay: FadeSlideIn.stagger(3, stepMs: 90),
                            child: Text(
                              AppString.onboardingLead,
                              style: text.bodyLarge?.copyWith(
                                fontSize: 15.sp,
                                height: 1.4,
                                color: palette.textMuted,
                              ),
                            ),
                          ),
                          SizedBox(height: 10.h),
                          FadeSlideIn(
                            delay: FadeSlideIn.stagger(4, stepMs: 90),
                            child: Text(
                              AppString.onboardingFacts,
                              style: _mono.copyWith(
                                fontSize: 12.sp,
                                color: palette.textMuted,
                                letterSpacing: 0.2,
                              ),
                            ),
                          ),
                          const Spacer(flex: 3),
                          SizedBox(height: 18.h),
                          FadeSlideIn(
                            delay: FadeSlideIn.stagger(5, stepMs: 90),
                            child: Column(
                              children: [
                                _AuthButton(
                                  onTap: () =>
                                      context.read<AppCubit>().signIn(false),
                                  label: AppString.continueWithApple,
                                  // Apple's guidelines: black on light, white on dark.
                                  background:
                                      isDark ? AppColors.white : AppColors.black,
                                  foreground:
                                      isDark ? AppColors.black : AppColors.white,
                                  icon: Assets.svgs.apple.svg(
                                    height: 18,
                                    width: 18,
                                    color: isDark
                                        ? AppColors.black
                                        : AppColors.white,
                                  ),
                                ),
                                SizedBox(height: 10.h),
                                _AuthButton(
                                  onTap: () =>
                                      context.read<AppCubit>().signIn(true),
                                  label: AppString.continueWithGoogle,
                                  background: palette.surface,
                                  foreground: palette.textPrimary,
                                  border: isDark
                                      ? AppColors.white.withValues(alpha: .14)
                                      : palette.border,
                                  icon: Assets.svgs.google
                                      .svg(height: 18, width: 18),
                                ),
                                SizedBox(height: 10.h),
                                Text(
                                  AppString.signInUnlocks,
                                  textAlign: TextAlign.center,
                                  style: text.bodySmall?.copyWith(
                                    fontSize: 12.5.sp,
                                    color: palette.textMuted,
                                  ),
                                ),
                                Pressable(
                                  onTap: () => AppRouter.pushAndClear(
                                      AppRouter.dashboard),
                                  child: Padding(
                                    padding: EdgeInsets.symmetric(
                                        vertical: 10.h, horizontal: 16.w),
                                    child: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Text(
                                          AppString.continueAsGuest,
                                          style: text.bodyMedium?.copyWith(
                                            fontSize: 14.5.sp,
                                            fontWeight: FontWeight.w600,
                                            color: palette.textPrimary,
                                          ),
                                        ),
                                        const SizedBox(width: 6),
                                        Icon(Icons.arrow_forward_rounded,
                                            size: 18,
                                            color: palette.textPrimary),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          SizedBox(height: 6.h),
                          Center(
                            child: Text.rich(
                              textAlign: TextAlign.center,
                              TextSpan(
                                text: AppString.byContinuing,
                                style: text.bodySmall?.copyWith(
                                  fontSize: 11.5.sp,
                                  height: 1.5,
                                  color: palette.textMuted,
                                ),
                                children: [
                                  TextSpan(
                                    text: AppString.termsOfService.trim(),
                                    recognizer: TapGestureRecognizer()
                                      ..onTap = () => _open(
                                          'https://dartcoder-d57cb.web.app/terms.html'),
                                    style: TextStyle(
                                      color: palette.textPrimary,
                                      decoration: TextDecoration.underline,
                                      decorationColor: palette.textMuted,
                                    ),
                                  ),
                                  TextSpan(text: ' ${AppString.andText}'),
                                  TextSpan(
                                    text: AppString.privacyPolicy.trim(),
                                    recognizer: TapGestureRecognizer()
                                      ..onTap = () => _open(
                                          'https://dartcoder-d57cb.web.app/privacy_policy.html'),
                                    style: TextStyle(
                                      color: palette.textPrimary,
                                      decoration: TextDecoration.underline,
                                      decorationColor: palette.textMuted,
                                    ),
                                  ),
                                  const TextSpan(text: '.'),
                                ],
                              ),
                            ),
                          ),
                          SizedBox(height: 16.h),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            if (state is AuthLoading) loadingWidget(context)
          ],
        );
      }),
    );
  }
}

/// Full-width sign-in button with a leading brand icon.
class _AuthButton extends StatelessWidget {
  const _AuthButton({
    required this.onTap,
    required this.label,
    required this.background,
    required this.foreground,
    required this.icon,
    this.border,
  });

  final VoidCallback onTap;
  final String label;
  final Color background;
  final Color foreground;
  final Color? border;
  final Widget icon;

  @override
  Widget build(BuildContext context) {
    return Pressable(
      onTap: onTap,
      child: Container(
        height: 48.h,
        width: double.infinity,
        decoration: BoxDecoration(
          color: background,
          borderRadius: BorderRadius.circular(14),
          border: border == null ? null : Border.all(color: border!),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            icon,
            const SizedBox(width: 10),
            Text(
              label,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontSize: 15.sp,
                    fontWeight: FontWeight.w600,
                    color: foreground,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

/// A tiny editor that types `print('Hello, Dart!')`, presses Run and shows
/// the output. Static when the platform asks for reduced motion.
class _TypingEditor extends StatefulWidget {
  const _TypingEditor();

  @override
  State<_TypingEditor> createState() => _TypingEditorState();
}

class _TypingEditorState extends State<_TypingEditor> {
  // Nord-style tokens, matching the in-app editor theme.
  static const _keyword = Color(0xff81A1C1);
  static const _fn = Color(0xff88C0D0);
  static const _string = Color(0xffA3BE8C);
  static const _plain = Color(0xffD8DEE9);
  static const _dim = Color(0xff616E88);

  static const _tokens = <(String, Color)>[
    ('void ', _keyword),
    ('main', _fn),
    ('() {\n  ', _plain),
    ('print', _fn),
    ('(', _plain),
    ("'Hello, Dart!'", _string),
    (');\n}', _plain),
  ];
  static final _length =
      _tokens.fold<int>(0, (sum, token) => sum + token.$1.length);

  Timer? _timer;
  int _shown = 0;
  bool _running = false;
  bool _done = false;
  bool _started = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_started) return;
    _started = true;
    if (MediaQuery.of(context).disableAnimations) {
      _shown = _length;
      _done = true;
      return;
    }
    // Wait for the entrance animation, then type at a natural pace.
    Future.delayed(const Duration(milliseconds: 650), () {
      if (!mounted) return;
      _timer = Timer.periodic(const Duration(milliseconds: 45), (t) {
        if (!mounted) return t.cancel();
        setState(() => _shown++);
        if (_shown >= _length) {
          t.cancel();
          _run();
        }
      });
    });
  }

  Future<void> _run() async {
    await Future.delayed(const Duration(milliseconds: 350));
    if (!mounted) return;
    setState(() => _running = true);
    await Future.delayed(const Duration(milliseconds: 450));
    if (!mounted) return;
    setState(() {
      _running = false;
      _done = true;
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  List<InlineSpan> _visibleSpans() {
    final spans = <InlineSpan>[];
    var left = _shown;
    for (final (text, color) in _tokens) {
      if (left <= 0) break;
      final part = text.length <= left ? text : text.substring(0, left);
      spans.add(TextSpan(text: part, style: TextStyle(color: color)));
      left -= part.length;
    }
    return spans;
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final code = _mono.copyWith(fontSize: 13.sp, height: 1.55, color: _plain);

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xff0B1216) : const Color(0xff111C22),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
            color: AppColors.white.withValues(alpha: isDark ? .08 : .04)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Title bar
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 8, 8),
            child: Row(
              children: [
                Text('main.dart',
                    style: _mono.copyWith(fontSize: 12.sp, color: _plain)),
                const Spacer(),
                AnimatedContainer(
                  duration: const Duration(milliseconds: 150),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: _running
                        ? AppColors.success.withValues(alpha: .25)
                        : AppColors.white.withValues(alpha: .06),
                    borderRadius: BorderRadius.circular(7),
                    border: Border.all(
                        color: AppColors.white.withValues(alpha: .1)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.play_arrow_rounded,
                          size: 14,
                          color: _running ? AppColors.success : _plain),
                      const SizedBox(width: 4),
                      Text(_running ? 'Running' : 'Run',
                          style: _mono.copyWith(
                              fontSize: 11.5.sp,
                              color: _running ? AppColors.success : _plain)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Divider(height: 1, color: AppColors.white.withValues(alpha: .07)),
          // Code with a blinking caret
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
            child: SizedBox(
              height: code.fontSize! * code.height! * 3,
              child: Text.rich(
                TextSpan(
                  style: code,
                  children: [
                    ..._visibleSpans(),
                    if (!_done)
                      const WidgetSpan(
                          alignment: PlaceholderAlignment.middle,
                          child: _Caret()),
                  ],
                ),
              ),
            ),
          ),
          Divider(height: 1, color: AppColors.white.withValues(alpha: .07)),
          // Console
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 10),
            child: Row(
              children: [
                Text('›', style: code.copyWith(color: _dim)),
                const SizedBox(width: 8),
                AnimatedOpacity(
                  duration: const Duration(milliseconds: 250),
                  opacity: _done ? 1 : 0,
                  child: Text('Hello, Dart!',
                      style: code.copyWith(color: _string)),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Caret extends StatefulWidget {
  const _Caret();

  @override
  State<_Caret> createState() => _CaretState();
}

class _CaretState extends State<_Caret> with SingleTickerProviderStateMixin {
  late final _blink = AnimationController(
      vsync: this, duration: const Duration(milliseconds: 1000))
    ..repeat();

  @override
  void dispose() {
    _blink.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
        animation: _blink,
        builder: (_, __) => Opacity(
          opacity: _blink.value < .5 ? 1 : 0,
          child: Container(
            width: 2,
            height: 16.sp,
            margin: const EdgeInsets.only(left: 1),
            color: AppColors.appBlue,
          ),
        ),
      );
}
