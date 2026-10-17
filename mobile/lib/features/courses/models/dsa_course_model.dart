import 'package:dartcoder/features/courses/models/quiz_model.dart';

/// A module (group of lessons) in `DSA_course_modules`.
class DsaModule {
  final int module;
  final String title;
  final String? desc;
  final int lessonCount;

  const DsaModule({
    required this.module,
    required this.title,
    this.desc,
    this.lessonCount = 0,
  });

  factory DsaModule.fromJson(Map<String, dynamic> json) => DsaModule(
        module: (json["module"] as num).toInt(),
        title: json["title"] as String? ?? 'Module ${json["module"]}',
        desc: json["desc"] as String?,
        lessonCount: (json["lessonCount"] as num?)?.toInt() ?? 0,
      );
}

/// A lesson summary in the `DSA_course` collection. The markdown and quiz
/// live in subcollections and are loaded with [DsaLessonContent].
class DsaCourseModel {
  final String id;
  final String? title;
  final String? desc;
  final int? module;
  final String? moduleTitle;

  /// Global sort key: `module * 100 + lessonNumber`.
  final num? order;
  final List<String> videos;
  final int questionCount;
  final int? readMinutes;

  DsaCourseModel({
    required this.id,
    this.title,
    this.desc,
    this.module,
    this.moduleTitle,
    this.order,
    this.videos = const [],
    this.questionCount = 0,
    this.readMinutes,
  });

  /// Position within its module, e.g. 3 for order 203.
  int? get lessonNumber => order == null ? null : order!.toInt() % 100;

  bool get hasQuiz => questionCount > 0;

  factory DsaCourseModel.fromJson(Map<String, dynamic> json,
          {required String id}) =>
      DsaCourseModel(
        id: id,
        title: (json["title"] ?? json["name"]) as String?,
        desc: (json["desc"] ?? json["description"]) as String?,
        module: (json["module"] as num?)?.toInt(),
        moduleTitle: json["moduleTitle"] as String?,
        order: (json["order"] ?? json["index"]) as num?,
        videos: List<String>.from(json["videos"] ?? const []),
        questionCount: (json["questionCount"] as num?)?.toInt() ?? 0,
        readMinutes: (json["readMinutes"] as num?)?.toInt(),
      );
}

/// The full body of a lesson: markdown plus quiz questions.
class DsaLessonContent {
  final String markdown;
  final List<Map<String, dynamic>> questions;

  const DsaLessonContent({required this.markdown, this.questions = const []});

  bool get hasQuiz => questions.isNotEmpty;

  /// Fresh quiz models each call, since [QuizModel.fromJson] shuffles options.
  List<QuizModel> get quiz =>
      questions.map((e) => QuizModel.fromJson(Map.of(e))).toList();
}
