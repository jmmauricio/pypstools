# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 08:18:05 2015

@author: jmmauricio
"""

import numpy as np

ds = open('../examples/gs_test.txt','r')

header = ds.readline()
data = np.loadtxt(ds, delimiter='\t',skiprows=1 )

test_dict =   {'sys':{
                      'time':[],
                      'buses':[],
                      'syms':[],
                      'loads':[]
                     },
               'bus':{},
               'sym':{},                       
               'load':{}
               }
it = 0               
for item_head in header.split('\t'):
    items = item_head.split(':')
    if items[0]=='sys':
        if not test_dict['sys'].has_key(items[1]):
            test_dict['sys'].update({items[1]:[]})
        test_dict['sys'][items[1]]= data[:,it]

        print('sys')
    if items[0]=='bus':
        if not test_dict['bus'].has_key(items[1]):
            test_dict['bus'].update({items[1]:{}})
        if not test_dict['bus'][items[1]].has_key(items[2]):
            test_dict['bus'][items[1]].update({items[2]:[]})
        test_dict['bus'][items[1]][items[2]] = data[:,it]        
        test_dict['sys']['buses'] += test_dict['bus'][items[1]]
        print('bus')        
    if items[0]=='sym':
        print('sym')   
    if items[0]=='line':
        print('line')     
    it += 1
#ds.close()
    