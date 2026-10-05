part of 'dsa_course_cubit.dart';

abstract class DsaCourseState {}

class DsaCourseInitial extends DsaCourseState {}

class DsaCourseLoading extends DsaCourseState {}

class DsaCourseLoaded extends DsaCourseState {}

class DsaCourseError extends DsaCourseState {
  final String message;
  DsaCourseError({required this.message});
}
