# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import numpy as np
import hickle
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))

import pypstools

pub = pypstools.publisher

results_path = './'

rst = pypstools.rst_tools 
rst_str = ''

tests_set_id = 'ieee12g_pvsync_10'
tests_set_hdf5_id = 'ieee12g_10_pvs'
results_dir = r'/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/{:s}/results'.format(tests_set_id) 
doc_dir = r'/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc'
rst_dir = os.path.join(doc_dir,'source','pvsync',tests_set_id,'vref_up')
pvsync_buses_list = [13,14]

rst_str += rst.chapter('Generator voltage reference change')

rst_str += '.. include:: description.rst' + '\n'*2

lw = 2.0

## speeds without pvsync

hdf5_path = os.path.join('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_base/results/ieee12g_base_pvs.hdf5')
h_base = hickle.load(hdf5_path)

hdf5_path = os.path.join(results_dir,'{:s}.hdf5'.format(tests_set_hdf5_id))
h_pvs = hickle.load(hdf5_path)


test_dict = {'sys':{'time':np.array([0.0]),
                    'buses':['1','2','3','4']},
             'bus':{'1':{'u':{'data':np.array([1.0 ])}},
                    '2':{'u':{'data':np.array([0.95])}},
                    '3':{'u':{'data':np.array([1.01])}},
                    '4':{'u':{'data':np.array([1.02])}}}
             }



test_data = {'tests_file':results_path,
             'test_id':'test1',
             'element':'bus',
             'variable':'u',
             'resuts_file_type':'dict'}

geo_data = {'geojson_file':'./ieee12g_50_pvs.json',
            'bottom_lat':43,  #  south dakota
            'top_lat':46.5,
            'left_lon':-104,
            'right_lon':-98,
            'mask_oceans':True}
           
plot_data = {'type':'absolute_heatmap',
             'z_max':1.03,
             'z_min':0.92,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear'}
            
            
      
time = 0.0
pub.psys_heatmap(test_data, geo_data, plot_data, time, test_dict)