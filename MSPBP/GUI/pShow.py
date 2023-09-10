import vtk
import numpy as np

from .colorMap import colorMap, colorMapIndex

Offset = np.array([1.0, 0.0, 0.0])  # 偏移的坐标，对称功能中要展示两个模型，一个actor需要右移动一个单位
def pShow(v_list, f_list, color=None):
    '''
    展示一个模型
    :param v_list: 模型的点， 大小为n*3
    :param f_list: 模型的面,  大小为m*3
    :param color: 展示模型的颜色，例如: "red" "blue"...
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    # 添加点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 创建PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    # 创建 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if color is None:
        actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    else:
        actor.GetProperty().SetColor(colors.GetColor3d(color))
    # 实例化
    render = vtk.vtkRenderer()
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
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowVertex(v_list, f_list, vertexIds, color="red", radius=0.01):
    '''
    在模型上展示顶点
    :param v_list: 模型上的点, 大小为 n*3
    :param f_list: 模型上的面, 大小为 m*3
    :param vertexIds: 要显示点的下标， 例如 [1,3,5,7]
    :param color: 显示点的颜色，默认“red”
    :param radius: 显示点的大小，默认0.01
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    v_list = Normalized(v_list)
    # 添加点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 创建 PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    # 创建 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    # 实例化
    render = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    render.AddActor(actor)
    for posid in vertexIds:
        pos = points.GetPoint(posid)
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(pos)
        sphereSource.SetRadius(radius)
        # 创建 mapper 和 actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphereSource.GetOutputPort())
        actor_tmp = vtk.vtkActor()
        actor_tmp.SetMapper(mapper)
        actor_tmp.GetProperty().SetColor(colors.GetColor3d(color))
        render.AddActor(actor_tmp)
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowPlane(v_list, f_list, center, normal, color="red"):
    '''
    在模型上展示截面
    :param v_list: 模型上的点, 大小为n*3
    :param f_list: 模型上的面, 大小为m*3
    :param center: 要展示截面的中心坐标,一定要是2维数组， 例如 [[0,0,0]] 或   [[0,0,0],                                                              [0,1,0]]
    :param normal:  要展示截面的法向量，大小与center相同
    :param color:  截面的颜色，默认红色。
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    v_min, v_max = v_list.min(), v_list.max()
    v_list = Normalized(v_list)
    # 添加顶点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 创建 PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    # 创建 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    # 实例化
    render = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    render.AddActor(actor)
    center = np.array(center)
    normal = np.array(normal)
    assert center.shape[0] == normal.shape[0], "center个数应与normal个数保持一致。"
    assert center.shape[1] == 3 & normal.shape[1] == 3, "center和normal应是n*3矩阵"
    center = (center - v_min) / (v_max - v_min)  # 由于点的坐标都正则化了，所以平面上的点先对应到正则化后的坐标上
    for i in range(center.shape[0]):
        planeSource = vtk.vtkPlaneSource()
        planeSource.SetCenter(center[i][0], center[i][1], center[i][2])
        planeSource.SetNormal(normal[i][0], normal[i][1], normal[i][2])
        # 创建 mapper 和 actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(planeSource.GetOutputPort())
        actor_tmp = vtk.vtkActor()
        actor_tmp.SetMapper(mapper)
        actor_tmp.GetProperty().SetColor(colors.GetColor3d(color))
        render.AddActor(actor_tmp)
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowLine(v_list, f_list, vertexStart, vertexEnd, lineColor="red", lineWidth=3, opacity=1):
    '''
    显示模型上的连线
    :param v_list: 模型上的点, 大小为 n*3
    :param f_list: 模型上的面, 大小为 m*3
    :param vertexStart: 连线的起始点， 一维数组
    :param vertexEnd: 连线的终止点， 一维数组
    :param lineColor: 连线的颜色，默认红色
    :param lineWidth: 连线的宽度，大小为 3
    :param opacity: 模型的透明度，大小在0-1之间。
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    v_list = Normalized(v_list)
    # 添加顶点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 创建PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    # 设置 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    actor.GetProperty().SetOpacity(opacity)
    # 实例化
    render = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    render.AddActor(actor)
    if (len(vertexStart) != len(vertexEnd)):
        raise RuntimeError("连线的起始顶点和终止定点数量不一致")
    else:
        for i in range(len(vertexStart)):
            pointStart = points.GetPoint(vertexStart[i])
            pointEnd = points.GetPoint(vertexEnd[i])
            lineSource = vtk.vtkLineSource()
            lineSource.SetPoint1(pointStart)
            lineSource.SetPoint2(pointEnd)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            line_actor = vtk.vtkActor()
            line_actor.SetMapper(mapper)
            line_actor.GetProperty().SetColor(colors.GetColor3d(lineColor))
            line_actor.GetProperty().SetLineWidth(lineWidth)
            render.AddActor(line_actor)
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowAll(v_list, f_list, vertexIds=None, vertexStart=None, vertexEnd=None, plane_center=None, plane_normal=None,
             vertexColor="blue", lineColor="red", lineWidth=3, planeColor="yellow", opacity=1, vertexfun=None,
             colorMapName="Jet"):
    '''
    在模型上展示顶点，连线，截面
    :param v_list: 模型上的点, 大小为n*3
    :param f_list: 模型上的面, 大小为m*3
    :param vertexIds: 要展示点的下标值，一维数组
    :param vertexStart: 连线的起始点下标值，一维数组
    :param vertexEnd:  连线的终止点下标值， 一维数组
    :param center: 要展示截面的中心坐标,一定要是2维数组， 例如 [[0,0,0]]或 [[0,0,0], [0,1,0]]
    :param normal:  要展示截面的法向量，大小与center相同
    :param vertexColor: 展示点的颜色，默认蓝色
    :param lineColor: 要展示直线的颜色，默认红色
    :param lineWidth: 要展示直线的宽度，默认3
    :param planeColor: 截面的颜色，默认黄色
    :param opacity: 模型的透明度，大小0-1之间
    :param vertexfun:点的颜色映射，一维数组，大小为nv
    :param colorMapName: 映射的颜色，默认为“Jet”,你可以传入(Jet,HSV,,Hot，Cool，Spring，
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    v_min, v_max = v_list.min(), v_list.max()
    v_list = Normalized(v_list)
    # 添加顶点
    points = vtk.vtkPoints()
    for v in v_list:
        points.InsertNextPoint(v)
    # 添加面片
    polys = vtk.vtkCellArray()
    for f in f_list:
        polys.InsertNextCell(len(f), f)
    # 创建PolyData
    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    # 创建 mapper 和 actor
    mapper = vtk.vtkPolyDataMapper()
    render = vtk.vtkRenderer()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(cube)
    else:
        mapper.SetInputData(cube)
    # 添加点的颜色映射
    if (vertexfun is not None):
        # 添加颜色映射的标量
        scalars = vtk.vtkFloatArray()
        fun = np.array(vertexfun).reshape((len(v_list), 1))
        for i in range(len(v_list)):
            scalars.InsertTuple1(i, fun[i, 0])
        cube.GetPointData().SetScalars(scalars)
        scalarRange = [fun.min(), fun.max()]
        pColorTable = getLookupTable(scalarRange, colorMapName)
        mapper.SetScalarRange(scalarRange[0], scalarRange[1])
        mapper.SetLookupTable(pColorTable)
        scalarBar = getScaleBarActor(pColorTable)
        render.AddActor2D(scalarBar)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    actor.GetProperty().SetOpacity(opacity)
    # 实例化
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("model")
    renderWindow.AddRenderer(render)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    render.AddActor(actor)
    # 添加标记点
    if (vertexIds is not None):
        for posid in vertexIds:
            pos = points.GetPoint(posid)
            sphereSource = vtk.vtkSphereSource()
            sphereSource.SetCenter(pos)
            sphereSource.SetRadius(0.01)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphereSource.GetOutputPort())
            actor_tmp = vtk.vtkActor()
            actor_tmp.SetMapper(mapper)
            actor_tmp.GetProperty().SetColor(colors.GetColor3d(vertexColor))
            render.AddActor(actor_tmp)
    # 添加连线
    if (vertexStart is not None and vertexEnd is not None):
        if (len(vertexStart) != len(vertexEnd)):
            raise RuntimeError("连线的起始顶点和终止定点数量不一致")
        else:
            for i in range(len(vertexStart)):
                pointStart = points.GetPoint(vertexStart[i])
                pointEnd = points.GetPoint(vertexEnd[i])
                lineSource = vtk.vtkLineSource()
                lineSource.SetPoint1(pointStart)
                lineSource.SetPoint2(pointEnd)
                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(lineSource.GetOutputPort())
                line_actor = vtk.vtkActor()
                line_actor.SetMapper(mapper)
                line_actor.GetProperty().SetColor(colors.GetColor3d(lineColor))
                line_actor.GetProperty().SetLineWidth(lineWidth)
                render.AddActor(line_actor)
    # 添加截面
    if (plane_center is not None and plane_normal is not None):
        center = np.array(plane_center)
        normal = np.array(plane_normal)
        assert center.shape[0] == normal.shape[0], "center个数应与normal个数保持一致。"
        assert center.shape[1] == 3 & normal.shape[1] == 3, "center和normal应是n*3矩阵"
        center = (center - v_min) / (v_max - v_min)  # 由于点的坐标都正则化了，所以平面上的点先对应到正则化后的坐标上
        for i in range(center.shape[0]):
            planeSource = vtk.vtkPlaneSource()
            planeSource.SetCenter(center[i][0], center[i][1], center[i][2])
            planeSource.SetNormal(normal[i][0], normal[i][1], normal[i][2])
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(planeSource.GetOutputPort())
            actor_tmp = vtk.vtkActor()
            actor_tmp.SetMapper(mapper)
            actor_tmp.GetProperty().SetColor(colors.GetColor3d(planeColor))
            render.AddActor(actor_tmp)
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
def pShowSymmetry(v_list1, f_list1, v_list2, f_list2, index1, index2, color=None, opacity=1):
    '''
    展示两个模型之间的对称点，将对称点用连线连接起来
    :param v_list1: 模型1的点, 大小为 n1*3
    :param f_list1: 模型1上的面片, 大小为 m1*3
    :param v_list2: 模型2上的点, 大小为 n2*3
    :param f_list2: 模型2上的面片, 大小为 m2*3
    :param index1:  模型1上的点，一维数组
    :param index2:  模型2上的点, 一维数组。注意index1和index2两个数组大小应一致，也就是说对应点应一样多
    :param color:   两个模型的颜色，默认银色
    :param opacity： 模型的透明度，大小为0-1之间
    :return: 无
    '''
    colors = vtk.vtkNamedColors()
    v_list1 = Normalized(v_list1)
    v_list2 = Normalized(v_list2)
    # 添加点
    points1 = vtk.vtkPoints()
    for v in v_list1:
        points1.InsertNextPoint(v)
    # 添加面片
    polys1 = vtk.vtkCellArray()
    for f in f_list1:
        polys1.InsertNextCell(len(f), f)
    # 创建PolyData
    cube1 = vtk.vtkPolyData()
    cube1.SetPoints(points1)
    cube1.SetPolys(polys1)
    points2 = vtk.vtkPoints()
    for v in v_list2:
        points2.InsertNextPoint(v)
    polys2 = vtk.vtkCellArray()
    for f in f_list2:
        polys2.InsertNextCell(len(f), f)
    # 创建 PolyData
    cube2 = vtk.vtkPolyData()
    cube2.SetPoints(points2)
    cube2.SetPolys(polys2)
    # 创建 mapper 和 actor
    mapper1 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper1.SetInput(cube1)
    else:
        mapper1.SetInputData(cube1)
    mapper2 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper2.SetInput(cube2)
    else:
        mapper2.SetInputData(cube2)
    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    if color is None:
        actor1.GetProperty().SetColor(colors.GetColor3d("Silver"))
    else:
        actor1.GetProperty().SetColor(colors.GetColor3d(color))
    actor1.GetProperty().SetOpacity(opacity)
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.SetPosition(Offset)
    if color is None:
        actor2.GetProperty().SetColor(colors.GetColor3d("Silver"))
    else:
        actor2.GetProperty().SetColor(colors.GetColor3d(color))
    actor2.GetProperty().SetOpacity(opacity)
    # 添加对称点连线
    pts = vtk.vtkPoints()
    line = vtk.vtkPolyLine()
    lines = vtk.vtkCellArray()
    cube3 = vtk.vtkPolyData()
    mapper3 = vtk.vtkPolyDataMapper()
    if len(index1) != len(index2):
        raise RuntimeError("index1和index2元素个数必须相同")
    else:
        for i in range(len(index1)):
            pts.InsertNextPoint(v_list1[index1[i]])
            pts.InsertNextPoint((v_list2[index2[i]] + Offset))
        num_points = pts.GetNumberOfPoints()
        for i in range(0, num_points, 2):
            line.GetPointIds().SetNumberOfIds(2)
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i + 1)
            lines.InsertNextCell(line)
    cube3.SetPoints(pts)
    cube3.SetLines(lines)
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper3.SetInput(cube3)
    else:
        mapper3.SetInputData(cube3)
    actor3 = vtk.vtkActor()
    actor3.SetMapper(mapper3)
    actor3.GetProperty().SetLineWidth(2)
    actor3.GetProperty().SetColor(1, 0, 0)
    # 实例化
    render = vtk.vtkRenderer()
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
    render.AddActor(actor3)
    render.SetBackground(1, 1, 1)
    renderWindow.Render()
    renderWindowInteractor.Start()
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    '''
    拾取点和展示点的下标
    '''
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
import numpy as np
def Normalized(a):
    '''
    normalize 0-1
    :param a: array you want normalize
    :return: a normalized array
    '''
    a = np.array(a)
    amin, amax = a.min(), a.max()
    a = (a - amin) / (amax - amin)
    return a
def getLookupTable(scalarRange, colorMapName):
    steps = 3
    step1 = (scalarRange[1] - scalarRange[0]) / steps
    index = colorMapIndex.get(colorMapName)
    if (abs(scalarRange[1] - scalarRange[0]) > 1e-10):
        pColorTable = vtk.vtkColorTransferFunction()
        pColorTable.AddRGBPoint(scalarRange[0], colorMap[index][0][0], colorMap[index][0][1],
                                colorMap[index][0][2])
        pColorTable.AddRGBPoint(scalarRange[0] + step1, colorMap[index][1][0], colorMap[index][1][1],
                                colorMap[index][1][2])
        pColorTable.AddRGBPoint(scalarRange[0] + 2 * step1, colorMap[index][2][0],
                                colorMap[index][2][1],
                                colorMap[index][2][2])
        pColorTable.AddRGBPoint(scalarRange[0] + 3 * step1, colorMap[index][3][0],
                                colorMap[index][3][1],
                                colorMap[index][3][2])
        return pColorTable
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