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

import matplotlib.pyplot as plt
import pypstools.digsilent_simulation as ds
import pypstools.publisher as pub

results_path =  '/home/jmmauricio/Documents/private/cdec_sing/digsilent_results/hola.txt'
test_dict =  ds.ds_2_dict(results_path)

from mpl_toolkits.basemap import Basemap



fig, (ax0) = plt.subplots(nrows=1)



results_dict = test_dict

test_data = {'tests_file':results_path,
             'test_id':'test1',
             'element':'bus',
             'variable':'u',
             'resuts_file_type':'dstxt'}

geo_data = {'geojson_file':'./geojson.json',
            'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666,
            'mask_oceans':True}
            
plot_data = {'type':'absolute_heatmap',
             'z_max':1.03,
             'z_min':0.98,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear',
             'map_name':'test'}
            
            
      

#for time in np.arange(0.1,3.0,0.1):
#(test_data, geo_data, plot_data, time, test_dict, ax)
#m = pub.psys_map(geo_data, plot_data, ax0)
x_data, y_data, z_data = pub.psys_scatter(test_data, geo_data, plot_data, 0.0, test_dict, m, ax0)


fig.show()