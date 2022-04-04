#use this program to explore the 8-puzzle problem
from Searching import *
import random
import numpy

TEST_TIME=200

if __name__ == "__main__":
    start=[1,2,3,4,5,6,7,8,0]
    goal=[0,1,2,3,4,5,6,7,8]
    s=Solution(start, goal)
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
        s.BFS(start, goal)
        tot_steps+=len(s.answer_list)
        # print(tot_steps)
    
    
    print("average steps:", tot_steps/TEST_TIME)