# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 08:18:05 2015

@author: jmmauricio
"""

import numpy as np

def ds2dict(results_path):
    '''Funcion para pasar de .txt de resultados de digsilent a .hdf5.
    Los resultados estan en una fila por paso de integración. 
    Da error por fila demasiado.
    
    
    Parameters
    ----------    
    results_path : string
                   path for the .txt file
                   
                   
    Returns
    -------
    test_dict : dictionary
                results as dictionaries with np.array                   
                   
    Example
    -------
                        
    >>> results_path =  '../examples/gs_test.txt'
    >>> test_dict = ds2hdf5_1(results_path)        
    
    '''    
    
    
    ds = open(results_path,'r')
    
    header = ds.readline()
    data = np.loadtxt(ds, delimiter='\t',skiprows=1, dtype=np.object )
    
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
    
    ds.close()
    
    return test_dict
   
    
def ds_txt_col_2_dict(results_path):
    '''Funcion para pasar de .txt de resultados de digsilent a .hdf5.
    Los resultados estan en una columna por paso de integración. 
    
    
    Parameters
    ----------    
    results_path : string
                   path for the .txt file
                   
                   
    Returns
    -------
    test_dict : dictionary
                results as dictionaries with np.array                   
                   
    Example
    -------
                        
    >>> results_path =  '../examples/gs_test.txt'
    >>> test_dict = ds2hdf5_1(results_path)        
    
    '''    
    
    test_dict =   {'sys':{
                          'time':[],
                          'buses':[],
                          'syms':[],
                          'loads':[]
                         },
                   'bus':{},
                   'sym':{},                       
                   'load':{},
                   'line':{}
                   }
    
   
    ds = open(results_path,'r')  # opens file
    
    header = ds.readline()  
    
    reading_header = True
    
    rows = 0
    
    header_list = header.split(':')
    test_dict['sys']['time']=np.array([float(header_list[1])])
    
    type_list = []
    id_list = []
    variable_list = []
    unit_list = []
    while reading_header == True:
        
        header = ds.readline() 
        header_list = header.split(':')
        

        
        if header_list[0]== 't':
           reading_header = False

        else: 
            type_list += [header_list[0]]
            
            if header_list[0] == 'bus':
                test_dict['sys']['buses'] += [header_list[1]]

            if header_list[0] == 'sym':
                test_dict['sys']['syms'] += [header_list[1]]
                
            id_list += [header_list[1]]
            variable_list += [header_list[2]]
            unit_list += [header_list[3].split('\t')[0]]
            if not test_dict[header_list[0]].has_key(header_list[1]):
                test_dict[header_list[0]].update({header_list[1]:{header_list[2]:{}}})
            if not test_dict[header_list[0]][header_list[1]].has_key(header_list[2]):
                test_dict[header_list[0]][header_list[1]].update({header_list[2]:{}})
            units = (header_list[3].split('\t')[0])
            value = float(header_list[3].split('\t')[1])
            test_dict[header_list[0]][header_list[1]][header_list[2]].update({'data':np.array([value])})
            test_dict[header_list[0]][header_list[1]][header_list[2]].update({'units':units})
        rows += 1
           
    element_data = zip(type_list,id_list,variable_list,unit_list) 
    data_row = header
    data_row_list = header_list 
    while data_row:
        for it in range(rows): 
            data_row_list = data_row.split(':')
            if data_row_list[0]=='t':
                test_dict['sys']['time'] = np.vstack((test_dict['sys']['time'], np.array([float(data_row_list[1])])))
            else:
                if len(data_row_list[0])>0:
                    element_type = element_data[it-1][0]
                    element_id = element_data[it-1][1]
                    element_variable = element_data[it-1][2]
                    element_unit = element_data[it-1][3]
                    previous_value = test_dict[element_type][element_id][element_variable]
                    data_row_value = np.array(float(data_row_list[0]))
                    previous_value = test_dict[element_type][element_id][element_variable]['data']
                    test_dict[element_type][element_id][element_variable]['data'] = np.hstack((previous_value, data_row_value))
            data_row = ds.readline()             
    ds.close()
            


        
#    data = np.loadtxt(ds, delimiter='\t',skiprows=1 )
#    

#    it = 0               
#    for item_head in header.split('\t'):
#        items = item_head.split(':')
#        if items[0]=='sys':
#            if not test_dict['sys'].has_key(items[1]):
#                test_dict['sys'].update({items[1]:[]})
#            test_dict['sys'][items[1]]= data[:,it]
#    
#            print('sys')
#        if items[0]=='bus':
#            if not test_dict['bus'].has_key(items[1]):
#                test_dict['bus'].update({items[1]:{}})
#            if not test_dict['bus'][items[1]].has_key(items[2]):
#                test_dict['bus'][items[1]].update({items[2]:[]})
#            test_dict['bus'][items[1]][items[2]] = data[:,it]        
#            test_dict['sys']['buses'] += test_dict['bus'][items[1]]
#            print('bus')        
#        if items[0]=='sym':
#            print('sym')   
#        if items[0]=='line':
#            print('line')     
#        it += 1
        
    return test_dict, type_list
 
if __name__ == "__main__":
    
    results_path =  '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/osm/ds_sing_1.txt'
    hdf5_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/osm/ds_sing_2.hdf5'
    test_dict, type_list =  ds_txt_col_2_dict(results_path)
    
    import hickle
    
    hickle.dump(test_dict,open(hdf5_file,'w'),compression='lzf')
    loaded = hickle.load(hdf5_file)