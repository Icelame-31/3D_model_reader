import numpy as np
from scipy.sparse import coo_matrix
import ctypes

from MSPBP.Utils.ConverUtil import Convert1DToCArray,Convert2DToCArray


def graphAdjacencyMatrix(f_list):
    '''
    计算三角形网格曲面的邻接矩阵
    :param f_list: 模型的面，大小为 m*3
    :return: 邻接矩阵，大小为 n*n, n是顶点的个数
    '''
    row,col = f_list.shape
    max = np.amax(f_list) + 1

    Ir = np.zeros((6 * row,), dtype=int)
    CIr = Convert1DToCArray(ctypes.c_int * len(Ir), Ir)
    Jr = np.zeros((6 * row,), dtype=int)
    CJr = Convert1DToCArray(ctypes.c_int * len(Jr), Jr)

    dll = ctypes.CDLL("AdjacencyMatrix.dll")
    dll.mainFun(Convert2DToCArray(f_list,ctypes.c_int), row, CIr, CJr)

    Ir = np.array(CIr)
    Jr = np.array(CJr)
    n = len(Ir)
    data = np.ones((n,),dtype=int)
    w = coo_matrix((data,(Ir,Jr)),shape=(max,max)).tocsr()
    w.data.fill(1)
    return w
