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
path = "Z:\\Group\\Projects\\MoS2\\Raman Spectra\\Slide01\\MoS2_SlideA1\\Run004Map.txt"
path2 = "Z:\\Group\\Projects\\MoS2\\Raman Spectra\\DavidMiller\\MoS2_SlideA2\\map2.txt"
def importRamanMap(pathToMapFile, fitType='G'):
    rawdata = pd.read_csv(pathToMapFile, sep='\t',skiprows=1, names = ['X','Y','wavenumber','Intensity'])
    x = rawdata
    xu= x.X.unique()
    yu= x.Y.unique()
    runList=[]
    print rawdata.Intensity.min()
    num=0
    for i in xu:
        for ii in yu:
            print num
            runList.append(ramanScan(x[x.X==i][x.Y==ii].sort('wavenumber')))
            if fitType == 'L':
                runList[-1].fitMoS2PeaksL()
            else:
                runList[-1].fitMoS2PeaksG()
#            df = pd.DataFrame[\
#            ({'X':runList[-1].xpos, 'Y':runList[-1].ypos, 'H1':runList[-1].out.params['g1_height'],\
#            'fwhm1':runList[-1].out.params['g1_fwhm'],'l1':runList[-1].out.params['g1_center'],\
#            'H2':runList[-1].out.params['g2_height'],\
#            'fwhm2':runList[-1].out.params['g2_fwhm'],'l2':runList[-1].out.params['g2_center']\
#            })
            num+=1
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
    
def plotHeatmaps(df, layers):
    layerDict = {'1L':[384.7,402.8], '2L':[383.3,405.5], \
    '3L':[383.2,406.5],'4L':[382.9,407.4], 'Bulk':[383,408]}    
    
    p1 = layerDict[layers][0]
    p2 = layerDict[layers][1]
    d = p2-p1
    
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
    sns.heatmap(peak1, vmin = p1-4, vmax =p1+4,cmap = 'RdBu_r')
    plt.title('e1')
    plt.show()
    sns.heatmap(peak2, vmin = p2-4, vmax = p2+4,cmap = 'RdBu_r')
    plt.title('g1')
    plt.show()
    sns.heatmap(split, vmin = d-8, vmax = d+8,cmap = 'RdBu_r')
    plt.title('delta')
    plt.show()    
layerDict = {'1L':[384.7,402.8], '2L':[383.3,405.5], \
'3L':[383.2,406.5],'4L':[382.9,407.4], 'Bulk':[383,408]}

