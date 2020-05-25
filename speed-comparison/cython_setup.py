from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("*.pyx"),
)
# setup(
#     ext_modules = cythonize("cython_Ofast.pyx", extra_compile_args =["-O3"]),
# )
# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Distutils import build_ext

# setup(
#   name = 'speedy',
#   ext_modules=[
#     Extension('cython_Ofast',
#               sources=['cython_Ofast.pyx'],
#               extra_compile_args=['-Ofast'],
#               language='c++')
#     ],
#   cmdclass = {'build_ext': build_ext}
# )
# setup(
#   name = 'speedy',
#   ext_modules=[
#     Extension('cython_O3',
#               sources=['cython_O3.pyx'],
#               extra_compile_args=['-O3'],
#               language='c++')
#     ],
#   cmdclass = {'build_ext': build_ext}
# )