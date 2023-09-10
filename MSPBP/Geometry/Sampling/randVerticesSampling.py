# -*- coding: utf-8 -*-

# @Time    : 2019/5/9 14:24
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np


def randVerticesSampling(V, F, N):
    '''
    随机取样法，进行顶点取样
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param N: 取样点的个数，数据类型int
    :return: 取样点的下标，一维数组大小为N
    '''
    n = V.shape[0]
    sample = np.random.randint(0, n, (N,))
    return sample
