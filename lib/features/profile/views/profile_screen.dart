import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
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
                  isDarkTheme.value = !isDarkTheme.value;
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
                    child: ValueListenableBuilder(
                        valueListenable: isDarkTheme,
                        builder: (_, isDark, __) {
                          return Row(
                            children: [
                              Icon(
                                isDark ? Icons.sunny : Icons.dark_mode,
                                color:
                                    isDark ? AppColors.white : AppColors.black,
                              ),
                              Padding(
                                padding: EdgeInsets.only(left: 3.0),
                                child: Text(
                                  isDark ? "Light Theme" : "Dark Theme",
                                  style: Theme.of(context)
                                      .textTheme
                                      .bodyMedium
                                      ?.copyWith(
                                          color: isDark
                                              ? AppColors.white
                                              : AppColors.black),
                                ),
                              ),
                            ],
                          );
                        })),
                PopupMenuItem(
                  value: "logout",
                  child: Row(
                    children: [
                      Icon(
                        Icons.logout,
                        color: isDarkTheme.value
                            ? AppColors.white
                            : AppColors.black,
                      ),
                      Padding(
                        padding: EdgeInsets.only(left: 3.0),
                        child: Text(
                          "Logout",
                          style: Theme.of(context)
                              .textTheme
                              .bodyMedium
                              ?.copyWith(),
                        ),
                      )
                    ],
                  ),
                ),
                PopupMenuItem(
                  value: "delete_account",
                  child: Row(
                    children: [
                      Icon(
                        Icons.delete,
                        color: AppColors.red,
                      ),
                      Padding(
                        padding: EdgeInsets.only(left: 3.0),
                        child: Text("Delete Account",
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(color: AppColors.red)),
                      ),
                    ],
                  ),
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
              if (user?.username != null && user!.username!.isNotEmpty) ...[
                SizedBox(height: 2.h),
                Text("@${user.username!}",
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w500,
                        color: AppColors.appBlue)),
              ],
              SizedBox(height: 4.h),
              Text("${AppString.joined} ${user?.createdAt?.year ?? "2023"}",
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      fontSize: 13,
                      fontWeight: FontWeight.normal,
                      color: AppColors.grey)),
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
        color: Theme.of(context).scaffoldBackgroundColor,
        border: Border.all(color: AppColors.grey.withValues(alpha: .1)),
        boxShadow: [
          BoxShadow(
            color: AppColors.grey.withValues(alpha: .05),
            blurRadius: 8,
            spreadRadius: 2,
            offset: const Offset(0, 4),
          ),
          BoxShadow(
            color: AppColors.grey.withValues(alpha: .01),
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
                      isNext ? AppColors.appBlue.withValues(alpha: 0.2) : null,
                  textColor: isNext ? AppColors.appBlue : null,
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
