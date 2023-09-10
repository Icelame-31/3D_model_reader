from scipy.sparse import coo_matrix,identity
import numpy as np

from .AdjacencyMatrix import graphAdjacencyMatrix


def meanMatrix(F, k):
    '''
    计算k环上函数的均值矩阵
    :param F: 模型的面片，大小为m*3
    :param k: k环邻域， 数据类型 int
    :return: 均值矩阵，大小为n*n, n是顶点的个数
    '''
    W = graphAdjacencyMatrix(F)
    n = W.shape[0]

    W = np.power(W, k)
    W1 = W + identity(n, format='csr')

    W1.data.fill(1)  # 非零元素用1代替
    data = 1 / np.sum(W1, axis=1)
    n = data.shape[0]
    M = coo_matrix((data.flat, (np.arange(n), np.arange(n))), shape=(n, n)).tocsc()

    M = np.dot(M, W1)
    return M
