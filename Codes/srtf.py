# SRTF scheduling algorithm (SJF with preemption)
def srtf_scheduling(arrival_time, burst_time):
    p = len(arrival_time)
    remaining_burst = burst_time[:]
    comp_time = [0] * p
    start_time = [None] * p
    visited = [False] * p
    sum_time = 0
    completed = 0
    gantt_data = []
    
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

        # Store the Gantt chart data
        gantt_data.append({'process': current_process + 1, 
                           'start_time': sum_time - 1, 
                           'burst_time': 1, 
                           'completion_time': comp_time[current_process] if remaining_burst[current_process] == 0 else None})

    # Print the Gantt chart and completion times
    print("\nGantt Chart:")
    for process in gantt_data:
        print(f"Process P{process['process']}: Start Time = {process['start_time']}, Burst Time = {process['burst_time']}")

    print("\nCompletion Times:")
    for i in range(p):
        print(f"Process P{i+1}: Completion Time = {comp_time[i]}")

# Input
arrival_time = list(map(int, input("Enter the arrival times (comma-separated): ").split(',')))
burst_time = list(map(int, input("Enter the burst times (comma-separated): ").split(',')))

# Validate input
if len(arrival_time) != len(burst_time):
    print("Error: The number of arrival times and burst times must be the same.")
else:
    # Run the SRTF scheduling algorithm
    srtf_scheduling(arrival_time, burst_time)
