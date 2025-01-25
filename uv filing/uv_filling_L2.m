% program uv_filling_L2.m
% Lao Baoqiang, SHAO, 2014.12.18
% lbq@shao.ac.cn
%
% purpose: to estimate the (u,v) filling factor of a 2D cloud of interferometric satellites
% note: it is not assumed that all (u,v,w) points are non-overlapping (not entirely true in general)
% note: the dipole effective area and "volume" are only coarse estimates
% 
% physical constants
clear all;
file0='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_u.dat';  %u\v\w data ·��
file1='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_v.dat';  %u\v\w data ·��
file2='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_w.dat';  %u\v\w data ·��

file3='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_oneweek_u.dat';  %u\v\w data ·��
file4='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_oneweek_v.dat';  %u\v\w data ·��
file5='D:\�Ϻ�����\UV filling\uv filing ����\uvwdata_oneweek_w.dat';  %u\v\w data ·��
%%------------------------------------------------------------------------------------------------
%��ȡuvw����
fid0=fopen(file0);
u_data=textscan(fid0,'%f'); 
u=u_data{1};   

fid1=fopen(file1);
v_data=textscan(fid1,'%f'); 
v=v_data{1}; 

fid2=fopen(file2);
w_data=textscan(fid2,'%f'); 
w=w_data{1}; 

fid3=fopen(file3);
u_oneweek_data=textscan(fid3,'%f'); 
u_oneweek=u_oneweek_data{1};   

fid4=fopen(file4);
v_oneweek_data=textscan(fid4,'%f'); 
v_oneweek=v_oneweek_data{1}; 

fid5=fopen(file5);
w_oneweek_data=textscan(fid5,'%f'); 
w_oneweek=w_oneweek_data{1}; 
%%------------------------------------------------------------------------------------------------
%���uv����С����
minline=50;
minline_oneweek=50;
len_uvw=length(u);        %���uvw���ݳ���
len_uvw_oneweek=length(u_oneweek);        %���uvw���ݳ���
for mm=1:len_uvw 
    for nn=mm+1:len_uvw 
        if u(mm)~=u(nn) && v(mm)~=v(nn)
            line_r=sqrt((u(mm)-u(nn))^2+(v(mm)-v(nn))^2);  
            if line_r<=minline
                minline=line_r;
            end
        end
    end
end

for mm=1:len_uvw_oneweek 
    for nn=mm+1:len_uvw_oneweek 
        if u_oneweek(mm)~=u_oneweek(nn) && v_oneweek(mm)~=v_oneweek(nn)
            line_r_oneweek=sqrt((u_oneweek(mm)-u_oneweek(nn))^2+(v_oneweek(mm)-v_oneweek(nn))^2);  
            if line_r_oneweek<=minline_oneweek
                minline_oneweek=line_r_oneweek;
            end
        end
    end
end
%%-----------------------------------------------------------------------------------------------
%���uv���ֵ����Сֵ
umax=max(u(:));
vmax=max(v(:));
umin=min(u(:));
vmin=min(v(:));

umax_oneweek=max(u(:));
vmax_oneweek=max(v(:));
umin_oneweek=min(u(:));
vmin_oneweek=min(v(:));
%%-----------------------------------------------------------------------------------------------
%�������
area_total=(umax-umin)*(vmax-vmin);

area_total_oneweek=(umax_oneweek-umin_oneweek)*(vmax_oneweek-vmin_oneweek);
%%-----------------------------------------------------------------------------------------------
%���uv��Ч���
uv_number=len_uvw;
unit_area=minline^2;
uv_area=uv_number*unit_area;

uv_number_oneweek=len_uvw_oneweek;
unit_area_oneweek=minline_oneweek^2;
uv_area_oneweek=uv_number_oneweek*unit_area_oneweek;
%%----------------------------------------------------------------------------------------------
%���uv filling fator
uv_area_f=uv_area/area_total;

uv_area_f_oneweek=uv_area_oneweek/area_total_oneweek;

                                                                              
                                               
                                             