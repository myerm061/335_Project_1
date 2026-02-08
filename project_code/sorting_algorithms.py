# CPSC 355 - Sorting Algorithms
# sorting_algorithms.py

# bubble sort alrotirhm 
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr 
# MergeSortAlgorithm
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr) // 2  
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# LinearSearchAlgorithm - O(n)
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Radix_Sort
def radix_sort(arr): 
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort_radix(arr, exp)
        exp *= 10
    return arr 

def counting_sort_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        digit = (arr[i]//exp) % 10
        count[digit] += 1
        
    for i in range(1, 10):
        count[i] += count[i-1]
    
    i = n-1
    while i >= 0:
        digit = (arr[i] // exp) % 10
        output[count[digit]-1] = arr[i]
        count[digit] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]

# QuickSortAlgorithm
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else: 
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        mid = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + mid + quick_sort(right)


# TestingAlgorithms
if __name__ == "__main__":
    test_arr = [64, 34, 25, 12, 22, 11, 90, 5, 22, 11]
    
    print('Unsorted Array:', test_arr)
    print('Buuble Sort: ', bubble_sort(test_arr.copy()))
    print('Merge Sort: ', merge_sort(test_arr.copy()))
    print('radix Sort: ', radix_sort(test_arr.copy()))
    print('quick Sort: ', quick_sort(test_arr.copy()))
    print('Linear Search for 22: ', linear_search(test_arr, 22))