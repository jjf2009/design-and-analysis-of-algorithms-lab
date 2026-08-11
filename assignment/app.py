import streamlit as st
import plotly.graph_objects as go


def parse_numbers(text: str):
    values = []
    for chunk in text.replace(",", " ").split():
        values.append(int(chunk))
    return values


def MaxMin(a, i, j, nodes, edges, trace, parent_id=None, side=None):
    """
    1-indexed divide-and-conquer MaxMin, matching the reference algorithm:
        Small(P): i == j            -> max = min = a[i]
        Small(P): i == j - 1        -> compare pair
        else: split at mid, recurse left/right, combine
    Builds the recursion tree (nodes/edges) and a trace table as it goes.
    """
    node_id = len(nodes)
    label = f"MaxMin({i}, {j})"
    nodes.append(
        {
            "id": node_id,
            "label": label,
            "range": (i, j),
            "parent": parent_id,
            "side": side,
        }
    )
    if parent_id is not None:
        edges.append((parent_id, node_id))

    # Small(P)
    if i == j:
        max_, min_ = a[i], a[i]
        nodes[node_id]["type"] = "base-1"
        nodes[node_id]["result"] = (max_, min_)
        trace.append((i, j, max_, min_))
        return max_, min_, node_id

    # Another case of Small(P)
    elif i == j - 1:
        if a[i] < a[j]:
            max_, min_ = a[j], a[i]
        else:
            max_, min_ = a[i], a[j]
        nodes[node_id]["type"] = "base-2"
        nodes[node_id]["result"] = (max_, min_)
        trace.append((i, j, max_, min_))
        return max_, min_, node_id

    # Divide
    else:
        mid = (i + j) // 2
        nodes[node_id]["type"] = "split"
        nodes[node_id]["mid"] = mid

        max1, min1, _ = MaxMin(a, i, mid, nodes, edges, trace, node_id, "L")
        max2, min2, _ = MaxMin(a, mid + 1, j, nodes, edges, trace, node_id, "R")

        max_ = max1 if max1 > max2 else max2
        min_ = min1 if min1 < min2 else min2

        nodes[node_id]["result"] = (max_, min_)
        trace.append((i, j, max_, min_))
        return max_, min_, node_id


def tree_figure(nodes, edges):
    levels = {}
    for node in nodes:
        depth = 0
        parent = node["parent"]
        while parent is not None:
            depth += 1
            parent = nodes[parent]["parent"]
        levels.setdefault(depth, []).append(node["id"])

    # Position leaves left-to-right by in-order traversal so the tree
    # doesn't overlap, then place internal nodes at the mean of children.
    x_pos = {}
    y_pos = {}

    def assign_x(node_id, next_leaf_x):
        node = nodes[node_id]
        children = [n["id"] for n in nodes if n["parent"] == node_id]
        if not children:
            x_pos[node_id] = next_leaf_x[0]
            next_leaf_x[0] += 1
        else:
            for c in children:
                assign_x(c, next_leaf_x)
            xs = [x_pos[c] for c in children]
            x_pos[node_id] = sum(xs) / len(xs)

    root_id = next(n["id"] for n in nodes if n["parent"] is None)
    assign_x(root_id, [0])

    for node in nodes:
        depth = 0
        parent = node["parent"]
        while parent is not None:
            depth += 1
            parent = nodes[parent]["parent"]
        y_pos[node["id"]] = -depth

    edge_x = []
    edge_y = []
    for parent_id, child_id in edges:
        edge_x.extend([x_pos[parent_id], x_pos[child_id], None])
        edge_y.extend([y_pos[parent_id], y_pos[child_id], None])

    node_x = []
    node_y = []
    labels = []
    colors = []

    for node in nodes:
        node_x.append(x_pos[node["id"]])
        node_y.append(y_pos[node["id"]])
        result = node.get("result")
        if result:
            label = f"{node['label']}<br>max={result[0]}, min={result[1]}"
        else:
            label = node["label"]
        labels.append(label)
        if node["type"] == "split":
            colors.append("#1f77b4")
        elif node["type"] == "base-1":
            colors.append("#2ca02c")
        else:
            colors.append("#ff7f0e")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="#9aa4b2", width=2),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=labels,
            textposition="top center",
            marker=dict(size=42, color=colors, line=dict(width=1, color="white")),
            hoverinfo="text",
            showlegend=False,
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=max(420, 130 + 100 * len(levels)),
    )
    return fig


st.set_page_config(page_title="MaxMin Visualizer", layout="wide")
st.title("MaxMin Recursive Tree Visualizer")
st.write(
    "Enter a list of integers to see the divide-and-conquer MaxMin recursion "
    "tree (1-indexed, matching the classic algorithm)."
)

default_values = "8 3 12 5 9 1 14 7"
input_text = st.text_area("Numbers", value=default_values, help="Use spaces or commas between numbers.")

if st.button("Run MaxMin"):
    try:
        values = parse_numbers(input_text)
        n = len(values)
        if n < 1:
            st.error("Please enter at least one integer.")
        else:
            # Dummy element at index 0 to make the array 1-indexed,
            # matching the reference implementation.
            a = [0] + values

            nodes = []
            edges = []
            trace = []
            maximum, minimum, _ = MaxMin(a, 1, n, nodes, edges, trace)

            col1, col2 = st.columns(2)
            col1.metric("Maximum", maximum)
            col2.metric("Minimum", minimum)

            st.subheader("Recursive Call Tree")
            st.plotly_chart(tree_figure(nodes, edges), use_container_width=True)

            st.subheader("Trace (i j max min)")
            st.caption("Printed in the order each call resolves, just like the console version.")
            trace_lines = ["i j max min"] + [f"{i} {j} {mx} {mn}" for i, j, mx, mn in trace]
            st.code("\n".join(trace_lines))

            st.subheader("Call Details")
            for node in nodes:
                result = node.get("result")
                if result:
                    st.write(f"{node['label']} -> max={result[0]}, min={result[1]}")
                else:
                    st.write(node["label"])
    except ValueError:
        st.error("Please enter only integers separated by spaces or commas.")