import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Bubble sort algorithm
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(n-1-i):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                yield data.copy()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, help='Size of the array to generate')
parser.add_argument('--range', type=int, help='Range of values for the random array')
args = parser.parse_args()

if args.size and args.range:
    data = [random.randint(1, args.range) for _ in range(args.size)]
else:
    data = [random.randint(1, 100) for _ in range(40)]

# Function to update the plot
def update_plot(frame, bars):
    for bar, val in zip(bars, frame):
        bar.set_height(val)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_title('Bubble Sort')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge')

# Generate frames for animation
frames = bubble_sort(data)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=1)
plt.show()
