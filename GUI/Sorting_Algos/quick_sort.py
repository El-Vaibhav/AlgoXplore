import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import sys
import tkinter as tk
from tkinter import messagebox

# Function to partition the array
def partition(l, low, high, color_data):
    pivot = l[low]
    color_data[low] = 'red'  # Mark pivot as red
    i = low + 1
    j = high

    yield l.copy(), color_data.copy()  # Show initial pivot selection

    while True:

        while i <= j and l[i] <= pivot:
            color_data[i] = 'brown'  # Show element i moving
            yield l.copy(), color_data.copy()
            i += 1
           
        while i <= j and l[j] > pivot:
            color_data[j] = 'yellow'  # Show element j moving
            yield l.copy(), color_data.copy()
            j -= 1
            
        if i <= j:
            l[i], l[j] = l[j], l[i]
            color_data[i] = 'cyan'  # Elements that are moved correctly
            color_data[j] = 'cyan'  # Elements that are moved correctly
            yield l.copy(), color_data.copy()
            color_data[i] = 'blue'  # Reset color after swap
            color_data[j] = 'blue'  # Reset color after swap
            yield l.copy(), color_data.copy()
        else:
            break

    l[low], l[j] = l[j], l[low]
    color_data[j] = 'green'  # Mark pivot's final position as green
    yield l.copy(), color_data.copy()

    # Reset pivot color if it's not at the final position
    for k in range(low, high + 1):
        if color_data[k] != 'green':
            color_data[k] = 'blue'

    return j

# Quick Sort recursive function
def quicksort(l, low, high, color_data):

    # The yield from expression is used to yield all values from another generator (or iterable) in a single statement. 
    # This is especially useful when you have a function that generates values, and you want to yield those values from another function.
    # quicksort is a generator function that is using yield from to call the partition function (which is also a generator). 
    # This makes the quicksort function yield all frames produced by partition, and then recursively yield frames from the subsequent recursive calls.
    
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
    plt.Rectangle((0, 0), 1, 1, color='yellow', label='Comparing with pivot from right side'),
    plt.Rectangle((0, 0), 1, 1, color='brown', label='Comparing with pivot from left side'),
    plt.Rectangle((0, 0), 1, 1, color='red', label='Pivot'),
    plt.Rectangle((0, 0), 1, 1, color='cyan', label='Swapping i and j pointers'),
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
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=400)
plt.show()
