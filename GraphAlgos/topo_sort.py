import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

# Given edges of the DAG
edges = [(5, 0), (4, 0), (5, 2), (2, 3), (3, 1), (4, 1)]

# Function to create DAG
def create_dag(edges):
    DAG = nx.DiGraph()
    DAG.add_edges_from(edges)
    return DAG

# Kahn's algorithm for topological sort using BFS
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

# Function to visualize topological sort using Kahn's algorithm
def visualize_kahns_toposort(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    plt.title("Topological Sort of a DAG using Kahn's Algorithm", fontsize=20)

    for node_colors, current_node in kahns_topological_sort(graph):
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
        plt.pause(2)  # Pause to visually show the traversal process

    plt.show()

# Create a DAG
DAG = create_dag(edges)

# Visualize topological sort
visualize_kahns_toposort(DAG)
