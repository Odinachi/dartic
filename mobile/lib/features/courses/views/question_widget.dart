import 'package:dartcoder/main.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';

class QuestionWidget extends StatefulWidget {
  const QuestionWidget({
    super.key,
    required this.question,
    required this.answerType,
    this.userAnswer,
    this.onType,
  });
  final String question;
  final String answerType;
  final dynamic userAnswer;
  final Function(int, String)? onType;

  @override
  State<QuestionWidget> createState() => _QuestionWidgetState();
}

class _QuestionWidgetState extends State<QuestionWidget> {
  @override
  Widget build(BuildContext context) {
    return _buildQuestionContent();
  }

  Widget _buildQuestionContent() {
    final parts = _parseQuestionText(widget.question);

    return RichText(
      text: TextSpan(
        children: parts.map((part) {
          if (part['isCode'] == true) {
            return WidgetSpan(
              child: Container(
                width: double.infinity,
                margin: const EdgeInsets.symmetric(vertical: 8.0),
                padding: const EdgeInsets.all(12.0),
                decoration: BoxDecoration(
                  color: isDarkTheme.value
                      ? AppColors.grey[800]
                      : AppColors.grey[200],
                  borderRadius: BorderRadius.circular(6.0),
                ),
                child: _buildCodeContent(part['text'] ?? ""),
              ),
            );
          } else {
            return TextSpan(
                text: part['text'] ?? "",
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(fontSize: 18));
          }
        }).toList(),
      ),
    );
  }

  Widget _buildCodeContent(String codeText) {
    final List<InlineSpan> codeSpans = [];
    final RegExp placeholderRegex = RegExp(r'(%order%|%fill%)');

    int lastEnd = 0;

    int currentOrder = 0;
    int currentFillIndex = 0;

    for (final match in placeholderRegex.allMatches(codeText)) {
      // Add syntax highlighted text before placeholder
      if (match.start > lastEnd) {
        codeSpans.addAll(_buildSyntaxHighlightedSpans(
          codeText.substring(lastEnd, match.start),
        ));
      }

      // Add interactive element for placeholder
      String placeholder = match.group(0)!;
      if (placeholder == '%order%') {
        currentOrder += 1;

        final answer = widget.userAnswer;

        final hasInput =
            (answer != null && answer is List && answer.length >= currentOrder);

        if (hasInput) {
          codeSpans.add(WidgetSpan(
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  height: 30,
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  margin: const EdgeInsets.symmetric(horizontal: 2),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(4),
                    color: AppColors.appBlue.withValues(alpha: .2),
                    border: Border.all(
                        color: AppColors.appBlue.withValues(alpha: .5)),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.grey.withValues(alpha: .05),
                        blurRadius: 8,
                        spreadRadius: 2,
                        offset: const Offset(0, 4),
                      ),
                      BoxShadow(
                        color: AppColors.grey.withValues(alpha: .01),
                        blurRadius: 4,
                        spreadRadius: 1,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: hasInput
                      ? Center(
                          child: Text(
                            hasInput ? answer[currentOrder - 1] : '',
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(fontSize: 12),
                          ),
                        )
                      : null,
                ),
              ],
            ),
          ));
        } else {
          codeSpans.add(WidgetSpan(
            child: Container(
              width: 60,
              height: 30,
              margin: const EdgeInsets.symmetric(horizontal: 2),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(4),
                border: Border.all(color: Colors.grey),
              ),
            ),
          ));
        }
      } else if (placeholder == '%fill%') {
        final fillIndex = currentFillIndex; // Capture current index
        codeSpans.add(WidgetSpan(
          child: Container(
            constraints: const BoxConstraints(minWidth: 60, maxWidth: 150),
            height: 30,
            margin: const EdgeInsets.symmetric(horizontal: 2),
            child: IntrinsicWidth(
              child: TextFormField(
                maxLines: 1,
                textInputAction: TextInputAction.done,
                initialValue: (widget.userAnswer != null &&
                        widget.userAnswer is List &&
                        widget.userAnswer.length > fillIndex)
                    ? widget.userAnswer[fillIndex]
                    : '',
                onChanged: (newValue) {
                  if (widget.onType != null) {
                    widget.onType!(fillIndex, newValue);
                  }
                },
                onFieldSubmitted: (newValue) {
                  if (widget.onType != null) {
                    widget.onType!(fillIndex, newValue);
                  }
                },
                style: const TextStyle(fontSize: 12),
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  contentPadding: EdgeInsets.all(4),
                  isDense: true,
                ),
              ),
            ),
          ),
        ));
        currentFillIndex += 1;
      }

      lastEnd = match.end;
    }

    // Add remaining syntax highlighted text
    if (lastEnd < codeText.length) {
      codeSpans.addAll(_buildSyntaxHighlightedSpans(
        codeText.substring(lastEnd),
      ));
    }

    return RichText(
      text: TextSpan(children: codeSpans),
    );
  }

  List<InlineSpan> _buildSyntaxHighlightedSpans(String text) {
    final List<InlineSpan> spans = [];
    final RegExp improvedTokenRegex = RegExp(
        // GROUP 1: Type Keywords
        r"(void|int|double|bool|String|var|const|final)\b"

        // GROUP 2: Access Modifiers
        r"|(public|private|protected|static|abstract)\b"

        // GROUP 3: Control Flow Keywords
        r"|(if|else|for|while|return)\b"

        // GROUP 4: Object-Oriented Keywords
        r"|(class|extends|implements)\b"

        // GROUP 5: Built-in Functions
        r"|(main|print)\b"

        // GROUP 7: Punctuation
        r"|([{}();,.])"

        // GROUP 8: Numbers
        r"|(\d+\.?\d*)"

        // GROUP 9: User-defined Identifiers
        r"|([A-Za-z_]\w*)"

        // GROUP 10: Whitespace
        r"|(\s+)");

    int lastEnd = 0;
    for (final match in improvedTokenRegex.allMatches(text)) {
      if (match.start > lastEnd) {
        spans.add(TextSpan(
          text: text.substring(lastEnd, match.start),
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.white70 : Colors.black87,
          ),
        ));
      }

      final token = match.group(0)!;

      if (match.group(1) != null) {
        // Type Keywords - Blue/Purple
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: Colors.purpleAccent,
            fontWeight: FontWeight.bold,
          ),
        ));
      } else if (match.group(2) != null) {
        // Access Modifiers - Orange

        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.orange[300] : Colors.orange[700],
            fontWeight: FontWeight.bold,
          ),
        ));
      } else if (match.group(3) != null) {
        // Control Flow Keywords - Purple/Magenta
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.purple[300] : Colors.purple[700],
            fontWeight: FontWeight.bold,
          ),
        ));
      } else if (match.group(4) != null) {
        // Object-Oriented Keywords - Teal
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.teal[300] : Colors.teal[700],
            fontWeight: FontWeight.bold,
          ),
        ));
      } else if (match.group(5) != null) {
        // Built-in Functions - Green

        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: Colors.blueAccent,
            fontWeight: FontWeight.bold,
          ),
        ));
      } else if (match.group(7) != null) {
        // Punctuation - Yellow/Amber
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.amber[300] : Colors.amber[800],
          ),
        ));
      } else if (match.group(8) != null) {
        // Numbers - Light Green
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value
                ? Colors.lightGreen[300]
                : Colors.lightGreen[700],
          ),
        ));
      } else if (match.group(9) != null) {
        // Identifiers - Cyan
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.cyan[300] : Colors.cyan[700],
          ),
        ));
      }

      // else if (match.group(10) != null) {
      //   // Whitespace
      //   spans.add(TextSpan(
      //     text: token,
      //     style: _getCodeTextStyle(),
      //   ));
      // }
      else {
        // Fallback
        spans.add(TextSpan(
          text: token,
          style: _getCodeTextStyle().copyWith(
            color: isDarkTheme.value ? Colors.white70 : Colors.black87,
          ),
        ));
      }

      lastEnd = match.end;
    }

    // Add any remaining text that wasn't matched
    if (lastEnd < text.length) {
      spans.add(TextSpan(
        text: text.substring(lastEnd),
        style: _getCodeTextStyle().copyWith(
          color: isDarkTheme.value ? Colors.white70 : Colors.black87,
        ),
      ));
    }

    return spans;
  }

  TextStyle _getCodeTextStyle() {
    return Theme.of(context).textTheme.bodyMedium?.copyWith(
              fontFamily: 'Courier',
              fontSize: 16,
            ) ??
        const TextStyle(fontFamily: 'Courier', fontSize: 16);
  }

  List<Map<String, dynamic>> _parseQuestionText(String text) {
    final List<Map<String, dynamic>> parts = [];
    final RegExp codeBlockRegex =
        RegExp(r'```(\w+)?\n(.*?)\n```', dotAll: true);

    int lastEnd = 0;
    for (final match in codeBlockRegex.allMatches(text)) {
      // Add text before code block
      if (match.start > lastEnd) {
        parts.add({
          'text': text.substring(lastEnd, match.start),
          'isCode': false,
        });
      }

      // Add code block without replacing placeholders
      String codeText = match.group(2)!;

      parts.add({
        'text': codeText,
        'isCode': true,
      });

      lastEnd = match.end;
    }

    // Add remaining text
    if (lastEnd < text.length) {
      parts.add({
        'text': text.substring(lastEnd),
        'isCode': false,
      });
    }

    return parts.isEmpty
        ? [
            {'text': text, 'isCode': false}
          ]
        : parts;
  }
}
