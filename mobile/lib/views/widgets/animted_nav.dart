import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class AnimatedBottomNav extends StatefulWidget {
  final bool isVisible;
  final VoidCallback onPrevious;
  final VoidCallback onEditor;
  final VoidCallback onQuiz;
  final VoidCallback onNext;

  const AnimatedBottomNav({
    super.key,
    required this.isVisible,
    required this.onPrevious,
    required this.onEditor,
    required this.onNext,
    required this.onQuiz,
  });

  @override
  State<AnimatedBottomNav> createState() => _AnimatedBottomNavState();
}

class _AnimatedBottomNavState extends State<AnimatedBottomNav> {
  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return AnimatedSlide(
      duration: const Duration(milliseconds: 450),
      curve: Curves.easeOutCubic,
      offset: widget.isVisible ? Offset.zero : const Offset(0, 1.2),
      child: AnimatedOpacity(
        duration: const Duration(milliseconds: 350),
        opacity: widget.isVisible ? 1.0 : 0.0,
        child: IgnorePointer(
          ignoring: !widget.isVisible,
          child: SafeArea(
            top: false,
            minimum: EdgeInsets.only(bottom: 12.h),
            child: Container(
              padding: EdgeInsets.all(10.r),
              decoration: BoxDecoration(
                color: palette.surface,
                borderRadius: BorderRadius.circular(22.r),
                border: Border.all(color: palette.border),
                boxShadow: [
                  BoxShadow(
                    color: palette.shadow,
                    blurRadius: 24,
                    offset: const Offset(0, 10),
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(children: [
                    Expanded(
                      child: _ActionChip(
                        icon: Icons.code_rounded,
                        label: AppString.practice,
                        color: AppColors.appBlue,
                        onTap: widget.onEditor,
                      ),
                    ),
                    SizedBox(width: 8.w),
                    Expanded(
                      child: _ActionChip(
                        icon: Icons.quiz_rounded,
                        label: AppString.takeQuiz,
                        color: AppColors.violet,
                        onTap: widget.onQuiz,
                      ),
                    ),
                  ]),
                  SizedBox(height: 8.h),
                  Row(children: [
                    Pressable(
                      onTap: widget.onPrevious,
                      child: Container(
                        width: 46.h,
                        height: 46.h,
                        decoration: BoxDecoration(
                          color: palette.surfaceAlt,
                          borderRadius: BorderRadius.circular(14.r),
                        ),
                        child: Tooltip(
                          message: AppString.previous,
                          child: Icon(Icons.arrow_back_rounded,
                              size: 20.sp, color: palette.textPrimary),
                        ),
                      ),
                    ),
                    SizedBox(width: 8.w),
                    Expanded(
                      child: AppButton(
                        onTap: widget.onNext,
                        text: AppString.nextCourse,
                      ),
                    ),
                  ]),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ActionChip extends StatelessWidget {
  const _ActionChip({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Pressable(
        onTap: onTap,
        child: Container(
          height: 42.h,
          decoration: BoxDecoration(
            color: color.withValues(alpha: .12),
            borderRadius: BorderRadius.circular(14.r),
          ),
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(icon, size: 17.sp, color: color),
            SizedBox(width: 6.w),
            Text(label,
                style: context.text.labelLarge
                    ?.copyWith(fontSize: 13.sp, color: color)),
          ]),
        ),
      );
}
