import 'dart:convert' as j;

class TestResult {
  final TestCase testCase;
  final dynamic actualOutput;
  final bool passed;
  final String? errorMessage;
  final Duration executionTime;

  const TestResult({
    required this.testCase,
    required this.actualOutput,
    required this.passed,
    this.errorMessage,
    required this.executionTime,
  });
}

class TestRunResult {
  final TestSuite? testSuite;
  final List<TestResult> results;
  final int passedCount;
  final int totalCount;
  final Duration totalExecutionTime;

  const TestRunResult({
    this.testSuite,
    required this.results,
    required this.passedCount,
    required this.totalCount,
    required this.totalExecutionTime,
  });

  double get passRate => totalCount > 0 ? passedCount / totalCount : 0.0;
}

class TestCase {
  final String? name;
  final List<dynamic>? inputs;
  final dynamic expectedOutput;
  final String? description;

  const TestCase({
    this.name,
    this.inputs,
    this.expectedOutput,
    this.description,
  });

  factory TestCase.fromJson(Map<String, dynamic> json) {
    return TestCase(
      name: json['name'],
      inputs: json['inputs'],
      expectedOutput: json['expected_output'],
      description: json['description'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'inputs': inputs,
      'expected_output': expectedOutput,
      'description': description,
    };
  }
}

class TestSuite {
  final String? answer;
  final String? description;
  final String? question;
  final String? functionName;
  final List<TestCase>? testCases;

  const TestSuite(
      {this.answer,
      this.functionName,
      this.testCases,
      this.description,
      this.question});

  factory TestSuite.fromJson(Map<String, dynamic> json) {
    return TestSuite(
      answer: json['answer'],
      description: json['description'],
      functionName: json['function_name'],
      question: json['question'],
      testCases: (json['test_cases'] as List<dynamic>? ?? [])
          .map((testCase) => TestCase.fromJson(
              testCase is String ? j.json.decode(testCase) : testCase))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'answer': answer,
      'description': description,
      'function_name': functionName,
      'question': question,
      'test_cases': testCases?.map((testCase) => testCase.toJson()).toList(),
    };
  }
}
