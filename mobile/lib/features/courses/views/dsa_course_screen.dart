import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dartcoder/features/courses/models/dsa_course_model.dart';
import 'package:dartcoder/features/courses/views/course_quiz.dart';
import 'package:dartcoder/features/courses/views/widget/video_player.dart';
import 'package:dartcoder/main.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:markdown_widget/markdown_widget.dart';

// ─────────────────────────────────────────────────────
//  LESSON LIST (paginated, filterable by module)
// ─────────────────────────────────────────────────────

class DsaCourseListScreen extends StatefulWidget {
  const DsaCourseListScreen({super.key});

  @override
  State<DsaCourseListScreen> createState() => _DsaCourseListScreenState();
}

class _DsaCourseListScreenState extends State<DsaCourseListScreen> {
  static const _pageSize = 10;

  final _scrollController = ScrollController();
  List<DsaModule> _modules = [];
  int? _selectedModule; // null = all modules

  final _lessons = <DsaCourseModel>[];
  DocumentSnapshot? _lastDocument;
  bool _hasMore = true;
  bool _loading = true;
  bool _loadingMore = false;
  String? _error;

  // Ignores responses from a previous filter if the user switches quickly.
  int _requestId = 0;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    _loadModules();
    _loadFirstPage();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _loadModules() async {
    final result = await firebaseService.fetchDsaModules();
    if (!mounted || result.modules == null) return;
    setState(() => _modules = result.modules!);
  }

  Future<void> _loadFirstPage() async {
    final request = ++_requestId;
    setState(() {
      _loading = true;
      _error = null;
      _lessons.clear();
      _lastDocument = null;
      _hasMore = true;
    });
    final result = await firebaseService.fetchDsaCoursePage(
        module: _selectedModule, limit: _pageSize);
    if (!mounted || request != _requestId) return;
    setState(() {
      _loading = false;
      _error = result.error;
      final page = result.lessons ?? const <DsaCourseModel>[];
      _lessons.addAll(page);
      _lastDocument = result.lastDocument;
      _hasMore = page.length == _pageSize;
    });
  }

  Future<void> _loadMore() async {
    if (_loading || _loadingMore || !_hasMore || _lastDocument == null) return;
    final request = _requestId;
    setState(() => _loadingMore = true);
    final result = await firebaseService.fetchDsaCoursePage(
      module: _selectedModule,
      limit: _pageSize,
      startAfterDocument: _lastDocument,
    );
    if (!mounted || request != _requestId) return;
    setState(() {
      _loadingMore = false;
      if (result.error != null) {
        _hasMore =
            false; // stop retrying automatically; pull to refresh retries
        return;
      }
      final page = result.lessons!;
      _lessons.addAll(page);
      _lastDocument = result.lastDocument ?? _lastDocument;
      _hasMore = page.length == _pageSize;
    });
  }

  void _onScroll() {
    final position = _scrollController.position;
    if (position.pixels >= position.maxScrollExtent - 300) _loadMore();
  }

  void _selectModule(int? module) {
    if (module == _selectedModule) return;
    setState(() => _selectedModule = module);
    if (_scrollController.hasClients) _scrollController.jumpTo(0);
    _loadFirstPage();
  }

  @override
  Widget build(BuildContext context) {
    final totalLessons = _modules.fold(0, (total, m) => total + m.lessonCount);
    return Scaffold(
      appBar: AppBar(title: const Text(AppString.dataStructures)),
      body: RefreshIndicator(
        onRefresh: () async {
          await Future.wait([_loadModules(), _loadFirstPage()]);
        },
        child: CustomScrollView(
          controller: _scrollController,
          physics: const AlwaysScrollableScrollPhysics(),
          slivers: [
            SliverPadding(
              padding: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 0),
              sliver: SliverToBoxAdapter(
                child: FadeSlideIn(
                  child: _Hero(
                    lessonCount: totalLessons,
                    moduleCount: _modules.length,
                  ),
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: _ModuleFilter(
                modules: _modules,
                selected: _selectedModule,
                onSelect: _selectModule,
              ),
            ),
            ..._buildBody(),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildBody() {
    if (_loading) {
      return [
        SliverPadding(
          padding: EdgeInsets.symmetric(horizontal: 20.w),
          sliver: SliverList.list(children: [
            for (var i = 0; i < 5; i++) ...[
              SkeletonBox(height: 84.h, radius: 16.r),
              SizedBox(height: 12.h),
            ],
          ]),
        ),
      ];
    }
    if (_error != null || _lessons.isEmpty) {
      return [
        SliverFillRemaining(
          hasScrollBody: false,
          child: _Message(
            icon: _error != null
                ? Icons.cloud_off_rounded
                : Icons.inventory_2_outlined,
            title: _error != null ? "Couldn't load lessons" : 'No lessons yet',
            subtitle: _error != null
                ? 'Check your connection and try again.'
                : 'New data structure lessons are on the way.',
            onRetry: _loadFirstPage,
          ),
        ),
      ];
    }
    return [
      SliverPadding(
        padding: EdgeInsets.fromLTRB(20.w, 0, 20.w, 32.h),
        sliver: SliverList.builder(
          itemCount: _lessons.length + 1,
          itemBuilder: (_, i) {
            if (i == _lessons.length) return _ListFooter(loading: _hasMore);
            final lesson = _lessons[i];
            final previous = i == 0 ? null : _lessons[i - 1];
            final startsModule =
                _selectedModule == null && previous?.module != lesson.module;
            return FadeSlideIn(
              key: ValueKey('${_selectedModule}_${lesson.id}'),
              delay: FadeSlideIn.stagger(i % _pageSize, stepMs: 40),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (startsModule) _ModuleHeading(lesson: lesson),
                  _LessonCard(
                    lesson: lesson,
                    onTap: () => AppRouter.push(
                      AppRouter.dsaCourseDetails,
                      arg: DsaCourseDetailsArgs(
                          lessons: List.of(_lessons), index: i),
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    ];
  }
}

class _Hero extends StatelessWidget {
  const _Hero({required this.lessonCount, required this.moduleCount});
  final int lessonCount;
  final int moduleCount;

  @override
  Widget build(BuildContext context) {
    final white80 = AppColors.white.withValues(alpha: .8);
    return Container(
      padding: EdgeInsets.all(18.r),
      decoration: BoxDecoration(
        gradient: AppColors.dataStructureGradient,
        borderRadius: BorderRadius.circular(20.r),
        boxShadow: [
          BoxShadow(
            color: AppColors.orange.withValues(alpha: .28),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Row(children: [
        Expanded(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            if (lessonCount > 0)
              Text('$moduleCount modules · $lessonCount lessons',
                  style: context.text.labelLarge?.copyWith(
                      fontSize: 11.sp, letterSpacing: .6, color: white80)),
            SizedBox(height: 6.h),
            Text('Data structures in Dart',
                style: context.text.headlineSmall
                    ?.copyWith(fontSize: 21.sp, color: AppColors.white)),
            SizedBox(height: 6.h),
            Text('From Big O to graphs, trees and dynamic programming.',
                style: context.text.bodyMedium
                    ?.copyWith(fontSize: 12.5.sp, height: 1.4, color: white80)),
          ]),
        ),
        SizedBox(width: 12.w),
        Container(
          width: 56.r,
          height: 56.r,
          decoration: BoxDecoration(
            color: AppColors.white.withValues(alpha: .18),
            borderRadius: BorderRadius.circular(16.r),
          ),
          child: Icon(Icons.account_tree_rounded,
              size: 28.sp, color: AppColors.white),
        ),
      ]),
    );
  }
}

class _ModuleFilter extends StatelessWidget {
  const _ModuleFilter({
    required this.modules,
    required this.selected,
    required this.onSelect,
  });
  final List<DsaModule> modules;
  final int? selected;
  final ValueChanged<int?> onSelect;

  @override
  Widget build(BuildContext context) {
    final options = <(int?, String)>[
      (null, 'All'),
      for (final m in modules) (m.module, m.title),
    ];
    return SizedBox(
      height: 62.h,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 14.h),
        itemCount: options.length,
        separatorBuilder: (_, __) => SizedBox(width: 8.w),
        itemBuilder: (_, i) {
          final (module, label) = options[i];
          final isSelected = module == selected;
          final palette = context.palette;
          return Pressable(
            onTap: () => onSelect(module),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: EdgeInsets.symmetric(horizontal: 14.w),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: isSelected
                    ? AppColors.orange.withValues(alpha: .15)
                    : palette.surface,
                borderRadius: BorderRadius.circular(100),
                border: Border.all(
                    color: isSelected
                        ? AppColors.orange.withValues(alpha: .7)
                        : palette.border),
              ),
              child: Text(
                module == null ? label : '$module · $label',
                style: context.text.labelLarge?.copyWith(
                    fontSize: 13.sp,
                    color: isSelected ? AppColors.orange : palette.textPrimary),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _ModuleHeading extends StatelessWidget {
  const _ModuleHeading({required this.lesson});
  final DsaCourseModel lesson;

  @override
  Widget build(BuildContext context) => Padding(
        padding: EdgeInsets.only(top: 8.h, bottom: 12.h),
        child: Row(children: [
          Text('MODULE ${lesson.module ?? ''}',
              style: context.text.labelLarge?.copyWith(
                  fontSize: 10.sp,
                  letterSpacing: 1,
                  color: context.palette.textMuted)),
          SizedBox(width: 8.w),
          Expanded(
            child: Text(lesson.moduleTitle ?? '',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: context.text.titleMedium?.copyWith(fontSize: 15.sp)),
          ),
        ]),
      );
}

class _LessonCard extends StatelessWidget {
  const _LessonCard({required this.lesson, required this.onTap});
  final DsaCourseModel lesson;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    const color = AppColors.orange;
    final badge = lesson.module != null && lesson.lessonNumber != null
        ? '${lesson.module}.${lesson.lessonNumber}'
        : '•';
    return Padding(
      padding: EdgeInsets.only(bottom: 12.h),
      child: AppCard(
        onTap: onTap,
        padding: EdgeInsets.fromLTRB(14.w, 14.h, 10.w, 14.h),
        child: Row(children: [
          Container(
            width: 40.r,
            height: 40.r,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: color.withValues(alpha: .14),
              borderRadius: BorderRadius.circular(12.r),
            ),
            child: Text(badge,
                style: context.text.labelLarge
                    ?.copyWith(fontSize: 12.5.sp, color: color)),
          ),
          SizedBox(width: 12.w),
          Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(lesson.title ?? 'Lesson',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: context.text.titleMedium?.copyWith(fontSize: 14.5.sp)),
              if (lesson.desc != null) ...[
                SizedBox(height: 4.h),
                Text(lesson.desc!,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: context.text.bodySmall
                        ?.copyWith(fontSize: 12.sp, height: 1.4)),
              ],
              SizedBox(height: 8.h),
              Wrap(spacing: 6.w, runSpacing: 4.h, children: [
                if (lesson.readMinutes != null)
                  Tag('${lesson.readMinutes} min read',
                      color: palette.textMuted, icon: Icons.schedule_rounded),
                if (lesson.hasQuiz)
                  Tag('${lesson.questionCount} questions',
                      color: AppColors.violet, icon: Icons.quiz_rounded),
                if (lesson.videos.isNotEmpty)
                  Tag('${lesson.videos.length} video${lesson.videos.length == 1 ? '' : 's'}',
                      color: palette.textMuted, icon: Icons.play_arrow_rounded),
              ]),
            ]),
          ),
          Icon(Icons.chevron_right_rounded,
              size: 20.sp, color: palette.textMuted),
        ]),
      ),
    );
  }
}

class _ListFooter extends StatelessWidget {
  const _ListFooter({required this.loading});
  final bool loading;

  @override
  Widget build(BuildContext context) => Padding(
        padding: EdgeInsets.symmetric(vertical: 16.h),
        child: Center(
          child: loading
              ? SizedBox.square(
                  dimension: 22.r,
                  child: const CircularProgressIndicator(strokeWidth: 2.5),
                )
              : Text("You've reached the end 🎉",
                  style: context.text.bodySmall?.copyWith(fontSize: 12.sp)),
        ),
      );
}

class _Message extends StatelessWidget {
  const _Message({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onRetry,
  });
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 40.w, vertical: 24.h),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Icon(icon, size: 48.sp, color: context.palette.textMuted),
            SizedBox(height: 12.h),
            Text(title,
                style: context.text.titleMedium?.copyWith(fontSize: 16.sp)),
            SizedBox(height: 4.h),
            Text(subtitle,
                textAlign: TextAlign.center,
                style: context.text.bodySmall?.copyWith(fontSize: 13.sp)),
            SizedBox(height: 20.h),
            SizedBox(
              width: 140.w,
              child: AppButton(text: 'Try again', onTap: onRetry),
            ),
          ]),
        ),
      );
}

// ─────────────────────────────────────────────────────
//  LESSON DETAILS (content + quiz fetched on open)
// ─────────────────────────────────────────────────────

class DsaCourseDetailsArgs {
  /// The lessons loaded on the list screen, used for previous/next.
  final List<DsaCourseModel> lessons;
  final int index;
  DsaCourseDetailsArgs({required this.lessons, required this.index});
}

class DsaCourseDetailsScreen extends StatefulWidget {
  const DsaCourseDetailsScreen({super.key, required this.arg});
  final DsaCourseDetailsArgs arg;

  @override
  State<DsaCourseDetailsScreen> createState() => _DsaCourseDetailsScreenState();
}

class _DsaCourseDetailsScreenState extends State<DsaCourseDetailsScreen> {
  final scrollController = ScrollController();
  late int index = widget.arg.index;
  late Future<({DsaLessonContent? content, String? error})> _content =
      firebaseService.fetchDsaLessonContent(lesson.id);

  List<DsaCourseModel> get lessons => widget.arg.lessons;
  DsaCourseModel get lesson => lessons[index];

  void _goTo(int newIndex) {
    if (newIndex < 0 || newIndex >= lessons.length) return;
    setState(() {
      index = newIndex;
      _content = firebaseService.fetchDsaLessonContent(lesson.id);
    });
    if (scrollController.hasClients) scrollController.jumpTo(0);
  }

  void _retry() => setState(
      () => _content = firebaseService.fetchDsaLessonContent(lesson.id));

  @override
  void dispose() {
    scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    final isLast = index == lessons.length - 1;
    return FutureBuilder(
      future: _content,
      builder: (context, snapshot) {
        final loading = snapshot.connectionState != ConnectionState.done;
        final content = snapshot.data?.content;
        final error = snapshot.data?.error;
        return Scaffold(
          appBar: AppBar(
            title: Text(lesson.title ?? ''),
            bottom: PreferredSize(
              preferredSize: const Size.fromHeight(3),
              child: AnimatedBuilder(
                animation: scrollController,
                builder: (_, __) {
                  final position = scrollController.hasClients
                      ? scrollController.position
                      : null;
                  final max = position?.hasContentDimensions == true
                      ? position!.maxScrollExtent
                      : 0.0;
                  final read = max <= 0 ? 0.0 : position!.pixels / max;
                  return LinearProgressIndicator(
                    value: read.clamp(0.0, 1.0),
                    minHeight: 3,
                    color: AppColors.orange,
                    backgroundColor: Colors.transparent,
                  );
                },
              ),
            ),
          ),
          bottomNavigationBar: SafeArea(
            minimum: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 12.h),
            child: Row(children: [
              Pressable(
                onTap: index == 0 ? null : () => _goTo(index - 1),
                child: Opacity(
                  opacity: index == 0 ? .4 : 1,
                  child: Container(
                    width: 46.h,
                    height: 46.h,
                    decoration: BoxDecoration(
                      color: palette.surfaceAlt,
                      borderRadius: BorderRadius.circular(14.r),
                    ),
                    child: Icon(Icons.arrow_back_rounded,
                        size: 20.sp, color: palette.textPrimary),
                  ),
                ),
              ),
              if (content?.hasQuiz ?? false) ...[
                SizedBox(width: 8.w),
                Expanded(
                  child: AppButton(
                    text: AppString.takeQuiz,
                    backgroundColor: AppColors.violet.withValues(alpha: .14),
                    textColor: AppColors.violet,
                    onTap: () => AppRouter.push(AppRouter.quiz,
                        arg: CourseQuizArg(
                            questions: content!.quiz, title: lesson.title)),
                  ),
                ),
              ],
              SizedBox(width: 8.w),
              Expanded(
                child: AppButton(
                  text: isLast ? 'Finish' : AppString.next,
                  onTap: isLast ? AppRouter.pop : () => _goTo(index + 1),
                ),
              ),
            ]),
          ),
          body: SingleChildScrollView(
            key: ValueKey(lesson.id),
            controller: scrollController,
            padding: EdgeInsets.fromLTRB(20.w, 12.h, 20.w, 32.h),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Wrap(spacing: 6.w, runSpacing: 6.h, children: [
                if (lesson.module != null)
                  Tag('Module ${lesson.module} · Lesson ${lesson.lessonNumber}',
                      color: AppColors.orange),
                if (lesson.readMinutes != null)
                  Tag('${lesson.readMinutes} min read',
                      color: palette.textMuted, icon: Icons.schedule_rounded),
              ]),
              SizedBox(height: 12.h),
              if (loading)
                const _ContentSkeleton()
              else if (error != null || content == null)
                _Message(
                  icon: Icons.cloud_off_rounded,
                  title: "Couldn't load this lesson",
                  subtitle: 'Check your connection and try again.',
                  onRetry: _retry,
                )
              else if (content.markdown.trim().isEmpty)
                Text(lesson.desc ?? 'Content for this lesson is coming soon.',
                    style: context.text.bodyMedium
                        ?.copyWith(fontSize: 14.sp, height: 1.5))
              else
                MarkdownWidget(
                  physics: const NeverScrollableScrollPhysics(),
                  shrinkWrap: true,
                  padding: EdgeInsets.zero,
                  data: content.markdown,
                  config: config,
                ),
              if (lesson.videos.isNotEmpty) ...[
                SizedBox(height: 24.h),
                const SectionHeader(AppString.videos),
                SizedBox(height: 12.h),
                for (final url in lesson.videos)
                  Padding(
                    padding: EdgeInsets.only(bottom: 15.h),
                    child: CustomVideoPlayer(key: ValueKey(url), videoUrl: url),
                  ),
              ],
            ]),
          ),
        );
      },
    );
  }
}

class _ContentSkeleton extends StatelessWidget {
  const _ContentSkeleton();

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SkeletonBox(height: 28.h, width: 220.w),
          SizedBox(height: 16.h),
          for (var i = 0; i < 4; i++) ...[
            SkeletonBox(height: 14.h),
            SizedBox(height: 8.h),
          ],
          SkeletonBox(height: 14.h, width: 160.w),
          SizedBox(height: 20.h),
          SkeletonBox(height: 140.h, radius: 12.r),
          SizedBox(height: 20.h),
          for (var i = 0; i < 3; i++) ...[
            SkeletonBox(height: 14.h),
            SizedBox(height: 8.h),
          ],
        ],
      );
}
