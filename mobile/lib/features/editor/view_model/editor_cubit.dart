import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dartcoder/features/editor/models/dsa_list_model.dart';
import 'package:dartcoder/features/editor/models/test_case.dart';
import 'package:dartcoder/services/firebase_services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'editor_state.dart';

class EditorCubit extends Cubit<EditorState> {
  final FirebaseServices firebaseServices;

  EditorCubit({required this.firebaseServices}) : super(EditorInitial());

  DocumentSnapshot? lastItem;
  List<DsaListModel> dsaList = [];
  bool hasMore = true;
  bool _isLoading = false;

  Future<void> fetchDSAList({
    int limit = 10,
    bool isRefresh = false,
  }) async {
    try {
      // Prevent multiple simultaneous calls
      if (_isLoading && !isRefresh) return;

      if (isRefresh) {
        // Reset for refresh
        lastItem = null;
        dsaList.clear();
        hasMore = true;
        _isLoading = true;
        emit(DSAListLoaded(isRefreshing: true));
      } else if (state is EditorLoading) {
        return;
      } else if (!isRefresh && state is! EditorInitial) {
        // Loading more items
        if (!hasMore) return; // Don't load if no more items
        _isLoading = true;
        emit(DSAListLoaded(
          hasMore: hasMore,
          isLoadingMore: true,
        ));
      } else {
        _isLoading = true;
        emit(EditorLoading());
      }

      final result = await firebaseServices.fetchDSA(
        limit: limit,
        startAfterDocument: lastItem,
      );

      _isLoading = false;

      if (result.error != null) {
        emit(EditorError(message: result.error!));
      } else {
        lastItem = result.lastDocument;
        if (result.documents != null && result.documents!.isNotEmpty) {
          if (isRefresh) {
            dsaList = result.documents!;
          } else {
            dsaList.addAll(result.documents!);
          }

          // Check if there are more items
          hasMore = result.documents!.length == limit;
        } else {
          hasMore = false;
        }

        emit(DSAListLoaded(
          hasMore: hasMore,
          isLoadingMore: false,
          isRefreshing: false,
        ));
      }
    } catch (e) {
      _isLoading = false;
      emit(EditorError(message: e.toString()));
    }
  }

  Future<void> refreshDSAList() async {
    await fetchDSAList(isRefresh: true);
  }

  Future<void> loadMoreDSAList() async {
    if (hasMore && !_isLoading && state is DSAListLoaded) {
      final currentState = state as DSAListLoaded;
      if (!currentState.isLoadingMore) {
        await fetchDSAList();
      }
    }
  }

  void getProblemsForDSA(String id) async {
    try {
      emit(EditorLoadingProblems());
      final result = await firebaseServices.fetchDsaProblems(id);
      if (result.error != null) {
        emit(EditorError(message: result.error!));
      } else {
        emit(EditorProblem(problem: result.data));
      }
    } catch (e) {
      emit(EditorError(message: e.toString()));
    }
  }
}
