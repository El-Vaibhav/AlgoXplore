
v=6

parent=[0,1,2,3,4,5] # initial parent parent[i]=i

rank=[0]*v # initial all ranks are zero


def find_ulimate_parent(node):

    if node == parent[node]:
        return node
    
    return find_ulimate_parent(parent[node])


def union(i,j):

    up_i = find_ulimate_parent(i)

    up_j = find_ulimate_parent(j)

    if up_i != up_j:  
        if rank[up_i] > rank[up_j]:
            parent[up_j] = up_i

        elif rank[up_j] > rank[up_i]:
            parent[up_i] = up_j

        else:
            parent[up_j] = up_i
            rank[up_i] += 1 

adj=[(4,3,9),(4,0,4),(3,2,5),(3,1,3),(3,0,1),(0,1,2),(2,1,3),(2,5,8),(1,5,7)]


# sort acc to weights
for i in range(len(adj)):
    
    for j in range(len(adj)-1-i):

        if adj[j][2]>adj[j+1][2]:

            adj[j],adj[j+1]=adj[j+1],adj[j]

mst=[]

sum=0
for i in adj:

    if find_ulimate_parent(i[0])!=find_ulimate_parent(i[1]):

        union(i[0],i[1])

        sum+=i[2]
        mst.append(i)

print(mst)
print("Weight is :" , sum)



            


