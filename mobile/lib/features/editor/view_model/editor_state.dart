part of 'editor_cubit.dart';

abstract class EditorState {}

class EditorInitial extends EditorState {}

class EditorProblem extends EditorState {
  final TestSuite? problem;
  EditorProblem({this.problem});
}

class EditorLoading extends EditorState {}
class EditorLoadingProblems extends EditorState {}

class DSAListLoaded extends EditorState {
  final bool hasMore;
  final bool isLoadingMore;
  final bool isRefreshing;

  DSAListLoaded({
    this.hasMore = true,
    this.isLoadingMore = false,
    this.isRefreshing = false,
  });
}

class EditorError extends EditorState {
  final String message;
  EditorError({required this.message});
}
