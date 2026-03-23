import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import tkinter as tk
from tkinter import messagebox
import sys


# Selection Sort Algorithm
# The algorithm divides the input list into two parts: the sublist of items already sorted,
# which is built up from left to right at the front (left) of the list, and the sublist
# of items remaining to be sorted that occupy the rest of the list.
# Initially, the sorted sublist is empty and the unsorted sublist is the entire input list.
# The algorithm proceeds by finding the smallest (or largest, depending on sorting order)
# element from the unsorted sublist, swapping it with the leftmost unsorted element,
# and moving the sublist boundaries one element to the right.

# Time Complexity: O(n^2) for the best, average, and worst case

def selection_sort(data, color_data):
    n = len(data)
    for i in range(n - 1):
        min_index = i
        color_data[min_index] = 'yellow'  # Mark the initial minimum element
        yield data.copy(), color_data.copy()
        
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                if min_index != i:
                    color_data[min_index] = 'blue'  # Reset previous minimum
                min_index = j
                color_data[min_index] = 'yellow'  # Mark new minimum candidate
            yield data.copy(), color_data.copy()

        if min_index != i:
            data[i], data[min_index] = data[min_index], data[i]
            color_data[i], color_data[min_index] = 'red', 'red'  # Mark swapped elements
            yield data.copy(), color_data.copy()
            color_data[i], color_data[min_index] = 'green', 'blue'  # Finalize the sorted element

        color_data[i] = 'green'  # Mark as sorted
        yield data.copy(), color_data.copy()

    # Mark the last element as sorted
    color_data[n - 1] = 'green'
    yield data.copy(), color_data.copy()

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Function to update the plot
def update_plot(frame, bars):
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Selection Sort Algorithm")
parser.add_argument('--size', type=int, default=20, help='Size of the array to generate')
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

# Define color legend annotations
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color='yellow', label='Current Minimum'),
    plt.Rectangle((0, 0), 1, 1, color='red', label='Swapped Elements'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='Sorted Elements'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='Unsorted Elements')
]

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Generate frames for animation
frames = selection_sort(data, color_data)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=200)
plt.show()
