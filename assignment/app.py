"""
DAA Lab — Algorithm Visualizer.

A single Streamlit app that visualizes every algorithm implemented in this
repository: divide and conquer, greedy, dynamic programming, backtracking,
branch and bound, and string matching. Each algorithm is reimplemented here as a
pure function (no console input) so the app is fully self-contained.

Run:
    pip install -r requirements.txt
    streamlit run app.py
"""

import heapq
import math
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

INF = float("inf")

# Colour-blind-friendly palette used throughout.
BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
RED = "#d62728"
GREY = "#9aa4b2"


# ──────────────────────────────────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────────────────────────────────
def parse_numbers(text):
    values = []
    for chunk in text.replace(",", " ").split():
        values.append(int(chunk))
    return values


def parse_floats(text):
    return [float(c) for c in text.replace(",", " ").split()]


def graph_figure(nodes, edges, pos, highlight=None, node_colors=None,
                 directed=False, title=""):
    """Draw a weighted graph. `edges` is a list of (u, v, w); `highlight` is a
    set of frozenset({u, v}) (or (u, v) tuples for directed) drawn in orange."""
    highlight = highlight or set()
    edge_traces = []
    annotations = []
    for u, v, w in edges:
        key = (u, v) if directed else frozenset((u, v))
        is_hi = key in highlight
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_traces.append(
            go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(color=ORANGE if is_hi else GREY, width=4 if is_hi else 1.5),
                hoverinfo="skip", showlegend=False,
            )
        )
        annotations.append(
            dict(x=(x0 + x1) / 2, y=(y0 + y1) / 2, text=str(w),
                 showarrow=False, font=dict(size=12, color="#333"),
                 bgcolor="rgba(255,255,255,0.7)")
        )
        if directed:
            annotations.append(
                dict(ax=x0, ay=y0, x=x1, y=y1, xref="x", yref="y",
                     axref="x", ayref="y", showarrow=True, arrowhead=3,
                     arrowsize=1.2, arrowwidth=1.5,
                     arrowcolor=ORANGE if is_hi else GREY, opacity=0.8)
            )

    node_x = [pos[n][0] for n in nodes]
    node_y = [pos[n][1] for n in nodes]
    colors = [node_colors.get(n, BLUE) if node_colors else BLUE for n in nodes]
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=[str(n) for n in nodes], textposition="middle center",
        textfont=dict(color="white", size=13),
        marker=dict(size=34, color=colors, line=dict(width=2, color="white")),
        hoverinfo="text", showlegend=False,
    )

    fig = go.Figure(edge_traces + [node_trace])
    fig.update_layout(
        title=title, margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        paper_bgcolor="white", plot_bgcolor="white",
        annotations=annotations, height=460,
    )
    return fig


def circular_layout(nodes):
    """Evenly space nodes on a circle — dependency-free and deterministic."""
    n = len(nodes)
    pos = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / max(1, n)
        pos[node] = (math.cos(angle), math.sin(angle))
    return pos


def layered_layout(nodes, edges):
    """Left-to-right layered layout: x = longest distance from the source,
    y spreads nodes within a stage. Ideal for staged/DAG graphs."""
    succ = defaultdict(list)
    for u, v, _ in edges:
        succ[u].append(v)
    stage = {n: 0 for n in nodes}
    for _ in range(len(nodes)):
        for u, v, _ in edges:
            if stage[u] + 1 > stage[v]:
                stage[v] = stage[u] + 1
    groups = defaultdict(list)
    for n in nodes:
        groups[stage[n]].append(n)
    pos = {}
    for s, members in groups.items():
        members = sorted(members)
        for i, n in enumerate(members):
            pos[n] = (s, -(i - (len(members) - 1) / 2))
    return pos


# ──────────────────────────────────────────────────────────────────────────
# Divide & Conquer
# ──────────────────────────────────────────────────────────────────────────
def maxmin_build(a, i, j, nodes, edges, parent_id=None):
    node_id = len(nodes)
    nodes.append({"id": node_id, "label": f"MaxMin({i},{j})", "parent": parent_id})
    if parent_id is not None:
        edges.append((parent_id, node_id))
    if i == j:
        res = (a[i], a[i]); nodes[node_id]["type"] = "base1"
    elif i == j - 1:
        res = (max(a[i], a[j]), min(a[i], a[j])); nodes[node_id]["type"] = "base2"
    else:
        mid = (i + j) // 2
        nodes[node_id]["type"] = "split"
        mx1, mn1 = maxmin_build(a, i, mid, nodes, edges, node_id)
        mx2, mn2 = maxmin_build(a, mid + 1, j, nodes, edges, node_id)
        res = (max(mx1, mx2), min(mn1, mn2))
    nodes[node_id]["result"] = res
    return res


def maxmin_tree_figure(nodes, edges):
    x_pos, y_pos = {}, {}

    def depth(n):
        d, p = 0, nodes[n]["parent"]
        while p is not None:
            d += 1; p = nodes[p]["parent"]
        return d

    leaf = [0]

    def assign_x(nid):
        children = [n["id"] for n in nodes if n["parent"] == nid]
        if not children:
            x_pos[nid] = leaf[0]; leaf[0] += 1
        else:
            for c in children:
                assign_x(c)
            x_pos[nid] = sum(x_pos[c] for c in children) / len(children)

    root = next(n["id"] for n in nodes if n["parent"] is None)
    assign_x(root)
    for n in nodes:
        y_pos[n["id"]] = -depth(n["id"])

    ex, ey = [], []
    for p, c in edges:
        ex += [x_pos[p], x_pos[c], None]
        ey += [y_pos[p], y_pos[c], None]

    palette = {"split": BLUE, "base1": GREEN, "base2": ORANGE}
    labels = [f"{n['label']}<br>max={n['result'][0]}, min={n['result'][1]}" for n in nodes]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines",
                             line=dict(color=GREY, width=2), hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=[x_pos[n["id"]] for n in nodes], y=[y_pos[n["id"]] for n in nodes],
        mode="markers+text", text=labels, textposition="top center",
        marker=dict(size=40, color=[palette[n["type"]] for n in nodes],
                    line=dict(width=1, color="white")), hoverinfo="text"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                      xaxis=dict(visible=False), yaxis=dict(visible=False),
                      paper_bgcolor="white", plot_bgcolor="white", height=480)
    return fig


def view_maxmin():
    st.caption("Divide and conquer: split the array, solve each half, combine "
               "with one max and one min comparison. Uses 3n/2 − 2 comparisons.")
    text = st.text_area("Numbers", "8 3 12 5 9 1 14 7")
    if st.button("Run MaxMin", type="primary"):
        values = parse_numbers(text)
        a = [0] + values
        nodes, edges = [], []
        mx, mn = maxmin_build(a, 1, len(values), nodes, edges)
        c1, c2 = st.columns(2)
        c1.metric("Maximum", mx); c2.metric("Minimum", mn)
        st.plotly_chart(maxmin_tree_figure(nodes, edges), use_container_width=True)


def merge_sort_frames(a):
    frames = []

    def rec(arr, offset):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = rec(arr[:mid], offset)
        right = rec(arr[mid:], offset + mid)
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged += left[i:] + right[j:]
        frames.append((f"merge {left} + {right}", merged[:]))
        return merged

    result = rec(a[:], 0)
    return result, frames


def view_merge_sort():
    st.caption("Divide and conquer: recursively split in half, then merge the "
               "sorted halves. Stable, O(n log n) in every case.")
    text = st.text_area("Numbers", "38 27 43 3 9 82 10")
    if st.button("Run Merge Sort", type="primary"):
        a = parse_numbers(text)
        result, frames = merge_sort_frames(a)
        st.success(f"Sorted: {result}")
        st.write("**Merge steps** (bottom-up):")
        for label, merged in frames:
            st.code(f"{label}  →  {merged}")


def quick_sort_frames(a):
    frames = []

    def partition(arr, lo, hi):
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]; i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        frames.append((pivot, lo, hi, arr[:]))
        return i

    def rec(arr, lo, hi):
        if lo < hi:
            p = partition(arr, lo, hi)
            rec(arr, lo, p - 1)
            rec(arr, p + 1, hi)

    arr = a[:]
    rec(arr, 0, len(arr) - 1)
    return arr, frames


def view_quick_sort():
    st.caption("Divide and conquer: choose a pivot, partition around it, recurse "
               "on each side. Average O(n log n), in place.")
    text = st.text_area("Numbers", "10 80 30 90 40 50 70")
    if st.button("Run Quick Sort", type="primary"):
        a = parse_numbers(text)
        result, frames = quick_sort_frames(a)
        st.success(f"Sorted: {result}")
        st.write("**Partition steps** (pivot in bold range):")
        for pivot, lo, hi, arr in frames:
            st.code(f"pivot={pivot}  range[{lo}..{hi}]  →  {arr}")


def strassen(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    m = n // 2
    def sub(M, r, c): return [row[c:c + m] for row in M[r:r + m]]
    def add(X, Y): return [[X[i][j] + Y[i][j] for j in range(len(X))] for i in range(len(X))]
    def dif(X, Y): return [[X[i][j] - Y[i][j] for j in range(len(X))] for i in range(len(X))]
    A11, A12, A21, A22 = sub(A, 0, 0), sub(A, 0, m), sub(A, m, 0), sub(A, m, m)
    B11, B12, B21, B22 = sub(B, 0, 0), sub(B, 0, m), sub(B, m, 0), sub(B, m, m)
    P = strassen(add(A11, A22), add(B11, B22))
    Q = strassen(add(A21, A22), B11)
    R = strassen(A11, dif(B12, B22))
    S = strassen(A22, dif(B21, B11))
    T = strassen(add(A11, A12), B22)
    U = strassen(dif(A21, A11), add(B11, B12))
    V = strassen(dif(A12, A22), add(B21, B22))
    C11 = add(dif(add(P, S), T), V)
    C12 = add(R, T)
    C21 = add(Q, S)
    C22 = add(dif(add(P, R), Q), U)
    C = [C11[i] + C12[i] for i in range(m)] + [C21[i] + C22[i] for i in range(m)]
    return C


def view_strassen():
    st.caption("Divide and conquer: multiply n×n matrices (n a power of 2) with "
               "7 recursive products instead of 8. O(n^2.807).")
    size = st.selectbox("Matrix size", [2, 4], index=0)
    c1, c2 = st.columns(2)
    default = "\n".join(" ".join(str((i + j) % 5 + 1) for j in range(size)) for i in range(size))
    a_text = c1.text_area("Matrix A (rows)", default, key="sa")
    b_text = c2.text_area("Matrix B (rows)", default, key="sb")
    if st.button("Multiply", type="primary"):
        A = [parse_numbers(r) for r in a_text.strip().splitlines()]
        B = [parse_numbers(r) for r in b_text.strip().splitlines()]
        C = strassen(A, B)
        c1.write("**A**"); c1.dataframe(pd.DataFrame(A))
        c2.write("**B**"); c2.dataframe(pd.DataFrame(B))
        st.write("**A × B**"); st.dataframe(pd.DataFrame(C))


# ──────────────────────────────────────────────────────────────────────────
# Greedy
# ──────────────────────────────────────────────────────────────────────────
def view_fractional_knapsack():
    st.caption("Greedy: take items by best profit/weight ratio, allowing a "
               "fraction of the last item. Optimal for the fractional problem.")
    c1, c2, c3 = st.columns(3)
    w_text = c1.text_input("Weights", "10 20 30")
    p_text = c2.text_input("Profits", "60 100 120")
    cap = c3.number_input("Capacity", value=50.0)
    if st.button("Fill knapsack", type="primary"):
        w = parse_floats(w_text); p = parse_floats(p_text)
        order = sorted(range(len(w)), key=lambda i: p[i] / w[i], reverse=True)
        rows, weight, profit = [], 0.0, 0.0
        for i in order:
            if weight + w[i] <= cap:
                frac = 1.0
            else:
                frac = (cap - weight) / w[i]
            rows.append({"item": i + 1, "weight": w[i], "profit": p[i],
                         "ratio": round(p[i] / w[i], 2), "fraction taken": round(frac, 3)})
            weight += w[i] * frac; profit += p[i] * frac
            if frac < 1.0:
                break
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.metric("Maximum profit", round(profit, 2))
        st.bar_chart(pd.DataFrame(rows).set_index("item")["fraction taken"])


def build_undirected(edges_text):
    edges, nodes = [], set()
    for line in edges_text.strip().splitlines():
        u, v, w = line.split()
        edges.append((int(u), int(v), int(w)))
        nodes.update((int(u), int(v)))
    return sorted(nodes), edges


def prim(nodes, edges):
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((w, v)); adj[v].append((w, u))
    start = nodes[0]
    visited = {start}
    heap = [(w, start, v) for w, v in adj[start]]
    heapq.heapify(heap)
    mst, cost = [], 0
    while heap and len(visited) < len(nodes):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v); mst.append((u, v, w)); cost += w
        for w2, x in adj[v]:
            if x not in visited:
                heapq.heappush(heap, (w2, v, x))
    return mst, cost


def kruskal(nodes, edges):
    parent = {n: n for n in nodes}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    mst, cost = [], 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; mst.append((u, v, w)); cost += w
    return mst, cost


def view_mst(which):
    algo = "Prim's" if which == "prim" else "Kruskal's"
    st.caption(f"Greedy: build a minimum spanning tree with {algo} algorithm. "
               "MST edges are highlighted in orange.")
    edges_text = st.text_area("Edges (u v w per line)",
                              "1 2 4\n1 3 1\n2 3 2\n2 4 5\n3 4 8\n3 5 6\n4 5 3",
                              height=160, key=f"mst_{which}")
    if st.button(f"Run {algo}", type="primary"):
        nodes, edges = build_undirected(edges_text)
        mst, cost = (prim if which == "prim" else kruskal)(nodes, edges)
        pos = circular_layout(nodes)
        hi = {frozenset((u, v)) for u, v, _ in mst}
        st.plotly_chart(graph_figure(nodes, edges, pos, highlight=hi,
                                     title=f"{algo} MST"), use_container_width=True)
        st.metric("Minimum cost", cost)
        st.write("**MST edges (in selection order):**")
        st.dataframe(pd.DataFrame(mst, columns=["u", "v", "weight"]),
                     use_container_width=True)


def dijkstra(nodes, edges, source):
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    dist = {n: INF for n in nodes}; dist[source] = 0
    parent = {n: None for n in nodes}
    heap = [(0, source)]; done = set()
    steps = []
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w; parent[v] = u
                heapq.heappush(heap, (dist[v], v))
        steps.append((u, dict(dist)))
    return dist, parent, steps


def view_dijkstra():
    st.caption("Greedy: shortest path from a source to every vertex. The "
               "shortest-path tree is highlighted.")
    edges_text = st.text_area("Edges (u v w per line)",
                              "1 2 7\n1 3 9\n1 6 14\n2 3 10\n2 4 15\n3 4 11\n3 6 2\n4 5 6\n5 6 9",
                              height=180, key="dij")
    if st.button("Run Dijkstra", type="primary"):
        nodes, edges = build_undirected(edges_text)
        source = nodes[0]
        dist, parent, steps = dijkstra(nodes, edges, source)
        pos = circular_layout(nodes)
        hi = {frozenset((parent[v], v)) for v in nodes if parent[v] is not None}
        st.plotly_chart(graph_figure(nodes, edges, pos, highlight=hi,
                                     title=f"Shortest paths from {source}"),
                        use_container_width=True)
        st.write(f"**Shortest distances from vertex {source}:**")
        st.dataframe(pd.DataFrame(
            [{"vertex": n, "distance": dist[n]} for n in nodes]),
            use_container_width=True)


def huffman_codes(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    heap = [[f, i, ch, None, None] for i, (ch, f) in enumerate(freq.items())]
    heapq.heapify(heap)
    counter = len(heap)
    nodes = {}  # id -> (symbol, left, right)
    while len(heap) > 1:
        a = heapq.heappop(heap); b = heapq.heappop(heap)
        nid = counter; counter += 1
        nodes[nid] = (None, a, b)
        heapq.heappush(heap, [a[0] + b[0], nid, None, a, b])
    root = heap[0]
    codes = {}

    def walk(node, prefix):
        f, nid, ch, left, right = node
        if ch is not None:
            codes[ch] = prefix or "0"
        else:
            walk(left, prefix + "0"); walk(right, prefix + "1")

    walk(root, "")
    return freq, codes


def view_huffman():
    st.caption("Greedy: build an optimal prefix code by repeatedly merging the "
               "two least-frequent symbols.")
    text = st.text_input("Text to compress", "mississippi")
    if st.button("Build Huffman code", type="primary") and text:
        freq, codes = huffman_codes(text)
        rows = [{"symbol": repr(ch), "frequency": freq[ch], "code": codes[ch],
                 "bits": len(codes[ch])} for ch in sorted(freq, key=lambda c: -freq[c])]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        encoded = "".join(codes[c] for c in text)
        fixed = len(text) * 8
        c1, c2, c3 = st.columns(3)
        c1.metric("Fixed (8-bit)", f"{fixed} bits")
        c2.metric("Huffman", f"{len(encoded)} bits")
        c3.metric("Compression", f"{len(encoded) / fixed:.0%}")
        st.code(encoded)


# ──────────────────────────────────────────────────────────────────────────
# Dynamic Programming
# ──────────────────────────────────────────────────────────────────────────
def view_multistage():
    st.caption("Dynamic programming: minimum-cost path through a staged graph "
               "using backward costs. The optimal path is highlighted.")
    edges_text = st.text_area(
        "Directed edges (u v w per line)",
        "1 2 9\n1 3 7\n1 4 3\n1 5 2\n2 6 4\n2 7 2\n2 8 1\n3 6 2\n3 7 7\n"
        "4 8 11\n5 7 11\n5 8 8\n6 9 6\n6 10 5\n7 9 4\n7 10 3\n8 10 5\n8 11 6\n"
        "9 12 4\n10 12 2\n11 12 5", height=200, key="ms")
    if st.button("Run Multistage", type="primary"):
        edges, nodes = [], set()
        for line in edges_text.strip().splitlines():
            u, v, w = map(int, line.split())
            edges.append((u, v, w)); nodes.update((u, v))
        n = max(nodes)
        cost = {(u, v): w for u, v, w in edges}
        succ = {u: [v for (uu, v) in cost if uu == u] for u in nodes}
        bcost = {n: 0}; nxt = {}
        for j in sorted(nodes, reverse=True):
            if j == n:
                continue
            best, choice = INF, None
            for v in succ.get(j, []):
                if cost[(j, v)] + bcost.get(v, INF) < best:
                    best = cost[(j, v)] + bcost[v]; choice = v
            bcost[j] = best; nxt[j] = choice
        path = [1]; v = 1
        while v != n:
            v = nxt[v]; path.append(v)
        pos = layered_layout(sorted(nodes), edges)
        hi = {(path[i], path[i + 1]) for i in range(len(path) - 1)}
        st.plotly_chart(graph_figure(sorted(nodes), edges, pos, highlight=hi,
                                     directed=True, title="Multistage graph"),
                        use_container_width=True)
        st.metric("Minimum cost", bcost[1])
        st.success("Optimal path:  " + " → ".join(map(str, path)))


def view_all_pairs():
    st.caption("Dynamic programming: Floyd–Warshall shortest path between every "
               "pair. Step through k to watch the matrix improve.")
    text = st.text_area("Cost matrix (INF for no edge; one row per line)",
                        "0 4 INF\nINF 0 2\n3 INF 0", height=120, key="ap")
    try:
        def cell(x): return INF if x.upper() == "INF" else int(x)
        A = [[cell(x) for x in row.split()] for row in text.strip().splitlines()]
        n = len(A)
        if n == 0 or any(len(row) != n for row in A):
            st.info("Enter a square cost matrix, one row per line.")
            return
    except ValueError:
        st.info("Enter integers (or INF) separated by spaces.")
        return
    snapshots = [("A(0) — direct edges", [row[:] for row in A])]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
        snapshots.append((f"A({k + 1}) — via vertex {k + 1}", [row[:] for row in A]))
    step = st.slider("Step k (intermediate vertices allowed)", 0, n, n)
    label, mat = snapshots[step]
    st.write(f"**{label}**")
    disp = [["INF" if v == INF else v for v in row] for row in mat]
    st.dataframe(pd.DataFrame(disp, index=range(1, n + 1),
                              columns=range(1, n + 1)), use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────
# Backtracking
# ──────────────────────────────────────────────────────────────────────────
def solve_n_queens(n):
    solutions = []
    def place(x, k):
        for i in range(k):
            if x[i] == x[k] or abs(x[i] - x[k]) == abs(i - k):
                return False
        return True
    def rec(x, k):
        if k == n:
            solutions.append(x[:]); return
        for col in range(n):
            x[k] = col
            if place(x, k):
                rec(x, k + 1)
    rec([0] * n, 0)
    return solutions


def board_figure(cols):
    n = len(cols)
    fig = go.Figure()
    for r in range(n):
        for c in range(n):
            fig.add_shape(type="rect", x0=c, y0=n - 1 - r, x1=c + 1, y1=n - r,
                          fillcolor="#eaeaea" if (r + c) % 2 else "white",
                          line=dict(color="#ccc"))
    fig.add_trace(go.Scatter(
        x=[c + 0.5 for c in cols], y=[n - 1 - r + 0.5 for r in range(n)],
        mode="text", text=["♛"] * n, textfont=dict(size=28), hoverinfo="skip"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=430,
                      xaxis=dict(visible=False, range=[0, n]),
                      yaxis=dict(visible=False, range=[0, n], scaleanchor="x"),
                      showlegend=False, paper_bgcolor="white")
    return fig


def view_n_queens():
    st.caption("Backtracking: place n queens so none attack each other. "
               "Change the board size or browse the solutions live.")
    n = st.slider("Board size n", 4, 8, 6)
    sols = solve_n_queens(n)
    st.success(f"{len(sols)} solutions for {n}-Queens.")
    if sols:
        idx = st.number_input("Show solution #", 1, len(sols), 1) - 1
        st.plotly_chart(board_figure(sols[idx]), use_container_width=True)


def view_sum_of_subsets():
    st.caption("Backtracking: find every subset that sums exactly to the target.")
    c1, c2 = st.columns(2)
    text = c1.text_input("Weights", "1 2 3 4 5")
    target = c2.number_input("Target sum", value=7)
    if st.button("Find subsets", type="primary"):
        w = sorted(parse_numbers(text))
        found = []
        def rec(k, current, chosen):
            if current == target:
                found.append(chosen[:]); return
            if k >= len(w) or current > target:
                return
            rec(k + 1, current + w[k], chosen + [w[k]])  # include
            rec(k + 1, current, chosen)                   # exclude
        rec(0, 0, [])
        # de-duplicate identical subsets
        uniq = sorted({tuple(s) for s in found})
        if uniq:
            st.success(f"{len(uniq)} subset(s) sum to {target}:")
            for s in uniq:
                st.code(f"{list(s)}  →  {sum(s)}")
        else:
            st.warning("No subset sums to the target.")


def view_graph_coloring():
    st.caption("Backtracking: colour vertices so no edge joins two of the same "
               "colour, using at most m colours.")
    c1, c2 = st.columns([3, 1])
    edges_text = c1.text_area("Edges (u v per line)",
                              "1 2\n1 3\n2 3\n3 4\n4 5\n5 1", height=150, key="gc")
    m = c2.number_input("Colours m", 1, 8, 3)
    if st.button("Colour graph", type="primary"):
        edges, nodes = [], set()
        for line in edges_text.strip().splitlines():
            u, v = map(int, line.split()); edges.append((u, v, "")); nodes.update((u, v))
        nodes = sorted(nodes)
        idx = {n: i for i, n in enumerate(nodes)}
        adj = [[0] * len(nodes) for _ in nodes]
        for u, v, _ in edges:
            adj[idx[u]][idx[v]] = adj[idx[v]][idx[u]] = 1
        colouring = [0] * len(nodes)
        def ok(k, c):
            return all(not (adj[k][j] and colouring[j] == c) for j in range(len(nodes)))
        def rec(k):
            if k == len(nodes):
                return True
            for c in range(1, m + 1):
                if ok(k, c):
                    colouring[k] = c
                    if rec(k + 1):
                        return True
                    colouring[k] = 0
            return False
        if rec(0):
            palette = [BLUE, ORANGE, GREEN, RED, "#9467bd", "#8c564b", "#e377c2", "#17becf"]
            node_colors = {n: palette[(colouring[idx[n]] - 1) % len(palette)] for n in nodes}
            pos = circular_layout(nodes)
            st.plotly_chart(graph_figure(nodes, edges, pos, node_colors=node_colors,
                                         title=f"{m}-colouring"), use_container_width=True)
            st.success(f"Valid colouring found with {m} colours: "
                       + ", ".join(f"{n}→c{colouring[idx[n]]}" for n in nodes))
        else:
            st.error(f"The graph cannot be coloured with {m} colours.")


# ──────────────────────────────────────────────────────────────────────────
# Branch & Bound
# ──────────────────────────────────────────────────────────────────────────
def knapsack_01_bb(w, p, capacity):
    n = len(w)
    order = sorted(range(n), key=lambda i: p[i] / w[i], reverse=True)
    w = [w[i] for i in order]; p = [p[i] for i in order]

    def bound(level, weight, profit):
        if weight >= capacity:
            return 0
        b, tw, j = profit, weight, level + 1
        while j < n and tw + w[j] <= capacity:
            tw += w[j]; b += p[j]; j += 1
        if j < n:
            b += (capacity - tw) * (p[j] / w[j])
        return b

    heap = [(-bound(-1, 0, 0), -1, 0, 0, [])]  # (-bound, level, profit, weight, taken)
    best, best_taken = 0, []
    while heap:
        nb, level, profit, weight, taken = heapq.heappop(heap)
        if -nb <= best:
            continue
        level += 1
        if level >= n:
            continue
        w2, p2 = weight + w[level], profit + p[level]
        if w2 <= capacity and p2 > best:
            best, best_taken = p2, taken + [level]
        for take, nw, npf, nt in ((True, w2, p2, taken + [level]),
                                   (False, weight, profit, taken)):
            b = bound(level, nw, npf)
            if b > best:
                heapq.heappush(heap, (-b, level, npf, nw, nt))
    return best, sorted(order[i] + 1 for i in best_taken)


def view_knapsack_bb():
    st.caption("Branch and bound: 0/1 knapsack (each item whole or not), pruning "
               "with the fractional upper bound.")
    c1, c2, c3 = st.columns(3)
    w_text = c1.text_input("Weights", "2 3 4 5", key="bbw")
    p_text = c2.text_input("Profits", "3 5 6 10", key="bbp")
    cap = c3.number_input("Capacity", value=5.0, key="bbc")
    if st.button("Solve 0/1 Knapsack", type="primary"):
        w = parse_floats(w_text); p = parse_floats(p_text)
        best, chosen = knapsack_01_bb(w, p, cap)
        st.metric("Maximum profit", best)
        st.success(f"Items selected (1-indexed): {chosen}")
        rows = [{"item": i + 1, "weight": w[i], "profit": p[i],
                 "selected": "✓" if (i + 1) in chosen else ""} for i in range(len(w))]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────
# String matching
# ──────────────────────────────────────────────────────────────────────────
def compute_lps(pattern):
    lps = [0] * len(pattern); length = 0; i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1; lps[i] = length; i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0; i += 1
    return lps


def kmp_search(text, pattern):
    lps = compute_lps(pattern); matches = []; i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
            if j == len(pattern):
                matches.append(i - j); j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return matches, lps


def boyer_moore(text, pattern):
    last = {ch: i for i, ch in enumerate(pattern)}
    m, n = len(pattern), len(text); matches = []; s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            matches.append(s); s += 1
        else:
            s += max(1, j - last.get(text[s + j], -1))
    return matches, last


def highlight_matches(text, pattern, matches):
    covered = [False] * len(text)
    for m in matches:
        for k in range(m, m + len(pattern)):
            covered[k] = True
    html = ""
    for i, ch in enumerate(text):
        if covered[i]:
            html += f"<span style='background:#ffe08a;font-weight:bold'>{ch}</span>"
        else:
            html += ch
    return f"<div style='font-family:monospace;font-size:18px'>{html}</div>"


def view_string_matching():
    st.caption("Two exact string-matching algorithms. Matches are highlighted; "
               "both agree on the positions.")
    c1, c2 = st.columns(2)
    text = c1.text_input("Text", "abababcababc")
    pattern = c2.text_input("Pattern", "ababc")
    if st.button("Search", type="primary") and pattern:
        kmp, lps = kmp_search(text, pattern)
        bm, last = boyer_moore(text, pattern)
        st.markdown(highlight_matches(text, pattern, kmp), unsafe_allow_html=True)
        st.write("")
        c1, c2 = st.columns(2)
        c1.metric("KMP matches at", str(kmp or "none"))
        c2.metric("Boyer–Moore matches at", str(bm or "none"))
        c1.write("**KMP LPS table**")
        c1.dataframe(pd.DataFrame({"char": list(pattern), "lps": lps}))
        c2.write("**Boyer–Moore last-occurrence**")
        c2.dataframe(pd.DataFrame([{"char": k, "index": v} for k, v in last.items()]))


# ──────────────────────────────────────────────────────────────────────────
# App shell
# ──────────────────────────────────────────────────────────────────────────
ALGORITHMS = {
    "Divide & Conquer": {
        "MaxMin (find max & min)": view_maxmin,
        "Merge Sort": view_merge_sort,
        "Quick Sort": view_quick_sort,
        "Strassen's Matrix Multiplication": view_strassen,
    },
    "Greedy": {
        "Fractional Knapsack": view_fractional_knapsack,
        "Prim's MST": lambda: view_mst("prim"),
        "Kruskal's MST": lambda: view_mst("kruskal"),
        "Dijkstra's Shortest Path": view_dijkstra,
        "Huffman Coding": view_huffman,
    },
    "Dynamic Programming": {
        "Multistage Graph": view_multistage,
        "All Pairs Shortest Path (Floyd–Warshall)": view_all_pairs,
    },
    "Backtracking": {
        "N-Queens": view_n_queens,
        "Sum of Subsets": view_sum_of_subsets,
        "Graph Colouring": view_graph_coloring,
    },
    "Branch & Bound": {
        "0/1 Knapsack": view_knapsack_bb,
    },
    "String Matching": {
        "KMP & Boyer–Moore": view_string_matching,
    },
}


def main():
    st.set_page_config(page_title="DAA Algorithm Visualizer", layout="wide")
    st.sidebar.title("DAA Algorithm Visualizer")
    st.sidebar.caption("CMP-307 — Design and Analysis of Algorithms Lab")
    category = st.sidebar.radio("Category", list(ALGORITHMS.keys()))
    algorithm = st.sidebar.selectbox("Algorithm", list(ALGORITHMS[category].keys()))
    st.sidebar.markdown("---")
    st.sidebar.caption("Interactive companion to the console programs in this "
                       "repository. Each view reimplements the algorithm and "
                       "draws its result.")

    st.title(algorithm)
    ALGORITHMS[category][algorithm]()


if __name__ == "__main__":
    main()
