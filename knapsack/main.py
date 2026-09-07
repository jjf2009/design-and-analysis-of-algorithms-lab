"""0/1 knapsack solved with dynamic programming.

Each item can be selected at most once.  The solver returns both the maximum
value and the zero-based indexes of the selected items.
"""


def knapsack(weights, values, capacity):
    """Return ``(maximum_value, selected_indices)`` for a 0/1 knapsack.

    ``weights`` and ``values`` must have the same length.  Weights and the
    capacity must be non-negative integers; values may be any numbers.
    """

    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a non-negative integer")
    if any(not isinstance(weight, int) or weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative integers")

    item_count = len(weights)
    table = [[0] * (capacity + 1) for _ in range(item_count + 1)]

    for item in range(1, item_count + 1):
        weight = weights[item - 1]
        value = values[item - 1]

        for current_capacity in range(capacity + 1):
            table[item][current_capacity] = table[item - 1][current_capacity]
            if weight <= current_capacity:
                with_item = table[item - 1][current_capacity - weight] + value
                table[item][current_capacity] = max(
                    table[item][current_capacity], with_item
                )

    selected_indices = []
    current_capacity = capacity
    for item in range(item_count, 0, -1):
        if table[item][current_capacity] != table[item - 1][current_capacity]:
            selected_indices.append(item - 1)
            current_capacity -= weights[item - 1]

    selected_indices.reverse()
    return table[item_count][capacity], selected_indices


def main():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    maximum_value, selected_indices = knapsack(weights, values, capacity)
    print(f"Maximum value: {maximum_value}")
    print(f"Selected item indexes: {selected_indices}")


if __name__ == "__main__":
    main()
