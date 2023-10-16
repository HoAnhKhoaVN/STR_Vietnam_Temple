from copy import deepcopy
from typing import List, Text, Dict
import numpy as np
import cv2
import os
from time import time


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
    new_J = deepcopy(J)
    # endregion
    count= 0

    lst_time_step_1 = []
    lst_time_step_2 = []
    while True:
        count+=1
        # print(f"Loop time {count}")
        # region 1. Image K
        s = time()
        pad_img = np.pad(
            array= J,
            pad_width= (1,1),
            mode='constant',
            constant_values=0
        )
        tmp = np.lib.stride_tricks.sliding_window_view(
            x = pad_img,
            window_shape=(3,3)
        )
        tmp = tmp.reshape(-1,9)

        K = np.max(tmp, axis= -1 ).reshape(J.shape)
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
        # print(f'Time step 2: {(e-s)} s ')

    BR = I - J



    print(f"Average time step 1: {np.mean(lst_time_step_1)}")
    print(f"Average time step 2: {np.mean(lst_time_step_2)}")
    
    return BR, J

def run_sliding_window():
    image_fn= 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test.png'
    addition_fn= 'sliding_window_numpy'
    ROOT = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/exp/bg_rm_lqn_cython'
    # image_fn = '35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_2.png'
    # image_fn = 'test_3.png'
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_4.png'
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
        
if __name__ == "__main__":
    run_sliding_window()