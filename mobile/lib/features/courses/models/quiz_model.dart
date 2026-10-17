import 'package:equatable/equatable.dart';

class QuizModel extends Equatable {
  final String? question;
  final List<String>? options;
  final List<String>? answer;
  final List<String>? userAnswer;
  final String? type;

  bool get isCorrect {
    if (userAnswer == null) return false;
    if (type == "mcq" || type == "fill") {
      if (answer is List) {
        List ua = userAnswer as List;
        List a = answer as List;
        if (ua.length != a.length) return false;
        for (int i = 0; i < ua.length; i++) {
          if (ua[i].replaceAll("\n", "\n").replaceAll("\\n", "\n") !=
              a[i].replaceAll("\n", "\n").replaceAll("\\n", "\n")) {
            return false;
          }
        }
        return true;
      }
      return userAnswer == answer;
    } else if (type == "order") {
      if (userAnswer is List && answer is List) {
        List ua = userAnswer as List;
        List a = answer as List;
        if (ua.length != a.length) return false;
        for (int i = 0; i < ua.length; i++) {
          if (ua[i] != a[i]) return false;
        }
        return true;
      } else {
        return false;
      }
    }
    return false;
  }

  const QuizModel({
    this.question,
    this.options,
    this.answer,
    this.type,
    this.userAnswer,
  });

  factory QuizModel.fromJson(Map<String, dynamic> json) {
    final opt = json["options"] == null ? [] : json["options"] as List?;
    opt?.shuffle();
    return QuizModel(
      question: json["question"],
      options: List<String>.from((opt ?? []).map((x) => x)),
      // answer: json["answer"],
      answer: json["answer"] == null
          ? []
          : List<String>.from(json["answer"]!.map((x) => x)),
      type: json["type"],
    );
  }

  Map<String, dynamic> toJson() => {
        "question": question,
        "options":
            options == null ? [] : List<dynamic>.from(options!.map((x) => x)),
        "answer": answer,
        "type": type,
      };

  QuizModel copyWith({
    String? question,
    List<String>? options,
    List<String>? answer,
    List<String>? userAnswer,
    String? type,
  }) {
    return QuizModel(
      question: question ?? this.question,
      options: options ?? this.options,
      answer: answer ?? this.answer,
      userAnswer: userAnswer,
      type: type ?? this.type,
    );
  }

  @override
  List<Object?> get props => [question, options, answer, userAnswer, type];
}
