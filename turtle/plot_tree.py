from turtle import *

speed('fastest')
rt(-90)
angle = 30


def plot_tree(sz, level):
    if level > 0:
        colormode(255)
        pencolor(0, 255 // level, 0)
        fd(sz)
        rt(angle)
        plot_tree(0.8 * sz, level - 1)
        pencolor(0, 255 // level, 0)
        lt(2 * angle)
        plot_tree(0.8 * sz, level - 1)
        pencolor(0, 255 // level, 0)
        rt(angle)
        fd(-sz)


plot_tree(80, 7)
