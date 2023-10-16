import numpy as np
def get_max_pixel_convonlution(
    image: np.ndarray
)-> np.ndarray:
    # region hyper_paramater
    img_h , img_w = image.shape
    ker_h, ker_w = 3,3
    pad , stride = 1,1
    # endregion

    # region padding
    pad_img = np.pad(
        array= image,
        pad_width= (pad,pad),
        mode='constant',
        constant_values=0
    )
    # endregion

    # region index caculate
    out_h= int((img_h-ker_h)+(2*pad)/stride) +1  #output height with same padding(10).
    out_w= int((img_w-ker_w)+(2*pad)/stride) +1  #output width with same padding(10).
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
    return K


if __name__ == '__main__':
    image = np.random.randint(low= 0, high= 256, dtype= np.uint8, size = (6,5))
    print(f'image: {image}')
    pad_img = np.pad(
        array= image,
        pad_width= (1,1),
        mode='constant',
        constant_values=0
    )
    print(f'pad_img: {pad_img}')
    img_h , img_w = 6,5
    ker_h, ker_w = 3,3
    pad , stride = 1,1
    out_h= int((img_h-ker_h)+(2*pad)/stride) +1  #output height with same padding(10).
    out_w= int((img_w-ker_w)+(2*pad)/stride) +1  #output width with same padding(10).

    print(f'(out_h, out_w) = ({out_h},{out_w})')

    i0=np.repeat(np.arange(ker_h), ker_h)
    i1=np.repeat(np.arange(img_h), img_h)
    j0=np.tile(np.arange(ker_w), ker_h)
    j1=np.tile(np.arange(img_h), img_w)
    i=i0.reshape(-1,1)+i1.reshape(1,-1)

    print(f'i = {i}')
    print(f'i shape = {i.shape}')
    j=j0.reshape(-1,1)+j1.reshape(1,-1)
    print(f'j shape= {j.shape}')

    select_img=pad_img[i,j].squeeze().transpose()
    K = np.max(select_img, axis=-1).reshape(img_h, img_w)
    print(f'K = {K}')