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
    visited = set()
    q = Queue()
    q.put((start, 0))  # Queue will store nodes along with their level
    visited.add(start)
    levels = {start: 0}
    
    for node in graph.nodes():
        if node != start:
            levels[node] = -1  # Initialize all nodes with level -1

    while not q.empty():
        node, level = q.get()
        yield visited, list(q.queue), levels, node, level  # Yield current state along with node and level
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                q.put((neighbor, level + 1))
                visited.add(neighbor)
                levels[neighbor] = level + 1

def visualize_bfs(graph, start):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)
    
    level_colors = ['blue', 'cyan', 'orange', 'magenta', 'purple']  # Different colors for different levels
    
    for visited, _, levels, current_node, current_level in bfs(graph, start):
        if stop_animation:
            break

        ax.clear()
        node_colors = [level_colors[levels[node] % len(level_colors)] if node == current_node else 'yellow' for node in graph.nodes()]
        
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='cyan',
            linewidths=1,
            width=2,
            ax=ax
        )
        
        nodes_at_current_level = [node for node, lvl in levels.items() if lvl == current_level]
        plt.title(f"BFS Algorithm Visualization - Level {current_level}\nCurrent Node: {current_node}\nNodes at this level: {nodes_at_current_level}")
        plt.draw()
        plt.pause(1.7)

    if not stop_animation:
        plt.pause(1.7)
        ax.clear()
        node_colors = ['red' for _ in graph.nodes()]
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=500,  
            font_size=10,  
            font_color='black',  
            edge_color='maroon',  
            linewidths=1,  
            width=2,
            ax=ax
        )
        plt.title("BFS Algorithm Visualization - All Nodes Visited", weight='bold')
        plt.pause(1.7)
    
    plt.show()

    
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
