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
tools = pypstools.tools

mail = 'jmmauricio6@gmail.com'
file_password = open('/home/jmmauricio/password.yaml')
password = file_password.read().rstrip()
file_password.close()

spreadsheet_name = 'red_sing_id'
geojson_path = './geojson.json'    
simplified_geojson_path = './geojson_simplified.json' 

feat_geo_total = tools.gspreadsheet2geojason(spreadsheet_name, mail,password,geojson_path)


tools.simplify_ways(geojson_path, simplified_geojson_path)
  