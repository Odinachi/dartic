class DsaListModel {
  final String? problemName;
  final String? difficulty;
  final String? description;
  final String? id;

  DsaListModel({this.problemName, this.difficulty, this.description, this.id});

  factory DsaListModel.fromJson(Map<String, dynamic> json, {String? id}) =>
      DsaListModel(
        problemName: json["problem_name"],
        difficulty: json["difficulty"],
        description: json["description"],
        id: id,
      );

  Map<String, dynamic> toJson() => {
        "problem_name": problemName,
        "difficulty": difficulty,
        "description": description,
      };
}
