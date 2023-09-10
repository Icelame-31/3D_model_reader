# -*- coding: utf-8 -*-

# @Time    : 2019/4/7 10:24
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#       
# ======================================================
import numpy as np
from scipy.sparse import coo_matrix

from MSPBP.Geometry.Matrix import graphAdjacencyMatrix

def extrema(F, fun, k, percent):
    '''
    计算三角形网格曲面上顶点函数fun的极值点的序号maximaIndex和minimaIndex,
    其中，如果一个顶点的函数值比起k环邻域顶点上的percent函数值都大就认为是极大值，对于极小值也类似。
    :param F: 模型的面片，大小为m*3
    :param fun: 顶点函数，大小为n*1矩阵
    :param k: k环临接域，数据类型int
    :param percent: 百分比，0-1之间
    :return:
    maximaIndex -- 极大值顶点下标
    minimaIndex -- 极小值顶点下标
    '''
    fun = fun.tolist()
    W = graphAdjacencyMatrix(F)
    n = W.shape[0]
    if (k > 1):
        W1 = (W ** k).tocsr()
        W1.data.fill(1)
        data = np.ones((n,), dtype=int)
        W2 = coo_matrix((data, (np.arange(n), np.arange(n))), shape=(n, n)).tocsr()
        neighbourMatrix = W1 - W2
    elif (k == 1):
        neighbourMatrix = W
    else:
        raise RuntimeError("k must be a negative integer!")

    neighbourMatrix = coo_matrix(neighbourMatrix)
    row = neighbourMatrix.row.tolist()
    col = neighbourMatrix.col.tolist()
    valPlus = [int(fun[row[i]] > fun[col[i]]) for i in range(len(row))]
    flagMatrixPlus = coo_matrix((valPlus, (row, col)), shape=(n, n))
    valPlus = [int(fun[row[i]] < fun[col[i]]) for i in range(len(row))]
    flagMatrixMinus = coo_matrix((valPlus, (row, col)), shape=(n, n))

    num = np.sum(neighbourMatrix, axis=1)
    numPlus = np.sum(flagMatrixPlus, axis=1)
    numMinus = np.sum(flagMatrixMinus, axis=1)

    maximaIndex = np.where(numPlus >= (percent * num))[0]
    minimaIndex = np.where(numMinus >= (percent * num))[0]

    return maximaIndex, minimaIndex
