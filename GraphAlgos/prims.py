import networkx as nx
import matplotlib.pyplot as plt
import heapq

v = 9
edges=[[0,1,4],[0,7,8],[1,7,11],[1,2,8],[7,8,8],[7,6,1],[2,8,2],[8,6,6],[2,5,4],[6,5,2],[2,3,7],[3,5,14],[3,4,9],[5,4,10]]

adj = [[] for _ in range(v)]
for i, j ,k in edges:
    adj[i].append((j,k))
    adj[j].append((i,k))

def create_graph(edges):
    G = nx.Graph()
    for i, j ,k in edges:
        G.add_edge(i, j,weight=k)
    return G

def prims(G):
   
   node_colors = ['skyblue'] * len(G.nodes())
   edge_colors = {edge: 'purple' for edge in G.edges()}
   node_list = list(G.nodes())
   q=[]

   heapq.heappush(q,(0,0,-1)) # wt , node , parent

   visited=[0]*v

   mst=[]

   ans=0

   l=[]
   while q and len(mst)!=v-1:

       wt,node,parent=heapq.heappop(q)

    # print(wt,node,parent)
    
       if parent!=-1 and not visited[node]:
           mst.append((parent,node,wt))

           yield node_colors,parent,edge_colors,mst
           
           ans+=wt


       visited[node]=1

       for neighbour,weight in adj[node]:

           if not visited[neighbour]:

               heapq.heappush(q,(weight,neighbour,node)) # wt , node , parent

   print(mst)
   

   for i in range(v):
       node_colors[i] = 'red'

   yield node_colors, i, edge_colors, []

    
def visualize_prims(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 8))
    
    
    for node_colors, current_node ,edge_color , path_edge in prims(graph):

        plt.clf()

        if path_edge:

            for i,j,k in path_edge:
                if[i,j,k] in edges:
                    edge_color[(i,j)]="red"
                elif[j,i,k] in edges:
                    edge_color[(j,i)]="red"
            

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

# prims(G)

visualize_prims(G)



