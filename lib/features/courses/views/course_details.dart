import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/courses/views/course_quiz.dart';
import 'package:dartcoder/features/courses/views/widget/video_player.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/views/widgets/animted_nav.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:markdown_widget/markdown_widget.dart';

import '../models/course_model.dart';

class CourseDetails extends StatefulWidget {
  const CourseDetails({super.key, this.arg});
  final CourseDetailsArgs? arg;

  @override
  State<CourseDetails> createState() => _CourseDetailsState();
}

class _CourseDetailsState extends State<CourseDetails> {
  final tocController = TocController();
  final scrollController = ScrollController();

  final courseNotifier = ValueNotifier(
    CourseModel(
      title: "Main",
      path: "assets/courses/main.md",
      id: 0,
    ),
  );

  void loadData(CourseModel course) async {
    await rootBundle.loadString(course.path ?? "").then((e) {
      dataStr = e;
      courseNotifier.value = course;
      showNav.value = false;
      setState(() {});
      tocController.jumpToIndex(0);
      // Reset scroll position to top when loading new data
      scrollController.animateTo(
        0,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    });
  }

  String dataStr = "";

  @override
  void initState() {
    super.initState();
    loadData(widget.arg?.course ?? courseNotifier.value);
    showNav.value = false;
  }

  @override
  void dispose() {
    scrollController.dispose();
    super.dispose();
  }

  final showNav = ValueNotifier(false);

  final courses = AppData.courses;

  late final _lastCourseId = courses.values
      .expand((e) => e)
      .map((e) => e.id ?? 0)
      .reduce((a, b) => a > b ? a : b);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
        valueListenable: courseNotifier,
        builder: (_, value, __) {
          return Scaffold(
            appBar: AppBar(
              centerTitle: true,
              title: Text(value.title ?? ""),
              bottom: PreferredSize(
                preferredSize: const Size.fromHeight(3),
                child: AnimatedBuilder(
                  animation: scrollController,
                  builder: (_, __) {
                    final position = scrollController.hasClients
                        ? scrollController.position
                        : null;
                    final max = position?.hasContentDimensions == true
                        ? position!.maxScrollExtent
                        : 0.0;
                    final read = max <= 0 ? 0.0 : position!.pixels / max;
                    return LinearProgressIndicator(
                      value: read.clamp(0.0, 1.0),
                      minHeight: 3,
                      backgroundColor: Colors.transparent,
                    );
                  },
                ),
              ),
            ),
            body: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20.0),
              child: Stack(
                children: [
                  NotificationListener(
                    onNotification: (ScrollNotification notification) {
                      if (notification is ScrollEndNotification) {
                        if (notification.metrics.pixels >=
                            notification.metrics.maxScrollExtent - 20) {
                          showNav.value = true;
                        } else {
                          showNav.value = false;
                        }
                      }
                      return true;
                    },
                    child: SingleChildScrollView(
                      controller: scrollController,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          MarkdownWidget(
                            physics: const NeverScrollableScrollPhysics(),
                            shrinkWrap: true,
                            padding: EdgeInsets.zero,
                            data: dataStr,
                            config: config,
                            tocController: tocController,
                          ),
                          SizedBox(height: 20.h),
                          if (courseNotifier.value.videos != null) ...[
                            Padding(
                              padding: EdgeInsets.only(bottom: 10.h, top: 10.h),
                              child: Column(
                                children: [
                                  Text(AppString.videos,
                                      style: Theme.of(context)
                                          .textTheme
                                          .bodyLarge
                                          ?.copyWith(
                                              fontSize: 20.sp,
                                              fontWeight: FontWeight.bold))
                                ],
                              ),
                            ),
                            ...?courseNotifier.value.videos?.map(
                              (e) => Padding(
                                padding: EdgeInsets.only(bottom: 15.h),
                                child: CustomVideoPlayer(videoUrl: e),
                              ),
                            ),
                          ],
                          SizedBox(height: 200.h),
                        ],
                      ),
                    ),
                  ),
                  ValueListenableBuilder(
                      valueListenable: showNav,
                      builder: (_, show, __) {
                        return Positioned(
                          left: 0,
                          right: 0,
                          bottom: 0,
                          child: AnimatedBottomNav(
                            onQuiz: () {
                              if (courseNotifier.value.quiz != null) {
                                AppRouter.push(
                                  AppRouter.quiz,
                                  arg: CourseQuizArg(
                                    course: courseNotifier.value,
                                  ),
                                );
                              } else {
                                AppRouter.showMessage(
                                    "No quiz available for this course");
                              }
                            },
                            isVisible: show,
                            onPrevious: () {
                              if (courseNotifier.value.id != 0) {
                                final item = courses.values
                                    .toList()
                                    .reduce((value, element) => value + element)
                                    .where((e) =>
                                        e.id == (courseNotifier.value.id! - 1))
                                    .firstOrNull;
                                if (item != null) {
                                  loadData(item);
                                  context
                                      .read<AppCubit>()
                                      .updateCurrentCourse(item.id ?? 0);
                                }
                              } else {
                                AppRouter.showMessage(
                                    "This is the first course");
                              }
                            },
                            onEditor: () {
                              AppRouter.push(AppRouter.editor,
                                  arg: EditorScreenArg(isPractice: true));
                            },
                            onNext: () {
                              if (courseNotifier.value.id != _lastCourseId) {
                                final item = courses.values
                                    .toList()
                                    .reduce((value, element) => value + element)
                                    .where((e) =>
                                        e.id == (courseNotifier.value.id! + 1))
                                    .firstOrNull;
                                if (item != null) {
                                  loadData(item);
                                  context
                                      .read<AppCubit>()
                                      .updateCurrentCourse(item.id ?? 0);
                                }
                              } else {
                                AppRouter.showMessage(
                                    "This is the last course");
                              }
                            },
                          ),
                        );
                      })
                ],
              ),
            ),
          );
        });
  }
}

class CourseDetailsArgs {
  final CourseModel course;
  CourseDetailsArgs({required this.course});
}
