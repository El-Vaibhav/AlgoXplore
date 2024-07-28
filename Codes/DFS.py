from queue import Queue
V=9

l=[[1],[2,3],[1,5,6],[1,4,7],[3,8],[2],[2],[3,8],[4,7]]

visited=[0]*V

ans=[]


def dfs(node):

    visited[node]=1
    ans.append(node)

    for i in l[node]:
       if not visited[i]:
          dfs(i)

node =1
dfs(node)
print(ans)

