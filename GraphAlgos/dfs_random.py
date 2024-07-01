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

def create_random_graph( v, m):
 
    return nx.barabasi_albert_graph(v, m)
    

def dfs(graph, node, visited):
    visited.add(node)
    yield visited, node  # Yield visited set and current node
    
    for i in graph.neighbors(node):
        if i not in visited:
            yield from dfs(graph, i, visited)  # Recursive call with updated visited set

def visualize_dfs(graph, start):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    visited = set()
    for visited_nodes, current_node in dfs(graph, start, visited):
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
        plt.pause(1.7)

    plt.show()
# Parameters for random graph

parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

    # Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges

else:
 v = 12
 m= 2  # Change parameters as needed

if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges must be at least 1 and less than the number of vertices.")
else:
    # Create random graph
    G = create_random_graph(v, m)

    # Visualize DFS on random graph
    try:
        visualize_dfs(G, 0)
    except ValueError as e:
        show_error(str(e))