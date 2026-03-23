def partition(l, low, high):

    pivot = l[low]  # tc = O(n^2) in worst case , best case = O(nlogn)
    i = low + 1
    j = high

    while True:
        while i <= j and l[i] <= pivot:
            i += 1
        while i <= j and l[j] > pivot:
            j -= 1
        if i <= j:
            l[i], l[j] = l[j], l[i]
        else:
            break

    l[low], l[j] = l[j], l[low] 
    return j

def quicksort(l, low, high):

    if low < high:
        pi = partition(l, low, high)
        quicksort(l, low, pi - 1)
        quicksort(l, pi + 1, high)

l = [2, 4, 8, 0, 1, 6]
low = 0
high = len(l) - 1

quicksort(l, low, high)
print(l)

# Its best algorithm if you want to find what will be the position of any element in the sorted array in least time 
# as when that element becomes pivot its position in the sorted array will be known in very less time

# Faster Average Case: Quick Sort typically has a better average-case time complexity of O(nlogn) compared to Merge Sort's guaranteed O(nlogn). Quick Sort's constant factors are lower, making it faster in practice.

# In-Place Sorting: Quick Sort is an in-place sorting algorithm, meaning it doesn't require additional memory proportional to the input size (only 
# O(logn) extra space for the recursion stack). Merge Sort requires O(n) extra memory for temporary arrays.

# Better Cache Performance: Since Quick Sort works on contiguous subarrays and minimizes jumps in memory access, it tends to have better cache locality and thus often performs better with modern memory architectures.

# Simpler to Implement for Arrays: Quick Sort's in-place partitioning makes it more straightforward to implement for arrays compared to Merge Sort, which requires more work for merging subarrays.

# Tail Recursion Optimization: In practice, Quick Sort can be optimized with tail recursion, reducing the space overhead of recursive function calls.

# Adaptive to Input: Quick Sort adapts to the structure of the input. Though it has a worst-case time complexity of O(n 2), with proper pivot selection (like random or median-of-three), this case is rare, and it performs efficiently on a wide range of inputs.