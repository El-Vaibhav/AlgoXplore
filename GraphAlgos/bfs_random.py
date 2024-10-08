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
        yield levels, node, level  # Yield current state along with node and level
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                q.put((neighbor, level + 1))
                visited.add(neighbor)
                levels[neighbor] = level + 1

def visualize_bfs(graph, start):
    # The spring layout tends to produce aesthetically pleasing results, where nodes are spaced out in a balanced way, 
    # avoiding overlaps and making the graph easier to interpret.

    # k controls the optimal distance between nodes
    # increasing scale will make the layout larger and nodes more spread out.
    # iterations defines the number of iterations the algorithm will run to stabilize the positions of the nodes.

    pos = nx.spring_layout(graph, k=13.5, scale=5, iterations=100)

    # fig (Figure):
    # Represents the entire window or page where the plot is drawn.
    # It is essentially a container for all the elements of a plot, including axes, labels, titles, etc.

    # ax (Axes):
    # Represents a single plot or graph within the figure.
    # It is where the actual plotting happens, such as drawing lines, bars, or scatter points.
    # A figure can contain multiple axes, allowing for multiple plots in a single figure.

    fig, ax = plt.subplots(figsize=(8, 8))

    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0") 

    stop_animation = False
    
    # on_close(event) is a callback function that gets triggered when the plot window is closed
    def on_close(event):
        nonlocal stop_animation
        stop_animation = True
    
    # This line connects the on_close function to the close_event of the Matplotlib figure canvas.
    # The canvas is part of the figure object and is responsible for drawing the plot to the screen or saving it to a file.
    fig.canvas.mpl_connect('close_event', on_close)
    
    level_colors = ['blue', 'brown', 'orange', 'green', 'purple', 'red',"yellow","grey"]  # Different colors for different levels
    node_colors = {node: 'yellow' for node in graph.nodes()}
    current_level = -1
     
    check = 1
    unique_levels = set()  # To track unique levels encountered
    for levels, current_node, level in bfs(graph, start):

    # Use plt.show() when you want to display a plot and are ready to stop the script until the plot window is closed.
    # Use plt.draw() when you want to update or refresh a plot that is already displayed, without blocking the script execution.

        if stop_animation:
            check = 0
            break

        unique_levels.add(level)  # Add current level to unique levels

        if level != current_level:
            current_level = level
            for node, lvl in levels.items():
                if lvl >= 0:
                    node_colors[node] = level_colors[lvl % len(level_colors)]

        # Temporarily color the current node as magenta
        colors = [node_colors[node] if node != current_node else 'magenta' for node in graph.nodes()]
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='cyan',
            width=2,
            ax=ax
        )

        nodes_at_current_level = [node for node, lvl in levels.items() if lvl == current_level]
        ax.set_title(f"BFS Algorithm Visualization - Level {current_level}\n\nCurrent Node: {current_node}\nNodes at this level: {nodes_at_current_level}", fontsize=16,
                     fontname='Times New Roman', fontweight='bold')
        
        legend_entries = [plt.Rectangle((0, 0), 1, 1, color='magenta', label='Current Node')]
        for lvl in sorted(unique_levels):
            legend_entries.append(plt.Rectangle((0, 0), 1, 1, color=level_colors[lvl % len(level_colors)], label=f'Level {lvl}'))
        
        # bbox_to_anchor parameter defines the bounding box that is used to anchor the legend. 
        # It is a tuple that specifies the position of the legend relative to the axes or figure.
        # A value of 1.05 means the anchor point is positioned 5% beyond the right edge of the axes.
        # A value of 1 means the anchor point is positioned at the top edge of the axes.

        ax.legend(handles=legend_entries, loc='upper right', fontsize=9, bbox_to_anchor=(1.05, 1))
        
        plt.draw()
        plt.pause(1.0)  # Short pause to highlight the current node
        
        # Restore the current node to its original color
        colors = [node_colors[node] for node in graph.nodes()]
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='cyan',
            width=2,
            ax=ax
        )
        ax.set_title(f"BFS Algorithm Visualization - Level {current_level}\n\nCurrent Node: {current_node}\nNodes at this level: {nodes_at_current_level}", fontsize=16,
                     fontname='Times New Roman', fontweight='bold')
        plt.draw()
        plt.pause(0.7)  # Continue with the normal pause duration
    
    if check:
        plt.pause(1.7)
        colors = [node_colors[node] for node in graph.nodes()]
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',   
            width=2,
            ax=ax
        )
        ax.set_title("BFS Algorithm Visualization - All Nodes Visited", fontsize=16,
                     fontname='Times New Roman', fontweight='bold')
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
    v = 23
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
