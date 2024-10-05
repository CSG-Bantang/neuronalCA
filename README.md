# Welcome to CSG-Bantang/neuronalCA

This an ongoing project highlighting systems involving:
1) Hodgkin-Huxley
2) Logistic Map
3) Game of Life
4) Brian's Brain
5) Neuronal Cellular Automata


## I. Hodgkin-Huxley (HH) Systems
The current version supports three ODE solvers:
1) LSODA
2) Forward Euler
3) Runge-Kutta 4th order. <br>

For the external stimulus, there are four sets of parameters which can be implemented in any combination, except when using LSODA<sup>a </sup>.
1) Constant Input: &emsp;&ensp; $ I_{ext} = I_0 $
2) Sinusoidal Input: &emsp; $ I_{ext} = I_s~\sin(2\pi~f_st) $
3) Noisy Input: &emsp;&emsp;&emsp; $ I_{ext} = I_n~\eta(t) $
4) Coupling Input: &emsp;&ensp; $ I_{ext} = \sum\limits_{j} I_{ij} $, where $ I_{ij} = -g~a_{ij}~(V_i-V_j)$ <br>
*<sup>a </sup> LSODA is incompatible with noisy and coupled systems.*

### A) Single HH Systems	