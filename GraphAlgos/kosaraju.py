import networkx as nx
import matplotlib.pyplot as plt

v = 8
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 7), (4, 5), (5, 6), (6, 4), (4, 7), (6, 7)]


def create_graph(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G

adj = [[] for _ in range(v)]
for i, j in edges:
    adj[i].append(j)

stack = []
visited = [0] * v

def kosaraju(G):
    global visited
    node_colors = ['skyblue'] * len(G.nodes())
    edge_colors = {edge: 'purple' for edge in G.edges()}
    node_list = list(G.nodes())
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
    for i, j in edges:
        rev_adj[j].append(i)
    l=[]

    def dfs(node,l):
        # nonlocal l
        visited[node] = 1
        l.append(node)
        for i in rev_adj[node]:
            if not visited[i]:
                dfs(i,l)

    count = 0

    colors=["yellow","red","purple","brown"]

    k=0

    for i in stack:
        l=[]
        if not visited[i]:
            dfs(i,l)
            print("--------")
            print(l,k)
            for  m in l:
                node_colors[node_list.index(m)]=colors[k]
                yield node_colors 
            l=[]

            count += 1
            k+=1
            

    print("Strongly connected components:", count)
    
def visualize_kosaraju(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 8))
    
    for node_colors in kosaraju(graph):
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
            # edge_color=[edge_color[edge] for edge in graph.edges()]
            width=2  
        )
        plt.title("Original Directed Graph")
        plt.pause(1.5)
         # Clear the plot after each iteration to draw the next one

    plt.show()

G = create_graph(edges)
visualize_kosaraju(G)


G = create_graph(edges)

kosaraju(G)
visualize_kosaraju(G)
