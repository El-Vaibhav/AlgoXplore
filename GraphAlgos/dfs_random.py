import networkx as nx
import matplotlib.pyplot as plt
import argparse
import tkinter as tk
from tkinter import messagebox

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

def create_random_graph(v, m):
    return nx.barabasi_albert_graph(v, m)

def dfs(graph, node, visited, depth):
    visited.add(node)
    yield visited, node, depth, ""  # Yield visited set, current node, current depth, and status (empty for normal traversal)
    
    for i in graph.neighbors(node):
        if i not in visited:
            yield from dfs(graph, i, visited, depth + 1)  # Recursive call with increased depth
            if len(visited) == len(graph.nodes):
                return
            yield visited, node, depth, "backtracking"  # Yield backtracking status

def visualize_dfs(graph, start):
    pos = nx.spring_layout(graph)
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))

    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0")  # Set the position to (0,0) which is the top-left of the screen
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    visited = set()
    for visited_nodes, current_node, depth, status in dfs(graph, start, visited, 0):
        if stop_animation:
            break

        ax.clear()
        if status == "backtracking":
            node_colors = ['magenta' if n == current_node else ('yellow' if n in visited_nodes else 'skyblue') for n in graph.nodes()]
        else:
            node_colors = ['yellow' if n in visited_nodes else 'skyblue' for n in graph.nodes()]
        
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',  
            width=2,
            ax=ax
        )

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'yellow', label='Current Node') , plt.Rectangle((0, 0), 1, 1, color= 'magenta', label='Backtracking')]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=10,bbox_to_anchor=(1.05, 1))
        
        plt.draw()
        if status == "backtracking":
            plt.title(f"DFS Algorithm Visualization\n\nCurrent Node: {current_node}         Current Depth: {depth} - Backtracking", fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        else:
            plt.title(f"DFS Algorithm Visualization\n\nCurrent Node: {current_node}         Current Depth: {depth}", fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.7)


    if not stop_animation:
        plt.pause(1.7)
        ax.clear()
        # The ax.clear() function is used to clear the current axes (ax) before re-drawing the plot.
        # By clearing the axes, you can ensure that the plot is refreshed with only the new drawing elements. 
        node_colors = ['red' for _ in graph.nodes()]
        nx.draw(
            graph, pos, 
            with_labels = True,
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',         
            width=2,
            ax=ax
        )
        plt.title("DFS Algorithm Visualization - All Nodes Visited",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.7)
    
    
    plt.show()
    

# Parameters for random graph
parser = argparse.ArgumentParser(description="DFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

# Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
    v = 8
    m = 2  # Default parameters if not provided

if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges must be at least 1 and less than the number of vertices.")
else:
    # Create random graph
    G = create_random_graph(v, m)

    # Visualize DFS on random graph
    visualize_dfs(G, 0)
