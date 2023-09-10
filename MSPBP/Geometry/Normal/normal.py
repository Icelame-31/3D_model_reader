# -*- coding: utf-8 -*-

# @Time    : 2019/4/1 16:50
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================
from MSPBP.Utils import base,triangles,util


def facetNormals(V, F):
    '''
    计算面片法向量
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :return: 面片法向量，大小为 m*3
    '''
    _triangles = base.triangles(V, F)
    normals = triangles.normals(_triangles)
    return normals

def vertexNormals(V,F):
    '''
    计算顶点的法向量
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :return: 顶点的法向量，大小为 n*3
    '''
    face_normals = facetNormals(V,F)
    sparse = base.faces_sparse(V,F)
    summed = sparse.dot(face_normals)
    vertex_normals = util.unitize(summed)
    return vertex_normals

