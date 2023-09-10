# -*- coding: utf-8 -*-

# @Time    : 2019/3/6 15:49
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#  参考论文 SMI 2009 paper "Dynamic harmonic fields for surface processing" 
# ======================================================

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def ConLinSys_elimination(A, B, ConIndex, ConValue):
    '''
    使用消元法求解带约束的线性方程组：A * X = B s.t A(ConIndex,:) = ConValue
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
    B = B - A[:, ConIndex] * ConValue
    B = B[unIndex, :]

    # %Change the matrix A, get unIndex row & unIndex col
    A = A[unIndex]  # first get unIndex row
    A = A[:, unIndex]  # then get unIndex col

    # The solution
    # t = cputime
    A = A.tocsc()
    B = coo_matrix(B).tocsc()

    unKnows = spsolve(A, B)

    # disp('The time of the linear system:');
    # cputime - t
    X = np.zeros((len(unIndex) + len(ConIndex), B.shape[1]))
    unKnows = unKnows.toarray()
    X[unIndex, :] = unKnows
    X[ConIndex, :] = ConValue
    return X
