
p = ["P1","P2","P3","P4","P5"]

ans={}

a_t = [0,5,12,2,9]

priority=[2,4,1,3,0]

b_t=[11,28,2,10,16]

p, a_t, priority, b_t = zip(*sorted(zip(p, a_t, priority, b_t), key=lambda x: (x[1], x[2], x[3])))

curr_time=a_t[0]

visited=set()

while len(ans)!=len(p):
 
    max_pri = float('-inf')

    for i in range(len(p)):

        if a_t[i] <= curr_time and p[i] not in visited:
            max_pri = max(max_pri,priority[i])
    
    for i in range(len(p)):

        if a_t[i] <=curr_time and priority[i] == max_pri and p[i] not in visited:
            curr_time += b_t[i]
            ans[p[i]] = curr_time
            visited.add(p[i])
            print(ans)
        else:
            curr_time+=1 # if no process can be selected cpu will remain idle

print(ans)


  








