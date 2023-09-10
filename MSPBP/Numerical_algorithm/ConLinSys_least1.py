# -*- coding: utf-8 -*-

# @Time    : 2019/4/14 12:12
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def ConLinSys_least1(A, B, ConIndex, ConValue):
    '''
    极小化下述带约束的线性最小二乘能量： ||A*X-B||^2 s.t X(ConIndex,:) = ConValue
    参考论文 SMI 2009 paper "Dynamic harmonic fields for surface processing",
    :param A: 二维矩阵，大小为 n*n
    :param B: 二维矩阵，大小为 n*k
    :param ConIndex: 一维数组，大小为 m
    :param ConValue:  二维矩阵，大小为 m*k
    :return: 求解结果，二维矩阵，大小为 n*k
    '''
    ConValue = np.array(ConValue)

    # The unknowns index
    unIndex = np.arange(0, A.shape[1])
    for index in ConIndex:
        unIndex[index] = -1
    unIndex = np.where(unIndex > -1)[0]

    # Change the matrix B
    B1 = A[:, ConIndex].dot(ConValue)
    B = B - B1

    # Change the matrix A
    A = A[:, unIndex]
    A = A.tocsc()
    B = sparse.coo_matrix(B).tocsc()

    unKnows = spsolve(A.T.dot(A).tocsc(), A.T.dot(B).tocsc())

    X = np.zeros((len(unIndex) + len(ConIndex), B.shape[1]))
    unKnows = unKnows.toarray()
    X[unIndex, :] = unKnows
    X[ConIndex, :] = ConValue
    return X
