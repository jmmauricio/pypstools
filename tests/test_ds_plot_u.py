# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))


import pypstools

ds = pypstools.digsilent_simulation
tools = pypstools.tools

geojson_file =  './osm_sing_simplified.json' 
subs = tools.geo2substations(geojson_file)

results_path =  'test_out.txt'
test_dict, type_list =  ds.ds_txt_col_2_dict(results_path)


import numpy as np
import matplotlib.pyplot as plt

fig_voltages = plt.figure(figsize=(10.0,10.0))

ax_u = fig_voltages.add_subplot(1,1,1)


t = test_dict['sys']['time']

for item in subs:
    if  test_dict['bus'].has_key(item):
        u = test_dict['bus'][unicode(item)]['fehz']['data']
        
        ax_u.plot(t,u, lw=2)



fig_voltages.show()
fig_voltages.savefig('powers.svg')
fig_voltages.savefig('powers.png')


