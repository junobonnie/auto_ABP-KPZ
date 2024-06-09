import numpy as np
import matplotlib.pyplot as plt
from atom import *
from ABP_density import CIC
import sys

def draw_map(title, cmap = 'viridis'):
    plt.figure(dpi=300)
    plt.imshow(map_, cmap)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(path + '/' + title + '.png', bbox_inches='tight')
    plt.close()

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
path = 'images/results/'+str(width)+'x'+str(height)


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

time = np.arange(0, 1000000, 10)
for t in time:
    k = t*20
    simulator.load_snapshot('snapshots/'+str(width)+'x'+str(height)+'/snapshot_%08d.hdf5'%(k))
    atoms = simulator.world.atoms
    cic = CIC(atoms, 5, width, height)
    map_ = cic.density_map()
    width_ = len(map_[0])
    height_ = len(map_)
    draw_map('0_%08d'%(k), 'plasma')
    print(t)
