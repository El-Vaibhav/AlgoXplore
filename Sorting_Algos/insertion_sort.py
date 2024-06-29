import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import sys
import tkinter as tk
from tkinter import messagebox

# Insertion sort algorithm

# Insertion sort is a simple and intuitive sorting algorithm. It builds the final sorted array one element at a time. Here’s a step-by-step explanation of how it works:
# Start with the Second Element:
# The first element of the array is considered sorted. The sorting process begins with the second element.
# Insert Each Element into the Sorted Portion:
# For each element in the unsorted portion of the array, find its correct position in the sorted portion and insert it there.
# This involves comparing the element to the elements in the sorted portion and shifting elements to the right to make room for the inserted element.
# Repeat the process for each subsequent element until the entire array is sorted.

# we one by one make the sorted array from left , start from 2nd element insert it to its sorted pos in left , then go to 3 rd element insert it in its sorted position in left ( with 1st and 2nd element) and go on doing this ....

# tc: bc : O(n) , array is sorted
#     wc , ac : O(n^2) wc when array is sorted in reverse order

def insertion_sort(data):

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
            yield data.copy()  # Yield a copy of the data after each swap
        data[j + 1] = key
        yield data.copy()  # Yield after placing the key

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()



def update_plot(frame, bars):
    data = frame
    for bar, val in zip(bars, data):
        bar.set_height(val)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, help='Size of the array to generate')
parser.add_argument('--range', type=int, help='Range of values for the random array')
args = parser.parse_args()

if args.size is not None and args.range is not None:
    if args.size <= 0:
        show_error("The size of the array must be a positive integer.")
        sys.exit(1)  # Exit the script
    elif args.range <= 0:
        show_error("The range of values must be a positive integer.")
        sys.exit(1)  # Exit the script
    else:
        data = [random.randint(1, args.range) for _ in range(args.size)]
else:
    show_error("Both --size and --range arguments must be provided.")
    sys.exit(1)  # Exit the script


fig, ax = plt.subplots()
ax.set_title('Insertion Sort')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge')

# Generate frames for animation
frames = insertion_sort(data)

ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=10)
plt.show()
