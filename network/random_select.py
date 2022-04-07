'''
Description: random select the data for training
Date: 2022-04-04 21:02:18
LastEditTime: 2022-04-07 21:32:25
'''
#this program can random select some lines in the file, and write them into a new file
import random
import numpy as np
import queue

#this function can random select some lines in a file and write them into a new file
# not so good for the lines with large steps are too much
def random_select(file_name,output_file_name,ratio=0.1):
    f=open(file_name,'r')
    f_out=open(output_file_name,'w')
    for line in f:
        if random.random()<ratio:
            f_out.write(line)
    f.close()
    f_out.close()

#states with small steps are more likely to be selected
def random_select_enhanced(file_name,output_file_name,ratio=0.1):
    f=open(file_name,'r')
    f_out=open(output_file_name,'w')
    for line in f:
        line=line.split(" ")
        current_step=int(line[1])
        if current_step<=10:
            f_out.write(line)
        else:
            if random.random()<ratio:
                f_out.write(line)
    f.close()
    f_out.close()

#this function can shuffle the lines in a file

def random_shuffle(file_name,output_file_name):
    f=open(file_name,'r')
    f_out=open(output_file_name,'w')
    lines=f.readlines()
    random.shuffle(lines)
    for line in lines:
        f_out.write(line)
    f.close()
    f_out.close()

if __name__=="__main__":
    random_select("data_full.txt","data_selected_enhanced.txt",0.2)
    random_shuffle("data_selected_enhanced.txt","data_selected_shuffle_enhanced.txt")