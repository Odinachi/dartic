import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/authetication/views/onboarding_screen.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/features/profile/views/profile_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/features/dashboard/views/home.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _index = 0;

  @override
  void initState() {
    super.initState();
    context.read<AppCubit>().getUserProfile();
  }

  void _select(int index) {
    if (index == _index) return;
    HapticFeedback.selectionClick();
    setState(() => _index = index);
  }

  @override
  Widget build(BuildContext context) {
    final isIOS = Theme.of(context).platform == TargetPlatform.iOS ||
        Theme.of(context).platform == TargetPlatform.macOS;
    return Scaffold(
      bottomNavigationBar: isIOS ? _cupertinoBar(context) : _materialBar(),
      body: IndexedStack(
        index: _index,
        children: [
          HomeScreen(
            onCourseTap: () => AppRouter.push(AppRouter.coursesList),
          ),
          EditorScreen(
            arg: EditorScreenArg(isPractice: false),
          ),
          FirebaseAuth.instance.currentUser != null
              ? ProfileScreen(
                  onDiveIn: () => AppRouter.push(AppRouter.coursesList),
                )
              : const OnboardingScreen(),
        ],
      ),
    );
  }

  Widget _cupertinoBar(BuildContext context) => CupertinoTabBar(
        currentIndex: _index,
        onTap: _select,
        activeColor: AppColors.appBlue,
        inactiveColor: context.palette.textMuted,
        backgroundColor: context.palette.background.withValues(alpha: .94),
        border:
            Border(top: BorderSide(color: context.palette.border, width: .5)),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.house),
            activeIcon: Icon(CupertinoIcons.house_fill),
            label: AppString.home,
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.chevron_left_slash_chevron_right),
            label: AppString.editor,
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.person),
            activeIcon: Icon(CupertinoIcons.person_fill),
            label: AppString.profile,
          ),
        ],
      );

  Widget _materialBar() => NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: _select,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home_rounded),
            label: AppString.home,
          ),
          NavigationDestination(
            icon: Icon(Icons.code_rounded),
            label: AppString.editor,
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline_rounded),
            selectedIcon: Icon(Icons.person_rounded),
            label: AppString.profile,
          ),
        ],
      );
}
