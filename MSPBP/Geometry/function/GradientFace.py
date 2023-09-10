# -*- coding: utf-8 -*-

# @Time    : 2019/3/4 08:07
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#    
# ======================================================

import numpy as np
import ctypes

from MSPBP.Utils.ConverUtil import Convert2DToCArray


def gradientFace(V, F, fun):
    '''
    计算三角形网格曲面上的顶点函数fun的梯度
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param fun: 顶点函数，大小为n*1矩阵
    :return: 大小为m*3矩阵，第i行为第i个三角面片的梯度
    '''
    rowf, colf = F.shape
    rowv, colv = V.shape
    fun = np.array(fun).reshape((rowv, 1))
    gradient = np.zeros((rowf, 3))

    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)
    Cgradient = Convert2DToCArray(gradient, ctypes.c_float)
    Cfun = Convert2DToCArray(fun, ctypes.c_float)

    gradientDLL = ctypes.CDLL("gradient.dll")
    gradientDLL.gradientFace(Cv_list, Cf_list, rowf, Cfun, Cgradient)

    gradient = np.array(Cgradient)
    return gradient
