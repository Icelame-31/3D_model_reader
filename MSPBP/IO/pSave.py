# -*- coding: utf-8 -*-
import tkinter as tk
import vtk
from tkinter import filedialog
def pSaveOFF(v_list, f_list, filename=None):
    '''
    模型保存为off文件
    :param v_list: 模型的点，大小为n*3
    :param f_list: 模型的面，大小为m*3
    :param filename:文件保存路径，数据类型 string, example filename="SavePath/model.off"
    :return: none
    '''
    if (filename == None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(filetypes=[('OFF', 'off')])
        filename = '%s%s' % (filename, '.off')
    else:
        filename = filename
    if ~v_list.any() or ~f_list.any():
        raise RuntimeError("facets or vertex is null")
    with open(filename, 'w') as file:
        file.write("OFF")
        file.write("\n")
        file.write(str(len(v_list)) + " " + str(len(f_list)) + " " + str(0))
        file.write("\n")
        for vertices in v_list:
            tmp = " ".join(str(i) for i in vertices)
            file.write(tmp + "\n")
        for faces in f_list:
            tmp = " ".join(str(i) for i in faces)
            file.write(str(len(faces)) + " " + tmp + "\n")
def pSaveSTL(v_list, f_list, filename=None):
    '''
    模型保存为stl文件
    :param v_list: 模型的点，大小为n*3
    :param f_list: 模型的面，大小为m*3
    :param filename:文件保存路径，数据类型 string,example filename="SavePath/model.stl"
    :return: none
    '''
    if (filename == None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(filetypes=[('STL', 'stl')])
        filename = '%s%s' % (filename, '.stl')
    else:
        filename = filename
    writer = vtk.vtkSTLWriter()
    vtkWriter(v_list, f_list, filename, writer)
def pSaveOBJ(v_list, f_list, filename=None):
    '''
    模型保存为obj文件
    :param v_list: 模型的点，大小为n*3
    :param f_list: 模型的面，大小为m*3
    :param filename:文件保存路径，数据类型 string,example filename="SavePath/model",这个比较特殊，不要加obj后缀，系统自带后缀
    :return: none
    '''
    if (filename == None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(filetypes=[('OBJ', 'obj')])
        filename = '%s' % (filename)
    else:
        filename = filename
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    render = vtk.vtkRenderer()
    render.AddActor(actor)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(render)
    expoter = vtk.vtkOBJExporter()
    expoter.SetFilePrefix(filename)
    expoter.SetInput(renderWindow)
    expoter.Write()
def pSavePLY(v_list, f_list, filename=None):
    '''
    模型保存为ply文件
    :param v_list: 模型的点，大小为n*3
    :param f_list: 模型的面，大小为m*3
    :param filename:文件保存路径，数据类型 string，example filename="SavePath/model.ply"
    :return: none
    '''
    if (filename == None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(filetypes=[('PLY', 'ply')])
        filename = '%s%s' % (filename, '.ply')
    else:
        filename = filename
    writer = vtk.vtkPLYWriter()
    vtkWriter(v_list, f_list, filename, writer)
def vtkWriter(v_list, f_list, filepath, writer):
    if ~v_list.any() or ~f_list.any():
        raise RuntimeError("facets or vertex is null")
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    writer.SetFileName(filepath)
    writer.SetInputData(cube)
    writer.Write()
