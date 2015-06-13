""" Tools for simulation with PSS/E.

(c) 2015 Juan Manuel Mauricio
"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg

import analysis

import xml.etree.ElementTree as ET
from StringIO import StringIO
import json

# -*- coding: cp1252 -*-
#[dyntools_demo.py]  09/22/100    Demo for using functions from dyntools module
# ====================================================================================================
'''
'dyntools' module provide access to data in PSS(R)E Dynamic Simulation Channel Output file.


'''
import yaml as ya
import os, sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
#from pypstools.tools import name2chan
#from pypstools.publisher.plot_tools import g_colors
#import pypstools.publisher.rst_basic as rst
import h5py

def psse(test_info, psse_version = 'PSSE33'):
    
    
    out_dir = test_info['out_dir']    
    raw_dyr_dir = test_info['raw_dyr_dir'] 
    out_dir = test_info['out_dir']     
    case_name = test_info['case_name']  
    # Get installed location of latest PSS(R)E version

    if psse_version == 'PSSE33':
        pssedir = r'C:\Program Files\PTI\PSSE33'
    if psse_version == 'PSSEUniversity33':        
        pssedir = r'C:\Program Files\PTI\PSSEUniversity33'
    
    # Files Used

    sys.path.append(os.path.join(os.getcwd(),'..','..'))  
    pssbindir  = os.path.join(pssedir,'PSSBIN')
    
    sys.path.append(os.path.join(os.getcwd(),'..'))
    
    if test_info.has_key('modellibrary'):
        libraryname = test_info['modellibrary']
    else:
        libraryname = os.path.join(raw_dyr_dir,'dsusr.dll')
    
    rawfile    = os.path.join(raw_dyr_dir,case_name + '.raw')
    dyrfile    = os.path.join(raw_dyr_dir,case_name + '.dyr')
    dyafile_avr= os.path.join(raw_dyr_dir,case_name + '_avr.dya')
    dyafile_gov= os.path.join(raw_dyr_dir,case_name + '_gov.dya')
    dyafile_pss= os.path.join(raw_dyr_dir,case_name + '_pss.dya')
    xsfile = os.path.join(out_dir,case_name + '_xs.txt')
    savfile    = os.path.join(out_dir,case_name + '.sav')
    savdynfile = os.path.join(out_dir,case_name + '_dyn.sav')
    snpfile    = os.path.join(out_dir,case_name + '.snp')
    outfile1   = os.path.join(out_dir,case_name + '.out')
    outfile2   = os.path.join(out_dir,case_name + '.out')
    outfile3   = os.path.join(out_dir,case_name + '.out')
    prgfile    = os.path.join(out_dir,'dyntools_demo_progress.txt')
    chnffile = os.path.join(out_dir,case_name + '.pkl') 
    lsa_file  = os.path.join(out_dir,case_name + '.lsa')
    lsa_dat  = os.path.join(out_dir,case_name + '.dat')
    ltifile = os.path.join(out_dir,'sys_abcd_f12.pkl')
    config_file = 'configuration.pkl'
    tests_config_file = os.path.join(out_dir,'tests.pkl')
    tests_out = os.path.join(out_dir,'tests_out.hdf5')


    # Check if running from Python Interpreter
    exename = sys.executable
    p, nx   = os.path.split(exename)
    nx      = nx.lower()
    if nx in ['python.exe', 'pythonw.exe']:
        os.environ['PATH'] = pssbindir + ';' + os.environ['PATH']
        sys.path.insert(0,pssbindir)
    
    
    import dyntools
    import psspy
    import redirect
    
    ierr = psspy.close_powerflow()
    
    redirect.psse2py()    
    
    _i = psspy._i
    _f = psspy._f

    ierr = psspy.psseinit(buses=80000)  # choose here bus numbers you want
    
    psspy.lines_per_page_one_device(1,90)
    psspy.progress_output(2,prgfile,[0,0])
    
    psspy.read(0,rawfile)
    
    
    S_b = 100.00
    
    ierr = psspy.fnsl([0,0,0,1,1,0,99,0])
    
    
    # Se guarda la solucion
    psspy.save(savfile)
    
    
    # Se convierten las cargas y los generadores para la simulacion dinamica
    psspy.cong(0)
    psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
    
    # se guarda la solucion .sav para simulacion dinamica
    psspy.save(savdynfile)
    ierr = psspy.addmodellibrary(libraryname)
    if ierr == 0: 
        print('Library {:s} added'.format(libraryname))
    if ierr == 1: 
        print('Library not found!')    
    # se cargan los datos dinamicos
    psspy.dyre_new([1,1,1,1],dyrfile,"","","")
      

    channels = test_info['channels'] 

    sid = 0    
    all_buses = 0
        
    for item in channels:
        

        # VOLT
        if item == 'u':
            if channels[item] == 'all':                
                flag, string = 2,'NUMBER'
                ierr, iarray = psspy.abusint(-1, flag, string)
            sid += 1
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])          
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,13,0])  # STATUS(5) = 13 VOLT, bus pu voltages (complex).  
            
        # ANG
        if item == 'phiu':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)                
            sid += 1
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 1 ANGLE, machine relative rotor angle (degrees).
        
        # SPD
        if item == 'speed':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)                
            sid += 1    
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,7,0])  # STATUS(5) = 7 SPEED, machine speed deviation from nominal (pu).           

        # PGEN
        if item == 'p_gen':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)                
            sid += 1    
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,2,0])  # STATUS(5) = 2 PELEC, machine electrical power (pu on SBASE).

        # QGEN
        if item == 'q_gen':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)                
            sid += 1    
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,3,0])  # STATUS(5) = 3 QELEC, machine reactive power.

        # PLOAD
        if item == 'p_load':
            if channels[item] == 'all':                
                flag, string = 4,'NUMBER'
                ierr, iarray = psspy.alodbusint(-1, flag, string)              
            sid += 1    
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,25,0])  #STATUS(5) = 25 PLOAD.         

        # QLOAD
        if item == 'p_load':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.alodbusint(-1, flag, string)                 
            sid += 1    
            psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
            psspy.chsb(sid,all_buses,[-1,-1,-1,1,26,0])  #STATUS(5) = 26 PLOAD.              
                        
    # se guarda todo en .snp
    psspy.snap([-1,-1,-1,-1,-1],snpfile)
    
    # se inicializa el sistema
    psspy.strt(0,outfile1)
    
  
    return psspy,dyntools,savdynfile,snpfile


def name2chan(chnf, varname, busnumber, bus_to=0):

    '''
    SPD
    FREQ
    ETRM
    PMEC
    VAR 5
    VAR 6
    '''

    if type(chnf)==type(()):
        chan_dict = chnf[1]
        #print type(chnf)

    else:       
        chan_dict = chnf.get_data()[1]

    for it in range(len(chan_dict)-1):

        var_name = chan_dict[it+1].split()[0]

        #print chan_dict
        bus_number = int(chan_dict[it+1].split()[1].split('[')[0])
        
        if varname==var_name and busnumber==bus_number:
            #print str(it+1) + ' : ' + chan_dict[it+1]
            return it+1

        pass



class tests:
    '''Class to simulate tests with PSS/E


    '''
    import hickle

    def __init__(self):
#        self.psspy = psspy
#        self.dyntools =dyntools
#        self.savdynfile = savdynfile
#        self.snpfile = snpfile
        self.channels_yaml = 'channels.yaml'
        self.t_pert = 1.0 # default time for perturbation
        self.t_end = 15.0 # default time to end the simulation
        self.dt = 0.001   # default integration time step
        self.decimation_file = 25
        self.decimation_progress = 1000
        self.tests_results = {}
        
    def set_up(self, yaml_file):

        import yaml as ya
        self.tests_yaml = yaml_file
        self.tests_info = ya.load(open(yaml_file,'r'))
        if self.tests_info.has_key('t_end'):
            self.t_end = self.tests_info['t_end']
            
        
        
    def set_up_psse(self,item_test):
        
        psspy,dyntools,savdynfile,snpfile = psse(item_test, psse_version = 'PSSE33')
        
        self.psspy = psspy
        self.dyntools = dyntools
        self.savdynfile = savdynfile
        self.snpfile = snpfile

    def run_tests(self):    
        
        
        for item_test in self.tests_info['tests']:   
            self.data = item_test 
            self.set_up_psse(item_test)
            self.outfile = os.path.join(item_test['out_dir'],item_test['case_name'] + '.out')
            self.run_test(self.outfile )
            self.outfile2dict()
            self.tests_results.update({item_test['test_id']:self.results_dict})
            
        tests_out = os.path.join(self.tests_info['hdf5file'])
        
        hickle.dump(self.tests_results, tests_out)
        
        return self.tests_results        
        
        
    def run_test(self, outfile):
        self.outfile = outfile
        psspy = self.psspy

        # load sav and snp:
        psspy.case(self.savdynfile)  # sav file with generators and loads converted
        psspy.rstr(self.snpfile)     # snp file with channels defined   
        psspy.strt(0,self.outfile)  # initialization (again)

        # system initialization
        psspy.strt(0,self.outfile)
        
        _i = psspy._i
        _f = psspy._f
        psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f, self.dt,_f,_f,_f,_f,_f])

	# runs without perturbation until t=1s
        psspy.run(0, self.t_pert,self.decimation_progress,self.decimation_file,self.decimation_file)

	# for no perturbation
        if self.data['test_type']=='none':
            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
            
	# for v_ref changes
        if self.data['test_type']=='v_ref_change':
            ibus = self.data['gen_bus']
            id   = self.data['gen_id']
            newval = self.data['change']

            ierr = psspy.increment_vref(ibus, str(id), newval)

            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)

	# for gen trip
        if self.data['test_type']=='gen_trip':
            ibus = self.data['gen_bus']
            id   = self.data['gen_id']

            ierr = psspy.dist_machine_trip(ibus,str(id))

            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
            
	# for load trip: load trip
        if self.data['test_type']=='load_trip':
            frmbus = self.data['load_bus']
            id   = self.data['load_id']
            ierr = psspy.purgload(frmbus, str(id))
            
                
            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
    
    
    
    
	# for load change: change in loads active and reactive powers
        if self.data['test_type']=='load_change':
            ibus = self.data['load_bus']
            id   = self.data['load_id']
            p_load_new   = self.data['p_load_new']
            q_load_new   = self.data['q_load_new']
            sid = 9
            psspy.bsys(sid,0,[0.0,0.0],0,[],ibus,[ibus],0,[],0,[])
            flag = 5
            string = 'O_TOTALACT'
            ierr, rarray = psspy.alodbusreal(sid, flag, string)
            
            print('TOTALACT:')
            print(ierr)
            print(rarray)
            
            psspy.scal_2(sid,0,1,[0,0,0,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0])
            psspy.scal_2(0,1,2,[_i,1,0,1,0],[ p_load_new,0.0,0.0,-.0,0.0,-.0, q_load_new])
            
                
            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
            
	# for line trip
        if self.data['test_type']=='line_trip':
            ibus = self.data['i_bus']
            jbus = self.data['j_bus']
            id   = self.data['ckt_id']
            ierr = psspy.dist_branch_trip(ibus, jbus, str(id))                
            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)


	# for bus_fault_line trip
        if self.data['test_type']=='bus_fault_line_trip':
            print(self.data['test_id'] )
            fault_duration = self.data['fault_duration'] 
            fault_bus = self.data['fault_bus']
            ibus = self.data['i_bus']
            jbus = self.data['j_bus']
            id   = self.data['ckt_id']
#            t_fault = t_end  
            units = 1
            basekv = 400.0
            values = [0.0,-0.2E+16] 
            ierr = psspy.dist_bus_fault(ibus, units, basekv, values)
            
            t_end = self.t_pert +  fault_duration
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
            
            ierr = psspy.dist_clear_fault(1)
            ierr = psspy.dist_branch_trip(ibus, jbus, str(id))  
            
            t_end = self.t_end
            psspy.run(0, t_end,self.decimation_progress,self.decimation_file,self.decimation_file)
            
            
            
        if self.data['test_type']=='freq_change':
            t_ends = np.arange(1.0,2.0,0.01)
            for t_end in t_ends:
                #print(t_end)
            
                ierr, number = psspy.mdlind(1, '1', 'GEN', 'STATE')
                psspy.change_state(number, [(t_end-1.0)*0.1,0.0,(t_end-1.0)*0.1])
                psspy.run(0, t_end,1000,1,0)
                

                
        if self.data['test_type']=='p_ref_change':      
            ierr, L = psspy.mdlind(13, '1', 'GEN', 'VAR')
            L_var = 1
            psspy.change_var(L+L_var-1, 100.0)
#            L_var = 14
#            psspy.change_var(L+L_var-1, 0.2)

            t_end = 1.2
            psspy.run(0, t_end,1000,1,0)
            t_ends = np.arange(t_end,15.0,0.05)
            for t_end in t_ends:
                #print(t_end)
            
                ierr, k_g09 = psspy.mdlind(9, '1', 'GEN', 'STATE')
                ierr, k_g10 = psspy.mdlind(10, '1', 'GEN', 'STATE')
                ierr, k_g11 = psspy.mdlind(11, '1', 'GEN', 'STATE')
                ierr, k_g12 = psspy.mdlind(12, '1', 'GEN', 'STATE')
                
                ierr, speed_9 = psspy.dsrval('STATE', k_g09 + 4) 
                ierr, speed_10 = psspy.dsrval('STATE', k_g10 + 4) 
                ierr, speed_11 = psspy.dsrval('STATE', k_g11 + 4) 
                ierr, speed_12 = psspy.dsrval('STATE', k_g12 + 3) 
                psspy.change_var(L+L_var-1, -100000.0*(speed_12-speed_10)+100.0)
                
                
                psspy.run(0, t_end,1000,1,0)
                

        if self.data['test_type']=='q_ref_change':      
            ierr, L = psspy.mdlind(13, '1', 'GEN', 'VAR')
            L_var = 2
            psspy.change_var(L+L_var-1, 100.0)
#            L_var = 14
#            psspy.change_var(L+L_var-1, 0.2)

            t_end = 1.2
            psspy.run(0, t_end,1000,1,0)
            t_ends = np.arange(t_end,15.0,0.05)
            for t_end in t_ends:
                #print(t_end)
            
                ierr, k_g09 = psspy.mdlind(9, '1', 'GEN', 'STATE')
                ierr, k_g10 = psspy.mdlind(10, '1', 'GEN', 'STATE')
                ierr, k_g11 = psspy.mdlind(11, '1', 'GEN', 'STATE')
                ierr, k_g12 = psspy.mdlind(12, '1', 'GEN', 'STATE')
                
                ierr, speed_9 = psspy.dsrval('STATE', k_g09 + 4) 
                ierr, speed_10 = psspy.dsrval('STATE', k_g10 + 4) 
                ierr, speed_11 = psspy.dsrval('STATE', k_g11 + 4) 
                ierr, speed_12 = psspy.dsrval('STATE', k_g12 + 3)
                psspy.change_var(L+L_var-1-1, -100000.0*(speed_12-speed_10)+100.0)
                psspy.change_var(L+L_var-1, 100000.0*(speed_12-speed_10)+100.0)
                
                
                psspy.run(0, t_end,1000,1,0)

                
            # comienza la simulacion
            psspy.run(0, 15.0,1000,1,0)
        
        
#        print psspy.dsrval('CON', con_idx)
        
        
       
    def outfile2dict(self):        
        '''Converts PSS/E .out file to python dictionary
 
        example:
        
            {'sys':{
                    'time':np.array([...])},
             'bus':{
                    'bus_1':{
                             'u':np.array([...]),
                             'phiu':np.array([...]),
                             'fehz':np.array([...])},
                    'bus_2':{
                             'u':np.array([...]),
                             'phiu':np.array([...]),
                             'fehz':np.array([...])}},         
             'sym':{
                    'gen_1':{'bus_id':'bus_1'
                             'p':np.array([...]),
                             'q':np.array([...]),
                             'speed':np.array([...]),
                             've':np.array([...]),
                             'phi':np.array([...])}},
             'load':{
                     'load_1':{'bus_id':'bus_2'
                               'p':np.array([...]),
                               'q':np.array([...])}}
            }
            
            
            bus_1':{'speed':np.array([...]),{'volt':np.array([...])}},
             'bus_2':{{'volt':np.array([...])}}}              
        '''
        
#        vip_buses = self.vip_buses
#        
#        self.var_list =      [('volt','VOLT',vip_buses), ('speed','SPD',vip_buses), ('p_gen','POWR',vip_buses),
#         ('q_gen','VARS',vip_buses), ('freq','FREQ',vip_buses)]

        psspy = self.psspy
        
#        channels_str = open(self.channels_yaml,'r').read()
        channels = self.data['channels']

        chnf = self.dyntools.CHNF(self.outfile)

        t = np.array(chnf.get_data()[2]['time'])
        self.t = t

        results_dict = {'sys':{'time':np.array(np.array(chnf.get_data()[2]['time']))},
                        'syms':[],
                        'loads':[],
                        'bus':{},
                        'sym':{},
                        'load':{}}

        syms = {}
        loads = {}
        for item in channels:
   
            # VOLT
            if item == 'u':
                bus_u_list = []
                if channels[item] == 'all':                
                    flag, string = 2,'NUMBER'
                    ierr, iarray = psspy.abusint(-1, flag, string)
                buses = {}
                for item in iarray[0]:
                    bus_id = 'bus_{:d}'.format(item)
                    u = np.array(chnf.get_data()[2][name2chan(chnf,'VOLT', item)])
                    buses.update({bus_id:{'u':{'data':u,'units':'pu'}}})
                    bus_u_list += [bus_id]                  
                buses.update({'bus_u_list':bus_u_list})
                
                   
#            # ANG
#            if item == 'phiu':
#                bus_u_list = []
#                if channels[item] == 'all':                
#                    flag, string = 2,'NUMBER'
#                    ierr, iarray = psspy.abusint(-1, flag, string)
#                buses = {}
#                for item in iarray[0]:
#                    bus_id = 'bus_{:d}'.format(item)
#                    phiu = np.array(chnf.get_data()[2][name2chan(chnf,'ANGLE', item)])
#                    buses.update({bus_id:{'phiu':{'data':phiu,'units':'pu'}}})
#                    bus_u_list += [bus_id]                  
#                buses.update({'bus_u_list':bus_u_list})
                    
            # SPD
            if item == 'speed':
                sym_speed_list = []
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.amachint(-1, flag, string)   
                for item in iarray[0]:
                    sym_id = 'sym_{:d}'.format(item)
                    sym_speed_list += [sym_id]
                    speed = np.array(chnf.get_data()[2][name2chan(chnf,'SPD', item)])
                    if not syms.has_key(sym_id):
                        syms.update({sym_id:{}})
                    syms[sym_id].update({'speed':{'data':speed,'units':'pu'}})
#                    syms.update({'sym_speed_list':sym_speed_list})


            # PGEN
            if item == 'p_gen':
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.amachint(-1, flag, string)   
                for item in iarray[0]:
                    sym_id = 'sym_{:d}'.format(item)
                    p_gen = np.array(chnf.get_data()[2][name2chan(chnf,'POWR', item)])
                    if not syms.has_key(sym_id):
                        syms.update({sym_id:{}})
                    syms[sym_id].update({'p_gen':{'data':p_gen,'units':'pu-s'}})
                    
            # QGEN
            if item == 'q_gen':
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.amachint(-1, flag, string)   
                for item in iarray[0]:
                    sym_id = 'sym_{:d}'.format(item)
                    q_gen = np.array(chnf.get_data()[2][name2chan(chnf,'VARS', item)])
                    if not syms.has_key(sym_id):
                        syms.update({sym_id:{}})
                    syms[sym_id].update({'q_gen':{'data':q_gen,'units':'pu-s'}})

            # Pt   NOT IMPLEMENTED IN CHSB
            if item == 'p_t':
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.amachint(-1, flag, string)   
                for item in iarray[0]:
                    sym_id = 'sym_{:d}'.format(item)
                    p_t = np.array(chnf.get_data()[2][name2chan(chnf,'PMECH', item)])
                    if not syms.has_key(sym_id):
                        syms.update({sym_id:{}})
                    syms[sym_id].update({'p_t':p_t})
                    
            # PLOD
            if item == 'p_load':
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.aloadint(sid, flag, string) 
                for item in iarray[0]:
                    load_id = 'load_{:d}'.format(item)
                    p_load = np.array(chnf.get_data()[2][name2chan(chnf,'PLOD', item)])
                    if not loads.has_key(load_id):
                        loads.update({load_id:{}})
                    loads[load_id].update({'p_load':{'data':p_load,'units':'pu-s'}})

        results_dict['bus'].update(buses)             
        results_dict['sym'].update(syms)  
        results_dict['load'].update(loads)  
        results_dict['syms'] =  sym_speed_list                            
                
        self.results_dict = results_dict
        

def outfile2dict(out_file):        
    '''Converts PSS/E .out file to python dictionary
 
    example:
    
        {'sys':{
                'time':np.array([...])},
         'bus':{
                'bus_1':{
                         'u':np.array([...]),
                         'phiu':np.array([...]),
                         'fehz':np.array([...])},
                'bus_2':{
                         'u':np.array([...]),
                         'phiu':np.array([...]),
                         'fehz':np.array([...])}},         
         'sym':{
                'gen_1':{'bus_id':'bus_1'
                         'p':np.array([...]),
                         'q':np.array([...]),
                         'speed':np.array([...]),
                         've':np.array([...]),
                         'phi':np.array([...])}},
         'load':{
                 'load_1':{'bus_id':'bus_2'
                           'p':np.array([...]),
                           'q':np.array([...])}}
        }
        
        
        bus_1':{'speed':np.array([...]),{'volt':np.array([...])}},
         'bus_2':{{'volt':np.array([...])}}}              
    '''
    
#        vip_buses = self.vip_buses
#        
#        self.var_list =      [('volt','VOLT',vip_buses), ('speed','SPD',vip_buses), ('p_gen','POWR',vip_buses),
#         ('q_gen','VARS',vip_buses), ('freq','FREQ',vip_buses)]


    pssedir = r'C:\Program Files\PTI\PSSE33'    
    pssbindir  = os.path.join(pssedir,'PSSBIN')
    
    # Check if running from Python Interpreter
    exename = sys.executable
    p, nx   = os.path.split(exename)
    nx      = nx.lower()
    if nx in ['python.exe', 'pythonw.exe']:
        os.environ['PATH'] = pssbindir + ';' + os.environ['PATH']
        sys.path.insert(0,pssbindir)
        
    import dyntools
    chnf = dyntools.CHNF(out_file)

    t = np.array(chnf.get_data()[2]['time'])

    results_dict = {'sys':{'time':np.array(np.array(chnf.get_data()[2]['time']))},
                    'syms':[],
                    'loads':[],
                    'bus':{},
                    'sym':{},
                    'load':{},
                    'line':{},}
    channels = {}
    syms = {}
    loads = {}
    
    for item in channels:
   
        # VOLT
        if item == 'u':
            bus_u_list = []
#            if channels[item] == 'all':                
#                flag, string = 2,'NUMBER'
#                ierr, iarray = psspy.abusint(-1, flag, string)
            buses = {}
            for item in iarray[0]:
                bus_id = 'bus_{:d}'.format(item)
                u = np.array(chnf.get_data()[2][name2chan(chnf,'VOLT', item)])
                buses.update({bus_id:{'u':{'data':u,'units':'pu'}}})
                bus_u_list += [bus_id]                  
            buses.update({'bus_u_list':bus_u_list})
            
               
#            # ANG
#            if item == 'phiu':
#                bus_u_list = []
#                if channels[item] == 'all':                
#                    flag, string = 2,'NUMBER'
#                    ierr, iarray = psspy.abusint(-1, flag, string)
#                buses = {}
#                for item in iarray[0]:
#                    bus_id = 'bus_{:d}'.format(item)
#                    phiu = np.array(chnf.get_data()[2][name2chan(chnf,'ANGLE', item)])
#                    buses.update({bus_id:{'phiu':{'data':phiu,'units':'pu'}}})
#                    bus_u_list += [bus_id]                  
#                buses.update({'bus_u_list':bus_u_list})
                
        # SPD
        if item == 'speed':
            sym_speed_list = []
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)   
            for item in iarray[0]:
                sym_id = 'sym_{:d}'.format(item)
                sym_speed_list += [sym_id]
                speed = np.array(chnf.get_data()[2][name2chan(chnf,'SPD', item)])
                if not syms.has_key(sym_id):
                    syms.update({sym_id:{}})
                syms[sym_id].update({'speed':{'data':speed,'units':'pu'}})
#                    syms.update({'sym_speed_list':sym_speed_list})


        # PGEN
        if item == 'p_gen':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)   
            for item in iarray[0]:
                sym_id = 'sym_{:d}'.format(item)
                p_gen = np.array(chnf.get_data()[2][name2chan(chnf,'POWR', item)])
                if not syms.has_key(sym_id):
                    syms.update({sym_id:{}})
                syms[sym_id].update({'p_gen':{'data':p_gen,'units':'pu-s'}})
                
        # QGEN
        if item == 'q_gen':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)   
            for item in iarray[0]:
                sym_id = 'sym_{:d}'.format(item)
                q_gen = np.array(chnf.get_data()[2][name2chan(chnf,'VARS', item)])
                if not syms.has_key(sym_id):
                    syms.update({sym_id:{}})
                syms[sym_id].update({'q_gen':{'data':q_gen,'units':'pu-s'}})

        # Pt   NOT IMPLEMENTED IN CHSB
        if item == 'p_t':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.amachint(-1, flag, string)   
            for item in iarray[0]:
                sym_id = 'sym_{:d}'.format(item)
                p_t = np.array(chnf.get_data()[2][name2chan(chnf,'PMECH', item)])
                if not syms.has_key(sym_id):
                    syms.update({sym_id:{}})
                syms[sym_id].update({'p_t':p_t})
                
        # PLOD
        if item == 'p_load':
            if channels[item] == 'all':                
                sid,flag, string = -1,4,'NUMBER'
                ierr, iarray = psspy.aloadint(sid, flag, string) 
            for item in iarray[0]:
                load_id = 'load_{:d}'.format(item)
                p_load = np.array(chnf.get_data()[2][name2chan(chnf,'PLOD', item)])
                if not loads.has_key(load_id):
                    loads.update({load_id:{}})
                loads[load_id].update({'p_load':{'data':p_load,'units':'pu-s'}})

#    results_dict['bus'].update(buses)             
#    results_dict['sym'].update(syms)  
#    results_dict['load'].update(loads)  
#    results_dict['syms'] =  sym_speed_list   


#    results_dict = {'sys':{'time':np.array(np.array(chnf.get_data()[2]['time']))},
#                    'syms':[],
#                    'loads':[],
#                    'bus':{},
#                    'sym':{},
#                    'load':{}}
#                    
                    
    values = chnf.chanid.values()[0]
    variable_dict = {
                     'ANGL':{'common_name':'phiu', 'element':'sym', 'units':'deg', 'tex':'$\sf \theta_{xxx}$'},
                     'POWR':{'common_name':'p_gen', 'element':'sym', 'units':'pu', 'tex':'$\sf p_{gxxx}$'},
                     'VARS':{'common_name':'q_gen', 'element':'sym', 'units':'pu', 'tex':'$\sf q_{qxxx}$'},
                     'ETRM':{'common_name':'v_t', 'element':'sym', 'units':'pu', 'tex':'$\sf v_{txxx}$'},
                     'EFD':{'common_name':'v_e', 'element':'sym', 'units':'pu', 'tex':'$\sf v_{fxxx}$'},
                     'PMEC':{'common_name':'p_t', 'element':'sym', 'units':'pu', 'tex':'$\sf p_{mxxx}$'},
                     'SPD': {'common_name':'speed', 'element':'sym', 'units':'pu', 'tex':'$\sf \omega_{xxx}$'},
                     'PLOD': {'common_name':'p_load', 'element':'load', 'units':'pu', 'tex':'$\sf p_{lxxx}$'},
                     'QLOD': {'common_name':'q_load', 'element':'load', 'units':'pu', 'tex':'$\sf q_{lxxx}$'},
                     'FREQ': {'common_name':'freq', 'element':'bus', 'units':'pu', 'tex':'$\sf f_{xxx}$'},
                     'VOLT': {'common_name':'u', 'element':'bus', 'units':'pu', 'tex':'$\sf u_{xxx}$'},
                     'POWR_FLOW': {'common_name':'p_flow', 'element':'line', 'units':'pu', 'tex':'$\sf p_{xxx}$'},
                     'VARS_FLOW': {'common_name':'q_flow', 'element':'line', 'units':'pu', 'tex':'$\sf q_{xxx}$'}
                    }
                    
    for item in values:
        value = values[item] 
        variable = (values[item]).split()[0]
#        print(value)
        if item != 'time':

            if value.split(']')[-1]  and not ('TO' in value):
                bus = (values[item]).split()[1].split('[')[0]
                id = (values[item]).split(']')[-1]
                if id == '1':                
                    bus_id = bus
                else:          
                    bus_id = bus + '_' + id 
                if not results_dict[variable_dict[variable]['element']].has_key(bus_id):
                    results_dict[variable_dict[variable]['element']].update({bus_id:{}})
                if not results_dict[variable_dict[variable]['element']][bus_id].has_key(variable_dict[variable]['common_name']):
                    results_dict[variable_dict[variable]['element']][bus_id].update({variable_dict[variable]['common_name']:{}})
                results_dict[variable_dict[variable]['element']][bus_id][variable_dict[variable]['common_name']]['data'] = np.array(chnf.chandata.values()[0][item])  
                results_dict[variable_dict[variable]['element']][bus_id][variable_dict[variable]['common_name']]['units'] = variable_dict[variable]['units']
                results_dict[variable_dict[variable]['element']][bus_id][variable_dict[variable]['common_name']]['tex'] = variable_dict[variable]['tex']
                
                
            if value.split(']')[-1] == ''  and not ('TO' in value):
                bus = value.split()[1].split('[')[0]
                if not results_dict[variable_dict[variable]['element']].has_key(bus):
                    results_dict[variable_dict[variable]['element']].update({bus:{}})
                if not results_dict[variable_dict[variable]['element']][bus].has_key(variable_dict[variable]['common_name']):
                    results_dict[variable_dict[variable]['element']][bus].update({variable_dict[variable]['common_name']:{}})
                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['data'] = np.array(chnf.chandata.values()[0][item])  
                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['units'] = variable_dict[variable]['units']
                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['tex'] = variable_dict[variable]['tex']
                
#            if 'TO' in value:
#                bus_i = value.split()[1]
#                bus_j = value.split()[3]
#                ckt = value.split()[5]
#                bus_id = bus_i + '_' + bus_j + '_' + ckt 
#                if not results_dict[variable_dict[variable]['element']].has_key(bus):
#                    results_dict[variable_dict[variable]['element']].update({bus:{}})
#                if not results_dict[variable_dict[variable]['element']][bus].has_key(variable_dict[variable]['common_name']):
#                    results_dict[variable_dict[variable]['element']][bus].update({variable_dict[variable]['common_name']:{}})
#                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['data'] = np.array(chnf.chandata.values()[0][item])  
#                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['units'] = variable_dict[variable]['units']
#                results_dict[variable_dict[variable]['element']][bus][variable_dict[variable]['common_name']]['tex'] = variable_dict[variable]['tex']
                
        if item == 'time':
            results_dict['sys']['time']  = np.array(np.array(chnf.get_data()[2]['time']))
            
                

#                                   
            
    return results_dict


def dict2hdf5(dictionary,hdf5_file):
    
    import hickle
    hickle.dump(dictionary, hdf5_file)
    
def dir2dict(directory):
    
    dir_list = os.listdir(directory)
    tests_dict = {}
    for item in dir_list:
        fileName, fileExtension = os.path.splitext(item)

        if fileExtension == '.out':
            print(fileName) 
            results_dict = outfile2dict(os.path.join(directory,item)) 
            tests_dict.update({fileName:results_dict})


    return tests_dict
        
def to_file(file_name, model, IBUS, ID):
     f = open(file_name + '.rst', 'w')
     f.write(toReST)
      
     
    
def device_writer(model, IBUS, ID, models_dict):
   
    Models = models_dict
    NI, NC, NS, NV = 0, 0, 0, 0
    toPSSE=''
    if Models[model].has_key('type'):
        if Models[model]['type']=='USRMDL':
            '''
                BUSID 'USRMDL' IM 'model name' IC IT NI NC NS NV data list
                    Where:
                        BUSID and IM are the external bus number and the machine id of the machine that is being
                        subject to test.
                        IC Is the user-model type code, which in this case would be 505 since the model is classified
                        as a "Machine Other model".
                        IT determines the placement in CONET. In this case, IT is 0 since the model does not need
                        to be called during dynamic simulation network solution.
                        NI Is the number of ICONs used by the model (NI = 2).
                        NC Is the number of CONs used by the model (NC = 6).
                        NS Is the number of STATEs used by the model. (NS = 0).
                        NV Is the number of VARs used by the model. (NV = 2).
            '''
            BUSID = IBUS
            IM  = ID
            IT = Models[model]['IT']
            IC = Models[model]['type_code']
            if Models[model].has_key('ICONs'): 
                NI=len(Models[model]['ICONs'])
            else:
                NI=Models[model]['NI']
                    
            if Models[model].has_key('CONs'):
                NC=len(Models[model]['CONs'])
            else:
                NC=Models[model]['NC']
                
            if Models[model].has_key('STATEs'):
                NS=len(Models[model]['STATEs'])

            else: 
                NS= Models[model]['NS']
                
            if Models[model].has_key('VARs'):
                NV=len(Models[model]['VARs'])   
            else: 
                NV= Models[model]['NV']                
            toPSSE = " %d 'USRMDL'  %s  '%s'   %d %d %d %d %d %d " %(IBUS, ID,  model, IC, IT, NI, NC, NS, NV)

    else:
        toPSSE = "{:d}  '{:s}' '{:s}'  ".format(IBUS,   model, str(ID))
        

                                                     
    
    toReST = ''


    
    if Models[model].has_key('ICONs'):
        
        toReST+=    'Integer Constants\n'
        toReST+=    len(toReST.split('\n')[-2])*'-' + '\n'
                                           
        toReST+=    '\n'                    
        toReST+=    '====== ==== ====== ===========================================================================\n' 
        toReST+=    'ICONS   #   Value  Description                             \n' 
        toReST+=    '====== ==== ====== ===========================================================================\n'
        ICONS=Models[model]['ICONs']
        it = 0
        it_row = 0
        for item in ICONS:
            it+=1
            toReST+='%5s %4d %6d   %s \n' %(item.keys()[0],it, item[item.keys()[0]]['typical'], item[item.keys()[0]]['Description'])
            it_row+=1
            if it_row>5:
                it_row=0
                toPSSE+=' \n'
            toPSSE+= '%4d  ' %(item[item.keys()[0]]['typical'])
        toReST+=    '====== ==== ====== ===========================================================================\n'
        toReST+=    '\n'
        toReST+=    '\n'

    if Models[model].has_key('CONs'):

        toReST+=    'Constants\n'
        toReST+=    len(toReST.split('\n')[-2])*'-' + '\n'
        toReST+=    '\n'
        toReST+=    '====== ==== ========= ===========================================================================\n'
        toReST+=    'CONS    #   Value     Description                             \n' 
        toReST+=    '====== ==== ========= ===========================================================================\n'
        CONS=Models[model]['CONs']
        it = 0
        it_row = 0
        for item in CONS:
            it+=1
            toReST+='%5s %4d %10.3f %s \n' %(item.keys()[0],it, item[item.keys()[0]]['typical'], item[item.keys()[0]]['Description'])
            it_row+=1
            if it_row>5:
                it_row=0
                toPSSE+=' \n'
            toPSSE+= '%4.3f  ' %(item[item.keys()[0]]['typical'])
        toReST+=    '====== ==== ========= ===========================================================================\n'
        toReST+=    '\n'
        toReST+=    '\n'


    if Models[model].has_key('STATEs'):
        toReST+=    'States\n'
        toReST+=    len(toReST.split('\n')[-2])*'-' + '\n'
        toReST+=    '\n'
        toReST+=    '====== ==== ========= ===========================================================================\n'
        toReST+=    'STATEs  #   Value     Description                             \n' 
        toReST+=    '====== ==== ========= ===========================================================================\n'
        STATEs=Models[model]['STATEs']
        for item in STATEs:
            toReST+='%5s %4s %10.3f %s \n' %(item.keys()[0],' ', 0.0, item[item.keys()[0]][u'Description']) 
        toReST+=    '====== ==== ========= ===========================================================================\n'

    toPSSE+='/ \n'


    return toReST, toPSSE



def test_118():
    
    tests_obj = tests()
    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\tests\pvsync\ieee118pvsync_10\ieee118_pvsinc_tests.yaml'
    tests_obj.set_up(yaml_file)
    tests_results = tests_obj.run_tests()

    return tests_results




def test_device_writer(case_dir, gen_types_file,file_name_dyr,file_name_rst):
    

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

def test_dev_wrtie():
    
    file_name_rst = 'ieee118_pvsync_4_100mva'
    file_name_dyr = 'ieee118_pvsync_4_100mva'
    case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/data/ieee118_pvsync/ieee118pvsync_1pv'
    gen_types_file = 'tgov_hygov_pvsync_4.tsv'
 
    file_name_rst = 'ieee118_pvsync_1_100mva'
    file_name_dyr = 'ieee118_pvsync_1_100mva'
    case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/data/ieee118_pvsync/ieee118pvsync_1pv'
    gen_types_file = 'tgov_hygov_pvsync_1.tsv'
    
    test_device_writer(case_dir, gen_types_file, file_name_dyr, file_name_rst)
    
from subprocess import *
import re

class InteractiveCommand:
	def __init__(self, process, prompt):
		self.process = process
		self.prompt  = prompt
		self.output  = ""
		self.wait_for_prompt()

	def wait_for_prompt(self):
		while not self.prompt.search(self.output):
			c = self.process.stdout.read(1)
			if len(self.output) == len(self.output + c):
				break
			self.output += c

		tmp = self.output

		self.output = ""
		return tmp

	def wait_for_prompt2(self,prompt2):
		while not prompt2.search(self.output):
			c = self.process.stdout.read(1)
			if len(self.output) == len(self.output + c):
				break
			self.output += c
		tmp = self.output

		self.output = ""
		return tmp

	def enter(self):
		self.process.stdin.write("\n")


	def command(self, command):
		self.process.stdin.write(command +"\n")
		print( command +"\n" )
		return self.wait_for_prompt()
		
	def command2(self,command,prompt2):

         print( command +"\n" )
         self.process.stdin.write(command +"\n")
         return self.wait_for_prompt2(prompt2)

def lsa2dat(input,output):
	promptDOSPUNTOS = re.compile(': ', re.M)
	promptFLECHA = re.compile('> ', re.M)

	p      = Popen( ["C:\Program Files\PTI\PSSE33\PSSBIN\LSYSAN33.exe"], stdin=PIPE, stdout=PIPE )
	prompt = re.compile('ACTIVITY\? ', re.M)
	cmd    = InteractiveCommand(p, prompt)
	cmd.command2("BCAS",promptDOSPUNTOS)
	cmd.command2(input,prompt)
	cmd.command2("MLIS",promptFLECHA)
	cmd.command2("2",promptDOSPUNTOS)
	cmd.command2(output,promptDOSPUNTOS)
	cmd.command("")
	cmd.command("STOP")

def lsa2dat_zeroes(input,output):
    promptDOSPUNTOS = re.compile(': ', re.M)
    promptFLECHA = re.compile('> ', re.M)
    
    p      = Popen( ["C:\Program Files\PTI\PSSE33\PSSBIN\LSYSAN33.exe"], stdin=PIPE, stdout=PIPE )
    prompt = re.compile('ACTIVITY\? ', re.M)
    cmd    = InteractiveCommand(p, prompt)
    cmd.command2("BCAS",promptDOSPUNTOS)
    cmd.command2(input,promptFLECHA)
    cmd.command2("1",prompt)
    cmd.command2("MLIS",promptFLECHA)
    cmd.command2("2",promptDOSPUNTOS)
    cmd.command2(output,promptDOSPUNTOS)
    cmd.command("")
    cmd.command("STOP")

   
if __name__ == "__main__":

#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_10\results\ieee12g_10_pvs.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_10\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)


#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_10\results\ieee12g_10_pv.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_10\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)
#    
#
    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_30\results\ieee12g_30_pv.hdf5"""  
    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_30\results"""
    test_dict_1 = dir2dict(directory)
    dict2hdf5(test_dict_1,hdf5_file)

#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_50\results\ieee12g_50_pv.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pv_50\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)
#    
#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_30\results\ieee12g_30_pvs.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_30\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)
#    fig_pvs_p = plt.figure()
    
#    fig_pvs_p.set_size_inches(10.0,10.0)
#    
#    ax_pvs_p_gen_trip_9  = fig_pvs_p.add_subplot(4,1,1)
#    ax_pvs_p_gen_trip_10 = fig_pvs_p.add_subplot(4,1,2)
#    ax_pvs_p_gen_trip_11 = fig_pvs_p.add_subplot(4,1,3)
#    ax_pvs_p_gen_trip_12 = fig_pvs_p.add_subplot(4,1,4)
#    
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_9.plot(test_dict_1['ieee12g_30_pvs_gen_trip_9']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_9']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_9.plot(test_dict_1['ieee12g_30_pvs_gen_trip_9']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_9']['sym'][str(it_gen)]['q_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_10.plot(test_dict_1['ieee12g_30_pvs_gen_trip_10']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_10']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_10.plot(test_dict_1['ieee12g_30_pvs_gen_trip_10']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_10']['sym'][str(it_gen)]['q_gen']['data'])
#
#   
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_11.plot(test_dict_1['ieee12g_30_pvs_gen_trip_11']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_11']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_11.plot(test_dict_1['ieee12g_30_pvs_gen_trip_11']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_11']['sym'][str(it_gen)]['q_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_12.plot(test_dict_1['ieee12g_30_pvs_gen_trip_12']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_12']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,19):
#        ax_pvs_p_gen_trip_12.plot(test_dict_1['ieee12g_30_pvs_gen_trip_12']['sys']['time'],test_dict_1['ieee12g_30_pvs_gen_trip_12']['sym'][str(it_gen)]['q_gen']['data'])
#                    
#    fig_pvs_p.show()
#
#    
#    
#
##
##
#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_50\results\ieee12g_50_pvs.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_50\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)
##
#    fig_pvs_p = plt.figure()
#    
#    fig_pvs_p.set_size_inches(10.0,10.0)
#    
#    ax_pvs_p_gen_trip_9  = fig_pvs_p.add_subplot(4,1,1)
#    ax_pvs_p_gen_trip_10 = fig_pvs_p.add_subplot(4,1,2)
#    ax_pvs_p_gen_trip_11 = fig_pvs_p.add_subplot(4,1,3)
#    ax_pvs_p_gen_trip_12 = fig_pvs_p.add_subplot(4,1,4)
#    
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_9.plot(test_dict_1['ieee12g_50_pvs_gen_trip_9']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_9']['sym'][str(it_gen)]['speed']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_9.plot(test_dict_1['ieee12g_50_pvs_gen_trip_9']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_9']['sym'][str(it_gen)]['q_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_10.plot(test_dict_1['ieee12g_50_pvs_gen_trip_10']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_10']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_10.plot(test_dict_1['ieee12g_50_pvs_gen_trip_10']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_10']['sym'][str(it_gen)]['q_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_11.plot(test_dict_1['ieee12g_50_pvs_gen_trip_11']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_11']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_11.plot(test_dict_1['ieee12g_50_pvs_gen_trip_11']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_11']['sym'][str(it_gen)]['q_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_12.plot(test_dict_1['ieee12g_50_pvs_gen_trip_12']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_12']['sym'][str(it_gen)]['p_gen']['data'])
#
#    for it_gen in range(13,21):
#        ax_pvs_p_gen_trip_12.plot(test_dict_1['ieee12g_50_pvs_gen_trip_12']['sys']['time'],test_dict_1['ieee12g_50_pvs_gen_trip_12']['sym'][str(it_gen)]['q_gen']['data'])
#
#     
#   
#    fig_pvs_p.show()

    
#    
#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_base\results\ieee12g_base_pvs.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_base\results"""
#    test_dict_2 = dir2dict(directory)
#    dict2hdf5(test_dict_2,hdf5_file)

#
#    in_file  = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_base\results\ieee12g_base_small_signal.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_base\results\ieee12g_base_small_signal.dat"""
#    lsa2dat(in_file,out_file)
#    
#    in_file  = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_10\results\ieee12g_10_pvs_small_signal.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_10\results\ieee12g_10_pvs_small_signal.dat"""
#    lsa2dat_zeroes(in_file,out_file)
#
#    in_file  = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_30\results\ieee12g_30_pvs_small_signal.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_30\results\ieee12g_30_pvs_small_signal.dat"""
#    lsa2dat_zeroes(in_file,out_file)
#    
#    in_file  = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_50\results\ieee12g_50_pvs_small_signal.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\code\ieee12g_pvsync_50\results\ieee12g_50_pvs_small_signal.dat"""
#    lsa2dat_zeroes(in_file,out_file)
#  

#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\ieee118_pvsync\code\ieee118_pvsync_base\results\ieee118_base_pvs.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\ieee118_pvsync\code\ieee118_pvsync_base\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)
#    
    
#    hdf5_file = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\ieee118_pvsync\code\ieee118_pvsync_10\results\ieee118_pvs_10.hdf5"""  
#    directory = r"""E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\ieee118_pvsync\code\ieee118_pvsync_10\results"""
#    test_dict_1 = dir2dict(directory)
#    dict2hdf5(test_dict_1,hdf5_file)    
#    in_file  = r"""E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\results\small_signal_channels_118.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\results\small_signal_channels_118.dat"""
#    in_file = r"""E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\results\small_signal_channels_no_sta_118.lsa"""
#    out_file = r"""E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\results\small_signal_channels_no_sta_118.dat"""
#    lsa2dat(in_file,out_file)