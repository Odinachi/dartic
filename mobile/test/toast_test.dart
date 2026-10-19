import 'package:dartcoder/shared/navigation/router.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_test/flutter_test.dart';

Widget _app({EdgeInsets keyboard = EdgeInsets.zero}) => ScreenUtilInit(
      designSize: const Size(360, 690),
      builder: (_, __) => MaterialApp(
        navigatorKey: AppRouter.navKey,
        builder: (context, child) => MediaQuery(
          data: MediaQuery.of(context).copyWith(viewInsets: keyboard),
          child: child!,
        ),
        home: Scaffold(
          floatingActionButton: Column(
            mainAxisSize: MainAxisSize.min,
            children: List.generate(
                3, (_) => const SizedBox(width: 60, height: 120)),
          ),
          body: const SizedBox.expand(),
        ),
      ),
    );

void main() {
  testWidgets('shows, replaces and hides messages', (tester) async {
    await tester.pumpWidget(_app());
    AppRouter.showMessage('First');
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('First'), findsOneWidget);

    AppRouter.showMessage('Second');
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('First'), findsNothing);
    expect(find.text('Second'), findsOneWidget);

    await tester.pump(const Duration(seconds: 3));
    await tester.pumpAndSettle();
    expect(find.text('Second'), findsNothing);
    expect(tester.takeException(), isNull);
  });

  testWidgets('stays on screen above the keyboard with a tall FAB',
      (tester) async {
    await tester.pumpWidget(
        _app(keyboard: const EdgeInsets.only(bottom: 300)));
    AppRouter.showMessage('Solved! +1 gem');
    await tester.pump(const Duration(milliseconds: 300));
    final rect = tester.getRect(find.text('Solved! +1 gem'));
    final screen = tester.view.physicalSize / tester.view.devicePixelRatio;
    expect(rect.top, greaterThanOrEqualTo(0));
    expect(rect.bottom, lessThanOrEqualTo(screen.height - 300));
    expect(tester.takeException(), isNull);
    await tester.pump(const Duration(seconds: 4));
  });
}
