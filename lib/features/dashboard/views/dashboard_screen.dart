import 'package:dartcoder/features/authentication/view_model/app_cubit.dart';
import 'package:dartcoder/features/authentication/views/onboarding_screen.dart';
import 'package:dartcoder/features/courses/views/courses_list_screen.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/features/profile/views/profile_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/features/dashboard/views/home.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  /// Screens at least this wide get a side rail instead of a bottom bar.
  static const double _railBreakpoint = 600;
  static const double _iconSize = 24;

  int _selectedIndex = 0;

  final _destinations = [
    (label: AppString.home, icon: Assets.svgs.home),
    (label: AppString.courses, icon: Assets.svgs.course),
    (label: AppString.editor, icon: Assets.svgs.editor),
    (label: AppString.profile, icon: Assets.svgs.person),
  ];

  @override
  void initState() {
    super.initState();

    context.read<AppCubit>().getUserProfile();
  }

  void _select(int index) => setState(() => _selectedIndex = index);

  Widget _page(int index) {
    switch (index) {
      case 0:
        return HomeScreen(onCourseTap: () => _select(1));
      case 1:
        return CoursesListScreen();
      case 2:
        return EditorScreen(arg: EditorScreenArg(isPractice: false));
      default:
        return FirebaseAuth.instance.currentUser != null
            ? ProfileScreen(onDiveIn: () => _select(1))
            : const OnboardingScreen();
    }
  }

  Widget _icon(SvgImage icon, Color color) => SizedBox.square(
        dimension: _iconSize,
        child: icon.svg(color: color),
      );

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final background = theme.scaffoldBackgroundColor;
    final inactive = isDark ? Colors.white70 : AppColors.grey.shade700;
    final indicator = AppColors.appBlue.withValues(alpha: 0.15);
    final labelStyle = theme.textTheme.bodyLarge?.copyWith(
      fontSize: 13,
      fontWeight: FontWeight.w600,
    );
    final page = KeyedSubtree(
      key: ValueKey(_selectedIndex),
      child: _page(_selectedIndex),
    );

    final isWide = MediaQuery.sizeOf(context).width >= _railBreakpoint;

    if (isWide) {
      return Scaffold(
        body: SafeArea(
          child: Row(
            children: [
              NavigationRail(
                selectedIndex: _selectedIndex,
                onDestinationSelected: _select,
                labelType: NavigationRailLabelType.all,
                backgroundColor: background,
                indicatorColor: indicator,
                groupAlignment: -0.8,
                selectedLabelTextStyle:
                    labelStyle?.copyWith(color: AppColors.appBlue),
                unselectedLabelTextStyle: labelStyle?.copyWith(color: inactive),
                destinations: [
                  for (final d in _destinations)
                    NavigationRailDestination(
                      icon: _icon(d.icon, inactive),
                      selectedIcon: _icon(d.icon, AppColors.appBlue),
                      label: Text(d.label),
                      padding: const EdgeInsets.symmetric(vertical: 6),
                    ),
                ],
              ),
              VerticalDivider(width: 1, color: theme.dividerColor),
              Expanded(child: page),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      body: page,
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          labelTextStyle: WidgetStateProperty.resolveWith(
            (states) => labelStyle?.copyWith(
              color: states.contains(WidgetState.selected)
                  ? AppColors.appBlue
                  : inactive,
            ),
          ),
        ),
        child: NavigationBar(
          selectedIndex: _selectedIndex,
          onDestinationSelected: _select,
          backgroundColor: background,
          surfaceTintColor: Colors.transparent,
          shadowColor: AppColors.grey.withValues(alpha: 0.2),
          elevation: 3,
          indicatorColor: indicator,
          labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
          destinations: [
            for (final d in _destinations)
              NavigationDestination(
                icon: _icon(d.icon, inactive),
                selectedIcon: _icon(d.icon, AppColors.appBlue),
                label: d.label,
              ),
          ],
        ),
      ),
    );
  }
}
