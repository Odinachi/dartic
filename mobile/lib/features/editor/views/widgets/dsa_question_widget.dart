import 'package:dartcoder/shared/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:markdown_widget/widget/markdown.dart';

class DsaQuestionWidget extends StatefulWidget {
  const DsaQuestionWidget({super.key, this.text});
  final String? text;

  @override
  State<DsaQuestionWidget> createState() => _DsaQuestionWidgetState();
}

class _DsaQuestionWidgetState extends State<DsaQuestionWidget> {
  @override
  void initState() {
    // WidgetsBinding.instance.addPostFrameCallback((_) {
    //   setFunc();
    // });
    super.initState();
  }

//   void setFunc() async {
//     try {
//       await FirebaseFirestore.instance.collection('DSA').add({
//         "description":
//             "Given an array of non-negative integers nums, you are initially positioned at the first index of the array. Each element in the array represents your maximum jump length at that position. Your goal is to reach the last index in the minimum number of jumps. You can assume that you can always reach the last index.",
//         "difficulty": "Hard",
//         "problem_name": "Jump Game II",
//       }).then((doc) {
//         doc.collection("problem").add({
//           "answer": """
// void main() {
//   print("Hello, Dartic!");
//   print(jump([2, 3, 1, 1, 4]));
//   print(jump([2, 3, 0, 1, 4]));
// }

// int jump(List<int> nums) {
//   if (nums.length <= 1) return 0;

//   int jumps = 0;
//   int currentEnd = 0;
//   int farthest = 0;

//   for (int i = 0; i < nums.length - 1; i++) {
//     farthest = farthest > (i + nums[i]) ? farthest : (i + nums[i]);

//     if (i == currentEnd) {
//       jumps++;
//       currentEnd = farthest;

//       if (currentEnd >= nums.length - 1) {
//         break;
//       }
//     }
//   }

//   return jumps;
// }
// """,
//           "question": """
// # Jump Game II
// **Difficulty:** Hard

// ## Problem Description

// You are given a **0-indexed** array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.

// Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where:

// - `0 <= j <= nums[i]` and
// - `i + j < n`

// Return the **minimum number of jumps** to reach `nums[n - 1]`. The test cases are generated such that you can reach `nums[n - 1]`.

// ## Examples

// ### Example 1:
// ```
// Input: nums = [2,3,1,1,4]
// Output: 2
// Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
// ```

// ### Example 2:
// ```
// Input: nums = [2,3,0,1,4]
// Output: 2
// Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
// ```

// ### Example 3:
// ```
// Input: nums = [1,2,3]
// Output: 2
// Explanation: Jump 1 step from index 0 to 1, then 2 steps to the last index.
// ```

// ## Constraints

// - `1 ≤ nums.length ≤ 10⁴`
// - `0 ≤ nums[i] ≤ 1000`
// - It's guaranteed that you can reach `nums[n - 1]`""",
//           "function_name": "jump",
//           "test_cases": [
//             json.encode({
//               "name": "Example 1",
//               "inputs": [
//                 [2, 3, 1, 1, 4]
//               ],
//               "expected_output": 2,
//               "description": "Standard case with multiple paths"
//             }),
//             json.encode({
//               "name": "Example 2",
//               "inputs": [
//                 [2, 3, 0, 1, 4]
//               ],
//               "expected_output": 2,
//               "description": "Array with zero that must be avoided"
//             }),
//             json.encode({
//               "name": "Example 3",
//               "inputs": [
//                 [1, 2, 3]
//               ],
//               "expected_output": 2,
//               "description": "Small array with increasing jumps"
//             }),
//             json.encode({
//               "name": "Single element",
//               "inputs": [
//                 [0]
//               ],
//               "expected_output": 0,
//               "description": "Already at the last index"
//             }),
//             json.encode({
//               "name": "Large jumps",
//               "inputs": [
//                 [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0]
//               ],
//               "expected_output": 2,
//               "description": "Can jump far from first position"
//             })
//           ]
//         });
//       });
//     } catch (e) {
//       // Handle error
//     }
//   }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 20.w),
        child: MarkdownWidget(
          data: widget.text ?? "",
          selectable: true,
          config: config,
        ),
      ),
    );
  }
}
