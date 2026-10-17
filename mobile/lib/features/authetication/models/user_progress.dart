class UserProgressModel {
  final num? currentCourse;
  final List<num>? passedCourses;
  final List<String>? passedDsa;

  UserProgressModel({
    this.currentCourse,
    this.passedCourses,
    this.passedDsa,
  });

  UserProgressModel copyWith({
    num? currentCourse,
    List<num>? passedCourses,
    List<String>? passedDsa,
  }) =>
      UserProgressModel(
        currentCourse: currentCourse ?? this.currentCourse,
        passedCourses: passedCourses ?? this.passedCourses,
        passedDsa: passedDsa ?? this.passedDsa,
      );

  factory UserProgressModel.fromJson(Map<String, dynamic> json) =>
      UserProgressModel(
        currentCourse: json["current_course"],
        passedCourses: json["passed_courses"] == null
            ? []
            : List<num>.from(json["passed_courses"]!.map((x) => x)),
        passedDsa: json["passed_dsa"] == null
            ? []
            : List<String>.from(json["passed_dsa"]!.map((x) => x)),
      );

  Map<String, dynamic> toJson() => {
    
        "current_course": currentCourse,
        "passed_courses": passedCourses == null
            ? []
            : List<dynamic>.from(passedCourses!.map((x) => x)),
        "passed_dsa": passedDsa == null
            ? []
            : List<dynamic>.from(passedDsa!.map((x) => x)),
      };
}
