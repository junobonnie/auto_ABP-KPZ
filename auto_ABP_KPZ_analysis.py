from multiprocessing import Pool
import os
import sys
import numpy as np

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이

def main(i):
    os.system('pypy3 ABP_KPZ_analysis.py %d %d %03d'%(width, height, i))

if __name__=='__main__':
    num_list = [33,33,34] # [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34]
    end_num = 0
    for num in num_list:
        pool = Pool(num)
        pool.map(main, [i for i in range(end_num+1, end_num+num+1)])
        pool.close()
        end_num += num

    Ws = []
    for i in range(1, 101):
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
