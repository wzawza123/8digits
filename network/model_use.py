import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from network.reader import *
import time
import matplotlib.pyplot as plt

tf.compat.v1.disable_eager_execution()

def input_number_list(prompt):
    print(prompt)
    number_list = []
    number_list = list(map(int, input().split(" ")))
    return number_list
    

model=load_model(".\\network\models\model_enhanced_small.h5")
print("model loaded successfully")

#the goal_state is fixed to [1,2,3,4,5,6,7,8,0]
def GetNetWorkOutput(x_in,goal_state):
    x_in_array=state_list_to_one_hot(x_in)
    x_in_array=np.array(x_in_array)
    x_in_array=x_in_array.reshape(1,9,9)
    return (model.predict(x_in_array)[0][0])