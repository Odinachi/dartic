import 'package:dartcoder/features/authetication/models/user_model.dart';
import 'package:dartcoder/features/authetication/models/user_progress.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

part 'app_state.dart';

class AppCubit extends Cubit<AppState> {
  AppCubit({required this.firebaseServices}) : super(AuthInitial());
  final FirebaseServices firebaseServices;

  UserModel? profile;
  UserProgressModel? userProgress;
  void signIn(
    bool isGoogle,
  ) async {
    emit(AuthLoading());

    final auth = isGoogle
        ? await firebaseServices.signInWithGoogle()
        : await firebaseServices.signInWithApple();

    if (auth.account != null) {
      final existingProfile = (await firebaseServices.getProfile()).user;
      if (existingProfile != null) {
        profile = existingProfile;
        if (existingProfile.currentLevel != null &&
            existingProfile.username != null &&
            existingProfile.username!.trim().isNotEmpty) {
          userProgress = (await firebaseServices.getUserProgress()).progress;
          emit(AuthSuccessful());
        } else {
          emit(AuthProfileMissing());
        }
      } else {
        profile = UserModel(
          uid: FirebaseAuth.instance.currentUser?.uid,
          firstName: auth.givenName ?? "",
          lastName: auth.familyName ?? "",
          email: FirebaseAuth.instance.currentUser?.email,
          photoUrl: FirebaseAuth.instance.currentUser?.photoURL,
          createdAt: DateTime.now(),
        );
        emit(AuthProfileMissing());
      }
    } else {
      emit(AuthError(auth.error ?? "Sign in failed"));
    }
  }

  void signOut() async {
    await firebaseServices.signOut();
    emit(AuthLogout());
  }

  void getUserProfile() async {
    if (FirebaseAuth.instance.currentUser == null) {
      return;
    }
    emit(AuthLoading());
    profile = (await firebaseServices.getProfile()).user;
    if (profile?.currentLevel != null &&
        profile?.username != null &&
        profile!.username!.trim().isNotEmpty) {
      userProgress = (await firebaseServices.getUserProgress()).progress;
      emit(AuthProfileExists());
    } else {
      emit(AuthProfileMissing());
    }
  }

  void deleteAccount() async {
    emit(AuthLoading());
    final result = await firebaseServices.deleteAccount();

    if (result.deleted == true) {
      emit(AuthLogout());
    } else {
      emit(AuthError(result.error ?? "Account deletion failed"));
    }
  }

  Future<({bool isAvailable, String? error})> checkUsernameAvailability(
      String username) async {
    return await firebaseServices.checkUsernameAvailability(username);
  }

  void updateUsername(String username) async {
    emit(AuthLoading());
    final cleanUsername = username.trim();
    final availability =
        await firebaseServices.checkUsernameAvailability(cleanUsername);
    if (!availability.isAvailable) {
      emit(AuthError(availability.error ?? "Username is already taken"));
      return;
    }

    final result = await firebaseServices.updateUsername(cleanUsername);
    if (result.success == true) {
      profile = (await firebaseServices.getProfile()).user;
      userProgress = (await firebaseServices.getUserProgress()).progress;
      emit(AuthProfileCreated());
    } else {
      emit(AuthError(result.error ?? "Failed to update username"));
    }
  }

  void createProfile({
    required String firstName,
    required String lastName,
    required String username,
    String? currentLevel,
  }) async {
    emit(AuthLoading());
    final cleanUsername = username.trim();
    final availability =
        await firebaseServices.checkUsernameAvailability(cleanUsername);
    if (!availability.isAvailable) {
      emit(AuthError(availability.error ?? "Username is already taken"));
      return;
    }

    final result = await firebaseServices.saveProfile(UserModel(
        uid: FirebaseAuth.instance.currentUser?.uid ?? '',
        firstName: firstName.trim(),
        lastName: lastName.trim(),
        username: cleanUsername,
        createdAt: profile?.createdAt ?? DateTime.now(),
        currentLevel: currentLevel ?? profile?.currentLevel,
        photoUrl:
            profile?.photoUrl ?? FirebaseAuth.instance.currentUser?.photoURL,
        email: FirebaseAuth.instance.currentUser?.email ?? ''));
    if (result.success == true) {
      profile = (await firebaseServices.getProfile()).user;
      userProgress = (await firebaseServices.getUserProgress()).progress;
      emit(AuthProfileCreated());
    } else {
      emit(AuthError(result.error ?? "Profile creation failed"));
    }
  }

  void updatePassedCourses(num id) async {
    if (FirebaseAuth.instance.currentUser == null) {
      return;
    }
    if (userProgress?.passedCourses?.contains(id) == true) {
      return;
    }
    userProgress = (userProgress ?? UserProgressModel())
        .copyWith(passedCourses: [...?userProgress?.passedCourses, id]);
    emit(AuthInitial());
    await firebaseServices.updatePassedCourses(id);
  }

  void updateCurrentCourse(num id) async {
    if (FirebaseAuth.instance.currentUser == null) {
      return;
    }
    if (userProgress == null) {
      userProgress = UserProgressModel(
        currentCourse: id,
      );
    } else {
      userProgress = userProgress?.copyWith(currentCourse: id);
    }

    emit(AuthInitial());
    await firebaseServices.updateCurrentCourse(id);
  }

  void markProblemAsSolved(String id) async {
    if (userProgress?.passedDsa?.contains(id) == true) {
      return;
    }
    if (userProgress == null) {
      userProgress = UserProgressModel(
        passedDsa: [id],
      );
    } else {
      userProgress =
          userProgress?.copyWith(passedDsa: [...?userProgress?.passedDsa, id]);
    }
    await firebaseServices.markProblemAsSolved(id);
    emit(AppUpdateProgress());
  }
}
