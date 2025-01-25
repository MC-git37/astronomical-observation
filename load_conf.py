# -*- coding:utf-8 -*-
"""
@functions: list all the parameters for testing
@author: Zhen ZHAO
@date: May 23, 2018
"""
import pickle
# velocity of light
light_speed = 299792458.8
# Earth radius [km]
earth_radius = 6378.1363
# Earth flattening
earth_flattening = 1 / 298.257
# square of ellipsoid eccentricity
eccentricity_square = earth_flattening * (2 - earth_flattening)
# GM constant # GM=3.986004418*1e14 #地球（包括大气）引力常数 单位为m^3/s^-2 折合3.986004418*1e5
GM = 3.986004418 * 1e5 # [km^3/s^-2]
###########################################
# 1. 观测时间的设置
###########################################
# 起始时间全局变量
StartTimeGlobalYear = 2019
StartTimeGlobalMonth = 1
StartTimeGlobalDay = 20
StartTimeGlobalHour = 0
StartTimeGlobalMinute = 0
StartTimeGlobalSecond = 0
# 结束时间全局变量
StopTimeGlobalYear = 2019
StopTimeGlobalMonth = 1
StopTimeGlobalDay = 20
StopTimeGlobalHour = 10
StopTimeGlobalMinute = 0
StopTimeGlobalSecond = 0
# 时间步长
TimeStepGlobalDay = 0
TimeStepGlobalHour = 0
TimeStepGlobalMinute = 5
TimeStepGlobalSecond = 0
###########################################
# 2. 观测参数的设置
###########################################
# 三种基线类型的选择标志
baseline_flag_gg = 1
baseline_flag_gs = 0
baseline_flag_ss = 0
# baseline_type = baseline_flag_gg | baseline_flag_gs | baseline_flag_ss
baseline_type = baseline_flag_gg + baseline_flag_gs * 2 + baseline_flag_ss * 4
# 001(1)->select GtoG 010(2)->SELECT GtoS, 100(4)->StoS
# 观测频率和带宽
obs_freq = 22e9
bandwidth = 3.2e7
# 单位选择标志 km or lambda
unit_flag = 'km'
# cutoff_mode=1 #截止模式选择
cutoff_mode = {'flag': 1, 'CutAngle': 10} # 截止模式选择，flag:0->取数据库中设置的水平角，1->取界面上设置的水平角 2->取大者，3->取小者
precession_mode = 0 # 进动模型选择，0->Two-Body,1->J2
###########################################
# 3. 源，观测站，卫星的信息
###########################################
# 源信息
pos_mat_src = [['0316+413', '3h19m48.160s', '41d30m42.10s'],
['0202+319', '2h5m4.925s', '32d12m30.095s']]
#
# pos_mat_src = [['0316+413