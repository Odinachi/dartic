import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/features/courses/views/course_details.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class CoursesListScreen extends StatefulWidget {
  const CoursesListScreen({
    super.key,
    this.title,
    this.courses,
    this.showBackButton = false,
    this.trackProgress = true,
  });
  final String? title;

  /// Courses grouped by section. Defaults to the bundled Dart course.
  final Map<String, List<CourseModel>>? courses;
  final bool showBackButton;

  /// Whether opening a course updates the user's Dart course progress.
  final bool trackProgress;

  @override
  State<CoursesListScreen> createState() => _CoursesListScreenState();
}

class _CoursesListScreenState extends State<CoursesListScreen> {
  Map<String, List<CourseModel>> get coursesMap =>
      widget.courses ?? AppData.courses;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: widget.showBackButton,
        title: Text(widget.title ?? AppString.dartCourse),
      ),
      body: Padding(
        padding: EdgeInsets.only(left: 20.w, right: 20.w, top: 20.h),
        child: SingleChildScrollView(
          child: Column(
            children: coursesMap.entries.map((e) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (e.key.isNotEmpty) ...[
                    Text(e.key,
                        style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            fontSize: 20, fontWeight: FontWeight.bold)),
                    SizedBox(height: 10.h),
                  ],
                  ListView.builder(
                      itemBuilder: (_, i) {
                        final course = e.value[i];
                        return ShadowContainer(
                          onTap: () {
                            AppRouter.push(AppRouter.courseDetails,
                                arg: CourseDetailsArgs(
                                  course: course,
                                  courses: widget.courses == null
                                      ? null
                                      : coursesMap.values
                                          .expand((e) => e)
                                          .toList(),
                                  trackProgress: widget.trackProgress,
                                ));
                          },
                          title: course.title,
                          desc: course.desc,
                        );
                      },
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: e.value.length)
                ],
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}
