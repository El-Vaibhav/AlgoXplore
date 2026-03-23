# priority queue having (dist,node) the one having min distance is taken out

# even normal queue can be used but it takes more time
import heapq

v=6

adj=[[(1,4),(2,4)] ,[(0,4),(2,2)] ,[(0,4),(1,2),(3,3),(4,1),(5,6)] , [(2,3),(5,2)] ,[(2,1),(5,3)] ,[(2,6),(3,2),(4,3)]]

strt=0

q=[]

heapq.heappush(q,(0,strt))  

dist=[float('inf')]*v

dist[strt]=0

while q:

    d,node=heapq.heappop(q)

    for i in adj[node]:

        if dist[i[0]] == min ( dist[i[0]] , d+i[1] ):   
            continue # don't push into pq if min distance there
        else:
          dist[i[0]] = min ( dist[i[0]] , d+i[1] ) 
          heapq.heappush(q,(dist[i[0]],i[0]))
            

print(dist)



