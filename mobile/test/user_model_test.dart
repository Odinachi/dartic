import 'package:dartcoder/features/authetication/models/user_model.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('UserModel tests', () {
    test('fromJson and toJson should correctly serialize and deserialize username', () {
      final json = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'username': 'janedoe_dev',
        'createdAt': '2026-09-11T12:00:00.000',
        'current_level': 'Intermediate',
        'uid': 'user123',
        'email': 'jane@example.com',
      };

      final user = UserModel.fromJson(json);
      expect(user.firstName, 'Jane');
      expect(user.lastName, 'Doe');
      expect(user.username, 'janedoe_dev');
      expect(user.currentLevel, 'Intermediate');
      expect(user.uid, 'user123');
      expect(user.email, 'jane@example.com');

      final serialized = user.toJson();
      expect(serialized['username'], 'janedoe_dev');
      expect(serialized['first_name'], 'Jane');
      expect(serialized['last_name'], 'Doe');
      expect(serialized['current_level'], 'Intermediate');
      expect(serialized['uid'], 'user123');
    });

    test('copyWith updates username and keeps existing fields', () {
      final user = UserModel(
        uid: 'user123',
        firstName: 'Jane',
        lastName: 'Doe',
        currentLevel: 'Beginner',
      );

      final updated = user.copyWith(username: 'new_username');
      expect(updated.username, 'new_username');
      expect(updated.firstName, 'Jane');
      expect(updated.lastName, 'Doe');
      expect(updated.currentLevel, 'Beginner');
      expect(updated.uid, 'user123');
    });
  });
}
