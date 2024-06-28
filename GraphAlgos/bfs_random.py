import argparse
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import tkinter as tk
from tkinter import messagebox

def create_random_graph(v, m):
    return nx.barabasi_albert_graph(v, m)

def bfs(graph, start):
    visited = set()
    q = Queue()
    q.put(start)
    visited.add(start)
    
    while not q.empty():
        node = q.get()
        yield visited, list(q.queue)
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)

def visualize_bfs(graph, start):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    for visited, _ in bfs(graph, start):
        if stop_animation:
            break

        ax.clear()
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=['red' if n in visited else 'purple' for n in graph.nodes()],
            node_size=500,
            font_size=10,
            font_color='white',
            edge_color='cyan',
            linewidths=1,
            width=2,
            ax=ax
        )
        plt.draw()
        plt.title("BFS Algorithm Visualization")
        plt.pause(1.7)
    
    plt.close(fig)

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

# Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
    # Default values if arguments are not provided
    v = 15
    m = 2

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges must be at least 1 and less than the number of vertices.")
else:
    # Create random graph
    G = create_random_graph(v, m)
    
    # Visualize BFS on random graph
    try:
        visualize_bfs(G, 0)
    except ValueError as e:
        show_error(str(e))
