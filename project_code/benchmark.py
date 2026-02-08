import random
import timeit

from sorting_algorithms import (
    bubble_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    linear_search,
)

def make_array(n, mode="random"):
    arr = [random.randint(0, 100000) for _ in range(n)]
    if mode == "sorted":
        arr.sort()
    elif mode == "reverse":
        arr.sort(reverse=True)
    return arr

def time_algo(algo, arr, repeat=3, *, is_search=False, target=None):
    if is_search:
        stmt = lambda: algo(arr, target)
    else:
        stmt = lambda: algo(arr.copy())
    return min(timeit.repeat(stmt, number=1, repeat=repeat))

if __name__ == "__main__":
    algos = {
        "Bubble": (bubble_sort, False),
        "Merge": (merge_sort, False),
        "Quick": (quick_sort, False),
        "Radix": (radix_sort, False),
        "Linear": (linear_search, True),
    }

    sizes = [100, 300, 1000, 3000]
    modes = ["random", "sorted", "reverse"]

    for mode in modes:
        print(f"\n=== mode: {mode} ===")
        for n in sizes:
            arr = make_array(n, mode)
            target = -1  # worst-case (not in array)

            print(f"\n n={n}")
            for name, (fn, is_search) in algos.items():
                t = time_algo(fn, arr, is_search=is_search, target=target)
                print(f"  {name:6s}: {t:.6f} sec")
