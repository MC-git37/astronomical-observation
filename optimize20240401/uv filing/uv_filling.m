% program fillng.m
% Albert-Jan Boonstra, ASTRON, 2014.11.05
% boonstra@astron.nl
%
% purpose: to estimate the (u,v,w) filling factor of a 3D cloud of interferometric satellites
% note: it is assumed that all (u,v,w) points are non-overlapping (not entirely true in general)
% note: the dipole effective area and "volume" are only coarse estimates
% note: calculations are done in ordinary space, not normalized with wavelengths
% physical constants
c = 3e8; % speed of light (m/s)
% system parameters
Nsat = 12; % number of satellites 卫星个数
Nss = [1 60 3600 24*3600 24*3600*30 24*3600*365]; % number of snapshots (resp.1s 1min 1d 1m 1y)1秒 1分.....1年 单位秒
Nf = 1000; % number of frequency bins (1 MHz bandwidth, 1 kHz channels) 带宽1MHz  1kHz 一个频段 1000个频点
f1 = 10e6; % sky frequency (MHz)
D = 100e3; % diameter satellite cloud (m) 直径
% derived numbers
lambda = c/f1; % sky wavelength (m) 波长
Nbl = 0.5*Nsat*(Nsat-1); % number of interferometers excluding autocorrelations
% projected area fraction
Aeff = lambda^2/4; % effective area of a single dipole (m^2)
Acloud = pi *(D/2)^2; % projected area of the cloud constellation (m^2)
eta_A = Nss * Nf * Aeff / Acloud; % area filling fraction (this is what counts for imaging)
% volumetric fraction
Veff = (lambda/2)^3; % antenna interferometer pair "volume" (m^3)
Vcloud = (4/3) * pi * (D/2)^3; % volume of satellite cloud (m^3)
eta_V = Nss * Nf * Veff/Vcloud; % volumetric filling fraction
figure(1);
plot(Nss,eta_A);
%hold on;
title('area filling fraction')
set(gca,'xscale','log')
set(gca,'yscale','log')

%plot([60 60 60 60 60 60],eta_A);

figure(2);
plot(Nss,eta_V);
title('volumetric filling fraction')
set(gca,'xscale','log')
set(gca,'yscale','log')