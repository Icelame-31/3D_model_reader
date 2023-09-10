def neighbourFacesOfVertex(F, numberOfVertex):
    '''
    计算每个点的邻接面片
    :param F: 模型的面片，大小为m*3
    :param numberOfVertex: 顶点的个数，数据类型 int
    :return: 返回一个列表，列表中第i个元素代表第i个顶点的邻接面片。
    '''
    NFOV = [[] for i in range(numberOfVertex)]
    for i in range(F.shape[0]):
        vertices = F[i]
        for vertex in vertices:
            NFOV[vertex].append(i)
    return NFOV


def neighbourFacesOfFace(F, numberOfVertex):
    '''
    计算每个面片的邻接面片
    :param F: 模型的面片，大小为m*3
    :param numberOfVertex: 顶点的个数，数据类型 int
    :return: 返回一个列表，列表中第i个元素代表第i个面片的邻接面片。
    '''
    NFOV = neighbourFacesOfVertex(F, numberOfVertex)
    NFOF = [[] for i in range(F.shape[0])]
    for i in range(F.shape[0]):
        vertices = F[i]
        for vertex in vertices:
            NFOF[i] = list(set(NFOF[i]) | set(NFOV[vertex]))
    return NFOF
