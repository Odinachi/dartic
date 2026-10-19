/// Gives untagged fenced code blocks a `dart` language tag.
///
/// markdown_widget logs "get language error" for every fence without a
/// language and renders it as plain text. Every code sample in Dartic is
/// Dart, so tagging them silences the log and turns on syntax highlighting.
/// Closing fences and fences that already name a language are left alone.
String tagUntaggedCodeFences(String markdown) {
  final fence = RegExp(r'^(\s*)(`{3,}|~{3,})(.*)$');
  final out = <String>[];
  String? openFence;
  for (final line in markdown.split('\n')) {
    final match = fence.firstMatch(line);
    if (match == null) {
      out.add(line);
    } else if (openFence == null) {
      openFence = match.group(2);
      final info = match.group(3)!.trim();
      out.add(info.isEmpty ? '${match.group(1)}${match.group(2)}dart' : line);
    } else {
      // A closing fence uses the same character, at least as long, no info.
      final marker = match.group(2)!;
      if (marker[0] == openFence[0] &&
          marker.length >= openFence.length &&
          match.group(3)!.trim().isEmpty) {
        openFence = null;
      }
      out.add(line);
    }
  }
  return out.join('\n');
}
