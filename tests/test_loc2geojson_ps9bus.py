# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:30:50 2015

@author: jmmauricio
"""

import sys,os
import numpy as np
from pypstools.tools import raw2pandas
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..','pypstools')))

import publisher
import tools
import rst_tools
pub = publisher

results_path = './'

rst = rst_tools 
rst_str = ''
    
loc_path = './ps9bus.loc'
geojson_path = './ps9bus.json'

bus_1,bus_2 = 1,2

bus_1_lon_lat = (-104,44.0)  #  south dakota
bus_1_2_dist = 200.0e3


feat_geo_buses, feat_geo_branches, geo_total = tools.loc2geojson(loc_path, geojson_path,bus_1,bus_2,bus_1_2_dist, bus_1_lon_lat)
