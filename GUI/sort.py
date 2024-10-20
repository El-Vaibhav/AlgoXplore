import tkinter as tk
from tkinter import messagebox,scrolledtext
from PIL import ImageTk, Image
import subprocess
import sys
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir1 = os.path.dirname(current_dir)

# Function to execute different sorting algorithms
def execute_sorting_algorithm(file_path, size=None, value_range=None):

    args = [sys.executable, file_path]
    # sys.executable: This is the Python interpreter that is currently running your main script. For example, it could be C:\Python39\python.exe on Windows.
    # file_path: The path to the Python script you want to execute (e.g., "path_to_sort.py").

    if size is not None and value_range is not None:
        args += ["--size", str(size), "--range", str(value_range)]
    
    subprocess.Popen(args) 
    # The subprocess.Popen(args) command runs the code from the file specified in the file_path by launching a new process in the operating system.

# Function to open the input dialog
def open_input_dialog(file_path, algorithm_name):
    def submit():
        try:
            size = int(size_entry.get())
            value_range = int(range_entry.get())
            close_dialogs()
            execute_sorting_algorithm(file_path, size=size, value_range=value_range)
            display_algorithm_explanation(algorithm_name,dialog)
            close_dialogs()

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for size and range.")
    
    def close_dialogs():
        dialog.destroy()
        explanation_dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Input Options")
    dialog.geometry("440x440+400+100")  # Set position to open the dialog on the right side
    dialog.configure(bg="brown")  # Set the background color to brown
    dialog.resizable(False, False)  # Disable maximizing

    # Configure the font
    font_style = ("Helvetica", 15, "bold")
    font_style2 = ("Helvetica", 13, "bold")

    tk.Label(dialog, text="Enter size and range for the random array:", fg="Yellow", bg="brown", font=font_style).pack(anchor=tk.W, padx=20, pady=(40,0))
    tk.Label(dialog, text="(enter upto 30 elements for better understanding)", fg="Yellow", bg="brown", font=font_style2).pack(anchor=tk.W, padx=(15,5) , pady=20)

    tk.Label(dialog, text="Size:", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
    size_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
    size_entry.pack(anchor=tk.W, padx=20, pady=15)
    
    tk.Label(dialog, text="Range (Start's From 1):", fg="white", bg="brown", font=font_style).pack(anchor=tk.W, padx=20)
    range_entry = tk.Entry(dialog, width=30, bg="white", font=font_style)
    range_entry.pack(anchor=tk.W, padx=20, pady=15)
    
    submit_button = tk.Button(dialog, text="Submit", command=submit, bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=20)

    # Display algorithm explanation
    explanation_dialog = display_algorithm_explanation(algorithm_name,dialog)

    # Bind close events to close both dialogs
    dialog.protocol("WM_DELETE_WINDOW", close_dialogs)
    explanation_dialog.protocol("WM_DELETE_WINDOW", close_dialogs)

def display_algorithm_code(algorithm_name):
    # Create a new window to display the code
    code_dialog = tk.Toplevel(root)
    code_dialog.title(f"{algorithm_name} Code")
    code_dialog.geometry("600x400")  # Adjust size as needed
    code_dialog.configure(bg="black")

    # Create a scrolled text widget to display the code
    code_text = scrolledtext.ScrolledText(code_dialog, wrap=tk.WORD, font=("Courier", 12,"bold"), bg="white", fg="darkblue")
    # The wrap=tk.WORD argument is specifying that the text should wrap at word boundaries, ensuring that words are not split across lines when wrapping occurs.

    code_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10) # will make the code_text widget expand to fill the entire space of its container in both dimensions, with 10 pixels of padding on all sides.

    # Map algorithm names to file paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Codes'))

    # code_paths = {
    # "Bubble Sort": os.path.join(base_dir, "bubble_sort.py"),
    # "Insertion Sort": os.path.join(base_dir, "insertion_sort.py"),
    # "Merge Sort": os.path.join(base_dir, "merge_sort.py"),
    # "Quick Sort": os.path.join(base_dir, "quick_sort.py"),
    # "Selection Sort": os.path.join(base_dir, "selection_sort.py"),  
    # }

    code_paths = {
    "Bubble Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\bubble_sort.py",
    "Insertion Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\insertion_sort.py",
    "Merge Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\merge_sort.py",
    "Quick Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Codes\\quick_sort.py",
    "Selection Sort": "C:\\Users\\HP\OneDrive\\Desktop\\algo_visualizer\\Codes\\selection_sort.py"
    }

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
    # Mapping algorithm names to their corresponding time complexity script paths
    tc_code_paths = {
   
        "Bubble Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
        "Insertion Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
        "Quick Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_log.py",
        "Merge Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_log.py",
        "Selection Sort": "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Time_Complexity\\N_sq.py",
    }

    # Get the code path for the selected algorithm
    code_path = tc_code_paths.get(algorithm_name)
    if code_path:
        try:
            # Execute the time complexity script for the selected algorithm
            subprocess.Popen([sys.executable, code_path])  # Run the corresponding time complexity script
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run time complexity code for {algorithm_name}: {str(e)}")
    else:
        messagebox.showerror("Error", "No time complexity script found for this algorithm.")

            
# Function to display algorithm explanation
def display_algorithm_explanation(algorithm_name,dialog):
    explanations = {
        "Bubble Sort": "Bubble Sort is a simple brute force sorting algorithm that repeatedly iterates through the list, compares adjacent elements, and swaps them if they are in the wrong order. The iteartion through the list is repeated until the whole list is sorted. On every iteration we get the sorted element of that iteration at the end of the array The time complexity is O(n^2) for all three cases (Worst , Avg , Best)",
        "Insertion Sort": "Insertion Sort one by one makes the sorted array starting from left most element.The first element is always sorted. It starts from the second element compares it with remaining left array (elemnt 1) , inserts it in it's correct position. Same way now it takes the third element compares it with the left array (element 1 and 2) and insert 3rd element in its sorted position. This way it sorts the array . The best case TC is O(N) when array is sorted , it is O(N^2) for worst and average case",
        "Quick Sort": "Quick Sort takes one pivot element starting from left or right and finds it's correct position in the array and then recursively apply the same algorithm to both left and right subarray of that pivot element. It's best case time complexity is O(NlogN) when the partion is balanced i.e no. of elements are same in both left and right partition. Its worst case TC is O(N^2) when the partition is like one part has only 1 element , other part has n-1 elements.",
        "Selection Sort": " Selection Sort one by one selects all elements of the array from left and finds the min element less than the current element in the right half of the array. Once the min is found it swaps it with the current element. It has an O(n^2) time complexity for all three cases (Best,Avg,Worst).",
        "Merge Sort": "Merge sort is a recursive algorithm which keeps on dividing the array into equal halfs and when maximum limit of partition reaches (1,1 element left in two arrays) it starts its work in the combine step . Starting from the last parition it starts merging the two sorted arrays (as the arrays having only 1,1 element (last possible partition) are sorted by itself) into a single merged sorted array . It does this from bottom to top and in the end we get the full sorted array. It's TC is O(NlogN) for all three cases."}

    explanation = explanations.get(algorithm_name, "No explanation available for this algorithm.")
    
    explanation_dialog = tk.Toplevel(root)
    explanation_dialog.title(f"{algorithm_name} Explanation")
    explanation_dialog.geometry("440x440+850+100")  # Set position to open the dialog on the far right side
    explanation_dialog.configure(bg="red")  # Set the background color to red
    explanation_dialog.resizable(False, False)  # Disable maximizing
    font_style = ("Helvetica", 14, "bold")
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

# TC button
    tc_button = tk.Button(button_frame, text="Time Complexity", command= lambda: display_algo_tc(algorithm_name), bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    tc_button.pack(side=tk.LEFT, padx=30)

# Code button
    code_button = tk.Button(button_frame, text="Code", command=lambda: display_algorithm_code(algorithm_name),
                        bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    code_button.pack(side=tk.LEFT, padx=10)
    
    return explanation_dialog

# Create the root window
root = tk.Tk()
root.configure(bg="#8DB8B8")
root.title("AlgoViz")
# root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.attributes('-fullscreen', True)

button_close = tk.Button(root, text="Close", command=root.quit, font=("Helvetica", 12, "bold"), bg="red", fg="black")
button_close.place(relx=1.0, rely=0.0, anchor="ne")  # Position at top right corner

# Message label
message_label = tk.Label(root, text="Choose any algorithm you want to visualize", font=("Georgia", 23, "bold"), fg="black", bg="#8DB8B8")
message_label.pack(side=tk.TOP, padx=10, pady=15)  # Positioned at the top with padding

# Load the image
base_dir = os.path.abspath(os.path.dirname(__file__))

# Construct the image path dynamically
image_path = os.path.join(base_dir, "img5.png")
image = Image.open(image_path)
image_width, image_height = image.size

# Create a photoimage object of the image
image_tk = ImageTk.PhotoImage(image)

frame_image = tk.Frame(root, bd=5, relief=tk.SUNKEN)
frame_image.pack(side=tk.TOP, padx=20, pady=20)

# Create a label widget to display the image
label = tk.Label(frame_image, image=image_tk)
label.pack(side=tk.TOP, padx=10, pady=30)  # Positioned below the message label

# Create a frame for the buttons
frame_buttons = tk.Frame(root, bg="#8DB8B8")
frame_buttons.pack(side=tk.LEFT, padx=50, pady=10)  # Pack to the left side with default anchor

# Button configurations
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sorting_Algos'))

# button_configs = [
#     ("Bubble Sort", "red", os.path.join(base_dir, "bubble_sort.py")),
#     ("Insertion Sort", "green", os.path.join(base_dir, "insertion_sort.py")),
#     ("Merge Sort", "blue", os.path.join(base_dir, "merge_sort.py")),
#     ("Quick Sort", "orange", os.path.join(base_dir, "quick_sort.py")),
#     ("Selection Sort", "purple", os.path.join(base_dir, "selection_sort.py"))
# ]

button_configs=[ ("Bubble Sort","red", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Sorting_Algos\\bubble_sort.py"),
    ("Insertion Sort","green", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Sorting_Algos\\insertion_sort.py"),
    ("Merge Sort","blue", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Sorting_Algos\\merge_sort.py"),
    ("Quick Sort", "orange", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\Sorting_Algos\\quick_sort.py"),
    ("Selection Sort", "purple","C:\\Users\\HP\OneDrive\\Desktop\\algo_visualizer\\Sorting_Algos\\selection_sort.py")]

# Create buttons dynamically
buttons = []
for text, bg_color, file_path in button_configs:
    button = tk.Button(frame_buttons, text=text, width=15, height=2,
                       command=lambda path=file_path, name=text: open_input_dialog(path, name),bd=6,  # Set border width
                       highlightbackground="black",  # Set border color
                       highlightthickness=1,
                       font=("Helvetica", 14, "bold"), bg=bg_color, fg="white")
    # The lambda function allows you to pass arguments to the open_input_dialog function.
    #  If you didn't use lambda, the command would execute the function immediately when the button is created, rather than when the button is clicked
    button.pack(side=tk.LEFT, padx=50, pady=5)
    buttons.append(button)


root.mainloop()