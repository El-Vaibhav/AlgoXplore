import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import tkinter as tk
from tkinter import messagebox

# Function to create a random graph with random edge weights
def create_random_graph(v, m):

    G = nx.barabasi_albert_graph(v, m)
    edges = []
    for (u, v) in G.edges():
        weight = random.randint(*(1,15))
        G[u][v]['weight'] = weight
        edges.append((u, v, weight))

    return G

# Kruskal's algorithm
def kruskals(G):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}

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
            yield node_colors, edge_colors, mst, total_weight

    print("MST:", mst)
    print("Total weight:", total_weight)
    yield "red", edge_colors, mst, total_weight

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Function to visualize Kruskal's algorithm
def visualize_kruskals(graph):
    pos = nx.spring_layout(graph)
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0") 
    stop_animation = False
    mst_edges = []
    mst_weight = 0

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    check=1
    for node_colors, edge_colors, path_edge, total_weight in kruskals(graph):

        if stop_animation:
            check=0
            break

        ax.clear()

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'red', label='Edges in MST')]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=12,bbox_to_anchor=(1.05, 1))
        
        if path_edge:
            mst_edges = path_edge  # Update mst_edges to include the latest MST edges
            mst_weight = total_weight  # Update mst_weight with the latest total weight
            for u, v in path_edge:
                edge_colors[(u, v)] = "red"
                edge_colors[(v, u)] = "red"
                plt.title(f"Kruskal's Algorithm Visualization\n\nCurrent Edge: ({u}------{v})",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')

        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            linewidths=1,
            width=3
        )

        edge_labels = {(u, v): f"{graph[u][v]['weight']}" for u, v in graph.edges()}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=11,
            font_color='blue'
        )
        plt.draw()
        plt.pause(1.5)

    # Remove edges that are not in MST
    mst_set = set(mst_edges) | set((v, u) for u, v in mst_edges)
    edges_to_remove = [(u, v) for u, v in graph.edges() if (u, v) not in mst_set and (v, u) not in mst_set]
    graph.remove_edges_from(edges_to_remove)

    # Final visualization without the non-MST edges
    if check:
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
        width=3
     )
     edge_labels = {(u, v): f"{graph[u][v]['weight']}" for u, v in graph.edges()}
     nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=11,
        font_color='blue'
     )

     plt.title(f"Kruskal's Algorithm - MST Total Weight: {mst_weight}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
     
     plt.show()


# Number of nodes in the random graph
parser = argparse.ArgumentParser(description="Kruskal's Algorithm")
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
