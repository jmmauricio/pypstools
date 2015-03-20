# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 07:32:22 2015

@author: jmmauricio
"""

import os

directory = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_50/simulations'

def rename_files():
    dir_list = os.listdir(directory)
    
    old_string = '.'
    new_string = ''
    for item in dir_list:
        fileName, fileExtension = os.path.splitext(item)
    
        if fileExtension == '.py':
            
    
            new_fileName = fileName.replace(old_string,new_string)
            
            print(fileName + ' -> ' + new_fileName) 
            print(os.path.join(directory,fileName + fileExtension))
            os.rename(os.path.join(directory,fileName  + fileExtension), os.path.join(directory,new_fileName+   fileExtension))
    


dir_list = os.listdir(directory)

old_string = 'ieee12g_pvsync_30'
new_string = 'ieee12g_pvsync_50'

old_string = 'ieee12g_30_pvs'
new_string = 'ieee12g_50_pvs'
for item in dir_list:
    fileName, fileExtension = os.path.splitext(item)

    if fileExtension == '.py':
        

        file_path = os.path.join(directory,fileName + fileExtension)
        file_obj = open(file_path, 'r')
        string = file_obj.read()
        string_new = string.replace(old_string, new_string)
        file_obj.close()
        print(string_new)
        file_obj = open(file_path, 'w')
        file_obj.write(string_new)
        file_obj.close()
        



