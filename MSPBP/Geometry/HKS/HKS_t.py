# -*- coding: utf-8 -*-

# @Time    : 2019/5/7 11:01
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================
from scipy.sparse import coo_matrix
import numpy as np

def HKS_t(evecs, evals, A, t, scale):
    '''
    计算时间为t的HKS, 参考论文： "A Concise and Provably Informative Multi-Scale Signature
    Based on Heat Diffusion"
    :param evecs: 该矩阵中的每列是Laplace-Beltrami算子的第i个本征函数
    :param evals: 该向量中的第i个元素是Laplace-Beltrami算子的第i个特征值
    :param A: 该向量中的第i个元素是与第i个顶点相关联的区域
    :param t: 时间参数t
    :param scale: 布尔类型
    :return: 该矩阵中的第i行是第i个顶点的热核签名
    '''
    if scale == True:
        t1 = np.abs(evals[1]) - np.abs(evals[1:])
        t1 = t1.reshape(len(t1),1)
        hks = np.power(np.abs(evecs[:, 1:]), 2).dot(np.exp(t1 * t))
        n = len(A)
        Am = coo_matrix((A, (np.arange(n), np.arange(n))), shape=(n, n))
        colsum = np.sum(Am * hks, axis=0)
        scale = 1.0 / colsum
        n2 = len(scale)
        scalem = coo_matrix((scale, (np.arange(n2), np.arange(n2))), shape=(n2, n2))
        hks = hks * scalem
    else:
        hks = np.power(np.abs(evecs[:, 1:]), 2) * np.exp((-1) * np.abs(evals[1:]) * t)
    return hks