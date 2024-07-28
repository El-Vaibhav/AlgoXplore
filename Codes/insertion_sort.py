
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









