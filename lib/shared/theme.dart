import 'package:flutter/material.dart';

/// The Dartic brand blue. It seeds both color schemes and is kept as the
/// exact primary color in light and dark mode.
const brandBlue = Color(0xff359EFF);

const _fontFamily = "SpaceGrotesk";

final ThemeData lightTheme = buildAppTheme(Brightness.light);
final ThemeData darkTheme = buildAppTheme(Brightness.dark);

ThemeData buildAppTheme(Brightness brightness) {
  final isDark = brightness == Brightness.dark;
  final seeded = ColorScheme.fromSeed(
    seedColor: brandBlue,
    brightness: brightness,
    dynamicSchemeVariant: DynamicSchemeVariant.fidelity,
  );
  final scheme = seeded.copyWith(
    primary: brandBlue,
    onPrimary: isDark ? seeded.onPrimary : Colors.white,
  );
  final palette = isDark ? AppPalette.dark : AppPalette.light;

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    fontFamily: _fontFamily,
    scaffoldBackgroundColor: scheme.surface,
    dividerColor: scheme.outlineVariant,
    iconTheme: IconThemeData(color: scheme.onSurface),
    extensions: [palette],
    appBarTheme: AppBarTheme(
      backgroundColor: scheme.surface,
      foregroundColor: scheme.onSurface,
      centerTitle: true,
      elevation: 0,
      scrolledUnderElevation: 2,
      shadowColor: scheme.shadow.withValues(alpha: .1),
      surfaceTintColor: Colors.transparent,
      titleTextStyle: TextStyle(
        color: scheme.onSurface,
        fontFamily: _fontFamily,
        fontSize: 20,
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: scheme.primary,
        foregroundColor: scheme.onPrimary,
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide(color: scheme.outline),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide(color: scheme.outline),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide(color: scheme.primary, width: 2),
      ),
    ),
    textSelectionTheme: TextSelectionThemeData(cursorColor: scheme.primary),
    progressIndicatorTheme: ProgressIndicatorThemeData(
      color: scheme.primary,
      linearTrackColor: scheme.surfaceContainerHighest,
    ),
    tabBarTheme: TabBarThemeData(
      labelColor: scheme.primary,
      unselectedLabelColor: scheme.onSurfaceVariant,
      indicator: UnderlineTabIndicator(
        borderSide: BorderSide(color: scheme.primary, width: 2),
      ),
    ),
    popupMenuTheme: PopupMenuThemeData(
      color: scheme.surfaceContainer,
      textStyle: TextStyle(color: scheme.onSurface, fontFamily: _fontFamily),
    ),
    snackBarTheme: SnackBarThemeData(
      backgroundColor: scheme.inverseSurface,
      contentTextStyle:
          TextStyle(color: scheme.onInverseSurface, fontFamily: _fontFamily),
    ),
  );
}

/// App-specific colors that Material's [ColorScheme] has no slot for.
/// Read them with `Theme.of(context).extension<AppPalette>()!` or
/// `context.palette`.
@immutable
class AppPalette extends ThemeExtension<AppPalette> {
  const AppPalette({
    required this.success,
    required this.onSuccess,
    required this.warning,
    required this.onWarning,
    required this.codeBackground,
    required this.codeText,
    required this.codeType,
    required this.codeModifier,
    required this.codeControl,
    required this.codeObject,
    required this.codeBuiltIn,
    required this.codePunctuation,
    required this.codeNumber,
    required this.codeIdentifier,
  });

  final Color success;
  final Color onSuccess;
  final Color warning;
  final Color onWarning;

  // Syntax colors for inline code snippets in quizzes.
  final Color codeBackground;
  final Color codeText;
  final Color codeType;
  final Color codeModifier;
  final Color codeControl;
  final Color codeObject;
  final Color codeBuiltIn;
  final Color codePunctuation;
  final Color codeNumber;
  final Color codeIdentifier;

  static const light = AppPalette(
    success: Color(0xff2E7D32),
    onSuccess: Colors.white,
    warning: Color(0xffE65100),
    onWarning: Colors.white,
    codeBackground: Color(0xffEEEEEE),
    codeText: Color(0xdd000000),
    codeType: Color(0xffAA00FF),
    codeModifier: Color(0xffF57C00),
    codeControl: Color(0xff7B1FA2),
    codeObject: Color(0xff00796B),
    codeBuiltIn: Color(0xff2962FF),
    codePunctuation: Color(0xffFF8F00),
    codeNumber: Color(0xff689F38),
    codeIdentifier: Color(0xff0097A7),
  );

  static const dark = AppPalette(
    success: Color(0xff81C784),
    onSuccess: Color(0xff00390A),
    warning: Color(0xffFFB74D),
    onWarning: Color(0xff4A2800),
    codeBackground: Color(0xff2A2F36),
    codeText: Color(0xb3ffffff),
    codeType: Color(0xffE040FB),
    codeModifier: Color(0xffFFB74D),
    codeControl: Color(0xffBA68C8),
    codeObject: Color(0xff4DB6AC),
    codeBuiltIn: Color(0xff82B1FF),
    codePunctuation: Color(0xffFFD54F),
    codeNumber: Color(0xffAED581),
    codeIdentifier: Color(0xff4DD0E1),
  );

  @override
  AppPalette copyWith({
    Color? success,
    Color? onSuccess,
    Color? warning,
    Color? onWarning,
    Color? codeBackground,
    Color? codeText,
    Color? codeType,
    Color? codeModifier,
    Color? codeControl,
    Color? codeObject,
    Color? codeBuiltIn,
    Color? codePunctuation,
    Color? codeNumber,
    Color? codeIdentifier,
  }) {
    return AppPalette(
      success: success ?? this.success,
      onSuccess: onSuccess ?? this.onSuccess,
      warning: warning ?? this.warning,
      onWarning: onWarning ?? this.onWarning,
      codeBackground: codeBackground ?? this.codeBackground,
      codeText: codeText ?? this.codeText,
      codeType: codeType ?? this.codeType,
      codeModifier: codeModifier ?? this.codeModifier,
      codeControl: codeControl ?? this.codeControl,
      codeObject: codeObject ?? this.codeObject,
      codeBuiltIn: codeBuiltIn ?? this.codeBuiltIn,
      codePunctuation: codePunctuation ?? this.codePunctuation,
      codeNumber: codeNumber ?? this.codeNumber,
      codeIdentifier: codeIdentifier ?? this.codeIdentifier,
    );
  }

  @override
  AppPalette lerp(AppPalette? other, double t) {
    if (other == null) return this;
    return AppPalette(
      success: Color.lerp(success, other.success, t)!,
      onSuccess: Color.lerp(onSuccess, other.onSuccess, t)!,
      warning: Color.lerp(warning, other.warning, t)!,
      onWarning: Color.lerp(onWarning, other.onWarning, t)!,
      codeBackground: Color.lerp(codeBackground, other.codeBackground, t)!,
      codeText: Color.lerp(codeText, other.codeText, t)!,
      codeType: Color.lerp(codeType, other.codeType, t)!,
      codeModifier: Color.lerp(codeModifier, other.codeModifier, t)!,
      codeControl: Color.lerp(codeControl, other.codeControl, t)!,
      codeObject: Color.lerp(codeObject, other.codeObject, t)!,
      codeBuiltIn: Color.lerp(codeBuiltIn, other.codeBuiltIn, t)!,
      codePunctuation: Color.lerp(codePunctuation, other.codePunctuation, t)!,
      codeNumber: Color.lerp(codeNumber, other.codeNumber, t)!,
      codeIdentifier: Color.lerp(codeIdentifier, other.codeIdentifier, t)!,
    );
  }
}

extension ThemeLookup on BuildContext {
  ThemeData get theme => Theme.of(this);
  ColorScheme get colors => Theme.of(this).colorScheme;
  AppPalette get palette => Theme.of(this).extension<AppPalette>()!;
  bool get isDark => Theme.of(this).brightness == Brightness.dark;
}
