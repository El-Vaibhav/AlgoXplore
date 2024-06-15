import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

# Given edges of the DAG
v = 6
adj = [[(1, 4), (2, 4)], [(0, 4), (2, 2)], [(0, 4), (1, 2), (3, 3), (4, 1), (5, 6)], [(2, 3), (5, 2)], [(2, 1), (5, 3)], [(2, 6), (3, 2), (4, 3)]]

edges = []

# Function to create DAG
def create_G(adj):
    G = nx.Graph()
    for i in range(len(adj)):
        for j in adj[i]:
            G.add_edge(i, j[0], weight=j[1])
            edges.append((i, j[0], j[1]))
    return G

# Dijkstra's algorithm
def dijkstra():
    strt = 0
    end = 5
    q = set()

    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())

    q.add((0, strt))

    dist = [float('inf')] * v
    dist[strt] = 0

    my_dict = {}
    ans = []

    visited = [0] * v
    visited[strt] = 1
    visited[end] = 1

    while len(q) > 0:
        node = min(q)[1]
        q.remove(min(q))

        if node == end:
            search = end
            while search != strt:
                for i in my_dict.keys():
                    if i == search:
                        ans.append((my_dict[i], search))
                        yield node_colors , i , edge_colors , ans
                        visited[my_dict[i]] = 1
                        search = my_dict[i]

        for i in adj[node]:
            if dist[i[0]] == min(dist[i[0]], dist[node] + i[1]):
                continue
            else:
                if (dist[i[0]], i[0]) in q:
                    q.remove((dist[i[0]], i[0]))

                dist[i[0]] = min(dist[i[0]], dist[node] + i[1])
                my_dict[i[0]] = node

                node_colors[node_list.index(i[0])] = 'yellow'
                q.add((dist[i[0]], i[0]))
                yield node_colors, i, edge_colors, []

    for i in range(len(visited)):
        if visited[i] == 1:
            node_colors[node_list.index(i)] = 'red'

    yield node_colors, i, edge_colors, ans

# Function to visualize Dijkstra's algorithm
def visualize_dijkstra(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    plt.title("Dijkstra's Algorithm", fontsize=20)

    for node_colors, current_node, edge_colors, path_edges in dijkstra():
        plt.clf()

        if path_edges:
            for edge in path_edges:
                edge_colors[edge[0],edge[1]] = 'red'
                edge_colors[edge[1],edge[0]] = 'red'


        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1000,
            font_size=14,
            font_color='black',
            edge_color=[edge_colors[edge] for edge in graph.edges()],
            width=2  # Edge width
        )
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            font_size=17,
            font_color='darkgreen'
        )
        plt.draw()
        plt.pause(0.5)  # Pause to visually show the traversal process

    plt.show()

G = create_G(adj)

visualize_dijkstra(G)
