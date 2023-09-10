# -*- coding: utf-8 -*-

# @Time    : 2019/5/20 9:31
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================

import numpy as np


def WKS(PHI, E, nWKS=100, wks_variance=6):
    '''
    计算WKS，参考论文 “ The Wave Kernel Signature: A Quantum Mechanical Approach To Shape Analysis
    M. Aubry, U. Schlickewei, D. Cremers”
    :param PHI: PHI是LB本征函数的（顶点数×300）矩阵
    :param E: E是LB特征值的向量（默认大小为300 x 1）
    :param nWKS: nWKS是Wave Kernel Singature的数量（默认为100）
    :param wks_variance: wks方差
    :return: WKS是（顶点数）×100 WKS 矩阵
    '''
    num_vertices = PHI.shape[0]
    nWKS = min(PHI.shape[1], nWKS)
    wks = np.zeros(shape=(num_vertices,nWKS))

    log_E = np.log(np.array([max(i,1e-6) for i in np.abs(E)]))
    e = np.linspace(log_E[1],(max(log_E))/1.02,nWKS)
    sigma = (e[1]-e[0])*wks_variance

    C = np.zeros(shape=(1,nWKS))

    for i in range(nWKS):
        t = np.exp((-(e[i]-log_E)**2)/(2*sigma**2))
        wks[:,i] = np.sum(PHI**2*np.tile(t,(num_vertices,1)),axis=1)
        C[0][i] = np.sum(t)

    wks[:,:] = wks[:,:]/np.tile(C,(num_vertices,1))
    return wks

