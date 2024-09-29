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

# Priority Scheduling (Non-Preemptive) algorithm generator using the new priority logic
def priority_scheduling(arrival_time, burst_time, priority):
    p = ["P"+str(i+1) for i in range(len(arrival_time))]
    
    # Sort based on arrival time, priority, and burst time
    p, arrival_time, priority, burst_time = zip(*sorted(zip(p, arrival_time, priority, burst_time), key=lambda x: (x[1], x[2], x[3])))
    
    curr_time = 0
    ans = {}
    visited = set()

    while len(ans) != len(p):
        max_pri = float('-inf')
        check=1
        
        for i in range(len(p)):
            if arrival_time[i] <= curr_time and p[i] not in visited:
                max_pri = max(max_pri, priority[i])

        for i in range(len(p)):
            if arrival_time[i] <= curr_time and priority[i] == max_pri and p[i] not in visited:
                curr_time += burst_time[i]
                ans[p[i]] = curr_time
                visited.add(p[i])
                check=0
                break

        if check:
            curr_time+=1

    # Completion time and start time logic
    comp_time = [ans[proc] for proc in p]
    start_time = [comp_time[i] - burst_time[i] for i in range(len(p))]
    gantt_data = []

    # Yield the state of the Gantt chart for visualization
    for i in range(len(p)):
        gantt_data.append({
            'process': int(p[i][1:]),  # Extract process number
            'start_time': start_time[i],
            'burst_time': burst_time[i],
            'completion_time': comp_time[i],
            'turn_around_time': comp_time[i] - arrival_time[i],
            'priority': priority[i],  # Add priority to the gantt_data
        })
        yield gantt_data.copy(), comp_time, start_time


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Priority Scheduling Algorithm")
parser.add_argument('--arrival_time', type=parse_comma_separated, required=True, help='Comma-separated list of arrival times (e.g., "[0,2,4,6]")')
parser.add_argument('--burst_time', type=parse_comma_separated, required=True, help='Comma-separated list of burst times (e.g., "[5,3,8,6]")')
parser.add_argument('--priority', type=parse_comma_separated, required=True, help='Comma-separated list of priorities (e.g., "[1,2,3,4]")')
args = parser.parse_args()

# Validate arrival_time, burst_time, and priority inputs
if len(args.arrival_time) != len(args.burst_time) or len(args.burst_time) != len(args.priority):
    show_error("The number of arrival times, burst times, and priorities must be the same.")
    sys.exit(1)  # Exit the script

arrival_time = args.arrival_time
burst_time = args.burst_time
priority = args.priority
processes = len(arrival_time)  # Number of processes is inferred from the length of the arrival_time list

print(f"Arrival Times: {arrival_time}")
print(f"Burst Times: {burst_time}")
print(f"Priorities: {priority}")

# Initialize the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), gridspec_kw={'height_ratios': [3, 2, 2]})
ax1.set_title("Priority Scheduling Visualization")
ax1.set_xlabel("Processes")
ax1.set_ylabel("Time")

# Set up plot limits for the animation
ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Y-axis covers the total burst time
ax1.set_xlim(0, processes)  # X-axis covers the number of processes

colors = [
    'green', 'blue', 'orange', 'purple', 'red',
    'cyan', 'magenta', 'yellow', 'lightgreen', 'lightblue'
]

# Define the update_plot function for animation
def update_plot(gantt_data):
    ax1.clear()  # Clear the current frame before adding new bars
    ax1.set_title("Priority Scheduling Visualization")
    ax1.set_xlabel("Processes")
    ax1.set_ylabel("Time")
    ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Reapply X and Y limits
    ax1.set_xlim(0, processes)

    # Unpack the gantt_data tuple
    gantt_data_list, completion_time, start_time = gantt_data

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
                     process['completion_time'], 
                     process['turn_around_time'],
                     process['priority']]  # Add priority to the process info
                     for process in gantt_data_list]

    # Add final table
    table = ax2.table(cellText=process_info,
                     colLabels=["P", "AT", "BT", "CT", "TAT", "Priority"],  # Add Priority column
                     cellLoc='center',
                     loc='center',
                     colColours=["lightblue"] * 6,  # Change length to 6
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
frames = priority_scheduling(arrival_time, burst_time, priority)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, frames=frames, repeat=False, interval=1300)

# Display the plot
plt.show()
