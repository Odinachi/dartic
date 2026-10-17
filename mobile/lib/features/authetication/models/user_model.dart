class UserModel {
  final String? firstName;
  final String? lastName;
  final String? username;
  final DateTime? createdAt;
  final String? currentLevel;
  final String? uid;
  final String? email;
  final String? photoUrl;

  UserModel({
    this.firstName,
    this.lastName,
    this.username,
    this.createdAt,
    this.currentLevel,
    this.uid,
    this.email,
    this.photoUrl,
  });

  UserModel copyWith({
    String? firstName,
    String? lastName,
    String? username,
    DateTime? createdAt,
    String? currentLevel,
    String? uid,
    String? email,
    String? photoUrl,
  }) =>
      UserModel(
        firstName: firstName ?? this.firstName,
        lastName: lastName ?? this.lastName,
        username: username ?? this.username,
        createdAt: createdAt ?? this.createdAt,
        currentLevel: currentLevel ?? this.currentLevel,
        uid: uid ?? this.uid,
        email: email ?? this.email,
        photoUrl: photoUrl ?? this.photoUrl,
      );

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        firstName: json["first_name"],
        lastName: json["last_name"],
        username: json["username"],
        createdAt: DateTime.tryParse(json["createdAt"] ?? ""),
        currentLevel: json["current_level"],
        uid: json["uid"],
        email: json["email"],
        photoUrl: json["photo_url"],
      );

  Map<String, dynamic> toJson() => {
        "first_name": firstName,
        "last_name": lastName,
        "username": username,
        "createdAt": createdAt?.toIso8601String(),
        "current_level": currentLevel,
        "uid": uid,
        "email": email,
        "photo_url": photoUrl,
      };
}
