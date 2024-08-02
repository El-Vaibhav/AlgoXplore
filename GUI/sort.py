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
    if size is not None and value_range is not None:
        args += ["--size", str(size), "--range", str(value_range)]
    
    subprocess.Popen(args)

# Function to open the input dialog
def open_input_dialog(file_path, algorithm_name):
    def submit():
        try:
            size = int(size_entry.get())
            value_range = int(range_entry.get())
            close_dialogs()
            execute_sorting_algorithm(file_path, size=size, value_range=value_range)
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
    explanation_dialog = display_algorithm_explanation(algorithm_name)

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
    code_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Map algorithm names to file paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Codes'))

    code_paths = {
    "Bubble Sort": os.path.join(base_dir, "bubble_sort.py"),
    "Insertion Sort": os.path.join(base_dir, "insertion_sort.py"),
    "Merge Sort": os.path.join(base_dir, "merge_sort.py"),
    "Quick Sort": os.path.join(base_dir, "quick_sort.py"),
    "Selection Sort": os.path.join(base_dir, "selection_sort.py"),  # Corrected the filename
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
# Function to display algorithm explanation
def display_algorithm_explanation(algorithm_name):
    explanations = {
        "Bubble Sort": "Bubble Sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. The time complexity is O(n^2) for all three cases (Worst , Avg , Best)",
        "Insertion Sort": "Insertion Sort is a simple sorting algorithm that builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort. The Time complexity for the best case is O(n) when the array is sorted , for the remaining cases it is O(n^2)",
        "Merge Sort": "Merge Sort is an efficient, stable, comparison-based, divide and conquer sorting algorithm. Most implementations produce a stable sort, meaning that the order of equal elements is the same in the input and output.",
        "Quick Sort": "Quick Sort is an efficient, in-place sorting algorithm that in practice is faster than MergeSort and HeapSort. However, it is not a stable sort, meaning that the relative order of equal sort items is not preserved.",
        "Selection Sort": "Selection Sort is an in-place comparison sorting algorithm. It has an O(n^2) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort."
    }

    explanation = explanations.get(algorithm_name, "No explanation available for this algorithm.")
    
    explanation_dialog = tk.Toplevel(root)
    explanation_dialog.title(f"{algorithm_name} Explanation")
    explanation_dialog.geometry("440x440+850+100")  # Set position to open the dialog on the far right side
    explanation_dialog.configure(bg="red")  # Set the background color to black
    explanation_dialog.resizable(False, False)  # Disable maximizing
    font_style = ("Helvetica", 15, "bold")
    explanation_label = tk.Label(explanation_dialog, text=explanation, font=font_style, fg="white", bg="red", wraplength=400, justify=tk.LEFT)
    explanation_label.pack(padx=20, pady=20)

    code_button = tk.Button(explanation_dialog, text="Code", command=lambda: display_algorithm_code(algorithm_name),
                            bg="grey", fg="black", font=("Helvetica", 12, "bold"))
    code_button.pack(pady=10)

    return explanation_dialog

# Create the root window
root = tk.Tk()
root.configure(bg="black")
root.title("AlgoViz")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.attributes('-fullscreen', True)

# def go_back():
#     root.destroy()
#     subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\1.py"])

# button_back = tk.Button(root, text="Back", command=go_back, font=("Helvetica", 12, "bold"), bg="lightcoral", fg="black")
# button_back.place(x=10, y=10)  # Position at top left corner

button_close = tk.Button(root, text="Close", command=root.quit, font=("Helvetica", 12, "bold"), bg="red", fg="black")
button_close.place(relx=1.0, rely=0.0, anchor="ne")  # Position at top right corner

# Optionally, add a bit of delay to ensure that screen information is fully updated
root.update_idletasks()
# Message label
message_label = tk.Label(root, text="Choose any algorithm you want to visualize", font=("Tahoma", 18, "bold"), fg="white", bg="black")
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
frame_buttons = tk.Frame(root, bg="black")
frame_buttons.pack(side=tk.LEFT, padx=50, pady=10)  # Pack to the left side with default anchor

# Button configurations
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sorting_Algos'))

button_configs = [
    ("Bubble Sort", "red", os.path.join(base_dir, "bubble_sort.py")),
    ("Insertion Sort", "green", os.path.join(base_dir, "insertion_sort.py")),
    ("Merge Sort", "blue", os.path.join(base_dir, "merge_sort.py")),
    ("Quick Sort", "orange", os.path.join(base_dir, "quick_sort.py")),
    ("Selection Sort", "purple", os.path.join(base_dir, "selection_sort.py"))
]

# Create buttons dynamically
buttons = []
for text, bg_color, file_path in button_configs:
    button = tk.Button(frame_buttons, text=text, width=15, height=2,
                       command=lambda path=file_path, name=text: open_input_dialog(path, name),
                       font=("Helvetica", 14, "bold"), bg=bg_color, fg="white")
    button.pack(side=tk.LEFT, padx=50, pady=5)
    buttons.append(button)

root.mainloop()
