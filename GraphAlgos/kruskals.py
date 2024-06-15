import networkx as nx
import matplotlib.pyplot as plt
import heapq

v = 9
edges=[[0,1,4],[0,7,8],[1,7,11],[1,2,8],[7,8,8],[7,6,1],[2,8,2],[8,6,6],[2,5,4],[6,5,2],[2,3,7],[3,5,14],[3,4,9],[5,4,10]]

parent=[i for i in range(v)] # initial parent parent[i]=i

rank=[0]*v # initial all ranks are zero

def create_graph(edges):
    G = nx.Graph()
    for i, j ,k in edges:
        G.add_edge(i, j,weight=k)
    return G

adj = [[] for _ in range(v)]
for i, j ,k in edges:
    adj[i].append((j,k))
    adj[j].append((i,k))

def find_ulimate_parent(node):

    if node==parent[node]:
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


def kruskals(G):
   
   node_colors = ['skyblue'] * len(G.nodes())
   edge_colors = {edge: 'purple' for edge in G.edges()}
   node_list = list(G.nodes())

   # sort acc to weights
   for i in range(len(edges)):
    
       for j in range(len(edges)-1-i):

           if edges[j][2]>edges[j+1][2]:

               edges[j],edges[j+1]=edges[j+1],edges[j]

   mst=[]

   sum=0
   for i in edges:

       if find_ulimate_parent(i[0])!=find_ulimate_parent(i[1]):

           union(i[0],i[1])

           sum+=i[2]
           mst.append(i)
           yield node_colors,i[0],edge_colors,mst

   print(mst)
   print("Weight is :" , sum)
   
   yield "red",None,edge_colors,mst

   

    
def visualize_kruskals(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 8))
    
    
    for node_colors, current_node ,edge_color , path_edge in kruskals(graph):

        plt.clf()

        if path_edge:

            for i in path_edge:
                    edge_color[(i[0],i[1])]="red"
                    edge_color[(i[1],i[0])]="red"
            

        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color=[edge_color[edge] for edge in graph.edges()],
            linewidths=1,  
            width=2  
        )
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='blue'
            
        )
        
        plt.draw()
        plt.pause(1.5)
    
    plt.show()

G = create_graph(edges)

# kruskals(G)

visualize_kruskals(G)



