import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class CoursesListScreen extends StatefulWidget {
  const CoursesListScreen({super.key, this.title});
  final String? title;

  @override
  State<CoursesListScreen> createState() => _CoursesListScreenState();
}

class _CoursesListScreenState extends State<CoursesListScreen> {
  final coursesMap = AppData.courses;

  static const _moduleColors = [
    AppColors.appBlue,
    AppColors.violet,
    AppColors.orange,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: true,
        title: Text(widget.title ?? AppString.dartCourse),
      ),
      body: BlocBuilder<AppCubit, AppState>(builder: (context, _) {
        final progress = context.read<AppCubit>().userProgress;
        final passed = progress?.passedCourses?.toSet() ?? const {};
        final currentId = progress?.currentCourse;
        final modules = coursesMap.entries.toList();

        return ListView.builder(
          padding: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 32.h),
          itemCount: modules.length,
          itemBuilder: (_, m) {
            final module = modules[m];
            final color = _moduleColors[m % _moduleColors.length];
            final doneCount =
                module.value.where((c) => passed.contains(c.id)).length;
            return FadeSlideIn(
              delay: FadeSlideIn.stagger(m, stepMs: 90),
              child: Padding(
                padding: EdgeInsets.only(bottom: 24.h),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _ModuleHeader(
                      index: m + 1,
                      title: module.key,
                      done: doneCount,
                      total: module.value.length,
                      color: color,
                    ),
                    SizedBox(height: 14.h),
                    for (var i = 0; i < module.value.length; i++)
                      _LessonTile(
                        course: module.value[i],
                        number: i + 1,
                        color: color,
                        isDone: passed.contains(module.value[i].id),
                        isCurrent: module.value[i].id == currentId,
                        isLast: i == module.value.length - 1,
                        onTap: () {
                          AppRouter.push(AppRouter.courseDetails,
                              arg: CourseDetailsArgs(course: module.value[i]));
                        },
                      ),
                  ],
                ),
              ),
            );
          },
        );
      }),
    );
  }
}

class _ModuleHeader extends StatelessWidget {
  const _ModuleHeader({
    required this.index,
    required this.title,
    required this.done,
    required this.total,
    required this.color,
  });
  final int index;
  final String title;
  final int done;
  final int total;
  final Color color;

  @override
  Widget build(BuildContext context) => AppCard(
        padding: EdgeInsets.all(14.r),
        child: Row(children: [
          ProgressRing(
            value: total == 0 ? 0 : done / total,
            size: 46.r,
            stroke: 4.r,
            color: color,
            child: Text('$index',
                style: context.text.titleMedium
                    ?.copyWith(fontSize: 15.sp, color: color)),
          ),
          SizedBox(width: 14.w),
          Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('MODULE $index',
                  style: context.text.labelLarge?.copyWith(
                      fontSize: 10.sp,
                      letterSpacing: 1,
                      color: context.palette.textMuted)),
              SizedBox(height: 2.h),
              Text(title,
                  style: context.text.titleLarge?.copyWith(fontSize: 18.sp)),
            ]),
          ),
          Tag('$done/$total', color: done == total ? AppColors.success : color),
        ]),
      );
}

class _LessonTile extends StatelessWidget {
  const _LessonTile({
    required this.course,
    required this.number,
    required this.color,
    required this.isDone,
    required this.isCurrent,
    required this.isLast,
    required this.onTap,
  });
  final CourseModel course;
  final int number;
  final Color color;
  final bool isDone;
  final bool isCurrent;
  final bool isLast;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final nodeColor = isDone ? AppColors.success : color;
    return IntrinsicHeight(
      child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        // Timeline rail
        SizedBox(
          width: 32.r,
          child: Column(children: [
            SizedBox(height: 16.h),
            Container(
              width: 28.r,
              height: 28.r,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isDone || isCurrent
                    ? nodeColor
                    : nodeColor.withValues(alpha: .12),
                boxShadow: isCurrent
                    ? [
                        BoxShadow(
                          color: nodeColor.withValues(alpha: .45),
                          blurRadius: 12,
                        ),
                      ]
                    : null,
              ),
              alignment: Alignment.center,
              child: isDone
                  ? Icon(Icons.check_rounded,
                      size: 16.sp, color: AppColors.white)
                  : Text('$number',
                      style: context.text.labelLarge?.copyWith(
                          fontSize: 12.sp,
                          color: isCurrent ? AppColors.white : nodeColor)),
            ),
            if (!isLast)
              Expanded(
                child: Container(
                  width: 2,
                  margin: EdgeInsets.only(top: 4.h),
                  decoration: BoxDecoration(
                    color: isDone
                        ? AppColors.success.withValues(alpha: .5)
                        : palette.border,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
          ]),
        ),
        SizedBox(width: 12.w),
        Expanded(
          child: Padding(
            padding: EdgeInsets.only(bottom: 10.h),
            child: AppCard(
              onTap: onTap,
              padding: EdgeInsets.fromLTRB(14.w, 12.h, 10.w, 12.h),
              borderColor: isCurrent ? color.withValues(alpha: .6) : null,
              child: Row(children: [
                Expanded(
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(children: [
                          Flexible(
                            child: Text(course.title ?? '',
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: context.text.titleMedium
                                    ?.copyWith(fontSize: 14.5.sp)),
                          ),
                          if (isCurrent) ...[
                            SizedBox(width: 8.w),
                            Tag('Up next', color: color),
                          ],
                        ]),
                        SizedBox(height: 4.h),
                        Text(course.desc ?? '',
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: context.text.bodySmall
                                ?.copyWith(fontSize: 12.sp, height: 1.4)),
                        if ((course.videos?.isNotEmpty ?? false) ||
                            course.quiz != null) ...[
                          SizedBox(height: 8.h),
                          Row(children: [
                            if (course.videos?.isNotEmpty ?? false)
                              _Meta(
                                  icon: Icons.play_circle_outline_rounded,
                                  label:
                                      '${course.videos!.length} video${course.videos!.length == 1 ? '' : 's'}'),
                            if (course.quiz != null) ...[
                              SizedBox(width: 12.w),
                              const _Meta(
                                  icon: Icons.quiz_outlined, label: 'Quiz'),
                            ],
                          ]),
                        ],
                      ]),
                ),
                Icon(Icons.chevron_right_rounded,
                    size: 20.sp, color: palette.textMuted),
              ]),
            ),
          ),
        ),
      ]),
    );
  }
}

class _Meta extends StatelessWidget {
  const _Meta({required this.icon, required this.label});
  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final muted = context.palette.textMuted;
    return Row(mainAxisSize: MainAxisSize.min, children: [
      Icon(icon, size: 13.sp, color: muted),
      SizedBox(width: 4.w),
      Text(label, style: context.text.bodySmall?.copyWith(fontSize: 11.sp)),
    ]);
  }
}
