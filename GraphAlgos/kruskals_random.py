import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import tkinter as tk
from tkinter import messagebox

# Function to create a random graph with random edge weights
def create_random_graph(v, m):
    G = nx.Graph()

    # Create nodes
    G.add_nodes_from(range(v))

    # Create edges
    for i in range(v):
        # Connect node `i` with `m` random nodes
        for _ in range(m):
            if i == v - 1:  # Ensure last node doesn't exceed index
                break
            rand_node = random.randint(i + 1, v - 1)  # Ensure edge goes forward
            if rand_node not in G[i]:
                weight = random.randint(1, 20)  # Assign random weight to edge
                G.add_edge(i, rand_node, weight=weight)

    return G

# Kruskal's algorithm
def kruskals(G):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())

    # Convert the graph edges to a list of (node1, node2, weight) tuples
    edges = [(u, v, G.edges[u, v]['weight']) for u, v in G.edges()]

    # Sort the edges based on weight
    edges.sort(key=lambda x: x[2])

    def find_ultimate_parent(node):
        if node == parent[node]:
            return node
        return find_ultimate_parent(parent[node])

    def union(i, j):
        up_i = find_ultimate_parent(i)
        up_j = find_ultimate_parent(j)

        if up_i != up_j:
            if rank[up_i] > rank[up_j]:
                parent[up_j] = up_i
            elif rank[up_j] > rank[up_i]:
                parent[up_i] = up_j
            else:
                parent[up_j] = up_i
                rank[up_i] += 1

    mst = []
    total_weight = 0

    for u, v, weight in edges:
        if find_ultimate_parent(u) != find_ultimate_parent(v):
            union(u, v)
            mst.append((u, v))
            total_weight += weight
            yield node_colors, u, edge_colors, mst

    print("MST:", mst)
    print("Total weight:", total_weight)
    yield "red", None, edge_colors, mst

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()
    
# Function to visualize Kruskal's algorithm
def visualize_kruskals(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, current_node, edge_colors, path_edge in kruskals(graph):

        if stop_animation:
            break

        ax.clear()

        if path_edge:
            for u, v in path_edge:
                edge_colors[(u, v)] = "red"
                edge_colors[(v, u)] = "red"

        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            linewidths=1,
            width=2
        )

        edge_labels = {(u, v): f"{graph[u][v]['weight']}" for u, v in graph.edges()}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=9,
            font_color='blue'
        )
        plt.title("Kruskal's Algorithm Visualization")

        plt.draw()
        plt.pause(1.5)

    plt.show()


# Number of nodes in the random graph
parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges_per_vertex', type=int, help='Number of edges per vertex')
args = parser.parse_args()

# Check if arguments are provided
if args.vertices is not None and args.edges_per_vertex is not None:
    v = args.vertices
    m = args.edges_per_vertex
else:
    v = 12
    m = 2  # Default to 2 edges per vertex

if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges per vertex must be at least 1 and less than the number of vertices.")
else:
    # Initialize parent and rank arrays for Union-Find
    parent = [i for i in range(v)]
    rank = [0] * v

    # Create a random graph
    random_graph = create_random_graph(v, m)

    # Visualize Kruskal's algorithm on the random graph
    try:
        visualize_kruskals(random_graph)
    except ValueError as e:
        show_error(str(e))
