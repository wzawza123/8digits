'''
Description: use the bfs to solve the 8 puzzle problem
Date: 2022-04-04 18:55:34
LastEditTime: 2022-04-04 20:33:09
'''
import random
import queue
import numpy as np
from visualization import *

valid_move={0:[1,3],1:[0,2,4],2:[1,5],3:[0,4,6],4:[1,3,5,7],5:[2,4,8],6:[3,7],7:[4,6,8],8:[5,7]}

class TreeNode:
    def __init__(self,state,parent):
        self.state=state
        self.parent=parent
        self.children=[]
        self.step=0
        self.board=Board(state,)
    def add_child(self,child):
        self.children.append(child)
    def set_step(self,step):
        self.step=step
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent
    def get_state(self):
        return self.state
    def get_step(self):
        return self.step

#transform the state list into integer
def state_list_to_integer(state_list):
    ans=0
    for i in range(9):
        ans=ans*10+state_list[i]
    return ans


def bfs_search_solution(start_state,end_state):
    root=TreeNode(start_state,None)
    q=queue.Queue()
    q.put(root)
    vis_set={}
    vis_set[state_list_to_integer(start_state)]=0
    root.set_step(0)
    while not q.empty():
        node=q.get()
        print(node.get_state(),node.get_step())
        if node.get_state()==end_state:
            return root
        for i in range(9):
            if node.get_state()[i]==0:
                zero_loc=i
                break
        for move in valid_move[zero_loc]:
            new_state=node.get_state().copy()
            new_state[zero_loc]=new_state[move]
            new_state[move]=0
            hash_value=state_list_to_integer(new_state)
            if hash_value not in vis_set:
                vis_set[hash_value]=node.get_step()+1
                new_node=TreeNode(new_state,node)
                node.add_child(new_node)
                new_node.set_step(node.get_step()+1)
                q.put(new_node)


#travel the tree to display
def bfs_travel(root):
    print("==========================================================")
    q=queue.Queue()
    q.put(root)
    while not q.empty():
        node=q.get()
        print(node.get_state(),node.get_step())
        for child in node.get_children():
            q.put(child)

def main():
    start_state=[1,2,3,4,5,6,7,8,0]
    end_state=[1,2,3,4,0,5,7,8,6]
    root=bfs_search_solution(start_state,end_state)
    bfs_travel(root)

if __name__ == '__main__':
    main()