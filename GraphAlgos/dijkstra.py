import networkx as nx
import matplotlib.pyplot as plt
import argparse
import tkinter as tk
from tkinter import messagebox

# Function to create a graph from a list of edges
def create_graph_from_edges(edges):
    G = nx.Graph()
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)
    return G

# Dijkstra's algorithm
def dijkstra(G, num_nodes, start_node, end_node):
    q = set()
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())
    q.add((0, start_node))

    dist = [float('inf')] * num_nodes
    dist[start_node] = 0

    my_dict = {}
    visited = [0] * num_nodes
    visited[start_node] = 1
    visited[end_node] = 1

    ans = []

    while len(q) > 0:
        node = min(q)[1]
        q.remove(min(q))
        # to backtrack and find the nodes in the shortest path
        if node == end_node:
            search = end_node
            while search != start_node:
                for i in my_dict.keys():
                    if i == search:
                        visited[my_dict[i]] = 1
                        ans.append((my_dict[i], search))
                        yield node_colors, i, edge_colors, ans, dist[end_node]
                        search = my_dict[i]
            
        for neighbor in G.neighbors(node):
            weight = G[node][neighbor]['weight']
            if dist[neighbor] == min(dist[neighbor], dist[node] + weight):
                continue
            else:
                if (dist[neighbor], neighbor) in q:
                    q.remove((dist[neighbor], neighbor))
                dist[neighbor] = min(dist[neighbor], dist[node] + weight)
                my_dict[neighbor] = node
                node_colors[node_list.index(neighbor)] = 'yellow'
                q.add((dist[neighbor], neighbor))
                yield node_colors, neighbor, edge_colors, ans, dist[end_node]

    for i in range(len(visited)):
        if visited[i] == 1:
            node_colors[node_list.index(i)] = 'red'
            
    yield node_colors, i, edge_colors, ans, dist[end_node]

# Function to visualize Dijkstra's algorithm
def visualize_dijkstra(graph, s, e):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    initial = True
    path_cost = float('inf')
    path_edges = []

    for node_colors, current_node, edge_colors, edges_in_path, cost in dijkstra(graph, len(graph.nodes()), s, e):
        if stop_animation:
            break

        ax.clear()

        if edges_in_path:
            for edge in edges_in_path:
                edge_colors[edge[0], edge[1]] = 'red'
                edge_colors[edge[1], edge[0]] = 'red'
        
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=400,
            font_size=12,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=10,
            font_color='blue'
        )

        plt.title(f"Dijkstra's Algorithm Visualization\n Node {s} to Node {e}\nExploring Nodes", fontsize=13)

        plt.draw()
        plt.pause(0.8)  # Pause to visually show the traversal process

        path_cost = cost
        path_edges = edges_in_path

    if path_edges:
        ax.clear()
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=400,
            font_size=12,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=10,
            font_color='blue'
        )
        path_nodes = [s] + [edge[1] for edge in path_edges]
        plt.title(f"Dijkstra's Algorithm Visualization\nPath Cost: {path_cost}\nNodes in Path: {path_nodes}", fontsize=14)
        plt.draw()
        plt.pause(2.5)  # Pause to show the final result

    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Dijkstra's Algorithm Visualization")
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
else:
    show_error("All arguments --edges, --start, and --end must be provided.")

# Check for input errors
num_nodes = max(max(edge[0], edge[1]) for edge in edges) + 1  # Determine the number of nodes

if num_nodes <= 0:
    show_error("The number of vertices must be a positive integer.")
elif s < 0 or s >= num_nodes or e < 0 or e >= num_nodes:
    show_error("Start and end vertices must be valid node indices within the graph.")
else:
    # Create a graph from the provided edges
    G = create_graph_from_edges(edges)

    # Visualize Dijkstra's algorithm on the provided graph
    try:
        visualize_dijkstra(G, s, e)
    except ValueError as ex:
        show_error(str(ex))

# Keep the plot open until the user closes it
plt.show()
