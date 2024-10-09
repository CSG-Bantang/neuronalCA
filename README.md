# Welcome to CSG-Bantang/neuronalCA

This an ongoing project highlighting systems involving:
1) Hodgkin-Huxley
2) Logistic Map
3) Game of Life
4) Brian's Brain
5) Neuronal Cellular Automata
6) Morris-Lecar
7) Wilson-Cowan
8) EEG Analysis
9) fMRI Analysis

For more information on the usage for each system, please refer to the [wiki page](https://github.com/CSG-Bantang/neuronalCA/wiki).

## I. Hodgkin-Huxley (HH) Systems
These systems involve solving coupled ordinary differential equations (ODEs) to describe the action potential across the neuronal membrane [[1]](#1). Solvers available are LSODA, forward Euler, and Runge-Kutta 4th order. To start, import the package using  `import HodgkinHuxley as HH`. Allowed systems are single HH, noisy HH, coupled HH, and noisy coupled HH.

For the external stimulus, there are four sets of parameters which can be implemented in any combination, except when using LSODA. *LSODA is incompatible with noisy and coupled systems.*
1) Constant Input: &emsp;&emsp; $I_{1} = I_0$
2) Sinusoidal Input [[2]](#2): $I_{2} = I_s~\sin(2\pi~f_s t)$
3) Noisy Input [[3]](#3): &emsp;&emsp; $I_{3} = I_n~\eta(t)$, where $\eta(t)\in[-0.5,0.5]$, $\langle \eta \rangle_t = 0$
4) Coupling Input [[3]](#3): &ensp; $I_{4} = \sum_{j} I_{ij}$, where $I_{ij} = -g a_{ij} (V_i-V_j)$

More comprehensive guide [here](https://github.com/CSG-Bantang/neuronalCA/wiki/Hodgkin‐Huxley-(HH)-Systems).

## II. Logistic Map (LM) Systems and Logistic Cellular Automata
These systems involve solving logistic equation given by $x_{t+1} = r x_{t} (1-x_{t})$, where
$r$ is the growth rate and $x_{t}$ is the state of the LM system at time $t$  [[4]](#4). To start, import the package using `import LogisticMap as LM`. 

The package solves the steady-state $x(t)$ and the input-output or return map $x_{t+1}$ vs $x_{t}$.

Additionally, the package solves the snapshots of the spatiotemporal dynamics of a Logistic CA where $x_{t}$ is the average $x$ of the neighboring cells. The initial state distribution can be uniform random or beta [[5]](#5) distribution.

More comprehensive guide [here](https://github.com/CSG-Bantang/neuronalCA/wiki/Logistic-Map-(LM)-Systems).

## III. Game of Life (GOL) Cellular Automata (CA)
These systems involve solving for the snapshots of the spatiotemporal dynamics of a Game of Life CA  [[6,7]](#6). To start, import the package using `import GameOfLife as GOL`. 

The `system` specifies the initial state of the system. <br>
Random initial state: 0 <br>
Still-lifes: 1 to 5 <br>
Oscillators: 6 to 10 <br>
Creepers: 11 to 14 <br>
Methuselahs: 15 to 17 <br>
To view and save the animation as GIF, use `GOL.animateGOL(soln, out='anim.gif')`.

More comprehensive guide [here](https://github.com/CSG-Bantang/neuronalCA/wiki/Game-of-Life-(GOL)-Cellular-Automata-(CA)).

## IV. Brian's Brain (BB) Cellular Automata (CA)
These systems involve solving for the snapshots of the spatiotemporal dynamics of a Brian's Brain CA [[8,9]](#8) and its extensions [[10,11]](#10). To start, import the package using `import BriansBrain as BB`. 

The dynamics of the original Brian's Brain can be analyzed by changing the lattice size, duration, and the initial state density `dq` and `df`. <br>
This package extends the dynamics by changing lattice and neighborhood boundary conditions, firing condition and/or refractory condition.

More comprehensive guide [here](https://github.com/CSG-Bantang/neuronalCA/wiki/Brian's-Brain-(BB)-Cellular-Automata-(CA)).

## References:

1. <a name="1"></a>Hodgkin, Alan L., and Andrew F. Huxley. "A quantitative description of membrane current and its application to conduction and excitation in nerve." The Journal of physiology 117.4 (1952): 500.
2. <a name="2"></a>Escosio, Rey Audie S., and Johnrob Y. Bantang. "Frequency response analysis of a Hodgkin-Huxley neuron in a generalized current density stimulus." Proceedings of the Samahang Pisika ng Pilipinas (2016).
3. <a name="3"></a>Pang, James Christopher S., Christopher P. Monterola, and Johnrob Y. Bantang. "Noise-induced synchronization in a lattice Hodgkin–Huxley neural network." Physica A: Statistical Mechanics and its Applications 393 (2014): 638-645.
4. <a name="4"></a>Tsuchiya, Takashi and Yamagishi, Daisuke. "The Complete Bifurcation Diagram for the Logistic Map" Zeitschrift für Naturforschung A, vol. 52, no. 6-7, 1997, pp. 513-516. https://doi.org/10.1515/zna-1997-6-708.
5. <a name="5"></a>“Beta Distribution.” Wikipedia, Wikimedia Foundation, 19 June 2024, en.wikipedia.org/wiki/Beta_distribution. 
6. <a name="6"></a>Gardner, Martin. "Mathematical games-The fantastic combinations of John Conway’s new solitaire game, Life, 1970." _Scientific American, October_: 120-123.
7. <a name="7"></a>“Conway’s Game of Life.” _Wikipedia_, Wikimedia Foundation, 16 Sept. 2024, en.wikipedia.org/wiki/Conway%27s_Game_of_Life.
8. <a name="8"></a>Resnick, Mitchel; Silverman, Brian (1996-02-04). "Exploring Emergence: The Brain Rules". Exploring Emergence. MIT Media Laboratory, Lifelong Kindergarten Group. Retrieved 2008-12-15.
9. <a name="9"></a>Hawick, K. A., and C. J. Scogings. "Cycles, transients, and complexity in the game of death spatial automaton." Proc. International Conference on Scientific Computing (CSC’11). CSREA, 2011.
10. <a name="10"></a>Ramos, Reinier Xander A., Jacqueline C. Dominguez, and Johnrob Y. Bantang. "Young and Aged Neuronal Tissue Dynamics With a Simplified Neuronal Patch Cellular Automata Model." Frontiers in Neuroinformatics 15 (2022): 763560.
11. <a name="11"></a>RXA Ramos and JY Bantang, Steady-state spiking behaviors of neuronal patch model based on an extension of Brian’s brain cellular automata, Proceedings of the Samahang Pisika ng Pilipinas 42, SPP-2024-2B-01 (2024). URL: https://proceedings.spp-online.org/article/view/SPP-2024-2B-01.