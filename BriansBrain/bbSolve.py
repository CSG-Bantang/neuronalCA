#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:28:56 2024

@author: reinierramos
"""

import numpy as np
import itertools as itools
from .bbutils import updateGrid
from numpy import random as nrand
from PIL import Image, ImageOps
from matplotlib import colors as mplc

rng = nrand.default_rng(17)
QFRcmap = mplc.ListedColormap(['black','khaki', 'rebeccapurple'], N=3)

def solveBB(L=50, lattice='toroidal',
            neighborhood='Moore', totalistic='outer', r=1,
            duration=30, tRefrac=1,
            Lambda=2, firingRule='=',
            dq=1/3, df=1/3):
    """
    Solves the spatiotemporal snapshots of a Brian's Brain (BB) CA. If called
    without kwargs, then this returns the original Brian's brain dynamics.

    Parameters
    ----------
    L : int, default is 50
        Lattice size for the BB CA.
        Must be greater than 0.
    lattice : str, default is 'toroidal'
        Lattice boundary condition.
        Accepted values: 'toroidal', 'spherical'.
    neighborhood : str, default is 'Moore'
        Neighborhood boundary condition.
        Accepted values: 'Moore', 'vonNeumann'.
    totalistic : str, default is 'outer'
        Neighborhood rule condition.
        Accepted values: 'inner', 'outer'.
    r : int, default is 1
        Radius of neighborhood.
        Currently not implemented, will be ignored if provided.
    duration : int, default is 30
        Number of timesteps to solve BB CA.
        Must be nonzero.
    tRefrac : int, default is 1
        Refractory period. 
        Number of timesteps that a neuron will stay "R".
    Lambda : int, default is 2
        Firing threshold.
        See `firingRule` for the interpretation.
    firingRule : str, default is '='
        Firing condition that sets inequality for `Lambda`.
        Interpreted as: "Q"->"F" if num_neighbors("Q") = Lambda.
        Accepted values: '=', '>=', '<=', '>', '<'.
    dq : float, default is 1/3
        Initial density of "Q" cells in the CA.
        Must be between [0,1].
        Note: total must be dq+df+dr=1.
    df : float, default is 1/3
        Initial density of "F" cells in the CA.
        Must be between [0,1].
        Note: total must be dq+df+dr=1.

    Returns
    -------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of BB CA.

    """
    dr = 1 - (dq+df)
    
    grid = rng.choice([0,1,2], size=(L,L), p=(dq,df,dr))
    grid_coords = list(itools.product(range(L), repeat=2))
    
    gridRefrac = np.zeros((L,L))
    gridRefrac[grid==2] = 1
    
    soln = np.zeros((duration+1, L,L))
    soln[0,:,:] = grid
    
    propsCA = {
        'lat':lattice,           'tot':totalistic,
        'nei':neighborhood,      'radius':r,
        'lambda':Lambda,         'firingRule': firingRule,
        'timeRefrac':tRefrac,    'L': L,
        'gridRefrac':gridRefrac}
    for t in range(duration):
        grid = updateGrid(L, grid, grid_coords, propsCA)
        gridRefrac[grid==2] += 1
        gridRefrac[grid==0] = 0
        gridRefrac[grid==1] = 0
        propsCA.update({'gridRefrac':gridRefrac})
        soln[t+1,:,:] = grid
    return soln

def animateBB(soln, out='animBB.gif'):
    """
    Saves the spatiotemporal dynamics of BB CA.

    Parameters
    ----------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of BB CA.
    out : str, default is 'animBB.gif'
        Output file name of the GIF.
        Must end with '.gif'
        
    """
    duration, L, _ = soln.shape
    resize = 200
    ims = [Image.fromarray(np.uint8(QFRcmap(soln[i,:,:]/2)*255)) for i in range(duration)]
    ims = [im.convert('P', palette=Image.ADAPTIVE, colors=3) for im in ims]
    ims = [ImageOps.contain(im, (resize,resize)) for im in ims]
    ims[0].save(fp=out, format='gif', append_images=ims, save_all=True, 
                duration=duration, loop=0)
    
