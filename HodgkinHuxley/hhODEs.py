#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:00:27 2024

@author: reinierramos
"""

import numpy as np

C   =    1
GNa =  120
GK  =   36
Glk =    0.3
ENa =  115
EK  = - 12
Elk =   10.6

def odes(vars_, t, params_):
    V, m, h, n = vars_.T
    channelNa = GNa * (ENa-V) * np.power(m,3) * h 
    channelK  = GK  * (EK -V) * np.power(n,4)
    channellk = Glk * (Elk-V)
    # if params_[-1]=='single':
    #     I = Isingle(t, *params_[:-1].astype(float))
    # if params_[-1]=='noisy':
    #     I = Inoisy(t, *params_[:-1].astype(float))
    if params_.get('type')=='coupled':
        I = Icoupled(t, params_)

    dVdt = (channelNa + channelK + channellk + I)/C
    dmdt = alpham(V)*(1-m) - betam(V)*m
    dhdt = alphah(V)*(1-h) - betah(V)*h
    dndt = alphan(V)*(1-n) - betan(V)*n
    return np.array([dVdt, dmdt, dhdt, dndt])

def alphan(V_): return 0.01*(10-V_) / (np.exp((10-V_)/10)-1)
def alpham(V_): return 0.1*(25-V_) / (np.exp((25-V_)/10)-1) 
def alphah(V_): return 0.07*np.exp(-V_/20)
def betah(V_):  return 1 / (np.exp((30-V_)/10)+1)
def betam(V_):  return 4*np.exp(-V_/18)
def betan(V_):  return 0.125*np.exp(-V_/80)

def n_inf(V_=0.0):  return alphan(V_) / (alphan(V_) + betan(V_))
def m_inf(V_=0.0):  return alpham(V_) / (alpham(V_) + betam(V_))
def h_inf(V_=0.0):  return alphah(V_) / (alphah(V_) + betah(V_))

def Isingle(t, Iconst = 10, pulseAmp = 0, pulseFreq = 0):
    pulseFreq /= 1000
    return Iconst + pulseAmp*np.sin(2*np.pi*pulseFreq*t)

def Inoisy(t, Iconst = 10, pulseAmp = 0, pulseFreq = 0
         , noiseAmp=0, noise=0):
    pulseFreq /= 1000
    return Iconst + pulseAmp*np.sin(2*np.pi*pulseFreq*t) + noiseAmp*(noise - 0.5)

def Icoupled(t, params_):
    Iconst = params_.get('Iconst')
    pulseAmp, pulseFreq = params_.get('pulseAmp'), params_.get('pulseFreq')
    # noiseAmp, noise = params_.get('noiseAmp'), params_.get('noise')
    g, aij, Vij = params_.get('couplStr'), params_.get('adjMat'), params_.get('Vij')
    # print(-g*aij*Vij)
    Iij = np.sum(-g*aij*Vij, axis=0)
    Isine  = pulseAmp*np.sin(2*np.pi*(pulseFreq/1000)*t)
    # Inoise = noiseAmp*(noise - 0.5)
    Iij[0] += Iconst + Isine ##+ Inoise
    return Iij
