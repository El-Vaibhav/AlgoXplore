import heapq

v=6

edges=[[5,4,9],[5,1,4],[4,1,1],[4,3,5],[4,2,3],[1,2,2],[3,2,3],[3,6,8],[2,6,7]]

adj=[[] for _ in range(v)]

for i,j,k in edges:
    adj[i-1].append((j-1,k))
    adj[j-1].append((i-1,k))


q=[]

heapq.heappush(q,(0,0,-1)) # wt , node , parent

visited=[0]*v

mst=[]

ans=0
while q and len(mst)!=v-1:

    wt,node,parent=heapq.heappop(q)

    # print(wt,node,parent)
    
    if parent!=-1 and not visited[node]:
        mst.append((parent,node)) # child,parent,weight
        ans+=wt

    visited[node]=1

    for neighbour,weight in adj[node]:

        if not visited[neighbour]:

            heapq.heappush(q,(weight,neighbour,node)) # wt , node , parent

print("MST edges" , mst)
print("MST weight" , ans)

            

            

