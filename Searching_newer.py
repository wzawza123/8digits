from queue import PriorityQueue
from queue import Queue
import time

from numpy import intersect1d
from network.model_use import *

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
            return fun(cur_state,goal_state)
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
    def NetworkHeur(self,cur_state,goal_state):
        ans=GetNetWorkOutput(cur_state, goal_state)
        if ans<5:
            #the network is not so good with small numbers
            for i in range(9):
                if(goal_state[i] == 0):
                    zero_pos = i
                    break
            return self.Manhattan(cur_state, zero_pos)
        return ans


    # 回溯函数，输出整体状态转移
    def BackTracking(self,close_list, final):
        TrackList = []
        cur = final
        while(True):
            state = self.Restore(cur[1])
            TrackList.insert(0, state)
            if(cur[0] == self.null_state):
                break
            cur = close_list[self.hash(cur[0])]
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



    def Astar(self , fun = Manhattan):
        #映射当前的状态
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()
        zero_pos = 0
        # 确定目标状态0的位置
        for i in range(9):
            if(goal_state[i] == 0):
                zero_pos = i

        Tracklist = []
        open_list = PriorityQueue()
        close_list = {}
        # 存储前缀状态与当前状态,第二个元组的三个元素分别为前一状态，当前状态和fn
        open_list.put((0+self.heuristic(start_state, goal_state,fun),
                      (self.null_state, start_state, 0)))
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
                Tracklist = self.BackTracking(close_list, q[1])
                break
            # fn值等于之前的值加一
            fn = q[1][2] + 1
            cur_zero_pos = 0
            for i in range(9):
                if(q[1][1][i] == 0):
                    cur_zero_pos = i
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hn = self.heuristic(nxt_state,  goal_state,fun)
                open_list.put((fn+hn,(q[1][1], nxt_state, fn)))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hn = self.heuristic(nxt_state,  goal_state,fun)
                open_list.put((fn+hn,(q[1][1], nxt_state, fn)))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hn = self.heuristic(nxt_state,  goal_state,fun)
                open_list.put((fn+hn,(q[1][1], nxt_state, fn)))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                hn = self.heuristic(nxt_state,  goal_state,fun)
                open_list.put((fn+hn,(q[1][1], nxt_state, fn)))
        end_time=time.time()
        return iter,(end_time-start_time),Tracklist

    def Greedy(self):
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()
        zero_pos = 0
        # 确定目标状态0的位置
        for i in range(9):
            if(goal_state[i] == 0):
                zero_pos = i
        Tracklist = []
        open_list = PriorityQueue()
        close_list = {}
        # 存储前缀状态与当前状态,第二个元组的三个元素分别为前一状态，当前状态和fn
        open_list.put((0,(self.null_state, start_state, 0)))
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
                Tracklist = self.BackTracking(close_list, q[1])
                break
            # fn值等于之前的值加一
            fn = q[1][2] + 1
            cur_zero_pos = 0
            for i in range(9):
                if(q[1][1][i] == 0):
                    cur_zero_pos = i
            # 判断可能的下一状态
            if(cur_zero_pos - 3 > 0):
                changepos = cur_zero_pos - 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((fn,(q[1][1], nxt_state, fn)))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((fn,(q[1][1], nxt_state, fn)))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((fn,(q[1][1], nxt_state, fn)))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = q[1][1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((fn,(q[1][1], nxt_state, fn)))
        end_time=time.time()
        return iter,(end_time-start_time),Tracklist

    def BFS(self):
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()
        iter = 0;
        Tracklist = []
        close_list = {}
        open_list = Queue()
        open_list.put((self.null_state,start_state))
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
                Tracklist = self.BackTracking(close_list,cur)
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
                open_list.put((cur[1],nxt_state))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((cur[1],nxt_state))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((cur[1],nxt_state))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.put((cur[1],nxt_state))
        end_time = time.time()

        return iter ,(end_time - start_time),Tracklist
    
    def DFS(self):
        start_state = self.Reflct(self.Start_state)
        goal_state = self.Reflct(self.Goal_state)
        start_time = time.time()
        iter = 0;
        open_list = [(self.null_state,start_state)]
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
                Tracklist = self.BackTracking(close_list,cur)
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
                open_list.append((cur[1],nxt_state))
            if(cur_zero_pos + 3 < 9):
                changepos = cur_zero_pos + 3
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.append((cur[1],nxt_state))
            if((cur_zero_pos + 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos + 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.append((cur[1],nxt_state))
            if((cur_zero_pos - 1) // 3 == cur_zero_pos // 3):
                changepos = cur_zero_pos - 1
                nxt_state = cur[1][:]
                nxt_state[cur_zero_pos] = nxt_state[changepos]
                nxt_state[changepos] = 0
                open_list.append((cur[1],nxt_state))
        end_time = time.time()

        return iter ,(end_time - start_time),Tracklist

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



def main():
    start = [8,7,6,5,4,3,2,1,0]
    end = [1,2,3,4,5,6,7,8,0]
    Tracklist = []
    a = Solution(start,end)
    if(a.Resolvable(start,end)):
        iternum,cost,Tracklist = a.Astar(a.NetworkHeur)
        print('A* Network Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
        iternum,cost,Tracklist=a.Greedy()
        print('Greedy Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
        iternum,cost,Tracklistr=a.BFS()
        print('BFS Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
        iternum,cost,Tracklist=a.DFS()
        print('DFS Alrithmetic\niteration:%i \ntime cost:%05f' %(iternum,cost))
    else:
        print('no solution')
    return
    
    
if __name__ == '__main__':
    main()
