import numpy as np

DTYPE = np.intc

cdef int clip(
    int a,
    int min_value,
    int max_value
):
    return min(max(a, min_value), max_value)


def compute(
    array_1,
    array_2,
    int a,
    int b,
    int c
):
    cdef Py_ssize_t x_max = array_1.shape[0]
    cdef Py_ssize_t y_max = array_1.shape[1]

    assert array_1.shape == array_2.shape
    assert array_1.dtype == DTYPE
    assert array_2.dtype == DTYPE

    res = np.zeros(
        shape= (x_max, y_max),
        dtype= DTYPE
    )

    cdef int tmp

    cdef Py_ssize_t x, y

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

