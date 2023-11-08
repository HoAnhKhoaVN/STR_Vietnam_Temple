import argparse
from copy import deepcopy
import numpy as np
import cv2
import os
from time import time
    
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
        # region 1. Image K
        s = time()

        K = cv2.dilate(
            src = J,
            kernel= cv2.getStructuringElement(
                shape= cv2.MORPH_RECT,
                ksize= (3,3)
            ),
            iterations= 1,
        )
        # print(f'K: {K}')
        e = time()
        lst_time_step_1.append((e-s))
        # endregion


        # region 2. Image J 
        # Step 2
        s = time()
        new_J = cv2.min(
            src1 = K,
            src2 = I,
        )
        # endregion

        if cv2.countNonZero(cv2.subtract(new_J,J)) == 0:
            break
        J = new_J
        e = time()
        lst_time_step_2.append((e-s))

    BR = I - J
    print(f'Count: {count}')
    print(f"Average time step 1: {np.mean(lst_time_step_1)}")
    print(f"Average time step 2: {np.mean(lst_time_step_2)}")
    
    return BR

if __name__ == "__main__":
    IMG_PATH = 'che_phong/img'
    OUT_RM_BG = 'che_phong/bg_rm_lqn'
    for img_name in os.listdir(IMG_PATH):
        image_fn = os.path.join(IMG_PATH, img_name)
        I = cv2.imread(image_fn, cv2.IMREAD_GRAYSCALE)
        BR= bg_rm_lqn(I = I)
        cv2.imwrite(
            filename= os.path.join(OUT_RM_BG,img_name),
            img = BR
        )