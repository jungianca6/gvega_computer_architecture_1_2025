import numpy as np


IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
GRID_SIZE = 4  # 4x4 = 16 cuadrantes


def extraerCuadrante(img_array, quadrant_num):
    row = (quadrant_num - 1) // GRID_SIZE
    col = (quadrant_num - 1) % GRID_SIZE

    quad_h = IMAGE_HEIGHT // GRID_SIZE
    quad_w = IMAGE_WIDTH // GRID_SIZE

    start_y = row * quad_h
    end_y = start_y + quad_h
    start_x = col * quad_w
    end_x = start_x + quad_w

    return img_array[start_y:end_y, start_x:end_x]

def guardarImg(cuadrante_array, path):
    cuadrante_array.astype(np.uint8).tofile(path)

def cargarImg(path, shape):
    return np.fromfile(path, dtype=np.uint8).reshape(shape)