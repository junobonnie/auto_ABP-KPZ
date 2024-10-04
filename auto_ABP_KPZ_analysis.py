from multiprocessing import Pool
import os
import sys
import numpy as np

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
time_cut = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[4]) #시뮬레이션 횟수

def main(i):
    os.system('pypy3 ABP_KPZ_analysis.py %d %d %03d %d'%(width, height, i, time_cut))

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

    Ws = []
    for i in range(1, sum(num_list)+1):
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%03d/W.txt"%(i), "r") as f:
            W_ = f.readlines()
            W_ = [float(w_) for w_ in W_]
            Ws.append(W_)

    Ws = np.array(Ws)
    W = np.mean(Ws, axis=0)
    std_W = np.std(Ws, axis=0)
    with open('snapshots/' + str(width) + 'x' + str(height) + "/W.txt", "w") as f:
        for w in W:
            f.write(str(w)+"\n")
    with open('snapshots/' + str(width) + 'x' + str(height) + "/std_W.txt", "w") as f:
        for std_w in std_W:
            f.write(str(std_w)+"\n")

    
    Hs = []
    for i in range(1, sum(num_list)+1):
        with open('snapshots/' + str(width) + 'x' + str(height) + "/%03d/H.txt"%(i), "r") as f:
            H_ = f.readlines()
            H_ = [float(h_) for h_ in H_]
            Hs.append(H_)

    Hs = np.array(Hs)
    H = np.mean(Hs, axis=0)
    std_H = np.std(Hs, axis=0)
    with open('snapshots/' + str(width) + 'x' + str(height) + "/H.txt", "w") as f:
        for h in H:
            f.write(str(h)+"\n")
    with open('snapshots/' + str(width) + 'x' + str(height) + "/std_H.txt", "w") as f:
        for std_h in std_H:
            f.write(str(std_h)+"\n")
