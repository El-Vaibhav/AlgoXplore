import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse



def create_random_graph(v, edges_per_node):
    G = nx.DiGraph()
    for i in range(v):
        for _ in range(edges_per_node):
            j = random.randint(0, v-1)  # Randomly select a target node
            G.add_edge(i, j)
    return G

def kosaraju(G):
    global visited
    node_colors = ['skyblue'] * len(G.nodes())
    node_list = list(G.nodes())

    adj = [[] for _ in range(v)]
    for i, j in G.edges():
        adj[i].append(j)

    stack = []
    visited = [0] * v

    def sort(node):
        visited[node] = 1
        for i in adj[node]:
            if not visited[i]:
                sort(i)
        stack.append(node)

    for i in range(v):
        if not visited[i]:
            sort(i)

    stack.reverse()

    visited = [0] * v

    rev_adj = [[] for _ in range(v)]
    for i, j in G.edges():
        rev_adj[j].append(i)
    l = []

    def dfs(node, l):
        visited[node] = 1
        l.append(node)
        for i in rev_adj[node]:
            if not visited[i]:
                dfs(i, l)

    count = 0
    
    colors=[]

    for _ in range(v):
        colors.append('#%06x' % random.randint(0, 0xFFFFFF))

    k = 0

    for i in stack:
        l = []
        if not visited[i]:
            dfs(i, l)
            for m in l:
                node_colors[node_list.index(m)] = colors[k]
                yield node_colors
            count += 1
            k += 1

def visualize_kosaraju(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    
    for node_colors in kosaraju(graph):
        if stop_animation:
            break

        ax.clear()

        plt.clf() 
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='black',
            arrowstyle='-|>',  # Arrow style
            arrowsize=20,  # Arrow size
            width=2  
        )
        plt.title("Original Directed Graph")
        plt.pause(1.5)

    plt.show()

# Creating a random directed graph with 8 nodes and 2 edges per node
parser = argparse.ArgumentParser(description="BFS")
parser.add_argument('--vertices', type=int, help='Number of vertices in the graph')
parser.add_argument('--edges', type=int, help='Number of edges to attach from a new node to existing nodes (m)')
args = parser.parse_args()

    # Check if arguments are provided
if args.vertices is not None and args.edges is not None:
    v = args.vertices
    m = args.edges
else:
 v = 11 # Number of nodes
 m = 2  # Number of edges per node

random_graph = create_random_graph(v, m)
visualize_kosaraju(random_graph)
