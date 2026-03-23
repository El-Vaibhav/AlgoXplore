import tkinter as tk
from tkinter import messagebox,scrolledtext
from PIL import ImageTk, Image
import subprocess
import sys
import os



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


# Function to execute different graph algorithms
def execute_graph_algorithm(script_path, edges, start=None, end=None, vertices=None):

    # Resolve script path again inside PyInstaller temp directory
    script_path = resource_path(script_path)

    args = [sys.executable, script_path, "--edges", str(edges)]

    if vertices:
        args.extend(["--vertices", str(vertices)])

    if start is not None and end is not None:
        args.extend(["--start", str(start), "--end", str(end)])

    subprocess.Popen(args)

# Function to open the initial dialog for choosing graph type
def open_initial_dialog(script_path, algorithm_name):
    initial_dialog = tk.Toplevel(root)
    initial_dialog.title("Choose Graph Type")
    initial_dialog.geometry("400x150+500+300")  # Adjust position as needed
    initial_dialog.configure(bg="brown")  # Set background color

    # Configure font style
    font_style = ("Helvetica", 14, "bold")

    # Function to handle when user selects to input their own graph
    def handle_own_graph():
        initial_dialog.destroy()
        open_input_dialog(script_path, algorithm_name, custom_graph=True)

    # Button for own graph input
    own_graph_button = tk.Button(initial_dialog, text="Enter Your Own Graph", command=handle_own_graph, bg="grey", fg="black", font=font_style)
    own_graph_button.pack(pady=10)

    # Function to handle when user selects to use a random graph
    def handle_random_graph():
        initial_dialog.destroy()
        open_input_dialog(script_path, algorithm_name, custom_graph=False)

    # Button for random graph input
    random_graph_button = tk.Button(initial_dialog, text="Enter Any Random Graph", command=handle_random_graph, bg="grey", fg="black", font=font_style)
    random_graph_button.pack(pady=10)

# Function to open the input dialog
def open_input_dialog(script_path, algorithm_name, custom_graph=False):
    def submit():
        nonlocal vertices_entry, edges_entry, start_entry, end_entry, explanation_dialog
        try:
            if not custom_graph:
                vertices = int(vertices_entry.get())
            if custom_graph:
                edges = eval(edges_entry.get())  # Assuming edges are entered as [(0,1,2), (1,2,3)]
                # edges_entry.get(): get() retrieves the text currently present in the edges_entry widget.
            else:
                edges = int(edges_entry.get())  # Assuming edges are entered as an integer (edges per vertex)

            start = None
            end = None
            if start_entry is not None and end_entry is not None:
                start = int(start_entry.get())
                end = int(end_entry.get())

            display_algorithm_explanation(algorithm_name,dialog)
            
            dialog.destroy()

            explanation_dialog.destroy()

            if custom_graph:
                custom_script_name = f"{algorithm_name.lower().replace(' ', '_')}.py"
                custom_script_path = f"GraphAlgos/{custom_script_name}"
                # custom_script_path = f"C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\{custom_script_name}"
                execute_graph_algorithm(custom_script_path, edges,start,end)
            else:
                execute_graph_algorithm(script_path, edges, start, end,vertices)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for vertices, edges, start, and end nodes.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    dialog = tk.Toplevel(root)
    dialog.title("Input Options")
    dialog.geometry("470x470+220+100")  # Set position to open the dialog

    if script_path.endswith("dijkstra_random.py") or script_path.endswith("bellman_random.py"):
        dialog.geometry("600x600")  # Larger size for Dijkstra's and Bellman-Ford
        dialog.configure(bg="brown")  # Set the background color to brown

        # Configure the font
        font_style = ("Helvetica", 14, "bold")
        
        if custom_graph:
            tk.Label(dialog, text="Enter the edges list:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=50)
            
            tk.Label(dialog, text="Edges (e.g., [(v1,v2,wt)]):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
            edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
            edges_entry.pack(anchor=tk.W, padx=20, pady=15)

            tk.Label(dialog, text="Enter the start node and end node:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=40)

            tk.Label(dialog, text="Start node:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
            start_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
            start_entry.pack(anchor=tk.W, padx=20, pady=5)

            tk.Label(dialog, text="End node:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
            end_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
            end_entry.pack(anchor=tk.W, padx=20, pady=5)


        else:
          tk.Label(dialog, text="Enter number of vertices and edges per vertex:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=20)

          tk.Label(dialog, text="Vertices:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
          vertices_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
          vertices_entry.pack(anchor=tk.W, padx=20, pady=5)

          tk.Label(dialog, text="Edges per vertex", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
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

        if custom_graph:

            tk.Label(dialog, text="Enter the edges list:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=50)

            if script_path.endswith("prims_random.py") or script_path.endswith("kruskals_random.py"):
                tk.Label(dialog, text="Edges (e.g., [(v1,v2,wt)]):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
                edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
                edges_entry.pack(anchor=tk.W, padx=20, pady=15)

            else:
             tk.Label(dialog, text="Edges (e.g., [(v1,v2)]):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
             edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
             edges_entry.pack(anchor=tk.W, padx=20, pady=15)

        else:
            tk.Label(dialog, text="Enter number of vertices and edges per vertex:", fg="yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=50)

            tk.Label(dialog, text="Vertices:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
            vertices_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
            vertices_entry.pack(anchor=tk.W, padx=20, pady=15)

            tk.Label(dialog, text="Edges per vertex :", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
            edges_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
            edges_entry.pack(anchor=tk.W, padx=20, pady=15)

        start_entry = None
        end_entry = None

    submit_button = tk.Button(dialog, text="Submit", command=submit, bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=20)

    # Display algorithm explanation
    
    explanation_dialog =  display_algorithm_explanation(algorithm_name,dialog)

def display_algorithm_code(algorithm_name):
    # Create a new window to display the code
    code_dialog = tk.Toplevel(root)
    code_dialog.title(f"{algorithm_name} Code")
    code_dialog.geometry("600x400")  # Adjust size as needed
    code_dialog.configure(bg="black")

    # Create a scrolled text widget to display the code
    code_text = scrolledtext.ScrolledText(code_dialog, wrap=tk.WORD, font=("Courier", 12,"bold"), bg="white", fg="darkblue")
    code_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    code_paths = {
    "DFS": resource_path("Codes/DFS.py"),
    "BFS": resource_path("Codes/BFS.py"),
    "Topo Sort": resource_path("Codes/kahns.py"),
    "Dijkstra": resource_path("Codes/dijkstra_priori_queue.py"),
    "Bellman Ford": resource_path("Codes/bellmann_ford.py"),
    "Prims": resource_path("Codes/Prims.py"),
    "Kruskals": resource_path("Codes/kruskals.py"),
    "Kosaraju": resource_path("Codes/strongly_connected_comp.py")
    }

    # code_paths = {
    # "DFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\DFS.py",
    # "BFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\BFS.py",
    # "Topo Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\kahns.py",
    # "Dijkstra": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\dijkstra_priori_queue.py",
    # "Bellman Ford": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\bellman_ford.py",
    # "Prims": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\Prims.py",
    # "Kruskals": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\kruskals.py",
    # "Kosaraju": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\strongly_connected_comp.py"
    # }


    # Get the code path for the selected algorithm
    code_path = code_paths.get(algorithm_name)
    if code_path:
        try:
            # Read and display the code
            with open(code_path, 'r') as file:
                code = file.read()
                code_text.insert(tk.END, code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load code for {algorithm_name}: {str(e)}")
def display_algo_tc(algorithm_name):
    import subprocess
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
    import sys


    tc_code_paths = {
    "DFS": resource_path("Time_Complexity/e_plus_v.py"),
    "BFS": resource_path("Time_Complexity/e_plus_v.py"),
    "Topo Sort": resource_path("Time_Complexity/e_plus_v.py"),
    "Dijkstra": resource_path("Time_Complexity/e_log_v.py"),
    "Bellman Ford": resource_path("Time_Complexity/ev.py"),
    "Prims": resource_path("Time_Complexity/e_log_v.py"),
    "Kruskals": resource_path("Time_Complexity/e_log_v.py"),
    "Kosaraju": resource_path("Time_Complexity/e_plus_v.py")
    }


    # # Time complexity script paths
    # tc_code_paths = {
    #     "DFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_plus_v.py",
    #     "BFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_plus_v.py",
    #     "Topo Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_plus_v.py",
    #     "Dijkstra": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_log_v.py",
    #     "Bellman Ford": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\ev.py",
    #     "Prims": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_log_v.py",
    #     "Kruskals": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_log_v.py",
    #     "Kosaraju": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\e_plus_v.py",
    # }

    # Detailed explanations
    complexity_explanations = {
        "DFS": (
            "Depth First Search (DFS) - Time Complexity Analysis:\n"
            "1. DFS visits each vertex exactly once.\n"
            "2. Each edge is considered once during traversal.\n"
            "3. Operations:\n"
            "   - Vertex processing: O(V)\n"
            "   - Edge processing: O(E)\n"
            "4. Total Time Complexity: O(V + E)\n"
            "5. Space Complexity: O(V) for recursion stack or explicit stack.\n"
        ),
        "BFS": (
            "Breadth First Search (BFS) - Time Complexity Analysis:\n"
            "1. Every vertex is enqueued and dequeued exactly once.\n"
            "2. Each edge is checked once when visiting neighbors.\n"
            "3. Operations:\n"
            "   - Queue operations for V vertices: O(V)\n"
            "   - Edge checks for E edges: O(E)\n"
            "4. Total Time Complexity: O(V + E)\n"
            "5. Space Complexity: O(V) for queue and visited list.\n"
        ),
        "Topo Sort": (
            "Topological Sorting - Time Complexity Analysis:\n"
            "1. Uses DFS traversal, similar to DFS complexity.\n"
            "2. Vertex processing: O(V)\n"
            "3. Edge processing: O(E)\n"
            "4. Total Time Complexity: O(V + E)\n"
            "5. Space Complexity: O(V) for recursion stack and result stack.\n"
        ),
        "Dijkstra": (
            "Dijkstra’s Algorithm - Time Complexity Analysis:\n"
            "1. Initialization of distances: O(V)\n"
            "2. Priority Queue (Min Heap):\n"
            "   - Insert/Extract Min: O(log V)\n"
            "   - Performed for each vertex: O(V log V)\n"
            "3. Edge Relaxation:\n"
            "   - Relaxed once per edge: O(E)\n"
            "   - Each relaxation involves heap operation: O(log V)\n"
            "   - Total: O(E log V)\n"
            "4. Total Time Complexity: O((V + E) log V)\n"
            "5. Space Complexity: O(V) for distances, O(V) for heap.\n"
        ),
        "Bellman Ford": (
            "Bellman-Ford Algorithm - Time Complexity Analysis:\n"
            "1. Initialization of distances: O(V)\n"
            "2. Relaxation of all edges (V-1) times:\n"
            "   - Each pass: O(E)\n"
            "   - Total for (V-1) passes: O(VE)\n"
            "3. Optional Negative Cycle Check: O(E)\n"
            "4. Total Time Complexity: O(VE)\n"
            "5. Space Complexity: O(V) for distances.\n"
        ),
        "Prims": (
            "Prim’s Algorithm (Min Heap) - Time Complexity Analysis:\n"
            "1. Initialization: O(V) for keys.\n"
            "2. Min Heap operations:\n"
            "   - Extract Min V times: O(V log V)\n"
            "   - Decrease Key for edges: O(E log V)\n"
            "3. Total Time Complexity: O(E log V)\n"
            "4. Space Complexity: O(V) for key array and heap.\n"
        ),
        "Kruskals": (
            "Kruskal’s Algorithm - Time Complexity Analysis:\n"
            "1. Sorting edges: O(E log E) ≈ O(E log V)\n"
            "2. Union-Find (Disjoint Set):\n"
            "   - Nearly constant time using path compression and union by rank.\n"
            "   - Performed for E edges: O(E α(V)), where α(V) ≈ 1\n"
            "3. Total Time Complexity: O(E log V)\n"
            "4. Space Complexity: O(V) for disjoint set.\n"
        ),
        "Kosaraju": (
            "Kosaraju’s Algorithm - Time Complexity Analysis:\n"
            "1. First DFS traversal: O(V + E)\n"
            "2. Transposing the graph: O(V + E)\n"
            "3. Second DFS traversal: O(V + E)\n"
            "4. Total Time Complexity: O(V + E)\n"
            "5. Space Complexity: O(V) for stack and visited list.\n"
        ),
    }

    code_path = tc_code_paths.get(algorithm_name)
    explanation_text = complexity_explanations.get(algorithm_name, "No explanation available.")

    if code_path:
        try:
            # Open TC graph window to far left
            tc_process = subprocess.Popen([sys.executable, code_path])

            # Open explanation window on right
            explanation_window = tk.Toplevel()
            explanation_window.title(f"{algorithm_name} - Time Complexity Analysis")
            explanation_window.geometry("520x450+900+100")  # Right of TC graph
            explanation_window.configure(bg="black")
            explanation_window.resizable(False, False)

            # Scrollable text widget
            scroll_text = scrolledtext.ScrolledText(explanation_window, wrap=tk.WORD, font=("Courier", 12, "bold"),
                                                    bg="black", fg="white")
            scroll_text.insert(tk.END, explanation_text)
            scroll_text.config(state=tk.DISABLED)
            scroll_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            def close_both():
                explanation_window.destroy()
                try:
                    tc_process.terminate()
                except Exception:
                    pass  # Already closed

            explanation_window.protocol("WM_DELETE_WINDOW", close_both)

            # Close handler
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run TC visualization: {str(e)}")
    else:
        messagebox.showerror("Error", "No TC script found for this algorithm.")



# Function to display algorithm explanation
def display_algorithm_explanation(algorithm_name,dialog):
    # Mapping from algorithm name to explanation
    explanations = {
        "DFS": "Depth First Search (DFS) is a graph traversal algorithm that uses recursion. It goes in one direction till all nodes in that path are over. Then it starts backtracking and visiting the nodes which are left. Uses recursion stack to add elements in one path which is moving. The time complexity is O(V + E), where V is the number of vertices and E is the number of edges in the graph.",
        "BFS": "Breadth First Search (BFS) is a graph traversal algorithm that traverses the graph level by level. It uses a queue and puts the start node in the queue initailly. Then it takes out element one by one from queue prints it, marks it as visited and add its neighbours (next level) into the queue. It Repeats this same step of taking out element from queue, printing it, adding its neighbour until the queue is empty. The time complexity is O(V + E), where V is the number of vertices and E is the number of edges in the graph.",
        "Topo Sort": "Topological Sorting of a directed acyclic graph (DAG) is a linear ordering of its vertices such that for every directed edge uv from vertex u to vertex v, u comes before v in the ordering.",
        "Dijkstra": "Dijkstra's algorithm is used for finding the shortest paths between nodes in a graph. It uses a priority queue to minimize the distance between the two nodes. Initailly the dist(strt node) = 0 and dist(other nodes) = infinite. The algorithm one by one takes out the current node from the priority queue and explores all its neighbours if d[v]<d[u]+w(u,v) then set d[v]=d[u]+w(u,v) where (u,v,w) are (parent,child,weight) respectively. This is repeated until the min heap is empty. Time complexity is O((V+E)logV)",
        "Bellman Ford": "The Bellman-Ford algorithm is an algorithm that computes shortest paths from a single source vertex to all of the other vertices in a weighted digraph.",
        "Prims": "Prim's algorithm is uesd to find MST for undirected graphs. It uses a min heap (priority queue) for minimizing the edge weight of the unvisited nodes. It one by one takes out edges from the priority queue, if not visited add it to the mst, marks the node as visited, then explores all the neighbours of the current node and if they are not visited add them to the min heap, this step is repeated until priority queue is exhausted or len(mst)!=v-1.",
        "Kruskals": "Kruskal's algorithm is used to find a minimum spanning tree for a connected weighted undirected graph. It first sorts the edges in ascending order according to there weights then one by one adds them while checking the graph is not forming a cycle. Stops when number of edges is equal to V-1. Kruskals can work even for disconnected graphs (where a path not exists between every two distinct vertices). It's Time complexity is O(ElogV)",
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

    
    def close_dialogs():
        explanation_dialog.destroy()
        dialog.destroy()

    # Bind the window close event (the "X" button) to close both dialogs
    explanation_dialog.protocol("WM_DELETE_WINDOW", close_dialogs)
    dialog.protocol("WM_DELETE_WINDOW", close_dialogs)

    button_frame = tk.Frame(explanation_dialog,bg="red")
    button_frame.pack(pady=20)

    tc_button = tk.Button(button_frame, text="Time Complexity", command= lambda: display_algo_tc(algorithm_name), bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    tc_button.pack(side=tk.LEFT, padx=30)

# Code button
    code_button = tk.Button(button_frame, text="Code", command=lambda: display_algorithm_code(algorithm_name),
                        bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    code_button.pack(side=tk.LEFT, padx=10)


    return explanation_dialog

# Create the root window
root = tk.Tk()
root.configure(bg="lightgreen")
root.attributes('-fullscreen', True)

button_close = tk.Button(root, text="Close", command=root.quit, font=("Helvetica", 12, "bold"), bg="red", fg="black")
button_close.place(relx=1.0, rely=0.0, anchor="ne")  # Position at top right corner

# Optionally, add a bit of delay to ensure that screen information is fully updated
root.update_idletasks()


# Construct the image path dynamically
image_path = resource_path("img2.jpg")
# image_path = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\img2.jpg"
image = Image.open(image_path)
image_width, image_height = image.size

# Text label at the top
title_label = tk.Label(root, text="Choose any algorithm you want to visualize", font=("Georgia", 23, "bold"), fg="black", bg="lightgreen")
title_label.pack(side=tk.TOP, pady=30)  # Center the title at the top

# Create a frame for the image with a border
frame_image = tk.Frame(root, bd=3, relief=tk.SUNKEN)
frame_image.pack(side=tk.LEFT, padx=60)

# Create a photoimage object of the image
image_tk = ImageTk.PhotoImage(image)

# Create a label widget to display the image within the frame
label_image = tk.Label(frame_image, image=image_tk)
label_image.pack()

frame_buttons = tk.Frame(root, bg="lightblue")
frame_buttons.pack(side=tk.RIGHT, padx=5, pady=88, anchor=tk.NE)

# Button labels and colors

button_specs = [
    ("DFS", "yellow", "GraphAlgos/dfs_random.py"),
    ("BFS", "red", "GraphAlgos/bfs_random.py"),
    ("Topo Sort", "lightgreen", "GraphAlgos/topo_sort_random.py"),
    ("Dijkstra", "cyan", "GraphAlgos/dijkstra_random.py"),
    ("Bellman Ford", "lightblue", "GraphAlgos/bellman_random.py"),
    ("Prims", "brown", "GraphAlgos/prims_random.py"),
    ("Kruskals", "grey", "GraphAlgos/kruskals_random.py"),
    ("Kosaraju", "white", "GraphAlgos/kosaraju_random.py")
]

# button_specs = [
#     ("DFS", "yellow", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dfs_random.py"),
#     ("BFS", "red", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bfs_random.py"),
#     ("Topo Sort", "lightgreen", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\topo_sort_random.py"),
#     ("Dijkstra", "cyan", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\dijkstra_random.py"),
#     ("Bellman Ford", "lightblue", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\bellman_random.py"),
#     ("Prims", "brown", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\prims_random.py"),
#     ("Kruskals", "grey", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kruskals_random.py"),
#     ("Kosaraju", "white", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GraphAlgos\\kosaraju_random.py")
# ]
# Function to create buttons dynamically
def create_buttons():
    for i, (text, color, script_path) in enumerate(button_specs):
        row = i // 2
        col = i % 2
        button = tk.Button(frame_buttons, text=text, width=15, height=2, command=lambda p=script_path, name=text: open_initial_dialog(p, name),
                           bd=6,  # Set border width
                           highlightbackground="black",  # Set border color
                           highlightthickness=1,
                           font=("Helvetica", 14, "bold"), bg=color, fg="black")
        button.grid(row=row, column=col, padx=37, pady=34)

# Call the function to create buttons
create_buttons()

# Create the root window
root.mainloop()
