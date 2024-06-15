import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse

# devide and conqer algo
# Divide: Split the array into two halves.
# Conquer: Recursively sort each half.
# Combine: Merge the two sorted halves to produce a single sorted array.
# recursively devide the array into subarrays until a single element is left in each subarray
# sort these subarrays from bottom to top and keep on comibining the sorted subarrays to reach towards the root of the final sorted array
# tc : bc , wc , ac : O(nlogn)

def merge(l, low, mid, high):
    i = low
    j = mid + 1
    k = low
    temp = [0]*len(l)

    while i <= mid and j <= high:
        if l[i] <= l[j]:
            temp[k] = l[i]
            i += 1
            k += 1
        else:
            temp[k] = l[j]
            j += 1
            k += 1

    while i <= mid:
        temp[k] = l[i]
        i += 1
        k += 1

    while j <= high:
        temp[k] = l[j]
        j += 1
        k += 1

    for i in range(low, high + 1):
        l[i] = temp[i]
    
    yield l.copy()

def merge_sort(l, low, high):
    if low < high:
        mid = (low + high) // 2
        yield from merge_sort(l, low, mid)
        yield from merge_sort(l, mid + 1, high)
        yield from merge(l, low, mid, high)
        yield l.copy()



def update_plot(frame, bars):
    data = frame
    for bar, val in zip(bars, data):          
        bar.set_height(val)

parser = argparse.ArgumentParser(description="Visualize Bubble Sort Algorithm")
parser.add_argument('--size', type=int, help='Size of the array to generate')
parser.add_argument('--range', type=int, help='Range of values for the random array')
args = parser.parse_args()

if args.size and args.range:
    data = [random.randint(1, args.range) for _ in range(args.size)]
else:
    data = [random.randint(1, 100) for _ in range(40)]


fig, ax = plt.subplots()
ax.set_title('Merge Sort')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_ylim(0, max(data) + 10)
bars = ax.bar(range(len(data)), data, align='edge')

# Generate frames for animation
frames = merge_sort(data, 0, len(data) - 1)

ani = animation.FuncAnimation(fig, update_plot, fargs=(bars,), frames=frames, repeat=False, interval=10)
plt.show()
