# kosaraju's algorithm

v = 8
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 7), (4, 5), (5, 6), (6, 4), (4, 7), (6, 7)]

adj = [ []  for _ in range (v)]

for i , j in edges:
    adj[i].append(j)

visited=[0]*v
stack=[]

# step 1
def sort(node):
    
   visited[node]=1

   for i in adj[node]:
        
      if not visited[i]:
         sort(i)
   stack.append(node)

for i in range(v):
   if not visited[i]:
      sort(i)

stack.reverse()

visited=[0]*v

# step 2

rev_adj=[[] for _ in range(v)]

for i , j in edges:
   rev_adj[j].append(i)

def dfs(node):
    
   visited[node]=1

   print(node)

   for i in rev_adj[node]:
        
      if not visited[i]:
         dfs(i)

# step 3
count=0
for i in stack:
   if not visited[i]:
      dfs(i)
      print("--------")
      count+=1

print("Strongly connected components :" , count)


    
    