import numpy as np

def clip(
    a,
    min_value,
    max_value
):
    return min(max(a, min_value), max_value)

DTYPE = np.intc
def compute(
    array_1,
    array_2,
    a,
    b,
    c
):
    x_max = array_1.shape[0]
    y_max = array_1.shape[1]

    assert array_1.shape == array_2.shape
    assert array_1.dtype == DTYPE
    assert array_2.dtype == DTYPE

    res = np.zeros(
        shape= (x_max, y_max),
        dtype= DTYPE
    )

    tmp = 0
    for x in range(x_max):
        for y in range(y_max):
            tmp = clip(
                a = array_1[x,y],
                min_value= 2,
                max_value= 10
            )

            tmp = tmp * a + array_2[x,y] *b
            res[x, y] = tmp + c


    return res