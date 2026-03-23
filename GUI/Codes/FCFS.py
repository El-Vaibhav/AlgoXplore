
# adv: simple , no need to know about the future refrences

# disdv : convoy effect if brst time more in start it cause a lot of wt for next process 

# tc = o(n^2) , n=no. of process
p=eval(input("Enter the number of process"))


burst_time=[]

print("Enter the burst time of all process: ")

for i in range(p):
    burst_time.append(eval(input()))

arrival_time=[]

print("Enter the arrival time of all process ")

for i in range(p):

    arrival_time.append(eval(input()))

# sorting according to arrival time

for i in range(p):

    for j in range(p-1):

        if i!=j and arrival_time[j]>arrival_time[j+1]:

           
            arrival_time[j] , arrival_time[j+1] = arrival_time[j+1] ,  arrival_time[j]
          

            burst_time[j] , burst_time[j+1] = burst_time[j+1] , burst_time[j]
           

comp_time = []

sum=arrival_time[0]

for i in range(p):
    sum+=burst_time[i]

    comp_time.append(sum)

print("Gantt chart:")

for i in comp_time:
    print(i, end=" ")

print("\n")
wt=0
tat=0

for i in range(p):
    wt+= comp_time[i]-burst_time[i]-arrival_time[i]
    tat+=comp_time[i]-arrival_time[i]

print("Average Waiting time:" , wt/p)


print("Average Turn around time:" , tat/p)





    
