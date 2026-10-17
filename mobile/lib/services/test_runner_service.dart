import 'dart:async';

import 'package:dart_eval/dart_eval.dart';
import 'package:dartcoder/features/editor/models/test_case.dart';

class TestRunnerService {
  static const int _timeoutMs = 5000; // 5 seconds timeout per test

  /// Runs a test suite against the provided user code
  static Future<TestRunResult> runTests({
    required String userCode,
    TestSuite? testSuite,
  }) async {
    final results = <TestResult>[];
    final stopwatch = Stopwatch()..start();

    for (final testCase in (testSuite?.testCases ?? [])) {
      final result = await _runSingleTest(
        userCode: userCode,
        testCase: testCase,
        functionName: testSuite?.functionName ?? "",
      );
      results.add(result);
    }

    stopwatch.stop();
    final passedCount = results.where((r) => r.passed).length;

    return TestRunResult(
      testSuite: testSuite,
      results: results,
      passedCount: passedCount,
      totalCount: results.length,
      totalExecutionTime: stopwatch.elapsed,
    );
  }

  static Future<TestResult> _runSingleTest({
    required String userCode,
    required TestCase testCase,
    required String functionName,
  }) async {
    final testStopwatch = Stopwatch()..start();

    try {
      // Create test code that calls the user's function with test inputs
      final testCode = _generateTestCode(
        userCode: userCode,
        functionName: functionName,
        inputs: testCase.inputs ?? [],
      );

      // Compile and execute with timeout
      final result = await _executeWithTimeout(testCode);
      testStopwatch.stop();

      // Parse the result and compare with exp ected output
      final actualOutput = _parseOutput(result);
      final passed = _compareOutputs(actualOutput, testCase.expectedOutput);

      return TestResult(
        testCase: testCase,
        actualOutput: actualOutput,
        passed: passed,
        executionTime: testStopwatch.elapsed,
      );
    } catch (e) {
      testStopwatch.stop();
      return TestResult(
        testCase: testCase,
        actualOutput: null,
        passed: false,
        errorMessage: e.toString(),
        executionTime: testStopwatch.elapsed,
      );
    }
  }

  static String _generateTestCode({
    required String userCode,
    required String functionName,
    required List<dynamic> inputs,
  }) {
    final inputsStr = inputs.map(_formatInput).join(', ');

    // Remove any existing main function from user code
    final cleanedUserCode = _removeMainFunction(userCode);

    return '''
$cleanedUserCode

void main() {
  try {
    final result = $functionName($inputsStr);
    print('RESULT:\${_serializeResult(result)}');
  } catch (e) {
    print('ERROR:\$e');
  }
}

String _serializeResult(dynamic result) {
  if (result is List) {
    return '[' + result.map((e) => e.toString()).join(',') + ']';
  }
  return result.toString();
}
''';
  }

  static String _removeMainFunction(String code) {
    // Remove main function and its body using regex
    // This regex matches: void main() { ... } including nested braces
    final mainFunctionRegex = RegExp(
      r'void\s+main\s*\([^)]*\)\s*\{',
      multiLine: true,
    );

    final match = mainFunctionRegex.firstMatch(code);
    if (match == null) {
      return code; // No main function found
    }

    // Find the matching closing brace
    int braceCount = 0;
    int start = match.start;
    int i = match.end - 1; // Start from the opening brace

    while (i < code.length) {
      if (code[i] == '{') {
        braceCount++;
      } else if (code[i] == '}') {
        braceCount--;
        if (braceCount == 0) {
          // Found the matching closing brace
          return code.substring(0, start) + code.substring(i + 1);
        }
      }
      i++;
    }

    // If we couldn't find matching braces, just remove from start to end
    return code.substring(0, start);
  }

  static String _formatInput(dynamic input) {
    if (input is String) {
      return '"$input"';
    } else if (input is List) {
      final elements = input.map(_formatInput).join(', ');
      return '[$elements]';
    }
    return input.toString();
  }

  static Future<String> _executeWithTimeout(String code) async {
    final completer = Completer<String>();
    String output = '';

    final timer = Timer(Duration(milliseconds: _timeoutMs), () {
      if (!completer.isCompleted) {
        completer.completeError('Test timed out after ${_timeoutMs}ms');
      }
    });

    try {
      final compiler = Compiler();
      final program = compiler.compileWriteAndLoad({
        'dart_coder': {
          'main.dart': code,
        }
      });

      runZoned(
        () async {
          try {
            final result =
                program.executeLib('package:dart_coder/main.dart', 'main');
            if (result is Future) {
              await result;
            }
            timer.cancel();
            if (!completer.isCompleted) {
              completer.complete(output);
            }
          } catch (e) {
            timer.cancel();
            if (!completer.isCompleted) {
              completer.completeError('Runtime Error: $e');
            }
          }
        },
        zoneSpecification: ZoneSpecification(
          handleUncaughtError: (self, parent, zone, error, stackTrace) {
            timer.cancel();
            if (!completer.isCompleted) {
              completer.completeError('Runtime Error: $error');
            }
          },
          print: (self, parent, zone, line) {
            output += '$line\n';
          },
        ),
      );
    } catch (e) {
      timer.cancel();
      if (!completer.isCompleted) {
        final errorMsg = e is CompileError ? e.message : e.toString();
        completer.completeError('Compilation Error: $errorMsg');
      }
    }

    return completer.future;
  }

  static dynamic _parseOutput(String output) {
    try {
      final lines = output.split('\n');
      for (final line in lines) {
        if (line.startsWith('RESULT:')) {
          final resultStr = line.substring(7);
          return _deserializeResult(resultStr);
        } else if (line.startsWith('ERROR:')) {
          throw Exception(line.substring(6));
        }
      }
      return null;
    } catch (e) {
      throw Exception('Failed to parse output: $e');
    }
  }

  static dynamic _deserializeResult(String resultStr) {
    // Handle list results like [0,1]
    if (resultStr.startsWith('[') && resultStr.endsWith(']')) {
      final content = resultStr.substring(1, resultStr.length - 1);
      if (content.isEmpty) return [];

      return content.split(',').map((s) {
        final trimmed = s.trim();
        if (int.tryParse(trimmed) != null) {
          return int.parse(trimmed);
        } else if (double.tryParse(trimmed) != null) {
          return double.parse(trimmed);
        }
        return trimmed;
      }).toList();
    }

    // Handle primitive results
    if (int.tryParse(resultStr) != null) {
      return int.parse(resultStr);
    } else if (double.tryParse(resultStr) != null) {
      return double.parse(resultStr);
    } else if (resultStr.toLowerCase() == 'true') {
      return true;
    } else if (resultStr.toLowerCase() == 'false') {
      return false;
    }

    return resultStr;
  }

  static bool _compareOutputs(dynamic actual, dynamic expected) {
    if (actual == null && expected == null) return true;
    if (actual == null || expected == null) return false;

    if (actual is List && expected is List) {
      if (actual.length != expected.length) return false;
      for (int i = 0; i < actual.length; i++) {
        if (!_compareOutputs(actual[i], expected[i])) return false;
      }
      return true;
    }

    return actual.toString() == expected.toString();
  }
}
