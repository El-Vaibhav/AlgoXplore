import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse

def create_barabasi_albert_weighted_graph(num_nodes, num_edges_per_node, weight_range=(-10, 10)):
    G = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)
    edges = []
    for (u, v) in G.edges():
        weight = random.randint(*weight_range)
        G[u][v]['weight'] = weight
        edges.append((u, v, weight))
    return G

def bellmann_ford(G, v,s,e):
    # strt = s
    # end = e  # Update the end node index

    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())

    dist = [float('inf')] * v
    dist[s] = 0

    prev = [None] * v

    colors = [plt.cm.rainbow(i / float(v - 1)) for i in range(v - 1)]  # Generate random colors

    # Perform Bellman-Ford algorithm
    for n in range(v - 1):
        node_colors = colors[n]
        for i, j in G.edges():
            k = G.edges[i, j]['weight']
            if dist[i] + k < dist[j]:
                dist[j] = dist[i] + k
                prev[j] = i

            yield node_colors, edge_colors, []

    # Construct the shortest path edges
    path = []
    u = e
    while prev[u] is not None:
        v = prev[u]
        path.append((v, u))
        u = v
        yield node_colors, edge_colors, path

    

def visualize_bellmann(graph, v,s,e):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for node_colors, edge_colors, path_edges in bellmann_ford(graph, v,s,e):
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
        plt.draw()
        plt.pause(0.1)  # Pause to visually show the traversal process

    plt.show()

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
 v = 15  # Number of nodes
 m = 2  # Number of edges per node
 s=0
 e=2

G = create_barabasi_albert_weighted_graph(v, m)
visualize_bellmann(G, v,s,e)
