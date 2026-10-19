import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:dartcoder/features/wallet/view_model/wallet_cubit.dart';
import 'package:dartcoder/main.dart' show coinStore;
import 'package:dartcoder/services/coin_store_service.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/atom-one-light.dart';
import 'package:flutter_highlight/themes/nord.dart';

const _coinColor = AppColors.amber;

/// A small coin icon used wherever coins are mentioned.
class CoinIcon extends StatelessWidget {
  const CoinIcon({super.key, this.size = 18});
  final double size;

  @override
  Widget build(BuildContext context) =>
      Icon(Icons.toll_rounded, size: size, color: _coinColor);
}

/// Live coin balance pill, e.g. in an app bar. Loads the wallet on first use.
class CoinBadge extends StatefulWidget {
  const CoinBadge({super.key});

  @override
  State<CoinBadge> createState() => _CoinBadgeState();
}

class _CoinBadgeState extends State<CoinBadge> {
  @override
  void initState() {
    super.initState();
    final cubit = context.read<WalletCubit>();
    if (cubit.state.wallet == null) cubit.load();
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<WalletCubit, WalletState>(builder: (context, state) {
      if (state.wallet == null && state.error != null) {
        return const SizedBox.shrink(); // signed out or offline
      }
      return Pressable(
        onTap: () => showCoinInfoSheet(context),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: _coinColor.withValues(alpha: .14),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CoinIcon(size: 18),
              const SizedBox(width: 5),
              state.wallet == null
                  ? const SizedBox(
                      width: 12,
                      height: 12,
                      child: CircularProgressIndicator(
                          strokeWidth: 1.6, color: _coinColor))
                  : Text(
                      '${state.coins}',
                      style: context.text.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: _coinColor,
                      ),
                    ),
            ],
          ),
        ),
      );
    });
  }
}

/// Explains how coins work, with a way into the coin store.
Future<void> showCoinInfoSheet(BuildContext context) async {
  final canBuy = coinStore.isAvailable;
  final buy = await _sheet(
    context,
    icon: const CoinIcon(size: 30),
    title: 'Coins',
    body:
        'Spend ${_coins(CoinRules.solutionCost)} to unlock a problem\'s solution. '
        'Once unlocked, it stays unlocked.\n\n'
        'Earn ${_coins(CoinRules.solveReward)} the first time you solve each problem'
        '${canBuy ? ', or get more in the coin store' : ''}. '
        'New accounts start with ${_coins(CoinRules.welcomeBonus)}.',
    primary: canBuy ? 'Get coins' : 'Got it',
    secondary: canBuy ? 'Close' : null,
  );
  if (buy == true && canBuy && context.mounted) await showCoinStore(context);
}

/// In-app coin store: packs sold through Apple / Google in-app purchase.
/// Purchased coins are credited by the server and arrive via the wallet stream.
Future<void> showCoinStore(BuildContext context) {
  if (FirebaseAuth.instance.currentUser == null) {
    AppRouter.showMessage('Sign in to get coins');
    return Future.value();
  }
  return showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: context.palette.surface,
    shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (_) => const _CoinStoreSheet(),
  );
}

class _CoinStoreSheet extends StatefulWidget {
  const _CoinStoreSheet();

  @override
  State<_CoinStoreSheet> createState() => _CoinStoreSheetState();
}

class _CoinStoreSheetState extends State<_CoinStoreSheet> {
  late final _packs = coinStore.fetchPacks();
  CoinPack? _buying;

  Future<void> _buy(CoinPack pack) async {
    setState(() => _buying = pack);
    final result = await coinStore.buy(pack);
    if (!mounted) return;
    setState(() => _buying = null);
    if (result.success) {
      Navigator.of(context).pop();
      AppRouter.showMessage(
          'Thanks! ${_coins(pack.coins)} will be added in a moment.');
    } else if (!result.cancelled) {
      AppRouter.showMessage(result.error ?? 'The purchase didn\'t go through');
    }
  }

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const _Grabber(),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Text('Get coins',
                      style: context.text.titleLarge
                          ?.copyWith(fontWeight: FontWeight.w700)),
                ),
                const CoinBadge(),
              ],
            ),
            const SizedBox(height: 6),
            Text('Unlock solutions whenever you\'re stuck.',
                style: context.text.bodyMedium
                    ?.copyWith(color: palette.textMuted)),
            const SizedBox(height: 16),
            FutureBuilder(
              future: _packs,
              builder: (context, snap) {
                if (!snap.hasData) {
                  return const Padding(
                    padding: EdgeInsets.symmetric(vertical: 32),
                    child: Center(
                        child: CircularProgressIndicator(color: _coinColor)),
                  );
                }
                final (:packs, :error) = snap.data!;
                if (packs.isEmpty) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 24),
                    child: Text(error ?? 'No coin packs available right now',
                        textAlign: TextAlign.center,
                        style: context.text.bodyMedium
                            ?.copyWith(color: palette.textMuted)),
                  );
                }
                return Column(
                  children: [
                    for (final pack in packs)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: _PackRow(
                          pack: pack,
                          busy: _buying == pack,
                          onTap: _buying == null ? () => _buy(pack) : null,
                        ),
                      ),
                  ],
                );
              },
            ),
            const SizedBox(height: 6),
            Text(
              'Charged to your ${Theme.of(context).platform == TargetPlatform.iOS ? 'Apple Account' : 'Google Play account'}. '
              'Coins never expire and can only be used in Dartic.',
              textAlign: TextAlign.center,
              style: context.text.bodySmall?.copyWith(color: palette.textMuted),
            ),
          ],
        ),
      ),
    );
  }
}

class _PackRow extends StatelessWidget {
  const _PackRow({required this.pack, required this.busy, this.onTap});

  final CoinPack pack;
  final bool busy;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return Pressable(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: palette.surfaceAlt,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: palette.border),
        ),
        child: Row(
          children: [
            const CoinIcon(size: 26),
            const SizedBox(width: 12),
            Expanded(
              child: Text(_coins(pack.coins),
                  style: context.text.titleMedium
                      ?.copyWith(fontWeight: FontWeight.w700)),
            ),
            Container(
              constraints: const BoxConstraints(minWidth: 86),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                gradient: AppColors.primaryGradient,
                borderRadius: BorderRadius.circular(10),
              ),
              child: busy
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: AppColors.white))
                  : Text(pack.price,
                      style: context.text.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w700,
                          color: AppColors.white)),
            ),
          ],
        ),
      ),
    );
  }
}

/// Asks to spend a coin on [problemId]'s solution, then shows it.
/// [onUseCode] receives the code if the user copies it into the editor.
Future<void> openSolution(
  BuildContext context, {
  required String problemId,
  required ValueChanged<String> onUseCode,
}) async {
  final cubit = context.read<WalletCubit>();
  if (cubit.state.wallet == null) await cubit.load();
  if (!context.mounted) return;

  if (!cubit.hasUnlocked(problemId)) {
    final wallet = cubit.state.wallet;
    if (wallet == null) {
      AppRouter.showMessage(cubit.state.error ?? 'Could not load your coins');
      return;
    }
    if (!wallet.canAffordSolution) {
      final canBuy = coinStore.isAvailable;
      final buy = await _sheet(
        context,
        icon: const CoinIcon(size: 30),
        title: 'Out of coins',
        body: 'Solve a problem you haven\'t solved before to earn '
            '${_coins(CoinRules.solveReward)}'
            '${canBuy ? ', or get a coin pack' : ''}, then come back to unlock this solution.',
        primary: canBuy ? 'Get coins' : 'Keep trying',
        secondary: canBuy ? 'Keep trying' : null,
      );
      if (buy == true && canBuy && context.mounted) await showCoinStore(context);
      return;
    }
    final confirmed = await _sheet(
      context,
      icon: const CoinIcon(size: 30),
      title: 'Unlock solution?',
      body: 'This costs ${_coins(CoinRules.solutionCost)}. '
          'You have ${_coins(wallet.coins)}. The solution stays unlocked for good.',
      primary: 'Unlock for ${_coins(CoinRules.solutionCost)}',
      secondary: 'Not now',
    );
    if (confirmed != true || !context.mounted) return;
  }

  final result = await cubit.unlockAndFetch(problemId);
  if (!context.mounted) return;
  if (result.answer == null) {
    AppRouter.showMessage(result.error ?? 'Could not load the solution');
    return;
  }
  await _showSolution(context, result.answer!, onUseCode);
}

String _coins(int n) => n == 1 ? '1 coin' : '$n coins';

Future<void> _showSolution(
    BuildContext context, String code, ValueChanged<String> onUseCode) {
  return showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: context.palette.surface,
    shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (sheetContext) => SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(
            maxHeight: MediaQuery.sizeOf(sheetContext).height * .85),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const _Grabber(),
              const SizedBox(height: 14),
              Text('Solution',
                  style: sheetContext.text.titleLarge
                      ?.copyWith(fontWeight: FontWeight.w700)),
              const SizedBox(height: 12),
              Flexible(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: SingleChildScrollView(
                    child: SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: HighlightView(
                        code,
                        language: 'dart',
                        theme: sheetContext.isDark ? nordTheme : atomOneLightTheme,
                        padding: const EdgeInsets.all(14),
                        textStyle: const TextStyle(
                          fontFamily: 'Menlo',
                          fontFamilyFallback: ['Courier', 'monospace'],
                          fontSize: 13,
                          height: 1.5,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _SheetButton(
                      label: 'Copy',
                      onTap: () {
                        Clipboard.setData(ClipboardData(text: code));
                        AppRouter.showMessage('Solution copied');
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: _SheetButton(
                      label: 'Use in editor',
                      primary: true,
                      onTap: () {
                        Navigator.of(sheetContext).pop();
                        onUseCode(code);
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    ),
  );
}

/// Simple bottom sheet with a title, body and one or two buttons.
/// Resolves to true when the primary button is tapped.
Future<bool?> _sheet(
  BuildContext context, {
  required Widget icon,
  required String title,
  required String body,
  required String primary,
  String? secondary,
}) {
  return showModalBottomSheet<bool>(
    context: context,
    backgroundColor: context.palette.surface,
    shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (sheetContext) => SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(24, 12, 24, 16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const _Grabber(),
            const SizedBox(height: 20),
            icon,
            const SizedBox(height: 12),
            Text(title,
                style: sheetContext.text.titleLarge
                    ?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            Text(body,
                textAlign: TextAlign.center,
                style: sheetContext.text.bodyMedium?.copyWith(
                    height: 1.45, color: sheetContext.palette.textMuted)),
            const SizedBox(height: 22),
            _SheetButton(
              label: primary,
              primary: true,
              onTap: () => Navigator.of(sheetContext).pop(true),
            ),
            if (secondary != null) ...[
              const SizedBox(height: 8),
              _SheetButton(
                label: secondary,
                onTap: () => Navigator.of(sheetContext).pop(false),
              ),
            ],
          ],
        ),
      ),
    ),
  );
}

class _Grabber extends StatelessWidget {
  const _Grabber();

  @override
  Widget build(BuildContext context) => Center(
        child: Container(
          width: 40,
          height: 4,
          decoration: BoxDecoration(
            color: context.palette.border,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
      );
}

class _SheetButton extends StatelessWidget {
  const _SheetButton(
      {required this.label, required this.onTap, this.primary = false});

  final String label;
  final VoidCallback onTap;
  final bool primary;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return Pressable(
      onTap: onTap,
      child: Container(
        height: 48,
        width: double.infinity,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: primary ? null : palette.surfaceAlt,
          gradient: primary ? AppColors.primaryGradient : null,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          label,
          style: context.text.bodyMedium?.copyWith(
            fontWeight: FontWeight.w700,
            color: primary ? AppColors.white : palette.textPrimary,
          ),
        ),
      ),
    );
  }
}
