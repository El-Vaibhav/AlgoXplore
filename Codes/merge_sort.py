import math
def merge(l, low, mid, high):
    i = low
    j = mid + 1
    k = low
    temp = [0]*len(l)

    while i <= mid and j <= high:  # tc = o(nlogn)
        if l[i] <= l[j]:
            temp[k] = l[i]
            i += 1
            k += 1
        else:
            temp[k] = l[j]
            j += 1
            k += 1
    while i <= mid:
        temp[k] = l[i]
        i += 1
        k += 1

    while j <= high:
        temp[k] = l[j]
        j += 1
        k += 1

    for i in range(low, high + 1):
        l[i] = temp[i]


def merge_sort(l, low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(l, low, mid)
        merge_sort(l, mid + 1, high)
        merge(l, low, mid, high)


l = [2, 4, 8, 0, 1, 6, -9, 910, -10]

merge_sort(l, 0, len(l) - 1)

print(l)

print(math.gcd(1529,14038))
