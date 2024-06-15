import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse

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

    ans=[]

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
                        yield node_colors , i , edge_colors , ans
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
                yield node_colors, neighbor, edge_colors, ans

    for i in range(len(visited)):
        if visited[i] == 1:
            node_colors[node_list.index(i)] = 'red'
            
    yield node_colors, i, edge_colors, ans

# Function to visualize Dijkstra's algorithm
def visualize_dijkstra(graph,s,e):
    pos = nx.spring_layout(graph)

    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, current_node, edge_colors, path_edges in dijkstra(graph, len(graph.nodes()), s, e):
        
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
            node_size=500,
            font_size=14,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=12,
            font_color='blue'
        )
        plt.draw()
        plt.pause(0.6)  # Pause to visually show the traversal process

# Create a random weighted graph using Barabási-Albert model

parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
parser.add_argument('--start', type=int, help='Start vextex')
parser.add_argument('--end', type=int, help='End vertex')

args = parser.parse_args()

    # Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
    s= args.start
    e= args.end
else:
 v = 9
 m = 2
 s=0
 e=8

G, edges = create_barabasi_albert_weighted_graph(v,m)

# Visualize Dijkstra's algorithm on the random graph
visualize_dijkstra(G,s,e)

# Keep the plot open until the user closes it
plt.show()
