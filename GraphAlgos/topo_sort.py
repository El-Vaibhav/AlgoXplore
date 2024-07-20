import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import argparse

# Function to create a graph from edges
def create_graph_from_edges(edges):
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G

# Topological sort function using Kahn's algorithm
def kahns_topological_sort(graph):
    in_deg = {node: 0 for node in graph.nodes()}
    for u, v in graph.edges():
        in_deg[v] += 1
    
    q = Queue()
    for node in in_deg:
        if in_deg[node] == 0:
            q.put(node)
    
    visited = set()
    node_colors = ['skyblue'] * len(graph.nodes())
    node_list = list(graph.nodes())
    traversal = []

    while not q.empty():
        node = q.get()
        traversal.append(node)
        visited.add(node)
        # node_colors[node_list.index(node)] = 'yellow'
        # # yield node_colors, node  # Yield current node colors and node
        
        for neighbor in graph.neighbors(node):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0 and neighbor not in visited:
                q.put(neighbor)

    # Coloring nodes according to traversal order
    for i in traversal:
        node_colors[node_list.index(i)] = 'yellow'
        yield node_colors, i,traversal

# Function to visualize topological sort
def visualize_toposort(graph):
    pos = nx.spring_layout(graph)
    stop_animation = False
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    check=1
    for node_colors, current_node,traversal in kahns_topological_sort(graph):
        if stop_animation:
            check=0
            break

        ax.clear()

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color= 'Yellow', label='Current Node')]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=12,bbox_to_anchor=(1.05, 1))


        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=12,
            font_color='black',
            edge_color='purple',
            arrows=True,  # Display directed edges with arrows
            arrowstyle='-|>',  # Arrow style
            arrowsize=10,  # Arrow size
            width=2  # Edge width
        )
        plt.title(f"Kahn's Algorithm Visualization\nCurrent Node: {current_node}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.draw()
        plt.pause(1.5)  # Pause to visually show the traversal process
    
    if check:
        plt.title(f"Kahn's Algorithm Visualization\n\nTopo Sort Order: {traversal}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Topological Sort using Kahn's Algorithm")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1), (1, 2), ...]')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples

        # Create custom graph
        G = create_graph_from_edges(edges)

        # Visualize topological sort on custom graph
        visualize_toposort(G)

    except Exception as e:
        print(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
