import time
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
import threading
b =0
Lat1 = 0
Lon1=0
mode=0
class telescope_state:
    def __init__(self, offline=True, online=False, ready=False, overhead=False):
        # telescope running state
        self.offline = offline
        self.online = online
        self.ready = ready
        self.overhead = overhead
        self.show_trace = True
        self.running = threading.Event()
    def __repr__(self):
        return "offline={0} overhead={1} ready={2} online={3}".format(self.offline, self.overhead, self.ready,
                                                                      self.online)
    def reset(self):
        self.offline = False
        self.online = False
        self.ready = False
        self.overhead = False
    # def pause(self):
    #    self.threadflag.clear()
    # def resume(self):
    #    self.threadflag.set()
    def stop(self):
        self.reset()
        self.ready = True
        self.running.clear()
def update_telescope_state(window, op_state):
    if op_state.offline:
        window["-stat-"].update("OFFLINE")
    elif op_state.online:
        window["-stat-"].update("ONLINE")
    elif op_state.ready:
        window["-stat-"].update("Ready")
    elif op_state.overhead:
        window["-stat-"].update("Overhead")
    else:
        window["-stat-"].update("ERROR")
def draw_fig(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg
def dianji(a, Lat, Lon):
    global b
    global Lon1
    global Lat1
    b = a
    Lat1 = Lat
    Lon1 = Lon

def foretime(c,time):
    global mode
    global observetime
    mode =c
    observetime=time

def RaDec_AltAz(src_pos: object, obstime: object = None, duration: object = None, overheadtime: object = None) -> object:
    src_coord = SkyCoord(src_pos, unit=(u.hour, u.deg), frame="icrs")
    global b
    global Lon1
    global Lat1
    global mode ,observetime
    # dawodang
    # site_loc = EarthLocation(lon=106.630, lat=26.380, height=1110.0288)
    # beijing
    if b == 0:
        site_loc = EarthLocation(lon=106.67, lat=26.44, height=1110.0288)
    if b == 1:
        site_loc = EarthLocation(lon=Lon1, lat=Lat1, height=1110.0288)  # 赤纬26
    #print(Lon1)
    if obstime is None:
        curtime = time.strftime("%Y-%m-%d %H:%M:%S")  # beijing time
        #print(curtime)
        curtime = Time(curtime) - 8 * u.hour  # UTC time
    elif duration is not None:
        curtime = obstime
        curtime = Time(curtime) - 8 * u.hour
        steps = np.linspace(0, duration, 6) * u.second
        curtime += steps
    elif overheadtime is not None:
        curtime = obstime
        curtime = Time(curtime) - 8 * u.hour
        curtime += overheadtime * u.second
    if mode==0:
        obs_frames = AltAz(location=site_loc, obstime=curtime)
    if mode ==1:
        obs_frames = AltAz(location=site_loc, obstime=observetime)
    #print('obs_coord = src_coord.transform_to(obs_frames)',obs_frames)
    obs_coord = src_coord.transform_to(obs_frames)
    return obs_coord.alt.deg, obs_coord.az.deg
def text_anno(ax, theta, r, text):
    theta *= np.pi / 180
    ax.text(theta, r, text)
def polar_anno(ax):
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.pyplot import MultipleLocator
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文
    ax.set_ylim(15, 90)
    ax.set_xlim(0, 24)
    x_major_locator = MultipleLocator(1)#间隔
    ax.xaxis.set_major_locator(x_major_locator)#把x轴的主刻度设置为1的倍数
    y_major_locator = MultipleLocator(5)  # 间隔
    ax.yaxis.set_major_locator(y_major_locator)  # 把y轴的主刻度设置为1的倍数
    # ax.set(xlabel='UTtime(h)', ylabel='alt(deg)')
    ax.set_xlabel('UT time(h)', fontsize=24)  # 标题字体
    ax.set_ylabel('Alt(deg)', fontsize=24)  # 标题字体
    ax.tick_params(axis='x', labelsize=18)  # 设置x轴刻度字体大小为12
    ax.tick_params(axis='y', labelsize=18)  # 设置y轴刻度字体大小为12
    ax.grid(linestyle=":", color="b")
    # plt.show()      #其影响uv的弹窗 ？

def plot_target_pos(ax, alt,time):
    polar_anno(ax)
    ax.plot([time], [alt], "ro", markersize=6)

def plot_trace(ax, alt, time, name):
    polar_anno(ax)
    # ax.plot(time, alt, ls="--", marker=".", lw=0.1, label=name)#label='crab',color="b"
    #ax.plot(time, alt, ls=None, marker='o', lw=0.1, label=name)
    ax.scatter(time, alt, marker='o', label=name)
    # ax.legend(bbox_to_anchor=(1.0000005, 1.0), loc='upper left', fontsize=11)  # 显示上标（图例）并固定位置
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), fontsize=15)
    ax.figure.tight_layout()    #调整窗口适应上标



def sun_moon(ax):
    ax.text(0.22 * np.pi, -40, "  Sun   ——", color='c', fontsize="x-large", ha="center", va="center")
    ax.text(0.24 * np.pi, -35, "Moon ——", color='y', fontsize="x-large", ha="center", va="center")

def get_pulsar_sche(filename):
    pulsar_sche = []
    with open(filename) as fp:
        lines = fp.readlines()
        for idx, line in enumerate(lines):
            if "SOURCE-TABLE" not in line:
                continue
            for sche in lines[idx + 5:]:
                if sche.strip() == "":
                    continue
                pulsar_sche.append(sche.strip().split())
            break
    return pulsar_sche
def update_pulsar_sche(window, sche, sche_idx, tot_sche, elastic_time=None, init=False):
    src_name = sche[1]
    src_ra, src_dec = sche[2:4]
    src_dm = sche[4]
    pol = sche[5]
    mode, ncha, nbin = sche[6:9]
    band = sche[9]
    length = sche[-1]
    # print("22", window)
    # print(sche_idx, tot_sche)
    window["-pulsar-state-"].update("{0} / {1}".format(sche_idx, tot_sche))
    window["-pulsar-src-"].update("{}".format(src_name))
    window["-pulsar-ra-"].update("{}".format(src_ra))
    window["-pulsar-dec-"].update("{}".format(src_dec))
    window["-pulsar-dm-"].update("{}".format(src_dm))
    # window["-pulsar-TR-"].update("{}".format(src_tr))
    window["-pulsar-pol-"].update("{}".format(pol))
    window["-pulsar-mode-"].update("{}".format(mode))
    window["-pulsar-band-"].update("{}".format(band))
    window["-pulsar-ncha-"].update("{}".format(ncha))
    window["-pulsar-nbin-"].update("{}".format(nbin))
    if init == True:
        window["-pulsar-left-time-"].update("{0} / {1} seconds".format("ready", length))
        window["-mode-"].update("Pulsar {}".format(mode))
        return
    window["-pulsar-left-time-"].update("{0:.1f} / {1} seconds".format(elastic_time, length))
def pulsar_observing_func(window, button_time, pulsar_sche, op_state, overhead_time=20):
    button_time_str = np.copy(button_time)
    button_time = time.mktime(time.strptime(button_time, "%Y-%m-%d %H:%M:%S"))
    tot_sche = len(pulsar_sche)
    cur_sche_time = 0
    for idx, sche in enumerate(pulsar_sche):
        # update to next source position
        update_pulsar_sche(window, sche, idx + 1, tot_sche, init=True)
        ra = window["-pulsar-ra-"].get()
        dec = window["-pulsar-dec-"].get()
        src_pos = " ".join([ra, dec])
        # the target position
        cur_sche_time += overhead_time
        alt, az = RaDec_AltAz(src_pos, obstime=button_time_str, overheadtime=cur_sche_time)
        window["-alt-"].update("{:.3f}".format(alt))
        window["-az-"].update("{:.3f}".format(az))
        # overhead time
        op_state.reset()
        op_state.overhead = True
        op_state.show_trace = True
        time.sleep(overhead_time)
        if not op_state.running.isSet():
            # cancled
            window.write_event_value("-CAN-PULSAR-", "")
            break
        # on source time
        cur_sche_time += float(sche[-1])
        op_state.reset()
        op_state.online = True
        while time.time() - button_time < cur_sche_time:
            if not op_state.running.isSet():
                # cancled
                window.write_event_value("-CAN-PULSAR-", "")
                break
            time.sleep(0.8)
            elastic_time = cur_sche_time + button_time - time.time()
            update_pulsar_sche(window, sche, idx + 1, tot_sche, elastic_time=elastic_time)
            ra = window["-pulsar-ra-"].get()
            dec = window["-pulsar-dec-"].get()
            src_pos = " ".join([ra, dec])
            alt, az = RaDec_AltAz(src_pos)
            window["-alt-"].update("{:.3f}".format(alt))
            window["-az-"].update("{:.3f}".format(az))
    if op_state.running.isSet():
        # finished
        op_state.reset()
        op_state.ready = True
        window.write_event_value("-END-PULSAR-", "")
def pulsar_observing(window, button_time, pulsar_sche, op_state):
    threading.Thread(target=pulsar_observing_func,
                     args=(window, button_time, pulsar_sche, op_state),
                     daemon=True).start()
