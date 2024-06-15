import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse

# devide and conquer algo
# Choose a Pivot:
# Select an element from the array to act as a pivot.
# Partitioning:
# Rearrange the array such that all elements less than the pivot come before it, and all elements greater than the pivot come after it. The pivot is now in its correct position in the sorted array.
# recursively this is done for all left and right subarrays wrt to that pivot element
# in quick sort all work is done in devide step

# tc : bc = ac = o(nlogn) partitioning in n/2 and n/2 (balanced partition)
#      wc = o(n^2) partitioning in n-1 and 1 ( unbalanced partition)


def partition(l, low, high):
    pivot = l[low]
    i = low + 1
    j = high

    while True:
        while i <= j and l[i] <= pivot:
            i += 1
        while i <= j and l[j] > pivot:
            j -= 1
        if i <= j:
            l[i], l[j] = l[j], l[i]
        else:
            break

    l[low], l[j] = l[j], l[low]
    return j

def quicksort(l, low, high):
    if low < high:
        pi = partition(l, low, high)
        yield l.copy()  # Yield a copy of the list after each partition
        yield from quicksort(l, low, pi - 1)
        yield from quicksort(l, pi + 1, high)

parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, help='Size of the array to generate')
parser.add_argument('--range', type=int, help='Range of values for the random array')
args = parser.parse_args()

if args.size and args.range:
    data = [random.randint(1, args.range) for _ in range(args.size)]
else:
    data = [random.randint(1, 100) for _ in range(40)]

def update_plot(frame, bars):
    data = frame
    for bar, val in zip(bars, data):          
        bar.set_height(val)


fig, ax = plt.subplots()
ax.set_title('Quick Sort')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge')

# Generate frames for animation
frames = quicksort(data, 0, len(data) - 1)

ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=10)
plt.show()
