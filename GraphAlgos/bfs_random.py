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
    q.put((start, 0))  # Queue will store nodes along with their level
    visited.add(start)
    levels = {start: 0}
    
    for node in graph.nodes():
        if node != start:
            levels[node] = -1  # Initialize all nodes with level -1

    while not q.empty():
        node, level = q.get()
        yield visited, list(q.queue), levels, node, level  # Yield current state along with node and level
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                q.put((neighbor, level + 1))
                visited.add(neighbor)
                levels[neighbor] = level + 1

def visualize_bfs(graph, start):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    level_colors = ['blue', 'cyan', 'orange', 'magenta', 'purple']  # Different colors for different levels
    
    for visited, _, levels, current_node, current_level in bfs(graph, start):
        if stop_animation:
            break

        ax.clear()
        node_colors = [level_colors[levels[node] % len(level_colors)] if node == current_node else 'yellow' for node in graph.nodes()]
        
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='cyan',
            linewidths=1,
            width=2,
            ax=ax
        )
        
        nodes_at_current_level = [node for node, lvl in levels.items() if lvl == current_level]
        plt.title(f"BFS Algorithm Visualization - Level {current_level}\n\nCurrent Node: {current_node}\nNodes at this level: {nodes_at_current_level}" ,fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.draw()
        plt.pause(1.7)
    
    if not stop_animation:
        plt.pause(1.7)
        ax.clear()
        node_colors = ['red' for _ in graph.nodes()]
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',  
            linewidths=1,  
            width=2,
            ax=ax
        )
        plt.title("BFS Algorithm Visualization - All Nodes Visited", fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.7)
    
    plt.show()
    
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
    v = 10
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
