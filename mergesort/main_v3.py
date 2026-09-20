import random
import string
import time


def merge_sort(values):
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


def main():
    sizes = [100, 200, 500, 7500, 10000]
    data_types = ["Integer", "Float", "Alphabet", "String"]

    datasets = {}

    for data_type in data_types:
        datasets[data_type] = []

        for size in sizes:
            if data_type == "Integer":
                values = [random.randint(1000, 9999) for _ in range(size)]
            elif data_type == "Float":
                values = [random.uniform(1000, 9999) for _ in range(size)]
            elif data_type == "Alphabet":
                values = [random.choice(string.ascii_uppercase) for _ in range(size)]
            else:
                values = [
                    "".join(random.choices(string.ascii_uppercase, k=random.randint(3, 10)))
                    for _ in range(size)
                ]

            datasets[data_type].append(values)

    for clock_name, clock in [("time", time.time), ("perf", time.perf_counter)]:
        print("\n" + clock_name + " results")

        for data_type in data_types:
            for size, values in zip(sizes, datasets[data_type]):
                start = clock()
                merge_sort(values.copy())
                elapsed = clock() - start
                print(f"{data_type}, n={size}: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
