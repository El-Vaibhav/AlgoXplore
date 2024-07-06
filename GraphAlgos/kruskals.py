import networkx as nx
import matplotlib.pyplot as plt
import argparse
import tkinter as tk
from tkinter import messagebox

# Function to create a graph from user-provided edges
def create_graph_from_edges(edges):
    G = nx.Graph()
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)
    return G

# Kruskal's algorithm implementation
def kruskals(G):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    edges = [(u, v, G.edges[u, v]['weight']) for u, v in G.edges()]

    # Sorting edges based on weight
    edges.sort(key=lambda x: x[2])

    parent = [i for i in range(len(G.nodes()))]
    rank = [0] * len(G.nodes())

    def find_ultimate_parent(node):
        if parent[node] != node:
            parent[node] = find_ultimate_parent(parent[node])
        return parent[node]

    def union(u, v):
        root_u = find_ultimate_parent(u)
        root_v = find_ultimate_parent(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1

    mst = []
    total_weight = 0

    for u, v, weight in edges:
        if find_ultimate_parent(u) != find_ultimate_parent(v):
            union(u, v)
            mst.append((u, v))
            total_weight += weight
            yield node_colors, u, edge_colors, mst, total_weight

    print("Minimum Spanning Tree:", mst)
    print("Total Weight:", total_weight)
    yield "red", None, edge_colors, mst, total_weight

# Function to visualize Kruskal's algorithm
def visualize_kruskals(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False
    mst_edges = []
    mst_weight = 0

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, current_node, edge_colors, path_edge, total_weight in kruskals(graph):
        if stop_animation:
            break

        ax.clear()

        if path_edge:
            mst_edges = path_edge  # Update mst_edges to include the latest MST edges
            mst_weight = total_weight  # Update mst_weight with the latest total weight
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
            font_size=12,
            font_color='blue'
        )
        plt.title("Kruskal's Algorithm Visualization")

        plt.draw()
        plt.pause(1.5)

    # Remove edges that are not in MST
    mst_set = set(mst_edges) | set((v, u) for u, v in mst_edges)
    edges_to_remove = [(u, v) for u, v in graph.edges() if (u, v) not in mst_set and (v, u) not in mst_set]
    graph.remove_edges_from(edges_to_remove)

    # Final visualization without the non-MST edges
    ax.clear()
    nx.draw(
        graph, pos,
        with_labels=True,
        node_color='red',
        node_size=500,
        font_size=10,
        font_color='black',
        edge_color='red',
        linewidths=1,
        width=2
    )
    edge_labels = {(u, v): f"{graph[u][v]['weight']}" for u, v in graph.edges()}
    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color='blue'
    )

    # Annotate the total weight of the MST
    plt.annotate(f"MST Total Weight: {mst_weight}", xy=(0.5, 0.95), xycoords='axes fraction', fontsize=12, ha='center', va='top')

    plt.title("Kruskal's Algorithm - MST Only")
    plt.show()

# Function to show error messages in GUI
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Kruskal's Algorithm")
parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [[u, v, weight], [u, v, weight], ...]')
args = parser.parse_args()

# Process user-provided edges
try:
    edges = eval(args.edges)  # Convert string input to a Python list of tuples
    if not isinstance(edges, list):
        raise ValueError("Edges must be provided as a list of lists/tuples.")
    for edge in edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 3:
            raise ValueError("Each edge must be a list/tuple of three elements: [u, v, weight].")

    # Create the graph from user-provided edges
    G = create_graph_from_edges(edges)

    # Visualize Kruskal's algorithm on the created graph
    visualize_kruskals(G)

except Exception as e:
    show_error(f"Error processing input: {str(e)}")
