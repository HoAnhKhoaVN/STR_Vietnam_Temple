from time import time
import code_cython
import compute_memview
import boundscheck_wraparound
import contiguous
import generic_code
import multi_process
import pure_python
import numpy as np


if __name__ == "__main__":
    # region Setup
    array_1 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
    array_2 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
    a, b, c = 4, 3, 9
    # endregion

    # # region Pure python
    # start = time()
    # pure_python.compute(
    #     array_1,
    #     array_2,
    #     a,
    #     b,
    #     c
    # )
    # end = time()
    # print(f'Run time python: {end - start} s')
    # # endregion

    # # region main
    # start = time()
    # code_cython.compute(
    #     array_1,
    #     array_2,
    #     a,
    #     b,
    #     c
    # )
    # end = time()
    # print(f'Run time cython: {end - start} s')
    # # endregion

    # region memview
    start = time()
    compute_memview.compute(
        array_1,
        array_2,
        a,
        b,
        c
    )
    end = time()
    print(f'Run time memview: {end - start} s')
    # endregion

    # region memview, dont check bound and negative indexes
    start = time()
    boundscheck_wraparound.compute(
        array_1,
        array_2,
        a,
        b,
        c
    )
    end = time()
    print(f'Run time memview, dont check bound and negative indexes: {end - start} s')
    # endregion

    # region memview
    contiguous.compute(
        array_1,
        array_2,
        a,
        b,
        c
    )
    end = time()
    print(f'Run time contiguous: {end - start} s')
    # endregion

    # region generic code
    generic_code.compute(
        array_1,
        array_2,
        a,
        b,
        c
    )
    end = time()
    print(f'Run time generic code: {end - start} s')
    # endregion
    
    # region multi process
    multi_process.compute(
        array_1,
        array_2,
        a,
        b,
        c
    )
    end = time()
    print(f'Run time multi process: {end - start} s')
    # endregion