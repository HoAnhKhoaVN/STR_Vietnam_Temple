import cv2
import os
from time import time
# import code_cython
# import compute_memview
import boundscheck_wrapare
import numpy as np
# from baseline import run_code_python

def run_boundscheck_wrapare():
    image_fn= 'test.png'
    addition_fn= 'boundscheck_wrapare'
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
    #     size = (5, 5),
    #     dtype= np.uint8
    # )
    s = time()
    BR, J = boundscheck_wrapare.bg_rm_lqn(
        I = 255-I,
    )
    e = time()
    print(f"Time remove background with boundscheck_wrapare: {e-s} s")
    
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
    # run_code_python()
    # run_code_cython()
    # run_compute_memory()
    run_boundscheck_wrapare()

