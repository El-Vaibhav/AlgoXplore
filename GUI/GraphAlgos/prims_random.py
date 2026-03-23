import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import argparse
import tkinter as tk
from tkinter import messagebox

def create_barabasi_albert_weighted_graph(num_nodes, num_edges_per_node, weight_range=(1, 10)):
    G = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)
    edges = []
    for (u, v) in G.edges():
        weight = random.randint(*weight_range)
        G[u][v]['weight'] = weight
        edges.append((u, v, weight))
    return G, edges

def prims(G, adj, v):
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    q = []

    heapq.heappush(q, (0, 0, -1))  # wt, node, parent

    visited = [0] * v
    mst = []
    ans = 0

    while q and len(mst) != v - 1:
        wt, node, parent = heapq.heappop(q)

        if parent != -1 and not visited[node]:
            mst.append((parent, node, wt))
            yield node_colors, edge_colors, mst, ans
            ans += wt

        visited[node] = 1

        for neighbour, weight in adj[node]:
            if not visited[neighbour]:
                heapq.heappush(q, (weight, neighbour, node))  # wt, node, parent

    for i in range(v):
        node_colors[i] = 'red'

    yield node_colors, edge_colors, mst, ans

def visualize_prims(graph, adj, v):
    pos = nx.spring_layout(graph)
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)  
    fig, ax = plt.subplots(figsize=(8, 8))
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0") 
    stop_animation = False
    mst_edges = []
    total_weight = 0

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    check=1
    for node_colors , edge_color, path_edge, ans in prims(graph, adj, v):
        
        if stop_animation:
            check = 0
            break

        ax.clear()

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'red', label='Edges in MST')]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=12,bbox_to_anchor=(1.05, 1))

        if path_edge:
            mst_edges = path_edge  # Update mst_edges to include the latest MST edges
            total_weight = ans  # Update total weight
            for i, j, k in path_edge:
                if (i, j) in edge_color:
                    edge_color[(i, j)] = "red"
                elif (j, i) in edge_color:
                    edge_color[(j, i)] = "red"
                plt.title(f"Prim's Algorithm Visualization\n\nCurrent Edge: ({i}------{j})",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
               
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color=[edge_color[edge] for edge in graph.edges()],
            linewidths=1,
            width=3
        )
        # If you don't include data=True, NetworkX will only return the node pairs (u, v) that define the edges,
        #  and you'll miss out on any additional information (such as weights) stored in the edge attributes.
        # d is this dictionary of attributes, so d['weight'] retrieves the value of the 'weight' key from the dictionary.

        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='blue'
        )   
        plt.draw()
        plt.pause(1.5)

    # Remove edges that are not in MST
    # As we are working with undirected graphs and we query for an edge, we don't know whether it is stored as (i, j) or (j, i). 
    # This is why we need to check for both representations.
    mst_set = set((u, v) for u, v, _ in mst_edges) | set((v, u) for u, v, _ in mst_edges)
    edges_to_remove = [(u, v) for u, v in graph.edges() if (u, v) not in mst_set and (v, u) not in mst_set]
    graph.remove_edges_from(edges_to_remove)

    # Final visualization without the non-MST edges

    if check:
     ax.clear()
     nx.draw(
        graph, pos,
        with_labels=True,
        node_color='red',
        node_size=500,
        font_size=10,
        font_color='black',
        edge_color='red',
        linewidths=1,
        width=3
     )
     edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
     nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color='blue'
     )

     plt.title(f"Prim's Algorithm - MST Total Weight: {total_weight}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
    
     plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Prim's Algorithm")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

# Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
    v = 7
    m = 3

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
elif m < 1 or m >= v:
    show_error("The number of edges per node must be at least 1 and less than the number of vertices.")
else:
    # Create a random graph
    G, edges = create_barabasi_albert_weighted_graph(v, m)

    adj = [[] for _ in range(v)]
    for i, j, k in edges:
        adj[i].append((j, k))
        adj[j].append((i, k))

    # Visualize Prim's algorithm on the random graph
    try:
        visualize_prims(G, adj, v)
    except ValueError as e:
        show_error(str(e))
