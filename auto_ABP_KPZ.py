from multiprocessing import Pool
import os
import sys
from mail import Mail

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
time_cut = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[4]) #시뮬레이션 횟수
for i in range(1, num+1):
    print("%03d >>"%i)
    os.system('abp-kpz-rust-freestanding %d %d %03d %d'%(width, height, i, time_cut))
    # os.system('abp-kpz-rust-freestanding-F_0is0 %d %d %03d %d'%(width, height, i, time_cut))
    # os.system('abp-kpz-rust-freestanding-ro-F_0is_half %d %d %03d %d'%(width, height, i, time_cut))
    # os.system('abp-kpz-rust-twofixed %d %d %03d %d'%(width, height, i, time_cut))
mail = Mail()
mail.set_subject("auto_ABP_KPZ %d %d %d %d is done."%(width, height, time_cut, num))
mail.add_text("")
mail.send()
'''
def main(i):
    os.system('pypy3 ABP_KPZ.py %d %d %03d'%(width, height, i))    

if __name__=='__main__':
    num_list = [33, 33, 34] #[33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34]
    end_num = 0
    for num in num_list:
        pool = Pool(num)
        pool.map(main, [i for i in range(end_num+1, end_num+num+1)])
        pool.close()
        end_num += num
'''
