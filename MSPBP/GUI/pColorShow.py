# -*- coding: utf-8 -*-
import numpy as np
import vtk
from .scalarFunctions import X_Axis, Y_Axis, Z_Axis
from .colorMap import colorMap, colorMapIndex
Offset = np.array([1.0, 0.0, 0.0])  # 偏移的坐标，对称功能中要展示两个模型，一个actor需要右移动一个单位
def pShowVertexFunctionX(v_list, f_list, colorMapName="Jet"):
    '''
    X轴作为标量进行函数映射
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    Summer，Autum，Winter，Gray，Bone，Copper，Pink，Lines)任意一种。
    :return: 无
    '''
    pShowVertexFunction(v_list, f_list, X_Axis(v_list), colorMapName)
def pShowVertexFunctionY(v_list, f_list, colorMapName="Jet"):
    '''
    Y轴作为标量进行函数映射
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    Summer，Autum，Winter，Gray，Bone，Copper，Pink，Lines)任意一种。
    :return: 无
    '''
    pShowVertexFunction(v_list, f_list, Y_Axis(v_list), colorMapName)
def pShowVertexFunctionZ(v_list, f_list, colorMapName="Jet"):
    '''
    Z轴作为标量进行函数映射
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    Summer，Autum，Winter，Gray，Bone，Copper，Pink，Lines)任意一种。
    :return: 无
    '''
    pShowVertexFunction(v_list, f_list, Z_Axis(v_list), colorMapName)
def pShowVertexFunction(v_list, f_list, fun, colorMapName="Jet"):
    '''
    点的函数颜色映射。给每个点一个标量值，进行颜色映射
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param fun: 每个点的标量值， 大小为 n*1, n为点的个数
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    Summer，Autum，Winter，Gray，Bone，Copper，Pink，Lines)任意一种。
    :return: 无
    '''
    #添加点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    #添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    #添加颜色映射的标量
    scalars = vtk.vtkFloatArray()
    fun = np.array(fun).reshape((len(v_list), 1))
    for i in range(len(v_list)):
        scalars.InsertTuple1(i, fun[i, 0])
    #创建PolyData
    cube = getPolyData(points, polys)
    cube.GetPointData().SetScalars(scalars)
    # 设置 vtkLookupTable.
    # 如果你不设置，它将会使用默认值
    scalarRange = [fun.min(), fun.max()]
    pColorTable = getLookupTable(scalarRange, colorMapName)
    # 设置 mapper 和 actor
    mapper, actor = getMapperAndActor(cube, pColorTable, scalarRange)
    #创建 vtkScaleBarActor
    scalarBar = getScaleBarActor(pColorTable)
    # 实例化
    visualize(actor, scalarBar)
def pShowVertexFunction_2model(v_list1, f_list1, v_list2, f_list2, fun1, fun2, colorMap='Jet'):
    '''
    用来同时展示两个模型，使用同一套颜色映射
    '''
    #添加第一个模型
    points1 = vtk.vtkPoints()
    for v in v_list1:
        points1.InsertNextPoint(v)
    #添加面片
    polys1 = vtk.vtkCellArray()
    for f in f_list1:
        polys1.InsertNextCell(len(f), f)
    #添加第二个模型
    points2 = vtk.vtkPoints()
    for v in v_list2:
        points2.InsertNextPoint(v)
    #添加面片
    polys2 = vtk.vtkCellArray()
    for f in f_list2:
        polys2.InsertNextCell(len(f), f)
    #添加颜色映射的标量
    scalars1 = vtk.vtkFloatArray()
    fun1 = np.array(fun1).reshape((len(v_list1), 1))
    for i in range(len(v_list1)):
        scalars1.InsertTuple1(i, fun1[i, 0])
    scalars2 = vtk.vtkFloatArray()
    fun2 = np.array(fun2).reshape((len(v_list2), 1))
    for i in range(len(v_list2)):
        scalars2.InsertTuple1(i, fun2[i, 0])
    #创建PolyData
    cube1 = getPolyData(points1, polys1)
    cube1.GetPointData().SetScalars(scalars1)
    cube2 = getPolyData(points2, polys2)
    cube2.GetPointData().SetScalars(scalars2)
    # 设置 vtkLookupTable.
    # 如果你不设置，它将会使用默认值
    scalarRange = [min(fun1.min(),fun2.min()), max(fun1.max(),fun2.max())]
    pColorTable = getLookupTable(scalarRange, colorMap)
    # 设置 mapper 和 actor
    mapper1, actor1 = getMapperAndActor(cube1, pColorTable, scalarRange)
    mapper2, actor2 = getMapperAndActor(cube2, pColorTable, scalarRange)
    actor2.SetPosition(Offset) #将第二个模型右移
    #创建 vtkScaleBarActor
    scalarBar = getScaleBarActor(pColorTable)
    # 实例化
    render = vtk.vtkRenderer()
    render.SetBackground(1, 1, 1)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # 点击模型上的一点获取其坐标
    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(render)
    renderWindowInteractor.SetInteractorStyle(style)
    render.AddActor(actor1)
    render.AddActor(actor2)
    render.AddActor2D(scalarBar)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowFacetFunction(v_list, f_list, fun, colorMapName="Jet"):
    '''
    面片的函数颜色映射。给每个面片一个标量值，进行颜色映射
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param fun: 每个面片的标量值， 大小为 m*1, m为面片的个数
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    Summer，Autum，Winter，Gray，Bone，Copper，Pink，Lines)任意一种。
    :return: 无
    '''
    #添加点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 添加颜色映射的标量
    scalars = vtk.vtkFloatArray()
    fun = np.array(fun).reshape((len(f_list), 1))
    for i in range(len(f_list)):
        scalars.InsertTuple1(i, fun[i, 0])
    # 创建PolyData
    cube = getPolyData(points, polys)
    cube.GetCellData().SetScalars(scalars)
    # 设置vtkLookupTable.
    scalarRange = [fun.min(), fun.max()]
    pColorTable = getLookupTable(scalarRange, colorMapName)
    mapper, actor = getMapperAndActor(cube, pColorTable, scalarRange)
    #创建 vtkScaleBarActor
    scalarBar = getScaleBarActor(pColorTable)
    #实例化
    visualize(actor, scalarBar)
def getPolyData(points, polys):
    #创建 PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    return cube
def getLookupTable(scalarRange, colorMapName):
    steps = 3
    step1 = (scalarRange[1] - scalarRange[0]) / steps
    index = colorMapIndex.get(colorMapName)
    if (abs(scalarRange[1] - scalarRange[0]) > 1e-10):
        pColorTable = vtk.vtkColorTransferFunction()
        pColorTable.AddRGBPoint(scalarRange[0],             colorMap[index][0][0], colorMap[index][0][1],colorMap[index][0][2])
        pColorTable.AddRGBPoint(scalarRange[0] + step1,     colorMap[index][1][0], colorMap[index][1][1],colorMap[index][1][2])
        pColorTable.AddRGBPoint(scalarRange[0] + 2 * step1, colorMap[index][2][0], colorMap[index][2][1],colorMap[index][2][2])
        pColorTable.AddRGBPoint(scalarRange[0] + 3 * step1, colorMap[index][3][0], colorMap[index][3][1],colorMap[index][3][2])
        return pColorTable
def getLookupTableByUser(scalarRange, colorMap):
    steps = 3
    step1 = (scalarRange[1] - scalarRange[0]) / steps
    if (abs(scalarRange[1] - scalarRange[0]) > 1e-10) and len(colorMap)>11:
        pColorTable = vtk.vtkColorTransferFunction()
        pColorTable.AddRGBPoint(scalarRange[0],             colorMap[0],colorMap[1],colorMap[2])
        pColorTable.AddRGBPoint(scalarRange[0] + step1,     colorMap[3],colorMap[4],colorMap[5])
        pColorTable.AddRGBPoint(scalarRange[0] + 2 * step1, colorMap[6],colorMap[7],colorMap[8])
        pColorTable.AddRGBPoint(scalarRange[0] + 3 * step1, colorMap[9],colorMap[10],colorMap[11])
        return pColorTable
def getMapperAndActor(cube, pColorTable, scalarRange):
    # 创建 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    mapper.SetScalarRange(scalarRange[0], scalarRange[1])
    mapper.SetLookupTable(pColorTable)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return mapper, actor
def getScaleBarActor(pColorTable):
    # 创建 vtkScaleBarActor
    scalarBar = vtk.vtkScalarBarActor()
    tp = scalarBar.GetTitleTextProperty()
    tp.SetColor(0.0, 0.0, 0.0)
    scalarBar.SetTitleTextProperty(tp)
    scalarBar.SetLabelTextProperty(tp)
    scalarBar.SetNumberOfLabels(4)
    scalarBar.SetPosition(0.8, 0.2)
    scalarBar.SetWidth(0.05)
    scalarBar.SetHeight(0.4)
    scalarBar.SetLabelFormat("%-#4.4f")
    scalarBar.SetLookupTable(pColorTable)
    scalarBar.SetOrientationToVertical()
    return scalarBar
def visualize(actor, scalarBar):
    # 实例化
    render = vtk.vtkRenderer()
    render.SetBackground(1, 1, 1)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # 点击模型上的一点获取其坐标
    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(render)
    renderWindowInteractor.SetInteractorStyle(style)
    render.AddActor(actor)
    render.AddActor2D(scalarBar)
    renderWindow.Render()
    renderWindowInteractor.Start()
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkCellPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        if (picker.GetCellId() < 0):
            print("您点击到了模型外面")
        else:
            selpt = picker.GetSelectionPoint()
            x = selpt[0]
            y = selpt[1]
            pickPos = picker.GetPickPosition()
            pointId = picker.GetPointId()
            # pos = "该点的index为： %d ,坐标为： %5.5f,  %5.5f,  %5.5f" % (pointId, pickPos[0], pickPos[1], pickPos[2])
            pos = "您点击的是第%d个点" % (pointId)
            print(pos)
        self.OnLeftButtonDown()