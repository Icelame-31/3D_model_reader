# -*- coding: utf-8 -*-

# @Time    : 2019/3/4 19:42
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
# ======================================================

import numpy as np
import ctypes

from MSPBP.Utils.ConverUtil import Convert1DToCArray, Convert2DToCArray
from MSPBP.Geometry.Matrix import cotangentLaplacian_noNormalize
from MSPBP.Geometry.Normal import normal
from MSPBP.Geometry.Area import VertexCellArea


def gaussCurvatures(V, F):
    '''
    计算模型的高斯曲率
    :param V: 模型的点, 大小为 n*3
    :param F: 模型的面片, 大小为 m*3
    :return: 模型的高斯曲率，一维数组，大小为n，即点的个数
    '''
    rowf, colf = F.shape
    rowv, colv = V.shape
    gaussCur = np.zeros((rowv,), dtype=float)

    CgaussCur = Convert1DToCArray(ctypes.c_float * len(gaussCur), gaussCur)
    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    curvatureDLL = ctypes.CDLL("Curvatures.dll")
    curvatureDLL.gaussCurvatures(Cv_list, Cf_list, rowv, rowf, CgaussCur)

    gaussCur = np.array(CgaussCur)
    return gaussCur


def meanCurvatures(V, F):
    '''
    计算模型的平均曲率
    :param V: 模型的点, 大小为 n*3
    :param F: 模型的面片, 大小为 m*3
    :return:  模型的平均曲率，一维数组，大小为n，即点的个数
    '''
    n = V.shape[0]
    L = cotangentLaplacian_noNormalize(V, F)
    LaplacianCooordinates = L.dot(V)
    vertexNormal = normal.vertexNormals(V, F)
    mixedArea = VertexCellArea(V, F)

    meanCur = np.zeros((n,), dtype=float)
    for i in range(n):
        lengthOfLC = np.linalg.norm(LaplacianCooordinates[i])
        meanCur[i] = 0.25 / mixedArea[i] * lengthOfLC * np.sign(np.dot(LaplacianCooordinates[i], vertexNormal[i]))
    return meanCur
