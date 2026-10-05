import 'package:dartcoder/shared/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_test/flutter_test.dart';

Widget _wrap(Widget child) => ScreenUtilInit(
  designSize: const Size(375, 812),
  builder: (_, __) => MaterialApp(
    home: Scaffold(body: Center(child: child)),
  ),
);

void main() {
  group('AppButton', () {
    testWidgets('calls onTap when pressed', (tester) async {
      var taps = 0;
      await tester.pumpWidget(
        _wrap(AppButton(text: 'Go', onTap: () => taps++)),
      );
      await tester.tap(find.byType(AppButton));
      expect(taps, 1);
    });

    testWidgets('uses OutlinedButton when borderColor is set', (tester) async {
      await tester.pumpWidget(
        _wrap(AppButton(text: 'Go', borderColor: Colors.grey, onTap: () {})),
      );
      expect(find.byType(OutlinedButton), findsOneWidget);
      expect(find.byType(FilledButton), findsNothing);
    });

    testWidgets('is disabled without onTap', (tester) async {
      final handle = tester.ensureSemantics();
      await tester.pumpWidget(_wrap(const AppButton(text: 'Go')));
      expect(
        tester.widget<FilledButton>(find.byType(FilledButton)).enabled,
        isFalse,
      );
      expect(
        tester.getSemantics(find.byType(FilledButton)),
        matchesSemantics(
          label: 'Go',
          isButton: true,
          hasEnabledState: true,
          isEnabled: false,
          isFocusable: false,
        ),
      );
      handle.dispose();
    });

    testWidgets('loading shows a spinner and blocks taps', (tester) async {
      var taps = 0;
      await tester.pumpWidget(
        _wrap(AppButton(text: 'Go', isLoading: true, onTap: () => taps++)),
      );
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      await tester.tap(find.byType(AppButton));
      expect(taps, 0);
    });

    testWidgets('exposes button semantics with its label', (tester) async {
      final handle = tester.ensureSemantics();
      await tester.pumpWidget(
        _wrap(
          AppButton(text: 'Go', semanticLabel: 'Start course', onTap: () {}),
        ),
      );
      expect(
        tester.getSemantics(find.byType(FilledButton)),
        matchesSemantics(
          label: 'Start course',
          isButton: true,
          hasEnabledState: true,
          isEnabled: true,
          isFocusable: true,
          hasTapAction: true,
          hasFocusAction: true,
        ),
      );
      handle.dispose();
    });
  });
}
