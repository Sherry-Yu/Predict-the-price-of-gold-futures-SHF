# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:50:22 2017

@author: john
"""

import xlrd
import numpy as np
import datetime,time
import matplotlib.pyplot as plt
import pandas as pd
import plotly.plotly as py
import plotly.tools as tls
import math
from predict_short import predict_short,examine
import random
#import axes

data=xlrd.open_workbook('AU1705.SHF.xlsx')# 读入数据
table=data.sheets()[0]#第一列为时间

nrows=table.nrows
ncols=table.ncols

Date=table.col_values(0,1,nrows)  # 日期
Ave_price=table.col_values(9,1,nrows) #均价

dateoffset = 693594 # 导入的Excel中的时间基准是与1900年1月1日的天数差，加一个偏置值转换为与1年1月1日的天数差，便于转化为时间的数据类型
Ave_price=np.array(Ave_price)
Date_index=np.array(Date)+dateoffset
Date_index=Date_index.astype(int)

x=np.array([datetime.date.fromordinal(Date_index[i]) for i in range(0,nrows-1)])#时间索引
y=Ave_price#均价

window=[5,5,5,5,5]# 用于预测未来5天均价的历史数据长度
start=50 #预测结果的起始日期
end=nrows-10 #预测结果的截止日期
thres=np.array([0.08,0.08,0.08,0.08,0.08])#判断胜率的阈值
p_1=np.array([predict_short(y[i:i+window[0]])[0] for i in range(start-window[0],end-window[0])])
p_2=np.array([predict_short(y[i:i+window[1]])[1] for i in range(start-window[1],end-window[1])])
p_3=np.array([predict_short(y[i:i+window[2]])[2] for i in range(start-window[2],end-window[2])])
p_4=np.array([predict_short(y[i:i+window[3]])[3] for i in range(start-window[3],end-window[3])])
p_5=np.array([predict_short(y[i:i+window[4]])[4] for i in range(start-window[4],end-window[4])])
#以上分别为利用历史数据对未来第x天的均价数据进行预测
print(examine(y[start:end],p_1,thres[0]))
print(examine(y[start:end],p_2,thres[1]))
print(examine(y[start:end],p_3,thres[2]))
print(examine(y[start:end],p_4,thres[3]))
print(examine(y[start:end],p_5,thres[4]))
#分别打印对未来第X天预测的质量判断结果:胜率
plt.plot(x[start:end],y[start:end])
plt.plot(x[start:end],p_5) #画出预测价格与真实价格的图。
# plt.plot(x[start:end],p_2)