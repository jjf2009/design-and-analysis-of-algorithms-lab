# Merge Sort

**DAA Lab — Experiment 2 (part a): Merge Sort.**

`main.py` implements the classic 1-indexed merge sort and prints the array at
every divide and merge step, using `|` markers to show the current split points
so the divide-and-conquer process can be traced.

## Algorithm

`MergeSort(low, high)` splits the range at `mid = (low + high) // 2`, sorts each
half recursively, then `Merge(low, mid, high)` interleaves the two sorted halves
into an auxiliary array `b` and copies them back into `a`.

## Variants

| File | What it adds |
|---|---|
| `main.py` | Traced version with split markers |
| `main_v2.py` | Alternate implementation |
| `main_v3.py` | Alternate implementation |

## Run

```bash
python3 main.py
```

Enter the size, then the elements separated by spaces.

## Complexity

`O(n log n)` time in the best, average, and worst case — the split is always
balanced. Space is `O(n)` for the auxiliary merge array. Merge sort is **stable**
and its performance is input-order-independent.
