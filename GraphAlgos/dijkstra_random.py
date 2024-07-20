import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import tkinter as tk
from tkinter import messagebox

# Function to create a random weighted graph using Barabási-Albert model
def create_barabasi_albert_weighted_graph(num_nodes, num_edges_per_node, weight_range=(1, 10)):
    G = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)
    edges = []
    for (u, v) in G.edges():
        weight = random.randint(*weight_range)
        G[u][v]['weight'] = weight
        edges.append((u, v, weight))
    return G, edges

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
    for node_colors, current_node, edge_colors, path_edges, path_cost in dijkstra(graph, len(graph.nodes()), s, e):
        if stop_animation:
            break

        ax.clear()

        if path_edges:
            for edge in path_edges:
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

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'yellow', label='Current Node')]
        ax.legend(handles=legend_entries, loc='upper left', fontsize=12)
   
        plt.title(
            f"Dijkstra's Algorithm Visualization - Node {s} to Node {e}\n\n 'Exploring Nodes'", 
            fontsize=15,
            fontname='Times New Roman',
            fontweight='bold')

        plt.draw()
        plt.pause(0.8)  # Pause to visually show the traversal process

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
        plt.title(
        f"Dijkstra's Algorithm Visualization\n\nPath Cost: {path_cost}\nNodes in Path: {[s] + [edge[1] for edge in path_edges]}",
        fontsize=15,
        fontname='Times New Roman',
        fontweight='bold'
        )
        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'red', label='Nodes in shortest path')]
        ax.legend(handles=legend_entries, loc='upper left', fontsize=12)

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
    v = 14
    m = 2
    s = 13
    e = 12

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges per node must be at least 1 and less than the number of vertices.")
elif s < 0 or s >= v or e < 0 or e >= v:
    show_error("Start and end vertices must be valid node indices within the graph.")
else:
    # Create a random weighted graph
    G, edges = create_barabasi_albert_weighted_graph(v, m)

    # Visualize Dijkstra's algorithm on the random graph
    try:
        visualize_dijkstra(G, s, e)
    except ValueError as e:
        show_error(str(e))

# Keep the plot open until the user closes it
plt.show()
