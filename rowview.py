from sublevelviz import *
from lipschitz import *
from random import randrange

T = [0.15, 0.3, 0.8]
# T = [0.6]
# g = gaussian(0, 0, 0.5, 0.9)
def g(x,y):
    return 0.5 * dist([x,y],[0,0])


def coord():
    return (randrange(100) / 50) - 1

n = 10

P2D = [[coord(), coord()] for i in range(n)]
P = [[x, y, g(x,y)] for x,y in P2D]

G = Grid(100,100)
F_max = Sub(max_extension(P, 1.5), G)
F_min = Sub(min_extension(P, 1.5), G)
c = (0.78,0.78, 1)
c2 = (1,0.78, 0.78)

fig = figure(bgcolor=(1, 1, 1))

for i, t in enumerate(T):
    cplx = F_max(t).translate([2.1*i, 0 , 0])
    if cplx:
        triangular_mesh(*cplx, color=c)
        flat = cplx.flatten().translate([0, -1.13, -0.1])
        if flat:
            triangular_mesh(*flat, color=c)
    cplx = F_min(t).translate([2.1*i, 0 , 0])
    if cplx:
        triangular_mesh(*cplx, color=c2)
        flat = cplx.flatten().translate([0, -1.1 , -0.1])
        if flat:    
            triangular_mesh(*flat, color=c2)

view(-90, 75, 30)
show()

