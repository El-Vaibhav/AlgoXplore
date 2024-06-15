import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

v = 9
edges = [(0, 1), (1, 2), (1, 6), (2, 3), (2, 4), (6, 7), (6, 8), (4, 5), (7, 5)]

adj = [[] for _ in range(v)]
for i, j in edges:
    adj[i].append(j)
    adj[j].append(i)

def create_graph(edges):
    G = nx.Graph()
    for i, j in edges:
        G.add_edge(i, j)
    return G

def bfs(start):
    visited = set()

    q = Queue()
    q.put(start)
    visited.add(start)
    
    while not q.empty():
        node = q.get()

        yield visited, list(q.queue)
        
        for i in adj[node]:
            if i not in visited:
                q.put(i)
                visited.add(i)

def visualize_bfs(graph, start):
    pos = nx.spring_layout(graph)  
    screen_width, screen_height = plt.figaspect(0.75)  
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for visited, _ in bfs(start):
        if stop_animation:
            break

        ax.clear()
        plt.clf()
        
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=['red' if n in visited else 'purple' for n in graph.nodes()],
            node_size=500,  
            font_size=10,  
            font_color='white',  
            edge_color='cyan',  
            linewidths=1,  
            width=2  
        )
        
        plt.draw()
        plt.pause(1.7)  
        
    

G = create_graph(edges)
visualize_bfs(G, 0)
