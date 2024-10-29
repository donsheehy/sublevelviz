from sublevelviz import *

def max_extension(P, t=1):
    def f(x,y):
        return min(pz + (t * dist([x, y], [px, py])) for px, py, pz in P)
    return f

def min_extension(P, t=1):
    def f(x,y):
        return max(pz - (t * dist([x, y], [px, py])) for px, py, pz in P)
    return f

if __name__ == '__main__':
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
