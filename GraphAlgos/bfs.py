import networkx as nx
import matplotlib.pyplot as plt
import argparse
from queue import Queue
import tkinter as tk
from tkinter import messagebox

def create_graph(edges):
    G = nx.Graph()
    for i, j in edges:
        G.add_edge(i, j)
    return G

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
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    level_colors = ['blue', 'brown', 'orange', 'magenta', 'purple', 'red']  # Different colors for different levels
    node_colors = {node: 'yellow' for node in graph.nodes()}
    current_level = -1
    
    unique_levels = set()  # To track unique levels encountered
    check = 1
    for visited, queue, levels, current_node, level in bfs(graph, start):
        if stop_animation:
            check = 0
            break

        unique_levels.add(level)  # Add current level to unique levels

        if level != current_level:
            current_level = level
            for node, lvl in levels.items():
                if lvl >= 0:
                    node_colors[node] = level_colors[lvl % len(level_colors)]

        legend_handles = [plt.Rectangle((1, 1), 1, 1, color='magenta', label='Current node')] 
        ax.legend(handles=legend_handles, loc='upper left',fontsize=12)

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
            linewidths=1,
            width=2,
            ax=ax
        )

        nodes_at_current_level = [node for node, lvl in levels.items() if lvl == current_level]
        ax.set_title(f"BFS Algorithm Visualization - Level {current_level}\n\nCurrent Node: {current_node}\nNodes at this level: {nodes_at_current_level}", fontsize=16,
                     fontname='Times New Roman', fontweight='bold')
        
        legend_entries = [plt.Rectangle((0, 0), 1, 1, color='magenta', label='Current Node')]
        for lvl in sorted(unique_levels):
            legend_entries.append(plt.Rectangle((0, 0), 1, 1, color=level_colors[lvl % len(level_colors)], label=f'Level {lvl}'))

        ax.legend(handles=legend_entries, loc='upper right', fontsize=9,bbox_to_anchor=(1.05, 1))
        
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
            linewidths=1,
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
            linewidths=1,  
            width=2,
            ax=ax
        )
        ax.set_title("BFS Algorithm Visualization - All Nodes Visited", fontsize=16,
                     fontname='Times New Roman', fontweight='bold')
        plt.pause(1.7)

    # Create legend entries
        legend_entries = []
        for lvl in sorted(unique_levels):
           legend_entries.append(plt.Rectangle((0, 0), 1, 1, color=level_colors[lvl % len(level_colors)], label=f'Level {lvl}'))

        plt.legend(handles=legend_entries, loc='upper right', fontsize=12,bbox_to_anchor=(1.05, 1))
    
    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

def main():
    parser = argparse.ArgumentParser(description="BFS Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1), (1, 2), ...]')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples
        if not isinstance(edges, list) or not all(isinstance(edge, tuple) and len(edge) == 2 for edge in edges):
            raise ValueError("Edges must be a list of tuples with exactly two elements each.")

        # Create custom graph
        G = create_graph(edges)

        # Visualize BFS on custom graph
        visualize_bfs(G, 0)  # Start BFS from node 0 (you can change as needed)

    except Exception as e:
        show_error(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
