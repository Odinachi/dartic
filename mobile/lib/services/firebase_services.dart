import 'dart:io';
import 'dart:convert';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dartcoder/features/authetication/models/user_model.dart';
import 'package:dartcoder/features/authetication/models/user_progress.dart';
import 'package:dartcoder/features/courses/models/dsa_course_model.dart';
import 'package:dartcoder/features/editor/models/dsa_list_model.dart';
import 'package:dartcoder/features/editor/models/test_case.dart';
import 'package:dartcoder/features/wallet/models/wallet_model.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

class FirebaseServices {
  final _auth = FirebaseAuth.instance;
  final _firestore = FirebaseFirestore.instance;

  Future<({OAuthCredential? oAuth, String? familyName, String? givenName})>
      _getAppleCredential(bool isGoogle) async {
    if (isGoogle) {
      await GoogleSignIn.instance.initialize();
      final googleUser =
          (await GoogleSignIn.instance.authenticate()).authentication;
      final auth = GoogleAuthProvider.credential(
        idToken: googleUser.idToken,
      );

      return (
        oAuth: auth,
        familyName: auth.appleFullPersonName?.familyName,
        givenName: auth.appleFullPersonName?.givenName
      );
    } else {
      final appleCredential = await SignInWithApple.getAppleIDCredential(
        webAuthenticationOptions: WebAuthenticationOptions(
            clientId: String.fromEnvironment("CLIENT_ID"),
            redirectUri: Uri.parse(String.fromEnvironment("REDIRECT_URI"))),
        scopes: [
          AppleIDAuthorizationScopes.email,
          AppleIDAuthorizationScopes.fullName,
        ],
      );

      return (
        oAuth: OAuthProvider("apple.com").credential(
          idToken: appleCredential.identityToken,
          accessToken: appleCredential.authorizationCode,
        ),
        familyName: appleCredential.familyName,
        givenName: appleCredential.givenName
      );
    }
  }

  // Google Sign-In
  Future<
      ({
        UserCredential? account,
        String? familyName,
        String? givenName,
        String? error
      })> signInWithGoogle() async {
    try {
      final credential = await _getAppleCredential(true);
      return (
        account: await _auth.signInWithCredential(credential.oAuth!),
        error: null,
        familyName: credential.familyName,
        givenName: credential.givenName,
      );
    } catch (e) {
      if (e is FirebaseAuthException) {
        return (
          account: null,
          error: e.message,
          familyName: null,
          givenName: null
        );
      }
      return (
        account: null,
        error: e.toString(),
        familyName: null,
        givenName: null
      );
    }
  }

  // Apple Sign-In
  Future<
      ({
        UserCredential? account,
        String? familyName,
        String? givenName,
        String? error
      })> signInWithApple() async {
    try {
      final credential = await _getAppleCredential(false);
      return (
        account: await _auth.signInWithCredential(credential.oAuth!),
        error: null,
        familyName: credential.familyName,
        givenName: credential.givenName,
      );
    } catch (e) {
      if (e is FirebaseAuthException) {
        return (
          account: null,
          error: e.message,
          familyName: null,
          givenName: null
        );
      }

      return (
        account: null,
        error: e.toString(),
        familyName: null,
        givenName: null
      );
    }
  }

  Future<void> signOut() async {
    await _auth.signOut();
    await GoogleSignIn.instance.signOut();
  }

  Future<({bool? success, String? error})> saveProfile(UserModel user) async {
    try {
      final userDoc = _firestore.collection('Users').doc(user.uid);
      await userDoc.set(user.toJson(), SetOptions(merge: true));
      return (success: true, error: null);
    } catch (e) {
      return (success: false, error: e.toString());
    }
  }

  Future<({bool? success, String? error})> updateUsername(
      String username) async {
    try {
      final uid = _auth.currentUser?.uid;
      if (uid == null) {
        return (success: false, error: "No user is currently signed in.");
      }
      final userDoc = _firestore.collection('Users').doc(uid);
      await userDoc.set({
        'username': username.trim(),
      }, SetOptions(merge: true));
      return (success: true, error: null);
    } catch (e) {
      return (success: false, error: e.toString());
    }
  }

  Future<({bool isAvailable, String? error})> checkUsernameAvailability(
      String username) async {
    try {
      final cleanUsername = username.trim();
      if (cleanUsername.isEmpty) {
        return (isAvailable: false, error: "Username cannot be empty");
      }
      final querySnapshot = await _firestore
          .collection('Users')
          .where('username', isEqualTo: cleanUsername)
          .limit(1)
          .get();

      if (querySnapshot.docs.isEmpty) {
        return (isAvailable: true, error: null);
      }

      final isOwnDoc = querySnapshot.docs.first.id == _auth.currentUser?.uid;
      return (
        isAvailable: isOwnDoc,
        error: isOwnDoc ? null : "Username is already taken"
      );
    } catch (e) {
      return (isAvailable: false, error: e.toString());
    }
  }

  Future<({UserModel? user, String? error})> getProfile() async {
    try {
      final userDoc =
          _firestore.collection('Users').doc(_auth.currentUser?.uid);
      final userSnapshot = await userDoc.get();
      if (userSnapshot.exists) {
        return (user: UserModel.fromJson(userSnapshot.data()!), error: null);
      }
      return (user: null, error: "User not found");
    } catch (e) {
      return (user: null, error: e.toString());
    }
  }

  Future<({UserProgressModel? progress, String? error})>
      getUserProgress() async {
    try {
      final progressDoc = _firestore
          .collection('Users')
          .doc(_auth.currentUser?.uid)
          .collection('progress')
          .doc('current');
      final progressSnapshot = await progressDoc.get();
      if (progressSnapshot.exists) {
        return (
          progress: UserProgressModel.fromJson(progressSnapshot.data()!),
          error: null
        );
      }
      return (progress: null, error: "User progress not found");
    } catch (e) {
      return (progress: null, error: e.toString());
    }
  }

  Future<void> updateCurrentCourse(num courseId) async {
    final progressDoc = _firestore
        .collection('Users')
        .doc(_auth.currentUser?.uid)
        .collection('progress')
        .doc('current');

    await progressDoc
        .set({'current_course': courseId}, SetOptions(merge: true));
  }

  Future<void> updatePassedCourses(num courseId) async {
    final progressDoc = _firestore
        .collection('Users')
        .doc(_auth.currentUser?.uid)
        .collection('progress')
        .doc('current');

    await progressDoc.set({
      'passed_courses': FieldValue.arrayUnion([courseId])
    }, SetOptions(merge: true));
  }

  Future<({bool? deleted, String? error})> deleteAccount() async {
    try {
      final user = _auth.currentUser;

      if (user != null) {
        final cred = await _getAppleCredential(
            _auth.currentUser?.providerData.firstOrNull?.providerId ==
                'google.com');

        if (cred.oAuth == null) {
          return (deleted: false, error: "Re-authentication failed.");
        }
        // Reauthenticate user before deletion
        await user.reauthenticateWithCredential(cred.oAuth!);

        // Delete user data from Firestore: subcollections first (deleting a
        // document doesn't delete its subcollections), then the profile.
        final userDoc = _firestore.collection('Users').doc(user.uid);
        await userDoc.collection('progress').doc('current').delete();
        await _walletDoc?.delete();
        await userDoc.delete();

        // Delete user authentication
        await user.delete();
        return (deleted: true, error: null);
      } else {
        return (deleted: false, error: "No user is currently signed in.");
      }
    } catch (e) {
      if (e is FirebaseAuthException) {
        return (deleted: false, error: e.message);
      }
      return (deleted: false, error: e.toString());
    }
  }

  Future<
      ({
        List<DsaListModel>? documents,
        DocumentSnapshot? lastDocument,
        String? error
      })> fetchDSA({
    int limit = 10,
    DocumentSnapshot? startAfterDocument,
  }) async {
    try {
      var query = _firestore
          .collection('DSA')
          .withConverter(
              fromFirestore: (snapshot, _) =>
                  DsaListModel.fromJson(snapshot.data()!, id: snapshot.id),
              toFirestore: (model, _) => model.toJson())
          .orderBy("difficulty")
          .limit(limit);

      if (startAfterDocument != null) {
        query = query.startAfterDocument(startAfterDocument);
      }

      final dsaSnapshot = await query.get();
      final data = dsaSnapshot.docs.map((doc) => doc.data()).toList();

      return (
        documents: data,
        lastDocument:
            dsaSnapshot.docs.isNotEmpty ? dsaSnapshot.docs.last : null,
        error: null
      );
    } catch (e) {
      return (documents: null, lastDocument: null, error: e.toString());
    }
  }

  Future<({List<DsaModule>? modules, String? error})> fetchDsaModules() async {
    try {
      final snapshot = await _firestore
          .collection('DSA_course_modules')
          .orderBy('module')
          .get();
      final modules =
          snapshot.docs.map((doc) => DsaModule.fromJson(doc.data())).toList();
      return (modules: modules, error: null);
    } catch (e) {
      return (modules: null, error: e.toString());
    }
  }

  /// One page of lesson summaries ordered by `order`. Filtering by [module]
  /// uses a range on `order` (module * 100 .. module * 100 + 99), so no
  /// composite index is needed.
  Future<
      ({
        List<DsaCourseModel>? lessons,
        DocumentSnapshot? lastDocument,
        String? error
      })> fetchDsaCoursePage({
    int? module,
    int limit = 10,
    DocumentSnapshot? startAfterDocument,
  }) async {
    try {
      Query<Map<String, dynamic>> query = _firestore.collection('DSA_course');
      if (module != null) {
        query = query
            .where('order', isGreaterThanOrEqualTo: module * 100)
            .where('order', isLessThan: (module + 1) * 100);
      }
      query = query.orderBy('order').limit(limit);
      if (startAfterDocument != null) {
        query = query.startAfterDocument(startAfterDocument);
      }
      final snapshot = await query.get();
      final lessons = snapshot.docs
          .map((doc) => DsaCourseModel.fromJson(doc.data(), id: doc.id))
          .toList();
      return (
        lessons: lessons,
        lastDocument: snapshot.docs.isEmpty ? null : snapshot.docs.last,
        error: null
      );
    } catch (e) {
      return (lessons: null, lastDocument: null, error: e.toString());
    }
  }

  final _dsaLessonCache = <String, DsaLessonContent>{};

  /// Loads a lesson's markdown and quiz in parallel. Results are cached for
  /// the session so moving back and forth between lessons is instant.
  Future<({DsaLessonContent? content, String? error})> fetchDsaLessonContent(
      String lessonId) async {
    final cached = _dsaLessonCache[lessonId];
    if (cached != null) return (content: cached, error: null);
    try {
      final lessonRef = _firestore.collection('DSA_course').doc(lessonId);
      final [contentDoc, quizDoc] = await Future.wait([
        lessonRef.collection('content').doc('main').get(),
        lessonRef.collection('quiz').doc('main').get(),
      ]);
      final rawQuestions = quizDoc.data()?['questions'];
      final content = DsaLessonContent(
        markdown: contentDoc.data()?['markdown'] as String? ?? '',
        questions: rawQuestions is List
            ? rawQuestions
                .whereType<Map>()
                .map((e) => Map<String, dynamic>.from(e))
                .toList()
            : const [],
      );
      _dsaLessonCache[lessonId] = content;
      return (content: content, error: null);
    } catch (e) {
      return (content: null, error: e.toString());
    }
  }

  Future<({TestSuite? data, String? error})> fetchDsaProblems(String id) async {
    try {
      final data = await _firestore
          .collection('DSA')
          .doc(id)
          .collection("problem")
          .get();
      if (data.docs.isNotEmpty && data.docs.firstOrNull != null) {
        return (data: TestSuite.fromJson(data.docs.first.data()), error: null);
      }

      return (data: null, error: "No problems found");
    } catch (e) {
      return (data: null, error: e.toString());
    }
  }

  // ── Gems ──────────────────────────────────────────────────
  //
  // Users/{uid}/wallet/main = { gems, unlocked: [problemId], rewarded: [problemId] }
  // Firestore rules only allow: creating it with the welcome bonus, spending
  // exactly one gem to unlock one problem, or earning exactly one gem for
  // the first solve of one problem.

  DocumentReference<Map<String, dynamic>>? get _walletDoc {
    final uid = _auth.currentUser?.uid;
    if (uid == null) return null;
    return _firestore
        .collection('Users')
        .doc(uid)
        .collection('wallet')
        .doc('main');
  }

  /// Returns the user's wallet, creating it with the welcome bonus if needed.
  Future<({WalletModel? wallet, String? error})> fetchWallet() async {
    final doc = _walletDoc;
    if (doc == null) return (wallet: null, error: "Sign in to use gems");
    try {
      final wallet = await _firestore.runTransaction((tx) async {
        final snap = await tx.get(doc);
        if (snap.exists) return WalletModel.fromJson(snap.data()!);
        tx.set(doc, {
          'gems': GemRules.welcomeBonus,
          'unlocked': <String>[],
          'rewarded': <String>[],
          'createdAt': FieldValue.serverTimestamp(),
        });
        return const WalletModel(gems: GemRules.welcomeBonus);
      });
      return (wallet: wallet, error: null);
    } catch (e) {
      return (wallet: null, error: e.toString());
    }
  }

  /// Live wallet updates, e.g. when the server credits purchased gems.
  Stream<WalletModel?> watchWallet() {
    final doc = _walletDoc;
    if (doc == null) return const Stream.empty();
    return doc.snapshots().map(
        (snap) => snap.exists ? WalletModel.fromJson(snap.data()!) : null);
  }

  /// Asks the server to credit any gem purchases it hasn't credited yet. The
  /// server verifies the ID token and reads purchases from RevenueCat itself,
  /// so the app never says what it bought. Returns how many gems were added.
  Future<({int gems, String? error})> syncGemPurchases() async {
    final user = _auth.currentUser;
    if (user == null) return (gems: 0, error: "Sign in to use gems");
    final client = HttpClient()..connectionTimeout = const Duration(seconds: 10);
    try {
      final token = await user.getIdToken();
      final request = await client.postUrl(Uri.parse(AppLinks.gemSync));
      request.headers.set(HttpHeaders.authorizationHeader, 'Bearer $token');
      final response =
          await request.close().timeout(const Duration(seconds: 20));
      final body = await response.transform(utf8.decoder).join();
      if (response.statusCode != 200) {
        return (gems: 0, error: "Sync failed (${response.statusCode})");
      }
      final gems = (jsonDecode(body)['gems'] as num?)?.toInt() ?? 0;
      return (gems: gems, error: null);
    } catch (e) {
      return (gems: 0, error: e.toString());
    } finally {
      client.close();
    }
  }

  /// Spends one gem to unlock [problemId]'s solution. Free if it's already
  /// unlocked. Returns the updated wallet.
  Future<({WalletModel? wallet, String? error})> unlockSolution(
      String problemId) async {
    final doc = _walletDoc;
    if (doc == null) return (wallet: null, error: "Sign in to use gems");
    try {
      final wallet = await _firestore.runTransaction((tx) async {
        final snap = await tx.get(doc);
        final current = WalletModel.fromJson(snap.data() ?? const {});
        if (current.hasUnlocked(problemId)) return current;
        if (!current.canAffordSolution) throw const NotEnoughGems();
        tx.update(doc, {
          'gems': FieldValue.increment(-GemRules.solutionCost),
          'unlocked': FieldValue.arrayUnion([problemId]),
        });
        return WalletModel(
          gems: current.gems - GemRules.solutionCost,
          unlocked: [...current.unlocked, problemId],
          rewarded: current.rewarded,
        );
      });
      return (wallet: wallet, error: null);
    } on NotEnoughGems {
      return (wallet: null, error: NotEnoughGems.message);
    } catch (e) {
      return (wallet: null, error: e.toString());
    }
  }

  /// Reads an unlocked solution from `DSA/{id}/solution/main`. Falls back to
  /// the legacy `answer` field on the problem doc for problems that haven't
  /// been migrated yet (see scripts/move_dsa_solutions).
  Future<({String? answer, String? error})> fetchSolution(
      String problemId) async {
    try {
      final solution = await _firestore
          .collection('DSA')
          .doc(problemId)
          .collection('solution')
          .doc('main')
          .get();
      final answer = solution.data()?['answer'] as String?;
      if (answer != null && answer.isNotEmpty) {
        return (answer: answer, error: null);
      }

      final legacy = await fetchDsaProblems(problemId);
      final legacyAnswer = legacy.data?.answer;
      if (legacyAnswer != null && legacyAnswer.isNotEmpty) {
        return (answer: legacyAnswer, error: null);
      }
      return (answer: null, error: "No solution available for this problem");
    } catch (e) {
      return (answer: null, error: e.toString());
    }
  }

  Future<void> markProblemAsSolved(String id) async {
    try {
      final progressDoc = _firestore
          .collection('Users')
          .doc(_auth.currentUser?.uid)
          .collection('progress')
          .doc('current');

      await progressDoc.set({
        'passed_dsa': FieldValue.arrayUnion([id])
      }, SetOptions(merge: true));
    } catch (e) {
      // Handle error if needed
    }
  }
}

/// Thrown inside the unlock transaction when the balance is too low.
class NotEnoughGems implements Exception {
  const NotEnoughGems();
  static const message = "Not enough gems";
}
