#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:34:43 2024

@author: reinierramos
"""

import numpy as np
from .caBoundary import getNeighbors


def updateGrid(L, grid, grid_coords, propsCA):
    """
    Updates the LCA grid applying logisticEquation.

    """
    rate = propsCA.get('rate')
    prev = grid.copy()
    for j,i in grid_coords:
        xin = np.mean(getNeighbors(propsCA, prev, j, i))
        grid[j,i] = logisticEquation(rate, xin)
    return grid

def logisticEquation(r=1.0, xt=0.5):    return r*xt*(1-xt)
