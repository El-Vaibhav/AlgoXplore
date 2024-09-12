import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import tkinter as tk
from tkinter import messagebox
import sys

# Bubble sort algorithm with color updates

# In the bubble sort function, yield allows the function to pause and return the current state of the data 
# (array values and colors). This is essential for visualizing the sorting process step by step. After returning 
# the current state, the function can be resumed from where it left off to continue sorting the array.
# The sorting process is broken down into discrete steps or "frames" of the animation. 
# Each yield statement produces one frame, showing the current state of the array. 
# These frames are then passed to the FuncAnimation function, which updates the plot at each step.


# Why yield copy?
# In Python, lists are mutable objects. If you were to yield the data list directly, any subsequent modification 
# to that list would affect the previously yielded versions as well, because all references to the list point to the same object in memory.
# By using data.copy(), you create a shallow copy of the list. This copy is a new list object that contains 
# the same elements as data, but it's independent of the original list. Therefore, changes to data after yielding won't 
# affect the copy that was yielded earlier.

def bubble_sort(data, color_data):
    n = len(data)
    for i in range(n):

        for j in range(n - 1 - i):

            color_data[j] = 'purple'  # Mark the elements being compared
            yield data.copy(), color_data.copy() # yield to update the visualization

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                color_data[j], color_data[j + 1] = 'red', 'red'  # Mark swapped elements
                yield data.copy(), color_data.copy()

            color_data[j], color_data[j + 1] = 'blue', 'blue'  # Reset to default color

        color_data[n - 1 - i] = 'green'  # Mark the last sorted element

        yield data.copy(), color_data.copy()  # Yield to update the visualization

    # for k in range(n):
    #     color_data[k] = 'green'  # Mark all elements as sorted
    # yield data.copy(), color_data.copy()  # Final yield to show all elements in green

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
# argparse is a Python library used to create user-friendly command-line interfaces.
# It allows you to define arguments that your script accepts from the command line, parse those arguments, and then use them within your script.

parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, default=10, help='Size of the array to generate')
parser.add_argument('--range', type=int, default=100, help='Range of values for the random array')

# when you run your script from the command line, the arguments passed are parsed and stored in the args variable as attributes.
# Once parsed, you can access the arguments through the args variable:
args = parser.parse_args()

# Validate and process arguments
if args.size <= 0:
    show_error("The size of the array must be a positive integer.")
    sys.exit(1)  # Exit the script
elif args.range <= 0:
    show_error("The range of values must be a positive integer.")
    sys.exit(1)  # Exit the script
else:
    data = [random.randint(1, args.range) for _ in range(args.size)] # genrate the array give random entries the number of entries are known :)

# Initialize color data for the bars
print(data)
color_data = ['blue'] * len(data)

# The update_plot function is used to update the bar chart during each step of the bubble sort. 
# As the sort progresses, the heights and colors of the bars will change to reflect the current state of the array.
def update_plot(frame, bars):
    # frame is a tuple containing data and color_data
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_ylim(0, max(data) + 10)
ax.set_title("Bubble Sort Visualization")

# When align='edge' is used, it means that the bars will be aligned such that one edge of the bar 
# (usually the left edge for vertical bars) is placed exactly at the corresponding x-coordinate.
# For example, if you have a bar positioned at x=0, the left edge of that bar will be at x=0.

bars = ax.bar(range(len(data)), data, align='edge', color='blue')

# Define color legend annotations using handles

# (0, 0): Lower-left corner coordinates.
# 1: Width of the rectangle.
# 1: Height of the rectangle.
# Since this rectangle is not actually being placed on the plot but is used in a legend, 
# the specific coordinates (0, 0) are arbitrary and do not affect the appearance of the rectangle in the legend.
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color='purple', label='Comparing with next element'),
    plt.Rectangle((0, 0), 1, 1, color='red', label='Swapped'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='Unsorted'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='Sorted')
]

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Generate frames for animation
frames = bubble_sort(data, color_data)

# Create animation

# FuncAnimation is a function provided by matplotlib.animation that allows you to create animations by 
# repeatedly calling a specified update function. It updates the figure (or plot) based on a series of 
# frames and redraws it at a specified interval.

ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=700)
plt.show()
