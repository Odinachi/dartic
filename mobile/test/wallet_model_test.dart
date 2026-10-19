import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('WalletModel', () {
    test('fromJson reads gems and lists', () {
      final wallet = WalletModel.fromJson({
        'gems': 2,
        'unlocked': ['p1'],
        'rewarded': ['p1', 'p2'],
      });
      expect(wallet.gems, 2);
      expect(wallet.unlocked, ['p1']);
      expect(wallet.rewarded, ['p1', 'p2']);
    });

    test('fromJson tolerates missing fields and Firestore number types', () {
      final wallet = WalletModel.fromJson({'gems': 3.0});
      expect(wallet.gems, 3);
      expect(wallet.unlocked, isEmpty);
      expect(wallet.rewarded, isEmpty);
      expect(WalletModel.fromJson({}).gems, 0);
    });

    test('hasUnlocked checks the unlocked list', () {
      const wallet = WalletModel(unlocked: ['p1']);
      expect(wallet.hasUnlocked('p1'), isTrue);
      expect(wallet.hasUnlocked('p2'), isFalse);
    });

    test('canAffordSolution needs at least the solution cost', () {
      expect(const WalletModel(gems: GemRules.solutionCost).canAffordSolution,
          isTrue);
      expect(const WalletModel(gems: 0).canAffordSolution, isFalse);
    });

    test('gem rules match firestore.rules', () {
      // firestore.rules hard-codes these; update both together.
      expect(GemRules.welcomeBonus, 3);
      expect(GemRules.solveReward, 1);
      expect(GemRules.solutionCost, 1);
    });
  });
}
