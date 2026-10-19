import 'dart:async';

import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class WalletState {
  final WalletModel? wallet;
  final bool loading;
  final String? error;

  const WalletState({this.wallet, this.loading = false, this.error});

  int get coins => wallet?.coins ?? 0;
}

/// Holds the signed-in user's coin wallet. [load] creates it if needed and
/// then keeps it in sync with Firestore, so coins credited by the server
/// (purchases) show up without a refresh.
class WalletCubit extends Cubit<WalletState> {
  WalletCubit({required this.firebaseServices}) : super(const WalletState());

  final FirebaseServices firebaseServices;
  StreamSubscription<WalletModel?>? _sub;

  Future<void> load() async {
    if (state.loading) return;
    emit(WalletState(wallet: state.wallet, loading: true));
    final result = await firebaseServices.fetchWallet();
    emit(WalletState(wallet: result.wallet ?? state.wallet, error: result.error));
    if (result.wallet != null) _watch();
  }

  void _watch() {
    _sub?.cancel();
    _sub = firebaseServices.watchWallet().listen((wallet) {
      if (wallet != null && !isClosed) emit(WalletState(wallet: wallet));
    }, onError: (_) {});
  }

  bool hasUnlocked(String problemId) =>
      state.wallet?.hasUnlocked(problemId) ?? false;

  /// Spends a coin (unless already unlocked) and returns the solution code.
  Future<({String? answer, String? error})> unlockAndFetch(
      String problemId) async {
    if (!hasUnlocked(problemId)) {
      final unlock = await firebaseServices.unlockSolution(problemId);
      if (unlock.error != null) return (answer: null, error: unlock.error);
      emit(WalletState(wallet: unlock.wallet));
    }
    return firebaseServices.fetchSolution(problemId);
  }

  /// Pays the first-solve reward for [problemId]. Returns true if a coin was
  /// earned (false if it was already collected or the call failed).
  Future<bool> rewardSolve(String problemId) async {
    if (state.wallet == null) await load();
    final result = await firebaseServices.rewardSolve(problemId);
    if (result.wallet != null) emit(WalletState(wallet: result.wallet));
    return result.rewarded;
  }

  /// Clear on sign-out so the next user doesn't see a stale balance.
  void reset() {
    _sub?.cancel();
    _sub = null;
    emit(const WalletState());
  }

  @override
  Future<void> close() {
    _sub?.cancel();
    return super.close();
  }
}
