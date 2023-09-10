# -*- coding: utf-8 -*-

# @Time    : 2019/5/7 11:01
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

from scipy.sparse import coo_matrix
from math import log, fabs
import numpy as np


def HKS(evecs, evals, A, scale):
    '''
    计算HKS, 参考论文： "A Concise and Provably Informative Multi-Scale Signature
    Based on Heat Diffusion"
    :param evecs: 该矩阵中的每列是Laplace-Beltrami算子的第i个本征函数
    :param evals: 该向量中的第i个元素是Laplace-Beltrami算子的第i个特征值
    :param A: 该向量中的第i个元素是与第i个顶点相关联的区域
    :param scale: 布尔类型
    :return: 该矩阵中的第i行是第i个顶点的热核签名
    '''
    tmin = fabs(4 * log(10) / np.max(evals))
    tmax = fabs(4 * log(10) / np.min(evals))
    nstep = 100

    stepsize = (log(tmax) - log(tmin)) / nstep
    logts = np.arange(start=log(tmin), step=stepsize, stop=log(tmax))
    ts = np.exp(logts)

    if scale == True:
        t1 = np.abs(evals[1]) - np.abs(evals[1:])
        t1 = t1.reshape(len(t1),1)
        ts = ts.reshape(1,len(ts))
        hks = np.power(np.abs(evecs[:, 1:]), 2).dot(np.exp(t1 * ts))
        n = len(A)
        Am = coo_matrix((A, (np.arange(n), np.arange(n))), shape=(n, n))
        colsum = np.sum(Am * hks, axis=0)
        scale = 1.0 / colsum
        n2 = len(scale)
        scalem = coo_matrix((scale, (np.arange(n2), np.arange(n2))), shape=(n2, n2))
        hks = hks * scalem
    else:
        hks = np.power(np.abs(evecs[:, 1:]), 2) * np.exp((-1) * np.abs(evals[1:]) * ts)
    return hks
