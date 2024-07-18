import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Divide and conquer algorithm (Merge Sort)
# Divide: Split the array into two halves.
# Conquer: Recursively sort each half.
# Combine: Merge the two sorted halves to produce a single sorted array.
# Recursively divide the array into subarrays until a single element is left in each subarray
# Sort these subarrays from bottom to top and keep on combining the sorted subarrays to reach toward the root of the final sorted array
# Time Complexity: O(n log n) for the best, average, and worst case

def merge(l, low, mid, high, color_data):
    i = low
    j = mid + 1
    k = low
    temp = [0] * len(l)

    while i <= mid and j <= high:
        color_data[i], color_data[j] = 'purple', 'purple'  # Mark elements being compared
        yield l.copy(), color_data.copy()
        if l[i] <= l[j]:
            temp[k] = l[i]
            color_data[k] = 'red'  # Mark element being merged
            i += 1
        else:
            temp[k] = l[j]
            color_data[k] = 'red'  # Mark element being merged
            j += 1
        k += 1
        yield l.copy(), color_data.copy()

    while i <= mid:
        temp[k] = l[i]
        color_data[k] = 'red'  # Mark element being merged
        i += 1
        k += 1
        yield l.copy(), color_data.copy()

    while j <= high:
        temp[k] = l[j]
        color_data[k] = 'red'  # Mark element being merged
        j += 1
        k += 1
        yield l.copy(), color_data.copy()

    for i in range(low, high + 1):
        l[i] = temp[i]
        color_data[i] = 'green'  # Mark elements as sorted
        yield l.copy(), color_data.copy()

def merge_sort(l, low, high, color_data):
    if low < high:
        mid = (low + high) // 2
        yield from merge_sort(l, low, mid, color_data)
        yield from merge_sort(l, mid + 1, high, color_data)
        yield from merge(l, low, mid, high, color_data)
        yield l.copy(), color_data.copy()

# Function to update the plot
def update_plot(frame, bars):
    data, color_data = frame
    for bar, val, color in zip(bars, data, color_data):
        bar.set_height(val)
        bar.set_color(color)

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Merge Sort Algorithm")
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
ax.set_title('Merge Sort Visualization')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge', color='blue', width=0.6)

# Define color legend annotations
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color='purple', label='Comparing'),
    plt.Rectangle((0, 0), 1, 1, color='red', label='Merging'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='Sorted'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='Unsorted')
]

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Generate frames for animation
frames = merge_sort(data, 0, len(data) - 1, color_data)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=400)
plt.show()
