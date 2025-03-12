# from multiprocessing import Pool
# import os
import sys
import numpy as np

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
# time_cut = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[3]) #시뮬레이션 횟수

if __name__=='__main__':

    Ws = []
    for i in range(1, num+1):
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
    for i in range(1, num+1):
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

    time = list(range(500000, 1000000, 10000))
    #time = list(range(100, 510, 100))
    #time = list(range(10000, 20010, 1000))
    for t in time:
        if t > 700000:
            break

        LWs = []
        for i in range(1, num+1):
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
