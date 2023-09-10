from scipy.sparse import coo_matrix
import ctypes
import numpy as np

from .AdjacencyMatrix import graphAdjacencyMatrix
from MSPBP.Utils.ConverUtil import Convert1DToCArray, Convert2DToCArray
from MSPBP.Geometry.Area import VertexCellArea


def graphLaplacian(F):
    '''
    计算三角形网格曲面的图的拉普拉斯矩阵
    :param F: 模型的片面，大小为 m*3
    :return: 图的拉普拉斯矩阵，大小为 n*n
    '''
    W = graphAdjacencyMatrix(F)
    data = np.sum(W, axis=1)
    n = data.shape[0]
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n))
    L = D - W
    return L


def tutteGraphLaplacian(F):
    '''
    计算三角形网格曲面的tutte图的拉普拉斯矩阵
    :param F: 模型的片面，大小为 m*3
    :return: tutte图的拉普拉斯矩阵，大小为 n*n
    '''
    W = graphAdjacencyMatrix(F)
    data = np.sum(W, axis=1)
    n = data.shape[0]
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n))
    K = D - W
    data = 1 / np.sum(W, axis=1)
    n = data.shape[0]
    R = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n))
    L = np.dot(R, K)
    return L


def normalizedGraphLaplacian(F):
    '''
    计算三角形网格曲面的图的规则化的拉普拉斯矩阵
    :param F: 模型的片面，大小为 m*3
    :return: 规则化的拉普拉斯矩阵，大小为n*n
    '''
    W = graphAdjacencyMatrix(F)
    data = np.sum(W, axis=1)
    n = data.shape[0]
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    K = D - W
    data = 1 / np.sqrt(data)
    D2 = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    L = np.dot(np.dot(D2, K), D2)
    return L


def cotangentLaplacian_noNormalize(V, F):
    '''
    计算三角形网格曲面的余切权的拉普拉斯矩阵
    :param V: 模型的点，大小为n*3
    :param F: 模型的面片，大小为m*3
    :return: 余切权的拉普拉斯矩阵，大小为n*n
    '''
    rowf, colf = F.shape
    rowV, colV = V.shape
    Ir = np.zeros((3 * rowf,), dtype=int)
    CIr = Convert1DToCArray(ctypes.c_int * len(Ir), Ir)
    Jr = np.zeros((3 * rowf,), dtype=int)
    CJr = Convert1DToCArray(ctypes.c_int * len(Jr), Jr)
    Vr = np.zeros((3 * rowf,), dtype=float)
    CVr = Convert1DToCArray(ctypes.c_float * len(Vr), Vr)

    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    dll = ctypes.CDLL("cotangentLaplacianMatrix.dll")
    dll.mainFun(Cv_list, Cf_list, rowf, CIr, CJr, CVr)

    Ir = np.array(CIr)
    Jr = np.array(CJr)
    Vr = np.array(CVr)
    Q = coo_matrix((Vr, (Ir, Jr)), shape=(rowV, rowV)).tocsc()
    W = 0.5 * (Q + Q.T)
    data = np.sum(W, axis=1)
    n = data.shape[0]
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    L = D - W
    return L


def cotangentLaplacian_normalize(V, F):
    '''
    计算三角形网格曲面的规则化的余切权的拉普拉斯矩阵
    :param V: 模型的点，大小为n*3
    :param F: 模型的面片，大小为m*3
    :return: 余切权的拉普拉斯矩阵，大小为n*n
    '''
    rowf, colf = F.shape
    rowV, colV = V.shape
    Ir = np.zeros((3 * rowf,), dtype=int)
    CIr = Convert1DToCArray(ctypes.c_int * len(Ir), Ir)
    Jr = np.zeros((3 * rowf,), dtype=int)
    CJr = Convert1DToCArray(ctypes.c_int * len(Jr), Jr)
    Vr = np.zeros((3 * rowf,), dtype=float)
    CVr = Convert1DToCArray(ctypes.c_float * len(Vr), Vr)

    Cv_list = Convert2DToCArray(V, ctypes.c_float)
    Cf_list = Convert2DToCArray(F, ctypes.c_int)

    dll = ctypes.CDLL("cotangentLaplacianMatrix.dll")
    dll.mainFun(Cv_list, Cf_list, rowf, CIr, CJr, CVr)

    Ir = np.array(CIr)
    Jr = np.array(CJr)
    Vr = np.array(CVr)
    Q = coo_matrix((Vr, (Ir, Jr)), shape=(rowV, rowV)).tocsc()
    W = 0.5 * (Q + Q.T)
    data = np.sum(W, axis=1)
    n = data.shape[0]
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    K = D - W
    data = 1.0 / data
    D = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    L = D.dot(K)
    return L


def LaplaceBeltrami(V, F):
    '''
    计算三角形网格曲面的Laplace Beltrami算子。
    :param V: 模型的点，大小为n*3
    :param F: 模型的面片，大小为m*3
    :return: Laplace Beltrami算子，大小为n*n
    '''
    K = cotangentLaplacian_noNormalize(V, F)
    area = 1 / VertexCellArea(V, F)
    n = len(area)
    D = coo_matrix((area.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()
    L = np.dot(D, K)
    return L
