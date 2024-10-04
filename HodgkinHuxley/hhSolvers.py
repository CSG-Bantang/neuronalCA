#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:47:26 2024

@author: reinierramos
"""

import numpy as np
import hhODEs as HH
from scipy.integrate import odeint
from numpy import random as nrand
from matplotlib import pyplot as plt

rng = nrand.default_rng()

def lsoda(tList, Iparams):
    Vrest = 0
    guess = [Vrest,HH.m_inf(Vrest), HH.h_inf(Vrest), HH.n_inf(Vrest)]
    soln   = odeint(HH.odes, guess, tList, args=(Iparams,))
    return soln

def euler(tList, Iparams):
    dt      = tList[1]- tList[0]
    soln    = np.zeros([len(tList), 4])
    guess   = [0,HH.m_inf(), HH.h_inf(), HH.n_inf()]
    soln[0] = guess
    for _i in range(len(tList)-1):
        V, m, h, n = HH.odes(guess, tList[_i+1], Iparams)
        guess += np.array([V, m, h, n])*dt
        soln[_i+1] = guess
    return soln

def rk4(tList, Iparams): 
    dt      = tList[1]- tList[0]
    soln    = np.zeros([len(tList), 4])
    guess   = [0,HH.m_inf(), HH.h_inf(), HH.n_inf()]
    soln[0] = guess
    for _i in range(len(tList)-1):
        k1 = dt * HH.odes(guess,        tList[_i+1],        Iparams)
        k2 = dt * HH.odes(guess+0.5*k1, tList[_i+1]+0.5*dt, Iparams)
        k3 = dt * HH.odes(guess+0.5*k2, tList[_i+1]+0.5*dt, Iparams)
        k4 = dt * HH.odes(guess+k3,     tList[_i+1]+dt,     Iparams)
        guess += (k1 + 2*(k2+k3) + k4)/6
        soln[_i+1] = guess
    return soln



def eulerNoisy(tList, Iparams):
    dt      = tList[1]- tList[0]
    soln    = np.zeros([len(tList), 4])
    guess   = [-0.283, 0.051, 0.584, 0.321]
    soln[0] = guess
    if Iparams[-1]=='noisy':
        noise = rng.random(len(tList))
    print(np.mean(noise))
    for _i in range(len(tList)-1):
        Iparams[-2] = noise[_i]
        V, m, h, n = HH.odes(guess, tList[_i+1], Iparams)
        guess += np.array([V, m, h, n])*dt
        soln[_i+1] = guess
    return soln

def rk4Noisy(tList, Iparams): 
    dt      = tList[1]- tList[0]
    soln    = np.zeros([len(tList), 4])
    guess   = [-0.283, 0.051, 0.584, 0.321]
    soln[0] = guess
    if Iparams[-1]=='noisy':
        noise = rng.random(len(tList))
    for _i in range(len(tList)-1):
        Iparams[-2] = noise[_i]
        k1 = dt * HH.odes(guess,        tList[_i+1],        Iparams)
        k2 = dt * HH.odes(guess+0.5*k1, tList[_i+1]+0.5*dt, Iparams)
        k3 = dt * HH.odes(guess+0.5*k2, tList[_i+1]+0.5*dt, Iparams)
        k4 = dt * HH.odes(guess+k3,     tList[_i+1]+dt,     Iparams)
        guess += (k1 + 2*(k2+k3) + k4)/6
        soln[_i+1] = guess
    return soln



def eulerCoupled(tList, Iparams):
    dt      = tList[1]- tList[0]
    population = Iparams.get('r') * Iparams.get('c')
    soln    = np.zeros([population, len(tList), 4])
    guess   = [-0.283, 0.051, 0.584, 0.321]
    soln[:,0,:] = guess
    guess = soln[:,0,:]
    for _i in range(len(tList)-1):
        Vi = np.tile(soln[:,_i,0], (population,1))
        Vj = Vi.T
        Vij = Vi-Vj
        Iparams.update({'Vij':Vij})
        next_ = HH.odes(guess, tList[_i+1], Iparams).T
        guess += next_*dt
        soln[:,_i+1, :] = guess
    return soln

def rk4Coupled(tList, Iparams): 
    dt      = tList[1]- tList[0]
    soln    = np.zeros([len(tList), 4])
    guess   = [-0.283, 0.051, 0.584, 0.321]
    soln[0] = guess
    if Iparams[-1]=='coupled':
        noise = rng.random(len(tList))
    for _i in range(len(tList)-1):
        Iparams[-2] = noise[_i]
        k1 = dt * HH.odes(guess,        tList[_i+1],        Iparams)
        k2 = dt * HH.odes(guess+0.5*k1, tList[_i+1]+0.5*dt, Iparams)
        k3 = dt * HH.odes(guess+0.5*k2, tList[_i+1]+0.5*dt, Iparams)
        k4 = dt * HH.odes(guess+k3,     tList[_i+1]+dt,     Iparams)
        guess += (k1 + 2*(k2+k3) + k4)/6
        soln[_i+1] = guess
    return soln



