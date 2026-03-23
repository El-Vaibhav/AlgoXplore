# kahns is topo sort using bfs indegree is used here
# kahns will give correct ans only in DAG
from queue import Queue
v=8

adj=[ [3],[0,7],[0,1],[1],[],[2,4],[],[]]
in_deg = [0]*v


for i in range(v):

    for j in adj[i]:
       in_deg[j]+=1

q=Queue()

visited=[0]*v

for i in range(v):

    if in_deg[i]==0:
        q.put(i)
        visited[i]=1

while q.qsize()>0:

    node = q.get()

    print(node,end=" ")

    for i in adj[node]:
        in_deg[i]-=1

        if in_deg[i]==0 and not visited[i]:
            q.put(i)
            visited[i]=1





