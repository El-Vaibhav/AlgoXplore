import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import tkinter as tk
from tkinter import messagebox

def create_random_graph(v, edges_per_node):
    G = nx.DiGraph()
    for i in range(v):
        for _ in range(edges_per_node):
            j = random.randint(0, v - 1)  # Randomly select a target node
            G.add_edge(i, j)
    return G

def kosaraju(G):
    global visited
    node_colors = ['skyblue'] * len(G.nodes())
    node_list = list(G.nodes())

    adj = [[] for _ in range(len(G))]
    for i, j in G.edges():
        adj[i].append(j)

    stack = []
    visited = [0] * len(G)

    def sort(node):
        visited[node] = 1
        for i in adj[node]:
            if not visited[i]:
                sort(i)
        stack.append(node)

    for i in range(len(G)):
        if not visited[i]:
            sort(i)

    stack.reverse()

    visited = [0] * len(G)

    rev_adj = [[] for _ in range(len(G))]
    for i, j in G.edges():
        rev_adj[j].append(i)
    l = []
    
    def dfs(node, l):

        visited[node] = 1
        l.append(node)
        for i in rev_adj[node]:
            if not visited[i]:
                dfs(i, l)
                
    count = 0
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(G))]

    k = 0

    for i in stack:
        l = []
        if not visited[i]:
            dfs(i, l)
            for m in l:
                node_colors[node_list.index(m)] = colors[k]
                yield node_colors 
            count += 1
            k += 1

    yield count  # Yield the count of connected components at the end

def visualize_kosaraju(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    generator = kosaraju(graph)
    unique_colors = {}
    check=1
    for node_colors in generator:
        if stop_animation:
            check=0
            break

        if isinstance(node_colors, int):
            total_components = node_colors
            continue

        ax.clear()
        for color in node_colors:
            if color !="skyblue" and color not in unique_colors:
                unique_colors[color] = f'Component {len(unique_colors) + 1}'

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color = color, label=label)
                          for color, label in unique_colors.items()]
        ax.legend(handles=legend_entries, loc='upper left', fontsize=11)

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
        plt.title("Kosaraju's Algorithm Visualization",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.5)
    
    if check:
     plt.title(f"Kosaraju's Algorithm Visualization\n\nTotal Number of Connected Components: {total_components}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
     plt.pause(1.5)

     plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Kosaraju's Algorithm")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

# Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
    v = 13  # Default number of nodes
    m = 2  # Default number of edges per node

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges per node must be at least 1 and less than the number of vertices.")
else:
    # Create random graph
    random_graph = create_random_graph(v, m)

    # Visualize Kosaraju's algorithm on random graph
    try:
        visualize_kosaraju(random_graph)
    except ValueError as e:
        show_error(str(e))
