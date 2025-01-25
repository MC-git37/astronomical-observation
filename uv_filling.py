import math
import numpy as np
import matplotlib.pyplot as plt
c = 3e8 # speed of light (m/s)
# % system parameters
Nsat = 12 # number of satellites 卫星个数
Nss = np.array([1,60 ,3600 ,24*3600, 24*3600*30 ,24*3600*365]) # number of snapshots (resp.1s 1min 1d 1m 1y)1秒 1分.....1年 单位秒
Nf = 1000 # number of frequency bins (1 MHz bandwidth, 1 kHz channels) 带宽1MHz  1kHz 一个频段 1000个频点
f1 = 10e6 # sky frequency (MHz)
D = 100e3 # diameter satellite cloud (m) 直径
# derived numbers
lambda1 = c/f1 # sky wavelength (m) 波长
Nbl = 0.5*Nsat*(Nsat-1) # number of interferometers excluding autocorrelations
# projected area fraction
Aeff = int(lambda1**2/4) # effective area of a single dipole (m^2)
Acloud = int(math.pi *(D/2)**2)  # projected area of the cloud constellation (m^2)
eta_A = Nss * Nf * Aeff / Acloud # area filling fraction (this is what counts for imaging)
# volumetric fraction
Veff = (lambda1/2)**3 # antenna interferometer pair "volume" (m^3)
Vcloud = (4/3) * math.pi * (D/2)**3 # volume of satellite cloud (m^3)
eta_V = Nss * Nf * float(Veff/Vcloud) # volumetric filling fraction
plt.figure(1)
plt.plot(Nss,eta_A)
plt.title('area filling fraction')
plt.xscale('log')
plt.yscale('log')
plt.show()
#plot([60 60 60 60 60 60],eta_A);
plt.figure(2)
plt.plot(Nss,eta_V)
plt.title('volumetric filling fraction')
plt.xscale('log')
plt.yscale('log')
plt.show()