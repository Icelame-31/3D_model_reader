# -*- coding: utf-8 -*-

# @Time    : 2019/4/1 16:52
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np

from MSPBP.Utils import util

def cross(triangles):
    """
    Returns the cross product of two edges from input triangles

    Parameters
    --------------
    triangles: (n, 3, 3) float
      Vertices of triangles

    Returns
    --------------
    crosses : (n, 3) float
      Cross product of two edge vectors
    """
    vectors = np.diff(triangles, axis=1)
    crosses = np.cross(vectors[:, 0], vectors[:, 1])
    return crosses

def area(triangles=None, crosses=None, sum=False):
    """
    Calculates the sum area of input triangles

    Parameters
    ----------
    triangles : (n, 3, 3) float
      Vertices of triangles
    crosses : (n, 3) float or None
      As a speedup don't re- compute cross products
    sum : bool
      Return summed area or individual triangle area

    Returns
    ----------
    area : (n,) float or float
      Individual or summed area depending on `sum` argument
    """
    if crosses is None:
        crosses = cross(triangles)
    area = (np.sum(crosses**2, axis=1)**.5) * .5
    if sum:
        return np.sum(area)
    return area

def normals(triangles=None, crosses=None):
    """
    Calculates the normals of input triangles

    Parameters
    ------------
    triangles : (n, 3, 3) float
      Vertex positions
    crosses : (n, 3) float
      Cross products of edge vectors

    Returns
    ------------
    normals : (m, 3) float
      Normal vectors
    valid : (n,) bool
      Was the face nonzero area or not
    """
    if crosses is None:
        crosses = cross(triangles)
    # unitize the cross product vectors
    unit= util.unitize(crosses)
    return unit

def angles(triangles):
    """
    Calculates the angles of input triangles.

    Parameters
    ------------
    triangles : (n, 3, 3) float
      Vertex positions

    Returns
    ------------
    angles : (n, 3) float
      Angles at vertex positions, in radians
    """

    # get a vector for each edge of the triangle
    u = triangles[:, 1] - triangles[:, 0]
    v = triangles[:, 2] - triangles[:, 0]
    w = triangles[:, 2] - triangles[:, 1]

    # normalize each vector in place
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    w /= np.linalg.norm(w, axis=1, keepdims=True)

    # run the cosine and an einsum that definitely does something
    a = np.arccos(np.clip(np.einsum('ij, ij->i', u, v), -1, 1))
    b = np.arccos(np.clip(np.einsum('ij, ij->i', -u, w), -1, 1))
    c = np.pi - a - b

    return np.column_stack([a, b, c])