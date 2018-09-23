import os, glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

c_files = glob.glob(os.path.join('clib', '*.c'))

examples_extension = Extension(
    "clib",
    ["clib.pyx"] + c_files,

    include_dirs=["clib"]
)

setup(
    name="clib",
    ext_modules=cythonize([examples_extension])
)
