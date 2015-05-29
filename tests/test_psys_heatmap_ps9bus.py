# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))

import matplotlib.pyplot as plt
import pypstools
#import digsilent_simulation

result_dict = pypstools.digsilent_simulation.ds_2_dict('./ps9bus_results.txt')

pub = pypstools.publisher


test_data = {'tests_file':'./ps9bus_results.txt',
             'test_id':'test1',
             'element':'bus',
             'variable':'fehz',
             'resuts_file_type':'h_dict'}
             
             
geo_data = {'geojson_file':'./ps9bus2.json',
            'bottom_lat':42.5,  #  south dakota
            'top_lat':44.2,
            'left_lon':-107.8,
            'right_lon':-104.5,
            'draw_map':False,
            'mask_oceans':True}
            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'ps9bus'}
            
            
fig = plt.figure()

ax1 = plt.subplot2grid((1,1), (0,0))
      
time = 1.0
test_dict = result_dict
pub.psys_heatmap(test_data, geo_data, plot_data, time, test_dict, ax1)
m = pub.psys_map(geo_data, plot_data, ax1)

fig.show()