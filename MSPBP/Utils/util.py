# -*- coding: utf-8 -*-

# @Time    : 2019/4/1 15:59
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
from itertools import combinations

# include constants here so we don't have to import
# a floating point threshold for 0.0
# we are setting it to 100x the resolution of a float64
# which works out to be 1e-13
TOL_ZERO = np.finfo(np.float64).resolution * 100
# how close to merge vertices
TOL_MERGE = 1e-8


def unitize(vectors,
            check_valid=False,
            threshold=None):
    """
    Unitize a vector or an array or row- vectors.

    Parameters
    ---------
    vectors : (n,m) or (j) float
       Vector or vectors to be unitized
    check_valid :  bool
       If set, will return mask of nonzero vectors
    threshold : float
       Cutoff for a value to be considered zero.

    Returns
    ---------
    unit :  (n,m) or (j) float
       Input vectors but unitized
    valid : (n,) bool or bool
        Mask of nonzero vectors returned if `check_valid`
    """
    # make sure we have a numpy array
    vectors = np.asanyarray(vectors)

    # allow user to set zero threshold
    if threshold is None:
        threshold = TOL_ZERO

    if len(vectors.shape) == 2:
        # for (m, d) arrays take the per- row unit vector
        # using sqrt and avoiding exponents is slightly faster
        # also dot with ones is faser than .sum(axis=1)
        norm = np.sqrt(np.dot(vectors * vectors,
                              [1.0] * vectors.shape[1]))
        # non-zero norms
        valid = norm > threshold
        # in-place reciprocal of nonzero norms
        norm[valid] **= -1
        # tile reciprocal of norm
        tiled = np.tile(norm, (vectors.shape[1], 1)).T
        # multiply by reciprocal of norm
        unit = vectors * tiled
    elif len(vectors.shape) == 1:
        # treat 1D arrays as a single vector
        norm = np.sqrt((vectors * vectors).sum())
        valid = norm > threshold
        if valid:
            unit = vectors / norm
        else:
            unit = vectors.copy()
    else:
        raise ValueError('vectors must be (n, ) or (n, d)!')

    if check_valid:
        return unit[valid], valid
    return unit

import scipy.sparse

def csr_row_set_nz_to_val(csr, row, value=0):
    """Set all nonzero elements (elements currently in the sparsity pattern)
    to the given value. Useful to set to 0 mostly.
    """
    if not isinstance(csr, scipy.sparse.csr_matrix):
        raise ValueError('Matrix given must be of CSR format.')
    csr.data[csr.indptr[row]:csr.indptr[row + 1]] = value


def csr_rows_set_nz_to_val(csr, rows, value=0):
    for row in rows:
        csr_row_set_nz_to_val(csr, row)
    if value == 0:
        csr.eliminate_zeros()
