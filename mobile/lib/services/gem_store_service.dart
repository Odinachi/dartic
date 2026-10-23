import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:purchases_flutter/purchases_flutter.dart';

/// A gem pack sold through Apple / Google in-app purchase via RevenueCat.
class GemPack {
  final Package package;
  final int gems;

  const GemPack(this.package, this.gems);

  String get price => package.storeProduct.priceString;
}

/// In-app gem purchases through RevenueCat.
///
/// Gems are credited server-side: after a purchase the app calls
/// POST /api/gems/sync (landing_page/api/gem_sync.py), which reads purchases
/// from RevenueCat and adds them to the Firestore wallet. Formerly: the webhook in
/// landing_page/api/index.py, which adds them to the Firestore wallet. The app only
/// starts the purchase and then watches the wallet.
///
/// Store setup (see README → Gems):
/// - consumable products named `dartic_gems_<amount>` (e.g. dartic_gems_10)
///   in App Store Connect and Play Console;
/// - a RevenueCat offering with identifier [offeringId] containing them;
/// - public SDK keys passed with --dart-define=RC_APPLE_KEY=… / RC_GOOGLE_KEY=….
class GemStoreService {
  static const offeringId = 'gems';

  static const _appleKey = String.fromEnvironment('RC_APPLE_KEY');
  static const _googleKey = String.fromEnvironment('RC_GOOGLE_KEY');

  bool _configured = false;

  /// False when the build has no RevenueCat key for this platform.
  bool get isAvailable => _configured;

  /// Gems granted by a product, from its id: `dartic_gems_25` → 25.
  /// The server (gem_webhook.gems_for_product) uses the same rule.
  static int? gemsForProduct(String productId) {
    final match = RegExp(r'gems_(\d+)').firstMatch(productId);
    return match == null ? null : int.tryParse(match.group(1)!);
  }

  /// Call once at startup, with the signed-in Firebase uid if there is one.
  Future<void> configure({String? uid}) async {
    if (_configured || kIsWeb) return;
    final key = Platform.isIOS ? _appleKey : _googleKey;
    if (key.isEmpty) return; // store disabled in this build
    try {
      final config = PurchasesConfiguration(key)..appUserID = uid;
      await Purchases.configure(config);
      _configured = true;
    } catch (e) {
      debugPrint('RevenueCat configure failed: $e');
    }
  }

  /// Ties purchases to the Firebase user so the server knows whose wallet to
  /// credit.
  Future<void> identify(String uid) async {
    if (!_configured) return;
    try {
      await Purchases.logIn(uid);
    } catch (e) {
      debugPrint('RevenueCat logIn failed: $e');
    }
  }

  Future<void> signOut() async {
    if (!_configured) return;
    try {
      if (!await Purchases.isAnonymous) await Purchases.logOut();
    } catch (e) {
      debugPrint('RevenueCat logOut failed: $e');
    }
  }

  /// Gem packs from the [offeringId] offering, smallest first.
  Future<({List<GemPack> packs, String? error})> fetchPacks() async {
    if (!_configured) {
      return (packs: <GemPack>[], error: 'Gem purchases aren\'t available right now');
    }
    try {
      final offerings = await Purchases.getOfferings();
      final offering = offerings.getOffering(offeringId) ?? offerings.current;
      final packs = <GemPack>[
        for (final p in offering?.availablePackages ?? const <Package>[])
          if (gemsForProduct(p.storeProduct.identifier) case final gems?)
            GemPack(p, gems),
      ]..sort((a, b) => a.gems.compareTo(b.gems));
      return (
        packs: packs,
        error: packs.isEmpty ? 'No gem packs available right now' : null
      );
    } on PlatformException catch (e) {
      return (packs: <GemPack>[], error: e.message ?? 'Could not load gem packs');
    }
  }

  /// Starts the store purchase. `cancelled` is true if the user backed out.
  Future<({bool success, bool cancelled, String? error})> buy(
      GemPack pack) async {
    try {
      await Purchases.purchase(PurchaseParams.package(pack.package));
      return (success: true, cancelled: false, error: null);
    } on PlatformException catch (e) {
      final code = PurchasesErrorHelper.getErrorCode(e);
      if (code == PurchasesErrorCode.purchaseCancelledError) {
        return (success: false, cancelled: true, error: null);
      }
      return (
        success: false,
        cancelled: false,
        error: e.message ?? 'The purchase didn\'t go through'
      );
    }
  }
}
