# sorting_steps.py (step generator for visualization)
# Each function yields: (arr, highlights, info)
# - arr: current array (mutated in-place)
# - highlights: list of indices to highlight
# - info: short status text

from typing import Generator, List, Tuple
import random

Step = Tuple[List[int], List[int], str]


def bubble_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            yield arr, [j, j + 1], f"Bubble: compare {j} vs {j+1}"
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield arr, [j, j + 1], f"Bubble: swap {j} <-> {j+1}"
        if not swapped:
            break
    yield arr, [], "Bubble: done"


def quick_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    # In-place quick sort using stack + Lomuto partition
    stack = [(0, len(arr) - 1)]

    def partition(lo: int, hi: int):
        pivot_idx = random.randint(lo, hi)
        arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            yield arr, [j, hi, i], f"Quick: j={j} compare pivot@{hi}"
            if arr[j] <= pivot:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield arr, [i, j, hi], f"Quick: swap i={i}, j={j}"
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        yield arr, [i, hi], f"Quick: place pivot -> {i}"
        return i

    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue

        gen = partition(lo, hi)
        pivot_index = None
        while True:
            try:
                step = next(gen)
                yield step
            except StopIteration as e:
                pivot_index = e.value
                break

        if pivot_index is None:
            continue

        left = (lo, pivot_index - 1)
        right = (pivot_index + 1, hi)

        # push larger first (optional optimization)
        if (left[1] - left[0]) > (right[1] - right[0]):
            stack.append(left)
            stack.append(right)
        else:
            stack.append(right)
            stack.append(left)

    yield arr, [], "Quick: done"


def merge_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    # Bottom-up (iterative) merge sort for smooth yielding
    n = len(arr)
    temp = arr[:]
    width = 1

    def merge(left: int, mid: int, right: int):
        i, j, k = left, mid, left
        while i < mid and j < right:
            yield arr, [i, j], f"Merge: compare i={i}, j={j} [{left}:{right}]"
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                j += 1
            k += 1

        while i < mid:
            temp[k] = arr[i]
            yield arr, [i], f"Merge: take left i={i} [{left}:{right}]"
            i += 1
            k += 1

        while j < right:
            temp[k] = arr[j]
            yield arr, [j], f"Merge: take right j={j} [{left}:{right}]"
            j += 1
            k += 1

        for t in range(left, right):
            arr[t] = temp[t]
            yield arr, [t], f"Merge: write t={t} [{left}:{right}]"

    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                for step in merge(left, mid, right):
                    yield step
        width *= 2

    yield arr, [], "Merge: done"


def radix_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    # LSD Radix Sort (base 10), non-negative integers only
    if not arr:
        yield arr, [], "Radix: done"
        return

    max_num = max(arr)
    exp = 1
    n = len(arr)
    output = [0] * n

    while max_num // exp > 0:
        count = [0] * 10

        for i in range(n):
            digit = (arr[i] // exp) % 10
            count[digit] += 1
            yield arr, [i], f"Radix: count digit={digit} (exp={exp})"

        for d in range(1, 10):
            count[d] += count[d - 1]
        yield arr, [], f"Radix: prefix sums (exp={exp})"

        for i in range(n - 1, -1, -1):
            digit = (arr[i] // exp) % 10
            output[count[digit] - 1] = arr[i]
            count[digit] -= 1
            yield arr, [i], f"Radix: place digit={digit} (exp={exp})"

        for i in range(n):
            arr[i] = output[i]
            yield arr, [i], f"Radix: write back (exp={exp})"

        exp *= 10

    yield arr, [], "Radix: done"
