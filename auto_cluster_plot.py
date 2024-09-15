from multiprocessing import Pool
import os
import sys
import numpy as np

def num_list(time):
    n = len(time)//unit_
    r = len(time)%unit_
    return [unit_ for _ in range(n)] + [r]

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
time_cut = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[4]) #시뮬레이션 횟수

def main(t):
    os.system('pypy3 cluster_plot.py %d %d %d %d'%(width, height, t, num))

time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000)])
time = time[(time<=time_cut)]
unit_ = 33

if __name__=='__main__':
    end_num_ = 0
    for num_ in num_list(time):
        pool = Pool(num_)
        pool.map(main, [t for t in time[end_num_: end_num_+num_]])
        pool.close()
        end_num_ += num_