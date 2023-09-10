# -*- coding: utf-8 -*-
from tkinter import filedialog
import tkinter as tk
import numpy as np
import vtk
def pReadOFF(filename=""):
    '''
    读取一个off文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('OFF', 'off')])
    else:
        file_path = filename
    v_list = []
    f_list = []
    with open(file_path, "r") as file:
        file.readline()
        line = file.readline()
        datas = line.split()
        v = int(datas[0])
        f = int(datas[1])
        for i in range(v):
            datas = file.readline().split()
            datas = [float(i) for i in datas[:]]
            v_list.append(datas)
        for i in range(f):
            datas = file.readline().split()
            datas = [int(i) for i in datas[1:]]
            f_list.append(datas)
    v_list = np.array(v_list)
    f_list = np.array(f_list)
    return v_list, f_list
def pReadOBJ(filename=""):
    '''
    读取一个obj文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if(filename==""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('OBJ', 'obj')])
    else:
        file_path = filename
    reader = vtk.vtkOBJReader()
    v_list, f_list = vtkReader(file_path, reader)
    return v_list, f_list
def pReadPLY(filename=""):
    '''
    读取一个ply文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('PLY', 'ply')])
    else:
        file_path = filename

    reader = vtk.vtkPLYReader()
    v_list, f_list = vtkReader(file_path, reader)
    return v_list, f_list
def pReadSTL(filename=""):
    '''
    读取一个stl文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('STL', 'stl')])
    else:
        file_path = filename
    reader = vtk.vtkSTLReader()
    v_list, f_list = vtkReader(file_path, reader)
    return v_list, f_list
def pRead3DStudio(filename=""):
    '''
    读取一个3DStudio文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('3DS', '3ds')])
    else:
        file_path = filename
    reader = vtk.vtk3DSImporter()
    v_list, f_list = vtkReader(file_path, reader)
    return v_list, f_list
def pReadPLOT3D(filename=""):
    '''
    读取一个PLOT3D文件
    :return:
    v_list -- 模型的点，大小为n*3
    f_list -- 模型的面，大小为m*3
    '''
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('PLOT3D', 'plot3d')])
    else:
        file_path = filename
    reader = vtk.vtkPLOT3DReader()
    v_list, f_list = vtkReader(file_path, reader)
    return v_list, f_list
def vtkReader(filepath, reader):
    reader.SetFileName(filepath)
    reader.Update()
    polydata = reader.GetOutput()
    v_list = []
    f_list = []
    for i in range(polydata.GetNumberOfPoints()):
        p = [0, 0, 0]
        polydata.GetPoint(i, p)
        v_list.append(p)
    ids = vtk.vtkIdList()
    for i in range(polydata.GetNumberOfCells()):
        polydata.GetCellPoints(i, ids)
        f_list.append([ids.GetId(0), ids.GetId(1), ids.GetId(2)])
    v_list = np.array(v_list)
    f_list = np.array(f_list)
    return v_list, f_list
def pReadOFFVertex(filename="",keypoint=[]):
    if (filename == ""):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('OFF', 'off')])
    else:
        file_path = filename
    v_list = []
    with open(file_path, "r") as file:
        file.readline()
        line = file.readline()
        datas = line.split()
        v = int(datas[0])
        for i in range(v):
            datas = file.readline().split()
            datas = [float(i) for i in datas[:]]
            v_list.append(datas)
    v_list = np.array(v_list)
    Vertex=[]
    for i in range(len(keypoint)):
        t=v_list[keypoint[i]]
        Vertex.append(t)
    Vertex=np.array(Vertex)
    return Vertex