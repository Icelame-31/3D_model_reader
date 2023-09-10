# -*- coding: utf-8 -*-

# @Time    : 2019/3/7 10:03
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#            
# ======================================================


import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def ConLinSys_least(A, B, ConIndex, ConValue, s):
    '''
    极小化下述线性最小二乘能量：min(||A*X - B||^2 + \sum_{j = 1}^{m}||s(j) * (X(ConIndex(j),:) - ConValue(j,:))||^2)
    参考论文 SMI 2009 paper "Dynamic harmonic fields for surface processing",
    :param A: 二维矩阵，大小为 n*n
    :param B: 二维矩阵，大小为 n*k
    :param ConIndex: 一维数组，大小为 m
    :param ConValue:  二维矩阵，大小为 m*k
    :param s: 二维矩阵，大小为 m*1
    :return: 求解结果，二维矩阵，大小为 n*k
    '''

    ConValue = np.array(ConValue)

    n = A.shape[1]
    w = np.zeros((n, 1))
    w[ConIndex, :] = s
    W = sparse.coo_matrix((w.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tolil()
    W = W[ConIndex, :]
    A = sparse.vstack((A, W)).tocsc()

    m = len(s)
    W1 = sparse.coo_matrix((s.flat, (np.arange(m), np.arange(m))), shape=(m, m)).tocsc()
    ConValue = sparse.coo_matrix(ConValue).tocsc()
    B = sparse.coo_matrix(B).tocsc()
    B = sparse.vstack((B, W1.dot(ConValue)))

    B = B.todense()
    X = spsolve(A.T.dot(A), A.T.dot(B))
    return X
