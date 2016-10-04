# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 12:15:35 2016

@author: David
"""

from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math
import os
from helperFiles import *
import seaborn as sns
from peak_Detect import peakdetect
#import lmPeakFit as lpf
import lmfit
path = "C:\\Users\\David\\Desktop\\MoS2_SlideA1\\Run004Map.txt"
def importRamanMap(pathToMapFile):
    rawdata = pd.read_csv(pathToMapFile, sep='\t',skiprows=1, names = ['X','Y','wavenumber','Intensity'])
    x = rawdata
    xu= x.X.unique()
    yu= x.Y.unique()
    runList=[]
    for i in xu:
        for ii in yu:
            runList.append(ramanScan(x[x.X==i][x.Y==ii].sort('wavenumber')))
            runList[-1].fitMoS2Peaks()
#            df = pd.DataFrame[\
#            ({'X':runList[-1].xpos, 'Y':runList[-1].ypos, 'H1':runList[-1].out.params['g1_height'],\
#            'fwhm1':runList[-1].out.params['g1_fwhm'],'l1':runList[-1].out.params['g1_center'],\
#            'H2':runList[-1].out.params['g2_height'],\
#            'fwhm2':runList[-1].out.params['g2_fwhm'],'l2':runList[-1].out.params['g2_center']\
#            })
    return runList, toDF(runList)
    
def toDF(classList):
    num=0
    for i in classList:
        idx = num
        if i.noFit:
            df = pd.DataFrame({'X':i.xpos, 'Y':i.ypos, 'H1':np.nan,\
            'fwhm1':np.nan,'l1':np.nan,\
            'H2':np.nan,\
            'fwhm2':np.nan,'l2':np.nan,\
            'split':np.nan},index=[idx])  
        else:
            df = pd.DataFrame({'X':i.xpos, 'Y':i.ypos, 'H1':i.out.params['g1_height'].value,\
            'fwhm1':i.out.params['g1_fwhm'].value,'l1':i.out.params['g1_center'].value,\
            'H2':i.out.params['g2_height'].value,\
            'fwhm2':i.out.params['g2_fwhm'].value,'l2':i.out.params['g2_center'].value,\
            'split':i.out.params['g2_center'].value-i.out.params['g1_center'].value},index=[idx])
        try:
            master = master.append(df)
        except:
            master = df
    num+=1
    return master
    
def plotHeatmaps(df):
#    data = data[((data.l2-data.l1)>15)]
#    data = data[((data.l2-data.l1)<30)]
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    print (data.l2-data.l1)
#    ax1.scatter(data.X,data.Y,c=data.l2-data.l1)
#    plt.colorbar(ax1)
    split = df.pivot(index = 'X', columns = 'Y', values = 'split')
    peak1 = df.pivot(index = 'X', columns = 'Y', values = 'l1')
    peak2 = df.pivot(index = 'X', columns = 'Y', values = 'l2')
    sns.heatmap(peak1, vmin = 380, vmax = 386)
    plt.title('e1')
    plt.show()
    sns.heatmap(peak2, vmin = 399, vmax = 410)
    plt.title('g1')
    plt.show()
    sns.heatmap(split, vmin = 15, vmax = 25)
    plt.title('delta')
    plt.show()
    

