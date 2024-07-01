import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random
import tkinter as tk
from tkinter import messagebox

def create_graph(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G

def kosaraju(G, V):
    node_colors = ['skyblue'] * (V + 1)
    node_list = list(G.nodes())

    adj = [[] for _ in range(V + 1)]
    for u, v in G.edges():
        adj[u].append(v)

    stack = []
    visited = [0] * (V + 1)

    def sort(node):
        visited[node] = 1
        for i in adj[node]:
            if not visited[i]:
                sort(i)
        stack.append(node)

    for i in range(V + 1):
        if not visited[i]:
            sort(i)

    stack.reverse()

    visited = [0] * (V + 1)

    rev_adj = [[] for _ in range(V + 1)]
    for u, v in G.edges():
        rev_adj[v].append(u)

    def dfs(node, l):
        visited[node] = 1
        l.append(node)
        for i in rev_adj[node]:
            if not visited[i]:
                dfs(i, l)

    count = 0
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(V + 1)]

    k = 0

    for i in stack:
        l = []
        if not visited[i]:
            dfs(i, l)
            for m in l:
                if m in node_list:
                    node_colors[node_list.index(m)] = colors[k]
            yield node_colors
            count += 1
            k += 1

def visualize_kosaraju(graph, V):
    pos = nx.circular_layout(graph)  # Default layout to circular
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors in kosaraju(graph, V):
        if stop_animation:
            break

        ax.clear()
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='black',
            arrowstyle='-|>',  # Arrow style
            arrowsize=20,  # Arrow size
            width=2
        )
        plt.title("Kosaraju's Algorithm Visualization")
        plt.pause(1.5)

    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Kosaraju's Algorithm")
parser.add_argument('--edges', type=str, help='List of edges in the format [(u, v), (u, v), ...]')
args = parser.parse_args()

# Check if arguments are provided
if args.edges is not None:
    edges = eval(args.edges)  # Convert string input to a Python list of tuples
    v = 0
    for i, j in edges:
        v = max(v, i)
        v = max(v, j)

    if not isinstance(edges, list):
        show_error("Edges must be provided as a list of tuples.")
        exit()
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2:
            show_error("Each edge must be a tuple of two elements: (u, v).")
            exit()
else:
    v = 8  # Default number of vertices
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 7), (4, 5), (5, 6), (6, 4), (4, 7), (6, 7)]  # Default edges

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
else:
    # Create the graph from user-provided edges
    G = create_graph(edges)

    # Visualize Kosaraju's algorithm on the created graph
    try:
        visualize_kosaraju(G, v)
    except ValueError as e:
        show_error(str(e))
