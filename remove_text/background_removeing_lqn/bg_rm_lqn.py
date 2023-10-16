from copy import deepcopy
from typing import List, Text, Dict
import numpy as np
import cv2
import os
from time import time

OFFSETS = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
def get_neighbors_of_a_pixel(
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
    I: np.ndarray, # grayscale
    debug: bool = True
)-> np.ndarray:
    # region 0. Read the image and preprocess the image
    I = 255 - I  # Inverse pixel
    H, W = I.shape
    J = np.zeros(I.shape, dtype=np.uint8)
    K = np.zeros(I.shape, dtype=np.uint8)

    J[0, :] = I[0, :] # Top edge
    J[H-1, :] = I[H-1, :] # Bottom edge
    J[:, 0] = I[:, 0] # Left edge
    J[:, W-1] = I[:, W-1] # Right 

    # J[0, :] = 0.3 # Top edge
    # J[H-1, :] = 0.3 # Bottom edge
    # J[:, 0] = 0.3 # Left edge
    # J[:, W-1] = 0.3 # Right 

    # region get neighbors
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
    if debug:
        print("======I ====")
        print(I)
        print("===== J ====")
        print(J)
        print(f'== get_neighbors_of_a_pixel ==')
        nb00 = get_neighbors_of_a_pixel(
                x=0,
                y=0,
                height= H,
                width= W
            )
        print(f"Neighbors of a pixel (0,0): {nb00}")
    new_J = deepcopy(J)
    # endregion
    count= 0


    while True:
        count+=1
        print(f"Loop time {count}")
        # region 1. Image K
        for x in range(H):
            for y in range(W):
                J_q = list(map(lambda cor : J[cor], cor2neighbor[(x,y)]))
                K[x,y] = max(J_q)
        # J_5 = J +5
        # J_10 = J +10
        # J_15 = J + 15
        # print(J_5)
        # print(J_10)
        # print(J_15)
        
        K = np.maximum(np.maximum(J+5, J+10), J+15)
        # print(K)
        exit(0)
        
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
        


if __name__ == "__main__":
    # image_fn= 'test.png'
    # image_fn = '35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'test_2.png'
    # image_fn = 'test_3.png'
    # image_fn = 'test_4.png'
    image_fn = 'test.png'
    # region get filename
    img_name = image_fn.split('.')[0]+'_am_ban'
    # img_name = image_fn.split('.')[0]+'_duong_ban'
    os.makedirs(
        name = img_name,
        exist_ok= True
    )
    # endregion


    I = cv2.imread(image_fn, cv2.IMREAD_GRAYSCALE)
    print(f'Shape image: {I.shape}')
    I = np.random.randint(
        low = 0,
        high= 256,
        size = (5, 5)
    )
    print(I)
    s = time()
    BR, J = bg_rm_lqn(
        I = I,
        debug= False
    )
    e = time()
    print(f"Time remove background: {e-s} s")
    
    # BR = I - J
    _, thresh = cv2.threshold(BR, 0, 255, cv2.THRESH_BINARY)
    cv2.imwrite(
        filename= os.path.join(img_name, f'I_{img_name}.png'),
        img= I
    )
    cv2.imwrite(
        filename= os.path.join(img_name, f'J_{img_name}.png'),
        img = J
    )

    cv2.imwrite(
        filename= os.path.join(img_name,f'BR_{img_name}.png'),
        img = BR
    )

    cv2.imwrite(
        filename= os.path.join(img_name, f'BR_threshold_{img_name}.png'),
        img = thresh
    )

    cv2.imwrite(
        filename= os.path.join(img_name, f'J_reinverse_{img_name}.png'),
        img = 255 - J
    )
    