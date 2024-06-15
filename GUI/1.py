import tkinter as tk
from PIL import ImageTk, Image
import subprocess

# Function to handle button click
def button_click1():
    subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\graph.py"])

def button_click2():
    subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\sort.py"])

# Create the root window
root = tk.Tk()
root.configure(bg="black")

# Welcome label
welcome_label = tk.Label(root, text="Welcome to AlgoXplore", font=("Tahoma", 18, "bold"), fg="white", bg="black")
welcome_label.pack(anchor=tk.N, padx=20, pady=20)  # Anchor to the North (top) with padding

# Load the main background image
image_path_main = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\img1.jpg"
image_main = Image.open(image_path_main)
image_width_main, image_height_main = image_main.size

# Create a photoimage object of the main image
image_tk_main = ImageTk.PhotoImage(image_main)

# Create a label widget to display the main image
label_main = tk.Label(root, image=image_tk_main)
label_main.pack()

# Load the small image 1
image_path_small1 = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\small_img1.png"
image_small1 = Image.open(image_path_small1)
image_width_small1, image_height_small1 = image_small1.size

# Resize the small image 1
new_width1 = 300  # Adjust this value as needed
new_height1 = int((new_width1 / image_width_small1) * image_height_small1)
image_small1 = image_small1.resize((new_width1, new_height1), Image.LANCZOS)

# Create a photoimage object of the small image 1
image_tk_small1 = ImageTk.PhotoImage(image_small1)

# Create a label widget to display the small image 1 with border
label_small_image1 = tk.Label(root, image=image_tk_small1, bg="black", highlightthickness=3, highlightbackground="white")
label_small_image1.place(x=200, y=(image_height_main - new_height1) // 1.2)  # Adjust position above button 1

# Frame for the first button (Explore Graph Algorithms)
frame_buttons1 = tk.Frame(root, bg="black")
frame_buttons1.place(x=200, y=(image_height_main - new_height1) // 1.2 + new_height1 + 20)  # Increase space below small image 1

# Button 1: Explore Graph Algorithms
button1 = tk.Button(frame_buttons1, text="Explore Graph Algorithms", width=35, height=2, command=button_click1,
                    font=("Helvetica", 15, "bold"), bg="lightgreen", fg="black")
button1.pack()

# Load the small image 2
image_path_small2 = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\small_img2.jpeg"
image_small2 = Image.open(image_path_small2)
image_width_small2, image_height_small2 = image_small2.size

# Resize the small image 2
new_width2 = 300  # Adjust this value as needed
new_height2 = int((new_width2 / image_width_small2) * image_height_small2)
image_small2 = image_small2.resize((new_width2, new_height2), Image.LANCZOS)

# Create a photoimage object of the small image 2
image_tk_small2 = ImageTk.PhotoImage(image_small2)

# Create a label widget to display the small image 2 with border
label_small_image2 = tk.Label(root, image=image_tk_small2, bg="black", highlightthickness=3, highlightbackground="white")
label_small_image2.place(x=1030, y=(image_height_main - new_height2) // 1.2)  # Adjust position above button 2

# Frame for the second button (Explore Sorting Algorithms)
frame_buttons2 = tk.Frame(root, bg="black")
frame_buttons2.place(x=910, y=(image_height_main - new_height2) // 1.2 + new_height2 + 20)  # Increase space below small image 2

# Button 2: Explore Sorting Algorithms
button2 = tk.Button(frame_buttons2, text="Explore Sorting Algorithms", width=35, height=2, command=button_click2,
                    font=("Helvetica", 15, "bold"), bg="lightblue", fg="black")
button2.pack()

# Start the main loop
root.mainloop()
