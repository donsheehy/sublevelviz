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
        return Triangulation(X, Y, Z, T)

class Triangulation:
    def __init__(self, X, Y, Z, T):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.T = T

    def translate(self, vec):
        dx, dy, dz = vec
        XX = [x + dx for x in self.X]
        YY = [y + dy for y in self.Y]
        ZZ = [z + dz for z in self.Z]
        return Triangulation(XX, YY, ZZ, self.T)

    def flatten(self):
        return Triangulation(self.X, [0 for y in self.Y], [y-1.1 for y in self.Y], self.T)
    
    def __iter__(self):
        yield self.X
        yield self.Y
        yield self.Z
        yield self.T

    def __bool__(self):
        return len(self.T) > 0

def dist(a,b):
    return (sqdist(a, b))**0.5

def sqdist(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def gaussian(px, py, sigma, scale):
    def g(x,y):
        return scale * np.exp(-(sqdist([x,y], [px,py]))/(sigma**2))
    return g

if __name__ == '__main__':
    def f(x,y):
        bumps = [(-0.35, 0.1, 0.3, 1), (-0.33, 0.1,0.15, -0.75), (0.25,-0.1,0.2, 0.75)]
        gs = [gaussian(*p) for p in bumps]
        return sum(g(x,y) for g in gs)

    G = Grid(1000, 1000)
    F = Sub(f, G)
    t = 0.3
    c = (0.78, 0.78, 0.78)
    fig = figure(bgcolor=(1, 1, 1))
    triangular_mesh(*F(t), color=c)
    show()
