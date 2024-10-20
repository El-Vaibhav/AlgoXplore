import tkinter as tk
from PIL import ImageTk, Image
import subprocess
import os

# Get the current script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Function to handle button click
def button_click1():
    # subprocess.Popen(["python", os.path.join(base_dir, "graph.py")])
    subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\graph.py"])

def button_click2():
    # subprocess.Popen(["python", os.path.join(base_dir, "sort.py")])
    subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\scheduling.py"])

def button_click3():
    # subprocess.Popen(["python", os.path.join(base_dir, "sort.py")])
    subprocess.Popen(["python", "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\sort.py"])
    
  
# Create the root window
root = tk.Tk()
root.configure(bg="#072B29")
# root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

root.attributes('-fullscreen', True)

# Welcome label , a Label is a widget used to display text or images
welcome_label = tk.Label(root, text="Welcome to AlgoXplore", font=("Tahoma", 18, "bold"), fg="white", bg="#072B29")

# pack() is one of Tkinter's geometry managers, which control the layout of widgets in a window. It arranges widgets in blocks before placing them in the parent widget.
welcome_label.pack(anchor=tk.N, padx=20, pady=20)  # Anchor to the North (tk.N) (top) with padding

# Load the main background image
# image_path_main = os.path.join(base_dir, "img1.jpg")
image_path_main = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\img1.jpg"
image_main = Image.open(image_path_main)
image_width_main, image_height_main = image_main.size

# Create a photoimage object of the main image
image_tk_main = ImageTk.PhotoImage(image_main)

# Create a label widget to display the main image
label_main = tk.Label(root, image=image_tk_main)
label_main.pack()

# Load the small image 1
# image_path_small1 = os.path.join(base_dir, "small_img1.png")
image_path_small1 = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\small_img1.png"
image_small1 = Image.open(image_path_small1)
image_width_small1, image_height_small1 = image_small1.size

# Resize the small image 1
new_width1 = 300  # Adjust this value as needed
new_height1 = int((new_width1 / image_width_small1) * image_height_small1) # adjusting new height according to new width using unitary method
image_small1 = image_small1.resize((new_width1, new_height1))

# Create a photoimage object of the small image 1
image_tk_small1 = ImageTk.PhotoImage(image_small1)

# Create a label widget to display the small image 1 with border
label_small_image1 = tk.Label(root, image=image_tk_small1, bg="black", highlightthickness=3, highlightbackground="white")

# using place here instead of pack 
# Unlike pack() or grid(), which arrange widgets relative to other widgets, place() allows you to specify exact positions i.e x and y coordinates
label_small_image1.place(x=200, y=(image_height_main - new_height1) // 1.1)  # Adjust position above button 1

# A Frame is a container widget used to organize and group other widgets, while a Label is a widget used to display text or images. For buttons we are using frame here
# Frame for the first button (Explore Graph Algorithms)
frame_buttons1 = tk.Frame(root, bg="black")
frame_buttons1.place(x=200, y=(image_height_main - new_height1) // 1.1 + new_height1 + 20)  # Increase space between button and small image1 using +20 

# Button 1: Explore Graph Algorithms
button1 = tk.Button(frame_buttons1, text="Explore Graph Algorithms", width=25, height=2, command=button_click1,
                    font=("Helvetica", 15, "bold"), bg="lightgreen", fg="black")
button1.pack() # to display the button

button_close = tk.Button(root, text="Close", command=root.quit, font=("Helvetica", 12, "bold"), bg="red", fg="black")
button_close.place(relx=1.0, rely=0.0, anchor="ne")  # Position at top right corner north east

# Load the small image 2
# image_path_small2 = os.path.join(base_dir, "small_img2.jpeg")
image_path_small2 = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\small_img3.png"
image_small2 = Image.open(image_path_small2)
image_width_small2, image_height_small2 = image_small2.size

# Resize the small image 2
new_width2 = 300  # Adjust this value as needed
new_height2 = 168
image_small2 = image_small2.resize((new_width2, new_height2))

# Create a photoimage object of the small image 2
image_tk_small2 = ImageTk.PhotoImage(image_small2)

# Create a label widget to display the small image 2 with border
label_small_image2 = tk.Label(root, image=image_tk_small2, bg="black", highlightthickness=3, highlightbackground="white")
label_small_image2.place(x=620, y=(image_height_main - new_height2) // 1.1)  # Adjust position above button 2

frame_buttons2 = tk.Frame(root, bg="black")
frame_buttons2.place(x=620, y=(image_height_main - new_height2) // 1.1 + new_height2 + 20)  # Increase space below small image 2

# Button 2: Explore Sorting Algorithms
button2 = tk.Button(frame_buttons2, text="Explore Scheduling Algorithms", width=25, height=2, command=button_click2,
                    font=("Helvetica", 15, "bold"), bg="#FFE79E", fg="black")
button2.pack()

# Load the small image 3
# image_path_small2 = os.path.join(base_dir, "small_img2.jpeg")
image_path_small3 = "C:\\Users\\HP\\OneDrive\\Desktop\\algo_visualizer\\GUI\\small_img2.jpeg"
image_small3 = Image.open(image_path_small3)
image_width_small3, image_height_small3 = image_small3.size

new_width3 = 300  # Adjust this value as needed
new_height3 = int((new_width3 / image_width_small3) * image_height_small3)
image_small3 = image_small3.resize((new_width3, new_height3))

# Create a photoimage object of the small image 2
image_tk_small3 = ImageTk.PhotoImage(image_small3)

# Create a label widget to display the small image 2 with border
label_small_image3 = tk.Label(root, image=image_tk_small3, bg="black", highlightthickness=3, highlightbackground="white")
label_small_image3.place(x=1030, y=(image_height_main - new_height3) // 1.1)  # Adjust position above button 3

# Frame for the second button (Explore Sorting Algorithms)
frame_buttons3 = tk.Frame(root, bg="black")
frame_buttons3.place(x=1029, y=(image_height_main - new_height3) // 1.1 + new_height3 + 20)  # Increase space below small image 2

# Button 2: Explore Sorting Algorithms
button3 = tk.Button(frame_buttons3, text="Explore Sorting Algorithms", width=25, height=2, command=button_click3,
                    font=("Helvetica", 15, "bold"), bg="lightblue", fg="black")
button3.pack()

# Start the main loop
root.mainloop()
