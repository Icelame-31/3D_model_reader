# -*- coding: utf-8 -*-

# @Time    : 2019/5/12 17:32
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#                     
# ======================================================
from .gaussNoise import gaussNoise
from MSPBP.Geometry.Distance import meanEdgeLength


def addNoise(V, F, percent):
    '''
    将高斯噪声添加到三角形网格中，噪声的平均值为0，并且噪声的方差与平均边长度成比例
    :param V: 模型的点，大小为 n*3
    :param F: 模型的面片，大小为m*3
    :param percent: 噪声的方差与平均边长度成比例，大小为0-1之间
    :return: 添加噪声后的矩阵，大小为n*3
    '''
    m, n = V.shape
    meanLength = meanEdgeLength(V, F)
    VV = V + gaussNoise(m, n, 0.0, percent * meanLength)
    return VV
