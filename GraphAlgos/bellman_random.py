import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import tkinter as tk
from tkinter import messagebox

def create_barabasi_albert_weighted_graph(num_nodes, num_edges_per_node, weight_range=(-10, 10)):
    G = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)
    for (u, v) in G.edges():
        weight = random.randint(*weight_range)
        G[u][v]['weight'] = weight
    return G

def bellman_ford(G, v, start, end):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}

    dist = [float('inf')] * v
    dist[start] = 0

    prev = [None] * v

    colors = [plt.cm.rainbow(i / float(v - 1)) for i in range(v - 1)]  # Generate random colors

    for n in range(v - 1):
        node_colors = colors[n]
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
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, edge_colors, path_edges in bellman_ford(graph, v, start, end):
        if stop_animation:
            break

        ax.clear()

        for u, v in path_edges:
            edge_colors[(u, v)] = 'red'
            edge_colors[(v, u)] = 'red'

        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=700,
            font_size=14,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )

        edge_labels = {(u, v): f"{graph.edges[u, v]['weight']}" for u, v in graph.edges()}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='blue'
        )
        plt.title(f"Bellman-Ford Algorithm Visualization\nFrom Node {start} to Node {end}", fontsize=18)
        plt.draw()
        plt.pause(0.1)  # Pause to visually show the traversal process

    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

def main():
    parser = argparse.ArgumentParser(description="Bellman-Ford Algorithm Visualization")
    parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
    parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
    parser.add_argument('--start', type=int, help='Start vertex')
    parser.add_argument('--end', type=int, help='End vertex')
    args = parser.parse_args()

    # Check if arguments are provided
    if args.vertices is not None and args.edges is not None and args.start is not None and args.end is not None:
        v = args.vertices
        m = args.edges
        s = args.start
        e = args.end
    else:
        v = 5  # Number of nodes
        m = 2  # Number of edges per node
        s = 0   # Start vertex
        e = 2   # End vertex

    # Check for input errors
    if v <= 0:
        show_error("The number of vertices must be a positive integer.")
    elif m < 1 or m >= v:
        show_error("The number of edges per node must be at least 1 and less than the number of vertices.")
    elif s < 0 or s >= v or e < 0 or e >= v:
        show_error("Start and end vertices must be valid node indices within the graph.")
    else:
        # Create a random weighted graph using Barabási-Albert model
        G = create_barabasi_albert_weighted_graph(v, m)

        # Visualize Bellman-Ford algorithm on the random graph
        try:
            visualize_bellman(G, v, s, e)
        except ValueError as e:
            show_error(str(e))

if __name__ == "__main__":
    main()
