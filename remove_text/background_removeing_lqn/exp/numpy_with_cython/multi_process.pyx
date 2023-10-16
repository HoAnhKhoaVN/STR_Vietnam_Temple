import numpy as np
cimport cython
from cython.parallel import prange

DTYPE = np.intc

cdef int clip(
    int a,
    int min_value,
    int max_value
) nogil:
    return min(max(a, min_value), max_value)

@cython.boundscheck(False)
@cython.wraparound(False)
def compute(
    int[:, :] array_1,
    int[:, :] array_2,
    int a,
    int b,
    int c
):
    cdef Py_ssize_t x_max = array_1.shape[0]
    cdef Py_ssize_t y_max = array_1.shape[1]

    assert tuple(array_1.shape) == tuple(array_2.shape)

    res = np.zeros(
        shape= (x_max, y_max),
        dtype= DTYPE
    )

    cdef int[:, :] res_view = res

    cdef int tmp
    cdef Py_ssize_t x, y



    for x in prange(x_max, nogil = True):
        for y in range(y_max):
            tmp = clip(
                a = array_1[x,y],
                min_value= 2,
                max_value= 10
            )

            tmp = tmp * a + array_2[x,y] *b
            res_view[x, y] = tmp + c
    return res

