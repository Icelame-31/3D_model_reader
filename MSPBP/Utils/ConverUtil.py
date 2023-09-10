# -*- coding: utf-8 -*-

# @Time    : 2019/3/30 10:26
# @Author  : hp
# @email   : hpcalifornia@163.com

# @Desc : ==============================================
#    python data conver c data with ctypes             
# ======================================================

def Convert1DToCArray(TYPE, ary):
    arow = TYPE(*ary.tolist())
    return arow


def Convert2DToCArray(ary, type):
    # ROW = ctypes.c_int * len(ary[0])
    ROW = type * len(ary[0])
    rows = []
    for i in range(len(ary)):
        rows.append(Convert1DToCArray(ROW, ary[i]))
    MATRIX = ROW * len(ary)
    return MATRIX(*rows)


