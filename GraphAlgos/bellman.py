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
        G.add_edge(edge[0], edge[1], weight=edge[2])
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
        for i, j, weight in G.edges(data='weight'):
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

def main():
    parser = argparse.ArgumentParser(description="Bellman-Ford Algorithm Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1, 5), (1, 2, -2), ...]')
    parser.add_argument('--start', type=int, required=True, help='Start vertex')
    parser.add_argument('--end', type=int, required=True, help='End vertex')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples

        # Create custom graph
        G = create_custom_graph(edges)

        # Visualize Bellman-Ford algorithm on custom graph
        visualize_bellman(G, args.vertices, args.start, args.end)

    except Exception as e:
        show_error(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
