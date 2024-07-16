import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import tkinter as tk
from tkinter import messagebox
import sys


# Selection sort is a straightforward sorting algorithm that operates by repeatedly finding the minimum 
# element from the unsorted part of the array and swapping it with the first unsorted element.

# iterate through the array to find the smallest element.
# This involves comparing each element with the current minimum element found so far.
# Swap with First Unsorted Element:
# Once the smallest element is found, swap it with the first element of the unsorted part of the array.
# This effectively adds the smallest element to the sorted portion of the array.
# Repeat the above steps for the remaining unsorted part of the array, excluding the elements that have already been sorted.

# tc = wc,bc,ac = O(n^2)
def selection_sort(data, color_data):
    n = len(data)
    for i in range(n - 1):
        min_index = i
        color_data[min_index] = 'yellow'  # Mark current minimum index in yellow
        for j in range(i + 1, n):
            color_data[j] = 'blue'  # Reset color for comparison
            if data[j] < data[min_index]:
                min_index = j
                color_data[min_index] = 'yellow'  # Update new minimum index in yellow
        if min_index != i:
            data[i], data[min_index] = data[min_index], data[i]
            color_data[i], color_data[min_index] = 'red', 'red'  # Mark swapped elements in red
            yield data.copy(), color_data.copy()  # Yield a copy of the data and color after each swap
        color_data[i] = 'green'  # Mark current sorted element in green

    # After sorting completes, mark all elements as green
    for k in range(n):
        color_data[k] = 'green'
        yield data.copy(), color_data.copy()

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

def update_plot(frame, bars):
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

parser = argparse.ArgumentParser(description="Visualize Selection Sort Algorithm")
parser.add_argument('--size', type=int, default=30, help='Size of the array to generate')
parser.add_argument('--range', type=int, default=100, help='Range of values for the random array')
args = parser.parse_args()

# Validate and process arguments
if args.size <= 0:
    show_error("The size of the array must be a positive integer.")
    sys.exit(1)  # Exit the script
elif args.range <= 0:
    show_error("The range of values must be a positive integer.")
    sys.exit(1)  # Exit the script
else:
    data = [random.randint(1, args.range) for _ in range(args.size)]

# Initialize color data for the bars
color_data = ['blue'] * len(data)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_title('Selection Sort Visualization')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge', color=color_data)

# Generate frames for animation
frames = selection_sort(data, color_data)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=10)
plt.show()
