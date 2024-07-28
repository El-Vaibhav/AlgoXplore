import networkx as nx
import matplotlib.pyplot as plt
import argparse
import tkinter as tk
from tkinter import messagebox
import matplotlib.colors as mcolors

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

def create_custom_graph(edges):
    G = nx.DiGraph()  # Use a directed graph for Bellman-Ford
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    return G

def generate_color_palette():
    """Return a fixed palette of 20 distinct colors."""
    return [
        "yellow", "blue", "green", "purple", "orange", "pink", "cyan", "magenta", 
        "lime", "turquoise", "violet", "gold", "lightblue", "lightgreen", "salmon", 
        "tan", "plum", "coral", "khaki", "lavender"
    ]

def bellman_ford(G, v, start, end):
    edge_colors = {edge: 'purple' for edge in G.edges()}

    dist = [float('inf')] * v
    dist[start] = 0

    prev = [None] * v

    # Generate a list of 20 colors
    colors = generate_color_palette()

    for n in range(v - 1):
        # Assign the same color to all nodes for the current iteration
        node_colors = [colors[n % len(colors)]] * len(G.nodes())
        for i, j in G.edges():
            weight = G.edges[i, j]['weight']
            if dist[i] + weight < dist[j]:
                dist[j] = dist[i] + weight
                prev[j] = i
        yield node_colors, edge_colors, []

    path = []
    u = end
    while prev[u] is not None:
        v = prev[u]
        path.append((v, u))
        u = v
        yield node_colors, edge_colors, path

def visualize_bellman(graph, v, start, end):
    pos = nx.spring_layout(graph)
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for iteration, (node_colors, edge_colors, path_edges) in enumerate(bellman_ford(graph, v, start, end)):
        if stop_animation:
            break

        ax.clear()

        # Highlight edges in the shortest path during iterations
        for u, v in path_edges:
            edge_colors[(u, v)] = 'black'
            edge_colors[(v, u)] = 'black'

        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=12,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )

        edge_labels = {(u, v): f"{graph.edges[u, v]['weight']}" for u, v in graph.edges()}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='darkblue'
        )
        plt.title(f"Iteration {iteration + 1}: Bellman-Ford Algorithm\nFrom Node {start} to Node {end}", fontsize=15,
        fontname='Times New Roman',
        fontweight='bold')
        plt.draw()
        plt.pause(1.0)  # Pause to visually show the traversal process

    # Final path coloring in red
    for u, v in path_edges:
        edge_colors[(u, v)] = 'red'
        edge_colors[(v, u)] = 'red'
    final_node_colors = ['red' if node in {start, end} else node_colors[node] for node in graph.nodes()]

    ax.clear()
    nx.draw(
        graph, pos,
        with_labels=True,
        node_color=final_node_colors,
        node_size=500,
        font_size=12,
        font_color='black',
        edge_color=[edge_colors[edge] for edge in graph.edges()],
        width=2
    )
    edge_labels = {(u, v): f"{graph.edges[u, v]['weight']}" for u, v in graph.edges()}
    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color='darkblue'
    )
    plt.title(f"Final Path: Bellman-Ford Algorithm\nFrom Node {start} to Node {end}",fontsize=15,
        fontname='Times New Roman',
        fontweight='bold')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Bellman-Ford Algorithm Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0,1,2), (1,2,3), ...]')
    parser.add_argument('--start', type=int, required=True, help='Start vertex')
    parser.add_argument('--end', type=int, required=True, help='End vertex')

    args = parser.parse_args()

    # Check if arguments are provided
    if args.edges is not None and args.start is not None and args.end is not None:
        try:
            edges = eval(args.edges)  # Convert string input to a Python list of tuples
            s = args.start
            e = args.end
        except Exception as ex:
            show_error(f"Invalid input: {ex}")
            return

    else:
        show_error("All arguments --edges, --start, and --end must be provided.")
        return

    # Check for input errors
    num_nodes = max(max(edge[0], edge[1]) for edge in edges) + 1  # Determine the number of nodes

    if num_nodes <= 0:
        show_error("The number of vertices must be a positive integer.")
        return
    elif s < 0 or s >= num_nodes or e < 0 or e >= num_nodes:
        show_error("Start and end vertices must be valid node indices within the graph.")
        return
    else:
        # Create a graph from the provided edges
        G = create_custom_graph(edges)

        # Visualize Bellman-Ford algorithm on the provided graph
        try:
            visualize_bellman(G, num_nodes, s, e)
        except ValueError as ex:
            show_error(str(ex))

if __name__ == "__main__":
    main()
