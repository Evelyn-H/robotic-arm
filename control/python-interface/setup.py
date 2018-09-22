from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

examples_extension = Extension(
    "clib",
    ["clib.pyx", "clib/examples.c"],
    include_dirs=["clib"]
)

setup(
    name="clib",
    ext_modules=cythonize([examples_extension])
)
