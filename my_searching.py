'''
Description: use the bfs to solve the 8 puzzle problem
Date: 2022-04-04 18:55:34
LastEditTime: 2022-04-04 23:00:59
'''
import random
import queue
import numpy as np
import pygame
from visualization import *

#define the tree node size
TREE_BOARD_SIZE=20
#define the max layer of the tree
TREE_MAX_LAYER=33
#define the layout parameters
TREE_LAYER_DISTANCE=100
TREE_NODE_DISTANCE=100
valid_move={0:[1,3],1:[0,2,4],2:[1,5],3:[0,4,6],4:[1,3,5,7],5:[2,4,8],6:[3,7],7:[4,6,8],8:[5,7]}

class TreeNode:
    def __init__(self,state,parent):
        self.state=state
        self.parent=parent
        self.step=0
        self.board=Board(0,0,TREE_BOARD_SIZE,BOARD_BG_COLOR,state)
        self.children=[]
    def display(self,screen):
        self.board.display(screen)
    def add_child(self,child):
        self.children.append(child)
        # pass
    def set_step(self,step):
        self.step=step
    def set_state(self,state):
        self.state=state
    def set_position(self,x,y):
        self.board.setPosition(x,y)
    def get_position(self):
        return self.board.getPosition()
    def get_middle_up(self):
        return self.board.getTopMiddle()
    def get_middle_bottom(self):
        return self.board.getBottomMiddle()
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent
    def get_state(self):
        return self.state
    def get_step(self):
        return self.step
    
class Tree:
    def __init__(self,root,x=0,y=0):
        self.root=root
        self.x=x
        self.y=y
        self.leaf_list=[[] for i in range(TREE_MAX_LAYER+1)]
        self.max_layer=0
    #use the bfs to initialize the leaf list of every layer
    def init_leaf_list(self):
        q=queue.Queue()
        q.put(self.root)
        while not q.empty():
            node=q.get()
            if node.get_step()<TREE_MAX_LAYER:
                self.leaf_list[node.get_step()].append(node)
                self.max_layer=max(self.max_layer,node.get_step())
            for child in node.get_children():
                q.put(child)
    #use the data in leafe list to set the node position
    def generate_node_position(self,mode=0):
        for i in range(len(self.leaf_list)):
            for j in range(len(self.leaf_list[i])):
                self.leaf_list[i][j].set_position(self.x+TREE_NODE_DISTANCE*j,self.y+TREE_LAYER_DISTANCE*i)
    #draw the tree
    def draw_tree(self,screen):
        #draw the node
        for i in range(len(self.leaf_list)):
            for j in range(len(self.leaf_list[i])):
                self.leaf_list[i][j].display(screen)
        #draw the branch
        for i in range(len(self.leaf_list)-1):
            for j in range(len(self.leaf_list[i])):
                for child in self.leaf_list[i][j].get_children():
                    pygame.draw.line(screen,BRANCH_COLOR,self.leaf_list[i][j].get_middle_bottom(),child.get_middle_up())
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
                #whether new is target
                if new_state==end_state:
                    return root


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
    start_state=[1,2,3,7,4,6,0,5,8]
    end_state=[1,2,3,4,5,6,7,8,0]
    root=bfs_search_solution(start_state,end_state)
    bfs_travel(root)
    searching_tree=Tree(root,50,50)
    searching_tree.init_leaf_list()
    searching_tree.generate_node_position()
    #init pygame window
    pygame.init()
    screen=pygame.display.set_mode((1280,840))
    pygame.display.set_caption("8 puzzle searching tree")
    isRunning=True
    #main loop
    while isRunning:
        #process the events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                isRunning=False
        #draw the background
        screen.fill((64,64,64))
        searching_tree.draw_tree(screen)
        # root.display(screen)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
    # vis_test()