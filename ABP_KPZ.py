# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 17:51:57 2024

@author: replica
"""

### 필요한 라이브러리 선언 ###
from vectortools import *
from atom import *
import sys
import random
#import time
### 필요한 라이브러리 선언 ###

#=============== 새로 추가된 부분 ===============#
k = 20 # 상수 설정
mu_1 = 1
mu_2 = 0.25
mu_3 =3/2
tau = 0.01

c1 = m.sqrt(2*tau*mu_1)
c2 = m.sqrt(2*tau*mu_2)
c3 = m.sqrt(2*tau*mu_3)

L = 5
v_0 = 0*Vector(0, -1)
class Atom(Atom):
    def __init__(self, element, pos, vel = Vector(0, 0), polarity = 0, is_static=False):
        self.element = element
        self.pos = pos
        self.vel = vel
        self.polarity = polarity
        self.is_static = is_static

    ### 상호작용 추가 ###
    def acc(self, other):
        r = self.pos - other.pos
        if not self == other and r.dot(r) < L**2:
            return k*(L/abs(r)-1)*r
        else:
            return Vector(0, 0)
    ### 상호작용 추가 ###
    
class Render(Render):
    def __init__(self, screen, width, height):
        pg.init()
        self.screen = screen
        self.width = width
        self.height = height
        self.render_vector = Vector(0, height)
        self.render_metric = Tensor(1, 0, 0, -1)
        self.origin_vector = Vector(width/2, height/2)

    def atom(self, atom):
        self.circle(atom.pos, atom.element.radius, (255*atom.polarity/(2*m.pi),0,0))
        
        
class Simulator(Simulator):
    def __init__(self, dt, world, render, grid_size = 100):
        self.dt = dt
        self.world = world
        self.render = render
        self.count_screen = 0
        self.count_snapshot = 0
        self.grid_size = grid_size
        self.grid = None
        
    def main(self):
        x_ = []
        v_ = []
       # t1 = time.time()
        self.make_grid()
        #t2 = time.time()
        for atom in self.world.atoms:
            atom_acc = Vector(0, 0)
            ### 상호작용 추가 ###
            atom_acc += self.acc(atom)
            atom.polarity += c3*random.gauss(0, 1)*self.dt
            atom.polarity %= 2*m.pi
            if not atom.is_static:
                u = SO2(atom.polarity).dot(Vector(1, 0))
                new_v = v_0 + mu_1*u + (mu_1-mu_2)*u.dot(atom_acc)*u + mu_2*atom_acc + c1*random.gauss(0, 1)*u + c2*SO2(m.pi/2).dot(u)
            else:
                new_v = Vector(0,0)
            ### 상호작용 추가 ###
            v_.append(new_v)
            x_.append((atom.pos + new_v*self.dt))
        #t3 = time.time()

        count = 0
        for atom in self.world.atoms:
            atom.pos = Vector((x_[count].x+self.render.width/2)%(self.render.width)-self.render.width/2, (x_[count].y+self.render.height/2)%(self.render.height)-self.render.height/2)
            atom.vel = v_[count]
            count = count + 1
        #t4 = time.time()

        # print(t2 - t1, t3 - t2, t4 - t3)
    def make_grid(self):
        w_ = self.render.width/self.grid_size
        h_ = self.render.height/self.grid_size
        nx = round(w_)
        ny = round(h_)
        if abs(nx-w_) > 0.00001 or abs(ny-h_) > 0.00001:
            raise ValueError('grid_size must be a divisor of width and height')
        grid = [[] for i in range(nx*ny)]
        for atom in self.world.atoms:
            i = int((self.render.width/2 + atom.pos.x)//self.grid_size)
            j = int((self.render.height/2 + atom.pos.y)//self.grid_size)
            if (0 <= i < nx) and (0 <= j < ny):
                grid[i+nx*j].append(atom)
        self.grid = grid
    
    def acc(self, atom):
        nx = round(self.render.width/self.grid_size)
        ny = round(self.render.height/self.grid_size)
        i = int((self.render.width/2 + atom.pos.x)//self.grid_size)
        j = int((self.render.height/2 + atom.pos.y)//self.grid_size)
        acc_ = Vector(0, 0)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                i_ = (i+di)%nx
                j_ = (j+dj)%ny
                # if atom == self.world.atoms[0]:
                    # self.render.polygon([Vector(i_*self.grid_size-self.render.width/2 , j_*self.grid_size-self.render.height/2), 
                    #                     Vector((i_+1)*self.grid_size-self.render.width/2 , j_*self.grid_size-self.render.height/2), 
                    #                     Vector((i_+1)*self.grid_size-self.render.width/2 , (j_+1)*self.grid_size-self.render.height/2), 
                    #                     Vector(i_*self.grid_size-self.render.width/2 , (j_+1)*self.grid_size-self.render.height/2)], red)
                for other in self.grid[i_+nx*j_]:
                    other_pos = other.pos - Vector((i_-di-i)*self.grid_size, (j_-dj-j)*self.grid_size)
                    r = atom.pos - other_pos
                    # if atom == self.world.atoms[0]:
                    #     self.render.polygon([atom.pos, other_pos], blue)
                    if not atom == other and r.dot(r) < L**2:
                        acc_ += k*(L/abs(r)-1)*r
        return acc_
    
    def save_snapshot(self, directory, skip_number = 0):
        if self.count_snapshot%(skip_number+1) == 0:
            snapshot = directory + '/snapshot_%08d.hdf5' % (self.count_snapshot)
            with h5py.File(snapshot, 'w') as f:
                f.attrs['count_snapshot'] = self.count_snapshot
                world = f.create_group('world')
                world.attrs['t'] = self.world.t
                world.attrs['gravity'] = self.world.gravity.list()
                atoms = world.create_group('atoms')
                N = len(self.world.atoms)
                element = [0]*N
                mass = [0]*N
                radius = [0]*N
                color = [0]*N
                pos = [0]*N
                vel = [0]*N
                polarity = [0]*N
                is_static = [0]*N
                count = 0
                for atom in self.world.atoms:
                    element[count] = atom.element.name
                    mass[count] = atom.element.mass
                    radius[count] = atom.element.radius
                    color[count] = (atom.element.color.r, atom.element.color.g, atom.element.color.b, atom.element.color.a)
                    pos[count] = atom.pos.list()
                    vel[count] = atom.vel.list()
                    polarity[count] = atom.polarity
                    is_static[count] = atom.is_static
                    count += 1
                atoms.create_dataset('element', data = element)
                atoms.create_dataset('mass', data = mass)
                atoms.create_dataset('radius', data = radius)
                atoms.create_dataset('color', data = color)
                atoms.create_dataset('pos', data = pos)
                atoms.create_dataset('vel', data = vel)
                atoms.create_dataset('polarity', data = polarity)
                atoms.create_dataset('is_static', data = is_static)
                walls = world.create_group('walls')
                N = len(self.world.walls)
                width = [0]*N
                height = [0]*N
                theta = [0]*N
                pos = [0]*N
                color = [0]*N
                count = 0
                for wall in self.world.walls:
                    width[count] = wall.width
                    height[count] = wall.height
                    theta[count] = wall.theta
                    pos[count] = wall.pos.list()
                    color[count] = (wall.color.r, wall.color.g, wall.color.b, wall.color.a)
                    count += 1
                walls.create_dataset('width', data = width)
                walls.create_dataset('height', data = height)
                walls.create_dataset('theta', data = theta)
                walls.create_dataset('pos', data = pos)
                walls.create_dataset('color', data = color)
            with open(directory + "/last_snapshot", "w") as f:
                f.write('snapshot_%08d.hdf5\n' % (self.count_snapshot))
        self.count_snapshot += 1

    def load_snapshot(self, snapshot_file):
        with h5py.File(snapshot_file, 'r') as f:
            self.count_snapshot = f.attrs['count_snapshot']
            world = f['world']
            t = world.attrs['t']
            #gravity = self.list_to_vector(list(world.attrs['gravity']))
            #element_ = world['atoms']['element']
            #mass_ = world['atoms']['mass']
            #radius_ = world['atoms']['radius']
            #color_ = world['atoms']['color']
            pos_ = world['atoms']['pos']
            vel_ = world['atoms']['vel']
            polarity_ = world['atoms']['polarity']
            is_static_ = world['atoms']['is_static']
            N = len(pos_)
            atoms = [0]*N
            for i in range(N):
                #element = Element(element_[i], float(mass_[i]), float(radius_[i]), pg.Color(color_[i]))
                element = Element("Helium", 1.0, 3.0, pg.Color('red'))
                pos = self.list_to_vector(pos_[i])
                vel = self.list_to_vector(vel_[i])
                atoms[i] = Atom(element, pos, vel, float(polarity_[i]), bool(is_static_[i]))
            #width_ = world['walls']['width']
            #height_ = world['walls']['height']
            #theta_ = world['walls']['theta']
            #pos_ = world['walls']['pos']
            #color_ = world['walls']['color']
            #N = len(width_)
            #walls = [0]*N
            #for i in range(N):
            #    walls[i] = Wall(width_[i], height_[i], theta_[i], self.list_to_vector(pos_[i]), pg.Color(color_[i]))
            walls=[]
            self.world = World(t, atoms, walls, gravity=Vector(0, 0))
        
#=============== 새로 추가된 부분 ===============#

### render 설정 ###
# 시뮬레이션 화면에 뭔가 그리는 함수는 다 render에 있음
width = int(sys.argv[1]) #시뮬레이션 공간의 가로길이
height = int(sys.argv[2]) #시뮬레이션 공간의 세로길이
folder = sys.argv[3]
#screen = pg.display.set_mode((width, height)) # 시뮬레이션 화면 설정

render = Render(None, width, height) # render 설정
### render 설정 ###

### 시뮬레이션 업데이트 시간 설정 ###
#clock = pg.time.Clock()
### 시뮬레이션 업데이트 시간 설정 ###

### 색깔 선언 ###
black = pg.Color('black')
white = pg.Color('white')
red = pg.Color('red')
green = pg.Color('green')
blue = pg.Color('blue')
### 색깔 선언 ###

### 벽 선언 ###
# Wall(가로 길이, 세로 길이, 회전 각도, 중심의 위치 벡터, 색깔)
#wall1 = Wall(800, 50, 0, Vector(-400, -180), blue)
# wall2 = Wall(50, 800, 0, Vector(-200, -400), blue)
# wall3 = Wall(50, 800, 0, Vector(150,-400), blue)
# wall4 = Wall(800, 50, 0, Vector(-400, 150), blue)

# wall1 = Wall(800, 50, 0, Vector(-400, -400), blue)
# wall2 = Wall(50, 800, 0, Vector(-400, -400), blue)
# wall3 = Wall(50, 800, 0, Vector(350,-400), blue)
# wall4 = Wall(800, 50, 0, Vector(-400, 350), blue)
# wall5 = Wall(100, 50, m.pi/4, Vector(-300, 0), blue)
### 벽 선언 ###

### 원소 선언 ###
# Element(원소의 이름, 질량, 반지름, 색깔)
e1 = Element(name = 'Helium', mass = 1, radius = 3, color = red)
### 원소 선언 ###

### 원자 선언 ###
# Atom(원소, 위치벡터, 속도벡터(디폴트 0벡터))
# atom1 = Atom(e1, Vector(-200, 0), Vector(50, 0))
# atom2 = Atom(e1, Vector(0, 0))
# atom3 = Atom(e1, Vector(25, -10))
# atom4 = Atom(e1, Vector(25, 10))
# atom5 = Atom(e1, Vector(50, -20))
# atom6 = Atom(e1, Vector(50, 0))
# atom7 = Atom(e1, Vector(50, 20))
### 원자 선언 ###

### 벽들과 원자들 선언 ###
# walls = [wall1, wall2, wall3, wall4]
# atoms = [atom1, atom2, atom3, atom4, atom5, atom6, atom7]


#=============== 새로 추가된 부분 ===============#
### 2체 문제 ###
# e2 = Element(name = 'Heavy', mass = 100, radius = 10, color = blue)
# atom1 = Atom(e1, Vector(20, 0), Vector(0, 0))
# atom2 = Atom(e1, Vector(0, 0), Vector(0, 0))
# walls = []
# atoms = [atom1, atom2]
### 2체 문제 ###

# ### 3체 문제 ###
# atom1 = Atom(e1, Vector(200, 0), Vector(0, 0))
# atom2 = Atom(e1, Vector(0, -200), Vector(0, 0))
# atom3 = Atom(e1, Vector(-200, 50), Vector(0, 0))
# walls = []
# atoms = [atom1, atom2, atom3]
# ### 3체 문제 ###
path = 'snapshots/' + str(width) + 'x' + str(height) + '/' + folder
try:
    with open(path + "/last_snapshot", "r") as f:
        last_snapshot = f.readline().strip()
        print(last_snapshot)
        ### 벽들과 원자들 선언 ###
        atoms = []
        walls = []
        ### 시뮬레이션 전체 외력(외부 가속도) 설정 ###
        gravity = Vector(0, 0)
        ### 시뮬레이션 전체 외력(외부 가속도) 설정 ###

        ### 시뮬레이션 월드 선언 ###
        # World(초기시간, 원자들, 벽들, 외부 가속도)
        world = World(0, atoms, walls, gravity)
        ### 시뮬레이션 월드 선언 ###
        simulator = Simulator(0.05, world, render, L)
        ### 시뮬레이터 선언 ###
        # Simulator(시간간격, 시뮬레이션 월드, 렌더)
        simulator.load_snapshot(path +"/"+ last_snapshot)
        print("load!!!!!!!!!!!!")

except:
    ## 구상성단 코드 ###
    walls = [] #[wall1]
    atoms = []
    for i in range(width//10):
        polarity = 2*m.pi*random.random()
        atoms.append(Atom(e1, Vector(10*i-width/2, 0), polarity=polarity, is_static=True))

    for i in range(width//10):
        for j in range(height//10):
            if not j==height//20:
                polarity = 2*m.pi*random.random()
                atoms.append(Atom(e1, Vector(10*i-width/2, 10*j-height/2), polarity=polarity))
    import os
    os.system("mkdir -p " + path)
## 구상성단 코드 ###
#=============== 새로 추가된 부분 ===============#

### 벽들과 원자들 선언 ###

### 시뮬레이션 전체 외력(외부 가속도) 설정 ###
    gravity = Vector(0, 0)
### 시뮬레이션 전체 외력(외부 가속도) 설정 ###

### 시뮬레이션 월드 선언 ###
# World(초기시간, 원자들, 벽들, 외부 가속도)
    world = World(0, atoms, walls, gravity)
### 시뮬레이션 월드 선언 ###

### 시뮬레이터 선언 ###
# Simulator(시간간격, 시뮬레이션 월드, 렌더)
    simulator = Simulator(0.05, world, render, L)
### 시뮬레이터 선언 ###
    print("start!!!!!!!!!!!!")
### 기존 시뮬레이션 스냅샷을 로드하는 코드 ###
# simulator.load_snapshot('snapshots/snapshot_00000400.hdf5')
### 기존 시뮬레이션 스냅샷을 로드하는 코드 ###

#import tracemalloc as tm
time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000), np.arange(1000000, 10000000, 100000)])
while True:
#    st = tm.take_snapshot()
    ### 시뮬레이션 시간 출력 ###
    # 꼭 필요한 코드가 아니지만 시뮬레이션 시간을 출력하려면 
    # 이렇게 할 수 있다는 걸 보여줄려고 추가한 코드 
    t = simulator.clock()
    ### 시뮬레이션 시간 출력 ###
    #for i in range(-240,240):
    #    if random.random() < 0.0001:
    #        position =  Vector(i, height/2)
    #        polarity = 2*m.pi*random.random()
    #        atoms.append(Atom(e1, position, polarity=polarity))
    
    ### 시뮬레이션 메인 부분 ###
    # simulator.draw_background(white) #시뮬레이션 배경화면 그리기
    # simulator.draw_grid(100) #격자그리기
    #simulator.draw_wall() #벽그리기
    #simulator.atom_wall_collision() #원자와 벽 사이의 충돌 고려
    #simulator.atom_atom_collision() #원자와 원자 사이의 충돌 고려 
    #simulator.atom_atom_fusion() #원자와 원자의 병합 고려

    
    simulator.main() #원자의 위치와 속력을 업데이트 하는 함수
    
#    end = tm.take_snapshot()
#    stats = end.compare_to(st, 'traceback')
#    top = stats[0]
#    print('\n'.join(top.traceback.format()))
    # simulator.draw_atom() # 원자 그리기
    ### 시뮬레이션 메인 부분 ###

    ### 시뮬레이션 화면에 텍스트 그리기 ###
    # render.text(텍스트, 폰트, 크기, 위치벡터, 색깔)
    # render.text('pos = (%.2f, %.2f)'%(atom1.pos.x, atom1.pos.y) , None, 30, Vector(atom1.pos.x -100, atom1.pos.y - 30), black)
    # render.text('vel = (%.2f, %.2f)'%(atom1.vel.x, atom1.vel.y) , None, 30, Vector(atom1.pos.x -100, atom1.pos.y - 50), black)

    # render.text('pos = (%.2f, %.2f)'%(atom7.pos.x, atom7.pos.y) , None, 30, Vector(atom7.pos.x -100, atom7.pos.y - 30), blue)
    # render.text('vel = (%.2f, %.2f)'%(atom7.vel.x, atom7.vel.y) , None, 30, Vector(atom7.pos.x -100, atom7.pos.y - 50), blue)
    ### 시뮬레이션 화면에 텍스트 그리기 ###
    
    ### 이거 없음 에러남 ###
    #for event in pg.event.get():
    #   if event.type == pg.QUIT:
    #       sys.exit()
    ### 이거 없음 에러남 ###
    
    ### 시뮬레이션 화면 업데이트 ###
    #clock.tick(100)# 시뮬레이션 화면 업데이트 시간간격
    #pg.display.update() #시뮬레이션 화면 업데이트
    ### 시뮬레이션 화면 업데이트 ###
        
    ### 매시간 마다 시뮬레이션 화면을 png로 저장하는 코드 ###
    # simulator.save_screen(저장위치, 건너뛸 개수(디폴트 0))
    #simulator.save_screen('images/')
    ### 매시간 마다 시뮬레이션 화면을 png로 저장하는 코드 ###
    
    ### 매시간 마다 시뮬레이션 스냅샷을 저장하는 코드 ###
    # simulator.save_screen(저장위치, 건너뛸 개수(디폴트 0))
    if simulator.count_snapshot in 20*time:
        simulator.save_snapshot(path)
        print(folder + ": " + str(t))
    else:
        simulator.count_snapshot += 1
    
    ### 매시간 마다 시뮬레이션 스냅샷을 저장하는 코드 ###
    if t > 100010: #10000010:
        break
