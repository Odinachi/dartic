part of 'app_cubit.dart';

abstract class AppState {}

class AuthInitial extends AppState {}

class AuthLoading extends AppState {}

class AuthSuccessful extends AppState {}

class AuthProfileExists extends AppState {}

class AuthProfileCreated extends AppState {}

class AuthProfileMissing extends AppState {}
class AppUpdateProgress extends AppState {
  final String? id;

  AppUpdateProgress({this.id});
}

class AuthLogout extends AppState {}

class AuthError extends AppState {
  final String message;

  AuthError(this.message);
}
