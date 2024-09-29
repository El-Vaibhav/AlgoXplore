# tc = o(n^2)

# adv : minimises waiting time

# disadv: we need to know all the future refrences 


p = int(input("Enter the number of processes: "))

burst_time = []

print("Enter the burst time of all processes: ")

for i in range(p):
    burst_time.append(int(input()))

arrival_time = []

print("Enter the arrival time of processes: ")

for i in range(p):
    arrival_time.append(int(input()))

for i in range(p):
    for j in range(p - 1):
        if arrival_time[j] > arrival_time[j + 1]:
            arrival_time[j], arrival_time[j + 1] = arrival_time[j + 1], arrival_time[j]
            burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]

        if arrival_time[j] == arrival_time[j + 1]:
            if burst_time[j] > burst_time[j + 1]:
                burst_time[j], burst_time[j + 1] = burst_time[j + 1], burst_time[j]

comp_time = [0] * p
comp_time[0] = 0

sum_time = 0

visited = [False] * p

if arrival_time[0] == 0:
    sum_time += burst_time[0]
else:
    sum_time += arrival_time[0] + burst_time[0]

comp_time[0] = sum_time
visited[0] = True

for j in range(1, p):
    if arrival_time[j] > sum_time:
        sum_time = arrival_time[j]

    k = 0
    min_time = 10000

    for i in range(p):
        if not visited[i] and arrival_time[i] <= sum_time and burst_time[i] < min_time:
            k = i
            min_time = burst_time[i]

    sum_time += min_time
    comp_time[j] = sum_time
    visited[k] = True

print("Gantt Chart:")
for i in range(p):
    print(comp_time[i], end=" ")

print("\n")

wt_time = 0
tat = 0

for k in range(p):
    wt_time += (comp_time[k] - burst_time[k] - arrival_time[k])
    tat += comp_time[k] - arrival_time[k]

print("Average waiting time:", wt_time / p)
print("Average Turn Around Time:", tat / p)
