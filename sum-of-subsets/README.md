# Sum of Subsets (Backtracking)

**DAA Lab — Experiment 11: Sum of Subsets problem using Backtracking.**

`main.py` finds every subset of a set of positive weights that sums exactly to a
target, using the bounded backtracking formulation from Horowitz–Sahni. The
weights are sorted ascending so the bounding conditions apply.

## Algorithm

`SumOfSubsets(k, remaining, current, target)` decides weight `w[k]`:

- **Include** `w[k]` when `current + w[k] ≤ target`; if it hits the target
  exactly, the subset is printed.
- **Exclude** `w[k]` only if the not-yet-considered weights can still reach the
  target (`current + remaining − w[k] ≥ target`) and the next weight would still
  fit (`current + w[k+1] ≤ target`).

These two bounds cut off branches that cannot possibly succeed.

## Run

```bash
python3 main.py
```

Enter the element count, the elements, and the target sum.

## Complexity

`O(2ⁿ)` in the worst case (all subsets), but the bounding conditions prune many
branches. Space is `O(n)` for the recursion.
