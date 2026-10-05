import 'package:dartcoder/services/cache_service.dart';
import 'package:flutter/material.dart';

/// Holds the user's theme choice. Defaults to following the system setting
/// and persists any explicit choice across restarts.
class ThemeController extends ValueNotifier<ThemeMode> {
  ThemeController({required CacheService cacheService})
      : _cacheService = cacheService,
        super(cacheService.getThemeMode());

  final CacheService _cacheService;

  void setThemeMode(ThemeMode mode) {
    if (mode == value) return;
    value = mode;
    _cacheService.saveThemeMode(mode);
  }
}
