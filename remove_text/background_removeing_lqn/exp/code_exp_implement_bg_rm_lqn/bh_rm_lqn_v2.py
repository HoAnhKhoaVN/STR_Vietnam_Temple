from copy import deepcopy
from typing import List, Text, Dict
import numpy as np
import cv2
import os
from time import time

def bg_rm_lqn_v2(
    I: np.ndarray, # grayscale
)-> np.ndarray:
    s = time()
    # region 0. Read the image and preprocess the image
    # I = 255 - I  # Inverse pixel
    H, W = I.shape
    # J = np.zeros(I.shape, dtype=np.uint8)
    # K = np.zeros(I.shape, dtype=np.uint8)

    # J[0, :] = I[0, :] # Top edge
    # J[H-1, :] = I[H-1, :] # Bottom edge
    # J[:, 0] = I[:, 0] # Left edge
    # J[:, W-1] = I[:, W-1] # Right 
    # e = time()

    # new_J = deepcopy(J)
    # endregion

    # region step 1
    pad_img = np.pad(
            array= I,
            pad_width= (1,1),
            mode='edge',
        )
    
    print(f'pad_img: {pad_img}')
    tmp = np.lib.stride_tricks.sliding_window_view(
            x = pad_img,
            window_shape=(3,3)
        )
    tmp = tmp.reshape(-1,9)
    print(f'tmp_I: {tmp}')
    b = 15
    F_x_y = np.min(tmp-b, axis= -1).reshape(I.shape)

    print(f'F_x_y: {F_x_y}')

    pad_img = np.pad(
            array= F_x_y,
            pad_width= (1,1),
            mode='edge',
        )
    tmp = np.lib.stride_tricks.sliding_window_view(
            x = pad_img,
            window_shape=(3,3)
        )
    tmp = tmp.reshape(-1,9)

    F_add_y = np.max(tmp+b, axis= -1).reshape(I.shape)
    print(f'F_add_y: {F_add_y}')

    # endregion


    # region step 2
    BR = I - F_add_y
    print(f'BR: {BR}')
    # endregion
    

    # print(f"Average time step 1: {np.mean(lst_time_step_1)}")
    # print(f"Average time step 2: {np.mean(lst_time_step_2)}")
    
    return BR, F_add_y


def run_bg_rm_lqn_v2():
    image_fn= 'test.png'
    addition_fn= '__v2'
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
    I = np.random.randint(
        low = 0,
        high= 256,
        size = (5, 5)
    )
    print(f'I: {I}')
    s = time()
    BR, J = bg_rm_lqn_v2(
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
    run_bg_rm_lqn_v2()