# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:41:49 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import numpy as np
from pypstools.tools import raw2pandas

sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..','pypstools')))

import publisher
import rst_tools
import digsilent_simulation

result_dict = digsilent_simulation.ds_2_dict('./ps9bus_results.txt')

import matplotlib.pyplot as plt


fig_omegas = plt.figure()

fig_omegas.set_size_inches(10.0,10.0)

ax_omegas = fig_omegas.add_subplot(1,1,1)

t = result_dict['sys']['time']

gens = ['G1','G2','G3']

it_g=1.0
omega_avg = np.copy(result_dict['sym'][gens[0]]['speed']['data'])
for gen in gens[1:]:
    it_g += 1.0
    omega_avg += result_dict['sym'][gen]['speed']['data'] 
omega_avg = omega_avg/it_g

for gen in gens:
    omega = result_dict['sym'][gen]['speed']['data']
    ax_omegas.plot(t,omega-omega_avg)

plt.show()