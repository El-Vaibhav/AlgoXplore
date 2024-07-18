import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import tkinter as tk
from tkinter import messagebox
import sys

# Bubble sort algorithm with color updates
def bubble_sort(data, color_data):
    n = len(data)
    for i in range(n):
        for j in range(n - 1 - i):
            color_data[j] = 'purple'  # Mark the elements being compared
            yield data.copy(), color_data.copy()
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                color_data[j], color_data[j + 1] = 'red', 'red'  # Mark swapped elements
                yield data.copy(), color_data.copy()
            color_data[j], color_data[j + 1] = 'blue', 'blue'  # Reset to default color
        color_data[n - 1 - i] = 'green'  # Mark the last sorted element
        yield data.copy(), color_data.copy()  # Yield to update the visualization
    for k in range(n):
        color_data[k] = 'green'  # Mark all elements as sorted
    yield data.copy(), color_data.copy()  # Final yield to show all elements in green

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, default=10, help='Size of the array to generate')
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

# Function to update the plot
def update_plot(frame, bars):
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_ylim(0, max(data) + 10)
ax.set_title("Bubble Sort Visualization")
bars = ax.bar(range(len(data)), data, align='edge', color='blue')

# Define color legend annotations using handles
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
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=900)
plt.show()
