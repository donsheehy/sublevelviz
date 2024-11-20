from sublevelviz import *
from delaunay import Del

if __name__ == '__main__':
    from math import sin, cos, pi
    def f(x,y):
        x = abs(x) # exploit some symmetry
        r = 0.5
        if y >= 0:
            return 1 - abs(dist([x,y], [0,0]) - r)
        elif y >= -r:
            return 1 - abs(x - r)
        else:
            return 1-dist([x,y], [r,-r])

    def ease(t):
        t *= 2
        if t < 1:
            return t * t * t / 2
        else:
            t -= 2
            return (t * t * t + 2) / 2

    def smooth(f, bottom, top):
        def smoothed_f(x,y):
            v = max(f(x,y), bottom)
            s = top-bottom
            alpha = ease((v - bottom)/s)
            return (1-alpha) * bottom + alpha * top
        return smoothed_f

    horseshoe = smooth(f, 0.5, 1)

    I = [-1, -.5,-.2, 0, .3, .5, .7,1]
    B = [-1, 1]
    # P = [[x,y] for x in I for y in I]
    BDY = [[x,y] for x in I for y in B] + [[x,y] for x in B for y in I]
    n = 20
    pt = lambda i: [0.5 * cos(i*pi/n), 0.5 * sin(pi*i/n)]
    SEMICIRCLE = [pt(i) for i in range(n)]
    LINES = [[x,y] for x in [-0.5, 0.5] for y in [-0.1, -0.2, -0.3,-0.4, -0.5]]
    P = BDY + SEMICIRCLE + LINES + [[0,0]]

    D = Sub(horseshoe, Del(P))
    t = 1000
    c = (0.78, 0.78, 0.78)
    black = (0,0,0)
    fig = figure(bgcolor=(1, 1, 1))
    # triangular_mesh(*F(t), tube_radius=0.2, color=c)
    triangular_mesh(*D(t), color=c)
    triangular_mesh(*D(t), representation='wireframe', color=black, tube_radius=0.5)


    G = Grid(200,200)
    F = Sub(horseshoe, G)

    t = 100

    # triangular_mesh(*F(t), color=c)
    
    show()
