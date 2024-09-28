import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import messagebox
import sys

# Function to display an error message using tkinter
def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

# Function to parse comma-separated input strings
def parse_comma_separated(value):
    try:
        return [int(x) for x in value.strip('[]').split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid input: {value}. Expected a comma-separated list of integers.")

# SJF scheduling algorithm generator
# SJF scheduling algorithm generator
def sjf_scheduling(arrival_time, burst_time):
    p = len(arrival_time)
    processes = list(range(p))

    # Sorting based on arrival time and burst time
    for i in range(p):
        for j in range(p - 1):
            if arrival_time[j] > arrival_time[j + 1]:
                arrival_time[j], arrival_time[j + 1] = arrival_time[j + 1], arrival_time[j]
                burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]
                processes[j], processes[j + 1] = processes[j + 1], processes[j]

            if arrival_time[j] == arrival_time[j + 1]:
                if burst_time[j] > burst_time[j + 1]:
                    burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]
                    processes[j], processes[j + 1] = processes[j + 1], processes[j]

    # Initialization for completion time and start time
    comp_time = [0] * p
    start_time = [0] * p
    turn_around_time = [0] * p
    sum_time = 0
    visited = [False] * p

    if arrival_time[0] == 0:
        sum_time += burst_time[0]
    else:
        sum_time += arrival_time[0] + burst_time[0]

    comp_time[0] = sum_time
    start_time[0] = arrival_time[0]
    visited[0] = True

    # Iterate through each process
    for j in range(1, p):
        if arrival_time[j] > sum_time:
            sum_time = arrival_time[j]

        k = -1
        min_time = float('inf')

        for i in range(p):
            if not visited[i] and arrival_time[i] <= sum_time and burst_time[i] < min_time:
                k = i
                min_time = burst_time[i]

        if k != -1:
            start_time[k] = sum_time
            sum_time += burst_time[k]
            comp_time[k] = sum_time
            visited[k] = True
        
    gantt_data = []
        # Yield the state of the Gantt chart for visualization
    for i in range(p):

        gantt_data.append({'process': processes[i] + 1, 
                       'start_time': start_time[i], 
                       'burst_time': burst_time[i], 
                       'completion_time': comp_time[i],
                       'turn_around_time': comp_time[i]-arrival_time[i]} 
                )
                
        yield gantt_data.copy(), comp_time ,turn_around_time


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize SJF Scheduling Algorithm")
parser.add_argument('--arrival_time', type=parse_comma_separated, required=True, help='Comma-separated list of arrival times (e.g., "[0,2,4,6]")')
parser.add_argument('--burst_time', type=parse_comma_separated, required=True, help='Comma-separated list of burst times (e.g., "[5,3,8,6]")')
args = parser.parse_args()

# Validate arrival_time and burst_time inputs
if len(args.arrival_time) != len(args.burst_time):
    show_error("The number of arrival times and burst times must be the same.")
    sys.exit(1)  # Exit the script

arrival_time = args.arrival_time
burst_time = args.burst_time
processes = len(arrival_time)  # Number of processes is inferred from the length of the arrival_time list

print(f"Arrival Times: {arrival_time}")
print(f"Burst Times: {burst_time}")

# Initialize the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [3, 2, 2]})
ax1.set_title("SJF Scheduling Visualization")
ax1.set_xlabel("Processes")
ax1.set_ylabel("Time")

# Set up plot limits for the animation
ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Y-axis covers the total burst time
ax1.set_xlim(0, processes)  # X-axis covers the number of processes

# Define the update_plot function for animation
# Update the update_plot function for animation
colors = [
    'green', 'blue', 'orange', 'purple', 'red',
    'cyan', 'magenta', 'yellow', 'lightgreen', 'lightblue'
]
def update_plot(gantt_data):
    ax1.clear()  # Clear the current frame before adding new bars
    ax1.set_title("SJF Scheduling Visualization")
    ax1.set_xlabel("Processes")
    ax1.set_ylabel("Time")
    ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Reapply X and Y limits
    ax1.set_xlim(0, processes)

    # Unpack the gantt_data tuple
    gantt_data_list, completion_time,turn_around_time = gantt_data

    # Set bar width
    bar_width = 0.8  # Adjust the width as needed

    # Add vertical bars
    for process in gantt_data_list:
        ax1.bar(process['process'] - 1, process['burst_time'], 
               bottom=process['start_time'], 
               color=colors[(process['process'] - 1) % len(colors)], 
               edgecolor='black', 
               width=bar_width)  # Set the width of the bars
        ax1.text(process['process'] - 1, 
                process['start_time'] + process['burst_time'] / 2, 
                f"P{process['process']}",
                ha='left', 
                va='center', 
                color='white')

    # Process table (legend-like display)
    ax2.clear()  # Clear previous table
    ax2.axis('off')  # Hide axes for the table

    # Construct process info for the table using gantt_data_list for correct order
    process_info = [[f"P{process['process']}", 
                     arrival_time[process['process'] - 1],  # Access by process index
                     process['burst_time'], 
                     process['completion_time'] , process['turn_around_time']] for process in gantt_data_list]

    # Add final table
    table = ax2.table(cellText=process_info, 
                     colLabels=["P", "AT", "BT", "CT","TAT"],
                     cellLoc='center', 
                     loc='center', 
                     colColours=["lightblue"] * 5, 
                     bbox=[0, 0, 1, 1])
    
    # Adjust font size for the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size if needed

    # Gantt Chart on ax3
    ax3.clear()  # Clear previous frame
    ax3.set_title("Gantt Chart")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Processes")

    for process in gantt_data_list:
        ax3.barh(f"P{process['process']}", process['burst_time'], left=process['start_time'], 
                 color=colors[(process['process'] - 1) % len(colors)], edgecolor='black')
        ax3.text(process['start_time'] + process['burst_time'] / 2, f"P{process['process']}", 
                 f"P{process['process']}", va='center', ha='center', color='white')
        
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0")  # Set the position to (0,0) which is the top-left of the screen

    
    plt.tight_layout()



# Generate frames for the animation
frames = sjf_scheduling(arrival_time, burst_time)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, frames=frames, repeat=False, interval=1300)

# Display the plot
plt.show()
