# -*- coding: utf-8 -*-

# @Time    : 2019/3/7 8:21
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================         
# ======================================================


import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from MSPBP.Utils import util


def ConLinSys_substitution(A, B, ConIndex, ConValue):
    '''
    使用替代法求解带约束的线性方程组：A * X = B s.t A(ConIndex,:) = ConValue
    参考论文 SMI 2009 paper "Dynamic harmonic fields for surface processing",
    :param A: 二维矩阵，大小为 n*n
    :param B: 二维矩阵，大小为 n*k
    :param ConIndex: 一维数组，大小为 m
    :param ConValue:  二维矩阵，大小为 m*k
    :return: 求解结果，二维矩阵，大小为 n*k
    '''
    ConValue = np.array(ConValue)

    A = A.tocsr()
    # Change the matrix A
    util.csr_rows_set_nz_to_val(A, ConIndex)
    A = A.tolil()
    for index in ConIndex:
        A[index, index] = 1.0

    # Change the matix B
    B[ConIndex, :] = ConValue

    # A = sparse.csc_matrix(A)
    A = A.tocsc()
    B = sparse.csc_matrix(B)
    X = spsolve(A, B).toarray()
    return X
