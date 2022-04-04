#this program can generate the data of 8 digits with given start states
import numpy as np
import queue

start_state=[1,2,3,4,5,6,7,8,0]
valid_move={0:[1,3],1:[0,2,4],2:[1,5],3:[0,4,6],4:[1,3,5,7],5:[2,4,8],6:[3,7],7:[4,6,8],8:[5,7]}

vis_set={}

#function for state list to state array
def state_list_to_array(state_list):
    state_list=np.array(state_list)
    state_array=state_list.reshape(3,3)
    return state_array
def state_array_to_list(state_array):
    state_array=np.array(state_array)
    state_list=state_array.reshape(9)
    return state_list
#hash the state list of the data into a unique number
def state_list_to_integer(state_list):
    ans=0
    for i in range(9):
        ans=ans*10+state_list[i]
    return ans

#save the data into a file
def saveData(file_name):
    f=open(file_name,'w')
    for i in vis_set:
        f.write(str(i)+' '+str(vis_set[i])+'\n')
    f.close()

#generate data with given size
def dataGenerate(size=100):
    state_cnt=1
    #using bfs to generate the data
    q=queue.Queue()
    q.put(start_state)
    vis_set[state_list_to_integer(start_state)]=0
    while not q.empty():
        state=q.get()
        hash_cur=state_list_to_integer(state)
        print(state,vis_set.get(hash_cur))
        
        for i in range(9):
            if state[i]==0:
                zero_loc=i
                break
        for move in valid_move[zero_loc]:
            new_state=state.copy()
            new_state[zero_loc]=new_state[move]
            new_state[move]=0
            if np.sum(new_state==start_state)==9:
                print("find the start state")
                print(state_cnt)
                return
            hash_value=state_list_to_integer(new_state)
            if hash_value not in vis_set:
                vis_set[hash_value]=vis_set[hash_cur]+1
                q.put(new_state)
                state_cnt+=1
                if state_cnt>=size:
                    return

if __name__=='__main__':
    #generate the data
    dataGenerate(200000)
    saveData(file_name='data.txt')