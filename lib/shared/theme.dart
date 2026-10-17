import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

const _fontFamily = "SpaceGrotesk";

final ThemeData lightTheme = _buildTheme(Brightness.light);
final ThemeData darkTheme = _buildTheme(Brightness.dark);

ThemeData _buildTheme(Brightness brightness) {
  final isDark = brightness == Brightness.dark;
  final palette = isDark ? AppPalette.dark : AppPalette.light;
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.appBlue,
    brightness: brightness,
  ).copyWith(
    primary: AppColors.appBlue,
    onPrimary: AppColors.white,
    secondary: AppColors.violet,
    surface: palette.background,
    onSurface: palette.textPrimary,
    error: AppColors.red,
  );

  final textTheme = TextTheme(
    displaySmall: TextStyle(
        color: palette.textPrimary,
        fontWeight: FontWeight.w700,
        letterSpacing: -.8),
    headlineSmall: TextStyle(
        color: palette.textPrimary,
        fontWeight: FontWeight.w700,
        letterSpacing: -.4),
    titleLarge: TextStyle(
        color: palette.textPrimary,
        fontWeight: FontWeight.w700,
        letterSpacing: -.3),
    titleMedium:
        TextStyle(color: palette.textPrimary, fontWeight: FontWeight.w600),
    bodyLarge: TextStyle(color: palette.textPrimary),
    bodyMedium: TextStyle(color: palette.textPrimary),
    bodySmall: TextStyle(color: palette.textMuted),
    labelLarge:
        TextStyle(color: palette.textPrimary, fontWeight: FontWeight.w600),
  ).apply(fontFamily: _fontFamily);

  final inputBorder = OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: BorderSide(color: palette.border),
  );

  return ThemeData(
    useMaterial3: true,
    brightness: brightness,
    fontFamily: _fontFamily,
    colorScheme: scheme,
    primaryColor: isDark ? Colors.blueGrey : AppColors.appBlue,
    scaffoldBackgroundColor: palette.background,
    canvasColor: palette.background,
    secondaryHeaderColor: isDark ? AppColors.black : null,
    dividerColor: palette.border,
    splashFactory: InkSparkle.splashFactory,
    extensions: [palette],
    textTheme: textTheme,
    iconTheme: const IconThemeData(color: Colors.white),
    pageTransitionsTheme: const PageTransitionsTheme(builders: {
      TargetPlatform.android: FadeForwardsPageTransitionsBuilder(),
      TargetPlatform.iOS: CupertinoPageTransitionsBuilder(),
      TargetPlatform.macOS: CupertinoPageTransitionsBuilder(),
    }),
    appBarTheme: AppBarTheme(
      backgroundColor: palette.background,
      foregroundColor: palette.textPrimary,
      centerTitle: true,
      elevation: 0,
      scrolledUnderElevation: 0,
      surfaceTintColor: Colors.transparent,
      titleTextStyle: TextStyle(
          color: palette.textPrimary,
          fontFamily: _fontFamily,
          fontSize: 18,
          fontWeight: FontWeight.w700,
          letterSpacing: -.2),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.appBlue,
        foregroundColor: AppColors.white,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: const TextStyle(
            fontFamily: _fontFamily, fontWeight: FontWeight.w700),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: palette.surface,
      border: inputBorder,
      enabledBorder: inputBorder,
      focusedBorder: inputBorder.copyWith(
          borderSide: const BorderSide(color: AppColors.appBlue, width: 1.5)),
    ),
    tabBarTheme: TabBarThemeData(
      labelColor: isDark ? AppColors.white : AppColors.appBlue,
      unselectedLabelColor: palette.textMuted,
      indicator: const UnderlineTabIndicator(
        borderSide: BorderSide(color: AppColors.appBlue, width: 2),
      ),
    ),
    snackBarTheme: SnackBarThemeData(
      behavior: SnackBarBehavior.floating,
      backgroundColor: isDark ? AppColors.white : AppColors.blackText,
      contentTextStyle: TextStyle(
          fontFamily: _fontFamily,
          color: isDark ? AppColors.blackText : AppColors.white,
          fontWeight: FontWeight.w500),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
    ),
    bottomSheetTheme: BottomSheetThemeData(
      backgroundColor: palette.background,
      surfaceTintColor: Colors.transparent,
      showDragHandle: true,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
    ),
    dialogTheme: DialogThemeData(
      backgroundColor: palette.background,
      surfaceTintColor: Colors.transparent,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
    ),
    progressIndicatorTheme: ProgressIndicatorThemeData(
      color: AppColors.appBlue,
      linearTrackColor: palette.surfaceAlt,
      circularTrackColor: palette.surfaceAlt,
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: palette.background,
      surfaceTintColor: Colors.transparent,
      indicatorColor: AppColors.appBlue.withValues(alpha: .16),
      height: 68,
      iconTheme: WidgetStateProperty.resolveWith((states) => IconThemeData(
          color: states.contains(WidgetState.selected)
              ? AppColors.appBlue
              : palette.textMuted)),
      labelTextStyle: WidgetStateProperty.resolveWith((states) => TextStyle(
          fontFamily: _fontFamily,
          fontSize: 12,
          fontWeight: states.contains(WidgetState.selected)
              ? FontWeight.w600
              : FontWeight.w500,
          color: states.contains(WidgetState.selected)
              ? palette.textPrimary
              : palette.textMuted)),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: palette.surface,
      side: BorderSide(color: palette.border),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(100)),
      labelStyle: TextStyle(
          fontFamily: _fontFamily,
          color: palette.textPrimary,
          fontWeight: FontWeight.w600),
    ),
  );
}

class AppColors {
  static const appBlue = Color(0xff359EFF);
  static const appBlueDeep = Color(0xff1F6FEB);
  static const violet = Color(0xff7C5CFF);
  static const teal = Color(0xff14B8A6);
  static const emerald = Color(0xff15805C);
  static const orange = Color(0xffFF6B35);
  static const amber = Color(0xffF9A825);

  static const white = Colors.white;
  static const black = Colors.black;
  static const grey = Colors.grey;
  static const blackText = Color(0xff121727);
  static const appGrey = Color(0xff111C22);

  static const red = Color(0xffFF3D00);

  static const green = Colors.green;
  static const success = Color(0xff22C55E);

  static const easy = Color(0xff22C55E);
  static const medium = Color(0xffF59E0B);
  static const hard = Color(0xffEF4444);

  static const primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xff359EFF), Color(0xff5B6CFF), Color(0xff7C5CFF)],
  );

  static const dsaGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xff10B981), Color(0xff0E9F8E), Color(0xff15805C)],
  );

  static const dataStructureGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xffFF8A3D), Color(0xffFF6B35), Color(0xffE5484D)],
  );

  static Color difficulty(String? difficulty) {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return easy;
      case 'medium':
        return medium;
      case 'hard':
        return hard;
      default:
        return grey;
    }
  }
}

/// Brightness-aware surface colors. Read with `context.palette`.
@immutable
class AppPalette extends ThemeExtension<AppPalette> {
  const AppPalette({
    required this.background,
    required this.surface,
    required this.surfaceAlt,
    required this.border,
    required this.textPrimary,
    required this.textMuted,
    required this.shadow,
  });

  final Color background;
  final Color surface;
  final Color surfaceAlt;
  final Color border;
  final Color textPrimary;
  final Color textMuted;
  final Color shadow;

  static const light = AppPalette(
    background: Color(0xffF7F8FA),
    surface: Colors.white,
    surfaceAlt: Color(0xffF0F2F5),
    border: Color(0xffE6E9EE),
    textPrimary: AppColors.blackText,
    textMuted: Color(0xff6B7280),
    shadow: Color(0x0F121727),
  );

  static const dark = AppPalette(
    background: AppColors.appGrey,
    surface: Color(0xff17242C),
    surfaceAlt: Color(0xff1E2D36),
    border: Color(0x14FFFFFF),
    textPrimary: AppColors.white,
    textMuted: Color(0xff8D9BA5),
    shadow: Color(0x40000000),
  );

  @override
  AppPalette copyWith({
    Color? background,
    Color? surface,
    Color? surfaceAlt,
    Color? border,
    Color? textPrimary,
    Color? textMuted,
    Color? shadow,
  }) =>
      AppPalette(
        background: background ?? this.background,
        surface: surface ?? this.surface,
        surfaceAlt: surfaceAlt ?? this.surfaceAlt,
        border: border ?? this.border,
        textPrimary: textPrimary ?? this.textPrimary,
        textMuted: textMuted ?? this.textMuted,
        shadow: shadow ?? this.shadow,
      );

  @override
  AppPalette lerp(AppPalette? other, double t) {
    if (other == null) return this;
    return AppPalette(
      background: Color.lerp(background, other.background, t)!,
      surface: Color.lerp(surface, other.surface, t)!,
      surfaceAlt: Color.lerp(surfaceAlt, other.surfaceAlt, t)!,
      border: Color.lerp(border, other.border, t)!,
      textPrimary: Color.lerp(textPrimary, other.textPrimary, t)!,
      textMuted: Color.lerp(textMuted, other.textMuted, t)!,
      shadow: Color.lerp(shadow, other.shadow, t)!,
    );
  }
}

extension AppThemeContext on BuildContext {
  AppPalette get palette =>
      Theme.of(this).extension<AppPalette>() ??
      (Theme.of(this).brightness == Brightness.dark
          ? AppPalette.dark
          : AppPalette.light);

  TextTheme get text => Theme.of(this).textTheme;

  bool get isDark => Theme.of(this).brightness == Brightness.dark;
}
