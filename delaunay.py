import numpy as np
from scipy.spatial import Delaunay
from sublevelviz import *


class Del:
    def __init__(self, P):
        """
        Initialize a Delaunay triangulation from a set of points in the plane.
        """
        self.P = P
        self.X = [x for x,y in P]
        self.Y = [y for x,y in P]
        self.triangles = Delaunay(P).simplices

    def __iter__(self):
        yield from self.P

if __name__ == '__main__':
    I = [-1, -.5,-.2, 0, .3, .5, .7,1]
    B = [-1, 1]
    # P = [[x,y] for x in I for y in I]
    BDY = [[x,y] for x in I for y in B] + [[x,y] for x in B for y in I]
    P = BDY + [[0,0], [0.5,0.4]]

    def f(x,y):
        bumps = [(-0.35, 0.1, 0.3, 1), (-0.33, 0.1,0.15, -0.75), (0.25,-0.1,0.2, 0.75)]
        gs = [gaussian(*p) for p in bumps]
        return sum(g(x,y) for g in gs)


    # def f(x,y):
    #     return sqdist([x,y], [0,0])

    F = Sub(f, Del(P))
    t = 1000
    c = (0.78, 0.78, 0.78)
    black = (0,0,0)
    fig = figure(bgcolor=(1, 1, 1))
    # triangular_mesh(*F(t), tube_radius=0.2, color=c)
    triangular_mesh(*F(t), color=c)
    triangular_mesh(*F(t), representation='wireframe', color=black, tube_radius=0.5)
    show()
