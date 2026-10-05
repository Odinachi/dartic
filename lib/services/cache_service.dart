import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CacheService {
  static final CacheService instance = CacheService._internal();

  factory CacheService() => instance;

  CacheService._internal();

  late final SharedPreferences sharedPreferences;
  final _codeKey = "code";
  final _themeModeKey = "theme_mode";

  Future<void> init() async {
    sharedPreferences = await SharedPreferences.getInstance();
  }

  void saveCode(String code, {String? key}) async {
    await sharedPreferences.setString(key ?? _codeKey, code);
  }

  void deleteCode({String? key}) async {
    await sharedPreferences.remove(key ?? _codeKey);
  }

  String? getCode({String? key}) =>
      sharedPreferences.getString(key ?? _codeKey);

  ThemeMode getThemeMode() {
    final name = sharedPreferences.getString(_themeModeKey);
    return ThemeMode.values.where((m) => m.name == name).firstOrNull ??
        ThemeMode.system;
  }

  Future<void> saveThemeMode(ThemeMode mode) async {
    await sharedPreferences.setString(_themeModeKey, mode.name);
  }
}
