# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 21:47:55 2024

@author: replica
"""
import numpy as np
import matplotlib.pyplot as plt
from atom import *
from ABP_density import CIC
from FloodFill import floodfill
import sys

def binarization(map_, threshold):
    return list(map(lambda x : list(map(lambda y : 1 if y > threshold else 0, x)), map_))

def draw_map(title, cmap = 'viridis'):
    plt.figure(dpi=300)
    plt.imshow(map_, cmap)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(path + '/' + title + '.png', bbox_inches='tight')
    plt.close()

def get_heights_1(map_):
    heights = [0 for i in range(len(map_[0]))]
    for i in range(len(map_[0])):
        for j in reversed(range(0, len(map_))):
            if map_[j][i] == 1:
                heights[i] = unit*j
                break
    return heights

def get_heights_2(map_):
    heights = [0 for i in range(len(map_[0]))]
    for i in range(len(map_[0])):
        for j in range(0, len(map_)):
            if map_[j][i] == 1:
                heights[i] = unit*j
                break
    return heights

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
folder = sys.argv[3]
time_cut = int(sys.argv[4]) #시뮬레이션 시간길이
unit = 5

path = 'images/results/'+ str(width) + 'x' + str(height) + '/' + folder

#screen = pg.display.set_mode((width, height))
render = Render(None, width, height)
clock = pg.time.Clock()

black = pg.Color('black')
white = pg.Color('white')
red = pg.Color('red')
green = pg.Color('green')
blue = pg.Color('blue')

walls = []
atoms = []

gravity = Vector(0, 0)
world = World(0, atoms, walls, gravity)

simulator = Simulator(0.01, world, render)

#W = []
#time_cut = 100010
time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000)])
with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/W.txt", "w") as f:
    with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/H.txt", "w") as ff:
        with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/W2.txt", "w") as f2:
            with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/H2.txt", "w") as ff2:
                with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/W1.txt", "w") as f1:
                    with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/H1.txt", "w") as ff1:
                        for t in time:
                            if t > time_cut:
                                break
                            k = t*20
                            simulator.load_snapshot('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + '/snapshot_%08d.hdf5'%(k))
                            atoms = simulator.world.atoms
                            cic = CIC(atoms, unit, width, height)
                            map_ = cic.density_map()
                            width_ = len(map_[0])
                            height_ = len(map_)
                    
                            #draw_map('0_%08d'%(k), 'plasma')
                            #map_ = np.flip(map_, axis=0)
                        
                            #draw_map('1_%08d'%(k), 'plasma')
                        
                            map_ = binarization(map_, 0.8)
                        
                            #draw_map('2_%08d'%(k), 'gray')
                        
                            clusters = floodfill(map_)
                            map_ = [[0 for i in range(width_)] for j in range(height_)]
                            for point in max(clusters, key=len):
                                i, j = point
                                map_[j][i] = 1
                            #draw_map('3_%08d'%(k))
                            print(folder + ": " + str(t))
                            heights_1 = get_heights_1(map_)
                            heights_2 = get_heights_2(map_)
                            heights = np.array(heights_1) - np.array(heights_2)
                            #print(heights)
                            std_1 = np.std(heights_1)
                            std_2 = np.std(heights_2)
                            std_ = np.std(heights)
                            #W.append(std_)
                            f1.write(str(std_1)+"\n")
                            ff1.write(str(np.mean(heights_1))+"\n")
                            f2.write(str(std_2)+"\n")
                            ff2.write(str(np.mean(heights_2))+"\n")
                            f.write(str(std_)+"\n")
                            ff.write(str(np.mean(heights))+"\n")
        

# W = np.array(W)
# kpz = (0.3)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
# plt.figure(dpi=300)
# plt.plot(time, W, label="KPZ Simulation")
# plt.plot(time, kpz, label="Family–Vicsek scaling relation")
# plt.legend()
# plt.xlabel("time")
# plt.ylabel("Standard Deviation of Heights")
# plt.xscale("log")
# plt.yscale("log")
# plt.savefig(str(width)+'x'+str(height)+'log_plot.png')
