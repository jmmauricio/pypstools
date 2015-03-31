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
tools = pypstools.tools

geojson_file =  './osm_sing_simplified.json' 
subs = tools.geo2substations(geojson_file)