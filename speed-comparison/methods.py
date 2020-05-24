import numpy as np
__all__ = [
    'numpy_for_loop',
    'jax_map',
    # 'jax_vmap',
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
    return map(lambda Xi: _jax_row(Xi, X, y, bw), X)


# def jax_vmap(X, y, bw):
#     return vmap(lambda X: _jax_row(X, y, bw), X)