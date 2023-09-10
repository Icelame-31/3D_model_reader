# -*- coding: utf-8 -*-

# @Time    : 2019/3/4 10:34
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#       
# ======================================================

import numpy as np
import ctypes

from MSPBP.Utils.ConverUtil import Convert2DToCArray


def divergence(V, F, G):
    '''
    计算三角形网格曲面上向量场的散度
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param G: 大小为m*3矩阵，第i行为第i个面片上的向量
    :return: 大小为n*1矩阵，第i个值为第i个顶点上的函数值
    '''
    rowf, colf = F.shape
    rowv, colv = V.shape
    div = np.zeros((rowv, 1))

    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)
    Cgradient = Convert2DToCArray(G, ctypes.c_float)
    Cdiv = Convert2DToCArray(div, ctypes.c_float)

    gradientDLL = ctypes.CDLL("gradient.dll")
    gradientDLL.divergence(Cv_list, Cf_list, rowf, Cgradient, Cdiv)

    div = np.array(Cdiv)
    return div
