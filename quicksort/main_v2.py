"""Quick sort benchmark using two elapsed-time measurement methods."""

import random
import string
import time


# Global array

a = []

# The original implementation displays each partition.  Benchmarking
# disables that output so the measured time represents sorting operations.
SHOW_PROCESS = False


def Interchange(a, i, j):
    # Exchange a[i] with a[j]
    p = a[i]
    a[i] = a[j]
    a[j] = p


def display_array(a, p, q, pivot_index=None, left=None, right=None):

    for i in range(1, len(a) - 1):

        # Opening bracket
        if i == p:
            print("[", end=" ")

        # Pivot in bold
        if i == pivot_index:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")
        else:
            print(a[i], end=" ")

        # Closing bracket
        if i == q:
            print("]", end=" ")

        # Space between elements
        elif i < len(a) - 2:
            print(end=" ")

    print()


def display_split(a, p, j, q):

    for i in range(1, len(a) - 1):

        # Left subarray
        if i == p:
            print("[", end=" ")

        print(a[i], end=" ")

        if i == j - 1:
            print("]", end=" ")

        # Pivot
        if i == j:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")

        # Right subarray
        if i == j + 1:
            print("[", end=" ")

        if i == q:
            print("]", end=" ")

        if i < len(a) - 2:
            print(end=" ")

    print()


def Partition(a, m, p):

    v = a[m]
    i = m
    j = p

    # Display current subarray with pivot
    if SHOW_PROCESS:
        print()
        display_array(a, m, p - 1, m)

    while True:

        # repeat
        i = i + 1

        while a[i] < v:
            i = i + 1

        # repeat
        j = j - 1

        while a[j] > v:
            j = j - 1

        # if (i < j)
        if i < j:
            Interchange(a, i, j)

        # until (i >= j)
        if i >= j:
            break

    a[m] = a[j]
    a[j] = v

    # Display the two partitions
    if SHOW_PROCESS:
        display_split(a, m, j, p - 1)

    return j


def QuickSort(a, p, q):

    # If there is more than one element
    if p < q:

        # Divide P into two subproblems
        j = Partition(a, p, q + 1)

        # Solve left subproblem
        QuickSort(a, p, j - 1)

        # Solve right subproblem
        QuickSort(a, j + 1, q)


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


def sentinel_for(data_type):
    """Return a value greater than every generated value of this type."""

    if data_type in ("Integer", "Float"):
        return float("inf")

    return "\U0010ffff"


def sort_once(values, sentinel):
    """Sort values with the original 1-indexed quick-sort implementation."""

    global a

    a = [None] + list(values) + [sentinel]
    QuickSort(a, 1, len(values))
    return a[1:len(values) + 1]


def measure(values, sentinel, clock):
    """Return the sort duration measured by the supplied clock function."""

    start = clock()
    sort_once(values, sentinel)
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
            size: measure(
                datasets[data_type][size],
                sentinel_for(data_type),
                clock,
            )
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
