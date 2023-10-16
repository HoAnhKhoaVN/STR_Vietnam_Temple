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

def get_neighbors_of_a_pixel_naive(  # Cython
    x: int,
    y: int,
    height: int,
    width: int,
    image: np.ndarray
)->List:
    neighbors = []
    for dx, dy in OFFSETS:
        new_x, new_y = x+dx, y+dy

        # Check if the new coordinates are within the bounds of the image
        if 0<= new_x < height and 0<= new_y < width:
            neighbors.append(image[new_x, new_y])
    return neighbors

def is_stable(
    J: np.ndarray,
    new_J: np.ndarray
)->bool:
    return np.all(J == new_J)

def bg_rm_lqn_naive(
    I: np.ndarray, # grayscale
)-> np.ndarray:
    s = time()
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
    new_J = deepcopy(J)
    # endregion
    count= 0

    lst_time_step_1 = []
    lst_time_step_2 = []
    while True:
        count+=1
        # Bước 1
        s = time()
        for x in range(H):
            for y in range(W):
                J_q = get_neighbors_of_a_pixel_naive(x,y,H,W,J)
                K[x,y] = max(J_q)
        e = time()
        lst_time_step_1.append((e-s))
        # Bước 2
        s = time()
        new_J = np.minimum(K, I)
        e = time()
        lst_time_step_2.append((e-s))
        # Đừng khi J ổn định
        if is_stable(J = J,new_J = new_J):
            break
        J = new_J
    BR = I - J

    print(f"Average time step 1: {np.mean(lst_time_step_1)}")
    print(f"Average time step 2: {np.mean(lst_time_step_2)}")
    
    return BR, J

def run_naive_python():
    image_fn= 'test.png'
    addition_fn= 'naive_python'
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
    BR, J = bg_rm_lqn_naive(
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
    run_naive_python()