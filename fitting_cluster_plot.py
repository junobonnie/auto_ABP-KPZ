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
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

def binarization(map_, threshold):
    return list(map(lambda x : list(map(lambda y : 1 if y > threshold else 0, x)), map_))

def draw_map(title, cmap = 'viridis'):
    plt.figure(dpi=300)
    plt.imshow(map_, cmap)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(path + '/' + title + '.png', bbox_inches='tight')
    plt.close()

def get_heights(map_):
    heights = [0 for i in range(len(map_[0]))]
    for i in range(len(map_[0])):
        for j in reversed(range(0, len(map_))):
            if map_[j][i] == 1:
                heights[i] = unit*j
                break
    return heights

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
t = int(sys.argv[3]) #시뮬레이션 시간길이
num = int(sys.argv[4]) #시뮬레이션 횟수
unit = 5

#W = []
#time_cut = 100010
clusters_ = []
for i in range(1, num+1):
    folder = '%03d'%i

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

    k = t*20
    simulator.load_snapshot('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + '/snapshot_%08d.hdf5'%(k))
    atoms = simulator.world.atoms
    cic = CIC(atoms, unit, width, height)
    map_ = cic.density_map()
    map_ = cic.density_map()
    width_ = len(map_[0])
    height_ = len(map_)

    #draw_map('0_%08d'%(k), 'plasma')
    #map_ = np.flip(map_, axis=0)
    for i in range(width_):
        for j in range(int(height/2)//5):
            map_[j][i] = 1   

    #draw_map('1_%08d'%(k), 'plasma')

    map_ = binarization(map_, 0.8)

    #draw_map('2_%08d'%(k), 'gray')

    clusters = floodfill(map_)

    largest_cluster = max(clusters, key=len)
    clusters = [cluster for cluster in clusters if cluster != largest_cluster]
    clusters_.extend(clusters)

hist = np.histogram([len(cluster) for cluster in clusters_], bins = 5000, range=(1, 5000))
x = hist[1][:-1]
y = hist[0]/num
print(t)

y_nonzero = y[y.nonzero()]
x_nonzero = x[y.nonzero()]

popt, pcov = curve_fit(log_func, x_nonzero, np.log(y_nonzero), p0=[5000., -2.16])
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
#popt = [5000., -2.16]
model = func(x_nonzero, *popt)

plt.figure(dpi=300)
# plt.hist([len(cluster) for cluster in clusters_], bins = 100, alpha=0.5, color='b', edgecolor='black', linewidth=1.2)
plt.step(x, y, where='mid', color='b', linewidth=1.2)
plt.fill_between(x, y, step='mid', color='b', alpha=0.5)
plt.plot(x_nonzero, model, color='r', linewidth=1.2, label='a = %.2f, b = %.2f'%(popt[0], popt[1]))
plt.legend()
plt.xlim(1, 5000)
plt.ylim(0.01, 2e4)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('Number of clusters')
plt.xlabel('Size')
plt.title('Cluster size distribution, %d x %d, %d, %d'%(width, height, t, num))
plt.savefig('fitting_cluster_size_distribution_%08d.png'%(k), bbox_inches='tight')
