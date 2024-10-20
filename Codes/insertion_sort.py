
arr = [2,-5,98,56,-10,7]


def insertion(arr):
    for i in range(0,len(arr)):  # tc = O(n^2)
        key = arr[i]
        j=i-1       
        while( j>=0 and arr[j] > key):
            arr[j+1]=arr[j]
            j=j-1

        arr[j+1] = key


insertion(arr)

print(arr)


# Here are the 6 advantages of Insertion Sort over Bubble Sort:

# Faster for Nearly Sorted Data: Insertion Sort works efficiently for lists that are already partially or nearly sorted, with a time complexity approaching 
# O(n) in these cases.

# Fewer Comparisons and Swaps: Insertion Sort generally requires fewer comparisons and swaps than Bubble Sort, especially in the average and best cases.

# Stable Sort: Insertion Sort preserves the relative order of elements with equal values, which is useful when stability is important.

# Adaptive Behavior: Insertion Sort adapts to the level of sorting already present in the input, making it much faster when the list is nearly sorted.

# Efficient for Small Data Sets: Insertion Sort is highly efficient for small datasets, and it is often used as a subroutine in other algorithms like QuickSort or MergeSort.

# Easy to Implement in Online Algorithms: Insertion Sort can process elements as they arrive, making it suitable for online algorithms that sort data incrementally.







