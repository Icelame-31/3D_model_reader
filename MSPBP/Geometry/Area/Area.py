# -*- coding: utf-8 -*-

# @Time    : 2019/3/30 10:24
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import ctypes
import numpy as np

from MSPBP.Utils.ConverUtil import Convert1DToCArray, Convert2DToCArray

def FacetArea(V, F):
    '''
    计算每个面片的面积
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为 m*3
    :return: 面片的面积，大小为 m*1， m是面片的个数
    '''
    rowf, colf = F.shape
    areaOfFacets = np.zeros((rowf,), dtype=float)

    CareaOfFacets = Convert1DToCArray(ctypes.c_float * len(areaOfFacets), areaOfFacets)
    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    AreaDLL = ctypes.CDLL("Area.dll")
    AreaDLL.FacetArea(Cv_list, Cf_list, rowf, CareaOfFacets)

    areaOfFacets = np.array(CareaOfFacets)
    return areaOfFacets


def VertexCellArea(V, F):
    '''
    计算每个点的Voronoi面积
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为 m*3
    :return: 每个点的Voronoi面积，大小为 n*1，n是点的个数
    '''
    rowf, colf = F.shape
    rowV, colV = V.shape
    cellAreaOfVertex = np.zeros((rowV,), dtype=float)

    CcellAreaOfVertex = Convert1DToCArray(ctypes.c_float * len(cellAreaOfVertex), cellAreaOfVertex)
    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    AreaDLL = ctypes.CDLL("Area.dll")
    AreaDLL.VertexCellArea(Cv_list, Cf_list, rowf, CcellAreaOfVertex)

    cellAreaOfVertex = np.array(CcellAreaOfVertex)
    return cellAreaOfVertex


def MixedArea(V, F):
    '''
    计算每个顶点的混合面积
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为 m*3
    :return: 每个顶点的混合面积，大小为 n*1，n是点的个数
    '''
    rowf, colf = F.shape
    rowV, colV = V.shape
    cellAreaOfVertex = np.zeros((rowV,), dtype=float)

    CcellAreaOfVertex = Convert1DToCArray(ctypes.c_float * len(cellAreaOfVertex), cellAreaOfVertex)
    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    AreaDLL = ctypes.CDLL("Area.dll")
    AreaDLL.MixedArea(Cv_list, Cf_list, rowf, CcellAreaOfVertex)

    cellAreaOfVertex = np.array(CcellAreaOfVertex)
    return cellAreaOfVertex