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
    
    Column Header
    
    Elemen                    Variable
    
    * Short Path and Name     * Parameter Name
    
    
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
    
    header_1 = ds.readline()  
    header_2 = ds.readline() 
    reading_header = True
    
    rows = 0
    
    
    header_1_list = header_1.split('\t')
    header_2_list = header_2.split('\t')
    
    print(header_1_list)
    print(header_2_list)
    
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
            

def ds_2_dict(results_path):
    '''Funcion para pasar dekl .txt de resultados de digsilent a python dict.
    Los resultados estan en una columna por paso de integración. 
    
    Column Header
    
    Element                    Variable
    
    * Short Path and Name     * Parameter Name
    
    
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
                          'loads':[],
                          'genstats':[],
                          'usrmodels':[],
                         },
                   'bus':{},
                   'sym':{},                       
                   'load':{},
                   'line':{},
                   'genstat':{},
                   'usrmodel':{},
                   }
       
    ds = open(results_path,'r')  # opens file  
    
    
    
    header_1 = ds.readline()  
    header_2 = ds.readline() 

    
#    return header_1
    header_1_list = header_1.replace('\r\n','').replace('\n','').split('\t')
    header_2_list = header_2.replace('\r\n','').replace('\n','').split('\t')

    names_list = []
    elements_list = []
    for item in header_1_list[1:]:
        name_element = item.split('\\')[-1].split('.')
        elements_list +=  [name_element[1]]
        names_list += [name_element[0]]

  
    item = header_1_list[-1]    
    name_element = item.split('\\')[-1].split('.') # hay que evitar el final con \r\n
#    print(name_element)
    element = name_element[1][:]
    name = name_element[0]
    
    
    # results to the dict   
    it_col = 0 
    data = np.loadtxt(ds, delimiter='\t',skiprows=2, dtype=np.float )

    test_dict['sys']['time']=data[:,it_col].astype(np.float)
    
    
    
    for name,element,variable_ds in zip(names_list, elements_list,header_2_list[1:]):
        it_col += 1
        ds2ps_dict = {'m:u1 in p.u.':('u','pu'),
                      'm:fe':('fe', 'Hz'),
                      'm:u1:bus1 in p.u.':('u','p.u.'),
                      'm:P:bus1 in MW':('p','MW'),
                      'm:Q:bus1 in Mvar':('q','Mvar'),
                      's:Q1 in Mvar':('q', 'Mvar'),
                      's:P1 in MW':('p', 'MW'),
                      's:ve in p.u.':('ve','p.u.'),
                      's:ie in p.u.':('ie','p.u.'),
                      'c:firel in deg':('phir','p.u.'),
                      's:xspeed in p.u.':('speed','p.u.'),
                      's:pt in p.u.':('pt','p.u.'), 
                      's:xmt in p.u.':('xmt','p.u.'), 
                      's:xme in p.u.':('xme','p.u.'), 
                      's:cur1 in p.u.':('cur1','p.u.'), 
                      's:pgt in p.u.':('pgt','p.u.'), 
                      's:ut in p.u.':('ut','p.u.'),
                      'm:Qsum:bus1 in Mvar':('q', 'Mvar'),
                      'm:Psum:bus1 in MW':('p', 'MW'),
                      'm:fehz in Hz':('fehz','Hz'),
                      's:i_bat in A':('i_bat','A')
                     }
#        print(element,name,variable_ds)
        
        if variable_ds in ds2ps_dict:
            variable = ds2ps_dict[variable_ds][0]
            units = ds2ps_dict[variable_ds][1]
        else:
            variable = variable_ds
            units = ''
            
        if element == 'ElmSym':
            if not (name in test_dict['sym']):
                test_dict['sym'].update({name:{}})
                test_dict['sys']['syms'] += [name]
                 
            test_dict['sym'][name].update({variable:{'data':data[:,it_col].astype(np.float),'units':units}})
            
        if element == 'ElmTerm':
            if not (name in test_dict['bus']):
                test_dict['bus'].update({name:{}})
                test_dict['sys']['buses'] += [name]
                
            test_dict['bus'][name].update({variable:{'data':data[:,it_col].astype(np.float),'units':units}})  
            
        if element == 'ElmLod':
            if not (name in test_dict['load']):
                test_dict['load'].update({name:{}})
                test_dict['sys']['loads'] += [name]
                
            test_dict['load'][name].update({variable:{'data':data[:,it_col].astype(np.float),'units':units}})            
            
        if element == 'ElmGenstat':
            if not (name in test_dict['genstat']):
                test_dict['genstat'].update({name:{}})
                test_dict['sys']['genstats'] += [name]
                
            test_dict['genstat'][name].update({variable:{'data':data[:,it_col].astype(np.float),'units':units}})       
            
        if element == 'ElmDsl':
            if not (name in test_dict['usrmodel']):
                test_dict['usrmodel'].update({name:{}})
                test_dict['sys']['usrmodels'] += [name]
                
            test_dict['usrmodel'][name].update({variable:{'data':data[:,it_col].astype(np.float),'units':units}})       
            
      
    ds.close()
        
        
    return test_dict
 
if __name__ == "__main__":
    import h5py
    import os
#    h_pvs   = h5py.File(hdf5_path,'w')
#    result_dict = ds_2_dict('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/code/results/Demanda Alta-Escenario 4_2_ANG2.txt')
#    result_dict = ds_2_dict('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/abengoa_ssp/errores_govs/200U16w_CC1plena')
#    result_dict = ds_2_dict('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/master/pbetancourt/PBetancourt/digsilent/resultados/Caso_3_PUNTA CATALINA 02.txt')
    result_dict = ds_2_dict(os.path.join('..','tests','ds_simout.txt'))
#    result_dict = ds_2_dict(r'C:\Users\jmmauricio\hola.txt')