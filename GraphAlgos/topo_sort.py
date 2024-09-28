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

# Topological sort function using Kahn's algorithm with cycle detection
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
        node_colors[node_list.index(node)] = 'yellow'
        
        for neighbor in graph.neighbors(node):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0 and neighbor not in visited:
                q.put(neighbor)

    if len(traversal) != len(graph.nodes()):
        # If the number of nodes processed is less than the total number of nodes, there is a cycle
        return None, "Graph is cyclic. Topological sort is not possible."

    # Coloring nodes according to traversal order
    for i in traversal:
        node_colors[node_list.index(i)] = 'yellow'
    
    return node_colors, traversal

# Function to visualize topological sort
def visualize_toposort(graph):
    pos = nx.spring_layout(graph, k=13.5, scale=2, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0") 
    
    def on_close(event):
        plt.close(fig)

    fig.canvas.mpl_connect('close_event', on_close)
    
    node_colors, traversal_or_message = kahns_topological_sort(graph)
    
    if node_colors is None:
        # Handle cyclic graph case
        ax.clear()
        ax.axis('off')  # Turn off axis
        ax.text(0.5, 0.5, traversal_or_message, fontsize=16, fontname='Times New Roman', fontweight='bold', ha='center', color='red')
        plt.title("Error", fontsize=16, fontname='Times New Roman', fontweight='bold')
        plt.show()
        return
    
    # Visualization for acyclic graph
    stop_animation = False
    for i in range(len(traversal_or_message)):
        if stop_animation:
            break

        ax.clear()

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color='yellow', label='Current Node')]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=12, bbox_to_anchor=(1.05, 1))

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
        plt.title(f"Kahn's Algorithm Visualization\nCurrent Node: {traversal_or_message[i]}", fontsize=16,
                  fontname='Times New Roman',
                  fontweight='bold')
        plt.draw()
        plt.pause(1.5)  # Pause to visually show the traversal process

    plt.title(f"Kahn's Algorithm Visualization\n\nTopo Sort Order: {traversal_or_message}", fontsize=16,
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
