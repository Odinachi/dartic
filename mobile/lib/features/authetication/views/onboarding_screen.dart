import 'dart:math' as math;

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
                  // Keep content at a readable width on tablets.
                  padding: EdgeInsets.symmetric(
                      horizontal: math.max(24.w, (constraints.maxWidth - 480) / 2)),
                  child: ConstrainedBox(
                    constraints:
                        BoxConstraints(minHeight: constraints.maxHeight),
                    child: IntrinsicHeight(
                      child: Column(
                        children: [
                          const Spacer(flex: 3),
                          FadeSlideIn(
                            child: Column(
                              children: [
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(20),
                                  child: Assets.images.appImg
                                      .image(width: 80, height: 80),
                                ),
                                SizedBox(height: 28.h),
                                Text.rich(
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
                                  textAlign: TextAlign.center,
                                  style: text.headlineLarge?.copyWith(
                                    fontSize: 34.sp,
                                    height: 1.08,
                                    fontWeight: FontWeight.w700,
                                    letterSpacing: -1.2,
                                    color: palette.textPrimary,
                                  ),
                                ),
                                SizedBox(height: 12.h),
                                Text(
                                  AppString.onboardingLead,
                                  textAlign: TextAlign.center,
                                  style: text.bodyLarge?.copyWith(
                                    fontSize: 15.sp,
                                    height: 1.45,
                                    color: palette.textMuted,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const Spacer(flex: 4),
                          SizedBox(height: 24.h),
                          FadeSlideIn(
                            delay: const Duration(milliseconds: 120),
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
                                SizedBox(height: 6.h),
                                Pressable(
                                  onTap: () => AppRouter.pushAndClear(
                                      AppRouter.dashboard),
                                  child: Padding(
                                    padding: EdgeInsets.symmetric(
                                        vertical: 14.h, horizontal: 16.w),
                                    child: Text(
                                      AppString.continueAsGuest,
                                      style: text.bodyMedium?.copyWith(
                                        fontSize: 14.5.sp,
                                        fontWeight: FontWeight.w600,
                                        color: palette.textMuted,
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Text.rich(
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
                                    ..onTap = () => _open(AppLinks.terms),
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
                                    ..onTap = () => _open(AppLinks.privacy),
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
        height: 50.h,
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
