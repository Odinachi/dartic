import 'package:dartcoder/features/editor/models/test_case.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class TestResultsWidget extends StatelessWidget {
  final TestRunResult? testResult;
  final bool isLoading;

  const TestResultsWidget({
    super.key,
    this.testResult,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Running tests...'),
          ],
        ),
      );
    }

    if (testResult == null) {
      return Center(
        child: Text(
          'Click "Run Tests" to check your solution',
          style:
              TextStyle(fontSize: 16, color: context.colors.onSurfaceVariant),
        ),
      );
    }

    return SingleChildScrollView(
      padding: EdgeInsets.all(16.w),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildSummaryCard(context),
          SizedBox(height: 16.h),
          _buildTestResultsList(context),
        ],
      ),
    );
  }

  Widget _buildSummaryCard(BuildContext context) {
    final passRate = testResult!.passRate;
    final color = passRate == 1.0
        ? context.palette.success
        : passRate > 0.5
            ? context.palette.warning
            : context.colors.error;

    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  passRate == 1.0 ? Icons.check_circle : Icons.error,
                  color: color,
                  size: 24,
                ),
                SizedBox(width: 8.w),
                Text(
                  '${testResult!.passedCount}/${testResult!.totalCount} Tests Passed',
                  style: TextStyle(
                    fontSize: 18.sp,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                ),
              ],
            ),
            SizedBox(height: 8.h),
            LinearProgressIndicator(
              value: passRate,
              backgroundColor: context.colors.surfaceContainerHighest,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
            SizedBox(height: 8.h),
            Text(
              'Execution time: ${testResult!.totalExecutionTime.inMilliseconds}ms',
              style: TextStyle(
                fontSize: 12.sp,
                color: context.colors.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTestResultsList(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Test Cases',
          style: TextStyle(
            fontSize: 16.sp,
            fontWeight: FontWeight.bold,
          ),
        ),
        SizedBox(height: 8.h),
        ...testResult!.results
            .map((result) => _buildTestCaseCard(context, result)),
      ],
    );
  }

  Widget _buildTestCaseCard(BuildContext context, TestResult result) {
    final passed = result.passed;
    final color = passed ? context.palette.success : context.colors.error;

    return Card(
      margin: EdgeInsets.only(bottom: 8.h),
      child: ExpansionTile(
        leading: Icon(
          passed ? Icons.check_circle : Icons.cancel,
          color: color,
        ),
        title: Text(
          result.testCase.name ?? "",
          style: TextStyle(
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
        subtitle: Text(
          passed ? 'Passed' : 'Failed',
          style: TextStyle(
            color: color,
            fontSize: 12.sp,
          ),
        ),
        trailing: Text(
          '${result.executionTime.inMilliseconds}ms',
          style: TextStyle(
            fontSize: 11.sp,
            color: context.colors.onSurfaceVariant,
          ),
        ),
        children: [
          Padding(
            padding: EdgeInsets.all(16.w),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (result.testCase.description != null) ...[
                  _buildDetailRow(
                      context, 'Description', result.testCase.description!),
                  SizedBox(height: 8.h),
                ],
                _buildDetailRow(context, 'Input',
                    _formatInput(result.testCase.inputs ?? [])),
                SizedBox(height: 8.h),
                _buildDetailRow(context, 'Expected',
                    _formatOutput(result.testCase.expectedOutput)),
                SizedBox(height: 8.h),
                _buildDetailRow(
                  context,
                  'Actual',
                  result.errorMessage ?? _formatOutput(result.actualOutput),
                  isError: result.errorMessage != null,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailRow(BuildContext context, String label, String value,
      {bool isError = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '$label:',
          style: TextStyle(
            fontWeight: FontWeight.w600,
            fontSize: 12.sp,
            color: context.colors.onSurfaceVariant,
          ),
        ),
        SizedBox(height: 4.h),
        Container(
          width: double.infinity,
          padding: EdgeInsets.all(8.w),
          decoration: BoxDecoration(
            color: isError
                ? context.colors.errorContainer
                : context.colors.surfaceContainerHigh,
            borderRadius: BorderRadius.circular(4),
            border: Border.all(
              color: isError
                  ? context.colors.error.withValues(alpha: .4)
                  : context.colors.outlineVariant,
            ),
          ),
          child: Text(
            value,
            style: TextStyle(
              fontFamily: 'monospace',
              fontSize: 11.sp,
              color: isError
                  ? context.colors.onErrorContainer
                  : context.colors.onSurface,
            ),
          ),
        ),
      ],
    );
  }

  String _formatInput(List<dynamic> inputs) {
    return inputs.map((input) {
      if (input is List) {
        return '[${input.join(', ')}]';
      }
      return input.toString();
    }).join(', ');
  }

  String _formatOutput(dynamic output) {
    if (output == null) return 'null';
    if (output is List) {
      return '[${output.join(', ')}]';
    }
    return output.toString();
  }
}
