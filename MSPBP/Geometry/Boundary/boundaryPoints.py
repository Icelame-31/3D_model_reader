# -*- coding: utf-8 -*-

# @Time    : 2019/5/13 8:40
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================
import numpy as np
from scipy.sparse import coo_matrix, find
import ctypes

from MSPBP.Utils.ConverUtil import Convert1DToCArray, Convert2DToCArray


def boundaryPoints(F):
    '''
    找出三角形面片网格的边界点
    :param F: 模型的面片, 大小为 m*3
    :return: 边界点的下标，一维数组
    '''
    row, col = F.shape
    max = np.amax(F) + 1

    Ir = np.zeros((6 * row,), dtype=int)
    CIr = Convert1DToCArray(ctypes.c_int * len(Ir), Ir)
    Jr = np.zeros((6 * row,), dtype=int)
    CJr = Convert1DToCArray(ctypes.c_int * len(Jr), Jr)

    dll = ctypes.CDLL("AdjacencyMatrix.dll")
    dll.mainFun(Convert2DToCArray(F, ctypes.c_int), row, CIr, CJr)

    Ir = np.array(CIr)
    Jr = np.array(CJr)
    n = len(Ir)
    data = np.ones((n,), dtype=int)
    w = coo_matrix((data, (Ir, Jr)), shape=(max, max)).tocsc()
    i, j, v = find(w == 1)
    index = np.append(i, j)
    index = np.unique(index)
    return index
