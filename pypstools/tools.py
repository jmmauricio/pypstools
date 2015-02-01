""" Tools for dealing with power system data and results.

(c) 2015 Juan Manuel Mauricio
"""

import numpy as np
import scipy.linalg
import scipy.integrate
import h5py

def dict_to_h5(file_name, dict_in, dict_deepness=3):  
    ''' Saves a dictionary to hdf5 file

    >>> a=2
    >>> b=3
    >>> c=np.array([1,2,3,4])
    >>> t=np.array([.1,.2,.3,.4])
    >>> data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    >>> file_name = 'foo.hdf5'
    >>> dict2h5(file_name, data_dict) 

    '''        
    f = h5py.File(file_name,'w')
    
    if dict_deepness==3:
        for test in dict_in:

            grp = f.create_group(test)
            for group in dict_in[test]:

                sub_grp = grp.create_group(group)
                for data in dict_in[test][group]:
                    var_name = data
                    var_values =  dict_in[test][group][data]

                    sub_grp.create_dataset(var_name, data=var_values)
                
        f.close()

def h5_to_dict(file_name, dict_deepness=3):  
    ''' Saves a dictionary to hdf5 file

    >>> a=2
    >>> b=3
    >>> c=np.array([1,2,3,4])
    >>> t=np.array([.1,.2,.3,.4])
    >>> data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    >>> file_name = 'foo.hdf5'
    >>> dict_to_h5(file_name, data_dict) 

    '''        
    h5 = h5py.File(file_name,'r')
    
    if dict_deepness==3:
        for test in dict_in:

            grp = f.create_group(test)
            for group in dict_in[test]:

                sub_grp = grp.create_group(group)
                for data in dict_in[test][group]:
                    var_name = data
                    var_values =  dict_in[test][group][data]

                    sub_grp.create_dataset(var_name, data=var_values)
                
        f.close()

        return dict_out

def loc2geojson():
    
    loc_path = '/home/jmmauricio-m/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.loc'
    loc_file = open(loc_path, 'r')
    
    reading_buses = False
    for row in loc_file.readlines():
#        print(len(row))

        if (reading_buses == True) and (row[0:1] == ' '):
            reading_buses = False
        
        if reading_buses == True:
            print((row))            
        
        if row[0:4]=='CART':
            reading_buses = True        
        
    
    
def test_tools_dict2h5():
    a=2
    b=3
    c=np.array([1,2,3,4])
    t=np.array([.1,.2,.3,.4])
    data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    
    file_name = 'foo.hdf5'
    dict_to_h5(file_name, data_dict) 


if __name__=="__main__":

    #test_tools_dict2h5()
    loc2geojson()
