# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 07:32:22 2015

@author: jmmauricio
"""

import os

directory = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/simulations/archive'



def rename_files(old_string, new_string,directory):
    dir_list = os.listdir(directory)
    

    for item in dir_list:
        fileName, fileExtension = os.path.splitext(item)
    
        if fileExtension == '.py':
            
    
            new_fileName = fileName.replace(old_string,new_string)
            
            print(fileName + ' -> ' + new_fileName) 
            print(os.path.join(directory,fileName + fileExtension))
            os.rename(os.path.join(directory,fileName  + fileExtension), os.path.join(directory,new_fileName+   fileExtension))
    
old_string = 'ieee12g_10_pvs'
new_string = 'ieee12g_base'
    
#rename_files(old_string, new_string,directory)


dir_list = os.listdir(directory)

old_string = 'ieee12g_10'
new_string = 'ieee118_10'

old_string = 'ieee_12_generic'
new_string = 'ieee118'


old_string = r'ieee118\code'
new_string = r'ieee_118\ieee118_pvsync\code'

old_string = r'10_pvs'
new_string = r'base'


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
        


#
