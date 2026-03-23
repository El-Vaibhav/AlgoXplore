import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import ImageTk, Image
import subprocess
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


# Function to execute different scheduling algorithms
def execute_scheduling_algorithm(file_path, arrival_time=None, burst_time=None, priority=None, time_quantum=None):

    # Resolve path inside PyInstaller temp directory
    file_path = resource_path(file_path)

    args = [sys.executable, file_path]

    if burst_time is not None:
        args += ["--burst_time", str(burst_time)]
    if arrival_time is not None:
        args += ["--arrival_time", str(arrival_time)]
    if priority is not None:
        args += ["--priority", str(priority)]
    if time_quantum is not None:
        args += ["--time_quantum", str(time_quantum)]

    subprocess.Popen(args)

# Function to open the input dialog
def open_input_dialog(file_path, algorithm_name):
    def submit():
        try:
            nonlocal arrival_entry, priority_entry,time_quant_entry
            arrival_time = arrival_entry.get() if arrival_entry else None
            burst_time = burst_entry.get()
            priority = priority_entry.get() if priority_entry else None
            time_quantum = time_quant_entry.get() if time_quant_entry else None
            close_dialogs()
            execute_scheduling_algorithm(file_path, arrival_time=arrival_time, burst_time=burst_time, priority=priority,time_quantum=time_quantum)
            display_algorithm_explanation(algorithm_name,dialog)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid input values.")
    
    def close_dialogs():
        dialog.destroy()
        explanation_dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Input Options")
    dialog.geometry("440x440+400+100")  # Set position to open the dialog on the right side
    dialog.configure(bg="brown")  # Set the background color to brown
    dialog.resizable(False, False)  # Disable maximizing

    font_style = ("Helvetica", 15, "bold")
    font_style2 = ("Helvetica", 13, "bold")
    font_style3 = ("Helvetica", 9, "bold")

     # Initialize entry fields
    arrival_entry = None
    priority_entry = None
    
    tk.Label(dialog, text="Enter details for the scheduling algorithm:", fg="Yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=(40,0))

    # if algorithm_name not in ["Priority"]:
    #  tk.Label(dialog, text="(enter values separated by commas)", fg="Yellow", bg="brown", font=font_style2).pack(anchor=tk.W, padx=(15,5) , pady=20)
    
    if algorithm_name not in ["Priority"] and algorithm_name not in ["RR"]  :
     tk.Label(dialog, text="(in case of no arrival time enter 0,0,0..)", fg="Yellow", bg="brown", font=font_style2).pack(anchor=tk.W, padx=(15,5) , pady=20)
    
    tk.Label(dialog, text="Arrival Time (eg 1,2,3,4):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
    arrival_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
    arrival_entry.pack(anchor=tk.W, padx=20, pady=15)
    
    tk.Label(dialog, text="Burst Time (eg 1,2,3,4):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
    burst_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
    burst_entry.pack(anchor=tk.W, padx=20, pady=15)
    
    if algorithm_name in ["RR"]:
        tk.Label(dialog, text="Time Quantum :", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        time_quant_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        time_quant_entry.pack(anchor=tk.W, padx=20, pady=15)
    else:
        time_quant_entry = None

    # Conditionally add priority entry based on algorithm type
    if algorithm_name in ["Priority"]:
        tk.Label(dialog, text="Priority (Largest number = max priority):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
        priority_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
        priority_entry.pack(anchor=tk.W, padx=20, pady=15)
    else:
        priority_entry = None

    submit_button = tk.Button(dialog, text="Submit", command=submit, bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=20)

    explanation_dialog = display_algorithm_explanation(algorithm_name,dialog)

    dialog.protocol("WM_DELETE_WINDOW", close_dialogs)
    explanation_dialog.protocol("WM_DELETE_WINDOW", close_dialogs)

def display_algo_tc(algorithm_name):
    import subprocess
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
    import sys

    # Time complexity script paths for scheduling algorithms


    tc_code_paths = {
    "FCFS": resource_path("Time_Complexity/N_sq.py"),
    "Priority": resource_path("Time_Complexity/N_log.py"),
    "SJF": resource_path("Time_Complexity/N_sq.py"),
    "SRTF": resource_path("Time_Complexity/N_sq.py"),
    "RR": resource_path("Time_Complexity/N_sq.py"),
    }

    # tc_code_paths = {
    #     "FCFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
    #     "Priority": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_log.py",
    #     "SJF": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
    #     "SRTF": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
    #     "RR": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
    # }

    # Detailed explanations for scheduling algorithms
    complexity_explanations = {
        "FCFS": (
            "First Come First Serve (FCFS) - Time Complexity Analysis:\n"
            "1. All processes are scheduled in the order they arrive.\n"
            "2. Sorting is not required.\n"
            "3. Processing N processes in order: O(N)\n"
            "4. In worst-case implementations (using lists improperly), it can take O(N^2).\n"
            "5. Time Complexity: O(N) or O(N^2) based on implementation.\n"
            "6. Space Complexity: O(N).\n"
        ),
        "Priority": (
            "Priority Scheduling - Time Complexity Analysis:\n"
            "1. Sorting processes by priority: O(N log N)\n"
            "2. Each process may be selected based on highest/lowest priority.\n"
            "3. Insertion in a priority queue: O(log N) per process.\n"
            "4. Total Time Complexity:\n"
            "   - With sorting: O(N log N)\n"
            "   - With PQ: O(N log N)\n"
            "5. Space Complexity: O(N).\n"
        ),
        "SJF": (
            "Shortest Job First (SJF) - Time Complexity Analysis:\n"
            "1. Requires sorting by burst time: O(N log N)\n"
            "2. If precomputed, execution is linear: O(N)\n"
            "3. Worst-case if unsorted and selected each time: O(N^2)\n"
            "4. Total Time Complexity: O(N log N) or O(N^2)\n"
            "5. Space Complexity: O(N).\n"
        ),
        "SRTF": (
            "Shortest Remaining Time First (SRTF) - Time Complexity Analysis:\n"
            "1. Requires checking remaining time at every unit time.\n"
            "2. Can use priority queue/min-heap for efficient selection: O(log N)\n"
            "3. Total Time Complexity:\n"
            "   - Without PQ: O(N^2)\n"
            "   - With PQ: O(N log N)\n"
            "4. Space Complexity: O(N).\n"
        ),
        "RR": (
            "Round Robin (RR) - Time Complexity Analysis:\n"
            "1. Each process gets time quantum in cyclic order.\n"
            "2. Worst-case: each process runs multiple times.\n"
            "3. Let K = average number of cycles per process.\n"
            "4. Total Time Complexity: O(N * K)\n"
            "5. For large K, can be O(N^2)\n"
            "6. Space Complexity: O(N).\n"
        ),
    }

    code_path = tc_code_paths.get(algorithm_name)
    explanation_text = complexity_explanations.get(algorithm_name, "No explanation available.")

    if code_path:
        try:
            # Launch TC graph window on far left
            tc_process =subprocess.Popen([sys.executable, code_path])

            # Launch explanation window on right
            explanation_window = tk.Toplevel()
            explanation_window.title(f"{algorithm_name} - Time Complexity Analysis")
            explanation_window.geometry("520x450+900+100")  # Right side
            explanation_window.configure(bg="black")
            explanation_window.resizable(False, False)

            # Scrollable detailed text
            scroll_text = scrolledtext.ScrolledText(explanation_window, wrap=tk.WORD,
                                                    font=("Courier", 12, "bold"),
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
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run TC visualization: {str(e)}")
    else:
        messagebox.showerror("Error", "No time complexity script found for this algorithm.")


def display_algorithm_code(algorithm_name):
    code_dialog = tk.Toplevel(root)
    code_dialog.title(f"{algorithm_name} Code")
    code_dialog.geometry("600x400")  # Adjust size as needed
    code_dialog.configure(bg="black")

    code_text = scrolledtext.ScrolledText(code_dialog, wrap=tk.WORD, font=("Courier", 12,"bold"), bg="white", fg="darkblue")
    code_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


    code_paths = {
    "FCFS": resource_path("Codes/FCFS.py"),
    "Priority": resource_path("Codes/Priority_NP.py"),
    "SJF": resource_path("Codes/SJF.py"),
    "SRTF": resource_path("Codes/SRTF.py"),
    "RR": resource_path("Codes/RR.py"),
    }


    # code_paths = {
    #     "FCFS": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\FCFS.py",
    #     "Priority": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\Priority_NP.py",
    #     "SJF": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\SJF.py",
    #     "SRTF": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\srtf.py",
    #     "RR": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\rr.py",
    # }

    code_path = code_paths.get(algorithm_name)
    if code_path:
        try:
            with open(code_path, 'r') as file:
                code = file.read()
                code_text.insert(tk.END, code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load code for {algorithm_name}: {str(e)}")

def display_algorithm_explanation(algorithm_name,dialog):
    explanations = {
        "FCFS": "First-Come, First-Served (FCFS) is a scheduling algorithm where processes are executed in the order they arrive in the ready queue. It is simple but can lead to long waiting times for some processes if a long process arrives before shorter ones.",
        "SJF": "Shortest Job First (SJF) is a scheduling algorithm that selects the process with the shortest execution time first. It can be preemptive (Shortest Remaining Time First) or non-preemptive. It minimizes average waiting time but may lead to starvation of longer processes.",
        "SRTF": "Shortest Remaining Time First (SRTF) is the preemptive version of SJF where the process with the shortest remaining time is executed first. It provides optimal scheduling in terms of minimizing average waiting time but can lead to high overhead due to frequent context switches.",
        "RR": "Round Robin (RR) is a preemptive scheduling algorithm where each process is assigned a fixed time slice (quantum) in a cyclic order. It ensures fairness and responsiveness but can lead to high turnaround times for processes if the quantum is too large.",
        "Priority": "Priority Scheduling is a Non preemptive scheduling algorithm where processes are executed based on their priority. Processes with higher priority are executed before those with lower priority. It can be preemptive or non-preemptive and may lead to starvation of low-priority processes."
    }

    explanation = explanations.get(algorithm_name, "No explanation available for this algorithm.")
    
    explanation_dialog = tk.Toplevel(root)
    explanation_dialog.title(f"{algorithm_name} Explanation")
    explanation_dialog.geometry("440x440+990+100")  # Set position to open the dialog on the far right side
    explanation_dialog.configure(bg="red")  # Set the background color to red
    explanation_dialog.resizable(False, False)  # Disable maximizing
    font_style = ("Helvetica", 15, "bold")
    explanation_label = tk.Label(explanation_dialog, text=explanation, font=font_style, fg="white", bg="red", wraplength=400, justify=tk.LEFT)
    explanation_label.pack(padx=20, pady=20)

    def close_dialogs():
     if dialog.winfo_exists():
        dialog.destroy()
     if explanation_dialog.winfo_exists():
        explanation_dialog.destroy()

    # Bind the window close event (the "X" button) to close both dialogs
    if dialog.winfo_exists():
     dialog.protocol("WM_DELETE_WINDOW", close_dialogs)

    if explanation_dialog.winfo_exists():
     explanation_dialog.protocol("WM_DELETE_WINDOW", close_dialogs)

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
root.configure(bg="black")
root.title("AlgoViz")
root.attributes('-fullscreen', True)

# Load the image and use it as a background


image_path = resource_path("laptop-infographic-online-6087062.png")

image = Image.open(image_path)
image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

image_tk = ImageTk.PhotoImage(image)

# Create a label to hold the background image
background_label = tk.Label(root, image=image_tk,borderwidth=35, relief="solid")
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the image to cover the whole window

# Create a frame to hold the buttons and other elements

instruction_label = tk.Label(root, text="Select any algorithm you want to visualize", bg="#ffc94d", fg="black", font=("Georgia", 23, "bold"))
instruction_label.pack(pady=55)  # Add padding to position it nicely at the top

button_configs = [
    ("FCFS", "red", "scheduling_algos/FCFS.py"),
    ("Priority", "cyan", "scheduling_algos/priority.py"),
    ("SJF", "lightblue", "scheduling_algos/SJF.py"),
    ("SRTF", "yellow", "scheduling_algos/SRTF.py"),
    ("RR", "lightgreen", "scheduling_algos/RR.py"),
]

# button_configs = [
#     ("FCFS", "red", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\scheduling_algos\\fcfs.py"),
#     ("SJF", "lightblue", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\scheduling_algos\\sjf.py"),
#     ("SRTF", "yellow", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\scheduling_algos\\srtf.py"),
#     ("RR", "lightgreen", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\scheduling_algos\\rr.py"),
#     ("Priority", "cyan", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\scheduling_algos\\priority.py")
# ]

frame_buttons = tk.Frame(root, bg="#ffc94d")  # Use quotes around the hex color code 

# Add padding to frame_buttons to push it down from the top of the window
frame_buttons.pack(pady=10)  # Add padding from the top

# Create buttons for each scheduling algorithm
for idx, (name, color, file_path) in enumerate(button_configs):
    button = tk.Button(frame_buttons, text=name, bg=color, font=("Helvetica", 17, "bold"), 
                       command=lambda n=name, p=file_path: open_input_dialog(p, n),width=7,bd=6,  # Set border width
                       highlightbackground="black",  # Set border color
                       highlightthickness=1)
    button.grid(row=10, column=idx, padx=80, pady=1)


button_close = tk.Button(root, text="Close", command=root.quit, font=("Helvetica", 12, "bold"), bg="red", fg="black")
button_close.place(relx=1.0, rely=0.0, anchor="ne")  # Position at top right corner

# Start the Tkinter event loop
root.mainloop()
