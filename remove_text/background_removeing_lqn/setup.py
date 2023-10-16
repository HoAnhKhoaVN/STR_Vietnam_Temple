from setuptools import setup
from Cython.Build import cythonize

setup(
    # ext_modules = cythonize("demo_cython.pyx")
    ext_modules = cythonize("compute_memview.pyx")
)