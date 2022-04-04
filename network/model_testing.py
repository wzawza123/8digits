import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from reader import *
import time
import matplotlib.pyplot as plt

def input_number_list(prompt):
    print(prompt)
    number_list = []
    number_list = list(map(int, input().split(" ")))
    return number_list
    

model=load_model(".\\models\\model_enhanced_small.h5")
print("reading data...")
start_forward_time=time.time()
x,y=readData(".\\data\\data_full.txt")
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