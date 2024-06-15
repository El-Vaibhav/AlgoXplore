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
def open_input_dialog(script_path):
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
    dialog.geometry("470x470")  # Default size
    
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

# Paths for each algorithm script
script_paths = [
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dfs_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bfs_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\topo_sort_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dijkstra_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bellman_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\prims_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kruskals_random.py",
    "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kosaraju_random.py"
]

# Button labels and colors
button_specs = [
    ("DFS", "yellow"),
    ("BFS", "red"),
    ("Topo Sort", "lightgreen"),
    ("Dijkstra", "cyan"),
    ("Bellman Ford", "lightblue"),
    ("Prims", "brown"),
    ("Kruskals", "grey"),
    ("Kosaraju", "white")
]

# Create a frame for the buttons
frame_buttons = tk.Frame(root, bg="black")
frame_buttons.pack(side=tk.RIGHT, padx=37, pady=72, anchor=tk.NE)

# Create buttons and place them in a 4x2 grid
for i, (text, color) in enumerate(button_specs):
    row = i // 2
    col = i % 2
    button = tk.Button(frame_buttons, text=text, width=15, height=2, command=lambda p=script_paths[i]: open_input_dialog(p),
                       font=("Helvetica", 14, "bold"), bg=color, fg="black")
    button.grid(row=row, column=col, padx=37, pady=34)

# Start the main loop
root.mainloop()
