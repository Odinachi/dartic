# Dynamic Programming Basics

Imagine someone asks you: *"What's 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1?"* You count: **8**. ✋

Then they add another **"+ 1"** to the end and ask again. You don't recount from scratch; you say **9** immediately, because you **remembered** the previous answer. 🧠

👉 That's the heart of **dynamic programming (DP)**:

> **Dynamic programming** solves problems by breaking them into **overlapping subproblems**, solving each subproblem **once**, and **storing** its answer for reuse. It turns many exponential-time recursive solutions into **polynomial** time.

DP is how apps compute the cheapest route through a grid, the difference between two text files, autocorrect suggestions, the best way to make change, and much more.

---

## 🔑 When Does DP Apply?

A problem is a good DP candidate when it has both:

1. **Optimal substructure**: The best answer can be built from the best answers to smaller versions of the same problem.
2. **Overlapping subproblems**: The same smaller problems come up **again and again**.

> 💡 If subproblems **don't** overlap (like merge sort's halves), plain **divide and conquer** is enough. DP is for when recursion keeps **repeating itself**.

---

## 🐢 The Problem: Repeated Work

```dart
var calls = 0;

int fib(int n) {
  calls++;
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

void main() {
  print(fib(30)); // 832040
  print('calls: $calls'); // 2692537 😱
}
```

**🔍 What This Code Does:**

1. **Two Recursive Calls**: Each `fib(n)` calls `fib(n − 1)` and `fib(n − 2)`.
2. **Massive Repetition**: `fib(28)` is computed twice, `fib(27)` three times, `fib(26)` five times...
3. **Exponential Time**: About **2.7 million** calls to compute `fib(30)`.

```text
                 fib(5)
              /         \
          fib(4)        fib(3)       ← fib(3) appears twice
         /     \        /    \
     fib(3)  fib(2)  fib(2) fib(1)   ← fib(2) appears three times
     /   \
 fib(2) fib(1)
```

There are only **31 different subproblems** (`fib(0)` to `fib(30)`), but we solve them millions of times. DP fixes exactly this.

---

## 🧠 Approach 1: Memoization (Top-Down)

Keep the natural recursion, but **cache** each result the first time it's computed.

```dart
var calls = 0;
final memo = <int, int>{};

int fib(int n) {
  calls++;
  if (n <= 1) return n;
  final cached = memo[n];
  if (cached != null) return cached;
  return memo[n] = fib(n - 1) + fib(n - 2); // store, then return
}

void main() {
  print(fib(30)); // 832040
  print('calls: $calls'); // 59
  print(fib(90)); // 2880067194370816120
}
```

**🔍 What This Code Does:**

1. **Check the Memo First**: If `n` was already solved, return it immediately.
2. **Compute Once**: Otherwise recurse, then store the result with `memo[n] = ...`.
3. **Assignment as Expression**: `return memo[n] = ...;` stores and returns in one line.
4. **From Millions to Dozens**: 59 calls instead of 2.7 million: **O(n)** time.
5. **Space**: O(n) for the memo plus O(n) recursion depth.

## 📋 Approach 2: Tabulation (Bottom-Up)

Solve the **smallest** subproblems first and build up to the answer in a table, with no recursion.

```dart
int fibTable(int n) {
  if (n <= 1) return n;
  final dp = List<int>.filled(n + 1, 0);
  dp[1] = 1;
  for (var i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2]; // each entry uses earlier entries
  }
  return dp[n];
}

int fibTwoVars(int n) {
  var prev = 0, curr = 1; // only the last two values are ever needed
  for (var i = 0; i < n; i++) {
    final next = prev + curr;
    prev = curr;
    curr = next;
  }
  return prev;
}

void main() {
  print(fibTable(30));  // 832040
  print(fibTwoVars(30)); // 832040
}
```

**🔍 What This Code Does:**

1. **DP Table**: `dp[i]` holds the answer to subproblem `i`.
2. **Fill in Order**: Each entry depends only on entries already computed.
3. **No Recursion**: No risk of stack overflow.
4. **Space Optimization**: Since only the last two values are needed, two variables replace the whole table: **O(1)** space.

| | Memoization (top-down) | Tabulation (bottom-up) |
|---|------------------------|------------------------|
| Style | Recursive + cache | Loops + table |
| Solves | Only subproblems actually needed | Every subproblem in the table |
| Stack overflow risk | Yes, on deep recursion | No |
| Easy to write from a recursive idea | ✅ | Needs a fill order |
| Space optimization | Harder | ✅ Often easy (keep only recent rows) |

---

## 🪜 The DP Recipe

1. **Define the state**: What does `dp[i]` (or `dp[i][j]`) mean, in words?
2. **Find the recurrence**: How does a state depend on smaller states?
3. **Set the base cases**: The smallest states you know directly.
4. **Choose an order**: Fill states so dependencies are ready (or memoize).
5. **Return the answer**: Which state holds the final result?

Let's apply it.

---

## 🧗 Example 1: Climbing Stairs

**Problem:** You can climb **1 or 2** steps at a time. How many distinct ways to reach step `n`?

1. **State**: `ways[i]` = number of ways to reach step `i`.
2. **Recurrence**: The last move was either 1 step (from `i − 1`) or 2 steps (from `i − 2`): `ways[i] = ways[i − 1] + ways[i − 2]`.
3. **Base cases**: `ways[0] = 1` (stand still), `ways[1] = 1`.

```dart
int climbStairs(int n) {
  final ways = List<int>.filled(n + 1, 0);
  ways[0] = 1;
  if (n >= 1) ways[1] = 1;
  for (var i = 2; i <= n; i++) {
    ways[i] = ways[i - 1] + ways[i - 2];
  }
  return ways[n];
}

void main() {
  print(climbStairs(4)); // 5: 1111, 112, 121, 211, 22
  print(climbStairs(10)); // 89
}
```

**🔍 What This Code Does:**

1. **Same Shape as Fibonacci**: Many DP problems reduce to familiar recurrences.
2. **Counting Problems**: The recurrence **adds** the number of ways from each possible previous state.
3. **O(n) Time**: One pass up the stairs.

---

## 🪙 Example 2: Coin Change (Minimum Coins)

**Problem:** Given coin values and an amount, find the **fewest coins** that make the amount, or −1 if impossible.

> Greedy (always take the biggest coin) fails: with coins `[1, 3, 4]` and amount `6`, greedy gives `4 + 1 + 1` (3 coins), but `3 + 3` uses only 2.

1. **State**: `dp[a]` = fewest coins to make amount `a`.
2. **Recurrence**: Try each coin `c` as the last coin: `dp[a] = min(dp[a − c] + 1)`.
3. **Base case**: `dp[0] = 0`.

```dart
int minCoins(List<int> coins, int amount) {
  const inf = 1 << 30;
  final dp = List<int>.filled(amount + 1, inf);
  dp[0] = 0;
  for (var a = 1; a <= amount; a++) {
    for (final c in coins) {
      if (c <= a && dp[a - c] + 1 < dp[a]) {
        dp[a] = dp[a - c] + 1;
      }
    }
  }
  return dp[amount] >= inf ? -1 : dp[amount];
}

void main() {
  print(minCoins([1, 3, 4], 6));     // 2 (3 + 3)
  print(minCoins([1, 5, 10, 25], 63)); // 6 (25 + 25 + 10 + 1 + 1 + 1)
  print(minCoins([2], 3));           // -1 (impossible)
}
```

**🔍 What This Code Does:**

1. **Infinity for Unknown**: `inf` marks amounts not yet reachable.
2. **Try Every Coin**: For each amount, use each coin as the "last" coin and keep the best.
3. **Builds on Smaller Amounts**: `dp[a − c]` was computed earlier in the loop.
4. **O(amount × coins)** time, O(amount) space.

### Counting the number of ways to make change

```dart
int countWays(List<int> coins, int amount) {
  final ways = List<int>.filled(amount + 1, 0);
  ways[0] = 1;
  for (final c in coins) {          // coins in the OUTER loop...
    for (var a = c; a <= amount; a++) {
      ways[a] += ways[a - c];       // ...so each combination is counted once
    }
  }
  return ways[amount];
}

void main() {
  print(countWays([1, 2, 5], 5)); // 4: 5, 2+2+1, 2+1+1+1, 1+1+1+1+1
}
```

**🔍 What This Code Does:**

1. **Counting, Not Minimizing**: Add ways instead of taking a minimum.
2. **Loop Order Matters**: Putting coins in the outer loop counts **combinations** (`1+2` and `2+1` are the same). Swapping the loops would count **orderings** instead.

---

## 🗺️ Example 3: Grid Paths (2D DP)

**Problem:** A robot starts at the top-left of a grid and moves only **right** or **down**. Each cell has a cost. Find the **cheapest** path to the bottom-right.

1. **State**: `dp[r][c]` = cheapest cost to reach cell `(r, c)`.
2. **Recurrence**: Arrive from above or from the left: `dp[r][c] = grid[r][c] + min(dp[r−1][c], dp[r][c−1])`.
3. **Base cases**: The first row and first column can only be reached one way.

```dart
import 'dart:math';

int minPathSum(List<List<int>> grid) {
  final rows = grid.length, cols = grid[0].length;
  final dp = List.generate(rows, (_) => List.filled(cols, 0));
  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      if (r == 0 && c == 0) {
        dp[r][c] = grid[r][c];
      } else if (r == 0) {
        dp[r][c] = dp[r][c - 1] + grid[r][c];
      } else if (c == 0) {
        dp[r][c] = dp[r - 1][c] + grid[r][c];
      } else {
        dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1]);
      }
    }
  }
  return dp[rows - 1][cols - 1];
}

void main() {
  print(minPathSum([
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1],
  ])); // 7: 1 → 3 → 1 → 1 → 1
}
```

**🔍 What This Code Does:**

1. **Row by Row**: When computing `(r, c)`, the cells above and to the left are already done.
2. **Edges**: The first row and column have only one way in.
3. **O(rows × cols)**: Each cell is computed once. Trying every path would be exponential.

---

## 📝 Example 4: Longest Common Subsequence

**Problem:** Find the length of the longest sequence of characters appearing in **both** strings in the same order (not necessarily contiguous). This powers **diff tools** and **DNA comparison**.

1. **State**: `dp[i][j]` = LCS length of the first `i` chars of `a` and the first `j` chars of `b`.
2. **Recurrence**:
   - If `a[i−1] == b[j−1]`: `dp[i][j] = dp[i−1][j−1] + 1`
   - Otherwise: `dp[i][j] = max(dp[i−1][j], dp[i][j−1])`
3. **Base cases**: `dp[0][*] = dp[*][0] = 0`.

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
  print(lcs('flutter', 'butter')); // 5 (utter)
  print(lcs('abcde', 'ace'));      // 3 (ace)
  print(lcs('dart', 'kotlin'));    // 1 (t)
}
```

**🔍 What This Code Does:**

1. **Extra Row and Column**: Index 0 means "empty prefix", which removes edge cases.
2. **Match**: Extend the LCS of both shorter prefixes by 1.
3. **No Match**: Drop a character from one string or the other and keep the better result.
4. **O(n × m)** time and space.

---

## 🎒 Example 5: 0/1 Knapsack

**Problem:** A backpack holds weight `W`. Each item has a weight and a value and can be taken **at most once**. Maximize the total value.

```dart
import 'dart:math';

int knapsack(List<(int weight, int value)> items, int capacity) {
  final dp = List<int>.filled(capacity + 1, 0); // dp[w] = best value with weight limit w
  for (final (weight, value) in items) {
    for (var w = capacity; w >= weight; w--) { // backwards: each item used once
      dp[w] = max(dp[w], dp[w - weight] + value);
    }
  }
  return dp[capacity];
}

void main() {
  final gear = [
    (1, 1),  // snacks
    (3, 4),  // tent
    (4, 5),  // stove
    (5, 7),  // sleeping bag
  ];
  print(knapsack(gear, 7)); // 9: tent (3, 4) + stove (4, 5)
}
```

**🔍 What This Code Does:**

1. **Choice per Item**: Either skip it (`dp[w]`) or take it (`dp[w − weight] + value`).
2. **1D Table**: Reuses one array across items to save memory.
3. **Backwards Loop**: Iterating `w` from high to low ensures each item is counted **once** per capacity. Going forwards would allow taking the same item repeatedly (that's the "unbounded" knapsack).
4. **Named Record Fields in the Type**: `(int weight, int value)` documents what each field means.
5. **O(items × capacity)**.

---

## 🧭 Recognizing DP Problems

| Clue in the problem | Likely DP |
|---------------------|-----------|
| "How many ways..." | Counting DP (sum over choices) |
| "Minimum / maximum cost / profit / length..." | Optimization DP (min/max over choices) |
| "Can you reach / form / partition..." | Boolean DP (OR over choices) |
| Choices at each step that affect later steps | DP over states |
| Brute force recursion repeats the same calls | Memoize it! |

> 💡 Start by writing the **brute-force recursion**. If it recomputes the same arguments, add a **memo**. Then, if needed, convert it into a **table**.

---

## ⚠️ Common Mistakes

### 1. Defining the state vaguely

"dp[i] is the answer" isn't enough. Write precisely: "dp[i] is the fewest coins to make amount i". A clear state makes the recurrence obvious.

### 2. Wrong base cases

`dp[0] = 0` vs `dp[0] = 1` changes everything. Ask: what's the answer for the empty/smallest input?

### 3. Wrong fill order

Every state must be computed **after** the states it depends on. In knapsack, the loop direction even changes the problem's meaning.

### 4. Using greedy where DP is needed

Coin change with `[1, 3, 4]` shows that locally best choices can be globally wrong.

### 5. Memo keys that miss part of the state

If the answer depends on two parameters, the memo key must include **both** (use a record like `(i, j)`).

```dart
final memo = <(int, int), int>{};

int gridPaths(int r, int c) {
  if (r == 0 || c == 0) return 1; // one way along an edge
  return memo[(r, c)] ??= gridPaths(r - 1, c) + gridPaths(r, c - 1);
}

void main() {
  print(gridPaths(2, 2));   // 6
  print(gridPaths(16, 16)); // 601080390
}
```

**🔍 What This Code Does:**

1. **Record Keys**: `(r, c)` captures the full state.
2. **`??=` Memoization**: Computes and stores only if the key is missing.
3. **Fast**: 17 × 17 states instead of hundreds of millions of paths.

---

## 🧪 Try It Yourself

1. **House robber**: maximize money robbed from houses in a row without robbing two neighbors.
2. **Longest increasing subsequence**: `dp[i]` = length of the longest increasing subsequence ending at `i`.
3. **Edit distance**: the minimum insertions, deletions and substitutions to turn one word into another (the basis of autocorrect).
4. **Word break**: can a string be split into words from a dictionary?

```dart
import 'dart:math';

int rob(List<int> houses) {
  var take = 0, skip = 0; // best so far if we take / skip the previous house
  for (final money in houses) {
    final newTake = skip + money;
    skip = max(take, skip);
    take = newTake;
  }
  return max(take, skip);
}

void main() {
  print(rob([2, 7, 9, 3, 1])); // 12: 2 + 9 + 1
}
```

**🔍 What This Code Does:**

1. **Two States**: The best total if the previous house was robbed, and if it wasn't.
2. **Transition**: Robbing this house requires skipping the previous one.
3. **O(n) Time, O(1) Space**: A tiny DP with only two variables.

---

## 📌 Key Takeaways

- ✅ **Dynamic programming** = solve **overlapping subproblems** once and reuse their answers.
- ✅ It needs **optimal substructure** and **overlapping subproblems**.
- ✅ **Memoization** (top-down) adds a cache to recursion; **tabulation** (bottom-up) fills a table with loops.
- ✅ Recipe: define the **state**, write the **recurrence**, set **base cases**, choose a **fill order**, return the **answer**.
- ✅ Classic problems: Fibonacci/stairs, coin change, grid paths, LCS, knapsack.
- ✅ DP often turns **exponential** brute force into **polynomial** time, and tables can often be shrunk to **O(1)** or one row.

🎉 **Congratulations!** You've completed the Data Structures course: from Big O and arrays to graphs, trees, sorting, and dynamic programming. Keep practicing in the **Algorithm practice** section to put it all to work!
