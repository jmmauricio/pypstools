# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 07:32:22 2015

@author: jmmauricio
"""

import os


directory = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/ieee118_pvsync/code/ieee118_pv_50/simulations'


def rename_files(old_string, new_string,directory):
    dir_list = os.listdir(directory)
    

    for item in dir_list:
        fileName, fileExtension = os.path.splitext(item)
    
        if fileExtension == '.py':
            
    
            new_fileName = fileName.replace(old_string,new_string)
            
            print(fileName + ' -> ' + new_fileName) 
            print(os.path.join(directory,fileName + fileExtension))
            os.rename(os.path.join(directory,fileName  + fileExtension), os.path.join(directory,new_fileName+   fileExtension))
    
old_string = 'ieee118_50_pvs'
new_string = 'ieee118_50_pv'

rename_files(old_string, new_string, directory)


old_string = 'ieee118_50_pvs'
new_string = 'ieee118_50_pv'

old_string = 'ieee118_pvsync_50'
new_string = 'ieee118_pv_50'

'''
# old_string = 'ieee118_pvsync_base_load_trip_4'
# new_string = 'ieee118_pvsync_base_load_trip_80'

# from_bus_old = 7
# to_bus_old = 8
# from_bus_new = 30
# to_bus_new = 26
# old_string = 'ieee118_pvsync_base_fault_{from_bus_old}_line_{from_bus_old}_{to_bus_old}'.format(from_bus_old=from_bus_old,to_bus_old=to_bus_old)
# new_string = 'ieee118_pvsync_base_fault_{from_bus_new}_line_{from_bus_new}_{to_bus_new}'.format(from_bus_new=from_bus_new,to_bus_new=to_bus_new)
#
#
# directory = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/ieee118_pvsync/doc/code/pvsync/ieee118_pvs_base'
#
# old_string = 'ieee12g'
# new_string = 'ieee118_pvs_base'
#
#

#
#

#
# old_string = 'ieee12g_10'
# new_string = 'ieee118_10'
#
# old_string = 'ieee12g_pvsync_base'
# new_string = 'ieee118_pvsync_base'
#
# #
# old_string = r'ieee_12_generic\code'
# new_string = r'ieee_118\ieee118_pvsync\code'
# #
# old_string = r'ieee12g_base_pvs_gen_trip_9'
# new_string = r'ieee118_base_pvs_gen_trip_89'
#
# old_string = r'ieee12g_base_pvs_load_trip_4'
# new_string = r'ieee118_base_pvs_load_trip_80'
#
#
# old_string = 'ieee12g_10_pvs_fault_{from_bus_old}_line_{from_bus_old}_{to_bus_old}'.format(from_bus_old=from_bus_old,to_bus_old=to_bus_old)
# new_string = 'ieee118_base_pvs_fault_{from_bus_new}_line_{from_bus_new}_{to_bus_new}'.format(from_bus_new=from_bus_new,to_bus_new=to_bus_new)
#
# #old_string = 'ieee12g_10_pvs_fault_38_line_38_65'
# #new_string = 'ieee118_base_pvs_fault_38_line_38_65'
#

old_string = 'gen_trip_12'
new_string = 'gen_trip_89'

# old_string = 'ieee118_10_pvs'
# new_string = 'ieee118_pvs_10'

'''

dir_list = os.listdir(directory)

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
       



