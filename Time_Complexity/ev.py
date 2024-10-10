import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate values for vertices (V) and edges (E)
V = np.linspace(1, 100, 100)  # Values for vertices from 1 to 100
E = 2 * V  # Assuming the number of edges E is roughly twice the number of vertices

# Time complexity O(E * V)
complexity = E * V

# Create the figure for 3D plotting
fig = plt.figure(figsize=(10, 6), facecolor='black')  # Set figure size and background color
ax = fig.add_subplot(111, projection='3d')

# Plot E (x-axis), V (y-axis), and complexity (z-axis)
ax.plot(E, V, complexity, color='blue', marker='o', markersize=5, label='O(E * V)')

# Set axis labels and title
ax.set_title('3D Graph of O(E * V)', color='white')
ax.set_xlabel('Number of Edges (E)', color='white')
ax.set_ylabel('Number of Vertices (V)', color='white')
ax.set_zlabel('Time Complexity O(E * V)', color='white')

# Customize the plot background and grid
ax.set_facecolor('black')  # Set the background color for the plot
ax.xaxis.set_tick_params(colors='white')  # Set tick colors for x-axis
ax.yaxis.set_tick_params(colors='white')  # Set tick colors for y-axis
ax.zaxis.set_tick_params(colors='white')  # Set tick colors for z-axis

# Customize grid
ax.xaxis._axinfo['grid'].update(color='grey', linestyle='--', linewidth=0.5)  # Grey grid for x-axis
ax.yaxis._axinfo['grid'].update(color='grey', linestyle='--', linewidth=0.5)  # Grey grid for y-axis
ax.zaxis._axinfo['grid'].update(color='grey', linestyle='--', linewidth=0.5)  # Grey grid for z-axis

# Show the plot
plt.show()
