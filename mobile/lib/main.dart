import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/editor/view_model/editor_cubit.dart';
import 'package:dartcoder/features/wallet/view_model/wallet_cubit.dart';
import 'package:dartcoder/firebase_options.dart';
import 'package:dartcoder/services/cache_service.dart';
import 'package:dartcoder/services/gem_store_service.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:dartcoder/services/notification_service.dart';
import 'package:dartcoder/shared/navigation/router.dart';
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
  await gemStore.configure(uid: FirebaseAuth.instance.currentUser?.uid);
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider<AppCubit>(
          create: (context) => AppCubit(firebaseServices: firebaseService),
        ),
        BlocProvider<EditorCubit>(
          create: (context) => EditorCubit(firebaseServices: firebaseService),
        ),
        BlocProvider<WalletCubit>(
          create: (context) => WalletCubit(firebaseServices: firebaseService),
        ),
      ],
      child: ValueListenableBuilder(
          valueListenable: isDarkTheme,
          builder: (_, isDark, __) {
            return ScreenUtilInit(
              // Phones scale from the default 360×690 design. Tablets use a
              // larger design so the UI isn't blown up ~3× on an iPad.
              designSize: _isTablet ? const Size(720, 1100) : const Size(360, 690),
              minTextAdapt: _isTablet,
              builder: (context, child) => MultiBlocListener(
                listeners: [
                  BlocListener<AppCubit, AppState>(listener: (context, state) {
                    if (state is AuthLogout) {
                      context.read<WalletCubit>().reset();
                      gemStore.signOut();
                      AppRouter.pushAndClear(AppRouter.onboarding);
                    } else if (state is AuthSuccessful) {
                      context.read<WalletCubit>().reset();
                      final uid = FirebaseAuth.instance.currentUser?.uid;
                      if (uid != null) gemStore.identify(uid);
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
final gemStore = GemStoreService();

bool get _isTablet {
  final view = WidgetsBinding.instance.platformDispatcher.views.first;
  return view.physicalSize.shortestSide / view.devicePixelRatio >= 600;
}
