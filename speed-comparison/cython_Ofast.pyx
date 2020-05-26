#distutils: language = c++
# cython: language_level=3 
#distutils: extra_compile_args = -Wno-unused-function -Wno-unneeded-internal-declaration -Ofast
import numpy as np
cimport numpy as np
from libc.math cimport exp, pow
cimport cython
DTYPE = np.float32

@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.initializedcheck(False)
@cython.overflowcheck(False)
def cython_simple(X, y, bw):

    cdef Py_ssize_t n = X.shape[0]

    result = np.zeros((n), dtype=DTYPE)
    cdef float[:] result_view = result
    cdef Py_ssize_t i 

    for i in range(n):
        W = np.exp(-0.5*((X - X[i])/bw)**2.)
        W /= W.sum()
        result_view[i] = np.sum(y*W)
    return result
import numpy as np
cimport numpy as np
from libc.math cimport exp, pow
cimport cython
DTYPE = np.float32



@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.initializedcheck(False)
@cython.overflowcheck(False)
cpdef cython_full(float[::1] X, float[::1] y, float bw):

    cdef Py_ssize_t n = X.shape[0]

    result = np.zeros((n), dtype=DTYPE)
    cdef float[::1] result_view = result
    cdef float[::1] W = np.zeros(n,dtype=DTYPE)
    cdef float tmp
    cdef Py_ssize_t i, j

    with nogil:
        for i in range(n):
            tmp = 0
            for j in range(n):
                W[j] = exp(-.5*pow((X[j] - X[i])/bw,2.))
                tmp += W[j]
            for j in range(n):
                result_view[i] += y[j]*W[j]/tmp
    return result
