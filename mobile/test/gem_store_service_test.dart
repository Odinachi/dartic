import 'package:dartcoder/services/gem_store_service.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('GemStoreService.gemsForProduct', () {
    test('reads the amount from dartic_gems_<n> product ids', () {
      expect(GemStoreService.gemsForProduct('dartic_gems_10'), 10);
      expect(GemStoreService.gemsForProduct('dartic_gems_100'), 100);
    });

    test('handles Google Play base-plan suffixes', () {
      expect(GemStoreService.gemsForProduct('dartic_gems_25:base'), 25);
    });

    test('returns null for products that are not gem packs', () {
      expect(GemStoreService.gemsForProduct('dartic_pro_monthly'), isNull);
    });
  });
}
