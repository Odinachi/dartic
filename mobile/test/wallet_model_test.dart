import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('WalletModel', () {
    test('fromJson reads coins and lists', () {
      final wallet = WalletModel.fromJson({
        'coins': 2,
        'unlocked': ['p1'],
        'rewarded': ['p1', 'p2'],
      });
      expect(wallet.coins, 2);
      expect(wallet.unlocked, ['p1']);
      expect(wallet.rewarded, ['p1', 'p2']);
    });

    test('fromJson tolerates missing fields and Firestore number types', () {
      final wallet = WalletModel.fromJson({'coins': 3.0});
      expect(wallet.coins, 3);
      expect(wallet.unlocked, isEmpty);
      expect(wallet.rewarded, isEmpty);
      expect(WalletModel.fromJson({}).coins, 0);
    });

    test('hasUnlocked checks the unlocked list', () {
      const wallet = WalletModel(unlocked: ['p1']);
      expect(wallet.hasUnlocked('p1'), isTrue);
      expect(wallet.hasUnlocked('p2'), isFalse);
    });

    test('canAffordSolution needs at least the solution cost', () {
      expect(const WalletModel(coins: CoinRules.solutionCost).canAffordSolution,
          isTrue);
      expect(const WalletModel(coins: 0).canAffordSolution, isFalse);
    });

    test('coin rules match firestore.rules', () {
      // firestore.rules hard-codes these; update both together.
      expect(CoinRules.welcomeBonus, 3);
      expect(CoinRules.solveReward, 1);
      expect(CoinRules.solutionCost, 1);
    });
  });
}
