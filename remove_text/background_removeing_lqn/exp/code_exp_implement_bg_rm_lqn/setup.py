from setuptools import setup
from Cython.Build import cythonize

setup(
    # ext_modules = cythonize("code_cython.pyx
    ext_modules = cythonize("boundscheck_wrapare.pyx")
)