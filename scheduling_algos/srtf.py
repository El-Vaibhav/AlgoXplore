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

# SRTF scheduling algorithm generator (SJF with preemption)
def srtf_scheduling(arrival_time, burst_time):
    p = len(arrival_time)
    remaining_burst = burst_time[:]
    comp_time = [0] * p
    start_time = [None] * p
    visited = [False] * p
    sum_time = 0
    gantt_data = []
    
    completed = 0
    while completed < p:
        # Find the process with the shortest remaining burst time that's arrived
        min_burst = float('inf')
        current_process = -1
        for i in range(p):
            if arrival_time[i] <= sum_time and remaining_burst[i] < min_burst and remaining_burst[i] > 0:
                min_burst = remaining_burst[i]
                current_process = i
        
        if current_process == -1:
            sum_time += 1  # If no process is found, increment time
            continue

        if start_time[current_process] is None:
            start_time[current_process] = sum_time  # Log the start time if it's the first time executing the process

        # Execute the current process for one unit of time
        remaining_burst[current_process] -= 1
        sum_time += 1
        
        # If process completes
        if remaining_burst[current_process] == 0:
            comp_time[current_process] = sum_time
            visited[current_process] = True
            completed += 1

        # Yield the current state of the Gantt chart for visualization
        gantt_data.append({'process': current_process + 1, 
                           'start_time': sum_time - 1, 
                           'burst_time': 1, 
                           'completion_time': comp_time[current_process] if remaining_burst[current_process] == 0 else None})

        yield gantt_data.copy(), comp_time

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize SRTF Scheduling Algorithm")
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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 6), gridspec_kw={'width_ratios': [3, 2]})
ax1.set_title("SRTF Scheduling Visualization")
ax1.set_xlabel("Processes")
ax1.set_ylabel("Time")

# Set up plot limits for the animation
ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Y-axis covers the total burst time
ax1.set_xlim(0, processes)  # X-axis covers the number of processes

# Define the update_plot function for animation
def update_plot(gantt_data):
    ax1.clear()  # Clear the current frame before adding new bars
    ax1.set_title("SRTF Scheduling Visualization")
    ax1.set_xlabel("Processes")
    ax1.set_ylabel("Time")
    ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Reapply X and Y limits
    ax1.set_xlim(0, processes)

    # Unpack the gantt_data tuple
    gantt_data_list, completion_time = gantt_data

    # Set bar width
    bar_width = 0.8  # Adjust the width as needed

    # Add vertical bars
    for process in gantt_data_list:
        ax1.bar(process['process'] - 1, process['burst_time'], 
                bottom=process['start_time'], 
                color='green', 
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
                     burst_time[process['process'] - 1], 
                     completion_time[process['process'] - 1]] for process in gantt_data_list if completion_time[process['process'] - 1] is not None]

    # Add final table
    table = ax2.table(cellText=process_info, 
                      colLabels=["P", "AT", "BT", "CT"],
                      cellLoc='center', 
                      loc='center', 
                      colColours=["lightblue"] * 4, 
                      bbox=[0, 0, 1, 1])
    
    # Adjust font size for the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size if needed
    
    plt.tight_layout()

# Generate frames for the animation
frames = srtf_scheduling(arrival_time, burst_time)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, frames=frames, repeat=False, interval=1300)

# Display the plot
plt.show()
