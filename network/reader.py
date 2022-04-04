#this program read the genreated data into list
import numpy as np
import queue

# transform integer to state list
def integer_to_list(integer):
    state_list=[0]*9
    for i in range(8,-1,-1):
        state_list[i]=integer%10
        integer=integer//10
    return state_list

#transform state list into one-hot vector
def state_list_to_one_hot(state_list):
    ans=np.zeros((9,9))
    state_list=np.array(state_list)
    for p in range(9):
        ans[p][state_list[p]]=1
    return ans
def readData(file_name,output=False):
    f=open(file_name,'r')
    x=[]
    y=[]
    for line in f:
        line=line.split(" ")
        single_list=integer_to_list(int(line[0]))
        # print(single_list)
        x.append(state_list_to_one_hot(single_list))
        y.append(int(line[1]))
        
    f.close()
    x=np.array(x)
    y=np.array(y)
    return x,y

if __name__=="__main__":
    x,y=readData("data.txt")
    print(x)
    print("==========================================================")
    print(y)
