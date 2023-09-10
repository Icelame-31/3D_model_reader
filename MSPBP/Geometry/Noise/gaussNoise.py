# -*- coding: utf-8 -*-

# @Time    : 2019/5/12 17:32
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np


def gaussNoise(m, n, meanValue, varValue):
    '''
    生成高斯噪声矩阵，该矩阵大小为m*n
    :param m: 高斯噪声矩阵的行数，数据类型 int
    :param n: 高斯噪声矩阵的列数，数据类型 int
    :param meanValue: 均值，数据类型 int
    :param varValue: 方差，数据类型 int
    :return: 高斯噪声矩阵，大小为m*n
    '''
    noise = meanValue + varValue * np.random.rand(m, n)
    return noise
