# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 18:56:34 2015

@author: jmmauricio
"""
from psse_simulation import device_writer
def test_device_writer():
    
    case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'
    gen_types_file = 'tgov_hygov_pvsync_10.tsv'
    file_name_rst = 'ieee118_pvsyn_10'
    file_name_dyr = 'ieee118_pvsyn_10'
    datas = np.genfromtxt(os.path.join(case_dir,gen_types_file), skiprows=1, delimiter='\t', usecols=(0), usemask=True ) 
    gen_thermal_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    
    datas = np.genfromtxt(os.path.join(case_dir,gen_types_file), skiprows=1, delimiter='\t', usecols=(1), usemask=True ) 
    gen_hydro_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    
    
    datas = np.genfromtxt(os.path.join(case_dir,gen_types_file), skiprows=1, delimiter='\t', usecols=(2), usemask=True ) 
    gen_cond_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)

    datas = np.genfromtxt(os.path.join(case_dir,gen_types_file), skiprows=1, delimiter='\t', usecols=(3), usemask=True ) 
    gen_bess_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)

    
    gen_raw_data =np.genfromtxt(os.path.join(case_dir,'raw_gens.csv'), delimiter=',', usecols=(0,9,10), dtype=[('buses','i'),('R_source','d'),('X_source','d')])
    #datas = np.genfromtxt('tgov_hygov_base.tsv', skiprows=1, delimiter='\t', usecols=(3), usemask=True ) 
    #gen_bess_buses = np.array(datas[np.logical_not(datas.mask)])
    
    import json
    models2dict =json.load(open(os.path.join(case_dir,'models_psse.json'),'r'))
    

    f_dyr = open(os.path.join(case_dir,file_name_dyr + '.dyr'), 'w')
    f_rst = open(os.path.join(case_dir,file_name_rst + '.rst'), 'w')
    toDYR = ''  
    toRST = ''
    
    ## hydro generators
    models = ['GENSAL','HYGOV','SEXS']
    IBUSES = gen_hydro_buses
    ID = 1
    
    for IBUS in IBUSES:
        
        for model in models:
            gen_raw_data['X_source'][np.where(gen_raw_data['buses']==IBUS)[0][0]] = models2dict['GENSAL']['CONs'][8]['J+8'][u'typical']
            toReST, toPSSE = device_writer(model, IBUS, ID, models2dict)
            toDYR += toPSSE
            toRST += toReST
    
    ## thermal generators        
    models = ['GENROU','TGOV1','SEXS']
    IBUSES = gen_thermal_buses
    ID = 1
    
    for IBUS in IBUSES:
        for model in models:
            gen_raw_data['X_source'][np.where(gen_raw_data['buses']==IBUS)[0][0]] = models2dict['GENROU']['CONs'][10]['J+10'][u'typical']
            toReST, toPSSE = device_writer(model, IBUS, ID, models2dict)
            toDYR += toPSSE
            toRST += toReST            
    
    ## condensators generators        
    models = ['GENROU','SEXS']
    IBUSES = gen_cond_buses
    ID = 1
    
    for IBUS in IBUSES:
        for model in models:
            gen_raw_data['X_source'][np.where(gen_raw_data['buses']==IBUS)[0][0]] = models2dict['GENROU']['CONs'][10]['J+10'][u'typical']
            toReST, toPSSE = device_writer(model, IBUS, ID, models2dict)
            toDYR += toPSSE
            toRST += toReST            
            
    ## condensators generators        
    models = ['PVSYN1']
    IBUSES = gen_bess_buses
    ID = 1
    
    for IBUS in IBUSES:
        for model in models:
#            gen_raw_data['X_source'][np.where(gen_raw_data['buses']==IBUS)[0][0]] = models2dict['PVSYN1']['CONs'][10]['J+10'][u'typical']
            toReST, toPSSE = device_writer(model, IBUS, ID, models2dict)
            toDYR += toPSSE
            toRST += toReST      
            
    f_dyr.write(toDYR)
    f_rst.write(toRST)
    f_dyr.close()
    f_rst.close()
    
    np.savetxt('test.out', gen_raw_data, delimiter='\t') 
    
if __name__ == "__main__":
    
    a = 1
    test_device_writer()