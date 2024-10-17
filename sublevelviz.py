import numpy as np
from mayavi.mlab import *

class Grid:
    def __init__(self, width, height, extent=[[-1.0, 1.0], [-1.0, 1.0]]):
        self.width = width
        self.height = height
        x_0, x_1 = extent[0]
        y_0, y_1 = extent[1]
        grid = np.meshgrid(np.linspace(x_0, x_1, width), np.linspace(y_0, y_1, height))
        self.X, self.Y = grid[0].flatten(), grid[1].flatten() 

        self.triangles = []
        for i in range(1, width):
            for j in range(1,height):
                a = j * width + i
                b = a - 1
                c = a - width
                d = c - 1
                self.triangles.append([a,b,c])
                self.triangles.append([b,c,d])

    def __iter__(self):
        return zip(self.X, self.Y)

class Sub:
    def __init__(self, f, domain):
        self.domain = domain
        self.Z = [f(x,y) for x,y in self.domain]

    def __call__(self, t):
        X = self.domain.X
        Y = self.domain.Y
        Z = self.Z
        all_triangles = self.domain.triangles

        def value(triangle):
            return max(self.Z[p] for p in triangle)

        T = [triangle for triangle in all_triangles if value(triangle) <= t]
        return X, Y, Z, T


def f(x,y):
    return np.exp(-(x**2 + y**2)/0.1)

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def max_extension(P):
    def f(x,y):
        return min(pz + dist([x, y], [px, py]) for px, py, pz in P)
    return f

def min_extension(P):
    def f(x,y):
        return max(pz - dist([x, y], [px, py]) for px, py, pz in P)
    return f


P = [(-0.5,0.5,0), (0.5,0.5,0), (0,-0.5, 0.5)]
f_max = max_extension(P)
f_min = min_extension(P)

G = Grid(1000,1000)
F_max = Sub(f_max, G)
F_min = Sub(f_min, G)
fig = figure(bgcolor=(1,1,1))

t = 0.3

triangular_mesh(*F_max(t), colormap='gray')
triangular_mesh(*F_min(t), colormap='gray')

show()
