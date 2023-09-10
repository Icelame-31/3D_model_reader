# PyQt5==5.15.4
# vtk==9.1.0
import json
import os
import sys
import time

import numpy as np
import vtkmodules.all as vtk
from PIL import ImageGrab
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QHBoxLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MSPBP import IO
from MSPBP.GUI.pColorShow import getLookupTable, getLookupTableByUser, getScaleBarActor


# 设置窗口
class SettingsDialog(QDialog):
    settings_applied = QtCore.pyqtSignal(int, int, int, bool, bool, bool, bool, int, int, bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('设置')

        # region添加控件
        self.label_point_size = QLabel('初始点大小:')
        self.input_point_size = QLineEdit()

        self.label_next_time = QLabel('切换时间ms:')
        self.input_next_time = QLineEdit()

        self.label_init_angle = QLabel('初始角度:')
        self.input_init_angle = QLineEdit()

        self.label_rotate = QLabel('自动旋转:')
        self.rotate_group = QButtonGroup()
        self.radio_rotate_y = QRadioButton('是')
        self.radio_rotate_n = QRadioButton('否')
        self.radio_rotate_y.setChecked(True)
        self.rotate_group.addButton(self.radio_rotate_y)
        self.rotate_group.addButton(self.radio_rotate_n)

        self.label_hands_mode = QLabel('手动模式:')
        self.hands_mode_group = QButtonGroup()
        self.radio_hands_mode_y = QRadioButton('是')
        self.radio_hands_mode_n = QRadioButton('否')
        self.radio_hands_mode_n.setChecked(True)
        self.hands_mode_group.addButton(self.radio_hands_mode_y)
        self.hands_mode_group.addButton(self.radio_hands_mode_n)

        self.label_cycle = QLabel('循环播放:')
        self.cycle_group = QButtonGroup()
        self.radio_cycle_y = QRadioButton('是')
        self.radio_cycle_n = QRadioButton('否')
        self.radio_cycle_y.setChecked(True)
        self.cycle_group.addButton(self.radio_cycle_y)
        self.cycle_group.addButton(self.radio_cycle_n)

        self.label_save_image = QLabel('保存图片:')
        self.save_image_group = QButtonGroup()
        self.radio_save_image_y = QRadioButton('是')
        self.radio_save_image_n = QRadioButton('否')
        self.radio_save_image_n.setChecked(True)
        self.save_image_group.addButton(self.radio_save_image_y)
        self.save_image_group.addButton(self.radio_save_image_n)

        self.label_aix_select = QLabel('轴性选择:')
        self.aix_select = QtWidgets.QComboBox()
        self.aix_select.addItem("X轴")
        self.aix_select.addItem("Y轴")
        self.aix_select.addItem("Z轴")

        self.label_colormap_select = QLabel('ColorMap选择:')
        self.colormap_select = QtWidgets.QComboBox()
        self.colormap_select.addItem("Jet")
        self.colormap_select.addItem("HSV")
        self.colormap_select.addItem("Hot")
        self.colormap_select.addItem("Spring")
        self.colormap_select.addItem("Summer")
        self.colormap_select.addItem("Autum")
        self.colormap_select.addItem("Winter")
        self.colormap_select.addItem("Gray")
        self.colormap_select.addItem("Bone")
        self.colormap_select.addItem("Copper")
        self.colormap_select.addItem("Pink")
        self.colormap_select.addItem("Lines")

        # 添加按钮控件
        self.save_button = QPushButton('确定')
        self.cancel_button = QPushButton('取消')

        # 连接按钮信号和槽函数
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.my_close)
        # endregion

        # region布局控件
        layout = QVBoxLayout()

        point_size_layout = QHBoxLayout()
        point_size_layout.addWidget(self.label_point_size)
        point_size_layout.addWidget(self.input_point_size)
        layout.addLayout(point_size_layout)

        next_time_layout = QHBoxLayout()
        next_time_layout.addWidget(self.label_next_time)
        next_time_layout.addWidget(self.input_next_time)
        layout.addLayout(next_time_layout)

        init_angle_layout = QHBoxLayout()
        init_angle_layout.addWidget(self.label_init_angle)
        init_angle_layout.addWidget(self.input_init_angle)
        layout.addLayout(init_angle_layout)

        aix_select_layout = QHBoxLayout()
        aix_select_layout.addWidget(self.label_aix_select)
        aix_select_layout.addWidget(self.aix_select)
        layout.addLayout(aix_select_layout)

        colormap_select_layout = QHBoxLayout()
        colormap_select_layout.addWidget(self.label_colormap_select)
        colormap_select_layout.addWidget(self.colormap_select)
        layout.addLayout(colormap_select_layout)

        rotate_layout = QHBoxLayout()
        rotate_layout.addWidget(self.label_rotate)
        rotate_layout.addWidget(self.radio_rotate_y)
        rotate_layout.addWidget(self.radio_rotate_n)
        layout.addLayout(rotate_layout)

        hands_mode_layout = QHBoxLayout()
        hands_mode_layout.addWidget(self.label_hands_mode)
        hands_mode_layout.addWidget(self.radio_hands_mode_y)
        hands_mode_layout.addWidget(self.radio_hands_mode_n)
        layout.addLayout(hands_mode_layout)

        cycle_layout = QHBoxLayout()
        cycle_layout.addWidget(self.label_cycle)
        cycle_layout.addWidget(self.radio_cycle_y)
        cycle_layout.addWidget(self.radio_cycle_n)
        layout.addLayout(cycle_layout)

        save_image_layout = QHBoxLayout()
        save_image_layout.addWidget(self.label_save_image)
        save_image_layout.addWidget(self.radio_save_image_y)
        save_image_layout.addWidget(self.radio_save_image_n)
        layout.addLayout(save_image_layout)


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        # endregion
        # region读取配置文件，给定默认值
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
        else:
            config = {}
        self.input_point_size.setText(str(config.get('point_size')))
        self.input_next_time.setText(str(config.get('next_time')))
        self.input_init_angle.setText(str(config.get('init_angle')))
        if config.get('rotate'):
            self.radio_rotate_y.setChecked(True)
        else:
            self.radio_rotate_n.setChecked(True)
        if config.get('hands_mode'):
            self.radio_hands_mode_y.setChecked(True)
        else:
            self.radio_hands_mode_n.setChecked(True)
        if config.get('cycle'):
            self.radio_cycle_y.setChecked(True)
        else:
            self.radio_cycle_n.setChecked(True)
        if config.get('save_image'):
            self.radio_save_image_y.setChecked(True)
        else:
            self.radio_save_image_n.setChecked(True)
        if config.get('aix_select')!=None:
            self.aix_select.setCurrentIndex(int(config.get('aix_select')))
        if config.get('colormap_select')!=None:
            self.colormap_select.setCurrentIndex(int(config.get('colormap_select')))
        # endregion


    def save_settings(self):
        # 获取参数
        try:
            point_size = int(self.input_point_size.text())
        except:
            point_size = 1
        try:
            next_time = int(self.input_next_time.text())
        except:
            next_time = 1000
        try:
            init_angle = int(self.input_init_angle.text())
        except:
            init_angle = 0
        rotate = self.radio_rotate_y.isChecked()  # 自动旋转是否选中
        hands_mode = self.radio_hands_mode_y.isChecked()  # 自动旋转是否选中
        cycle = self.radio_cycle_y.isChecked()  # 自动旋转是否选中
        save_image = self.radio_save_image_y.isChecked()  # 自动旋转是否选中
        aix_select = self.aix_select.currentIndex()
        colormap_select = self.colormap_select.currentIndex()
        # 参数保存到文件中
        config = {
            'point_size': point_size,
            'next_time': next_time,
            'init_angle': init_angle,
            'rotate': rotate,
            'cycle': cycle,
            'hands_mode': hands_mode,
            'save_image': save_image,
            'aix_select': aix_select,
            'colormap_select': colormap_select,
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
        # 信号返回
        self.settings_applied.emit(point_size, next_time, init_angle, rotate, hands_mode, cycle, save_image, aix_select, colormap_select, False)
        self.close()

    def my_close(self):
        self.settings_applied.emit(1, 1, 0, False, False, False, False, 0, 0, True)
        self.close()


# 主窗口
class Ui_MainWindow(QMainWindow):

    # 设置UI
    def setupUi(self, MainWindow):
        # 设置窗口长宽
        screen = ImageGrab.grab()
        window_width, window_height = screen.size
        window_width = int(window_width * 0.8)
        window_height = int(window_height * 0.8)
        # window_height = int(window_height - 95)

        # 设置窗口
        MainWindow.setObjectName("vtk")
        MainWindow.resize(window_width, window_height)  # 长，宽
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 画布
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(8, 8, window_width - 16, window_height - 50))
        self.widget.setObjectName("widget")
        self.vtk_show = QVTKRenderWindowInteractor(self.widget)
        self.vtk_show.resize(self.widget.size())

        # 创建菜单栏
        self.menubar = QMenuBar(MainWindow)
        # 主菜单
        self.open_menu = QMenu("打开模型", self.menubar)
        self.colormap_menu = QMenu("ColorMap", self.menubar)
        self.object_menu = QMenu("设置对象", self.menubar)
        self.pc_xyz_menu = QAction("打开点云XYZ", MainWindow)
        self.pc_seq_menu = QAction("打开点云序列", MainWindow)
        self.next_menu = QAction("下一帧", MainWindow)
        self.add_menu = QAction("增加点大小", MainWindow)
        self.sub_menu = QAction("减小点大小", MainWindow)
        self.rotate_menu = QAction("模型旋转", MainWindow)
        self.menubar.addMenu(self.open_menu)
        self.menubar.addMenu(self.colormap_menu)
        self.menubar.addMenu(self.object_menu)
        self.menubar.addAction(self.pc_xyz_menu)
        self.menubar.addAction(self.pc_seq_menu)
        self.menubar.addAction(self.next_menu)
        self.menubar.addAction(self.add_menu)
        self.menubar.addAction(self.sub_menu)
        self.menubar.addAction(self.rotate_menu)
        # 设置禁用状态
        self.next_menu.setEnabled(False)

        # 二级菜单 打开模型
        self.off_open = QAction("打开OFF文件", MainWindow)
        self.obj_open = QAction("打开OBJ文件", MainWindow)
        self.ply_open = QAction("打开PLY文件", MainWindow)
        self.stl_open = QAction("打开STL文件", MainWindow)
        self.vtk_open = QAction("打开VTK文件", MainWindow)
        self.pts_open = QAction("打开PTS文件", MainWindow)
        self.open_menu.addAction(self.off_open)
        self.open_menu.addAction(self.obj_open)
        self.open_menu.addAction(self.ply_open)
        self.open_menu.addAction(self.stl_open)
        self.open_menu.addAction(self.vtk_open)
        self.open_menu.addAction(self.pts_open)

        # 二级菜单 ColorMap
        self.aix_select = QMenu("轴性选择", self.menubar)
        self.color_select = QMenu("颜色模式", self.menubar)
        self.colormap_menu.addMenu(self.aix_select)
        self.colormap_menu.addMenu(self.color_select)

        # 二级菜单 设置对象
        self.edge_open = QAction("打开边界边", MainWindow)
        self.bg_color = QAction("修改背景颜色", MainWindow)
        self.obj_color = QAction("修改对象颜色", MainWindow)
        self.edge_color = QAction("修改边界边颜色", MainWindow)
        self.object_menu.addAction(self.edge_open)
        self.object_menu.addAction(self.bg_color)
        self.object_menu.addAction(self.obj_color)
        self.object_menu.addAction(self.edge_color)

        # 三级菜单 轴性选择
        self.aix_x = QAction("X轴", MainWindow)
        self.aix_y = QAction("Y轴", MainWindow)
        self.aix_z = QAction("Z轴", MainWindow)
        self.read_from_file = QAction("文件读取", MainWindow)
        self.aix_select.addAction(self.aix_x)
        self.aix_select.addAction(self.aix_y)
        self.aix_select.addAction(self.aix_z)
        self.aix_select.addAction(self.read_from_file)

        # 三级菜单 颜色模式
        self.color_jet = QAction("Jet", MainWindow)
        self.color_hsv = QAction("HSV", MainWindow)
        self.color_hot = QAction("Hot", MainWindow)
        self.color_cool = QAction("Cool", MainWindow)
        self.color_spring = QAction("Spring", MainWindow)
        self.color_summer = QAction("Summer", MainWindow)
        self.color_autum = QAction("Autum", MainWindow)
        self.color_winter = QAction("Winter", MainWindow)
        self.color_gray = QAction("Gray", MainWindow)
        self.color_bone = QAction("Bone", MainWindow)
        self.color_copper = QAction("Copper", MainWindow)
        self.color_pink = QAction("Pink", MainWindow)
        self.color_lines = QAction("Lines", MainWindow)
        self.color_read = QAction("文件读取", MainWindow)
        self.color_select.addAction(self.color_jet)
        self.color_select.addAction(self.color_hsv)
        self.color_select.addAction(self.color_hot)
        self.color_select.addAction(self.color_cool)
        self.color_select.addAction(self.color_spring)
        self.color_select.addAction(self.color_summer)
        self.color_select.addAction(self.color_autum)
        self.color_select.addAction(self.color_winter)
        self.color_select.addAction(self.color_gray)
        self.color_select.addAction(self.color_bone)
        self.color_select.addAction(self.color_copper)
        self.color_select.addAction(self.color_pink)
        self.color_select.addAction(self.color_lines)
        self.color_select.addAction(self.color_read)

        MainWindow.setMenuBar(self.menubar)

        # 设置菜单按钮连接的功能
        # 打开模型
        self.off_open.triggered.connect(self.read_off)
        self.obj_open.triggered.connect(self.read_obj)
        self.ply_open.triggered.connect(self.read_ply)
        self.stl_open.triggered.connect(self.read_stl)
        self.vtk_open.triggered.connect(self.read_vtk)
        self.pts_open.triggered.connect(self.read_point_cloud)
        # ColorMap
        self.aix_x.triggered.connect(self.functionxyz_aix_x)
        self.aix_y.triggered.connect(self.functionxyz_aix_y)
        self.aix_z.triggered.connect(self.functionxyz_aix_z)
        self.read_from_file.triggered.connect(self.functionxyz_read_from_file)
        # 设置对象
        self.edge_open.triggered.connect(self.show_edge)
        self.bg_color.triggered.connect(self.change_bg)
        self.obj_color.triggered.connect(self.change_3d)
        self.edge_color.triggered.connect(self.change_edge)
        # 轴性选择
        self.color_jet.triggered.connect(self.colormap_jet)
        self.color_hsv.triggered.connect(self.colormap_hsv)
        self.color_hot.triggered.connect(self.colormap_hot)
        self.color_cool.triggered.connect(self.colormap_cool)
        self.color_spring.triggered.connect(self.colormap_spring)
        self.color_summer.triggered.connect(self.colormap_summer)
        self.color_autum.triggered.connect(self.colormap_autum)
        self.color_winter.triggered.connect(self.colormap_winter)
        self.color_gray.triggered.connect(self.colormap_gray)
        self.color_bone.triggered.connect(self.colormap_bone)
        self.color_copper.triggered.connect(self.colormap_copper)
        self.color_pink.triggered.connect(self.colormap_pink)
        self.color_lines.triggered.connect(self.colormap_lines)
        self.color_read.triggered.connect(self.colormap_read)
        # 主菜单
        self.pc_xyz_menu.triggered.connect(self.read_point_cloud_xyz)
        self.pc_seq_menu.triggered.connect(self.read_point_cloud_seq)
        self.next_menu.triggered.connect(self.read_point_cloud_seq_next)
        self.add_menu.triggered.connect(self.add_points_size)
        self.sub_menu.triggered.connect(self.not_add_points_size)
        self.rotate_menu.triggered.connect(self.rotate)

        # region初始化参数
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage('OK')
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sphere = None
        self.mapper = None
        self.actor = None
        self.edgeActor = None
        self.renderer = None
        self.i_ren = None
        self.filename = ""
        self.colorbg = (1.0, 1.0, 1.0)
        self.color3d = (1.0, 1.0, 1.0)
        self.coloreg = (1.0, 0, 0)
        self.xyz = "X轴"
        self.readXYZ = None
        self.is_user_colormap = False
        self.user_colormap = None
        self.colormapname = 'Jet'
        self.timer_count = 0
        self.is_show_seq = False
        self.remaining_time = 0
        self.point_size = 0
        self.next_time = 1000
        self.auto_rotate = True
        self.hands_mode = False
        self.cycle = True
        self.init_angle = 0
        self.save_image = False
        self.aix_select = 0
        self.colormap_select = 0
        self.is_close = True
        # endregion
    # 设置UI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "三维模型阅读器 [西红柿炒番茄出品]"))

    # 读取文件中的点云序列
    def read_point_cloud_seq(self):
        # 开始播放序列
        if self.is_show_seq:
            self.timer.stop()
            self.pc_seq_menu.setText('打开点云序列')
            self.next_menu.setEnabled(False)
            self.is_show_seq = False
        else:
            # 打开设置窗口
            setting_window = SettingsDialog()
            setting_window.settings_applied.connect(self.handle_settings_applied)
            setting_window.exec_()

    # 接受设置窗口传来的参数
    def handle_settings_applied(self, point_size, next_time, init_angle, rotate, hands_mode, cycle, save_image, aix_select, colormap_select, is_close):
        # 接受设置参数
        self.point_size, self.next_time, self.init_angle, self.auto_rotate, self.hands_mode, self.cycle, self.save_image, self.aix_select, self.colormap_select, self.is_close = point_size, next_time, init_angle, rotate, hands_mode, cycle, save_image, aix_select, colormap_select, is_close
        if self.is_close:
            return
        # 展示
        self.read_file('xyz')
        if self.filename != "":
            self.is_show_seq = True
            # 获取目录中的所有点云文件
            self.xyz_file_path = os.path.dirname(self.filename)
            self.xyz_files = os.listdir(self.xyz_file_path)
            self.xyz_files = [x for x in self.xyz_files if '.xyz' in x]

            try:
                self.xyz_files.sort(key=lambda x: int(x.split('.')[0]))
            except:
                pass

            # 创建定时器，每秒更新一次
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.timer_show_xyz)
            self.remaining_time = len(self.xyz_files) - 1
            self.timer_show_xyz()
            if self.save_image:
                self.save_img()
            if self.hands_mode:
                self.next_menu.setEnabled(True)
            else:
                self.timer.start(self.next_time)  # 3秒钟更新一次
            self.pc_seq_menu.setText('停止播放')
        else:
            self.statusbar.showMessage("取消文件选择")

    def rotate(self):
        if self.i_ren == None:
            return
        self.i_ren.AddObserver('TimerEvent', self.rotate_execute)
        self.i_ren.CreateRepeatingTimer(100)
        self.vtk_show.update()
        self.vtk_show.Start()

    def rotate_execute(self, obj, event):
        if self.timer_count % 1 == 0:
            self.actor.RotateY(1)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1

    def read_point_cloud(self):
        self.read_file('pts')
        if self.filename != "":
            m_points = vtk.vtkPoints()
            vertices = vtk.vtkCellArray()

            file_content = []
            with open(self.filename, 'r') as f:
                file_content = [x.strip() for x in f.readlines()]

            self.v_list = []
            for i, x in enumerate(file_content):
                line = [float(s) for s in x.split(" ")]
                if len(line) == 3:
                    self.v_list.append(line)
                    m_points.InsertPoint(i, line[0], line[1], line[2])
                    vertices.InsertNextCell(1)
                    vertices.InsertCellPoint(i)
            self.v_list = np.array(self.v_list)

            self.cube = vtk.vtkPolyData()
            self.cube.SetPoints(m_points)
            self.cube.SetVerts(vertices)

            # 创建 mapper 和 actor
            self.mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                self.mapper.SetInput(self.cube)
            else:
                self.mapper.SetInputData(self.cube)

            self.actor = vtk.vtkActor()
            self.actor.SetMapper(self.mapper)
            self.actor.GetProperty().SetColor(self.color3d)

            self.renderer = vtk.vtkRenderer()
            self.renderer.AddActor(self.actor)
            self.renderer.SetBackground((0.0, 0.0, 0.0))

            render_window = self.vtk_show.GetRenderWindow()
            for renderer in render_window.GetRenderers():
                render_window.RemoveRenderer(renderer)
                renderer.RemoveAllViewProps()
            self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
            self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
            self.vtk_show.Render()
            self.i_ren.Initialize()
            self.vtk_show.update()
            self.vtk_show.Start()

        else:
            self.statusbar.showMessage("取消文件选择")

    def read_point_cloud_xyz(self):
        self.read_file('xyz')
        if self.filename != "":
            self.deal_point_cloud_xyz(self.filename)
            self.statusbar.showMessage(f'{self.filename} ({self.points_number})')
        else:
            self.statusbar.showMessage("取消文件选择")

    def read_point_cloud_seq_next(self):
        self.timer_show_xyz()
        # self.save_img()

    # 保存成图片
    def save_img(self):
        renWin = self.vtk_show.GetRenderWindow()
        # 将窗口保存为PNG图像
        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(renWin)
        w2i.Update()

        if not os.path.exists('./output_img'):
            os.mkdir('./output_img')

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(f"./output_img/{time.strftime('%Y_%m_%d_%H_%M_%S')}.png")
        writer.SetInputData(w2i.GetOutput())
        writer.Write()

    def timer_show_xyz(self):
        if self.remaining_time >= 0:
            xyz_list = ['X轴', 'Y轴', 'Z轴']
            colormap_list = ['Jet', 'HSV', 'Hot', 'Spring', 'Summer', 'Autum', 'Winter', 'Gray', 'Bone', 'Copper', 'Pink', 'Lines']
            self.deal_point_cloud_xyz(os.path.join(self.xyz_file_path, self.xyz_files[self.remaining_time]), points_size=self.point_size, init_rotate=self.init_angle, xyz=xyz_list[self.aix_select], colormap=colormap_list[self.colormap_select])
            # 保存图片
            if self.save_image:
                self.save_img()
            # 设置是否自动旋转
            if self.auto_rotate:
                self.rotate()

            fp = os.path.join(self.xyz_file_path, self.xyz_files[self.remaining_time])
            self.statusbar.showMessage(f'{fp} ({self.points_number})')
            self.remaining_time -= 1
        else:
            if self.cycle:  # 循环播放
                self.remaining_time = len(self.xyz_files) - 1
                self.timer_show_xyz()
            else: # 播放完停止
                self.timer.stop()
                self.pc_seq_menu.setText('打开点云序列')
                self.next_menu.setEnabled(False)
                self.is_show_seq = False

    def deal_point_cloud_xyz(self, filename, points_size=1, init_rotate=None, colormap=None, xyz=None):
        m_points = vtk.vtkPoints()
        vertices = vtk.vtkCellArray()

        file_content = []
        with open(filename, 'r') as f:
            file_content = [x.strip() for x in f.readlines()]
        # 点云中心移动到坐标原点
        points = [x.split(' ') for x in file_content]
        points = np.array(points, dtype=float)
        center = np.mean(points, axis=0)
        points -= center
        self.points_number = points.shape[0]

        self.v_list = []
        for i, x in enumerate(points):
            line = [float(x[0]), float(x[1]), float(x[2])]
            if len(line) == 3:
                self.v_list.append(line)
                m_points.InsertPoint(i, line[0], line[1], line[2])
                vertices.InsertNextCell(1)
                vertices.InsertCellPoint(i)
        self.v_list = np.array(self.v_list)

        self.cube = vtk.vtkPolyData()
        self.cube.SetPoints(m_points)
        self.cube.SetVerts(vertices)

        # 创建 mapper 和 actor
        self.mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(self.cube)
        else:
            self.mapper.SetInputData(self.cube)

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        if init_rotate!=None:
            self.actor.RotateY(init_rotate)
        self.actor.GetProperty().SetColor([0, 0, 0])
        self.points_size = points_size
        self.actor.GetProperty().SetPointSize(self.points_size)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground((1.0, 1.0, 1.0))

        render_window = self.vtk_show.GetRenderWindow()
        for renderer in render_window.GetRenderers():
            render_window.RemoveRenderer(renderer)
            renderer.RemoveAllViewProps()

        self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
        self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
        self.vtk_show.Render()
        self.i_ren.Initialize()
        self.vtk_show.update()
        self.vtk_show.Start()

        if xyz!=None:
            self.functionxyz(xyz)
        if colormap!=None:
            self.colormap(colormap)

    def add_points_size(self):
        self.points_size += 1
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor([0, 0, 0])
        self.actor.GetProperty().SetPointSize(self.points_size)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground((1.0, 1.0, 1.0))

        render_window = self.vtk_show.GetRenderWindow()
        for renderer in render_window.GetRenderers():
            render_window.RemoveRenderer(renderer)
            renderer.RemoveAllViewProps()

        self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
        self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
        self.vtk_show.Render()
        self.i_ren.Initialize()
        self.vtk_show.update()
        self.vtk_show.Start()

    def not_add_points_size(self):
        self.points_size -= 1
        if self.points_size < 1:
            self.points_size = 1
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor([0, 0, 0])
        self.actor.GetProperty().SetPointSize(self.points_size)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground((1.0, 1.0, 1.0))

        render_window = self.vtk_show.GetRenderWindow()
        for renderer in render_window.GetRenderers():
            render_window.RemoveRenderer(renderer)
            renderer.RemoveAllViewProps()

        self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
        self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
        self.vtk_show.Render()
        self.i_ren.Initialize()
        self.vtk_show.update()
        self.vtk_show.Start()

    def read_off(self):
        self.read_file("off")
        if self.filename != "":
            self.off2obj()
            self.show_actor("三维文件/1.obj")
        else:
            self.statusbar.showMessage("取消文件选择")

    def read_obj(self):
        self.read_file("obj")
        if self.filename != "":
            self.show_actor(self.filename)
        else:
            self.statusbar.showMessage("取消文件选择")

    def show_actor(self, filename=''):
        item = QStandardItem()
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 有复选框 可用
        item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
        item.setData(filename, Qt.UserRole)
        item.setData(filename.split('/')[-1], Qt.DisplayRole)  # 0.obj  0
        self.v_list, self.f_list = IO.pReadOBJ(item.data(Qt.UserRole))

        # 添加点
        points = vtk.vtkPoints()
        for v in self.v_list:
            points.InsertNextPoint(v)

        # 添加面片
        polys = vtk.vtkCellArray()
        for f in self.f_list:
            polys.InsertNextCell(len(f), f)

        # 创建PolyData
        self.cube = vtk.vtkPolyData()
        self.cube.SetPoints(points)
        self.cube.SetPolys(polys)

        # 创建 mapper 和 actor
        self.mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(self.cube)
        else:
            self.mapper.SetInputData(self.cube)

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(self.color3d)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(self.colorbg)

        render_window = self.vtk_show.GetRenderWindow()
        for renderer in render_window.GetRenderers():
            render_window.RemoveRenderer(renderer)
            renderer.RemoveAllViewProps()

        self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
        self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
        self.vtk_show.Render()
        self.i_ren.Initialize()
        self.vtk_show.update()
        self.vtk_show.Start()

    def colormap_jet(self):
        self.colormap('Jet')

    def colormap_hsv(self):
        self.colormap('HSV')

    def colormap_hot(self):
        self.colormap('Hot')

    def colormap_cool(self):
        self.colormap('Cool')

    def colormap_spring(self):
        self.colormap('Spring')

    def colormap_summer(self):
        self.colormap('Summer')

    def colormap_autum(self):
        self.colormap('Autum')

    def colormap_winter(self):
        self.colormap('Winter')

    def colormap_gray(self):
        self.colormap('Gray')

    def colormap_bone(self):
        self.colormap('Bone')

    def colormap_copper(self):
        self.colormap('Copper')

    def colormap_pink(self):
        self.colormap('Pink')

    def colormap_lines(self):
        self.colormap('Lines')

    def colormap_read(self):
        self.colormap('Read')

    def colormap(self, colormapname='Jet'):
        if colormapname == 'Read':
            self.read_file('txt')
            if self.filename != '':
                with open(self.filename, 'r') as f:
                    self.user_colormap = [float(line.rstrip("\n")) for line in f.readlines()]
                    if len(self.user_colormap) < 12:
                        self.is_user_colormap = False
                        self.statusbar.showMessage("colormap数值取前12行，行数不足。[过多时忽略12行以后的数值]")
                        return False
                    else:
                        self.is_user_colormap = True
        else:
            self.is_user_colormap = False
            self.colormapname = colormapname

        if self.xyz == '':
            self.statusbar.showMessage("请先选择xyz轴")
        else:
            self.statusbar.showMessage(self.xyz + ' ' + colormapname)
            if self.actor != None and not (self.filename == '' and colormapname == 'Read'):
                self.actor.GetMapper().ScalarVisibilityOn()
                if self.edgeActor != None:
                    self.edgeActor.GetMapper().ScalarVisibilityOn()
                if self.xyz == 'X轴' or self.xyz == 'Write_X':
                    fun = self.v_list[:, 0]
                elif self.xyz == 'Y轴' or self.xyz == 'Write_Y':
                    fun = self.v_list[:, 1]
                elif self.xyz == 'Z轴' or self.xyz == 'Write_Z':
                    fun = self.v_list[:, 2]
                elif self.xyz == 'Read':
                    if self.readXYZ == None:
                        fun = self.v_list[:, 0]
                    else:
                        xp = np.arange(0, self.v_list.shape[0], self.v_list.shape[0] / len(self.readXYZ))
                        fp = np.array(self.readXYZ)
                        x = range(self.v_list.shape[0])
                        fun = np.interp(x, xp, fp)

                scalars = vtk.vtkFloatArray()
                fun = np.array(fun).reshape((len(self.v_list), 1))
                for i in range(len(self.v_list)):
                    scalars.InsertTuple1(i, fun[i, 0])
                cube = self.cube
                cube.GetPointData().SetScalars(scalars)
                scalarRange = [fun.min(), fun.max()]
                if self.is_user_colormap:
                    pColorTable = getLookupTableByUser(scalarRange, colorMap=self.user_colormap)
                else:
                    if colormapname != 'Read':
                        pColorTable = getLookupTable(scalarRange, colorMapName=colormapname)

                mapper = self.mapper
                mapper.SetScalarRange(scalarRange[0], scalarRange[1])
                mapper.SetLookupTable(pColorTable)
                actor = self.actor
                actor.SetMapper(mapper)
                transform = vtk.vtkTransform()
                transform.PostMultiply()
                actor.SetUserTransform(transform)
                scalarBar = getScaleBarActor(pColorTable)
                render = self.renderer
                render.AddActor2D(scalarBar)
                render.ResetCamera()
                self.vtk_show.update()
            else:
                self.statusbar.showMessage("请先选择要显示的文件")

    def functionxyz_aix_x(self):
        self.functionxyz('X轴')

    def functionxyz_aix_y(self):
        self.functionxyz('Y轴')

    def functionxyz_aix_z(self):
        self.functionxyz('Z轴')

    def functionxyz_read_from_file(self):
        self.functionxyz('Read')

    def functionxyz(self, xyz):
        self.statusbar.showMessage(xyz)
        self.xyz = xyz
        if xyz == 'Read':
            self.read_file('txt')
            if self.filename != '':
                with open(self.filename, 'r') as f:
                    self.readXYZ = [float(line.rstrip("\n")) for line in f.readlines()]

        if xyz == 'Write_X':
            if self.actor != None:
                with open('其他文件/w_x.txt', 'w') as f:
                    xzx = [str(x) + '\n' for x in self.v_list[:, 0]]
                    f.writelines(xzx)
                self.statusbar.showMessage("成功写出X坐标到文件w_x.txt")
            else:
                self.statusbar.showMessage("请先打开文件")

        if xyz == 'Write_Y':
            if self.actor != None:
                with open('其他文件/w_y.txt', 'w') as f:
                    xzx = [str(x) + '\n' for x in self.v_list[:, 1]]
                    f.writelines(xzx)
                self.statusbar.showMessage("成功写出Y坐标到文件w_y.txt")
            else:
                self.statusbar.showMessage("请先打开文件")

        if xyz == 'Write_Z':
            if self.actor != None:
                with open('其他文件/w_z.txt', 'w') as f:
                    xzx = [str(x) + '\n' for x in self.v_list[:, 2]]
                    f.writelines(xzx)
                self.statusbar.showMessage("成功写出Z坐标到文件w_z.txt")
            else:
                self.statusbar.showMessage("请先打开文件")
        self.colormap(colormapname=self.colormapname)

    def read_ply(self):
        self.read_file("ply")
        if self.filename != "":
            self.sphere = vtk.vtkPLYReader()
            self.sphere.SetFileName(self.filename)
            self.sphere.Update()
            self.show()

    def read_stl(self):
        self.read_file("stl")
        if self.filename != "":
            self.sphere = vtk.vtkSTLReader()
            self.sphere.SetFileName(self.filename)
            self.sphere.Update()
            self.show()

    def read_vtk(self):
        self.read_file("vtk")
        if self.filename != "":
            self.sphere = vtk.vtkPolyDataReader()
            self.sphere.SetFileName(self.filename)
            self.sphere.Update()
            self.show()

    def show_edge(self):
        if self.renderer != None:
            _translate = QtCore.QCoreApplication.translate
            if self.edgeActor == None:
                self.edge_open.setText('关闭边界边')
                featureEdges = vtk.vtkFeatureEdges()
                featureEdges.SetInputData(self.cube)
                featureEdges.BoundaryEdgesOn()
                featureEdges.FeatureEdgesOff()
                featureEdges.ManifoldEdgesOff()
                featureEdges.NonManifoldEdgesOff()
                featureEdges.ColoringOff()
                featureEdges.Update()
                edgeMapper = vtk.vtkPolyDataMapper()
                edgeMapper.SetInputConnection(featureEdges.GetOutputPort())
                self.edgeActor = vtk.vtkActor()
                self.edgeActor.SetMapper(edgeMapper)
                self.edgeActor.GetProperty().SetColor(self.coloreg)
                self.renderer.AddActor(self.edgeActor)
            else:
                self.edge_open.setText('打开边界边')
                self.renderer.RemoveActor(self.edgeActor)
                self.edgeActor = None
        else:
            self.statusbar.showMessage("请先选择要显示的文件")

    def change_edge(self):
        if self.edgeActor != None:
            color = QColorDialog.getColor()
            if color.isValid():
                self.edgeActor.GetMapper().ScalarVisibilityOff()
                self.coloreg = color.getRgb()[0:3]
                color_list = list(self.coloreg)
                color_list[0] = float(color_list[0] / 255)
                color_list[1] = float(color_list[1] / 255)
                color_list[2] = float(color_list[2] / 255)
                self.coloreg = tuple(color_list)
                self.edgeActor.GetProperty().SetColor(self.coloreg)
        else:
            self.statusbar.showMessage("请先打开边界边")

    def change_bg(self):
        if self.renderer != None:
            color = QColorDialog.getColor()
            if color.isValid():
                self.colorbg = color.getRgb()[0:3]
                color_list = list(self.colorbg)
                color_list[0] = float(color_list[0] / 255)
                color_list[1] = float(color_list[1] / 255)
                color_list[2] = float(color_list[2] / 255)
                self.colorbg = tuple(color_list)
                self.renderer.SetBackground(self.colorbg)
        else:
            self.statusbar.showMessage("请先选择要显示的文件")

    def change_3d(self):
        if self.actor != None:
            color = QColorDialog.getColor()
            if color.isValid():
                self.actor.GetMapper().ScalarVisibilityOff()
                self.color3d = color.getRgb()[0:3]
                color_list = list(self.color3d)
                color_list[0] = float(color_list[0] / 255)
                color_list[1] = float(color_list[1] / 255)
                color_list[2] = float(color_list[2] / 255)
                self.color3d = tuple(color_list)
                self.actor.GetProperty().SetColor(self.color3d)
        else:
            self.statusbar.showMessage("请先选择要显示的文件")

    def show(self):
        # 2.polyDataMapper
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.sphere.GetOutputPort())
        self.mapper.Update()

        # 3.actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(self.color3d)

        # 4.renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(self.colorbg)

        # 5.windows
        render_window = self.vtk_show.GetRenderWindow()
        for renderer in render_window.GetRenderers():
            render_window.RemoveRenderer(renderer)
            renderer.RemoveAllViewProps()
        self.vtk_show.GetRenderWindow().AddRenderer(self.renderer)
        self.i_ren = self.vtk_show.GetRenderWindow().GetInteractor()
        self.vtk_show.Render()
        self.i_ren.Initialize()
        self.vtk_show.Start()

    def read_file(self, file_type):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.filename, _ = dialog.getOpenFileName(dialog, "Open file", "", "files (*." + file_type + ")")
        self.statusbar.showMessage(self.filename)

    def off2obj(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        v_num = 10
        outputlines = list()
        for i in range(0, len(lines)):
            lines[i] = lines[i].rstrip('\n')
            # 获取定点数和面数
            if i == 1:
                line = lines[i].split(" ")
                v_num = int(line[0])
            # 定点数据生成
            if i > 1 and i < (v_num + 2):
                s = "v " + lines[i] + "\n"
                outputlines.append(s)
            # 面数据生成
            if i > (v_num + 1):
                ss = lines[i].split(" ")
                news = ""
                if ss[0] != "":
                    for j in range(1, int(ss[0]) + 1):
                        ss[j] = str(int(ss[j]) + 1)
                        news += " " + ss[j]
                    s = "f " + news + "\n"
                    outputlines.append(s)
        fw = open("三维文件/1.obj", "w")
        fw.writelines(outputlines)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # ui = Setting_xyz_seq()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
