#this program is to visualize the testing result
import matplotlib.pyplot as plt
import numpy as np


def main():
    algorithms=["GREEDY","BFS","DFS","MANHATTAN","WRONG","NETWORK"]
    average_iterations=[182617.81,217526.66,94295.9,1891.06,26830.93,322.0]
    average_steps=[24.75,25.06, 50340.0,23.6,24.66,25.69]
    average_time=[2.7479917669296263,2.307027590274811,17.138290095329285,0.050763657093048094,0.4626274514198303,0.46960781335830687]
    time_per_iterations=[0,0,0,0,0,0]
    for i in range(len(algorithms)):
        time_per_iterations[i]=average_time[i]/average_iterations[i]
    
    # plt.bar(algorithms,average_iterations,color="blue",label="average iterations")
    #show average_time
    plt.xlabel("Algorithms")
    # plt.ylabel("Average Time(s)")
    # plt.bar(algorithms,average_time,color="red",label="average time")
    #show time_per_iterations
    # plt.bar(algorithms,time_per_iterations,color="green",label="time per iteration")
    # plt.yscale("log")
    #show average step except dfs
    algorithms.pop(2)
    average_steps.pop(2)
    plt.bar(algorithms,average_steps,color="green",label="average steps")
    plt.legend()
    plt.show()

if __name__=="__main__":
    main()