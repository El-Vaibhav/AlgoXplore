from queue import Queue

V = 5

l = [[1,2,3],[],[4],[],[]]

visited = [0]*V

s = 0

q = Queue()

c=0

q.put((s,c))
visited[s] = 1

while q.qsize()>0 :

    node ,c = q.get()

    print(node, "level:", c)

    for i in l[node]:

        if not visited[i]:
            q.put((i,c+1))
            visited[i] = 1
