import 'package:flutter/cupertino.dart';

import '../services/cache_service.dart';

/// Undo/redo history for one editor screen. Each EditorScreen owns its own
/// instance, so screens don't share history or notify each other's widgets.
class TextEditor {
  TextEditor({required this.cacheService});

  final CacheService cacheService;

  final state = ValueNotifier(TextEditorState(
      undoStack: [],
      redoStack: [],
      currentText: "",
      canUndo: false,
      canRedo: false));

  String _currentText = "";

  void setText(String newText, {String? key}) {
    state.value.undoStack.add(_currentText);
    _currentText = newText;
    state.value.redoStack.clear();

    _updateNotifier(key: key);
  }

  void undo({String? key}) {
    if (state.value.undoStack.isNotEmpty) {
      state.value.redoStack.add(_currentText);
      _currentText = state.value.undoStack.removeLast();

      _updateNotifier(key: key);
    }
  }

  void redo({String? key}) {
    if (state.value.redoStack.isNotEmpty) {
      state.value.undoStack.add(_currentText);
      _currentText = state.value.redoStack.removeLast();

      _updateNotifier(key: key);
    }
  }

  String get text => _currentText;

  void dispose() => state.dispose();

  void _updateNotifier({String? key}) {
    state.value = TextEditorState(
      undoStack: List.from(state.value.undoStack),
      redoStack: List.from(state.value.redoStack),
      currentText: _currentText,
      canUndo: state.value.undoStack.length > 1,
      canRedo: state.value.redoStack.isNotEmpty,
    );
    cacheService.saveCode(
      _currentText,
      key: key,
    );
  }
}

class TextEditorState {
  final List<String> undoStack;
  final List<String> redoStack;
  final String currentText;
  final bool canUndo;
  final bool canRedo;

  TextEditorState({
    required this.undoStack,
    required this.redoStack,
    required this.currentText,
    required this.canUndo,
    required this.canRedo,
  });
}

String getPreviousLine(String text, int offset) {
  final lines = text.substring(0, offset).split('\n');
  return lines.isNotEmpty ? lines.last : "";
}

String getLeadingSpaces(String line) {
  final match = RegExp(r'^(\s*)').firstMatch(line);
  return match?.group(0) ?? "";
}
