# -*- coding: utf-8 -*-

# @Time    : 2019/5/6 20:39
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
from scipy.sparse import coo_matrix


from MSPBP.Geometry.Matrix import graphAdjacencyMatrix


def meanEdgeLength(V, F):
    '''
    计算模型的平均边长
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为 m*3
    :return: 边的平均长度，int
    '''
    W = graphAdjacencyMatrix(F)
    W = W.tocoo()
    row,col = W.row,W.col
    edge = V[row, :] - V[col, :]
    edgeLength = np.sqrt(np.sum(np.power(edge, 2), axis=1))
    meanLength = np.mean(edgeLength)
    return meanLength

def meanEdgeLength1Ring(V,F):
    '''
    计算一环邻域的平均边长
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为 m*3
    :return: 一环邻域的平均边长，二维数组，大小为 n*1
    '''
    W = graphAdjacencyMatrix(F)
    W = W.tocoo()
    row, col = W.row, W.col
    edge = V[row, :] - V[col, :]
    edgeLength = np.sqrt(np.sum(np.power(edge, 2), axis=1))

    M = coo_matrix((edgeLength,(row,col)),shape=(W.shape))

    meanLength = np.mean(M,axis=1)
    return meanLength
