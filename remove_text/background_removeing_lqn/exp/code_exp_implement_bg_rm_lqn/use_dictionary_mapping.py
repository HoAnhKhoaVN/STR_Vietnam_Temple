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
            (1, 1),
            (0,0)]
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
    return np.all(J == new_J)


def bg_rm_lqn(
    I: np.ndarray, # grayscale
)-> np.ndarray:
    s = time()
    # region 0. Read the image and preprocess the image
    I = 255 - I  # Inverse pixel
    H, W = I.shape
    J = np.zeros(I.shape, dtype=np.uint8)
    K = np.zeros(I.shape, dtype=np.uint8)

    J[0, :] = I[0, :] # Top edge
    J[H-1, :] = I[H-1, :] # Bottom edge
    J[:, 0] = I[:, 0] # Left edge
    J[:, W-1] = I[:, W-1] # Right 
    e = time()
    print(f'Time preprocessing: {e-s} s')
    # region get neighbors

    s = time()
    cor2neighbor = dict()
    for x in range(H):
        for y in range(W):
            N_G_p = get_neighbors_of_a_pixel(
                x = x,
                y = y,
                height= H,
                width= W
            )
            cor2neighbor[(x,y)] = N_G_p
    # endregion
    e = time()
    print(f'Time get neighbors: {e-s} s')

    new_J = deepcopy(J)
    # endregion
    count= 0

    lst_time_step_1 = []
    lst_time_step_2 = []
    while True:
        count+=1
        # print(f"Loop time {count}")
        # region 1. Image K => Cython
        s = time()
        for x in range(H):
            for y in range(W):
                J_q = list(map(lambda cor : J[cor], cor2neighbor[(x,y)]))
                K[x,y] = max(J_q)
        # K = get_max_pixel_convonlution(J)
        e = time()
        lst_time_step_1.append((e-s))
        # print(f'Time step 1: {(e-s)} s ')
        # endregion


        # region 2. Image J 
        # Step 2
        s = time()
        new_J = np.minimum(K, I)
        # endregion

        if is_stable(
            J = J,
            new_J = new_J
        ):
            break
        J = new_J
        e = time()
        lst_time_step_2.append((e-s))
    BR = I - J

    print(f"Average time step 1: {np.mean(lst_time_step_1)}")
    print(f"Average time step 2: {np.mean(lst_time_step_2)}")
    
    return BR, J


def run_use_dict_mapping_python():
    image_fn= 'test.png'
    addition_fn= 'use_dict_mapping_python'
    ROOT = ''
    # image_fn = '35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'test_2.png'
    # image_fn = 'test_3.png'
    # image_fn = 'test_4.png'
    # region get filename
    img_name = image_fn.split('/')[-1].split('.')[0]+'_'+ addition_fn
    fd_name = os.path.join(ROOT, img_name)
    os.makedirs(
        name = fd_name,
        exist_ok= True
    )
    # endregion

    I = cv2.imread(image_fn, cv2.IMREAD_GRAYSCALE)
    print(f'Shape image: {I.shape}')
    # I = np.random.randint(
    #     low = 0,
    #     high= 256,
    #     size = (5, 5)
    # )
    s = time()
    BR, J = bg_rm_lqn(
        I = I,
    )
    e = time()
    print(f"Time remove background with code python: {e-s} s")
    
    # BR = I - J
    _, thresh = cv2.threshold(BR, 0, 255, cv2.THRESH_BINARY)
    cv2.imwrite(
        filename= os.path.join(fd_name, f'I_{img_name}.png'),
        img= I
    )
    cv2.imwrite(
        filename= os.path.join(fd_name, f'J_{img_name}.png'),
        img = J
    )

    cv2.imwrite(
        filename= os.path.join(fd_name,f'BR_{img_name}.png'),
        img = BR
    )

    cv2.imwrite(
        filename= os.path.join(fd_name, f'BR_threshold_{img_name}.png'),
        img = thresh
    )

    cv2.imwrite(
        filename= os.path.join(fd_name, f'J_reinverse_{img_name}.png'),
        img = 255 - J
    )

if __name__ == '__main__':
    run_use_dict_mapping_python()