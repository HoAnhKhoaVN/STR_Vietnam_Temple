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
    
    return BR, J

def run_opencv_morphology(
    image_fn : str
):
    # image_fn= 'test.png'
    # image_fn = 'in1.jpg'
    # image_fn = '35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'IMG/sptn-page3-fig1-so01.jpeg'
    # image_fn = 'IMG/sptn-page3-fig2-so02.jpeg'
    # image_fn = 'IMG/sptn-page7-fig2-so13.jpeg'
    addition_fn= 'opencv_morphology'
    ROOT = ''
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_2.png'
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
    #     size = (5, 5),
    #     dtype= np.uint8
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
        img = 255-BR
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
    # # region construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    # help="path to input image")
    # args = vars(ap.parse_args())
    # # endregion
    img_fn = 'IMG/z4821586225415_68730dadf6fecfe6ce6937fb69704506.jpg'
    run_opencv_morphology(img_fn)