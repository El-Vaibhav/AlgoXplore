import networkx as nx
import matplotlib.pyplot as plt

v = 12
edges = [(0, 1), (1, 2), (1, 6), (2, 3), (2, 4), (6, 7), (6, 8), (4, 5), (7, 9), (9, 10), (10, 11)]

adj = [[] for _ in range(v)]
for i, j in edges:
    adj[i].append(j)
    adj[j].append(i)

def create_graph(edges):
    G = nx.Graph()
    for i, j in edges:
        G.add_edge(i, j)
    return G

def dfs(node, visited):
    visited.add(node)
    yield visited, node  # Yield visited set and current node
    
    for i in adj[node]:
        if i not in visited:
            yield from dfs(i, visited)  # Recursive call with updated visited set

def visualize_dfs(graph, start):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 8))
    
    visited = set()
    for visited_nodes, current_node in dfs(start, visited):
        plt.clf()
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=['yellow' if n in visited_nodes else 'skyblue' for n in graph.nodes()],
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',  
            linewidths=1,  
            width=2  
        )
        
        plt.draw()
        plt.pause(1.0)
    
G = create_graph(edges)

for i in range(v):
    visualize_dfs(G, i)


