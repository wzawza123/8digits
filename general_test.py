'''
Description: 
Date: 2022-04-04 21:02:18
LastEditTime: 2022-04-05 10:21:50
'''
#use this program to explore the 8-puzzle problem
from Searching_newer import *
import random
import numpy
import matplotlib.pyplot as plt

TEST_TIME=300

if __name__ == "__main__":
    start=[1,2,3,4,5,6,7,8,0]
    goal=[0,1,2,3,4,5,6,7,8]
    s=Solution(start, goal)
    step_list=[0 for i in range(33)]
    faliure=0
    tot_steps=0
    for i in range(TEST_TIME):
        if i%10==0:
            print(i)
        #generate random start and goal
        random.shuffle(start)
        random.shuffle(goal)
        while s.Resolvable(start, goal)==None:
            random.shuffle(start)
            random.shuffle(goal)
        s.Start_state=start
        s.Goal_state=goal
        iter,time_consumed,anslist=s.BFS()
        if len(anslist)==0:
            faliure=faliure+1
            continue
        tot_steps+=len(anslist)
        step_list[len(anslist)]+=1
        # print(tot_steps)
    
    #draw the scatter of step list
    plt.scatter(range(len(step_list)),step_list)
    plt.show()
    print("average steps:", tot_steps/(TEST_TIME-faliure))