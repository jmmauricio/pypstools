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

pub = pypstools.publisher

geo_data = {'geojson_file':'./ieee12g_50_pvs.json',
            'bottom_lat':43,  #  south dakota
            'top_lat':46.5,
            'left_lon':-104,
            'right_lon':-98,
            'mask_oceans':True}
            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'ieee12g'}
            
            
m = pub.psys_map(geo_data, plot_data)