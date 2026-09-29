# Quick Sort

**DAA Lab — Experiment 2 (part b): Quick Sort.**

`main.py` implements 1-indexed quick sort using the Hoare-style partition from
Horowitz–Sahni, with a sentinel `∞` at the end of the array. It highlights the
pivot in bold and prints the array after each partition so the process can be
traced.

## Algorithm

`Partition(a, m, p)` takes the first element `a[m]` as the pivot `v`, then walks
`i` up from the left while `a[i] < v` and `j` down from the right while
`a[j] > v`, swapping the out-of-place pair whenever `i < j`. When the pointers
cross, the pivot is dropped into position `j`, splitting the range so everything
left of the pivot is `≤ v` and everything right is `≥ v`. `QuickSort` then
recurses on the two partitions.

## Variants

| File | What it adds |
|---|---|
| `main.py` | Traced version with pivot highlighting |
| `main_v2.py` | Alternate implementation |

## Run

```bash
python3 main.py
```

Enter the size, then the elements separated by spaces.

## Complexity

Average `O(n log n)`; worst case `O(n²)` on already-sorted or reverse-sorted
input with first-element pivot. In-place — `O(log n)` stack space on average.
Quick sort is **not stable**.
