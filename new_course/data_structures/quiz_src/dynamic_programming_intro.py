QUESTIONS = [
    mcq(r"""
What is dynamic programming?
""", ["Solving overlapping subproblems once and reusing their stored answers",
       "Programming that changes at runtime", "Allocating memory dynamically",
       "Sorting data dynamically"],
        "Solving overlapping subproblems once and reusing their stored answers"),

    mcq(r"""
Which two properties make a problem suitable for DP?
""", ["Optimal substructure and overlapping subproblems", "Sorted input and unique keys",
       "Recursion and randomness", "Graphs and trees"],
        "Optimal substructure and overlapping subproblems"),

    mcq(r"""
What does "overlapping subproblems" mean?
""", ["The same smaller problems are solved many times by naive recursion",
       "Subproblems share memory", "Subproblems run in parallel", "Each subproblem is unique"],
        "The same smaller problems are solved many times by naive recursion"),

    mcq(r"""
What does "optimal substructure" mean?
""", ["The best answer can be built from best answers to smaller subproblems",
       "The data is sorted", "The problem has a tree structure", "Every choice is greedy"],
        "The best answer can be built from best answers to smaller subproblems"),

    mcq(r"""
Why is merge sort divide and conquer rather than DP?
""", ["Its subproblems (the two halves) don't overlap", "It isn't recursive",
       "It doesn't have subproblems", "It is DP"], "Its subproblems (the two halves) don't overlap"),

    mcq(r"""
What is memoization?
""", ["Caching results of recursive calls so each subproblem is solved once",
       "Writing memos in code comments", "Filling a table bottom-up", "Sorting the inputs"],
        "Caching results of recursive calls so each subproblem is solved once"),

    mcq(r"""
What is tabulation?
""", ["Filling a table from the smallest subproblems up, using loops", "Caching recursive calls",
       "Printing results as a table", "Sorting a table"],
        "Filling a table from the smallest subproblems up, using loops"),

    mcq(r"""
Which approach can overflow the call stack on very large inputs?
""", ["Memoization (top-down recursion)", "Tabulation (bottom-up)", "Both equally", "Neither"],
        "Memoization (top-down recursion)"),

    mcq(r"""
Which approach only solves the subproblems that are actually needed?
""", ["Memoization", "Tabulation", "Both", "Neither"], "Memoization"),

    mcq(r"""
How many calls does naive recursive fib(30) make?
""", ["About 2.7 million", "30", "59", "About 1,000"], "About 2.7 million"),

    mcq(r"""
What does this print?

```dart
var calls = 0;
final memo = <int, int>{};

int fib(int n) {
  calls++;
  if (n <= 1) return n;
  return memo[n] ??= fib(n - 1) + fib(n - 2);
}

void main() {
  fib(10);
  print(calls);
}
```
""", ["19", "177", "10", "55"], "19"),

    mcq(r"""
What does this print?

```dart
int fibTable(int n) {
  if (n <= 1) return n;
  final dp = List<int>.filled(n + 1, 0);
  dp[1] = 1;
  for (var i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}

void main() {
  print(fibTable(12));
}
```
""", ["144", "89", "233", "12"], "144"),

    mcq(r"""
What is the time complexity of memoized or tabulated Fibonacci?
""", ["O(n)", "O(2ⁿ)", "O(n²)", "O(log n)"], "O(n)"),

    mcq(r"""
How can tabulated Fibonacci use O(1) space?
""", ["Keep only the last two values instead of the whole table", "Use a Set",
       "Use recursion", "It can't"], "Keep only the last two values instead of the whole table"),

    order(r"""
Complete the DP recipe in order:

```dart
// 1. define the %order%
// 2. write the %order%
// 3. set the %order%
// 4. choose a fill order, then return the answer
```
""", ["state", "recurrence", "base cases", "pivot", "heap"],
        ["state", "recurrence", "base cases"]),

    mcq(r"""
In "climbing stairs" (1 or 2 steps at a time), what is the recurrence?
""", ["ways[i] = ways[i − 1] + ways[i − 2]", "ways[i] = ways[i − 1] × 2",
       "ways[i] = i", "ways[i] = ways[i − 1] + 1"], "ways[i] = ways[i − 1] + ways[i − 2]"),

    mcq(r"""
What does this print?

```dart
int climb(int n) {
  final w = List<int>.filled(n + 1, 0);
  w[0] = 1;
  if (n >= 1) w[1] = 1;
  for (var i = 2; i <= n; i++) {
    w[i] = w[i - 1] + w[i - 2];
  }
  return w[n];
}

void main() {
  print(climb(5));
}
```
""", ["8", "5", "13", "10"], "8"),

    mcq(r"""
Why does greedy fail for coin change with coins [1, 3, 4] and amount 6?
""", ["Greedy picks 4 + 1 + 1 (3 coins) but 3 + 3 uses only 2",
       "Greedy can't use coin 1", "6 can't be made", "Greedy works fine"],
        "Greedy picks 4 + 1 + 1 (3 coins) but 3 + 3 uses only 2"),

    mcq(r"""
In minimum coin change, what does dp[a] represent?
""", ["The fewest coins needed to make amount a", "The number of ways to make a",
       "The largest coin ≤ a", "The amount a itself"],
        "The fewest coins needed to make amount a"),

    mcq(r"""
What is the base case of minimum coin change?
""", ["dp[0] = 0", "dp[0] = 1", "dp[1] = 1", "dp[0] = infinity"], "dp[0] = 0"),

    mcq(r"""
What does this print?

```dart
int minCoins(List<int> coins, int amount) {
  const inf = 1 << 30;
  final dp = List<int>.filled(amount + 1, inf);
  dp[0] = 0;
  for (var a = 1; a <= amount; a++) {
    for (final c in coins) {
      if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
    }
  }
  return dp[amount] >= inf ? -1 : dp[amount];
}

void main() {
  print(minCoins([1, 3, 4], 6));
  print(minCoins([5, 10], 3));
}
```
""", ["2 then -1", "3 then -1", "2 then 0", "6 then 3"], "2 then -1"),

    mcq(r"""
What is the time complexity of minimum coin change with A as the amount and C coins?
""", ["O(A × C)", "O(A + C)", "O(2^A)", "O(C log A)"], "O(A × C)"),

    mcq(r"""
In "count the ways to make change", why must coins be the OUTER loop?
""", ["So each combination is counted once (1+2 and 2+1 count as one)",
       "For speed only", "To avoid negative indexes", "It doesn't matter"],
        "So each combination is counted once (1+2 and 2+1 count as one)"),

    mcq(r"""
What does this print?

```dart
int countWays(List<int> coins, int amount) {
  final ways = List<int>.filled(amount + 1, 0);
  ways[0] = 1;
  for (final c in coins) {
    for (var a = c; a <= amount; a++) {
      ways[a] += ways[a - c];
    }
  }
  return ways[amount];
}

void main() {
  print(countWays([1, 2], 4));
}
```
""", ["3", "5", "4", "2"], "3"),

    mcq(r"""
In counting DP, why is ways[0] = 1?
""", ["There's exactly one way to make amount 0: use no coins", "It's arbitrary",
       "To avoid division by zero", "Because coin 1 exists"],
        "There's exactly one way to make amount 0: use no coins"),

    mcq(r"""
In the minimum-path-sum grid (moving right or down), what is the recurrence?
""", ["dp[r][c] = grid[r][c] + min(dp[r−1][c], dp[r][c−1])",
       "dp[r][c] = dp[r−1][c] + dp[r][c−1]", "dp[r][c] = max of neighbors",
       "dp[r][c] = grid[r][c]"],
        "dp[r][c] = grid[r][c] + min(dp[r−1][c], dp[r][c−1])"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int minPath(List<List<int>> g) {
  final r = g.length, c = g[0].length;
  final dp = List.generate(r, (_) => List.filled(c, 0));
  for (var i = 0; i < r; i++) {
    for (var j = 0; j < c; j++) {
      if (i == 0 && j == 0) {
        dp[i][j] = g[i][j];
      } else if (i == 0) {
        dp[i][j] = dp[i][j - 1] + g[i][j];
      } else if (j == 0) {
        dp[i][j] = dp[i - 1][j] + g[i][j];
      } else {
        dp[i][j] = g[i][j] + min(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[r - 1][c - 1];
}

void main() {
  print(minPath([[1, 2], [5, 1]]));
}
```
""", ["4", "7", "3", "9"], "4"),

    mcq(r"""
How many monotonic (right/down only) paths cross a 2×2-step grid (from (0,0) to (2,2))?
""", ["6", "4", "2", "8"], "6"),

    mcq(r"""
What does this print?

```dart
final memo = <(int, int), int>{};

int paths(int r, int c) {
  if (r == 0 || c == 0) return 1;
  return memo[(r, c)] ??= paths(r - 1, c) + paths(r, c - 1);
}

void main() {
  print(paths(3, 3));
}
```
""", ["20", "6", "9", "27"], "20"),

    mcq(r"""
Why use a record like `(r, c)` as the memo key in grid DP?
""", ["The answer depends on both coordinates, so the key must include both",
       "Records are faster than ints", "Maps require records", "To sort the keys"],
        "The answer depends on both coordinates, so the key must include both"),

    mcq(r"""
What is the longest common subsequence (LCS) of 'abcde' and 'ace'?
""", ["ace (length 3)", "abc (length 3)", "a (length 1)", "abcde (length 5)"],
        "ace (length 3)"),

    mcq(r"""
In LCS, when a[i−1] == b[j−1], what is dp[i][j]?
""", ["dp[i−1][j−1] + 1", "max(dp[i−1][j], dp[i][j−1])", "0", "dp[i][j−1]"],
        "dp[i−1][j−1] + 1"),

    mcq(r"""
In LCS, when a[i−1] != b[j−1], what is dp[i][j]?
""", ["max(dp[i−1][j], dp[i][j−1])", "dp[i−1][j−1] + 1", "0", "dp[i−1][j−1]"],
        "max(dp[i−1][j], dp[i][j−1])"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int lcs(String a, String b) {
  final dp = List.generate(a.length + 1, (_) => List.filled(b.length + 1, 0));
  for (var i = 1; i <= a.length; i++) {
    for (var j = 1; j <= b.length; j++) {
      dp[i][j] = a[i - 1] == b[j - 1]
          ? dp[i - 1][j - 1] + 1
          : max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp[a.length][b.length];
}

void main() {
  print(lcs('dart', 'start'));
  print(lcs('abc', 'xyz'));
}
```
""", ["3 then 0", "4 then 0", "3 then 1", "2 then 0"], "3 then 0"),

    mcq(r"""
Which real tool is based on LCS?
""", ["File diff tools (showing what changed)", "Image compression", "Password hashing",
       "Network routing"], "File diff tools (showing what changed)"),

    mcq(r"""
What is the time complexity of LCS for strings of lengths n and m?
""", ["O(n × m)", "O(n + m)", "O(2^(n+m))", "O(n log m)"], "O(n × m)"),

    mcq(r"""
In 0/1 knapsack, what choice is made for each item?
""", ["Take it or skip it", "Take a fraction of it", "Take it unlimited times",
       "Sort it"], "Take it or skip it"),

    mcq(r"""
In the 1D 0/1 knapsack table, why is the capacity loop run BACKWARDS?
""", ["So each item is used at most once per capacity", "To find the maximum faster",
       "To avoid negative weights", "It doesn't matter"],
        "So each item is used at most once per capacity"),

    mcq(r"""
What happens if the 1D knapsack loop runs FORWARDS over capacity?
""", ["Items can be reused, which solves the unbounded knapsack instead",
       "It crashes", "It gives the same answer", "It always returns 0"],
        "Items can be reused, which solves the unbounded knapsack instead"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int knapsack(List<(int, int)> items, int cap) {
  final dp = List<int>.filled(cap + 1, 0);
  for (final (w, v) in items) {
    for (var c = cap; c >= w; c--) {
      dp[c] = max(dp[c], dp[c - w] + v);
    }
  }
  return dp[cap];
}

void main() {
  print(knapsack([(1, 1), (3, 4), (4, 5), (5, 7)], 7));
}
```
""", ["9", "8", "12", "17"], "9"),

    mcq(r"""
What is the time complexity of 0/1 knapsack with n items and capacity W?
""", ["O(n × W)", "O(2ⁿ)", "O(n + W)", "O(n log W)"], "O(n × W)"),

    mcq(r"""
Which phrase in a problem usually signals counting DP?
""", ["\"How many ways...\"", "\"Find the shortest path in a weighted graph\"",
       "\"Sort the list\"", "\"Is the string a palindrome?\""], "\"How many ways...\""),

    mcq(r"""
Which phrase usually signals optimization DP?
""", ["\"Minimum cost\" or \"maximum profit\"", "\"Reverse the list\"",
       "\"Print every element\"", "\"Find the first element\""],
        "\"Minimum cost\" or \"maximum profit\""),

    mcq(r"""
What's a good first step when you suspect DP?
""", ["Write the brute-force recursion and check if it repeats the same calls",
       "Sort the input", "Use a priority queue", "Guess a formula"],
        "Write the brute-force recursion and check if it repeats the same calls"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int rob(List<int> h) {
  var take = 0, skip = 0;
  for (final m in h) {
    final nt = skip + m;
    skip = max(take, skip);
    take = nt;
  }
  return max(take, skip);
}

void main() {
  print(rob([1, 2, 3, 1]));
  print(rob([2, 1, 1, 2]));
}
```
""", ["4 then 4", "3 then 3", "4 then 3", "7 then 6"], "4 then 4"),

    mcq(r"""
In house robber, why does robbing the current house use the previous "skip" value?
""", ["You can't rob two adjacent houses", "Skip is always larger", "To save memory",
       "It's random"], "You can't rob two adjacent houses"),

    mcq(r"""
What does `return memo[n] ??= compute();` do?
""", ["Computes and stores the value only if memo[n] is null, then returns it",
       "Always recomputes", "Deletes memo[n]", "Returns null"],
        "Computes and stores the value only if memo[n] is null, then returns it"),

    mcq(r"""
What problem does edit distance solve?
""", ["The minimum insertions, deletions and substitutions to turn one string into another",
       "The longest palindrome", "The number of vowels", "Sorting strings"],
        "The minimum insertions, deletions and substitutions to turn one string into another"),

    mcq(r"""
Which app feature commonly uses edit distance?
""", ["Autocorrect and spelling suggestions", "Image filters", "Push notifications",
       "Battery optimization"], "Autocorrect and spelling suggestions"),

    mcq(r"""
In the longest increasing subsequence DP, what does dp[i] usually mean?
""", ["Length of the longest increasing subsequence ending at index i",
       "The i-th smallest element", "The number of elements before i", "The sum up to i"],
        "Length of the longest increasing subsequence ending at index i"),

    mcq(r"""
What does this print?

```dart
import 'dart:math';

int lis(List<int> a) {
  final dp = List<int>.filled(a.length, 1);
  for (var i = 0; i < a.length; i++) {
    for (var j = 0; j < i; j++) {
      if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
    }
  }
  return dp.reduce(max);
}

void main() {
  print(lis([10, 9, 2, 5, 3, 7, 101, 18]));
}
```
""", ["4", "3", "5", "8"], "4"),

    mcq(r"""
What is the most common mistake when defining a DP?
""", ["A vague state definition", "Using too many comments", "Using loops",
       "Using integers"], "A vague state definition"),

    fill(r"""
Store and return a memoized value in one line:

```dart
final memo = <int, int>{};

int f(int n) {
  if (n <= 1) return 1;
  return memo[n] %fill% f(n - 1) * n;
}
```
""", "??="),

    mcq(r"""
DP often converts which kind of brute-force running time into polynomial time?
""", ["Exponential", "Logarithmic", "Constant", "Linear"], "Exponential"),
]
