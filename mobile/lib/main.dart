import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/editor/view_model/editor_cubit.dart';
import 'package:dartcoder/firebase_options.dart';
import 'package:dartcoder/services/cache_service.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:dartcoder/services/notification_service.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/text_editor.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

final isDarkTheme = ValueNotifier<bool>(true);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  await cacheService.init();
  NotificationService().init();
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider<AppCubit>(
          create: (context) => AppCubit(firebaseServices: firebaseService),
        ),
        BlocProvider<EditorCubit>(
          create: (context) => EditorCubit(firebaseServices: firebaseService),
        ),
      ],
      child: ValueListenableBuilder(
          valueListenable: isDarkTheme,
          builder: (_, isDark, __) {
            return ScreenUtilInit(
              builder: (context, child) => MultiBlocListener(
                listeners: [
                  BlocListener<AppCubit, AppState>(listener: (_, state) {
                    if (state is AuthLogout) {
                      AppRouter.pushAndClear(AppRouter.onboarding);
                    } else if (state is AuthSuccessful) {
                      AppRouter.pushAndClear(AppRouter.dashboard);
                    } else if (state is AuthError) {
                      AppRouter.showMessage(state.message);
                    } else if (state is AuthProfileMissing) {
                      AppRouter.push(AppRouter.createProfile);
                    } else if (state is AuthProfileCreated) {
                      AppRouter.pushAndClear(AppRouter.dashboard);
                    }
                  }),
                  BlocListener<EditorCubit, EditorState>(
                    listener: (_, state) {
                      if (state is EditorError) {
                        AppRouter.showMessage(state.message);
                      }
                    },
                  ),
                ],
                child: MaterialApp(
                  navigatorKey: AppRouter.navKey,
                  themeMode: isDark ? ThemeMode.dark : ThemeMode.light,
                  theme: lightTheme,
                  darkTheme: darkTheme,
                  debugShowCheckedModeBanner: false,
                  onGenerateRoute: AppRouter.generateRoute,
                  initialRoute: FirebaseAuth.instance.currentUser != null
                      ? AppRouter.dashboard
                      : AppRouter.onboarding,
                ),
              ),
            );
          }),
    ),
  );
}

final cacheService = CacheService();
final firebaseService = FirebaseServices();
final editor = TextEditor(cacheService: cacheService);
