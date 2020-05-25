import numpy as np
__all__ = [
    'numpy_for_loop',
    'jax_map',
    # 'jax_vmap',
    'cython_Ofast_simple',
    'cython_Ofast_full',
    'cython_O3_simple',
    'cython_O3_full',
    'tf_map',
]


def numpy_for_loop(X, y, bw):
    S = np.zeros_like(X)
    for i in range(X.shape[0]):
        W = np.exp(-0.5*((X - X[i])/bw)**2.)
        W = W/np.sum(W)
        S[i] = np.sum(y*W)
    return S

from jax import numpy as jnp
from jax import jit, vmap
from jax.lax import map


def _jax_row(Xi, X, y, bw):
    W = jnp.exp(-0.5*((X - Xi)/bw)**2.)
    W = W/jnp.sum(W)
    return jnp.sum(y*W)


def jax_map(X, y, bw):
    return np.asarray(map(lambda Xi: _jax_row(Xi, X, y, bw), X))


# def jax_vmap(X, y, bw):
#     return vmap(lambda X: _jax_row(X, y, bw), X)


import cython_Ofast

def cython_Ofast_simple(X, y, bw):
    return cython_Ofast.cython_simple(X, y, bw)


def cython_Ofast_full(X, y, bw):
    return cython_Ofast.cython_full(X, y, bw)

import cython_O3

def cython_O3_simple(X, y, bw):
    return cython_O3.cython_simple(X, y, bw)


def cython_O3_full(X, y, bw):
    return cython_O3.cython_full(X, y, bw)

import tensorflow as tf

#Disable CUDA devices
from os import environ
environ["CUDA_VISIBLE_DEVICES"] = "-1"

def tf_map(X, y, bw, parallel_iterations=1000):
    bw = tf.stop_gradient(tf.convert_to_tensor(X, dtype=tf.float32))
    X = tf.stop_gradient(tf.convert_to_tensor(X, dtype=tf.float32))
    y = tf.stop_gradient(tf.convert_to_tensor(y, dtype=tf.float32))

    @tf.function
    def _tf_map(X, y, bw):
        def _tf_row(Xi):
            W = tf.math.exp(-0.5*((X - Xi)/bw)**2.)
            W = W/tf.reduce_sum(W)
            return tf.reduce_sum(y*W)
        return tf.map_fn(_tf_row, X, parallel_iterations=parallel_iterations)

    return _tf_map(X, y, bw)

