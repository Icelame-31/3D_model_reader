# -*- coding: utf-8 -*-

# @Time    : 2019/5/7 10:16
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
import numpy as np

from MSPBP.Geometry.Matrix import cotangentLaplacian_noNormalize
from MSPBP.Geometry.Area import MixedArea


def eigenDecoLaplacian(V, F, k):
    '''
    计算拉普拉斯矩阵特征向量和特征值
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面，大小为 m*3
    :param k: 期望的特征值和特征向量的数量，数据类型 int
    :return:
    eigvalue - 特征值
    eigvector - 特征向量
    mixedArea - 点的混合面积
    '''
    W = cotangentLaplacian_noNormalize(V, F)
    mixedArea = MixedArea(V, F)

    n = len(mixedArea)
    A = coo_matrix((mixedArea, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    eigvalue, eigvector = eigsh(W, k=k, M=A, which='SM')
    return eigvalue, eigvector, mixedArea
