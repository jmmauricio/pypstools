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

tests_set_id = 'ieee12g_pvsync_10'
tests_set_hdf5_id = 'ieee12g_10_pvs'
results_dir = r'/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/{:s}/results'.format(tests_set_id) 
doc_dir = r'/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc'
rst_dir = os.path.join(doc_dir,'source','pvsync',tests_set_id,'vref_up')
pvsync_buses_list = [13,14]
1
rst_str += rst.chapter('Generator voltage reference change')

rst_str += '.. include:: description.rst' + '\n'*2

lw = 2.0

## speeds without pvsync

raw_file='/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/system/ieee12g_pvsync_10.raw'
raw_df_dict =  raw2pandas(raw_file)


test_dict = raw_df_dict



test_data = {'tests_file':results_path,
             'test_id':'test1',
             'element':'bus',
             'variable':'VM',
             'resuts_file_type':'raw_dict'}

geo_data = {'geojson_file':'./ieee12g_50_pvs.json',
            'bottom_lat':43,  #  south dakota
            'top_lat':46.5,
            'left_lon':-104,
            'right_lon':-98,
            'mask_oceans':True}
           
plot_data = {'type':'absolute_heatmap',
             'z_max':1.05,
             'z_min':0.95,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear',
             'map_name':'ieee12g_u'}
            
          
fig = plt.figure()

ax1 = plt.subplot2grid((2,2), (0,0), rowspan=3)
      
time = 0.0

pub.psys_heatmap(test_data, geo_data, plot_data, time, test_dict, ax1)
m = pub.psys_map(geo_data, plot_data, ax1)


fig.show()