import networkx as nx
import matplotlib.pyplot as plt
import time
from queue import Queue
import argparse

# Function to create a random DAG using the Barabási-Albert model
def create_random_dag(v, m):
    G = nx.barabasi_albert_graph(v, m)
    DAG = nx.DiGraph()
    for edge in G.edges():
        if edge[0] < edge[1]:
            DAG.add_edge(edge[0], edge[1])
        else:
            DAG.add_edge(edge[1], edge[0])
    return DAG

# Topological sort function using Depth-First Search (DFS)
def kahns_topological_sort(graph):
    in_deg = {node: 0 for node in graph.nodes()}
    for u, v in graph.edges():
        in_deg[v] += 1
    
    q = Queue()
    for node in in_deg:
        if in_deg[node] == 0:
            q.put(node)
    
    visited = set()
    node_colors = ['skyblue'] * len(graph.nodes())
    node_list = list(graph.nodes())
    traversal = []

    while not q.empty():
        node = q.get()
        traversal.append(node)
        visited.add(node)
        node_colors[node_list.index(node)] = 'yellow'
        yield node_colors, node  # Yield current node colors and node
        
        for neighbor in graph.neighbors(node):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0 and neighbor not in visited:
                q.put(neighbor)

    # Coloring nodes according to traversal order
    for i in traversal:
        node_colors[node_list.index(i)] = 'cyan'
        yield node_colors, i


# Function to visualize topological sort
def visualize_toposort(graph):
    pos = nx.spring_layout(graph)
    stop_animation = False
    fig, ax = plt.subplots(figsize=(8, 8))
    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    for node_colors, current_node in kahns_topological_sort(graph):
        if stop_animation:
            break

        ax.clear()

        plt.clf()
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1000,
            font_size=14,
            font_color='black',
            edge_color='purple',
            arrows=True,  # Display directed edges with arrows
            arrowstyle='-|>',  # Arrow style
            arrowsize=10,  # Arrow size
            width=2  # Edge width
        )
        plt.title(f"Current Node: {current_node}", fontsize=20)
        plt.draw()
        plt.pause(0.5)  # Pause to visually show the traversal process

    plt.close(fig)

# Create a random DAG
parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

    # Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
 v = 10
 m = 1
DAG = create_random_dag(v, m)

# Visualize topological sort
visualize_toposort(DAG)
