# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:48:39 2017

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
import random

def predict_short(ori):
    """

    """
    m=len(ori) # m=5#用于预测的历史数据长度
    add=np.array([sum(ori[0:(i+1)]) for i in range(0,m)]) # 1 阶累加矢量
   
    B_1=-0.5*(add[0:m-1]+add[1:m])#计算B矩阵的第一个分量
    B_2=np.ones(m-1) # 计算B矩阵的第2个分量
    B=np.mat([B_1,B_2]).transpose() #生成B矩阵
    Y=np.mat(ori[1:m]).transpose()# 由0阶原始数据所得的Y矢量
    alpha=((B.T*B).I)*B.T*Y #计算微分方程的参数a,b
    
    a=alpha[0,0]
    b=alpha[1,0]
    
    F=-np.array([(-b/a+ori[0])*math.e**(a*(i+m-1))+b/a for i in range(0,6)])#根据微分方程得到预测数据的1阶累加值
    out=F[1:6]-F[0:5]#差分得到预测数据
    
    noise=0.20#判断是否为噪声的阈值
    last=np.mean(ori[m-5:m])
    
    for i in range(0,5):#本循环为低通滤波器
        if out[i]>(1+noise)*last or out[i]<(1-noise)*last:
            out[i]=last

    return out
    
def examine(old,new,thres):#检查预测质量的函数 threshold为判断胜率的阈值
    L=len(old)
    error=np.array([(new[i]/old[i]-1) for i in range(0,L)])#误差率
    error=abs(error)
    mean_error_rate=100*np.mean(error)#百分数误差率的均值
    std_error_rate=100*np.std(error)#百分数表示的误差率的标准差
    win_rate=100*sum(np.array([int(error[i]<thres) for i in range(0,L)]))/L#胜率
    
    out=np.array([mean_error_rate,std_error_rate,win_rate])#返回三个判断质量的参量
    return out
    