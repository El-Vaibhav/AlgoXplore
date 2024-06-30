import networkx as nx
import matplotlib.pyplot as plt
import argparse
from queue import Queue

def create_graph(edges):
    G = nx.Graph()
    for i, j in edges:
        G.add_edge(i, j)
    return G

def bfs(graph, start):
    adj = nx.to_dict_of_lists(graph)
    visited = set()

    q = Queue()
    q.put(start)
    visited.add(start)
    
    while not q.empty():
        node = q.get()

        yield visited, list(q.queue)
        
        for i in adj[node]:
            if i not in visited:
                q.put(i)
                visited.add(i)

def visualize_bfs(graph, start):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    for visited, _ in bfs(graph, start):
        if stop_animation:
            break

        ax.clear()
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=['red' if n in visited else 'purple' for n in graph.nodes()],
            node_size=500,  
            font_size=10,  
            font_color='white',  
            edge_color='cyan',  
            linewidths=1,  
            width=2,
            ax=ax  
        )
        plt.title("BFS Algorithm Visualization")
        plt.draw()
        plt.pause(2.0)

    plt.show()  # Show the plot window after the loop completes

def main():
    parser = argparse.ArgumentParser(description="BFS Visualization")
    parser.add_argument('--edges', type=str, required=True, help='List of edges in the format [(0, 1), (1, 2), ...]')
    args = parser.parse_args()

    try:
        edges = eval(args.edges)  # Convert string input to a Python list of tuples

        # Create custom graph
        G = create_graph(edges)

        # Visualize BFS on custom graph
        visualize_bfs(G, 0)  # Start BFS from node 0 (you can change as needed)

    except Exception as e:
        print(f"Error processing input: {str(e)}")

if __name__ == '__main__':
    main()
