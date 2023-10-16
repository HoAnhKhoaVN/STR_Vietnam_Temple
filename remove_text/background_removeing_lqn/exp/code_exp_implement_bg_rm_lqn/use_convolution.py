from copy import deepcopy
from typing import List, Text, Dict
import numpy as np
import cv2
import os
from time import time

def get_max_pixel_convonlution(
    image: np.ndarray
)-> np.ndarray:
    # region hyper_paramater
    img_h , img_w = image.shape
    ker_h, ker_w = 3,3
    pad , stride = 1,1

    pad_value = 0.0
    square_img = np.zeros(2 * [max(image.shape)], dtype=np.uint8)
    square_img[:img_h, :img_w] = image
    # endregion

    # region get mask
    mask = np.zeros(2 * [max(image.shape)], dtype=np.uint8)
    valid_image = np.ones_like(image)
    mask[:img_h, :img_w] = valid_image

    # print(f'Mask: {mask}')
    # endregion

    # region padding
    pad_img = np.pad(
        array= square_img,
        pad_width= (pad, pad),
        mode='constant',
        constant_values=0
    )
    # print(f'pad_img :{pad_img}')
    img_h , img_w = square_img.shape
    # endregion

    # print(f'square_img: {square_img}')

    # region index caculate
    # out_h= int((img_h-ker_h)+(2*pad)/stride) +1  #output height with same padding(10).
    # out_w= int((img_w-ker_w)+(2*pad)/stride) +1  #output width with same padding(10).
    i0=np.repeat(np.arange(ker_h), ker_h)
    i1=np.repeat(np.arange(img_h), img_h)
    j0=np.tile(np.arange(ker_w), ker_h)
    j1=np.tile(np.arange(img_h), img_w)
    i=i0.reshape(-1,1)+i1.reshape(1,-1)
    j=j0.reshape(-1,1)+j1.reshape(1,-1)
    # endregion

    # region calculate maximum pixel
    # print(f'pad_img.shape:  {pad_img.shape}')
    # print(f'i.shape:  {i.shape}')
    # print(f'j.shape:  {j.shape}')
    select_img=pad_img[i,j].squeeze().transpose()
    K = np.max(select_img, axis=-1).reshape(img_h, img_w)
    # endregion

    # region bitwise and
    res = np.multiply(K,mask)
    nz = np.nonzero(res)  # Indices of all nonzero elements
    arr_trimmed = res[nz[0].min():nz[0].max()+1,
                    nz[1].min():nz[1].max()+1]

    

    # endregion
    # print(f'K: {K}')
    # print(f'K.shape: {K.shape}')

    # res = K[...,mask]
    # print(f'res: {res}')
    # print(f'res.shape: {res.shape}')

    # print(f'res: {arr_trimmed}')
    # print(f'res.shape: {arr_trimmed.shape}')
    return arr_trimmed

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
        K = get_max_pixel_convonlution(J)
        e = time()
        lst_time_step_1.append((e-s))
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


def run_use_convolution():
    image_fn= 'test.png'
    addition_fn= 'run_use_convolution'
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
    run_use_convolution()