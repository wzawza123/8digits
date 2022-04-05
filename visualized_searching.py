from operator import truediv
from queue import PriorityQueue
from queue import Queue
import time
from my_searching import Tree, TreeNode
from visualization import *

class Solution:
    #空状态
    null_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #开始状态与目标状态
    Start_state = []
    Goal_state = []
    #将实际的状态映射到顺序状态
    Reflct_dict = {}
    #映射回实际的状态
    Restore_dict = {}
    
    def __init__(self,start:list[int],goal:list[int]):
        self.Start_state = start[:]
        self.Goal_state = goal[:]
        zero_pos = 0
        for i in range(9):
            if(goal[i] == 0):
                zero_pos = i
        for i in range(9):
            if(i<zero_pos):
                self.Reflct_dict[goal[i]] = i+1
                self.Restore_dict[i+1] = goal[i]
            if(i == zero_pos):
                self.Reflct_dict[goal[i]] = 0
                self.Restore_dict[0] = goal[i]
            if(i > zero_pos):
                self.Reflct_dict[goal[i]] = i
                self.Restore_dict[i] = goal[i]
        return

    #选择启发函数，默认状态下选择曼哈顿距离（第三个参数为空）作为启发函数
    #注意，此函数中，fun函数不可以带self参数
    def heuristic(self,cur_state, goal_state:list[int],fun):
        if fun == self.WrongTiles:
            return fun(cur_state,goal_state)
        if  fun == self.NetworkHeur:
            return fun()
        zero_pos = 0
        # 确定目标状态0的位置
        for i in range(9):
            if(goal_state[i] == 0):
                zero_pos = i
        return fun(cur_state,zero_pos)

    #启发函数1，采用曼哈顿距离
    def Manhattan(self,cur_state,zero_pos):
        cost = 0
        for i in range(9):
            if(cur_state[i] != 0):
                pos = cur_state[i]-1
                if(pos >= zero_pos):
                    pos += 1
                cost += abs(pos % 3 - i % 3) + abs(pos//3 - i//3)
        return cost

    #启发函数2，采用错误的片数
    def WrongTiles(self,cur_state,goal_state):
        num = 0;
        for i in range(9):
            if(cur_state[i]!= goal_state[i]):
                num = num + 1
        return num

    #启发函数3，采用网络返回值，当前恒返回0
    def NetworkHeur(self):
        return 0


    # 回溯函数，输出整体状态转移
    def BackTracking(self,close_list, final,output = False):
        TrackList = []
        cur = final
        while(True):
            state = self.Restore(cur[1])
            TrackList.insert(0, state)
            if(cur[0] == self.null_state):
                break
            cur = close_list[self.hash(cur[0])]

        if(output == True):
            for state in TrackList:
                print(state)

        return TrackList

    #用于close_dict的key
    def hash(self,state:list[int]):
        return "".join([str(x) for x in state])

    #判断问题的可解性
    def Resolvable(self,start_state: list[int] = Start_state[:], goal_state: list[int] = Goal_state[:]):
        start_num = 0
        for i in range(9):
            for j in range(0,i):
                if(start_state[j]>start_state[i] & start_state[i]!= 0):
                    start_num = start_num + 1
        goal_num = 0
        for i in range(9):
            for j in range(0,i):
                if(goal_state[j]>goal_state[i] & goal_state[i]!= 0):
                    goal_num = goal_num + 1
        return (goal_num % 2) == (start_num % 2)



    def Astar(self , fun = Manhattan,Display = False):
        #映射当前的状态
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()

        #initial the root node
        root = TreeNode(self.Restore(start_state),None)
        root.set_step(0)

        #initial lists
        Tracklist = []
        open_list = PriorityQueue()
        close_list = {}

        #计算root的启发函数
        hn = self.heuristic(start_state, goal_state,fun)
        root.set_fx(hn)
        # 存储前缀状态与当前状态,第二个元组的三个元素分别为前一状态，当前状态和fn
        open_list.put((0+hn,(self.null_state, start_state, 0,root)))
        #迭代次数
        iter = 0
        while(True):
            iter = iter + 1
            # 如果优先队列已空，寻找失败
            if(open_list.empty()):
                print('failure')
                break
            q = open_list.get()
            # 如果当前状态已经在close_list中，不再处理
            if(self.hash(q[1][1]) in close_list):
                continue
            close_list[self.hash(q[1][1])] = (q[1][0],q[1][1])
            # 如果是目标状态，进行回溯并输出状态转移
            if(q[1][1] == goal_state):
                Tracklist = self.BackTracking(close_list, q[1],Display)
                break
            # fn值等于之前的值加一
            fn = q[1][2] + 1
            cur_zero_pos = 0
            for i in range(9):
                if(q[1][1][i] == 0):
                    cur_zero_pos = i
                    break
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    hn = self.heuristic(nxt_state,  goal_state,fun)
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    new_node.set_fx(hn+fn)
                    open_list.put((fn+hn,(q[1][1], nxt_state, fn,new_node)))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    hn = self.heuristic(nxt_state,  goal_state,fun)
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    new_node.set_fx(hn+fn)
                    open_list.put((fn+hn,(q[1][1], nxt_state, fn,new_node)))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    hn = self.heuristic(nxt_state,  goal_state,fun)
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    new_node.set_fx(hn+fn)
                    open_list.put((fn+hn,(q[1][1], nxt_state, fn,new_node)))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    hn = self.heuristic(nxt_state,  goal_state,fun)
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    new_node.set_fx(hn+fn)
                    open_list.put((fn+hn,(q[1][1], nxt_state, fn,new_node)))
        end_time=time.time()
        
        return iter,(end_time-start_time),Tracklist,root

    def Greedy(self,Display = False):
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()


        #initial the root node
        root = TreeNode(self.Restore(start_state),None)
        root.set_step(0)

        Tracklist = []
        open_list = PriorityQueue()
        close_list = {}
        # 存储前缀状态与当前状态,第二个元组的三个元素分别为前一状态，当前状态和fn
        open_list.put((0,(self.null_state, start_state, 0, root)))
        #迭代次数
        iter = 0
        while(True):
            iter = iter + 1
            # 如果优先队列已空，寻找失败
            if(open_list.empty()):
                print('failure')
                break
            q = open_list.get()
            # 如果当前状态已经在close_list中，不再处理
            if(self.hash(q[1][1]) in close_list):
                continue
            close_list[self.hash(q[1][1])] = (q[1][0],q[1][1])
            # 如果是目标状态，进行回溯并输出状态转移
            if(q[1][1] == goal_state):
                Tracklist = self.BackTracking(close_list, q[1],Display)
                break
            # fn值等于之前的值加一
            fn = q[1][2] + 1
            cur_zero_pos = 0
            for i in range(9):
                if(q[1][1][i] == 0):
                    cur_zero_pos = i
                    break
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    #状态需要重新映射之后作为输出
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    open_list.put((fn,(q[1][1], nxt_state,fn,new_node)))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    open_list.put((fn,(q[1][1], nxt_state,fn,new_node)))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    open_list.put((fn,(q[1][1], nxt_state,fn,new_node)))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),q[1][3])
                    q[1][3].add_child(new_node)
                    new_node.set_step(q[1][3].get_step()+1)
                    open_list.put((fn,(q[1][1], nxt_state,fn,new_node)))
        end_time=time.time()
        return iter,(end_time-start_time),Tracklist,root

    def BFS(self,Display = False):


        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()


        #initial the root node
        root = TreeNode(self.Restore(start_state),None)
        root.set_step(0)

        iter = 0;
        Tracklist = []
        close_list = {}
        open_list = Queue()
        open_list.put((self.null_state,start_state,root))
        while(True):
            iter = iter + 1
            if(open_list.empty()):
                print('failure')
                break
            cur = open_list.get()
            if(self.hash(cur[1]) in close_list):
                continue
            close_list[self.hash(cur[1])] = (cur[0],cur[1])
            if(cur[1]==goal_state):
                Tracklist = self.BackTracking(close_list,cur,Display)
                break
            cur_zero_pos = 0
            for i in range(9):
                if(cur[1][i] == 0):
                    cur_zero_pos = i
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[2])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.put((cur[1],nxt_state,new_node))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.put((cur[1],nxt_state,new_node))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.put((cur[1],nxt_state,new_node))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.put((cur[1],nxt_state,new_node))
        end_time = time.time()
        return iter ,(end_time - start_time),Tracklist,root
    
    def DFS(self,Display = False):
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()
        iter = 0;

        #initial the root node
        root = TreeNode(self.Restore(start_state),None)
        root.set_step(0)

        open_list = [(self.null_state,start_state,root)]
        close_list = {}
        Tracklist = []
        while(True):
            iter = iter + 1
            if(open_list == []):
                print('failure')
                break
            cur = open_list[-1]
            open_list.pop()
            #Solution found
            if(cur[1] == goal_state):
                Tracklist = self.BackTracking(close_list,cur,Display)
                break
            if(self.hash(cur[1]) in close_list):
                continue
            close_list[self.hash(cur[1])] = (cur[0],cur[1])
            cur_zero_pos = 0
            for i in range(9):
                if(cur[1][i] == 0):
                    cur_zero_pos = i
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)                
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.append((cur[1],nxt_state,new_node))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)                
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.append((cur[1],nxt_state,new_node))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)                
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.append((cur[1],nxt_state,new_node))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hash_value = self.hash(nxt_state)                
                if(hash_value not in close_list):
                    new_node = TreeNode(self.Restore(nxt_state),cur[0])
                    cur[2].add_child(new_node)
                    new_node.set_step(cur[2].get_step()+1)
                    open_list.append((cur[1],nxt_state,new_node))
        end_time = time.time()

        return iter ,(end_time - start_time),Tracklist,root

    #正向与反向映射函数
    def Reflct(self,actullyGoal:list[int]):
        state = actullyGoal[:]
        for i in range(9):
            state[i] = self.Reflct_dict[actullyGoal[i]]
        return state

    def Restore(self,ReflectState:list[int]):
        state = ReflectState[:]
        for i in range(9):
            state[i] = self.Restore_dict[ReflectState[i]]
        return state

    def Display(self,root:TreeNode):
        #test whether root is a TreeNode
        assert isinstance(root,TreeNode)
        searching_tree=Tree(root,50,50)
        searching_tree.init_leaf_list()
        searching_tree.generate_node_position()
        searching_tree.generate_critical(self.Goal_state)
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
    #backtrack the treenode from the solution leaf, to marke the path as critical
    def BackTrackingTree(self,cur,root):
        while(cur!=root):
            cur.set_critical()
            cur = cur.get_parent()

# def main():
#     start = [1,2,3,8,4,5,7,6,0]
#     end = [1,2,3,8,0,4,7,6,5]
#     Tracklist = []
#     a = Solution(start,end)
#     if(a.Resolvable(start,end)):
#         iternum,cost,Tracklist,root = a.Astar(a.Manhattan)
#         print('A* Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
#         iternum,cost,Tracklist,root=a.Greedy()
#         print('Greedy Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
#         iternum,cost,Tracklist,root,=a.BFS(Display= True)
#         print('BFS Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
#         iternum,cost,Tracklist,root=a.DFS()
#         print('DFS Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
#         a.Display(root)
#     else:
#         print('no solution')
#     return
    
    
# main()
def main():
    start = [1,2,3,4,6,8,7,0,5]
    end = [1,2,3,4,5,6,7,8,0]
    Tracklist = []
    a = Solution(start,end)
    if(a.Resolvable(start,end)):
        iternum,cost,Tracklist,root = a.Astar(a.Manhattan)
        print('A* Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
        a.Display(root)
    else:
        print('no solution')
    return

if __name__ == '__main__':
    main()