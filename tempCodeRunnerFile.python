from random import randint
from copy import deepcopy
from random import randint
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np

WT = 0
TT = 0

class _PreemptivePriorityScheduling: # Class for simulating Preemptive Priority CPU Scheduling
    process_list = [] # List to Store the Processes [PID, AT, BT, RT, PL,CT]
    fourColumnProcessList = []
        
    def inputRandom(self, no_of_processes, max_BT): # RANDOM INPUT
        half = no_of_processes // 2 
        randomizer_limit = no_of_processes + half # Randomizer limit is 150% of the Number of Processes
        
        for process_id in range(1, no_of_processes + 1): # Loop to enter random values for each process
            temporary = [] 

            while True:
                arrival_time = randint(0, randomizer_limit)
                
                if [pr for pr in self.process_list if pr[1] == arrival_time]:
                    pass
                else:
                    break

            burst_time = randint(1, max_BT)
            
            remaining_time = deepcopy(burst_time)

            priority_level = randint(1, no_of_processes)
            
            completion_time = 0

            temporary = [f"P{process_id}", arrival_time, burst_time, remaining_time, priority_level, completion_time]

            
            self.process_list.append(temporary)
            self.fourColumnProcessList.append([f"P{process_id}", arrival_time, burst_time, priority_level])


        return self.fourColumnProcessList
        
    def schedulingProcess(self): # Scheduling Algorithm
        current_time = 0 # Current Time Frame
        completed_list = [] # List for completed processes
        ready_queue = [] # Memory Queue
         # this is a 2 dimensional array in which [0] is the process name [1] service time [2] execution stop time
        cur_process_data = {}
        flag = True
        temp = None
        counter = 0
        while len(completed_list) < len(self.process_list): # Loop for the Algorithm
            for process in self.process_list:
                if process[1] <= current_time and process not in completed_list and process not in ready_queue: # Inserting newly arrived processes to the Memory Queue
                    ready_queue.append(process)
            
           
            if not ready_queue: # Checking for idle time
                current_time += 1
                continue # Skip rest of the algorithm if idle time
            
            ready_queue.sort(key=lambda x: x[4]) # Sorting the ready queue based on Priority Level
            
            current_process = ready_queue[0] # Set current process as process with highest level in memory queue
            current_process[3] -= 1 # Decerement current process bust time
            if flag:
                cur_process_data[counter] = []
                cur_process_data[counter].append(current_process[0])
                cur_process_data[counter].append(current_time)
                temp = current_process[0]
                flag = False
            elif temp != current_process[0]:
                counter += 1
                cur_process_data[counter-1].append(current_time)
                flag = True
            
            if current_process[3] == 0: # Check if process is Completed
                completed_list.append(current_process) # Append current process to completed list
                ready_queue.pop(0) # Remove current process from ready queue
                current_process[5] = current_time + 1 # Set completion time for current process
            
            current_time += 1 # Increment Current Time Frame

        last_process = list(cur_process_data.keys())[-1]
        cur_process_data[last_process].append(current_time)
        # Initialize Totals of TT and WT
        total_wt = 0
        total_tt = 0
        
        for process in self.process_list: # Loop to calculate WT and TT of each rocess
            turnaround_time = process[5] - process[1] # Calculate TT of process (Completion Time - Arrival Time)
            waiting_time = turnaround_time - process[2] # Calculate WT of process (Turnaround Time - Burst Time)
            
            total_wt += waiting_time # Add TT of the process to the total
            total_tt += turnaround_time # Add WT of the process to the total
        
        global TT
        global WT
        # Compute Averages
        TT = total_wt / len(self.process_list)
        WT = total_tt / len(self.process_list)
        
        return cur_process_data

    def plot_gantt_chart(self, cur_process_data):
        fig, gnt = plt.subplots()
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Processes')

        try:
            colors = plt.cm.viridis(np.linspace(0, 1, len(cur_process_data)))

            for i, (key, value) in enumerate(cur_process_data.items()):
                process_name = value[0]
                start_time = value[1]
                end_time = value[2]

                # Use a different color for each process
                color = colors[i]
                gnt.broken_barh([(start_time, end_time - start_time)], (0, 1), facecolors=(color))

                # Add process labels
                gnt.text(start_time + 1, 1, process_name, verticalalignment='center', horizontalalignment='center', color='black')

            plt.savefig("./GANTT_OUTPUT/GTChart.png", bbox_inches='tight', dpi=100)
        except:
            plt.savefig("./GANTT_OUTPUT/GTChart.png", bbox_inches='tight', dpi=100)

# Main Machinery
def runner(process_list):
    proseso = _PreemptivePriorityScheduling() # Create instance
    cur = proseso.schedulingProcess() # Run Scheduling Algotihm
    proseso.plot_gantt_chart(cur)