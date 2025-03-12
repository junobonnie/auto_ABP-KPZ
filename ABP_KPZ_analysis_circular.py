# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 21:47:55 2024

@author: replica
"""
import numpy as np
#import matplotlib.pyplot as plt
from atom import *
#from ABP_density import CIC
#from FloodFill import floodfill
import sys

#def binarization(map_, threshold):
#    return list(map(lambda x : list(map(lambda y : 1 if y > threshold else 0, x)), map_))

def transport(atoms, width, height, dx, dy):
    for atom in atoms:
        atom.pos.x += dx
        atom.pos.y += dy
        if atom.pos.x < 0:
            atom.pos.x += width
        elif atom.pos.x >= width:
            atom.pos.x -= width
        if atom.pos.y < 0:
            atom.pos.y += height
        elif atom.pos.y >= height:
            atom.pos.y -= height

def find_cluster(atoms, seed_atom, radius):
    candidates = atoms.copy()
    candidates.remove(seed_atom)
    cluster = [seed_atom]
    for atom in cluster:
        for candidate in candidates:
            d = atom.pos - candidate.pos
            if d.dot(d) < radius**2:
                candidates.remove(candidate)
                cluster.append(candidate)
    return cluster

def get_heights(atoms, seed_atom, radius, half_sampling_number):
    unsorted_heights = []
    cluster = find_cluster(atoms, seed_atom, radius)
    pos_center = seed_atom.pos
    angles = np.linspace(0, np.pi, half_sampling_number+1)[:-1]
    for angle in angles:
        edge_candidate = []
        for atom in cluster:
            COS = np.cos(angle)
            SIN = np.sin(angle)
            if abs(SIN*(atom.pos.x - pos_center.x) + COS*(pos_center.y - atom.pos.y)) < radius:
                #B = (x_c-xs[i])*COS + (y_c-ys[i])*SIN
                B = (pos_center.x-atom.pos.x)*COS + (pos_center.y-atom.pos.y)*SIN
                #C = (x_c-xs[i])**2+(y_c-ys[i])**2-0.4**2
                C = (pos_center.x-atom.pos.x)**2+(pos_center.y-atom.pos.y)**2-radius**2
                t0 = -B-np.sqrt(B**2-C)
                t1 = -B+np.sqrt(B**2-C)
                edge_candidate.append(t0)
                edge_candidate.append(t1)
        t = min(edge_candidate)
        unsorted_heights.append(t)
        t = max(edge_candidate)
        unsorted_heights.append(t)

    heights = [0 for i in range(2*len(angles))]
    for i in range(2*len(angles)):
        height = unsorted_heights[i]
        if i%2==0:
            heights[len(angles)+i//2] = height
        else:
            heights[i//2] = height
    return heights

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
folder = sys.argv[3]
time_cut = int(sys.argv[4]) #시뮬레이션 시간길이

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
    with open('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + "/H.txt", "w") as f2:
        for t in time:
            if t > time_cut:
                break
            k = t*20
            simulator.load_snapshot('snapshots/' + str(width) + 'x' + str(height) + '/' + folder + '/snapshot_%08d.hdf5'%(k))
            atoms = simulator.world.atoms
            
            transport(atoms, width, height, 1440, -1600)
            seed_atom = atoms[76640]
            heights = get_heights(atoms, seed_atom, radius=5, half_sampling_number=100)
            #print(heights)
            std_ = np.std(heights)
            #W.append(std_)
            f.write(str(std_)+"\n")
            ave = np.mean(heights)
            f2.write(str(ave)+"\n")
            print(t, "is done.")
        
        
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
