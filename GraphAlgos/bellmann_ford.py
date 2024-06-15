import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import random


v = 6

edges=[[3,2,6],[5,3,1],[0,1,5],[1,5,-3],[1,2,-2],[3,4,-2],[2,4,3]]

# Function to create DAG
def create_G():
    G = nx.Graph()
    for i,j,k in edges:
        G.add_edge(i,j,weight = k)
    
    return G


def bellmann_ford(G,v):
    strt = 0
    end = 4

    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())

    dist = [float('inf')] * v
    dist[strt] = 0

    prev = [None] * v

    colors=["blue","grey","cyan","yellow","pink"]

    # Perform Bellman-Ford algorithm
    for  n in range(v - 1):
        for i, j, k in edges:
            node_colors[i]=colors[n]
            node_colors[j]=colors[n]
            if dist[i] + k < dist[j]:
                dist[j] = dist[i] + k
                prev[j] = i
                

            yield node_colors,edge_colors,[]
        

    # Construct the shortest path edges
    path = []
    u = end
    while prev[u] is not None:
        v = prev[u]
        path.append((v, u))
        u = v
        
        yield node_colors, edge_colors, path


# Function to visualize Dijkstra's algorithm
def visualize_bellmann(graph,v):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 12))  # Adjust figure size as needed
    plt.title("Bellmann Algorithm", fontsize=20)

    for node_colors,edge_colors,path_edges in bellmann_ford(graph,v):
        plt.clf()

        
        for u,v in path_edges:
            edge_colors[(u,v)] = 'red'
            edge_colors[(v,u)]= 'red'
                
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=700,
            font_size=14,
            font_color='black',
            # edge_color="brown",
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )

        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='blue'
            
        )
        plt.draw()
        plt.pause(0.2)  # Pause to visually show the traversal process

    plt.show()

G = create_G()

visualize_bellmann(G,v)
