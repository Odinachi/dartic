import 'package:dartcoder/services/cache_service.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/theme_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  group('app theme', () {
    test('keeps the brand blue as primary in light and dark', () {
      expect(lightTheme.colorScheme.primary, brandBlue);
      expect(darkTheme.colorScheme.primary, brandBlue);
      expect(lightTheme.colorScheme.brightness, Brightness.light);
      expect(darkTheme.colorScheme.brightness, Brightness.dark);
    });

    test('exposes the app palette in both themes', () {
      expect(lightTheme.extension<AppPalette>(), AppPalette.light);
      expect(darkTheme.extension<AppPalette>(), AppPalette.dark);
    });
  });

  group('ThemeController', () {
    final cache = CacheService();

    setUpAll(() async {
      SharedPreferences.setMockInitialValues({});
      await cache.init();
    });

    setUp(() => cache.sharedPreferences.clear());

    test('follows the system by default', () {
      expect(ThemeController(cacheService: cache).value, ThemeMode.system);
    });

    test('persists the chosen mode across restarts', () async {
      ThemeController(cacheService: cache).setThemeMode(ThemeMode.dark);
      await Future<void>.delayed(Duration.zero);

      expect(ThemeController(cacheService: cache).value, ThemeMode.dark);
    });
  });
}
