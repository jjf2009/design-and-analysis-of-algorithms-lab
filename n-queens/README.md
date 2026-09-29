# N-Queens (Backtracking)

**DAA Lab — Experiment 10: N-Queens problem using Backtracking.**

`main.py` places `n` queens on an `n × n` board so that no two attack each other,
using backtracking. `x[k]` records the column of the queen in row `k`, so two
queens never share a row by construction.

## Algorithm

`Place(x, k)` checks the queen in row `k` against every earlier queen: a conflict
exists if they share a column (`x[i] == x[k]`) or a diagonal
(`|x[i] − x[k]| == |i − k|`). `NQueens(x, k, n)` tries every column for row `k`,
recursing to the next row on a legal placement and backtracking on a dead end.
Each complete assignment is printed as a board.

## Run

```bash
python3 main.py
```

Enter the board size `n`. (`n = 4` gives 2 solutions; `n = 8` gives 92.)

## Complexity

Worst case `O(n!)` placements explored, but the constraint checks prune the tree
sharply. Space is `O(n)` for the column array and recursion stack.
