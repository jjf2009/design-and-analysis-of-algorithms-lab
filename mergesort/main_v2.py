"""Merge sort benchmark using two elapsed-time measurement methods."""

import random
import string
import time


# Global arrays

a = []
b = []

split_positions = []
SHOW_PROCESS = False


def display():

    result = ""

    for i in range(1, len(a)):

        result += str(a[i])

        if i in split_positions:
            result += " | "
        elif i < len(a) - 1:
            result += " "

    print(result)


def MergeSort(low, high):

    if low < high:

        # Divide P into subproblems
        mid = (low + high) // 2

        # Add the split
        split_positions.append(mid)

        # Display the split
        if SHOW_PROCESS:
            display()

        # Solve the subproblems
        MergeSort(low, mid)
        MergeSort(mid + 1, high)

        # Combine the solutions
        Merge(low, mid, high)

        # Remove the split after merging
        if mid in split_positions:
            split_positions.remove(mid)

        # Display the merged result
        if SHOW_PROCESS:
            display()


def Merge(low, mid, high):

    # h := low, i := low, j := mid + 1
    h = low
    i = low
    j = mid + 1

    # while (h <= mid) and (j <= high)
    while (h <= mid) and (j <= high):

        if a[h] <= a[j]:
            b[i] = a[h]
            h = h + 1

        else:
            b[i] = a[j]
            j = j + 1

        i = i + 1

    # if (h > mid)
    if h > mid:

        for k in range(j, high + 1):
            b[i] = a[k]
            i = i + 1

    # else
    else:

        for k in range(h, mid + 1):
            b[i] = a[k]
            i = i + 1

    # Copy merged elements back
    for k in range(low, high + 1):
        a[k] = b[k]


SIZES = (100, 200, 500, 7500, 10000)
DATA_TYPES = ("Integer", "Float", "Alphabet", "String")


def generate_data(data_type, size):
    """Generate one homogeneous random dataset for the requested type."""

    if data_type == "Integer":
        return [random.randint(1000, 9999) for _ in range(size)]

    if data_type == "Float":
        return [round(random.uniform(1000, 9999), 4) for _ in range(size)]

    if data_type == "Alphabet":
        return [random.choice(string.ascii_uppercase) for _ in range(size)]

    if data_type == "String":
        return [
            "".join(random.choices(string.ascii_uppercase, k=random.randint(3, 10)))
            for _ in range(size)
        ]

    raise ValueError(f"Unsupported data type: {data_type}")


def sort_once(values):
    """Sort values with the original 1-indexed merge-sort implementation."""

    global a, b

    a = [None] + list(values)
    b = [None] * (len(values) + 1)
    split_positions.clear()
    MergeSort(1, len(values))
    return a[1:]


def measure(values, clock):
    """Return the sort duration measured by the supplied clock function."""

    start = clock()
    sort_once(values)
    return clock() - start


def create_datasets():
    """Create one dataset per data type and size before timing begins."""

    return {
        data_type: {
            size: generate_data(data_type, size)
            for size in SIZES
        }
        for data_type in DATA_TYPES
    }


def benchmark(datasets, clock):
    """Measure every data type and size using one independent sort run."""

    return {
        data_type: {
            size: measure(datasets[data_type][size], clock)
            for size in SIZES
        }
        for data_type in DATA_TYPES
    }


def print_table(title, results):
    print(f"{title}:")
    print("DataType | " + " | ".join(f"n={size}" for size in SIZES))

    for data_type in DATA_TYPES:
        values = " | ".join(f"{results[data_type][size]:.6f}" for size in SIZES)
        print(f"{data_type:<8} | {values}")

    print()


def main():
    datasets = create_datasets()

    method_1_results = benchmark(datasets, time.time)
    method_2_results = benchmark(datasets, time.perf_counter)

    print_table("Method 1", method_1_results)
    print_table("Method 2", method_2_results)


if __name__ == "__main__":
    main()
