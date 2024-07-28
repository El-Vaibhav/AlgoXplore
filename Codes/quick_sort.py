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
