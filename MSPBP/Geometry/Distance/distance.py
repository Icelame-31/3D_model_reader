# -*- coding: utf-8 -*-

# @Time    : 2019/4/7 21:44
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np
import ctypes
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

from MSPBP.Utils.ConverUtil import Convert1DToCArray, Convert2DToCArray


def geodesicDistance_dijkstra(V, F, point_list):
    '''
    用dijkstra方法计算下标为point_list的点到所有点的测地距离
    :param V: 模型的点, 大小为 n*3
    :param F: 模型的面片, 大小为m*3
    :param point_list: 一些点的下标, 一维数组
    :return: 下标为point_list的点到所有点的测地距离，二维数组，大小为 point_list中点的个数 * n
    '''
    point_list = np.array(point_list)
    rowf, colf = F.shape
    rowv, colv = V.shape

    Ir = np.zeros((3 * rowf,), dtype=int)
    Jr = np.zeros((3 * rowf,), dtype=int)
    Vr = np.zeros((3 * rowf,), dtype=float)

    CIr = Convert1DToCArray(ctypes.c_int * len(Ir), Ir)
    CJr = Convert1DToCArray(ctypes.c_int * len(Jr), Jr)
    CVr = Convert1DToCArray(ctypes.c_float * len(Vr), Vr)
    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    distanceDLL = ctypes.CDLL("distance.dll")
    distanceDLL.distanceMatrix(Cv_list, Cf_list, rowf, CIr, CJr, CVr)

    Ir = np.array(CIr)
    Jr = np.array(CJr)
    Vr = np.array(CVr)

    graphDistanceMatrix = coo_matrix((Vr, (Ir, Jr)), shape=(rowv, rowv)).tocsc()
    D = dijkstra(graphDistanceMatrix, indices=point_list)
    return D



def geodesicDistance_single(V, F, i):
    '''
    使用gdist方法计算某个点到所有点的测地距离
    gdist 是一个python第三方工具包,详细信息请查看 https://github.com/the-virtual-brain/tvb-geodesic
    :param V: 模型的点,大小为 n*3
    :param F: 模型的面片,大小为 m*3
    :param i: 某个点的下标.  int
    :return: 某个点到所有点的测地距, 二维数组大小为：1*n
    '''
    try:
        import gdist
    except:
        RuntimeError("导入gdist失败，请先安装tvb-geodesic工具包")
    src = np.array([i])
    D = gdist.compute_gdist(V, F, source_indices=src)
    return D


def geodesicDistance_multiple(V, F, point_list):
    '''
    使用gdist方法，计算某些点彼此之间的测地距
    gdist 是一个python第三方工具包,详细信息请查看 https://github.com/the-virtual-brain/tvb-geodesic
    :param V: 模型的点,大小为 n*3
    :param F: 模型的面片,大小为 m*3
    :param point_list: 点的下标，一维数组
    :return: 测地距矩阵，二维，大小为 l*l， l为point_list的大小
    例如，返回矩阵为d，d(i,j）表示下标为i的点到下标为j的点的测地距离
    '''
    try:
        import gdist
    except:
        RuntimeError("导入gdist失败，请先安装tvb-geodesic工具包")
    trg = np.array(point_list)
    D = []
    for point in point_list:
        d = gdist.compute_gdist(V, F, source_indices=np.array([point]), target_indices=trg)
        D.append(d)
    D = np.array(D)
    return D


def geodesicDistance_pair(V, F, point_pairs):
    '''
    计算每对点之间的测地距离
    :param V: 模型的点,大小为 n*3
    :param F: 模型的面片,大小为 m*3
    :param point_pairs: 每对点下标值, 二维数组，且该数组只有两列，因为每行表示两个配对点。
                例如: [[2,4],
                      [5,8],
                      [100,1000]]
    :return: 每对点的下标及他们之间的测地距, 格式类似于 [pairid distance]
            [[(2, 4) 10.856139624223475]
            [(5, 8) 10.667389971624317]
            [(100, 1000) 86.42070108348551]]
    '''
    try:
        import gdist
    except:
        RuntimeError("导入gdist失败，请先安装tvb-geodesic工具包")
    point_pairs = np.array(point_pairs)
    assert point_pairs.shape[1] == 2, '计算距离的点必须成对出现，你需要传入一个n*2矩阵'
    D = []
    for pair in point_pairs:
        d = gdist.compute_gdist(V, F, source_indices=np.array([pair[0]]), target_indices=np.array([pair[1]]))
        D.append([(pair[0], pair[1]), float(d)])
    D = np.array(D)
    return D


def commuteTimeDistance(eigvector, eigvalue, i):
    '''
    计算所有点到下标为i的点的通勤距离
    :param eigvector: 特征向量，二维数组
    :param eigvalue: 特征值，一维数组
    :param i: 某点的下标
    :return: 一维数组，大小为点的个数
    '''
    eigvector = eigvector[:, 1:]
    eigvalue = eigvalue[1:]
    n = eigvector.shape[0]

    data = (-1.0) * np.ones((n,))
    matrix = coo_matrix((data, (np.arange(n), np.arange(n))), shape=(n, n)).tolil()
    matrix[:, i] = 1.0
    matrix[i, :] = 0.0
    M = matrix * eigvector
    M = M ** 2

    eigvalue = 1.0 / eigvalue
    d = M * eigvalue
    return d


def diffusionDistance(eigvector, eigvalue, i, t):
    '''
    计算所有点到下标为i顶点的时间参数为t的扩散距离
    :param eigvector: 特征向量，二维数组
    :param eigvalue: 特征值，一维数组
    :param i: 下标值
    :param t: 时间参数
    :return: 一维数组，大小为点的个数
    '''
    eigvector = eigvector[:, 1:]
    eigvalue = eigvalue[1:]
    n = eigvector.shape[0]

    data = (-1.0) * np.ones((n,))
    matrix = coo_matrix((data, (np.arange(n), np.arange(n))), shape=(n, n)).tolil()
    matrix[:, i] = 1.0
    matrix[i, :] = 0.0
    M = matrix * eigvector
    M = M ** 2

    eigvalue = np.exp(-2.0 * t * eigvalue)
    d = M * eigvalue
    return d


def biHarmonicDistance(eigvector, eigvalue, i):
    '''
    计算所有点到下标为i的点的双调和距离
    :param eigvector: 特征向量，二维数组
    :param eigvalue: 特征值，一维数组
    :param i: 下标值
    :return: 一维数组，大小为点的个数
    '''
    eigvector = eigvector[:, 1:]
    eigvalue = eigvalue[1:]
    n = eigvector.shape[0]

    data = (-1.0) * np.ones((n,))
    matrix = coo_matrix((data, (np.arange(n), np.arange(n))), shape=(n, n)).tolil()
    matrix[:, i] = 1.0
    matrix[i, :] = 0.0
    M = matrix * eigvector
    M = M ** 2

    eigvalue = 1.0 / np.power(eigvalue, 2)
    d = M * eigvalue
    return d
