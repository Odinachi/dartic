class CourseModel {
  final String? title;
  final String? path;
  final String? desc;
  final String? quiz;
  final int? id;
  final bool? canPractice;
  final bool? isCourse;
  final bool? completed;
  final List<String>? videos;

  /// Markdown body for courses served from Firestore (e.g. DSA_Course).
  /// When set it is rendered instead of loading [path] from the asset bundle.
  final String? content;

  /// Section heading used to group courses in the course list.
  final String? section;

  CourseModel({
    this.title,
    this.path,
    this.id,
    this.desc,
    this.quiz,
    this.canPractice = true,
    this.isCourse = true,
    this.completed = false,
    this.videos,
    this.content,
    this.section,
  });

  factory CourseModel.fromJson(Map<String, dynamic> json) => CourseModel(
        title: json["title"],
        path: json["path"],
        id: (json["id"] as num?)?.toInt(),
        desc: json["desc"],
        quiz: json["quiz"],
        canPractice: json["canPractice"] ?? true,
        isCourse: json["isCourse"] ?? true,
        completed: json["completed"] ?? false,
        videos: List<String>.from(json["videos"] ?? []),
        content: json["content"],
        section: json["section"],
      );

  Map<String, dynamic> toJson() => {
        "title": title,
        "path": path,
        "id": id,
        "desc": desc,
        "quiz": quiz,
        "canPractice": canPractice,
        "isCourse": isCourse,
        "completed": completed,
        "videos": videos,
        "content": content,
        "section": section,
      };
}
