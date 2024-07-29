import numpy as np
import matplotlib.pyplot as plt
from atom import *
from ABP_density import CIC
import sys

def draw_map(title, t, cmap = 'viridis'):
    plt.figure(dpi=300)
    plt.text(-20, -20, "%.2e s"%t, fontsize=5, color='red')
    plt.imshow(map_, cmap)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(path + '/' + title + '.png', bbox_inches='tight')
    plt.close()

def density_vs_height(atoms, t, unit_height=48):
    density = [0 for i in range(int(height//unit_height))]
    for atom in atoms:
        density[int((atom.pos.y+height/2)//unit_height)] += 1
    density = np.array(density)
    density = density/(unit_height*width)
    heights_ = np.linspace(0, height, int(height//unit_height))
    plt.figure(dpi=300)
    plt.step(heights_, density, label="Density")
    plt.axvline(x=height/2, color='red', label='middle line')
    plt.title("Density vs Height at t=%.2e s"%t)
    plt.xlabel("Height")
    plt.ylabel("Density")
    plt.xlim(0, height)
    plt.ylim(0, 0.05)
    plt.legend()
    plt.savefig(path + '/density_vs_height_%08d.png'%(20*t))
    plt.close()

width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
folder = "%03d"%(int(sys.argv[3]))
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

time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000), np.arange(1000000, 10000000, 100000)])
for t in time:
    k = t*20
    simulator.load_snapshot('snapshots/'+str(width)+'x'+str(height)+'/'+folder+'/snapshot_%08d.hdf5'%(k))
    atoms = simulator.world.atoms
    cic = CIC(atoms, 5, width, height)
    map_ = cic.density_map()
    width_ = len(map_[0])
    height_ = len(map_)
    draw_map('0_%08d'%(k), t, 'plasma')
    density_vs_height(atoms, t)
    print(t)
