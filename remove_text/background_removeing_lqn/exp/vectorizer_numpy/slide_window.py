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
    pad  = 1

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
    select_img=pad_img[i,j].squeeze().transpose()
    K = np.max(select_img, axis=-1).reshape(img_h, img_w)
    # endregion

    # region bitwise and
    res = np.multiply(K,mask)
    nz = np.nonzero(res)  # Indices of all nonzero elements
    arr_trimmed = res[nz[0].min():nz[0].max()+1,
                    nz[1].min():nz[1].max()+1]
    
    # endregion
    return arr_trimmed

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

def get_neighbors_of_a_pixel_naive(  # Cython
    x: int,
    y: int,
    height: int,
    width: int,
    iamge: np.ndarray
)->List:
    neighbors = []
    for dx, dy in OFFSETS:
        new_x, new_y = x+dx, y+dy

        # Check if the new coordinates are within the bounds of the image
        if 0<= new_x < height and 0<= new_y < width:
            neighbors.append(iamge[new_x, new_y])
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

def bg_rm_lqn_naive(
    I: np.ndarray, # grayscale
    debug: bool = True
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

    # if debug:
    #     print("======I ====")
    #     print(I)
    #     print("===== J ====")
    #     print(J)
    #     print(f'== get_neighbors_of_a_pixel ==')
    #     nb00 = get_neighbors_of_a_pixel(
    #             x=0,
    #             y=0,
    #             height= H,
    #             width= W
    #         )
    #     print(f"Neighbors of a pixel (0,0): {nb00}")
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
                J_q = get_neighbors_of_a_pixel_naive(
                    x,
                    y,
                    H,
                    W,
                    J
                )
                # print(f'J_q: {J_q}')
                K[x,y] = max(J_q)
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
    
def bg_rm_lqn(
    I: np.ndarray, # grayscale
    debug: bool = True
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
    # print(f'Time preprocessing: {e-s} s')
    # region get neighbors

    # s = time()
    # cor2neighbor = dict()
    # for x in range(H):# Cython
    #     for y in range(W):
    #         N_G_p = get_neighbors_of_a_pixel(
    #             x = x,
    #             y = y,
    #             height= H,
    #             width= W
    #         )
    #         cor2neighbor[(x,y)] = N_G_p
    # endregion
    # e = time()
    # print(f'Time get neighbors: {e-s} s')

    # if debug:
    #     print("======I ====")
    #     print(I)
    #     print("===== J ====")
    #     print(J)
    #     print(f'== get_neighbors_of_a_pixel ==')
    #     nb00 = get_neighbors_of_a_pixel(
    #             x=0,
    #             y=0,
    #             height= H,
    #             width= W
    #         )
    #     print(f"Neighbors of a pixel (0,0): {nb00}")
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
        # for x in range(H):
        #     for y in range(W):
        #         J_q = list(map(lambda cor : J[cor], cor2neighbor[(x,y)]))
        #         K[x,y] = max(J_q)
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

def run_code_python():
    image_fn= 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test.png'
    addition_fn= 'code_python'
    ROOT = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/exp/bg_rm_lqn_cython'
    # image_fn = '35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_2.png'
    # image_fn = 'test_3.png'
    image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_4.png'
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
        debug= False
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
    image_fn= 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test.png'
    addition_fn= 'slide_window'
    ROOT = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/exp/bg_rm_lqn_cython'
    image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/35227268_1442578812555603_8324419005091676160_n.jpg'
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_2.png'
    # image_fn = 'D:/Master/OCR_Nom/fulllow_ocr_temple/remove_text/background_removeing_lqn/test_3.png'
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
    #     size = (5, 6)
    # )
    s = time()
    BR, J = bg_rm_lqn(
    # BR, J = bg_rm_lqn_naive(
        I = I,
        debug= False
    )
    e = time()
    print(f"Time remove background: {e-s} s")
    
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
    