import 'package:dartcoder/features/courses/models/course_model.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'dsa_course_state.dart';

class DsaCourseCubit extends Cubit<DsaCourseState> {
  final FirebaseServices firebaseServices;

  DsaCourseCubit({required this.firebaseServices}) : super(DsaCourseInitial());

  List<CourseModel> courses = [];

  /// Courses grouped by their `section` field, in the order they arrive.
  Map<String, List<CourseModel>> get groupedCourses {
    final grouped = <String, List<CourseModel>>{};
    for (final course in courses) {
      grouped.putIfAbsent(course.section ?? "", () => []).add(course);
    }
    return grouped;
  }

  Future<void> fetchCourses({bool isRefresh = false}) async {
    if (state is DsaCourseLoading) return;
    if (state is DsaCourseLoaded && !isRefresh) return;

    emit(DsaCourseLoading());
    final result = await firebaseServices.fetchDsaCourses();

    if (result.error != null) {
      emit(DsaCourseError(message: result.error!));
    } else {
      courses = result.courses ?? [];
      emit(DsaCourseLoaded());
    }
  }
}
