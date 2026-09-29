# DAA Algorithm Visualizer

**DAA Lab — Assignment: an interactive [Streamlit](https://streamlit.io/) app that
visualizes every algorithm implemented in this repository.**

`app.py` is a single self-contained app. Pick a category and algorithm from the
sidebar and it draws the algorithm's result — graphs, matrices, boards, trees, and
step traces. Each algorithm is reimplemented inside the app as a pure function (no
console input), so the app does not depend on the other folders.

## Algorithms covered

| Category | Visualizations |
|---|---|
| Divide & Conquer | MaxMin recursion tree, Merge Sort steps, Quick Sort partitions, Strassen matrices |
| Greedy | Fractional Knapsack table, Prim & Kruskal MST (highlighted), Dijkstra shortest-path tree, Huffman codes |
| Dynamic Programming | Multistage Graph (path highlighted), Floyd–Warshall matrix stepper |
| Backtracking | N-Queens board browser, Sum of Subsets, Graph Colouring (coloured graph) |
| Branch & Bound | 0/1 Knapsack selection |
| String Matching | KMP & Boyer–Moore with match highlighting, LPS and last-occurrence tables |

## Setup and run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens in the browser. Every view has editable inputs (with sensible
defaults) and updates live.

## Notes

- Graph algorithms draw the input graph and highlight the computed edges (MST,
  shortest-path tree, optimal multistage path). Undirected graphs use a circular
  layout; the multistage graph uses a left-to-right layered layout by stage.
- The Floyd–Warshall view has a slider to step through `A(0) … A(n)` and watch the
  distance matrix improve as each intermediate vertex is allowed.
- Only `streamlit`, `plotly`, and `pandas` are required — layouts are computed
  without any external graph library.
