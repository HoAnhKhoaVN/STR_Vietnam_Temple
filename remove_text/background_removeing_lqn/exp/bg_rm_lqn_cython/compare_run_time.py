from naive_python import run_naive_python
from use_dictionary_mapping import run_use_dict_mapping_python
from run import run_boundscheck_wrapare
from use_convolution import run_use_convolution
from sliding_window import run_sliding_window

if __name__ == '__main__':
    print(f"==== RUN NAIVE PYTHON =====")
    run_naive_python()

    print(f"==== USE DICTIONARY MAPPING =====")
    run_use_dict_mapping_python()

    print(f"==== CYTHON =====")
    run_boundscheck_wrapare()

    print(f"==== CONVOLUTION =====")
    run_use_convolution()
    
    print(f"==== SLIDING WINDOW NUMPY =====")
    run_sliding_window()

