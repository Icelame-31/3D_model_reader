# -*- coding: utf-8 -*-

# @Time    : 2019/5/9 14:24
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import random
import numpy as np

from MSPBP.Geometry.Distance import geodesicDistance_dijkstra


def farthestVerticesSampling_dijkstra(V, F, N):
    '''
    通过dijsktra方法进行测地距取样
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param N: 取样点的个数，数据类型int
    :return: 取样点的下标，一维数组大小为N
    '''
    n = V.shape[0]
    sample = [round(n * random.random())]
    d = np.full((n, 1), np.inf)
    for k in range(N - 1):
        _in = sample
        D = geodesicDistance_dijkstra(V, F, _in)
        D = D.T
        d = np.min(D,axis=1)
        idx = np.argmax(d)
        sample.append(idx)
    sample = np.array(sample)
    return sample

def farthestVerticesSampling(V, F, N):
    '''
    通过测地距取样
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param N: 取样点的个数，数据类型int
    :return: 取样点的下标，一维数组大小为N
    '''
    try:
        import gdist
    except:
        RuntimeError("导入gdist失败，请先安装tvb-geodesic工具包")
    n = V.shape[0]
    sample = [round(n * random.random())]
    d = np.full((n, 1), np.inf)
    for k in range(N - 1):
        _in = np.array(sample).astype(np.int32)
        D = gdist.compute_gdist(V,F,source_indices=_in)
        D = D.T
        d = D
        idx = np.argmax(d)
        sample.append(idx)
    sample = np.array(sample)
    return sample