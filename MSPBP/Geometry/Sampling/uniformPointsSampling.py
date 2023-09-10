# -*- coding: utf-8 -*-

# @Time    : 2019/5/12 16:23
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
from MSPBP.Geometry.Area import FacetArea


def uniformPointsSampling(V, F, N):
    '''
    通过随机过程进行顶点取样
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param N: 取样点的个数，数据类型int
    :return: 取样点的下标，一维数组大小为N
    '''
    area = FacetArea(V, F)
    cumArea = np.cumsum(area)
    samples = []
    for i in range(N):
        randNum = np.random.rand() * cumArea[-1]
        z = np.abs(cumArea - randNum)
        indexOfFacet = np.argmin(z)
        p1 = V[F[indexOfFacet][0]]
        p2 = V[F[indexOfFacet][1]]
        p3 = V[F[indexOfFacet][2]]
        r1 = np.random.rand()
        r2 = np.random.rand()
        sample = (1 - np.sqrt(r1)) * p1 + np.sqrt(r1) * (1 - r2) * p2 + np.sqrt(r1) * r2 * p3
        samples.append(sample)
    samples = np.array(samples)
    return samples
