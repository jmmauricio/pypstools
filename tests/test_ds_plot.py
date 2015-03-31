# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
sys.path.insert(0,os.path.abspath(__file__+"/../pypstools"))


import pypstools

ds = pypstools.digsilent_simulation

results_path =  'test_out.txt'
test_dict, type_list =  ds.ds_txt_col_2_dict(results_path)


import numpy as np
import matplotlib.pyplot as plt

fig_powers = plt.figure(figsize=(10.0,10.0))

ax_p = fig_powers.add_subplot(2,1,1)
ax_q = fig_powers.add_subplot(2,1,2)

t = test_dict['sys']['time']

for item in test_dict['sys']['syms']:
    p = test_dict['sym'][item]['P1']['data']
    q = test_dict['sym'][item]['Q1']['data']
    
    ax_p.plot(t,p, lw=2)
    ax_q.plot(t,q, lw=2)


fig_powers.show()
fig_powers.savefig('powers.svg')
fig_powers.savefig('powers.png')


