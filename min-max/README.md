# MinMax (Divide and Conquer)

**DAA Lab — Experiment 1: Find the maximum and minimum using divide and conquer.**

`main.py` finds the largest and smallest element of a 1-indexed array by
splitting it in half, solving each half recursively, and combining the two
results with a single comparison of maxes and a single comparison of mins.

## Algorithm

`MaxMin(i, j)` handles three cases (the classic Horowitz–Sahni formulation):

- `i == j` — one element: it is both the max and the min.
- `i == j - 1` — two elements: one comparison sets both.
- otherwise — split at `mid = (i + j) // 2`, recurse on both halves, and combine.

Each call prints its `i j max min` line so the recursion can be traced by hand.

## Run

```bash
python3 main.py
```

Enter the size, then the elements separated by spaces.

## Complexity

`3n/2 - 2` comparisons for `n` elements — fewer than the `2n - 2` of the naive
linear scan. Time `O(n)`; recursion depth (stack space) `O(log n)`.

> See also [`../assignment`](../assignment) for a Streamlit visualizer that draws
> the MaxMin recursion tree.
