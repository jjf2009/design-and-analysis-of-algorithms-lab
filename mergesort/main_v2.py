"""Merge sort benchmark using two elapsed-time measurement methods."""

import random
import string
import time


SIZES = (100, 200, 500, 7500, 10000)
DATA_TYPES = ("Integer", "Float", "Alphabet", "String")


def merge_sort(values):
    """Return values sorted using merge sort."""
    if len(values) <= 1:
        return values

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def generate_data(data_type, size):
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


def measure(values, clock):
    start = clock()
    merge_sort(values.copy())
    return clock() - start


def create_datasets():
    return {
        data_type: {
            size: generate_data(data_type, size)
            for size in SIZES
        }
        for data_type in DATA_TYPES
    }


def benchmark(datasets, clock):
    return {
        data_type: {
            size: measure(datasets[data_type][size], clock)
            for size in SIZES
        }
        for data_type in DATA_TYPES
    }


def print_table(title, results):
    print(title)
    print("DataType | " + " | ".join(f"n={size}" for size in SIZES))

    for data_type in DATA_TYPES:
        values = " | ".join(f"{results[data_type][size]:.6f}" for size in SIZES)
        print(f"{data_type:<8} | {values}")

    print()


def main():
    datasets = create_datasets()

    print_table("Method 1", benchmark(datasets, time.time))
    print_table("Method 2", benchmark(datasets, time.perf_counter))


if __name__ == "__main__":
    main()
