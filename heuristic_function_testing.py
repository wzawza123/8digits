'''
Description: test the model with the actuall data
Date: 2022-04-04 21:02:18
LastEditTime: 2022-04-07 20:30:20
'''
from cProfile import label
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from network.reader import *
import time
import matplotlib.pyplot as plt
from Searching_newer import *

def input_number_list(prompt):
    print(prompt)
    number_list = []
    number_list = list(map(int, input().split(" ")))
    return number_list
    

def heuristic_function_testing(algorithm="manhattan"):
    x,y=readData(".\\network\\data\\data_full.txt","list")
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,5,6,7,8,0]
    solClass=Solution(start_state,end_state)
    tot_error=0
    ans=[]
    for i in range(len(x)):
        if(i%100==0):
            print(i)
        if(algorithm=="manhattan"):
            ans.append(solClass.heuristic(solClass.Reflct(x[i]),solClass.Reflct(end_state),solClass.Manhattan))
        elif algorithm=="wrong_tiles":
            ans.append(solClass.heuristic(solClass.Reflct(x[i]),solClass.Reflct(end_state),solClass.WrongTiles))
        elif algorithm=="network":
            ans.append(solClass.heuristic(solClass.Reflct(x[i]),solClass.Reflct(end_state),solClass.NetworkHeur))
        tot_error+=abs(ans[i]-y[i])
    plt.scatter(y,ans,c="red",s=4,label=algorithm)
    plt.plot(y,y,c="blue",label="real cost",linewidth=1,linestyle="--")
    # plt.scatter(range(len(x)),y,c="blue",s=2,label="real")
    plt.xlabel("real")
    plt.ylabel("predict")
    plt.legend()
    plt.show()
    print("average error:",tot_error/len(x))
    # print(solClass.heuristic(start,end,solClass.Manhattan))

def network_testing():
    model=load_model(".\\network\\models\\model_enhanced_small.h5")
    print("reading data...")
    start_forward_time=time.time()
    x,y=readData(".\\network\\data\\data_full.txt")
    #test the time of forwarding
    print("forwarding...")
    y_pred=model.predict(x)
    end_forward_time=time.time()

    print(y)
    #calculate the average error between y and y_pred
    error=0
    detailed_error=[0 for i in range(y.max()+1)]
    detailed_cnt=[0 for i in range(y.max()+1)]
    print("max=",y.max()+1)
    for i in range(len(y)):
        if i%100==0:
            print(i)
        error+=abs(y[i]-y_pred[i])[0]
        detailed_error[y[i]]+=abs(y[i]-y_pred[i])[0]
        detailed_cnt[y[i]]+=1
    error=error/len(y)
    for i in range(y.max()+1):
        detailed_error[i]=detailed_error[i]/detailed_cnt[i]
    # print(detailed_error)
    #show detailed error of detail_error
    plt.scatter(range(y.max()+1),detailed_error)
    plt.xlabel("steps")
    plt.ylabel("error")
    plt.show()

    print("average error:",error)
    print("total forwarding time:",end_forward_time-start_forward_time)
    print("total samples:",len(x))
    print("avearage forwarding time:",(end_forward_time-start_forward_time)/len(x))

    while True:
        x_in=input_number_list("Please input the number list:")
        x_in_array=state_list_to_one_hot(x_in)
        x_in_array=np.array(x_in_array)
        x_in_array=x_in_array.reshape(1,9,9)
        print(model.predict(x_in_array))

if __name__=="__main__":
    # network_testing()
    heuristic_function_testing("network")