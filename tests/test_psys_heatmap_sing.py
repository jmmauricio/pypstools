# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import numpy as np
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))


import pypstools
ds = pypstools.digsilent_simulation

results_path =  'test_out.txt'
test_dict, type_list =  ds.ds_txt_col_2_dict(results_path)

pub = pypstools.publisher


results_dict = test_dict

test_data = {'tests_file':results_path,
             'test_id':'test1',
             'element':'bus',
             'variable':'u',
             'resuts_file_type':'dstxt'}

geo_data = {'geojson_file':'./geojson_simplified.json',
            'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666,
            'mask_oceans':True}
            
plot_data = {'type':'absolute_heatmap',
             'z_max':1.03,
             'z_min':0.92,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear'}
            
            
      

for time in np.arange(0.1,3.0,0.1):
    pub.psys_heatmap(test_data, geo_data, plot_data, time)