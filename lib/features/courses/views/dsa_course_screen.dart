import 'package:dartcoder/features/courses/view_model/dsa_course_cubit.dart';
import 'package:dartcoder/features/courses/views/courses_list_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

/// The Data Structure course, whose lessons come from the
/// `DSA_Course` Firestore collection.
class DsaCourseScreen extends StatefulWidget {
  const DsaCourseScreen({super.key});

  @override
  State<DsaCourseScreen> createState() => _DsaCourseScreenState();
}

class _DsaCourseScreenState extends State<DsaCourseScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DsaCourseCubit>().fetchCourses();
    });
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<DsaCourseCubit, DsaCourseState>(
      builder: (context, state) {
        final cubit = context.read<DsaCourseCubit>();

        if (state is DsaCourseLoaded && cubit.courses.isNotEmpty) {
          return CoursesListScreen(
            title: AppString.dataStructureCourse,
            courses: cubit.groupedCourses,
            showBackButton: true,
            trackProgress: false,
          );
        }

        return Scaffold(
          appBar: AppBar(title: const Text(AppString.dataStructureCourse)),
          body: Center(
            child: switch (state) {
              DsaCourseError(:final message) => _message(
                  message,
                  onRetry: () => cubit.fetchCourses(isRefresh: true),
                ),
              DsaCourseLoaded() => _message(
                  AppString.noCoursesYet,
                  onRetry: () => cubit.fetchCourses(isRefresh: true),
                ),
              _ => const CircularProgressIndicator(),
            },
          ),
        );
      },
    );
  }

  Widget _message(String text, {required VoidCallback onRetry}) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20.w),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            text,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          SizedBox(height: 15.h),
          AppButton(text: AppString.retry, onTap: onRetry),
        ],
      ),
    );
  }
}
