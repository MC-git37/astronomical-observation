import time
import traceback
from datetime import date
import matplotlib  #画图
from tianxian import functions
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg #画图
import astropy.coordinates as apyc  #天文坐标系
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure  #导入画图模块Figure
from datetime import datetime
import numpy as np  #数值计算扩展
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u  #单位换算
from socket import *
#import functions
#from youhua import function #导入文件
from untitle import Ui_MainWindow
import datetime
from matplotlib import pyplot as plt
import uv as uv
countdown = 0
a=0
a2=0
a3=0
a4=0
a5=0
a6=0
a7=0
a8=0
a9=0
a10=0
b1=0
b2=0
b3=0
b4=0
b5=0
b6=0
b7=0
b8=0
b9=0
b10=0
current_shown_pulsar_index = 0
Lat = 0
Lon =0
c=0
alt_star=20
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, autoscale_on=False)
        functions.polar_anno(self.axes)
        super(MplCanvas, self).__init__(self.fig)
class MplCanvas_1(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, autoscale_on=True)
        functions.polar_anno(self.axes)
        super(MplCanvas_1, self).__init__(self.fig)

class MplCanvas_2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, autoscale_on=True)
        # self.axes = plt.subplot(111, autoscale_on=True)
        super(MplCanvas_2, self).__init__(self.fig)


class MainWindow(QMainWindow):  #程序主界面
    def __init__(self, flags, *args, **kwargs):
        super().__init__()
        self.setWindowTitle("Antenna Control")
        self.timerForCom = QTimer()  # for com and update alt and az
        self.timerForCom.setInterval(1000)
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1s 刷新一次
        self.timer2 = QTimer()
        self.timer2.setInterval(1000 )  # 再定义一个计时器，1分钟执行一次
        self.timerShowCurrentLst = QTimer()
        self.timerShowCurrentLst.setInterval(1000)
        self.timersave = QTimer()
        self.timersave.setInterval(1000)
        self.timer3=QTimer()
        self.timer3.setInterval(1000)
        self.mainView = Ui_MainWindow()   # showCurrentLST
        self.mainView.setupUi(self)
        self.resize(2000, 1000)  #
        self.threadpool = QThreadPool()
        self.init_telescope_status()
        self.initView()  # self.init_LST_status()
        self.initView_1()  # self.init_LST_status()
        self.initView_2()  # self.init_LST_status()
        self.init_listeners()
        self.timerForCom.start()

    def initView_2(self):
        matplotlib.rcParams['axes.unicode_minus'] = False #坐标轴负号
        hboxlayout = QHBoxLayout()
        self.canvas_2 = MplCanvas_2(self)
        hboxlayout.addWidget(self.canvas_2)
        self.mainView.widget_graphics_3.setLayout(hboxlayout)
        self.mainView.widget_graphics_3.show()

    def initView_1(self):
        hboxlayout = QHBoxLayout()  # central part
        self.canvas_1 = MplCanvas_1(self)
        hboxlayout.addWidget(self.canvas_1)
        self.mainView.widget_graphics_2.setLayout(hboxlayout)
        self.mainView.widget_graphics_2.show()

    def initView(self):
        hboxlayout = QHBoxLayout()  # central part
        self.canvas = MplCanvas(self)
        hboxlayout.addWidget(self.canvas)
        self.mainView.widget_graphics.setLayout(hboxlayout)
        self.mainView.widget_graphics.show()
        #self.mainView.lcd_remaining_time.setDigitCount(10)  # right pannel
        #self.mainView.pb_load_sourceFile_cancel.setEnabled(False)

    def init_listeners(self): #按钮调用
        self.mainView.pushButton_browse_src.clicked.connect(self.onBtnBrowseClicked)
        self.mainView.pushButton_browse_src_2.clicked.connect(self.onBtnBrowseClicked_2)
        self.mainView.pb_load_sourceFile_submit.clicked.connect(self.onBtnSubmitClicked)
        self.mainView.pb_load_sourceFile_submit_2.clicked.connect(self.onBtnSubmitClicked_2)
        self.mainView.pb_load_sourceFile_cancel.clicked.connect(self.onBtnCancelClicked)
        self.mainView.pb_load_sourceFile_cancel_2.clicked.connect(self.onBtnCancelClicked_2)
        self.mainView.pb_load_sourceFile_import.clicked.connect(self.onBtnimportClicked_1)
        self.mainView.pb_load_sourceFile_import_2.clicked.connect(self.onBtnimportClicked_2)
        self.mainView.pb_load_sourceFile_import_3.clicked.connect(self.onBtnimportClicked_3)
        self.mainView.pb_load_sourceFile_import_4.clicked.connect(self.onBtnimportClicked_4)
        self.mainView.pb_load_sourceFile_import_5.clicked.connect(self.onBtnimportClicked_5)
        self.mainView.pb_load_sourceFile_import_6.clicked.connect(self.onBtnimportClicked_6)
        self.mainView.pb_load_sourceFile_import_7.clicked.connect(self.onBtnimportClicked_7)
        self.mainView.pb_load_sourceFile_import_8.clicked.connect(self.onBtnimportClicked_8)
        self.mainView.pb_load_sourceFile_import_9.clicked.connect(self.onBtnimportClicked_9)
        self.mainView.pb_load_sourceFile_import_10.clicked.connect(self.onBtnimportClicked_10)
        self.mainView.track_1.clicked.connect(self.onBtntrackClicked_1)
        self.mainView.track_2.clicked.connect(self.onBtntrackClicked_2)
        self.mainView.track_3.clicked.connect(self.onBtntrackClicked_3)
        self.mainView.track_4.clicked.connect(self.onBtntrackClicked_4)
        self.mainView.track_5.clicked.connect(self.onBtntrackClicked_5)
        self.mainView.track_6.clicked.connect(self.onBtntrackClicked_6)
        self.mainView.track_7.clicked.connect(self.onBtntrackClicked_7)
        self.mainView.track_8.clicked.connect(self.onBtntrackClicked_8)
        self.mainView.track_9.clicked.connect(self.onBtntrackClicked_9)
        self.mainView.track_10.clicked.connect(self.onBtntrackClicked_10)
        self.mainView.stop_1.clicked.connect(self.onBtnstop_1)
        self.mainView.stop_2.clicked.connect(self.onBtnstop_2)
        self.mainView.stop_3.clicked.connect(self.onBtnstop_3)
        self.mainView.stop_4.clicked.connect(self.onBtnstop_4)
        self.mainView.stop_5.clicked.connect(self.onBtnstop_5)
        self.mainView.stop_6.clicked.connect(self.onBtnstop_6)
        self.mainView.stop_7.clicked.connect(self.onBtnstop_7)
        self.mainView.stop_8.clicked.connect(self.onBtnstop_8)
        self.mainView.stop_9.clicked.connect(self.onBtnstop_9)
        self.mainView.stop_10.clicked.connect(self.onBtnstop_10)
        self.mainView.sort_1.clicked.connect(self.onBtnsort_1)
        self.mainView.sort_2.clicked.connect(self.onBtnsort_2)
        self.mainView.sort_3.clicked.connect(self.onBtnsort_3)
        self.mainView.sort_4.clicked.connect(self.onBtnsort_4)
        self.mainView.sort_5.clicked.connect(self.onBtnsort_5)
        self.mainView.sort_6.clicked.connect(self.onBtnsort_6)
        self.mainView.sort_7.clicked.connect(self.onBtnsort_7)
        self.mainView.sort_8.clicked.connect(self.onBtnsort_8)
        self.mainView.sort_9.clicked.connect(self.onBtnsort_9)
        self.mainView.sort_10.clicked.connect(self.onBtnsort_10)
        self.mainView.foretime_sure_Button.clicked.connect(self.onBtnforetime)
        self.mainView.pb_load_alt_sure.clicked.connect(self.onBtnaltsure)
        self.mainView.uv_sure.clicked.connect(self.onBtnaltuv)


    def onBtnBrowseClicked(self): #浏览文件
        sources_info = QFileDialog.getOpenFileName(self, 'Choose File', "tianxian")[0]
        if len(sources_info) != 0:
            self.mainView.lineEdit_source_path.setText(sources_info)
            self.source_list = functions.get_pulsar_sche(sources_info)    #获取目标文件所有信息后放入列表

    def onBtnBrowseClicked_2(self): #浏览文件
        sources_info = QFileDialog.getOpenFileName(self, 'Choose File', "tianxian")[0]
        if len(sources_info) != 0:
            self.mainView.lineEdit_source_path_2.setText(sources_info)
            self.source_list_2 = functions.get_pulsar_sche(sources_info)    #获取目标文件所有信息后放入列表

    def onBtnimportClicked_1(self):
        global a
        global Lat
        global Lon
        a=1
        Lon = float(self.mainView.lineEdit_6.text())
        Lat = float(self.mainView.lineEdit_7.text())
        functions.dianji(a, Lat, Lon)
    def onBtnimportClicked_2(self):
        global a2
        global Lat
        global Lon
        a2=1
        Lon = float(self.mainView.lineEdit_10.text())
        Lat = float(self.mainView.lineEdit_11.text())
        functions.dianji(a2, Lat, Lon)
    def onBtnimportClicked_3(self):
        global a3
        global Lat
        global Lon
        a3=1
        Lon = float(self.mainView.lineEdit_14.text())
        Lat = float(self.mainView.lineEdit_15.text())
        functions.dianji(a3, Lat, Lon)
    def onBtnimportClicked_4(self):
        global a4
        global Lat
        global Lon
        a4=1
        Lon = float(self.mainView.lineEdit_22.text())
        Lat = float(self.mainView.lineEdit_23.text())
        functions.dianji(a4, Lat, Lon)
    def onBtnimportClicked_5(self):
        global a5
        global Lat
        global Lon
        a5=1
        Lon = float(self.mainView.lineEdit_26.text())
        Lat = float(self.mainView.lineEdit_27.text())
        functions.dianji(a5, Lat, Lon)
    def onBtnimportClicked_6(self):
        global a6
        global Lat
        global Lon
        a6=1
        Lon = float(self.mainView.lineEdit_30.text())
        Lat = float(self.mainView.lineEdit_31.text())
        functions.dianji(a6, Lat, Lon)
    def onBtnimportClicked_7(self):
        global a7
        global Lat
        global Lon
        a7=1
        Lon = float(self.mainView.lineEdit_34.text())
        Lat = float(self.mainView.lineEdit_35.text())
        functions.dianji(a7, Lat, Lon)
    def onBtnimportClicked_8(self):
        global a8
        global Lat
        global Lon
        a8=1
        Lon = float(self.mainView.lineEdit_38.text())
        Lat = float(self.mainView.lineEdit_39.text())
        functions.dianji(a8, Lat, Lon)
    def onBtnimportClicked_9(self):
        global a9
        global Lat
        global Lon
        a9=1
        Lon = float(self.mainView.lineEdit_42.text())
        Lat = float(self.mainView.lineEdit_43.text())
        functions.dianji(a9, Lat, Lon)
    def onBtnimportClicked_10(self):
        global a10
        global Lat
        global Lon
        a10=1
        Lon = float(self.mainView.lineEdit_46.text())
        Lat = float(self.mainView.lineEdit_47.text())
        functions.dianji(a10, Lat, Lon)

    def onBtntrackClicked_1(self):
        global b1,a
        global Lat
        global Lon
        if a==1:
            pass
        else:
            b1 = 1
            Lat = 26.44
            Lon = 106.1
            functions.dianji(b1, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_2(self):
        global b2,a2
        global Lat
        global Lon
        if a2==1:
            pass
        else:
            b2 = 1
            Lat = 26.44
            Lon = 106.2
            functions.dianji(b2, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_3(self):
        global b3,a3
        global Lat
        global Lon
        if a3==1:
            pass
        else:
            b3 = 1
            Lat = 26.44
            Lon = 106.3
            functions.dianji(b3, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_4(self):
        global b4,a4
        global Lat
        global Lon
        if a4==1:
            pass
        else:
            b4 = 1
            Lat = 26.44
            Lon = 106.4
            functions.dianji(b4, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_5(self):
        global b5,a5
        global Lat
        global Lon
        if a5==1:
            pass
        else:
            b5 = 1
            Lat = 26.44
            Lon = 106.5
            functions.dianji(b5, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_6(self):
        global b6,a6
        global Lat
        global Lon
        if a6==1:
            pass
        else:
            b6 = 1
            Lat = 26.44
            Lon = 106.6
            functions.dianji(b6, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_7(self):
        global b7,a7
        global Lat
        global Lon
        if a7==1:
            pass
        else:
            b7 = 1
            Lat = 26.44
            Lon = 106.7
            functions.dianji(b7, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_8(self):
        global b8,a8
        global Lat
        global Lon
        if a8==1:
            pass
        else:
            b8 = 1
            Lat = 26.44
            Lon = 106.8
            functions.dianji(b8, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_9(self):
        global b9,a9
        global Lat
        global Lon
        if a9==1:
            pass
        else:
            b9 = 1
            Lat = 26.44
            Lon = 106.9
            functions.dianji(b9, Lat, Lon)
        self.onBtnSubmitClicked()
    def onBtntrackClicked_10(self):
        global b10,a10
        global Lat
        global Lon
        if a10==1:
            pass
        else:
            b10 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b10, Lat, Lon)
        self.onBtnSubmitClicked()

    def onBtnstop_1(self):
        global a, b1
        a=0
        b1=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_6.setText(' ')
        self.mainView.lineEdit_7.setText(' ')
        self.mainView.lineEdit_8.setText(' ')
        self.mainView.lineEdit_9.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_2(self):
        global a2, b2
        a2=0
        b2=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_10.setText(' ')
        self.mainView.lineEdit_11.setText(' ')
        self.mainView.lineEdit_12.setText(' ')
        self.mainView.lineEdit_13.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_3(self):
        global a3, b3
        a3=0
        b3=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_14.setText(' ')
        self.mainView.lineEdit_15.setText(' ')
        self.mainView.lineEdit_16.setText(' ')
        self.mainView.lineEdit_17.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_4(self):
        global a4, b4
        a4=0
        b4=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_22.setText(' ')
        self.mainView.lineEdit_23.setText(' ')
        self.mainView.lineEdit_24.setText(' ')
        self.mainView.lineEdit_25.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_5(self):
        global a5, b5
        a5=0
        b5=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_26.setText(' ')
        self.mainView.lineEdit_27.setText(' ')
        self.mainView.lineEdit_28.setText(' ')
        self.mainView.lineEdit_29.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_6(self):
        global a6, b6
        a6=0
        b6=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_30.setText(' ')
        self.mainView.lineEdit_31.setText(' ')
        self.mainView.lineEdit_32.setText(' ')
        self.mainView.lineEdit_33.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_7(self):
        global a7, b7
        a7=0
        b7=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_34.setText(' ')
        self.mainView.lineEdit_35.setText(' ')
        self.mainView.lineEdit_36.setText(' ')
        self.mainView.lineEdit_37.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_8(self):
        global a8, b8
        a8=0
        b8=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_38.setText(' ')
        self.mainView.lineEdit_39.setText(' ')
        self.mainView.lineEdit_40.setText(' ')
        self.mainView.lineEdit_41.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_9(self):
        global a9, b9
        a9=0
        b9=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_42.setText(' ')
        self.mainView.lineEdit_43.setText(' ')
        self.mainView.lineEdit_44.setText(' ')
        self.mainView.lineEdit_45.setText(' ')
        self.mainView.lineEdit_now.setText(' ')
    def onBtnstop_10(self):
        global a10, b10
        a10=0
        b10=0
        functions.dianji(0, 0, 0)
        self.mainView.lineEdit_46.setText(' ')
        self.mainView.lineEdit_47.setText(' ')
        self.mainView.lineEdit_48.setText(' ')
        self.mainView.lineEdit_49.setText(' ')
        self.mainView.lineEdit_now.setText(' ')

    def onBtnsort_1(self):
        global b1,a
        global Lat
        global Lon
        if a==1:
            pass
        else:
            b1 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b1, Lat, Lon)
        self.mainView.lineEdit_8.setText(str(Lon))
        self.mainView.lineEdit_9.setText(str(Lat))
        self.mainView.lineEdit_now.setText('1')
        self.onBtnOptimizeClicked()
    def onBtnsort_2(self):
        global b2,a2
        global Lat
        global Lon
        if a==1:
            pass
        else:
            b2 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b2, Lat, Lon)
        self.mainView.lineEdit_12.setText(str(Lon))
        self.mainView.lineEdit_13.setText(str(Lat))
        self.mainView.lineEdit_now.setText('2')
        self.onBtnOptimizeClicked()
    def onBtnsort_3(self):
        global b3,a3
        global Lat
        global Lon
        if a3==1:
            pass
        else:
            b3 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b3, Lat, Lon)
        self.mainView.lineEdit_16.setText(str(Lon))
        self.mainView.lineEdit_17.setText(str(Lat))
        self.mainView.lineEdit_now.setText('3')
        self.onBtnOptimizeClicked()
    def onBtnsort_4(self):
        global b4,a4
        global Lat
        global Lon
        if a4==1:
            pass
        else:
            b4 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b4, Lat, Lon)
        self.mainView.lineEdit_24.setText(str(Lon))
        self.mainView.lineEdit_25.setText(str(Lat))
        self.mainView.lineEdit_now.setText('4')
        self.onBtnOptimizeClicked()
    def onBtnsort_5(self):
        global b5,a5
        global Lat
        global Lon
        if a5==1:
            pass
        else:
            b5 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b5, Lat, Lon)
        self.mainView.lineEdit_28.setText(str(Lon))
        self.mainView.lineEdit_29.setText(str(Lat))
        self.mainView.lineEdit_now.setText('5')
        self.onBtnOptimizeClicked()
    def onBtnsort_6(self):
        global b6,a6
        global Lat
        global Lon
        if a6==1:
            pass
        else:
            b6 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b6, Lat, Lon)
        self.mainView.lineEdit_32.setText(str(Lon))
        self.mainView.lineEdit_33.setText(str(Lat))
        self.mainView.lineEdit_now.setText('6')
        self.onBtnOptimizeClicked()
    def onBtnsort_7(self):
        global b7,a7
        global Lat
        global Lon
        if a7==1:
            pass
        else:
            b7 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b7, Lat, Lon)
        self.mainView.lineEdit_36.setText(str(Lon))
        self.mainView.lineEdit_37.setText(str(Lat))
        self.mainView.lineEdit_now.setText('7')
        self.onBtnOptimizeClicked()
    def onBtnsort_8(self):
        global b8,a8
        global Lat
        global Lon
        if a8==1:
            pass
        else:
            b8 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b8, Lat, Lon)
        self.mainView.lineEdit_40.setText(str(Lon))
        self.mainView.lineEdit_41.setText(str(Lat))
        self.mainView.lineEdit_now.setText('8')
        self.onBtnOptimizeClicked()
    def onBtnsort_9(self):
        global b9,a9
        global Lat
        global Lon
        if a9==1:
            pass
        else:
            b9 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b9, Lat, Lon)
        self.mainView.lineEdit_44.setText(str(Lon))
        self.mainView.lineEdit_45.setText(str(Lat))
        self.mainView.lineEdit_now.setText('9')
        self.onBtnOptimizeClicked()
    def onBtnsort_10(self):
        global b10,a10
        global Lat
        global Lon
        if a10==1:
            pass
        else:
            b10 = 1
            Lat = 26.44
            Lon = 106.10
            functions.dianji(b10, Lat, Lon)
        self.mainView.lineEdit_48.setText(str(Lon))
        self.mainView.lineEdit_49.setText(str(Lat))
        self.mainView.lineEdit_now.setText('10')
        self.onBtnOptimizeClicked()

    def onBtnaltsure(self):
        global alt_star
        alt_star =float(self.mainView.lineEdit_foretime_2.text())

    def onBtnforetime(self):
        global c
        c=1
        foretime=self.mainView.lineEdit_foretime.text()
        foretime1=Time(foretime)- 8 * u.hour
        functions.foretime(c, foretime1)

    def onBtnSubmitClicked_2(self):  # 提交数据，sche出现
        from datetime import datetime
        source_path_2 = self.mainView.lineEdit_source_path_2.text()
        if source_path_2 == '':
            print("Please specify source file")
            return
        sche = self.source_list_2[0]
        self.canvas_1.axes.cla()# 清除绘图
        for i in self.source_list_2:
            name = i[1]
            ra = i[2]
            dec = i[3]
            src_pos = " ".join([ra, dec])
            alt, az = functions.RaDec_AltAz(src_pos, duration=300)
            alt2 = "%.3f" % alt
            az2 = "%.3f" % az
            self.mainView.lineEdit_4.setText("  " + alt2)
            self.mainView.lineEdit_5.setText("  " + az2)
            observing_location = EarthLocation(lat=26.44 * u.deg, lon=106.67 * u.deg)  # 赤纬26
            observing_time = Time(datetime.utcnow(), scale='utc', location=observing_location)
            h = int(str(observing_time).split(' ')[1].split(':')[0])
            m = float(int(str(observing_time).split(' ')[1].split(':')[1]) / 60)
            s = float(float(str(observing_time).split(' ')[1].split(':')[2]) / 3600)
            time_now = h + m + s
            # self.canvas.axes.cla()
            trace_start_time = time.time()  # 返回当前时间的时间戳
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(trace_start_time))  # beijing time 时间格式
            alt_arr, ltime = self.get_path_alts_azs(src_pos, start_time, duration=86400)
            ltime_1 = []
            for i in ltime:
                h = int(str(i).split(' ')[1].split(':')[0])
                m = (int(str(i).split(' ')[1].split(':')[1]) / 60)
                s = (float(str(i).split(' ')[1].split(':')[2]) / 3600)
                ltime_1.append(h + m + s)
            functions.plot_trace(self.canvas_1.axes, alt_arr, ltime_1, name)
            functions.plot_target_pos(self.canvas_1.axes, alt, time_now)
            self.canvas_1.draw()
            # self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\dingbiao.eps", dpi=400)
            # self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\dingbiao.png", dpi=400)
            # self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\dingbiao.pdf", dpi=400)
            self.mainView.pushButton_browse_src_2.setEnabled(False)
            self.mainView.pb_load_sourceFile_submit_2.setEnabled(False)
            self.mainView.pb_load_sourceFile_cancel_2.setEnabled(True)


    def onBtnSubmitClicked(self): #提交数据，sche出现
        global a, a2, a3, a4, a5, a6, a7, a8, a9, a10, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10
        global Lat
        global Lon
        from datetime import datetime
        source_path = self.mainView.lineEdit_source_path.text()
        if source_path == '':
            print("Please specify source file")
            return
        sche = self.source_list[0]
        self.canvas.axes.cla()  # 清除绘图
        for i in self.source_list:
            name = i[1]
            ra = i[2]
            dec = i[3]
            src_pos = " ".join([ra, dec])
            alt, az = functions.RaDec_AltAz(src_pos, duration=300)
            alt2 = "%.3f" % alt
            az2 = "%.3f" % az
            self.mainView.lineEdit_4.setText("  " + alt2)
            self.mainView.lineEdit_5.setText("  " + az2)
            if a == 0:
                observing_location = EarthLocation(lat=26.44 * u.deg, lon=106.67 * u.deg)  # 赤纬26
                self.mainView.lineEdit_8.setText('106.67')
                self.mainView.lineEdit_9.setText('26.44')
                self.mainView.lineEdit_now.setText('1')
            if b1 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_8.setText(str(Lon))
                self.mainView.lineEdit_9.setText(str(Lat))
                self.mainView.lineEdit_now.setText('1')
            if b2 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_12.setText(str(Lon))
                self.mainView.lineEdit_13.setText(str(Lat))
                self.mainView.lineEdit_now.setText('2')
            if b3 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_16.setText(str(Lon))
                self.mainView.lineEdit_17.setText(str(Lat))
                self.mainView.lineEdit_now.setText('3')
            if b4 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_24.setText(str(Lon))
                self.mainView.lineEdit_25.setText(str(Lat))
                self.mainView.lineEdit_now.setText('4')
            if b5 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_28.setText(str(Lon))
                self.mainView.lineEdit_29.setText(str(Lat))
                self.mainView.lineEdit_now.setText('5')
            if b6 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_32.setText(str(Lon))
                self.mainView.lineEdit_33.setText(str(Lat))
                self.mainView.lineEdit_now.setText('6')
            if b7 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_36.setText(str(Lon))
                self.mainView.lineEdit_37.setText(str(Lat))
                self.mainView.lineEdit_now.setText('7')
            if b8 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_40.setText(str(Lon))
                self.mainView.lineEdit_41.setText(str(Lat))
                self.mainView.lineEdit_now.setText('8')
            if b9 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_44.setText(str(Lon))
                self.mainView.lineEdit_45.setText(str(Lat))
                self.mainView.lineEdit_now.setText('9')
            if b10 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_48.setText(str(Lon))
                self.mainView.lineEdit_49.setText(str(Lat))
                self.mainView.lineEdit_now.setText('10')

            if a == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_8.setText(str(Lon))
                self.mainView.lineEdit_9.setText(str(Lat))
                self.mainView.lineEdit_now.setText('1')
            if a2 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_12.setText(str(Lon))
                self.mainView.lineEdit_13.setText(str(Lat))
                self.mainView.lineEdit_now.setText('2')
            if a3 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_16.setText(str(Lon))
                self.mainView.lineEdit_17.setText(str(Lat))
                self.mainView.lineEdit_now.setText('3')
            if a4 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_24.setText(str(Lon))
                self.mainView.lineEdit_25.setText(str(Lat))
                self.mainView.lineEdit_now.setText('4')
            if a5 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_28.setText(str(Lon))
                self.mainView.lineEdit_29.setText(str(Lat))
                self.mainView.lineEdit_now.setText('5')
            if a6 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_32.setText(str(Lon))
                self.mainView.lineEdit_33.setText(str(Lat))
                self.mainView.lineEdit_now.setText('6')
            if a7 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_36.setText(str(Lon))
                self.mainView.lineEdit_37.setText(str(Lat))
                self.mainView.lineEdit_now.setText('7')
            if a8 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_40.setText(str(Lon))
                self.mainView.lineEdit_41.setText(str(Lat))
                self.mainView.lineEdit_now.setText('8')
            if a9 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_44.setText(str(Lon))
                self.mainView.lineEdit_45.setText(str(Lat))
                self.mainView.lineEdit_now.setText('9')
            if a10 == 1:
                observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)
                self.mainView.lineEdit_48.setText(str(Lon))
                self.mainView.lineEdit_49.setText(str(Lat))
                self.mainView.lineEdit_now.setText('10')
            observing_time = Time(datetime.utcnow(), scale='utc', location=observing_location)
            h = int(str(observing_time).split(' ')[1].split(':')[0])
            m = float(int(str(observing_time).split(' ')[1].split(':')[1]) / 60)
            s = float(float(str(observing_time).split(' ')[1].split(':')[2]) / 3600)
            time_now = h + m + s
           # self.canvas.axes.cla()
            trace_start_time = time.time()  # 返回当前时间的时间戳
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(trace_start_time))  # beijing time 时间格式
            alt_arr, ltime = self.get_path_alts_azs(src_pos, start_time, duration=86400)

            ltime_1 = []
            for i in ltime:
                h = int(str(i).split(' ')[1].split(':')[0])
                m = (int(str(i).split(' ')[1].split(':')[1]) / 60)
                s = (float(str(i).split(' ')[1].split(':')[2]) / 3600)
                ltime_1.append(h + m + s)
            # alt_arr_2=[]
            # for i in range (0,len(alt_arr)):
            #     alt_arr_2.append(alt_arr[i])
            #
            # for i in range(0, len(ltime_1)):
            #     if ltime_1[i] >= 23.95:
            #         # ltime_1 = ltime_1[i:1]+ltime_1[i+3:-1]
            #         ltime_1 = np.concatenate((ltime_1[2:i], ltime_1[i+3:-1]))
            #         alt_arr=[]
            #         alt_arr=np.concatenate((alt_arr_2[2:i], alt_arr_2[i+3:-1]))
            #         break
            #     else:
            #         pass


            functions.plot_trace(self.canvas.axes, alt_arr, ltime_1, name)

            # functions.plot_trace(self.canvas.axes, alt_arr, ltime_1, name)
            functions.plot_target_pos(self.canvas.axes, alt, time_now)
            self.canvas.draw()
            #self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\dingbiao.png",dpi=400)
            #self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\dingbiao.pdf",dpi=400)
        if sche is not None:
            #global countdown
           # countdown = int(sche[-1])
            self.mainView.lcd_remaining_time.display("86400")
            #self.showPulsarInfo(sche)
            self.mainView.pushButton_browse_src.setEnabled(False)
            self.mainView.pb_load_sourceFile_submit.setEnabled(False)
            self.mainView.pb_load_sourceFile_cancel.setEnabled(True)

    def time(self):
        localTimer = QTimer(self)
        localTimer.timeout.connect(self.onBtnSubmitClicked)
        localTimer.start(10000)

    def onBtnOptimizeClicked(self):
        from interval3 import Interval
        from interval3 import IntervalSet
        from datetime import datetime
        global alt_star
        sources_info = QFileDialog.getOpenFileName(self, 'Choose File', "tianxian")[0]
        if len(sources_info) != 0:
            self.goal_list = functions.get_pulsar_sche(sources_info)  # 获取目标文件所有信息后放入列表
            sche = self.goal_list[0]
            self.canvas.axes.cla()  # 清除绘图
            value_dict = dict()
        for i in self.goal_list:
            name = i[1]
            ra = i[2]
            dec = i[3]
            src_pos = " ".join([ra, dec])
            alt, az = functions.RaDec_AltAz(src_pos, duration=300)
            alt2 = "%.3f" % alt
            az2 = "%.3f" % az
            observing_location = EarthLocation(lat=26.44 * u.deg, lon=106.67 * u.deg)  # 赤纬26
            # trace_start_time = ('2022-07-23 19:32:20')
            start_time = self.mainView.lineEdit_foretime.text()  # 输入时间日期
            alt_arr, ltime = self.get_path_alts_azs(src_pos, start_time, duration=86400)
            observing_time = Time(start_time) - 8 * u.hour
            h = int(str(observing_time).split(' ')[1].split(':')[0])
            m = float(int(str(observing_time).split(' ')[1].split(':')[1]) / 60)
            s = float(float(str(observing_time).split(' ')[1].split(':')[2]) / 3600)
            time_now = (h + m + s)
            max1 = max(alt_arr)
            k = alt_star
            alt_arr1 = [x for x in alt_arr if x > k]
            while len(alt_arr1) == 0:
                k -= 1
                alt_arr1 = [x for x in alt_arr if x > k]
            min1 = min(alt_arr1)
            print(name)
            #print(max1)
            #print(min1)
            value = max1 - min1
            print(value)
            value_dict.update({name: value})
            value_dict_sorted = sorted(value_dict.items(), key=lambda x: x[1], reverse=False)
            value1 = []
            for m in range(len(value_dict_sorted)):
                value1.append(value_dict_sorted[m][0])
            if len(value1) == len(self.goal_list):
                name = []
                equal = []
                time_len = IntervalSet()
                for j in value1:
                    for i in range(len(self.goal_list)):
                        name.append(self.goal_list[i][1])
                    prio = self.goal_list[name.index(j)]
                    name_prio = prio[1]
                    ra_prio = prio[2]
                    dec_prio = prio[3]
                    time_ref = int(int(prio[-1]) / 86.4)  # source输入时间
                    print(name_prio)
                    src_pos_prio = " ".join([ra_prio, dec_prio])
                    alt_pos, az_pos = functions.RaDec_AltAz(src_pos_prio, duration=300)
                    alt_arr1, ltime = self.get_path_alts_azs(src_pos_prio, start_time, duration=86400)
                    equal = np.argwhere(alt_arr1 > alt_star)  # 将大于预设值的俯仰索引提取出
                    time_cut = 0
                    if time_len:
                        equal1 = equal * 86.4 / 3600
                        equal = []
                        for k in equal1:
                            time_self4 = float(k)
                            if time_self4 in time_len:
                                pass
                            else:
                                equal.append(time_self4 * 3600 / 86.4)
                        equal = np.array(equal)  # 横向数组转纵向双重数组
                    if len(equal):
                        time_cut = len(equal)  # 有效俯仰长度
                    if time_ref < time_cut:
                        if time_cut - time_ref > time_ref:
                            time_cut = int((time_cut - time_ref) / 2)
                            time_ref = time_cut + time_ref
                            equal = equal[time_cut:time_ref]

                        else:
                            time_cut = int(time_cut / 2)
                            time_star = int(time_cut - (time_ref / 2))
                            time_stop = int(time_cut + (time_ref / 2))
                            equal = equal[time_star:time_stop]
                    # print(equal)
                    time_self = equal * 86.4 / 3600
                    time_self2 = []
                    time_1 = []
                    time_3 = []
                    for l in time_self:
                        time_self1 = float(l)
                        if time_self1 in time_len:
                            pass
                        else:
                            time_1.append(time_self1)
                            time_3.append(round((time_self1 * 3600) / 86.4))
                            a = float("%.3f" % (time_self1 + time_now))
                            if a > 24:
                                b = float("%.3f" % (a - 24))
                                time_self2.append(b)
                            else:
                                time_self2.append(a)
                            max_time = float(max(time_1))
                            min_time = float(min(time_1))
                    alt_prio = (alt_arr1[time_3])
                    time_prio = (time_self2)
                    functions.plot_trace(self.canvas.axes, alt_prio, time_prio, name_prio)
                    # functions.plot_target_pos(self.canvas.axes, alt_pos, time_now)
                    self.canvas.draw()
                    self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\sort.png", dpi=400)
                    self.canvas.figure.savefig(r"C:\Users\Administrator\Desktop\论文图片9.6\sort.pdf", dpi=400)
                    if len(time_1):
                        MAX = max([time_1[i] - time_1[i - 1] for i in range(1, len(time_1))])
                        if MAX > 0.1:
                            for i in range(1, len(time_1)):
                                if time_1[i] - time_1[i - 1] == MAX:
                                    time_len.add(Interval(0, time_1[i - 1]))
                                    time_len.add(Interval(time_1[i], time_1[-1]))
                        else:
                            time_len.add(Interval(min_time, max_time))
                    print(time_len)

    def onBtnaltuv(self):  #uv
        self.canvas_2.axes.cla()
        uv.run_uv_basic(self.canvas_2.axes)
        self.canvas_2.draw()

    def onBtnCancelClicked(self):  #取消
        self.timer.stop()
        global countdown
        countdown = 0
        global current_shown_pulsar_index
        current_shown_pulsar_index = 0
        self.mainView.pushButton_browse_src.setEnabled(True)
        #self.mainView.pb_load_sourceFile_sure.setEnabled(True)
        self.mainView.pb_load_sourceFile_submit.setEnabled(True)
        self.mainView.pb_load_sourceFile_cancel.setEnabled(False)
        self.canvas.axes.cla()  #清除绘图
        #self.clearPulsarInfo() #调用显示函数
        self.mainView.lineEdit_source_path.clear()

    def onBtnCancelClicked_2(self):  # 取消
        self.mainView.pushButton_browse_src_2.setEnabled(True)
        self.mainView.pb_load_sourceFile_submit_2.setEnabled(True)
        self.mainView.pb_load_sourceFile_cancel_2.setEnabled(False)
        self.canvas_1.axes.cla()
        self.mainView.lineEdit_source_path_2.clear()

    def get_path_alts_azs(self, src_pos, observe_time, duration=None, overheadtime=None):
        global a, a2, a3, a4, a5, a6 , a7, a8, a9, a10, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10
        global Lon
        global Lat
        src_coord  = SkyCoord(src_pos, unit=(u.hour, u.deg), frame="icrs")
        if a == 0:
            site_loc = EarthLocation(lon=106.67, lat=26.44, height=1110.0288)
        if b1 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b2 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b3 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b4 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b5 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b6 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b7 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b8 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b9 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if b10 == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)

        if a == 1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a2==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a3==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a4==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a5==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a6==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a7 == 1:
                site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a8==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a9==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        if a10==1:
            site_loc = EarthLocation(lon=Lon, lat=Lat, height=1110.0288)
        #site_loc = EarthLocation(lon=106.67, lat=26.44, height=1110.0288)
        observe_time = Time(observe_time) - 8 * u.hour
        steps = np.linspace(0, duration, 1000) * u.second
        observe_time += steps   #观测时间段列表
        obs_frames = AltAz(location=site_loc, obstime=observe_time)
        obs_coord = src_coord.transform_to(obs_frames)
        #print(obs_coord.alt.deg,obs_coord.az.deg)
        return obs_coord.alt.deg, observe_time


    def init_telescope_status(self):  # 调用恒星时显示函数
        localTimer = QTimer(self)
        localTimer.timeout.connect(self.showCurrentTimeAndDate)
        localTimer.start(1000)

    def showCurrentTimeAndDate(self):  # 显示恒星时
        global c
        global a
        global Lon
        global Lat
        from astropy.coordinates import EarthLocation
        from astropy.time import Time
        from datetime import datetime
        from astropy import units as u
        if c==0:
            self.mainView.sort_1.setEnabled(False)
            self.mainView.sort_2.setEnabled(False)
            self.mainView.sort_3.setEnabled(False)
            self.mainView.sort_4.setEnabled(False)
            self.mainView.sort_5.setEnabled(False)
            self.mainView.sort_6.setEnabled(False)
            self.mainView.sort_7.setEnabled(False)
            self.mainView.sort_8.setEnabled(False)
            self.mainView.sort_9.setEnabled(False)
            self.mainView.sort_10.setEnabled(False)
        if c==1:
            self.mainView.sort_1.setEnabled(True)
            self.mainView.sort_2.setEnabled(True)
            self.mainView.sort_3.setEnabled(True)
            self.mainView.sort_4.setEnabled(True)
            self.mainView.sort_5.setEnabled(True)
            self.mainView.sort_6.setEnabled(True)
            self.mainView.sort_7.setEnabled(True)
            self.mainView.sort_8.setEnabled(True)
            self.mainView.sort_9.setEnabled(True)
            self.mainView.sort_10.setEnabled(True)
        qdate = QDate()
        current_date = qdate.currentDate().toString("yyyy-MM-dd")
        qtime = QTime()
        label_time = qtime.currentTime().toString("hh:mm:ss")
        #self.mainView.lineEdit_3.setText(current_date + ' ' + label_time)  # 显示北京时间
        if a==0:
            observing_location = EarthLocation(lat=26.44 * u.deg, lon=106.67 * u.deg)  # 赤纬26
        if a==1:
            observing_location = EarthLocation(lat=Lat * u.deg, lon=Lon * u.deg)  # 赤纬26
        observing_time = Time(datetime.utcnow(), scale='utc', location=observing_location)
        self.mainView.lineEdit_2.setText(str(observing_time)[:-7])  # 显示世界时间
        LST = observing_time.sidereal_time('mean')
        lst = str(LST).replace("h", ":").replace("m", ":").replace("s", " ")
        if lst[1] == ':':
            self.mainView.lineEdit_1.setText(current_date + ' ' + '0' + lst[:-7])  # 显示恒星时
        else:
            self.mainView.lineEdit_1.setText(current_date + ' ' + lst[:-6])  # 显示





