import 'package:dartcoder/shared/markdown.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('tagUntaggedCodeFences', () {
    test('tags an untagged opening fence and leaves the closing one', () {
      expect(tagUntaggedCodeFences('a\n```\nprint(1);\n```\nb'),
          'a\n```dart\nprint(1);\n```\nb');
    });

    test('keeps fences that already have a language', () {
      const md = '```json\n{}\n```';
      expect(tagUntaggedCodeFences(md), md);
    });

    test('handles several blocks and indentation', () {
      expect(tagUntaggedCodeFences('```\nx\n```\n  ```\ny\n  ```'),
          '```dart\nx\n```\n  ```dart\ny\n  ```');
    });

    test('ignores backticks inside a tilde block', () {
      expect(tagUntaggedCodeFences('~~~\n```\n~~~'), '~~~dart\n```\n~~~');
    });
  });
}
