import os
import sys
import numpy as np

folder = str(sys.argv[1]) #시뮬레이션 공간의 가로길이
xx = float(sys.argv[2]) #시뮬레이션 공간의 세로길이
yy = float(sys.argv[3]) #시뮬레이션 시간길이

while True:
    os.system('ABP_KPZ_analysis_circular_iter --width=2880 --height=3200 --folder=%s --timecut=700000 --xx=%f --yy=%f > temp'%(folder, xx, yy))
    xx_ = xx
    yy_ = yy
    with open('temp', 'r') as f:
        lines = f.readlines()
    xx -= float(lines[-1].split(" ")[0])
    yy -= float(lines[-1].split(" ")[1])
    print(xx, yy)
    if abs(xx-xx_) < 0.1 and abs(yy-yy_) < 0.1:
        break
    