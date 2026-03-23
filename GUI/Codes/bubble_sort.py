l=[2,4,8,0,1,6]

for i in range(0,len(l)):   # tc = O(n^2) , best case O(n)
    for j in range(0,len(l)-1-i):
        if(l[j]>l[j+1]):
            l[j],l[j+1]=l[j+1],l[j]

print("Sorted list is ",l)

