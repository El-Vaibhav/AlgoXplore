import numpy as np
import matplotlib.pyplot as plt

# Generate values for n
n = np.linspace(1, 100, 100)  # Values from 1 to 100
log_n = np.log(n)  # Compute logarithm (base e)

# Create the plot
plt.figure(figsize=(8, 6), facecolor='black')  # Set figure size and background color

# Plot O(log n)
plt.plot(n, log_n, color='blue', linewidth=2, marker='o', markersize=5)  # Blue line with markers

# Customize the plot
plt.title('Graph of O(log(n))', color='white')  # Title color
plt.xlabel('n', color='white')  # X-axis label color
plt.ylabel('O(log(n))', color='white')  # Y-axis label color
plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Customize grid
plt.tick_params(colors='white')  # Ticks color
plt.gca().set_facecolor('black')  # Set plot background color

manager = plt.get_current_fig_manager()
try:
    manager.window.wm_geometry("+50+100")  # Far left position
except AttributeError:
    pass  # For systems that don't support this
# Show the plot
# Show the plot
plt.show()
