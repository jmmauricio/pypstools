# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import numpy as np
from pypstools.tools import raw2pandas
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..','pypstools')))

import publisher
import rst_tools
pub = publisher

results_path = './'

rst = rst_tools 
rst_str = ''

lw = 2.0

## speeds without pvsync

raw_file='./ieee118.raw'
raw_df_dict =  raw2pandas(raw_file)


test_dict = raw_df_dict



test_data = {'tests_file':results_path,
             'test_id':'test1',
             'element':'generator',
             'variable':'PG',
             'resuts_file_type':'raw_dict'}

geo_data = {'geojson_file':'./geo_ieee118.json',
            'bottom_lat':17.75,  #  south dakota
            'top_lat':18.93,
            'left_lon':-67.7,
            'right_lon':-65.5087,
            'mask_oceans':True, 
            'draw_map':False}
       
plot_data = {'type':'absolute_heatmap',
#             'z_max':1500.0,
#             'z_min':0.0,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear',
             'map_name':'ieee118_u',
             'map_resolution':'h'}
            
          
fig = plt.figure()

ax1 = plt.subplot2grid((1,1), (0,0))
      
time = 0.0

pub.psys_heatmap_add(test_data, geo_data, plot_data, time, test_dict, ax1)
m = pub.psys_map(geo_data, plot_data, ax1)


fig.show()