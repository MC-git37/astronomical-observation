import numpy as np
import matplotlib.pyplot as plt
file0 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_1hour_u.dat"  # u\v\w data 路径
file1 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_1hour_v.dat"  # u\v\w data 路径
file2 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_2hour_u.dat"  # u\v\w data 路径
file3 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_2hour_v.dat"  # u\v\w data 路径
file4 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_4hour_u.dat"  # u\v\w data 路径
file5 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_4hour_v.dat"  # u\v\w data 路径
file6 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_8hour_u.dat"  # u\v\w data 路径
file7 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_8hour_v.dat"  # u\v\w data 路径
file8 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_12hour_u.dat"  # u\v\w data 路径
file9 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_12hour_v.dat"  # u\v\w data 路径
file10 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_24hour_u.dat"  # u\v\w data 路径
file11 = r"C:\Users\Administrator\Desktop\uv filing 代码\uvdata_24hour_v.dat"  # u\v\w data 路径
# 读取uvw数据
u_data = np.loadtxt(file0, skiprows=1)
u = u_data
v_data = np.loadtxt(file1, skiprows=1)
v = v_data
u_oneweek_data = np.loadtxt(file2, skiprows=1)
u_oneweek = u_oneweek_data
v_oneweek_data = np.loadtxt(file3, skiprows=1)
v_oneweek = v_oneweek_data

u_onemonth_data = np.loadtxt(file4, skiprows=1)
u_onemonth = u_onemonth_data
v_onemonth_data = np.loadtxt(file5, skiprows=1)
v_onemonth = v_onemonth_data

u_halfyear_data = np.loadtxt(file6, skiprows=1)
u_halfyear = u_halfyear_data
v_halfyear_data = np.loadtxt(file7, skiprows=1)
v_halfyear = v_halfyear_data

u_12hour_data = np.loadtxt(file8, skiprows=1)
u_12hour = u_12hour_data
v_12hour_data = np.loadtxt(file9, skiprows=1)
v_12hour = v_12hour_data

u_24hour_data = np.loadtxt(file10, skiprows=1)
u_24hour = u_24hour_data
v_24hour_data = np.loadtxt(file11, skiprows=1)
v_24hour = v_24hour_data
# np.savetxt(r"C:\Users\Administrator\Desktop\uv filing 代码\test.dat",v_data,fmt='%.07f')
# 求出uv点最小距离
minline = 50
minline_oneweek = 50
minline_onemonth = 50
minline_halfyear = 50
minline_12hour = 50
minline_24hour = 50
print('开始')
len_uvw = len(u)  # 求解uvw数据长度
len_uvw_oneweek = len(u_oneweek)  # 求解uvw数据长度
len_uvw_onemonth = len(u_onemonth)
len_uvw_halfyear = len(u_halfyear)
len_uvw_12hour = len(u_12hour)
len_uvw_24hour = len(u_24hour)
for mm in range(len_uvw):
    for nn in range(mm + 1, len_uvw):
        if u[mm] != u[nn] and v[mm] != v[nn]:
            line_r = np.sqrt((u[mm] - u[nn]) ** 2 + (v[mm] - v[nn]) ** 2)
            if line_r <= minline:
                minline = line_r
print(1)
for mm in range(len_uvw_oneweek):
    for nn in range(mm + 1, len_uvw_oneweek):
        if u_oneweek[mm] != u_oneweek[nn] and v_oneweek[mm] != v_oneweek[nn]:
            line_r_oneweek = np.sqrt((u_oneweek[mm] - u_oneweek[nn]) ** 2 + (v_oneweek[mm] - v_oneweek[nn]) ** 2)
            if line_r_oneweek <= minline_oneweek:
                minline_oneweek = line_r_oneweek
print(2)
for mm in range(len_uvw_onemonth):
    for nn in range(mm + 1, len_uvw_onemonth):
        if u_onemonth[mm] != u_onemonth[nn] and v_onemonth[mm] != v_onemonth[nn]:
            line_r_onemonth = np.sqrt((u_onemonth[mm] - u_onemonth[nn]) ** 2 + (v_onemonth[mm] - v_onemonth[nn]) ** 2)
            if line_r_onemonth<= minline_onemonth:
                minline_onemonth = line_r_onemonth
print(4)
for mm in range(len_uvw_halfyear):
    for nn in range(mm + 1, len_uvw_halfyear):
        if u_halfyear[mm] != u_halfyear[nn] and v_halfyear[mm] != v_halfyear[nn]:
            line_r_halfyear = np.sqrt((u_halfyear[mm] - u_halfyear[nn]) ** 2 + (v_halfyear[mm] - v_halfyear[nn]) ** 2)
            if line_r_halfyear <= minline_halfyear:
                minline_halfyear = line_r_halfyear
print(8)
for mm in range(len_uvw_12hour):
    for nn in range(mm + 1, len_uvw_12hour):
        if u_12hour[mm] != u_12hour[nn] and v_12hour[mm] != v_12hour[nn]:
            line_r_12hour = np.sqrt((u_12hour[mm] - u_12hour[nn]) ** 2 + (v_12hour[mm] - v_12hour[nn]) ** 2)
            if line_r_12hour <= minline_12hour:
                minline_12hour = line_r_12hour
print(12)
for mm in range(len_uvw_24hour):
    for nn in range(mm + 1, len_uvw_24hour):
        if u_24hour[mm] != u_24hour[nn] and v_24hour[mm] != v_24hour[nn]:
            line_r_24hour = np.sqrt((u_24hour[mm] - u_24hour[nn]) ** 2 + (v_24hour[mm] - v_24hour[nn]) ** 2)
            if line_r_24hour <= minline_24hour:
                minline_24hour = line_r_24hour
print(24)

# 求解uv最大值、最小值
umax = np.max(u)
vmax = np.max(v)
umin = np.min(u)
vmin = np.min(v)

umax_oneweek = np.max(u_oneweek)
vmax_oneweek = np.max(v_oneweek)
umin_oneweek = np.min(u_oneweek)
vmin_oneweek = np.min(v_oneweek)

umax_onemonth = np.max(u_onemonth)
vmax_onemonth = np.max(v_onemonth)
umin_onemonth = np.min(u_onemonth)
vmin_onemonth = np.min(v_onemonth)

umax_halfyear = np.max(u_halfyear)
vmax_halfyear = np.max(v_halfyear)
umin_halfyear = np.min(u_halfyear)
vmin_halfyear = np.min(v_halfyear)

umax_12hour = np.max(u_12hour)
vmax_12hour = np.max(v_12hour)
umin_12hour = np.min(u_12hour)
vmin_12hour = np.min(v_12hour)

umax_24hour = np.max(u_24hour)
vmax_24hour = np.max(v_24hour)
umin_24hour = np.min(u_24hour)
vmin_24hour = np.min(v_24hour)
# 求总面积
area_total = (umax - umin) * (vmax - vmin)
area_total_oneweek = (umax_oneweek - umin_oneweek) * (vmax_oneweek - vmin_oneweek)
area_total_onemonth = (umax_onemonth - umin_onemonth) * (vmax_onemonth - vmin_onemonth)
area_total_halfyear = (umax_halfyear - umin_halfyear) * (vmax_halfyear - vmin_halfyear)
area_total_12hour = (umax_12hour - umin_12hour) * (vmax_12hour - vmin_12hour)
area_total_24hour = (umax_24hour - umin_24hour) * (vmax_24hour - vmin_24hour)
# 求解uv有效面积
uv_number = len_uvw
unit_area = minline ** 2
uv_area = uv_number * unit_area

uv_number_oneweek = len_uvw_oneweek
unit_area_oneweek = minline_oneweek *minline_oneweek
uv_area_oneweek = uv_number_oneweek * unit_area_oneweek

uv_number_onemonth = len_uvw_onemonth
unit_area_onemonth = minline_onemonth *minline_onemonth
uv_area_onemonth = uv_number_onemonth * unit_area_onemonth

uv_number_halfyear = len_uvw_halfyear
unit_area_halfyear = minline_halfyear *minline_halfyear
uv_area_halfyear = uv_number_halfyear * unit_area_halfyear

uv_number_12hour = len_uvw_12hour
unit_area_12hour = minline_12hour *minline_12hour
uv_area_12hour = uv_number_12hour * unit_area_12hour

uv_number_24hour = len_uvw_24hour
unit_area_24hour = minline_24hour *minline_24hour
uv_area_24hour = uv_number_24hour * unit_area_24hour
# 求解uv filling factor
uv_area_f = uv_area / area_total
uv_area_f_oneweek = float(uv_area_oneweek / area_total_oneweek)
uv_area_f_onemonth = float(uv_area_onemonth / area_total_onemonth)
uv_area_f_halfyear = float(uv_area_halfyear / area_total_halfyear)
uv_area_f_12hour = float(uv_area_12hour / area_total_12hour)
uv_area_f_24hour = float(uv_area_24hour / area_total_24hour)
print(uv_area_f)
print(uv_area_f_oneweek)
print(uv_area_f_onemonth)
print(uv_area_f_halfyear)
print(uv_area_f_12hour)
print(uv_area_f_24hour)
plt.figure(dpi=200)
plt.plot([1,2,4,8,12,24],[uv_area_f,uv_area_f_oneweek,uv_area_f_onemonth,uv_area_f_halfyear,uv_area_f_12hour,uv_area_f_24hour],marker='o')
plt.title('spatial filling&repeating factor')
plt.xlabel('time/day')
plt.ylabel('factor')
plt.show()