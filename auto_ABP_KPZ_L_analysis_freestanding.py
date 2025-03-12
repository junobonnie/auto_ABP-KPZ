from multiprocessing import Pool
import os
import sys
import numpy as np

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
time_cut = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[4]) #시뮬레이션 횟수

def main(i):
    os.system('pypy3 ABP_KPZ_L_analysis_freestanding.py %d %d %03d %d'%(width, height, i, time_cut))

if __name__=='__main__':
    if num == 50:
        num_list = [10, 10, 10, 10, 10]
    elif num == 100:
        num_list = [33,33,34]
    elif num == 500:
        num_list = [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34]
    elif num < 30:
        num_list = [num]
    end_num = 0
    for num in num_list:
        pool = Pool(num)
        pool.map(main, [i for i in range(end_num+1, end_num+num+1)])
        pool.close()
        end_num += num

    time = list(range(0, 100010, 20000))
    #time = list(range(100, 510, 100))
    #time = list(range(10000, 20010, 1000))
    for t in time:
        if t > time_cut:
            break

        LWs = []
        for i in range(1, sum(num_list)+1):
            with open('snapshots/' + str(width) + 'x' + str(height) + "/%03d/%d_LW.txt"%(i, t), "r") as f:
                LW_ = f.readlines()
                LW_ = [float(lw_) for lw_ in LW_]
                LWs.append(LW_)

        LWs = np.array(LWs)
        LW = np.mean(LWs, axis=0)
        std_LW = np.std(LWs, axis=0)
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_LW.txt"%(t), "w") as f:
            for lw in LW:
                f.write(str(lw)+"\n")
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_std_LW.txt"%(t), "w") as f:
            for std_lw in std_LW:
                f.write(str(std_lw)+"\n")
        
        LWs_1 = []
        for i in range(1, sum(num_list)+1):
            with open('snapshots/' + str(width) + 'x' + str(height) + "/%03d/%d_LW1.txt"%(i, t), "r") as f:
                LW_1 = f.readlines()
                LW_1 = [float(lw_1) for lw_1 in LW_1]
                LWs_1.append(LW_1)

        LWs_1 = np.array(LWs_1)
        LW_1 = np.mean(LWs_1, axis=0)
        std_LW_1 = np.std(LWs_1, axis=0)
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_LW1.txt"%(t), "w") as f:
            for lw_1 in LW_1:
                f.write(str(lw_1)+"\n")
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_std_LW1.txt"%(t), "w") as f:
            for std_lw_1 in std_LW_1:
                f.write(str(std_lw_1)+"\n")

        LWs_2 = []
        for i in range(1, sum(num_list)+1):
            with open('snapshots/' + str(width) + 'x' + str(height) + "/%03d/%d_LW2.txt"%(i, t), "r") as f:
                LW_2 = f.readlines()
                LW_2 = [float(lw_2) for lw_2 in LW_2]
                LWs_2.append(LW_2)

        LWs_2 = np.array(LWs_2)
        LW_2 = np.mean(LWs_2, axis=0)
        std_LW_2 = np.std(LWs_2, axis=0)
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_LW2.txt"%(t), "w") as f:
            for lw_2 in LW_2:
                f.write(str(lw_2)+"\n")
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%d_std_LW2.txt"%(t), "w") as f:
            for std_lw_2 in std_LW_2:
                f.write(str(std_lw_2)+"\n")


    

