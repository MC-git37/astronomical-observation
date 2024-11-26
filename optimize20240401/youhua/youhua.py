import time
import traceback
import matplotlib  #画图
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
#from youhua import  #导入文件
from untitle import Ui_MainWindow
import datetime
countdown = 0
current_shown_pulsar_index = 0

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, autoscale_on=False)
        functions.polar_anno(self.axes)
        super(MplCanvas, self).__init__(self.fig)

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
        self.init_listeners()
        self.timerForCom.start()

    def initView(self):
        hboxlayout = QHBoxLayout()  # central part
        self.canvas = MplCanvas(self)
        hboxlayout.addWidget(self.canvas)
        self.mainView.widget_graphics.setLayout(hboxlayout)
        self.mainView.widget_graphics.show()
        self.mainView.lcd_remaining_time.setDigitCount(10)  # right pannel
        self.mainView.pushButton_cancel.setEnabled(False)

    def init_telescope_status(self):  #调用恒星时显示函数
        localTimer = QTimer(self)
        localTimer.timeout.connect(self.showCurrentTimeAndDate)
        localTimer.start(1000)

    def showCurrentTimeAndDate(self):  #显示恒星时
        from astropy.coordinates import EarthLocation
        from astropy.time import Time
        from datetime import datetime
        from astropy import units as u
        qdate = QDate()
        current_date = qdate.currentDate().toString("yyyy-MM-dd")
        qtime = QTime()
        label_time = qtime.currentTime().toString("hh:mm:ss")
       # self.mainView.lineEdit_17.setText(current_date + ' ' + label_time)    #显示北京时间
        observing_location = EarthLocation(lat=26.44 * u.deg, lon=106.67 * u.deg)  # 赤纬26
        observing_time = Time(datetime.utcnow(), scale='utc', location=observing_location)
        #self.mainView.lineEdit_16.setText(str(observing_time)[:-7])  # 显示世界时间
        LST = observing_time.sidereal_time('mean')
        lst=str(LST).replace("h", ":").replace("m", ":").replace("s", " ")
        print(lst)
        if lst[1]==':':
            self.mainView.lineEdit_1.setText(current_date + ' ' + '0'+lst[:-6])  # 显示恒星时
        else:
            self.mainView.lineEdit_1.setText(current_date + ' ' + lst[:-6])  # 显示
     #   self.communication() 调用的之后的其他函数
     #   self.con_azzlt_all()

    def init_listeners(self): #按钮调用
        self.mainView.pushButton_browse_src.clicked.connect(self.onBtnBrowseClicked)
        self.mainView.pb_load_sourceFile_submit.clicked.connect(self.onBtnSubmitClicked)
        self.mainView.pushButton_cancel.clicked.connect(self.onBtnCancelClicked)
        self.mainView.pushButton_run.clicked.connect(self.onBtnRunClicked)
        self.mainView.pb_load_sourceFile_order.clicked.connect(self.onBtnOrderClicked)
        self.timer.timeout.connect(self.updateRightPanelPulsarInfo)

    def onBtnBrowseClicked(self): #浏览文件
        sources_info = QFileDialog.getOpenFileName(self, 'Choose File', "youhua")[0]
        print(sources_info)
        if len(sources_info) != 0:
            self.mainView.lineEdit_source_path.setText(sources_info)
            self.source_list = functions.get_pulsar_sche(sources_info)
          #  self.mainView.pb_load_sourceFile_submit.setEnabled(False)
    #def onBtnOrderClicked(self): #排序
        Trans = list()
        Ulti = list()


    def onBtnSubmitClicked(self): #提交数据，sche出现
        source_path = self.mainView.lineEdit_source_path.text()
        print(source_path)
        if source_path == '':
            print("Please specify source file")
            return
        sche = self.source_list[0]
        if sche is not None:
            global countdown
            countdown = int(sche[-1])
            self.mainView.lcd_remaining_time.display(sche[-1])
            #self.showPulsarInfo(sche) 显示数据信息
            self.mainView.pushButton_browse_src.setEnabled(False)
            self.mainView.pb_load_sourceFile_submit.setEnabled(False)
            self.mainView.pushButton_cancel.setEnabled(True)
            #self.mainView.label_working_status.setText("Ready")


    def onBtnRunClicked(self): #确认
        if self.mainView.pb_load_sourceFile_submit.isEnabled():
            print("Please submit the source file you want to run!")
            return
        global countdown
        sche = self.source_list[0]
        duration_of_the_first_pulsar = sche[-1]
        countdown = int(duration_of_the_first_pulsar)
        self.mainView.pushButton_run.setEnabled(False)
        # self.mainView.label_observing_mode_left.setText("Overhead")
        self.timer.start()

    def onBtnCancelClicked(self):  #取消
        self.timer.stop()
        global countdown
        countdown = 0
        global current_shown_pulsar_index
        current_shown_pulsar_index = 0
        self.mainView.pushButton_run.setEnabled(True)
        self.mainView.pushButton_browse_src.setEnabled(True)
        self.mainView.pb_load_sourceFile_submit.setEnabled(True)
        self.mainView.pushButton_cancel.setEnabled(False)
        self.canvas.axes.cla()  #清除绘图
        #self.clearPulsarInfo()
        self.mainView.lineEdit_source_path.clear()

    def updateRightPanelPulsarInfo(self):  #将当前观测的恒星信息转化为方位俯仰？
        global countdown
        global current_shown_pulsar_index
        if countdown > 0:
            countdown -= 1
            self.mainView.lcd_remaining_time.display("{}".format(countdown))
            current_pulsar = self.source_list[current_shown_pulsar_index]  #当前卫星列表索引
            ra, dec = current_pulsar[2:4]
            src_pos = " ".join([ra, dec])
            duration = float(current_pulsar[-1])
            alt, az = functions.RaDec_AltAz(src_pos=src_pos, duration=duration)
            self.canvas.axes.cla()     #清除绘图
            trace_start_time = time.time()    #返回当前时间的时间戳
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(trace_start_time))  # beijing time 时间格式
            alt_arr, az_arr = self.get_path_alts_azs(src_pos, start_time, duration=duration)
            print(alt_arr)
            functions.plot_trace(self.canvas.axes, alt_arr)
            functions.plot_target_pos(self.canvas.axes, alt)
            self.canvas.draw()
            alt2 = "%.3f" % alt
            az2 = "%.3f" % az
            self.mainView.lineEdit_5.setText("  " + alt2)
            self.mainView.lineEdit_4.setText("  " + az2)
           # if alt > 0:
                #try:
                    #self.saveData()
                    #self.pulasrContral_all()  #控制天线转动
               # except Exception:
                    #print(traceback.format_exc())
        else:
            self.canvas.axes.cla()
            current_shown_pulsar_index += 1
            source_num = len(self.source_list)
            if current_shown_pulsar_index < source_num:
                the_next_source = self.source_list[current_shown_pulsar_index]
                #self.showPulsarInfo(the_next_source)
                countdown = int(the_next_source[-1])
                self.mainView.lcd_remaining_time.display("{}".format(countdown))
            else:
                print("Observing is over")
                self.canvas.axes.cla()
                self.timer.stop()
                self.clearPulsarInfo()
                self.mainView.pushButton_browse_src.setEnabled(True)
                self.mainView.pb_load_sourceFile_submit.setEnabled(True)
                self.mainView.pushButton_run.setEnabled(True)
                countdown = 0
                current_shown_pulsar_index = 0
    def get_path_alts_azs(self, src_pos, observe_time, duration=None, overheadtime=None):
        src_coord  = SkyCoord(src_pos, unit=(u.hour, u.deg), frame="icrs")
        site_loc = EarthLocation(lon=106.67, lat=26.44, height=1110.0288)
        observe_time = Time(observe_time) - 8 * u.hour
        steps = np.linspace(0, duration, 6400) * u.second
        observe_time += steps
        obs_frames = Alt(location=site_loc, obstime=observe_time)
        obs_coord = src_coord.transform_to(obs_frames)
        print(obs_coord.alt.deg,obs_coord.az.deg)
        return obs_coord.alt.deg, obs_coord.az.deg






