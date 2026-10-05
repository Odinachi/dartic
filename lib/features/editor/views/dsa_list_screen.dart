import 'package:dartcoder/features/authentication/view_model/app_cubit.dart';
import 'package:dartcoder/features/editor/view_model/editor_cubit.dart';
import 'package:dartcoder/features/editor/views/editor_screen.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

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
            'No more items to load',
            style: TextStyle(color: context.colors.onSurfaceVariant),
          ),
        ),
      );
    }
    return const SizedBox.shrink();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppString.dsa),
      ),
      body: SafeArea(
        child: BlocBuilder<AppCubit, AppState>(builder: (_, __) {
          return BlocBuilder<EditorCubit, EditorState>(
            builder: (_, state) {
              final cubit = context.read<EditorCubit>();
              final dsaList = cubit.dsaList;
              if (state is EditorLoading) {
                return const Center(child: CircularProgressIndicator());
              } else if (state is DSAListLoaded || state is EditorInitial) {
                if (dsaList.isEmpty &&
                    state is DSAListLoaded &&
                    !state.isRefreshing) {
                  return const Center(
                    child: Text('No DSA problems found'),
                  );
                }
              }

              return RefreshIndicator(
                onRefresh: _onRefresh,
                child: ListView.builder(
                  padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  controller: _scrollController,
                  physics: const AlwaysScrollableScrollPhysics(),
                  itemCount: _getListItemCount(dsaList, state),
                  itemBuilder: (_, index) {
                    if (index == dsaList.length) {
                      // Loading indicator at the bottom
                      return _buildBottomLoader(state);
                    }

                    final dsaItem = dsaList[index];
                   return ShadowContainer(
                      completed: context
                          .read<AppCubit>()
                          .userProgress
                          ?.passedDsa
                          ?.contains(dsaItem.id),
                      onTap: () {
                        AppRouter.push(AppRouter.editor,
                            arg: EditorScreenArg(
                                dsa: dsaItem, isPractice: true));
                      },
                      title: dsaItem.problemName,
                      desc: dsaItem.description,
                      difficulty: dsaItem.difficulty,
                    );
                  },
                ),
              );
            },
          );
        }),
      ),
    );
  }
}
