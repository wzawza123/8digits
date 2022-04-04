#this program is used to train the model basing on the data

import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from reader import *

def input_number_list(prompt):
    print(prompt)
    number_list = []
    number_list = list(map(int, input().split(" ")))
    return number_list

#read data
x,y = readData("data_selected_shuffle_enhanced.txt")


#create model
model = keras.Sequential([
    layers.Flatten(input_shape=(9,9)),
    layers.Dense(162, activation='relu'),
    layers.Dense(162, activation='relu'),
    layers.Dense(1)
])

model.summary()

model.compile(optimizer='adam',loss='mse',metrics=['mae'])

model.fit(x,y,epochs=400)

model.save('model.h5')
y_pred=model.predict(x)
print(y_pred)
while True:
    x_in=input_number_list("Please input the number list:")
    x_in_array=state_list_to_one_hot(x_in)
    x_in_array=np.array(x_in_array)
    x_in_array=x_in_array.reshape(1,9,9)
    print(model.predict(x_in_array))
# print(y_pred.shape)
