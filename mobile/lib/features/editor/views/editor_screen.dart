import 'dart:async';

import 'package:dart_eval/dart_eval.dart';
import 'package:dart_eval/dart_eval_bridge.dart';
import 'package:dart_style/dart_style.dart';
import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/editor/models/dsa_list_model.dart';
import 'package:dartcoder/features/editor/models/test_case.dart';
import 'package:dartcoder/features/editor/view_model/editor_cubit.dart';
import 'package:dartcoder/features/editor/views/widgets/dsa_question_widget.dart';
import 'package:dartcoder/features/editor/views/widgets/test_results_widget.dart';
import 'package:dartcoder/main.dart';
import 'package:dartcoder/services/test_runner_service.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/text_editor.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart';
import 'package:flutter_highlight/themes/atom-one-light.dart';
import 'package:flutter_highlight/themes/nord.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:highlight/languages/dart.dart';

class EditorScreen extends StatefulWidget {
  const EditorScreen({super.key, this.arg});

  final EditorScreenArg? arg;
  @override
  State<EditorScreen> createState() => _EditorScreenState();
}

class _EditorScreenState extends State<EditorScreen>
    with SingleTickerProviderStateMixin {
  final controller = CodeController(
    language: dart,
  );

  final _outputNotifier = ValueNotifier<String>("");
  final _testResultNotifier = ValueNotifier<TestRunResult?>(null);
  final _isTestingNotifier = ValueNotifier<bool>(false);
  late final TabController _tabController;

  void _listen() => setState(() {});

  Timer? _debounce;

  final baseCode = '''void main() {
  print("Hello, Dartic!");
}''';

  @override
  void initState() {
    controller.text =
        cacheService.getCode(key: widget.arg?.dsa?.id) ?? baseCode;

    editor.setText(controller.fullText, key: widget.arg?.dsa?.id);
    _tabController =
        TabController(length: widget.arg?.dsa != null ? 4 : 2, vsync: this)
          ..addListener(_listen);

    controller.addListener(() {
      final text = controller.text;
      final selection = controller.selection;

      if (text.isNotEmpty &&
          selection.baseOffset > 1 &&
          selection.baseOffset <= text.length &&
          text[selection.baseOffset - 1] == '\n') {
        // Check for newline insertion
        final prevLine = getPreviousLine(text, selection.baseOffset);
        final leadingSpaces = getLeadingSpaces(prevLine);

        // Insert two spaces + whatever indent the previous line had
        final newText = text.replaceRange(
          selection.baseOffset,
          selection.baseOffset,
          '$leadingSpaces  ', // you can replace with '\t' if you prefer real tabs
        );

        controller.value = TextEditingValue(
          text: newText,
          selection: TextSelection.collapsed(
            offset: selection.baseOffset + 2,
          ),
        );
      }
    });

    if (widget.arg?.dsa != null) {
      context.read<EditorCubit>().getProblemsForDSA(widget.arg?.dsa?.id ?? "");
    }
    super.initState();
  }

  @override
  void dispose() {
    _tabController.removeListener(_listen);
    _debounce?.cancel();
    _outputNotifier.dispose();
    _testResultNotifier.dispose();
    _isTestingNotifier.dispose();
    super.dispose();
  }

  bool _isSubstantialChange(String oldText, String newText) {
    if (newText.trim() == oldText.trim()) return false;
    if ((newText.length - oldText.length).abs() < 5) return false;
    return true;
  }

  void _onTextChanged(String newText) {
    if (_debounce?.isActive ?? false) _debounce!.cancel();

    _debounce = Timer(const Duration(milliseconds: 500), () {
      if (_isSubstantialChange(editor.text, newText)) {
        editor.setText(newText, key: widget.arg?.dsa?.id);
      }
    });
  }

  Future<void> _runCode() async {
    cacheService.saveCode(controller.fullText, key: widget.arg?.dsa?.id);
    _tabController.animateTo(widget.arg?.dsa != null ? 2 : 1);
    _unfocus();
    _outputNotifier.value = "";

    try {
      final compiler = Compiler();
      final program = compiler.compileWriteAndLoad({
        'dart_coder': {
          'main.dart': controller.fullText,
        }
      });

      await runZoned(
        () async {
          try {
            final result =
                program.executeLib('package:dart_coder/main.dart', 'main');

            if (result is Future) {
              await result;
            }
          } catch (e, stackTrace) {
            _outputNotifier.value += 'Runtime Error: $e\n';
            _outputNotifier.value += 'Stack Trace: $stackTrace\n';
          }
        },
        zoneSpecification: ZoneSpecification(
          handleUncaughtError: (self, parent, zone, error, stackTrace) {
            _outputNotifier.value += 'Uncaught Error: $error\n';
            _outputNotifier.value += 'Stack Trace: $stackTrace\n';
          },
          print: (self, parent, zone, line) {
            _outputNotifier.value += '$line\n';
          },
        ),
      );
    } catch (e) {
      _outputNotifier.value =
          e is CompileError ? e.message : "Error: ${e.toString()}";
    }
  }

  Future<void> _runTests() async {
    if (widget.arg?.dsa == null) return;

    cacheService.saveCode(controller.fullText, key: widget.arg?.dsa?.id);
    _tabController.animateTo(3); // Navigate to test results tab
    _unfocus();

    _isTestingNotifier.value = true;
    _testResultNotifier.value = null;

    try {
      final result = await TestRunnerService.runTests(
        userCode: controller.fullText,
        testSuite: testSuite,
      );
      _testResultNotifier.value = result;

      if (_testResultNotifier.value?.passedCount ==
          testSuite?.testCases?.length) {
        if (mounted) {
          context
              .read<AppCubit>()
              .markProblemAsSolved(widget.arg?.dsa?.id ?? "");
        }
      }
    } catch (e) {
      // Handle test execution error
      _testResultNotifier.value = TestRunResult(
        testSuite: testSuite,
        results: [],
        passedCount: 0,
        totalCount: 0,
        totalExecutionTime: Duration.zero,
      );
    } finally {
      _isTestingNotifier.value = false;
    }
  }

  String beautify(String i) {
    final importRegex = RegExp(r'import\s+[^;]+;', multiLine: true);

    final imports =
        importRegex.allMatches(i).map((m) => m.group(0)!.trim()).toSet();

    String cleanedCode = i.replaceAll(importRegex, "").trim();

    String formattedCode;
    try {
      formattedCode =
          DartFormatter(languageVersion: Version(3, 9, 2)).format(cleanedCode);
    } catch (_) {
      formattedCode = cleanedCode;
    }

    return '${imports.join("\n")}${imports.isNotEmpty ? "\n\n" : ""}$formattedCode';
  }

  void _unfocus() => FocusScope.of(context).unfocus();

  Widget? _buildFloatingActionButtons() {
    if (_tabController.index == (widget.arg?.dsa != null ? 1 : 0)) {
      // Code editor tab - show run and test buttons
      if (widget.arg?.dsa != null) {
        return Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            // Test button
            GestureDetector(
              onTap: _runTests,
              child: Container(
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Theme.of(context).primaryColor,
                  ),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.check,
                  size: 50,
                  color: Theme.of(context).primaryColor,
                ),
              ),
            ),
            const SizedBox(height: 16),
            // Run button
            GestureDetector(
              onTap: _runCode,
              child: Container(
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Theme.of(context).primaryColor,
                  ),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.play_arrow,
                  size: 50,
                  color: Theme.of(context).primaryColor,
                ),
              ),
            ),
          ],
        );
      } else {
        // Non-DSA mode - just run button
        return GestureDetector(
          onTap: _runCode,
          child: Container(
            decoration: BoxDecoration(
              border: Border.all(
                color: Theme.of(context).primaryColor,
              ),
              shape: BoxShape.circle,
            ),
            child: Icon(
              Icons.play_arrow,
              size: 50,
              color: Theme.of(context).primaryColor,
            ),
          ),
        );
      }
    }
    return null;
  }

  TestSuite? testSuite;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: _buildFloatingActionButtons(),
      appBar: AppBar(
        leadingWidth: 90,
        centerTitle: true,
        automaticallyImplyLeading:
            widget.arg?.isPractice == true || widget.arg?.dsa != null
                ? true
                : false,
        leading: (_tabController.index != 0)
            ? GestureDetector(
                onTap: () {
                  _tabController.animateTo(_tabController.index == 3
                      ? 2
                      : _tabController.index == 2
                          ? 1
                          : _tabController.index == 1
                              ? 0
                              : 0);
                },
                child: const Icon(Icons.arrow_back_ios),
              )
            : null,
        title: const Text('Dartic'),
        actions: _tabController.index == (widget.arg?.dsa != null ? 1 : 0)
            ? [
                ValueListenableBuilder(
                    valueListenable: editor.state,
                    builder: (_, state, __) {
                      return Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const SizedBox(
                            width: 20,
                          ),
                          GestureDetector(
                            onTap: state.canUndo
                                ? () {
                                    editor.undo(key: widget.arg?.dsa?.id);
                                    controller.text = editor.text;
                                  }
                                : null,
                            child: Icon(
                              color: state.canUndo
                                  ? null
                                  : Theme.of(context)
                                      .iconTheme
                                      .color
                                      ?.withValues(alpha: .5),
                              Icons.undo,
                              size: 30,
                            ),
                          ),
                          const SizedBox(
                            width: 10,
                          ),
                          GestureDetector(
                            onTap: state.canRedo
                                ? () {
                                    editor.redo(key: widget.arg?.dsa?.id);
                                    controller.text = editor.text;
                                  }
                                : null,
                            child: Icon(
                              color: state.canRedo
                                  ? null
                                  : Theme.of(context)
                                      .iconTheme
                                      .color
                                      ?.withValues(alpha: .5),
                              Icons.redo,
                              size: 30,
                            ),
                          ),
                        ],
                      );
                    }),
                PopupMenuButton(
                  initialValue: null,
                  onSelected: (v) {
                    if (v == "clear") {
                      editor.setText(baseCode, key: widget.arg?.dsa?.id);
                      controller.text = baseCode;
                    } else if (v == "format") {
                      controller.text = beautify(controller.text);
                    } else if (v == "solution") {
                      controller.text = beautify(testSuite?.answer ?? "");
                    }
                  },
                  itemBuilder: (BuildContext context) => <PopupMenuEntry>[
                    const PopupMenuItem(value: "clear", child: Text('Clear')),
                    const PopupMenuItem(
                        value: "format", child: Text('Beautify')),
                    if (widget.arg?.dsa != null &&
                        testSuite?.answer?.isNotEmpty == true)
                      const PopupMenuItem(
                          value: "solution", child: Text('Solution')),
                  ],
                  child: const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 20.0),
                    child: Icon(
                      Icons.more_vert,
                      size: 30,
                    ),
                  ),
                ),
              ]
            : null,
      ),
      body: BlocConsumer<EditorCubit, EditorState>(listener: (context, state) {
        if (state is EditorProblem) {
          Future.delayed(Duration(milliseconds: 1000), () {
            if (widget.arg?.dsa != null &&
                controller.text.contains(testSuite?.functionName ?? "") ==
                    false) {
              if (widget.arg?.dsa != null &&
                  controller.text.contains(testSuite?.functionName ?? "") ==
                      false) {
                controller.text = '''void main() {
  print("Hello, Dartic!");
}

 ${testSuite?.functionName}() {
  // Write your code here and specify the return type
}
''';
              }
            }
          });
        }
      }, builder: (_, state) {
        if (state is EditorProblem) {
          testSuite = state.problem;
        }
        return SizedBox(
          height: double.infinity,
          width: double.infinity,
          child: Stack(
            children: [
              Padding(
                padding: EdgeInsets.only(top: 10.0, bottom: 10.h),
                child: Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(bottom: 10.0),
                      child: TabBar(
                        controller: _tabController,
                        splashFactory: NoSplash.splashFactory,
                        indicator: const BoxDecoration(),
                        dividerColor: Colors.transparent,
                        tabs: [
                          if (widget.arg?.dsa != null) Text("Question"),
                          Text("Code"),
                          Text("Output"),
                          if (widget.arg?.dsa != null) Text("Tests"),
                        ],
                      ),
                    ),
                    Expanded(
                      child: TabBarView(controller: _tabController, children: [
                        if (widget.arg?.dsa != null)
                          DsaQuestionWidget(text: testSuite?.question ?? ""),
                        ValueListenableBuilder(
                            valueListenable: isDarkTheme,
                            builder: (_, isDark, __) {
                              return CodeTheme(
                                data: CodeThemeData(
                                    styles:
                                        isDark ? nordTheme : atomOneLightTheme),
                                child: Container(
                                  color: isDark
                                      ? const Color(0xff2E3440)
                                      : const Color(0xfffafafa),
                                  child: CodeField(
                                    expands: true,
                                    onChanged: _onTextChanged,
                                    gutterStyle: const GutterStyle(
                                      showFoldingHandles: false,
                                      width: 70,
                                    ),
                                    controller: controller,
                                  ),
                                ),
                              );
                            }),
                        ValueListenableBuilder(
                            valueListenable: _outputNotifier,
                            builder: (_, output, __) {
                              return SingleChildScrollView(
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 20, vertical: 20),
                                  child: Text(output),
                                ),
                              );
                            }),
                        if (widget.arg?.dsa != null)
                          ValueListenableBuilder<bool>(
                            valueListenable: _isTestingNotifier,
                            builder: (_, isTesting, __) {
                              return ValueListenableBuilder<TestRunResult?>(
                                valueListenable: _testResultNotifier,
                                builder: (_, testResult, __) {
                                  return TestResultsWidget(
                                    testResult: testResult,
                                    isLoading: isTesting,
                                  );
                                },
                              );
                            },
                          ),
                      ]),
                    ),
                  ],
                ),
              ),
              if (state is EditorLoadingProblems) loadingWidget(context)
            ],
          ),
        );
      }),
    );
  }
}

class EditorScreenArg {
  EditorScreenArg({this.dsa, this.isPractice});
  final bool? isPractice;
  final DsaListModel? dsa;
}
