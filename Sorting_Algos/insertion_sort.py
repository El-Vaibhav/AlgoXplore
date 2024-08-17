import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import sys
import tkinter as tk
from tkinter import messagebox

# Insertion sort is a simple and intuitive sorting algorithm. It builds the final sorted array one element at a time.
# Start with the Second Element:
# The first element of the array is considered sorted. The sorting process begins with the second element.
# Insert Each Element into the Sorted Portion:
# For each element in the unsorted portion of the array, find its correct position in the sorted portion and insert it there.
# This involves comparing the element to the elements in the sorted portion and shifting elements to the right to make room for the inserted element.
# Repeat the process for each subsequent element until the entire array is sorted.

# Time complexity: 
# Best case: O(n) - the array is already sorted.
# Worst case and average case: O(n^2) - the array is sorted in reverse order.

def insertion_sort(data, color_data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            color_data[j + 1] = 'red'  # Highlight comparison
            yield data.copy(), color_data.copy()
            color_data[j + 1] = 'green'  # set color of sorted element
            j -= 1
        data[j + 1] = key
        color_data[j + 1] = 'green'  # Mark as sorted
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
parser = argparse.ArgumentParser(description="Visualize Insertion Sort Algorithm")
parser.add_argument('--size', type=int, default=15, help='Size of the array to generate')
parser.add_argument('--range', type=int, default=100, help='Range of values for the random array')
args = parser.parse_args()

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

fig, ax = plt.subplots()
ax.set_ylim(0, max(data) + 10)
ax.set_title("Insertion Sort Visualization")
bars = ax.bar(range(len(data)), data, align='edge', color='blue', width=0.6)

# Define color legend annotations using handles
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color='red', label='Comparing with sorted array'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='Inserted at correct position'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='Unsorted'),
    plt.Rectangle((0, 0), 1, 1, color='brown', label='Sorted')
]

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Generate frames for animation
frames = insertion_sort(data, color_data)

ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=480)
plt.show()
