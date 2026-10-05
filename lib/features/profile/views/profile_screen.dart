import 'package:dartcoder/features/authentication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:dartcoder/main.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
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
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          actions: [
            PopupMenuButton(
              initialValue: null,
              onSelected: (v) {
                if (v == "theme") {
                  _showThemePicker();
                } else if (v == "logout") {
                  context.read<AppCubit>().signOut();
                } else if (v == "delete_account") {
                  AppRouter.showConfirmation(
                      "Are you sure you want to delete your account? This action is irreversible.",
                      onConfirm: () {
                    context.read<AppCubit>().deleteAccount();
                  });
                }
              },
              itemBuilder: (BuildContext context) => <PopupMenuEntry>[
                PopupMenuItem(
                  value: "theme",
                  child: _menuRow(
                      icon: _themeIcon(themeController.value),
                      text: "Theme: ${_themeLabel(themeController.value)}"),
                ),
                PopupMenuItem(
                  value: "logout",
                  child: _menuRow(icon: Icons.logout, text: "Logout"),
                ),
                PopupMenuItem(
                  value: "delete_account",
                  child: _menuRow(
                      icon: Icons.delete,
                      text: "Delete Account",
                      color: context.colors.error),
                ),
              ],
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20.0),
                child: Icon(
                  Icons.settings_outlined,
                  size: 20.sp,
                ),
              ),
            ),
          ],
          automaticallyImplyLeading: false,
          title: const Text(AppString.profile),
        ),
        body: BlocBuilder<AppCubit, AppState>(builder: (_, state) {
          final user = context.read<AppCubit>().profile;
          final currentCourse = courseList
              .reduce((value, element) => value + element)
              .where((e) =>
                  e.id == context.read<AppCubit>().userProgress?.currentCourse)
              .firstOrNull;

          CourseModel? nextCourse;
          if (currentCourse != null && currentCourse.id != 30) {
            nextCourse = courseList
                .reduce((value, element) => value + element)
                .where((e) => e.id == ((currentCourse.id ?? 0) + 1))
                .firstOrNull;
          }
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(height: 20.h),
              Padding(
                padding: EdgeInsets.symmetric(
                  horizontal: 40.w,
                ),
                child: FittedBox(
                  child: Text(
                      "${user?.firstName ?? ""}  ${user?.lastName ?? ""}",
                      maxLines: 1,
                      textAlign: TextAlign.center,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontSize: 23, fontWeight: FontWeight.bold)),
                ),
              ),
              Text("${AppString.joined} ${user?.createdAt?.year ?? "2023"}",
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      fontSize: 13,
                      fontWeight: FontWeight.normal,
                      color: context.colors.onSurfaceVariant)),
              SizedBox(height: 40.h),
              Padding(
                padding: EdgeInsets.only(
                  left: 20.w,
                  right: 20.w,
                ),
                child: Text(AppString.courseProgress,
                    textAlign: TextAlign.left,
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
              SizedBox(height: 20.h),
              currentCourse != null
                  ? Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        actionContainer(
                            title: currentCourse.title,
                            desc: currentCourse.desc,
                            onTap: () {
                              AppRouter.push(AppRouter.courseDetails,
                                  arg:
                                      CourseDetailsArgs(course: currentCourse));
                            }),
                        SizedBox(height: 20.h),
                        if (nextCourse != null)
                          actionContainer(
                              actionText: "Start",
                              title: nextCourse.title,
                              desc: nextCourse.desc,
                              isNext: true,
                              onTap: () {
                                AppRouter.push(AppRouter.courseDetails,
                                    arg:
                                        CourseDetailsArgs(course: nextCourse!));
                              }),
                      ],
                    )
                  : Column(
                      children: [
                        Assets.json.jumpIn.lottie(
                            height: 250.h,
                            width: double.infinity,
                            fit: BoxFit.cover),
                        SizedBox(height: 20.h),
                        Padding(
                          padding: EdgeInsets.symmetric(horizontal: 20.w),
                          child: AppButton(
                            text: AppString.diveIn,
                            onTap: widget.onDiveIn,
                          ),
                        ),
                      ],
                    )
            ],
          );
        }),
      ),
    );
  }

  Widget _menuRow(
      {required IconData icon, required String text, Color? color}) {
    return Row(
      children: [
        Icon(icon, color: color ?? context.colors.onSurface),
        Padding(
          padding: const EdgeInsets.only(left: 8.0),
          child: Text(text,
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(color: color ?? context.colors.onSurface)),
        ),
      ],
    );
  }

  static IconData _themeIcon(ThemeMode mode) => switch (mode) {
        ThemeMode.system => Icons.brightness_auto,
        ThemeMode.light => Icons.light_mode,
        ThemeMode.dark => Icons.dark_mode,
      };

  static String _themeLabel(ThemeMode mode) => switch (mode) {
        ThemeMode.system => "System",
        ThemeMode.light => "Light",
        ThemeMode.dark => "Dark",
      };

  void _showThemePicker() {
    showDialog<void>(
      context: context,
      builder: (dialogContext) => SimpleDialog(
        title: const Text("Theme"),
        children: [
          for (final mode in ThemeMode.values)
            SimpleDialogOption(
              onPressed: () {
                themeController.setThemeMode(mode);
                Navigator.of(dialogContext).pop();
              },
              child: Row(
                children: [
                  Icon(_themeIcon(mode)),
                  const SizedBox(width: 12),
                  Expanded(child: Text(_themeLabel(mode))),
                  if (themeController.value == mode)
                    Icon(Icons.check, color: dialogContext.colors.primary),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget actionContainer(
      {String? title,
      String? desc,
      VoidCallback? onTap,
      String? actionText,
      bool isNext = false}) {
    return Container(
      margin: EdgeInsets.only(bottom: 10.h, left: 20.w, right: 20.w),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10.r),
        color: context.colors.surfaceContainerLow,
        border: Border.all(color: context.colors.outlineVariant),
        boxShadow: [
          BoxShadow(
            color: context.colors.shadow.withValues(alpha: .05),
            blurRadius: 8,
            spreadRadius: 2,
            offset: const Offset(0, 4),
          ),
          BoxShadow(
            color: context.colors.shadow.withValues(alpha: .01),
            blurRadius: 4,
            spreadRadius: 1,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 10.h),
        child: ListTile(
          contentPadding: EdgeInsets.zero,
          title: Text(title ?? "",
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context)
                  .textTheme
                  .bodyLarge
                  ?.copyWith(fontSize: 18, fontWeight: FontWeight.w600)),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(desc ?? "",
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(fontSize: 12)),
              SizedBox(height: 20.h),
              SizedBox(
                width: isNext ? 80.w : 100.w,
                child: AppButton(
                  backgroundColor:
                      isNext ? context.colors.primaryContainer : null,
                  textColor: isNext ? context.colors.onPrimaryContainer : null,
                  onTap: onTap,
                  text: actionText ?? "Continue",
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
