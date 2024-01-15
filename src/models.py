import numpy as np
from math import sqrt

def sierpinski_make(size, level):
    pyramids = []

    height = size * sqrt(6) / 3

    sierpinski((0, height, 0), size, level, pyramids)

    return pyramids

def sierpinski(top, size, level, pyramids):
    if level <= 1:
        pyramids.append(top)
        return
    
    size /= 2
    sierpinski(top, size, level - 1, pyramids)

    vertexA = (top[0], top[1] - size * sqrt(6) / 3, top[2] + size * sqrt(3)/3)
    sierpinski(vertexA, size, level -1, pyramids)

    vertexB = (top[0] - size / 2, top[1] - size * sqrt(6) / 3, top[2] - size * sqrt(3)/6)
    sierpinski(vertexB, size, level - 1, pyramids)

    vertexC = (top[0] + size / 2, top[1] - size * sqrt(6) / 3, top[2] - size * sqrt(3)/6)
    sierpinski(vertexC, size, level - 1, pyramids)
    

vertices = np.array([
    # vertex positions              # normals                   # tex coords
    -0.5, -0.8165, -0.288,          0.0, -1.0, 0.0,             1.0, 0.0,
    0.5, -0.8165, -0.288,           0.0, -1.0, 0.0,             0.0, 0.0,
    0.0, -0.8165, 0.577,            0.0, -1.0, 0.0,             0.5, 1.0,

    -0.5, -0.8165, -0.288,          0.0, 0.288, -0.8165,        1.0, 0.0,
    0.5, -0.8165, -0.288,           0.0, 0.288, -0.8165,        0.0, 0.0,
    0.0, 0.0, 0.0,                  0.0, 0.288, -0.8165,        0.5, 1.0,

    0.5, -0.8165, -0.288,           0.706, 0.289, 0.408,     1.0, 0.0,
    0.0, -0.8165, 0.577,            0.706, 0.289, 0.408,     0.0, 0.0,
    0.0, 0.0, 0.0,                  0.706, 0.289, 0.408,     0.5, 1.0,

    -0.5, -0.8165, -0.288,          -0.706, 0.289, 0.408,       0.0, 0.0,
    0.0, -0.8165, 0.577,            -0.706, 0.289, 0.408,       1.0, 0.0,
    0.0, 0.0, 0.0,                  -0.706, 0.289, 0.408,       0.5, 1.0,

    ], dtype = np.float32)

floor_vertices = np.array([
    -100, 0, -100,                0.0, 1.0, 0.0,              0.0, 0.0,
    -100, 0, 100,                 0.0, 1.0, 0.0,              0.0, 30.0,
    100, 0, 100,                  0.0, 1.0, 0.0,              30.0, 30.0,

    100, 0, 100,                  0.0, 1.0, 0.0,              30.0, 30.0, 
    100, 0, -100,                 0.0, 1.0, 0.0,              30.0, 0.0,
    -100, 0, -100,                0.0, 1.0, 0.0,              0.0, 0.0
    ], dtype = np.float32)