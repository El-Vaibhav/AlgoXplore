v=6

edges=[[0,1,5],[1,2,-2],[1,5,-3],[2,4,3],[3,2,6],[3,4,-2],[],[5,3,1]]


dist = [float('inf')] * v

dist[0]=0

for i in range(v-1):

    for j in edges:

        if len(j)==3:
            u,v,w = j
            dist[v]=min(dist[v],dist[u]+w)

print(dist)

for j in edges:

        if len(j)==3:
            u,v,w = j
            if dist[u]+w < dist[v]  :
                 print("Negative cycle found")
                 break


    
    
    
    