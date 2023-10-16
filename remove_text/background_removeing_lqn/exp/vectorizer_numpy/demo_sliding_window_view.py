import numpy as np


if __name__ == '__main__':
    image = np.random.randint(low= 0, high= 256, dtype= np.uint8, size = (6,5))
    print(f'image: {image}')
    pad_img = np.pad(
        array= image,
        pad_width= (1,1),
        mode='constant',
        constant_values=0
    )

    res = np.lib.stride_tricks.sliding_window_view(
        x = pad_img,
        window_shape=(3,3)
    )
    res = res.reshape(-1,9)
    print(res.shape)
    K = np.max(res, axis= -1 ).reshape(image.shape)
    print(f'K : {K}')
    # print(res)