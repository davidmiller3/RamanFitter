# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 12:05:47 2016

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:12:09 2016

@author: David
"""
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math
import os
from lmfit.models import GaussianModel, LinearModel, LorentzianModel
import lmfit
from peak_Detect import peakdetect
def doubleGaussian(x,y,FWHM1, FWHM2, loc1,loc2,h1,h2):
    sig1=FWHM1/2.35
    sig2=FWHM2/2.35    
    amp1=h1*sig1*np.sqrt(2*np.pi)
    amp2=h2*sig2*np.sqrt(2*np.pi)
#Define a linear model and a Damped Oscillator Model    
    line_mod = LinearModel(prefix='line_')
    g1_mod = GaussianModel(prefix='g1_')
    g2_mod = GaussianModel(prefix='g2_')
#Initial Pars for Linear Model
    pars =  line_mod.make_params(intercept=0, slope=0)
    pars['line_intercept'].set(0, vary=True)
    pars['line_slope'].set(0, vary=True)
    pars.update(g1_mod.make_params())
    pars.update(g2_mod.make_params())
#Extend param list to use multiple peaks. Currently unused.
#Add fit parameters, Center, Amplitude, and Sigma
    pars['g1'+'_center'].set(loc1,min=375, max=390)
    pars['g1'+'_sigma'].set(sig1,min=2, max=25)
    pars['g1'+'_amplitude'].set(amp1)    
    pars['g2'+'_center'].set(loc2,min=400, max=415)
    pars['g2'+'_sigma'].set(sig2,min=2, max=25)
    pars['g2'+'_amplitude'].set(amp2)    
#Create full model. Add linear model and all peaks
    mod=line_mod+g1_mod+g2_mod
#Initialize fit
    init = mod.eval(pars, x=x)
#Do the fit. The weight exponential can weight the points porportional to the
#amplitude of y point. In this way, points on peak can be given more weight.     
    out=mod.fit(y, pars,x=x)
#Get the fit parameters
    fittedsigma1 = out.params['g1_sigma'].value
    fittedAmp1 = out.params['g1_amplitude'].value
    fittedCenter1 = out.params['g1_center'].value
    fittedsigma2 = out.params['g2_sigma'].value
    fittedAmp2 = out.params['g2_amplitude'].value
    fittedCenter2 = out.params['g2_center'].value
    fittedIntercept = out.params['line_intercept'].value
    fittedSlope = out.params['line_slope'].value
#Returns the output fit as well as an array of the fit parameters
    """Returns output fit as will as list of important fitting parameters"""
    return out, [fittedCenter1, fittedAmp1, fittedsigma1], [fittedCenter2, fittedAmp2, fittedsigma2]
    
def doubleLorentizan(x,y,FWHM1, FWHM2, loc1,loc2,h1,h2):
    sig1=FWHM1/2
    sig2=FWHM2/2
    amp1=h1*np.pi
    amp2=h2*np.pi
#Define a linear model and a Damped Oscillator Model    
    line_mod = LinearModel(prefix='line_')
    g1_mod = LorentzianModel(prefix='g1_')
    g2_mod = LorentzianModel(prefix='g2_')
#Initial Pars for Linear Model
    pars =  line_mod.make_params(intercept=0, slope=0)
    pars['line_intercept'].set(0, vary=True)
    pars['line_slope'].set(0, vary=True)
    pars.update(g1_mod.make_params())
    pars.update(g2_mod.make_params())
#Extend param list to use multiple peaks. Currently unused.
#Add fit parameters, Center, Amplitude, and Sigma
    pars['g1'+'_center'].set(loc1,min=375, max=390)
    pars['g1'+'_sigma'].set(sig1,min=2, max=25)
    pars['g1'+'_amplitude'].set(amp1)    
    pars['g2'+'_center'].set(loc2,min=400, max=415)
    pars['g2'+'_sigma'].set(sig2,min=2, max=25)
    pars['g2'+'_amplitude'].set(amp2)    
#Create full model. Add linear model and all peaks
    mod=line_mod+g1_mod+g2_mod
#Initialize fit
    init = mod.eval(pars, x=x)
#Do the fit. The weight exponential can weight the points porportional to the
#amplitude of y point. In this way, points on peak can be given more weight.     
    out=mod.fit(y, pars,x=x)
#Get the fit parameters
    fittedsigma1 = out.params['g1_sigma'].value
    fittedAmp1 = out.params['g1_amplitude'].value
    fittedCenter1 = out.params['g1_center'].value
    fittedsigma2 = out.params['g2_sigma'].value
    fittedAmp2 = out.params['g2_amplitude'].value
    fittedCenter2 = out.params['g2_center'].value
    fittedIntercept = out.params['line_intercept'].value
    fittedSlope = out.params['line_slope'].value
#Returns the output fit as well as an array of the fit parameters
    """Returns output fit as will as list of important fitting parameters"""
    return out, [fittedCenter1, fittedAmp1, fittedsigma1], [fittedCenter2, fittedAmp2, fittedsigma2]
    
    
        
    

class ramanScan():
    def __init__(self,pdarray):
#Path to data
        self.pdarray=pdarray
        self.xpos=pdarray.X.max()
        self.ypos=pdarray.Y.max()
        self.wnarray=pdarray.wavenumber
        self.iarray = pdarray.Intensity
    def fitMoS2PeaksG(self):
        low = 350
        high = 425
        smalldf = self.pdarray[self.pdarray.wavenumber<high][self.pdarray.wavenumber>low]
        try:
            if len(peakdetect(smalldf.Intensity, smalldf.wavenumber, lookahead = 2, delta=np.absolute(smalldf.Intensity.mean())*1.1)[0])==0:
                self.noFit = True
            else:
                self.out,self.g1,self.g2 = doubleGaussian(smalldf.wavenumber,smalldf.Intensity,20,20,385,402,0,0)
                self.noFit=False
        except:
            self.noFit = True

    def fitMoS2PeaksL(self):
        low = 350
        high = 425
        smalldf = self.pdarray[self.pdarray.wavenumber<high][self.pdarray.wavenumber>low]
        try:
            if len(peakdetect(smalldf.Intensity, smalldf.wavenumber, lookahead = 2, delta=np.absolute(smalldf.Intensity.mean())*1.1)[0])==0:
                self.noFit = True
                print 'no'
            else:
                self.out,self.g1,self.g2 = doubleLorentizan(smalldf.wavenumber,smalldf.Intensity,20,20,385,402,0,0)
                self.noFit=False
                print 'yes'
        except:
            self.noFit = True
            print 'no'
            

