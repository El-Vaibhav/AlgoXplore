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

def create_custom_graph(edges):
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G

def dfs(graph, node, visited, depth, stop_animation):
    visited.add(node)
    yield visited, node, depth, ""  # Yield visited set, current node, current depth, and status (empty for normal traversal)
    
    for neighbor in graph.neighbors(node):
        if stop_animation[0]:
            return
        if neighbor not in visited:
            yield from dfs(graph, neighbor, visited, depth + 1, stop_animation)  # Recursive call with increased depth
            if stop_animation[0]:
                return
            if len(visited) == len(graph.nodes):
                return  # Stop further backtracking if all nodes are visited
            yield visited, node, depth, "backtracking"  # Yield backtracking status

def visualize_dfs(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = [False]

    def on_close(event):
        stop_animation[0] = True

    fig.canvas.mpl_connect('close_event', on_close)

    visited = set()
    current_depth = 0

    for node in graph.nodes():
        if node not in visited:
            for visited_nodes, current_node, depth, status in dfs(graph, node, visited, 0, stop_animation):
                if stop_animation[0]:
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
                    linewidths=1,  
                    width=2,
                    ax=ax
                )
                
                plt.draw()
                current_depth = depth
                if status == "backtracking":
                    plt.title(f"DFS Algorithm Visualization\n\nCurrent Node: {current_node}         Current Depth: {current_depth} - Backtracking", weight='bold')
                else:
                    plt.title(f"DFS Algorithm Visualization\n\nCurrent Node: {current_node}         Current Depth: {current_depth}", weight='bold')
                plt.pause(1.7)

            # Check if all nodes are visited
            if len(visited_nodes) == len(graph.nodes()):
                break

    # After all nodes are visited
    if not stop_animation[0]:
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
        plt.title("DFS Algorithm Visualization - All Nodes Visited", fontsize=14.2, weight='bold')
        plt.draw()  # Make sure the final plot is drawn
        plt.pause(1.7)
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="DFS Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1), (1, 2), ...]')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples

        # Create custom graph
        G = create_custom_graph(edges)

        # Visualize DFS on custom graph
        visualize_dfs(G)  # Visualize DFS starting from all nodes to cover disconnected graphs

    except Exception as e:
        show_error(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
