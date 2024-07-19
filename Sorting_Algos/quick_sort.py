import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import sys
import tkinter as tk
from tkinter import messagebox

# Quick Sort Algorithm
# Choose a Pivot:
# Select an element from the array to act as a pivot.
# Partitioning:
# Rearrange the array such that all elements less than the pivot come before it,
# and all elements greater than the pivot come after it. The pivot is now in its
# correct position in the sorted array.
# Recursively apply Quick Sort to the left and right subarrays around the pivot.

# Time Complexity:
#   - Best Case (Balanced Partition): O(n log n)
#   - Average Case: O(n log n)
#   - Worst Case (Unbalanced Partition): O(n^2)

# Function to partition the array
def partition(l, low, high, color_data):
    pivot = l[high]
    color_data[high] = 'red'  # Mark pivot as red
    i = low - 1

    yield l.copy(), color_data.copy()  # Show initial pivot selection

    for j in range(low, high):
        color_data[j] = 'yellow'  # Mark elements being compared
        yield l.copy(), color_data.copy()

        if l[j] < pivot:
            i += 1
            l[i], l[j] = l[j], l[i]
            color_data[i] = 'cyan'  # Elements that are moved correctly
            yield l.copy(), color_data.copy()

        color_data[j] = 'blue'  # Reset color after comparison

    l[i + 1], l[high] = l[high], l[i + 1]
    color_data[i + 1] = 'green'  # Mark pivot's final position as green
    yield l.copy(), color_data.copy()

    # Reset pivot color if it's not at the final position
    for k in range(low, high + 1):
        if color_data[k] != 'green':
            color_data[k] = 'blue'

    return i + 1

# Quick Sort recursive function
def quicksort(l, low, high, color_data):
    if low < high:
        pi = yield from partition(l, low, high, color_data)
        yield from quicksort(l, low, pi - 1, color_data)
        yield from quicksort(l, pi + 1, high, color_data)

    # Mark entire array as sorted (green) after sorting is complete
    if low == 0 and high == len(l) - 1:
        for i in range(len(l)):
            color_data[i] = 'green'
            yield l.copy(), color_data.copy()

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Quick Sort Algorithm")
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
ax.set_title('Quick Sort Visualization')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge', color=color_data)

# Define color legend annotations
legend_handles = [
    plt.Rectangle((1, 1), 0, 1, color='yellow', label='Comparing with pivot'),
    plt.Rectangle((0, 0), 1, 1, color='red', label='Pivot'),
    plt.Rectangle((0, 0), 1, 1, color='cyan', label='Correct Partition relative to pivot'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='Sorted'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='Unsorted')
]

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Function to update the plot with each frame
def update_plot(frame, bars):
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

# Generate frames for animation
frames = quicksort(data, 0, len(data) - 1, color_data)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=300)
plt.show()
