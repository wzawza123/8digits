#use this program to compare different searching methods
from Searching_newer import *
from matplotlib.pyplot import *
import random
import cProfile

#init random seed
random.seed(0)

def bfs_testing(test_times=100):
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.BFS()
        tot_iteration+=iternum
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("BFS: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times," tot_steps:",tot_steps,file=open("bfs_testing.txt","w"))
def dfs_testing(test_times=100):
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.DFS()
        tot_iteration+=iternum
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("DFS: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times,file=open("dfs_testing.txt","w"))

def a_star_manhattan_testing(test_times=100):
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.Astar(sol_class.Manhattan)
        tot_iteration+=iternum
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("A*_manhattan: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times," tot steps:",tot_steps,file=open("a_star_manhattan_testing.txt","w"))
def a_star_network_testing(test_times=100):
    start_state=[8,7,6,5,4,3,2,1,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.Astar(sol_class.NetworkHeur)
        tot_iteration+=iternum
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("A*_network: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times,file=open("a_star_network_testing.txt","w"))
def a_star_wrong_tiles(test_times=100):
    start_state=[8,7,6,5,4,3,2,1,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.Astar(sol_class.WrongTiles)
        tot_iteration+=iternum
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("A*_network: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times,file=open("a_star_wrong_tiles.txt","w"))
def greedy_testing(test_times=100):
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    ans_list=[]
    #create solution states
    sol_class=Solution(start_state,end_state)
    #create valuables to record the performance
    tot_iteration=0
    tot_steps=0
    tot_time_consumed=0
    for i in range(test_times):
        if(i%10==0):
            print("test times:",i)
        random.shuffle(start_state)
        while not sol_class.Resolvable(start_state,end_state):
            random.shuffle(start_state)
            sol_class.Start_state=start_state
        #start searching
        iternum,time_consumed,ans_list=sol_class.Greedy()
        tot_iteration+=iternum 
        tot_steps+=len(ans_list)
        tot_time_consumed+=time_consumed
    print("Greedy: average iterations:",tot_iteration/test_times," average steps:",tot_steps/test_times," average time consumed:",tot_time_consumed/test_times,file=open("greedy_testing.txt","w"))

def fixed_end_compare(test_times=200):
    #compare the performance of different algorithms
    # testing bfs
    bfs_testing(200)
    #testing a*_manhattan
    # a_star_manhattan_testing(test_times)
    # cProfile.run("a_star_network_testing(1)",filename="a_star_network_testing.txt")
    # a_star_network_testing(test_times)
    # greedy_testing(test_times)
    # a_star_wrong_tiles(test_times)
    # dfs_testing(10)
def main():
    fixed_end_compare()

if __name__ == '__main__':
    main()