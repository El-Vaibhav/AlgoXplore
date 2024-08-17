arr = [2,1,0,3,4,1,1.5]

for i in range(len(arr)):

    m =float('inf')

    for j in range(i+1,len(arr)):
        m = min(m,arr[j])

    for j in range(i+1,len(arr)):

        if arr[j]==m and arr[j]<arr[i]:
            arr[i],arr[j]=arr[j],arr[i]



print(arr)