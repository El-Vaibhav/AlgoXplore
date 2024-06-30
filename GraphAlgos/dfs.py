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

def dfs(graph, node, visited):
    visited.add(node)
    yield visited, node  # Yield visited set and current node
    
    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            yield from dfs(graph, neighbor, visited)  # Recursive call with updated visited set

def visualize_dfs(graph, start_node):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    visited = set()
    for visited_nodes, current_node in dfs(graph, start_node, visited):
        if stop_animation:
            break

        ax.clear()
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=['yellow' if n in visited_nodes else 'skyblue' for n in graph.nodes()],
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',  
            linewidths=1,  
            width=2,
            ax=ax
        )
        
        plt.draw()
        plt.title("DFS Algorithm Visualization")
        plt.pause(2.0)

    plt.show()  # Show the plot window after the loop completes

def main():
    parser = argparse.ArgumentParser(description="DFS Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1), (1, 2), ...]')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples

        # Create custom graph
        G = create_custom_graph(edges)

        # Visualize DFS on custom graph
        visualize_dfs(G, 0)  # Start DFS from node 0 (you can change as needed)

    except Exception as e:
        show_error(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
