# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""


import sys,os
sys.path.insert(0,os.path.abspath(__file__+"/../pypstools"))


import pypstools

ds = pypstools.digsilent_simulation

results_path =  'test_out.txt'
test_dict, type_list =  ds.ds_txt_col_2_dict(results_path)
    


