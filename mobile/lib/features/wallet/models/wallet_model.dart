/// Coin economy settings. Firestore rules (firestore.rules) enforce the same
/// numbers, so change both together.
class CoinRules {
  /// Coins granted once, when a user's wallet is first created.
  static const welcomeBonus = 3;

  /// Coins earned the first time a user solves each problem.
  static const solveReward = 1;

  /// Coins spent to unlock one problem's solution (unlocked for good).
  static const solutionCost = 1;
}

/// A user's coin wallet: `Users/{uid}/wallet/main`.
class WalletModel {
  final int coins;

  /// Problem IDs whose solutions this user has unlocked.
  final List<String> unlocked;

  /// Problem IDs this user has already been paid a solve reward for.
  final List<String> rewarded;

  const WalletModel({
    this.coins = 0,
    this.unlocked = const [],
    this.rewarded = const [],
  });

  factory WalletModel.fromJson(Map<String, dynamic> json) => WalletModel(
        coins: (json['coins'] as num?)?.toInt() ?? 0,
        unlocked: List<String>.from(json['unlocked'] ?? const []),
        rewarded: List<String>.from(json['rewarded'] ?? const []),
      );

  bool hasUnlocked(String problemId) => unlocked.contains(problemId);

  bool get canAffordSolution => coins >= CoinRules.solutionCost;
}
