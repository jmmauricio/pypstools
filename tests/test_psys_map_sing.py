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


geo_data = {'geojson_file':'./geojson_simplified.json',
            'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666,
            'mask_oceans':True}
            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'sing_simple'}
            
            
m = pub.psys_map(geo_data, plot_data)