# -*- coding: utf-8 -*-

# @Time    : 2019/3/1 21:07
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#        
# ======================================================

import numpy as np
from scipy.sparse import coo_matrix


def connectivityInformations(F):
    k = 0
    n = len(F)
    Ir = [0 for i in range(n * 3)]
    Jr = [0 for i in range(n * 3)]
    Vr = [0 for i in range(n * 3)]
    for i in range(n):
        face = F[i]
        v1 = face[0]
        v2 = face[1]
        v3 = face[2]

        Ir[k] = v1
        Jr[k] = v2
        Vr[k] = i
        k += 1

        Ir[k] = v2
        Jr[k] = v3
        Vr[k] = i
        k += 1

        Ir[k] = v3
        Jr[k] = v1
        Vr[k] = i
        k += 1
    return (Ir, Jr, Vr)


def edge(F):
    '''
    获取三角面片的边信息
    :param F: 模型面片，大小为 m*3
    :return: 边的信息矩阵，二维矩阵，大小为 边的个数 * 4,
     E[i,0],E[i,1]是第i条边的两个顶点
     E[i,2],E[i,3]是第i条边相邻的两个面片
    '''
    (Ir, Jr, Vr) = connectivityInformations(F)
    n = max(max(Ir), max(Jr)) + 1
    faceInformation = coo_matrix((Vr, (Ir, Jr)), shape=(n, n))
    row = faceInformation.row
    col = faceInformation.col
    index = [i for i in range(len(row)) if row[i] < col[i]]
    E = np.zeros((len(index), 4))
    faceInformation = faceInformation.toarray()
    k = 0
    for i in index:
        v1 = row[i]
        v2 = col[i]
        f1 = faceInformation[v1, v2]
        f2 = faceInformation[v2, v1]
        E[k, 0] = v1
        E[k, 1] = v2
        E[k, 2] = f1
        E[k, 3] = f2
        k += 1
    return E


def halfEdge(F):
    '''
    计算三角面片的半边信息。
    半边是指：同一条边由于起始点和终止点不同可以划分为两条半边，半边正好是边的两倍。
    :param F: 模型面片，大小为 m*3
    :return: 边的信息矩阵，二维矩阵，大小为 半边的个数 * 4,
     E[i,0],E[i,1]是第i条边的起始点和终止点
     E[i,2],E[i,3]是第i条边相邻的两个面片
    '''
    E = edge(F)
    E2 = np.zeros(E.shape)
    E2[:, 0] = E[:, 1]
    E2[:, 1] = E[:, 0]
    E2[:, 2] = E[:, 3]
    E2[:, 3] = E[:, 2]
    HE = np.vstack((E, E2))
    return HE
