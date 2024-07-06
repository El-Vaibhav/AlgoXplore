import networkx as nx
import matplotlib.pyplot as plt
import heapq
import argparse
import tkinter as tk
from tkinter import messagebox

def create_custom_graph(edges):
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    return G

def prims(G, adj, v):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    q = []

    heapq.heappush(q, (0, 0, -1))  # weight, node, parent

    visited = [0] * v
    mst = []
    total_weight = 0

    while q and len(mst) != v - 1:
        wt, node, parent = heapq.heappop(q)

        if parent != -1 and not visited[node]:
            mst.append((parent, node, wt))
            total_weight += wt
            yield node_colors, parent, edge_colors, mst, total_weight

        visited[node] = 1

        for neighbour, weight in adj[node]:
            if not visited[neighbour]:
                heapq.heappush(q, (weight, neighbour, node))  # weight, node, parent

    for i in range(v):
        node_colors[i] = 'red'

    yield node_colors, i, edge_colors, [], total_weight

def visualize_prims(graph, adj, v, edges):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False
    mst_edges = []
    total_weight = 0

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, current_node, edge_color, path_edge, total_weight in prims(graph, adj, v):
        if stop_animation:
            break

        ax.clear()

        if path_edge:
            mst_edges = path_edge  # Update mst_edges to include the latest MST edges
            for i, j, k in path_edge:
                if (i, j) in edge_color:
                    edge_color[(i, j)] = "red"
                elif (j, i) in edge_color:
                    edge_color[(j, i)] = "red"

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

        plt.title("Prim's Algorithm Visualization")
        plt.draw()
        plt.pause(1.5)

    # Remove edges that are not in MST
    mst_set = set((u, v) for u, v, _ in mst_edges) | set((v, u) for u, v, _ in mst_edges)
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
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color='blue'
    )
    plt.title(f"Prim's Algorithm - MST Total Weight: {total_weight}")
    
    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Prim's Algorithm")
parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1, 4), (0, 7, 8), ...]')
args = parser.parse_args()

try:
    # Convert edges string to a Python list of tuples
    edges = eval(args.edges)

    # Create custom graph
    G = create_custom_graph(edges)
    
    v = 0
    for i, j, k in edges:
        v = max(v, i)
        v = max(v, j)

    # `v` is the maximum node index, so we need `v+1` for the adjacency list
    adj = [[] for _ in range(v + 1)]

    for i, j, k in edges:
        adj[i].append((j, k))
        adj[j].append((i, k))

    # Visualize Prim's algorithm on the custom graph
    visualize_prims(G, adj, v + 1, edges)

except Exception as e:
    show_error(f"Error processing input: {str(e)}")
