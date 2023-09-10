# -*- coding: utf-8 -*-

# @Time    : 2019/4/1 16:48
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
from scipy.sparse import coo_matrix



def triangles(V, F):
    """
    Actual triangles of the mesh (points, not indexes)

    Returns
    ---------
    triangles : (n, 3, 3) float
      Points of triangle vertices
    """
    # use of advanced indexing on our tracked arrays will
    # trigger a change flag which means the MD5 will have to be
    # recomputed. We can escape this check by viewing the array.
    triangles = V.view(np.ndarray)[F]
    return triangles


def faces_sparse(V, F):
    """
    Return a sparse matrix for which vertices are contained in which faces.

    Returns
    ---------
    sparse: scipy.sparse.coo_matrix of shape (column_count, len(faces))
            dtype is boolean

    Examples
     ----------
    In [1]: sparse = faces_sparse(len(mesh.vertices), mesh.faces)

    In [2]: sparse.shape
    Out[2]: (12, 20)

    In [3]: mesh.faces.shape
    Out[3]: (20, 3)

    In [4]: mesh.vertices.shape
    Out[4]: (12, 3)

    In [5]: dense = sparse.toarray().astype(int)

    In [6]: dense
    Out[6]:
    array([[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
           [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
           [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
           [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1]])

    In [7]: dense.sum(axis=0)
    Out[7]: array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    """
    column_count = len(V)
    indices = np.asanyarray(F)

    row = indices.reshape(-1)
    col = np.tile(np.arange(len(indices)).reshape(
        (-1, 1)), (1, indices.shape[1])).reshape(-1)

    shape = (column_count, len(indices))
    data = np.ones(len(col), dtype=np.bool)
    sparse = coo_matrix((data, (row, col)),
                        shape=shape,
                        dtype=np.bool)
    return sparse


def face_angles_sparse(V, F):
    _triangles = triangles(V, F)
    from . import triangles as tr
    angles = tr.angles(_triangles)
    _faces_sparse = faces_sparse(V, F)
    matrix = coo_matrix((angles.flatten(), (_faces_sparse.row, _faces_sparse.col)),
                        _faces_sparse.shape)
    return matrix
