#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:07:58 2024

@author: reinierramos
"""

import numpy as np
import itertools as itools
from numpy import random as nrand
from .lcautils import updateGrid
from PIL import Image, ImageOps
from matplotlib import pyplot as plt

rng = nrand.default_rng(17)
LCAcmap = plt.get_cmap('magma')

def solveLCA(rate=4, duration=50, init='uniform', L=50, lattice='toroidal', 
             neighborhood='Moore', totalistic='outer', r=1, **kwargs):
    """
    Solves the spatiotemporal snapshots of a Logistic CA. If called
    without kwargs, then this uses uniform initial state distribution.
    See `init` for more information.

    Parameters
    ----------
    rate : float, default is 4
        Logistic growth rate.
        Must be between [0, 4].
    duration : int, default is 50
        Number of timesteps to solve Logistic CA.
        Must be nonzero.
    init : str, default is 'uniform'
        Random distribution to initialize LCA.
        Accepted values: 'uniform' and 'beta'.
        If 'beta', additional `kwargs must be provided, 
        either `(a=, b=)` or `(mu=, nu=)`.
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

    **kwargs : dict
        Additional arguments needed to specify shape parameters of beta 
        distribution. If mu and v  are specified, then the parameters
        and b are automatically computed.
        a: float, must be nonzero, a=mu*nu
        b: float, must be nonzero, b=(1-mu)*nu
        mu: float, mean, Must be in (0,1).
        nu: float, precision of the mean, 
                  "sample size" in Bayes theorem.

    Returns
    -------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of Logistic CA.

    """
    if init=='beta' and kwargs.get('a') and kwargs.get('b'):
        a, b = kwargs.get('a'), kwargs.get('b')
        grid = rng.beta(a, b, size=(L, L), dtype=np.float32)
    if init=='beta' and kwargs.get('mu') and kwargs.get('nu'):
        mu, nu = kwargs.get('mu'), kwargs.get('nu')
        a, b = mu*nu, (1-mu)*nu
        grid = rng.beta(a, b, size=(L, L), dtype=np.float32)
    if init=='uniform':
        grid = rng.random(size=(L,L), dtype=np.float32)
    grid_coords = list(itools.product(range(L), repeat=2))
    
    soln = np.zeros((duration+1, L,L), dtype=np.float32)
    soln[0,:,:] = grid
    
    propsCA = {
        'lat':lattice,      'tot':totalistic,
        'nei':neighborhood, 'radius':r,
        'L': L,             'rate':rate}
    
    for t in range(duration):
        grid = updateGrid(L, grid, grid_coords, propsCA)
        soln[t+1,:,:] = grid
    return soln

def animateLCA(soln, out='animLCA.gif'):
    """
    Saves the spatiotemporal dynamics of Logistic CA.

    Parameters
    ----------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of LCA.
    out : str, default is 'animLCA.gif'
        Output file name of the GIF.
        Must end with '.gif'
        
    """
    duration, L, _ = soln.shape
    resize = 200
    ims = [Image.fromarray(np.uint8(LCAcmap(soln[i,:,:])*255)) for i in range(duration)]
    ims = [im.convert('P', palette=Image.ADAPTIVE, colors=100) for im in ims]
    ims = [ImageOps.contain(im, (resize,resize)) for im in ims]
    ims[0].save(fp=out, format='gif', append_images=ims, save_all=True, 
                duration=duration, loop=0)
    
    
    