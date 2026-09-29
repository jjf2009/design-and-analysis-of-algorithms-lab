# Graph Coloring (Backtracking)

**DAA Lab — Experiment 12: Graph Coloring using Backtracking.**

`main.py` solves the m-colouring problem: assign one of `m` colours to every
vertex of a graph so that no edge joins two vertices of the same colour. It finds
**all** valid colourings by backtracking.

## Algorithm

`NextValue(x, k, m)` cycles vertex `k` through colours `1 … m` (0 means "no
colour left"), skipping any colour already used by an adjacent vertex.
`MColoring(x, k, m)` assigns a colour to vertex `k`, then recurses to vertex
`k + 1`; when the last vertex is coloured, the assignment is printed. Exhausting
the colours for a vertex backtracks to the previous one.

## Run

```bash
python3 main.py
```

Enter the vertex count, the number of colours `m`, then the adjacency matrix rows
(`0`/`1`).

## Complexity

`O(mⁿ)` in the worst case — `m` colour choices for each of `n` vertices — reduced
in practice by the adjacency pruning. Space is `O(n)`.
