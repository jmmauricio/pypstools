""" Tools for dealing with power system data and results.

(c) 2015 Juan Manuel Mauricio
"""

import numpy as np
import scipy.linalg
import scipy.integrate
import h5py

def dict2h5(file_name, dict_in, dict_deepness=3):  
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
    
    if deepness==3:
        for test in data_dict:
            print test
            grp = f.create_group(test)
            for group in data_dict[test]:
                print group
                sub_grp = grp.create_group(group)
                for data in data_dict[test][group]:
                    var_name = data
                    var_values =  data_dict[test][group][data]
                    print var_name, var_values
                    sub_grp.create_dataset(var_name, data=var_values)
                
        f.close()

def test_tools_dict2:
    a=2
    b=3
    c=np.array([1,2,3,4])
    t=np.array([.1,.2,.3,.4])
    data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    file_name = 'foo.hdf5'
    dict2h5(file_name, data_dict) 


if __name__=="__main__":

    test_tools_dict2()
