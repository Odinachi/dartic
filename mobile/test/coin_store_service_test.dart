import 'package:dartcoder/services/coin_store_service.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('CoinStoreService.coinsForProduct', () {
    test('reads the amount from dartic_coins_<n> product ids', () {
      expect(CoinStoreService.coinsForProduct('dartic_coins_10'), 10);
      expect(CoinStoreService.coinsForProduct('dartic_coins_100'), 100);
    });

    test('handles Google Play base-plan suffixes', () {
      expect(CoinStoreService.coinsForProduct('dartic_coins_25:base'), 25);
    });

    test('returns null for products that are not coin packs', () {
      expect(CoinStoreService.coinsForProduct('dartic_pro_monthly'), isNull);
    });
  });
}
