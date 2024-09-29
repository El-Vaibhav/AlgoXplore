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

# Round Robin scheduling algorithm
def round_robin_scheduling(arrival_time, burst_time, time_quantum=2):
    n = len(arrival_time)
    proc = [[arrival_time[i], burst_time[i], burst_time[i], 0] for i in range(n)]  # [arrival, burst, remaining_time, flag]
    
    completion_time = [0] * n
    turn_around = [0] * n
    wait_time = [0] * n
    gantt_data = []
    
    total_time_counted = 0
    total_time = sum(burst_time)
    
    while total_time > 0:
        for i in range(n):
            if proc[i][2] > 0:
                if proc[i][2] <= time_quantum:
                    total_time_counted += proc[i][2]
                    total_time -= proc[i][2]
                    proc[i][2] = 0
                    proc[i][3] = 1  # Mark process as complete
                else:
                    proc[i][2] -= time_quantum
                    total_time -= time_quantum
                    total_time_counted += time_quantum

                if proc[i][2] == 0 and proc[i][3] == 1:
                    completion_time[i] = total_time_counted
                    turn_around[i] = completion_time[i] - proc[i][0]
                    wait_time[i] = turn_around[i] - proc[i][1]
                
                gantt_data.append({
                    'process': i + 1,
                    'start_time': total_time_counted - time_quantum if proc[i][2] != 0 else total_time_counted - (time_quantum + proc[i][2]),
                    'burst_time': proc[i][1] - proc[i][2],  # How much burst time was consumed
                    'completion_time': total_time_counted,
                })
    
    # After computing, yield the data one process at a time
    for i in range(len(gantt_data)):
        yield gantt_data[:i + 1], turn_around, completion_time

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize Round Robin Scheduling Algorithm")
parser.add_argument('--arrival_time', type=parse_comma_separated, default="[0, 1, 2, 3]", help='Comma-separated list of arrival times (e.g., "[0,1,2,3]")')
parser.add_argument('--burst_time', type=parse_comma_separated, default="[5, 4, 3, 2]", help='Comma-separated list of burst times (e.g., "[5,4,3,2]")')
parser.add_argument('--time_quantum', type=parse_comma_separated, default="2", help='Time quantum (e.g., 2)')
args = parser.parse_args()

arrival_time = args.arrival_time
burst_time = args.burst_time
time_quant = int(args.time_quantum[0])

processes = len(arrival_time)

print(f"Arrival Times: {arrival_time}")
print(f"Burst Times: {burst_time}")

# Initialize the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), gridspec_kw={'height_ratios': [3, 2, 2]})
ax1.set_title("Round Robin Scheduling Visualization")
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
    ax1.set_title("Round Robin Scheduling Visualization")
    ax1.set_xlabel("Processes")
    ax1.set_ylabel("Time")
    ax1.set_ylim(0, sum(burst_time) + max(arrival_time))  # Reapply X and Y limits
    ax1.set_xlim(0, processes)

    # Unpack the gantt_data tuple
    gantt_data_list, turn_around_time, completion_time = gantt_data

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
    
    # Add final table
    process_info = [[f"P{p+1}", arrival_time[p], burst_time[p], completion_time[p], turn_around_time[p]] 
                    for p in range(processes)]
    
    table = ax2.table(cellText=process_info, 
                     colLabels=["P", "AT", "BT", "CT", "TAT"],
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
frames = round_robin_scheduling(arrival_time, burst_time, time_quant)

# Create animation
ani = animation.FuncAnimation(fig, update_plot, frames=frames, repeat=False, interval=1300)

# Display the plot
plt.show()
