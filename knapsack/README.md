# 0/1 Knapsack

`main.py` implements the 0/1 knapsack algorithm using dynamic programming.
Each item can be selected at most once. The `knapsack` function returns the
maximum value and the zero-based indexes of one optimal selection.

Run the example with:

```bash
python3 knapsack/main.py
```

The time complexity is `O(n * capacity)` and the space complexity is the same,
because the full table is retained to reconstruct the selected items.
