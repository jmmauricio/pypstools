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

geo_data = {'geojson_file':'./ps9bus.json',
            'bottom_lat':42.5,  #  south dakota
            'top_lat':44.2,
            'left_lon':-107.8,
            'right_lon':-104.5,
            'mask_oceans':True}
            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'ps9bus'}
            
            
m = pub.psys_map(geo_data, plot_data)