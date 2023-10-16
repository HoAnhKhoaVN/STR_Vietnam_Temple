from copy import deepcopy
from typing import List, Text, Dict
import numpy as np
import cv2
import os
from time import time

OFFSETS = [(0, 1),
            (1, 0), 
            (0, -1), 
            (-1, 0), 
            (-1, -1), 
            (-1, 1), 
            (1, -1), 
            (1, 1)]
def get_neighbors_of_a_pixel(  # Cython
    x: int,
    y: int,
    height: int,
    width: int
)->List:
    neighbors = [(x,y)]
    for dx, dy in OFFSETS:
        new_x, new_y = x+dx, y+dy

        # Check if the new coordinates are within the bounds of the image
        if 0<= new_x < height and 0<= new_y < width:
            neighbors.append((new_x, new_y))
    return neighbors

def is_stable(
    J: np.ndarray,
    new_J: np.ndarray
)->bool:
    # print("J")
    # print(J)
    # print("new_J")
    # print(new_J)
    return np.all(J == new_J)


def bg_rm_lqn(
    I # grayscale
):
    # region 0. Read the image and preprocess the image
    # I = 255 - I  # Inverse pixel
    cdef Py_ssize_t H = I.shape[0]
    cdef Py_ssize_t W = I.shape[1]
    J = np.zeros(I.shape, dtype=np.uint8)
    K = np.zeros(I.shape, dtype=np.uint8)

    J[0, :] = I[0, :] # Top edge
    J[H-1, :] = I[H-1, :] # Bottom edge
    J[:, 0] = I[:, 0] # Left edge
    J[:, W-1] = I[:, W-1] # Right 

    cdef unsigned char[:, :] J_view = J
    cdef unsigned char[:, :] K_view = K

    # region get neighbors
    cor2neighbor = dict()
    cdef Py_ssize_t x, y
    cdef unsigned char tmp
    # cdef N_G_p
    for x in range(H):# Cython
        for y in range(W):
            N_G_p = get_neighbors_of_a_pixel(
                x = x,
                y = y,
                height= H,
                width= W
            )
            cor2neighbor[(x,y)] = N_G_p
    # endregion
    new_J = deepcopy(J)
    # endregion
    count= 0


    while True:
        count+=1
        # print(f"Loop time {count}")
        # region 1. Image K => Cython
        for x in range(H):
            for y in range(W):
                J_q = max(list(map(lambda a, b : J[a,b], cor2neighbor[(x,y)])))
                K[x,y] =J_q
        # endregion


        # region 2. Image J 
        # Step 2
        new_J = np.minimum(K, I)
        # endregion

        if is_stable(
            J = J,
            new_J = new_J
        ):
            break
        J = new_J

    BR = I - J
    
    return BR, J