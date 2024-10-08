#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:30:11 2024

@author: reinierramos
"""

import numpy as np
from .caBoundary import getNeighbors

STATES = 3
Q,F,R = range(STATES)

lambdaFunc = {'=':np.equal, '>': np.greater, '>=':np.greater_equal,
              '<':np.less, '<=':np.less_equal}

def updateGrid(L, grid, grid_coords, propsCA):
    """
    Updates the BB grid applying bbRules.

    """
    firingRule = lambdaFunc.get(propsCA.get('firingRule'))
    timeRefrac = propsCA.get('timeRefrac')
    gridRefrac = propsCA.get('gridRefrac')
    prev = grid.copy()
    for j,i in grid_coords:
        cell = prev[j,i]
        neighbors = getNeighbors(propsCA, prev, j, i)
        firingNeighbors = np.sum(neighbors, where=(neighbors==1))
        firingCondition = firingRule(firingNeighbors, propsCA.get('lambda'))
        refracCondition = (gridRefrac[j,i]<timeRefrac)
        grid[j,i] = bbRules(cell, firingCondition, refracCondition)
    return grid

def bbRules(cell, firingCondition, refracCondition):
    """
    BB Transition Rules:
        if cell=F,                           cell->R
        if cell=R and refracCondition=False, cell->Q
        if cell=Q and firingCondition=True,  cell->F
        if cell=R and refracCondition=True,  cell stays R 
    Refractory condition is given by `tRefrac`.
    Firing condition is given by `firingRule` and `Lambda`.

    """
    return R*(cell==F) + Q*(not refracCondition)*(cell==R) + F*firingCondition*(cell==Q) + \
           R*refracCondition*(cell==R)