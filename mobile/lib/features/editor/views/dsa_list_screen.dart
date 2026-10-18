import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/features/editor/view_model/editor_cubit.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/features/wallet/views/coin_widgets.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:dartcoder/shared/widgets/ui.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class DsaListScreen extends StatefulWidget {
  const DsaListScreen({super.key});

  @override
  State<DsaListScreen> createState() => _DsaListScreenState();
}

class _DsaListScreenState extends State<DsaListScreen> {
  final ScrollController _scrollController = ScrollController();
  bool _isNearBottom = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    // Initial fetch
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<EditorCubit>().fetchDSAList();
    });
  }

  @override
  void dispose() {
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.hasClients) {
      final threshold = _scrollController.position.maxScrollExtent - 200;
      final isNearBottom = _scrollController.position.pixels >= threshold;

      if (isNearBottom && !_isNearBottom) {
        _isNearBottom = true;
        context.read<EditorCubit>().loadMoreDSAList();
      } else if (!isNearBottom) {
        _isNearBottom = false;
      }
    }
  }

  Future<void> _onRefresh() async {
    await context.read<EditorCubit>().refreshDSAList();
  }

  int _getListItemCount(List dsaList, EditorState state) {
    if (state is DSAListLoaded && (state.hasMore || state.isLoadingMore)) {
      return dsaList.length + 1;
    }
    return dsaList.length;
  }

  Widget _buildBottomLoader(EditorState state) {
    if (state is DSAListLoaded && state.isLoadingMore) {
      return const Padding(
        padding: EdgeInsets.all(16.0),
        child: Center(child: CircularProgressIndicator()),
      );
    } else if (state is DSAListLoaded && !state.hasMore) {
      return Padding(
        padding: const EdgeInsets.all(16.0),
        child: Center(
          child: Text(
            "You've reached the end",
            style: context.text.bodySmall,
          ),
        ),
      );
    }
    return const SizedBox.shrink();
  }

  static const _filters = ['All', 'Easy', 'Medium', 'Hard'];
  String _filter = 'All';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppString.dsa),
        actions: const [
          CoinBadge(),
          SizedBox(width: 16),
        ],
      ),
      body: SafeArea(
        child: BlocBuilder<AppCubit, AppState>(builder: (_, __) {
          return BlocBuilder<EditorCubit, EditorState>(
            builder: (_, state) {
              final cubit = context.read<EditorCubit>();
              final allItems = cubit.dsaList;
              final solved =
                  context.read<AppCubit>().userProgress?.passedDsa?.toSet() ??
                      const <String>{};
              if (state is EditorLoading) {
                return const _DsaSkeleton();
              } else if (state is DSAListLoaded || state is EditorInitial) {
                if (allItems.isEmpty &&
                    state is DSAListLoaded &&
                    !state.isRefreshing) {
                  return const _EmptyState();
                }
              }

              final dsaList = _filter == 'All'
                  ? allItems
                  : allItems
                      .where((e) =>
                          e.difficulty?.toLowerCase() == _filter.toLowerCase())
                      .toList();
              final solvedCount =
                  allItems.where((e) => solved.contains(e.id)).length;

              return RefreshIndicator(
                onRefresh: _onRefresh,
                child: CustomScrollView(
                  controller: _scrollController,
                  physics: const AlwaysScrollableScrollPhysics(),
                  slivers: [
                    SliverPadding(
                      padding: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 0),
                      sliver: SliverToBoxAdapter(
                        child: FadeSlideIn(
                          child: _SummaryCard(
                              solved: solvedCount, total: allItems.length),
                        ),
                      ),
                    ),
                    SliverToBoxAdapter(
                      child: SizedBox(
                        height: 60.h,
                        child: ListView.separated(
                          scrollDirection: Axis.horizontal,
                          padding: EdgeInsets.symmetric(
                              horizontal: 20.w, vertical: 14.h),
                          itemCount: _filters.length,
                          separatorBuilder: (_, __) => SizedBox(width: 8.w),
                          itemBuilder: (_, i) {
                            final f = _filters[i];
                            final count = f == 'All'
                                ? allItems.length
                                : allItems
                                    .where((e) =>
                                        e.difficulty?.toLowerCase() ==
                                        f.toLowerCase())
                                    .length;
                            return _FilterChip(
                              label: f,
                              count: count,
                              color: f == 'All'
                                  ? AppColors.appBlue
                                  : AppColors.difficulty(f),
                              selected: _filter == f,
                              onTap: () => setState(() => _filter = f),
                            );
                          },
                        ),
                      ),
                    ),
                    SliverPadding(
                      padding: EdgeInsets.symmetric(horizontal: 20.w),
                      sliver: SliverList.builder(
                        itemCount: _getListItemCount(dsaList, state),
                        itemBuilder: (_, index) {
                          if (index == dsaList.length) {
                            // Loading indicator at the bottom
                            return _buildBottomLoader(state);
                          }

                          final dsaItem = dsaList[index];
                          return FadeSlideIn(
                            key: ValueKey('${_filter}_${dsaItem.id}'),
                            delay: FadeSlideIn.stagger(index, stepMs: 45),
                            child: ShadowContainer(
                              completed: solved.contains(dsaItem.id),
                              onTap: () {
                                AppRouter.push(AppRouter.editor,
                                    arg: EditorScreenArg(
                                        dsa: dsaItem, isPractice: true));
                              },
                              title: dsaItem.problemName,
                              desc: dsaItem.description,
                              difficulty: dsaItem.difficulty,
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              );
            },
          );
        }),
      ),
    );
  }
}

class _SummaryCard extends StatelessWidget {
  const _SummaryCard({required this.solved, required this.total});
  final int solved;
  final int total;

  @override
  Widget build(BuildContext context) {
    final white70 = AppColors.white.withValues(alpha: .8);
    return Container(
      padding: EdgeInsets.all(18.r),
      decoration: BoxDecoration(
        gradient: AppColors.dsaGradient,
        borderRadius: BorderRadius.circular(20.r),
        boxShadow: [
          BoxShadow(
            color: AppColors.emerald.withValues(alpha: .3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Row(children: [
        Expanded(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Problem solving',
                style: context.text.bodyMedium
                    ?.copyWith(fontSize: 12.5.sp, color: white70)),
            SizedBox(height: 4.h),
            Text.rich(
              TextSpan(children: [
                TextSpan(
                    text: '$solved',
                    style: context.text.displaySmall
                        ?.copyWith(fontSize: 30.sp, color: AppColors.white)),
                TextSpan(
                    text: ' / $total solved',
                    style: context.text.titleMedium
                        ?.copyWith(fontSize: 14.sp, color: white70)),
              ]),
            ),
            SizedBox(height: 6.h),
            Text('Sharpen your algorithms one problem at a time.',
                style: context.text.bodySmall
                    ?.copyWith(fontSize: 12.sp, color: white70)),
          ]),
        ),
        SizedBox(width: 12.w),
        ProgressRing(
          value: total == 0 ? 0 : solved / total,
          size: 62.r,
          stroke: 6.r,
          child: Icon(Icons.emoji_events_rounded,
              size: 24.sp, color: AppColors.white),
        ),
      ]),
    );
  }
}

class _FilterChip extends StatelessWidget {
  const _FilterChip({
    required this.label,
    required this.count,
    required this.color,
    required this.selected,
    required this.onTap,
  });
  final String label;
  final int count;
  final Color color;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final palette = context.palette;
    return Pressable(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: EdgeInsets.symmetric(horizontal: 14.w),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: selected ? color.withValues(alpha: .15) : palette.surface,
          borderRadius: BorderRadius.circular(100),
          border: Border.all(
              color: selected ? color.withValues(alpha: .7) : palette.border),
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Text(label,
              style: context.text.labelLarge?.copyWith(
                  fontSize: 13.sp,
                  color: selected ? color : palette.textPrimary)),
          SizedBox(width: 6.w),
          Text('$count',
              style: context.text.labelLarge?.copyWith(
                  fontSize: 11.sp,
                  color: selected ? color : palette.textMuted)),
        ]),
      ),
    );
  }
}

class _DsaSkeleton extends StatelessWidget {
  const _DsaSkeleton();

  @override
  Widget build(BuildContext context) => ListView(
        physics: const NeverScrollableScrollPhysics(),
        padding: EdgeInsets.fromLTRB(20.w, 8.h, 20.w, 0),
        children: [
          SkeletonBox(height: 110.h, radius: 20.r),
          SizedBox(height: 16.h),
          Row(children: [
            for (var i = 0; i < 4; i++) ...[
              SkeletonBox(height: 32.h, width: 64.w, radius: 100),
              SizedBox(width: 8.w),
            ],
          ]),
          SizedBox(height: 16.h),
          for (var i = 0; i < 5; i++) ...[
            SkeletonBox(height: 92.h, radius: 16.r),
            SizedBox(height: 12.h),
          ],
        ],
      );
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) => Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.inventory_2_outlined,
              size: 48.sp, color: context.palette.textMuted),
          SizedBox(height: 12.h),
          Text('No problems yet',
              style: context.text.titleMedium?.copyWith(fontSize: 16.sp)),
          SizedBox(height: 4.h),
          Text('Check back soon for new challenges.',
              style: context.text.bodySmall?.copyWith(fontSize: 13.sp)),
        ]),
      );
}
