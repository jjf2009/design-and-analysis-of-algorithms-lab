# Strassen's Matrix Multiplication

**DAA Lab — Experiment 3: Strassen's Matrix Multiplication.**

`main.py` multiplies two `n × n` matrices (where `n` is a power of 2) with
Strassen's divide-and-conquer method, which needs only **7** recursive
multiplications of `n/2 × n/2` blocks instead of the 8 used by the standard
block method.

## Algorithm

Each matrix is split into four quadrants. Strassen computes seven products
`P … V` from sums and differences of quadrants, then combines them into the four
result quadrants `C11, C12, C21, C22`:

```
P = (A11 + A22)(B11 + B22)      C11 = P + S - T + V
Q = (A21 + A22) B11             C12 = R + T
R = A11 (B12 - B22)             C21 = Q + S
S = A22 (B21 - B11)             C22 = P + R - Q + U
T = (A11 + A12) B22
U = (A21 - A11)(B11 + B12)
V = (A12 - A22)(B21 + B22)
```

Helpers `add_matrix` and `subtract_matrix` do the quadrant arithmetic; recursion
bottoms out at the `1 × 1` base case.

## Run

```bash
python3 main.py
```

Enter the size (a power of 2: 2, 4, 8, …), then each matrix row by row.

## Complexity

`O(n^log₂7) ≈ O(n^2.807)`, beating the `O(n³)` of standard multiplication for
large `n`. The trade-off is extra additions and auxiliary matrices.
