import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import subprocess
import sys

# Function to execute different graph algorithms
def execute_graph_algorithm(script_path, vertices=None, edges=None, start=None, end=None):
    args = [sys.executable, script_path]
    if vertices is not None and edges is not None:
        args += ["--vertices", str(vertices), "--edges", str(edges)]
    if start is not None:
        args += ["--start", str(start)]
    if end is not None:
        args += ["--end", str(end)]
    
    subprocess.Popen(args)

# Function to open the input dialog
def open_input_dialog(script_path, algorithm_name):
    def submit():
        nonlocal vertices_entry, edges_entry, start_entry, end_entry
        try:
            vertices = int(vertices_entry.get())
            edges = int(edges_entry.get())
            start = int(start_entry.get()) if start_entry else None
            end = int(end_entry.get()) if end_entry else None
            dialog.destroy()
            execute_graph_algorithm(script_path, vertices=vertices, edges=edges, start=start, end=end)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for vertices, edges, start node, and end node.")
    
    dialog = tk.Toplevel(root)
    dialog.title("Input Options")
    dialog.geometry("470x470+220+100")  # Set position to open the dialog on the right side
    
    if script_path.endswith("dijkstra_random.py") or script_path.endswith("bellman_random.py"):
        dialog.geometry("600x600")  # Larger size for Dijkstra's and Bellman-Ford
        dialog.configure(bg="brown")  # Set the background color to brown

        # Configure the font
        font_style = ("Helvetica", 14, "bold")

        tk.Label(dialog, text="Enter number of vertices and edges per vertex:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=20)
        
        tk.Label(dialog, text="Vertices:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        vertices_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        vertices_entry.pack(anchor=tk.W, padx=20, pady=5)
        
        tk.Label(dialog, text="Edges per vertex:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        edges_entry.pack(anchor=tk.W, padx=20, pady=5)

        tk.Label(dialog, text="Enter the start node and end node:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=40)
        
        tk.Label(dialog, text="Start node:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        start_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        start_entry.pack(anchor=tk.W, padx=20, pady=5)

        tk.Label(dialog, text="End node:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        end_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        end_entry.pack(anchor=tk.W, padx=20, pady=5)
    else:
        dialog.configure(bg="brown")  # Set the background color to brown

        # Configure the font
        font_style = ("Helvetica", 14, "bold")

        tk.Label(dialog, text="Enter number of vertices and edges per vertex:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=50)
        
        tk.Label(dialog, text="Vertices:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        vertices_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        vertices_entry.pack(anchor=tk.W, padx=20, pady=15)
        
        tk.Label(dialog, text="Edges per vertex:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        edges_entry.pack(anchor=tk.W, padx=20, pady=15)

        start_entry = None
        end_entry = None
    
    submit_button = tk.Button(dialog, text="Submit", command=submit, bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=20)

    # Display algorithm explanation
    display_algorithm_explanation(algorithm_name)

# Function to display algorithm explanation
def display_algorithm_explanation(algorithm_name):
    # Mapping from algorithm name to explanation
    explanations = {
        "DFS": "Depth First Search (DFS) is a graph traversal algorithm that starts at the root node and explores as far as possible along each branch before backtracking.",
        "BFS": "Breadth First Search (BFS) is a graph traversal algorithm that starts at the root node and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.",
        "Topo Sort": "Topological Sorting of a directed acyclic graph (DAG) is a linear ordering of its vertices such that for every directed edge uv from vertex u to vertex v, u comes before v in the ordering.",
        "Dijkstra": "Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a graph, which may represent, for example, road networks.",
        "Bellman Ford": "The Bellman-Ford algorithm is an algorithm that computes shortest paths from a single source vertex to all of the other vertices in a weighted digraph.",
        "Prims": "Prim's algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph. This means it finds a subset of the edges that forms a tree that includes every vertex.",
        "Kruskals": "Kruskal's algorithm is an algorithm in graph theory that finds a minimum spanning tree for a connected weighted graph. This means it finds a subset of the edges that forms a tree that includes every vertex.",
        "Kosaraju": "Kosaraju's algorithm is used to find the strongly connected components (SCCs) of a directed graph. It does so in linear time."
    }

    explanation = explanations.get(algorithm_name, "No explanation available for this algorithm.")
    explanation_dialog = tk.Toplevel(root)
    explanation_dialog.title(f"{algorithm_name} Explanation")
    explanation_dialog.geometry("440x440+850+100")  # Set position to open the dialog on the far right side
    explanation_dialog.configure(bg="red")  # Set the background color to black
    explanation_dialog.resizable(False, False)  # Disable maximizing
    font_style=("Helvetica", 15,"bold")
    explanation_label = tk.Label(explanation_dialog, text=explanation, font=font_style, fg="white", bg="red", wraplength=400, justify=tk.LEFT)
    explanation_label.pack(padx=20, pady=20)
# Create the root window
root = tk.Tk()
root.configure(bg="black")

# Load the image
image_path = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\img3.jpg"
image = Image.open(image_path)
image_width, image_height = image.size

# Text label at the top
title_label = tk.Label(root, text="Choose any algorithm you want to visualize", font=("Tahoma", 18, "bold"), fg="white", bg="black")
title_label.pack(side=tk.TOP, pady=30)  # Center the title at the top

# Create a frame for the image with a border
frame_image = tk.Frame(root, bd=3, relief=tk.SUNKEN)
frame_image.pack(side=tk.LEFT, padx=10, pady=70)

# Create a photoimage object of the image
image_tk = ImageTk.PhotoImage(image)

# Create a label widget to display the image within the frame
label_image = tk.Label(frame_image, image=image_tk)
label_image.pack()


frame_buttons = tk.Frame(root, bg="black")
frame_buttons.pack(side=tk.RIGHT, padx=37, pady=72, anchor=tk.NE)


# Button labels and colors
button_specs = [
    ("DFS", "yellow", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dfs_random.py"),
    ("BFS", "red", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bfs_random.py"),
    ("Topo Sort", "lightgreen", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\topo_sort_random.py"),
    ("Dijkstra", "cyan", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dijkstra_random.py"),
    ("Bellman Ford", "lightblue", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bellman_random.py"),
    ("Prims", "brown", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\prims_random.py"),
    ("Kruskals", "grey", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kruskals_random.py"),
    ("Kosaraju", "white", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kosaraju_random.py")
]

# Function to create buttons dynamically
def create_buttons():
    for i, (text, color, script_path) in enumerate(button_specs):
        row = i // 2
        col = i % 2
        button = tk.Button(frame_buttons, text=text, width=15, height=2, command=lambda p=script_path, name=text: open_input_dialog(p, name),
                           font=("Helvetica", 14, "bold"), bg=color, fg="black")
        button.grid(row=row, column=col, padx=37, pady=34)

# Call the function to create buttons
create_buttons()

# Create the root window
root.mainloop()

