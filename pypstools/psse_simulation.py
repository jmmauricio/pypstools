""" Tools for simulation with PSS/E.

(c) 2015 Juan Manuel Mauricio
"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg

import analysis
import hickle


# -*- coding: cp1252 -*-
#[dyntools_demo.py]  09/22/100    Demo for using functions from dyntools module
# ====================================================================================================
'''
'dyntools' module provide access to data in PSS(R)E Dynamic Simulation Channel Output file.


'''
import yaml 
import os, sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
#from pypstools.tools import name2chan
#from pypstools.publisher.plot_tools import g_colors
#import pypstools.publisher.rst_basic as rst
import h5py

def psse(case_name,raw_dyr_dir,casedir,vip_buses, psse_version = 'PSSE33', channels_yaml = 'channels.yaml' ):
    # =============================================================================================
    # Get installed location of latest PSS(R)E version

    if psse_version == 'PSSE33':
        pssedir = r'C:\Program Files\PTI\PSSE33'
    if psse_version == 'PSSEUniversity33':        
        pssedir = r'C:\Program Files\PTI\PSSEUniversity33'
    
    # =============================================================================================
    # Files Used
    
    print(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(),'..','..'))  
    pssbindir  = os.path.join(pssedir,'PSSBIN')

    #casedir=r'E:\jmmauricio\Documents\public\jmmauricio6\RESEARCH\psse_models\test\pvsyn1\data\inf_pvsync'
    sys.path.append(os.path.join(os.getcwd(),'..'))
    libraryname = os.path.join(casedir,'dsusr.dll')
    print(libraryname)
    rawfile    = os.path.join(raw_dyr_dir,case_name + '.raw')
    dyrfile    = os.path.join(raw_dyr_dir,case_name + '.dyr')
    dyafile_avr= os.path.join(raw_dyr_dir,case_name + '_avr.dya')
    dyafile_gov= os.path.join(raw_dyr_dir,case_name + '_gov.dya')
    dyafile_pss= os.path.join(raw_dyr_dir,case_name + '_pss.dya')
    xsfile = os.path.join(casedir,case_name + '_xs.txt')
    savfile    = os.path.join(casedir,case_name + '.sav')
    savdynfile = os.path.join(casedir,case_name + '_dyn.sav')
    snpfile    = os.path.join(casedir,case_name + '.snp')
    outfile1   = os.path.join(casedir,case_name + '.out')
    outfile2   = os.path.join(casedir,case_name + '.out')
    outfile3   = os.path.join(casedir,case_name + '.out')
    prgfile    = os.path.join(casedir,'dyntools_demo_progress.txt')
    chnffile = os.path.join(casedir,case_name + '.pkl') 
    lsa_file  = os.path.join(casedir,case_name + '.lsa')
    lsa_dat  = os.path.join(casedir,case_name + '.dat')
    ltifile = os.path.join(casedir,'sys_abcd_f12.pkl')
    config_file = 'configuration.pkl'
    tests_config_file = os.path.join(casedir,'tests.pkl')
    tests_out = os.path.join(casedir,'tests_out.hdf5')
    # =============================================================================================
    
    
    # =============================================================================================
    # Check if running from Python Interpreter
    exename = sys.executable
    p, nx   = os.path.split(exename)
    nx      = nx.lower()
    if nx in ['python.exe', 'pythonw.exe']:
        os.environ['PATH'] = pssbindir + ';' + os.environ['PATH']
        sys.path.insert(0,pssbindir)
    
    
    import dyntools
    
    import redirect
    redirect.psse2py()    
    import psspy
    _i = psspy._i
    _f = psspy._f
    
    import psspy
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
    
    
    # se cargan los datos dinamicos
    psspy.dyre_new([1,1,1,1],dyrfile,"","","")
      
    
    channels_str = open(channels_yaml,'r').read()
    channels = yaml.load(channels_str)

    sid = 0    
    all_buses = 0
        
    for item in channels:
        print(item)

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
            
            
            
    #    STATUS(5) = 1 ANGLE, machine relative rotor angle (degrees).
    
    
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 4 ETERM, machine terminal voltage (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 5 EFD, generator main field voltage (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 6 PMECH, turbine mechanical power (pu on MBASE).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 7 SPEED, machine speed deviation from nominal (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 8 XADIFD, machine field current (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 9 ECOMP, voltage regulator compensated voltage (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 10 VOTHSG, stabilizer output signal (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 11 VREF, voltage regulator voltage setpoint (pu).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 12 BSFREQ, bus pu frequency deviations.
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 13 VOLT, bus pu voltages (complex).
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 14 voltage and angle
    #psspy.chsb(0,all_buses,[-1,-1,-1,1,1,0])  # STATUS(5) = 15 flow (P).
    #STATUS(5) = 16 flow (P and Q).
    #STATUS(5) = 17 flow (MVA).
    #STATUS(5) = 18 apparent impedance (R and X).
    #STATUS(5) = 21 ITERM.
    #STATUS(5) = 22 machine apparent impedance
    #STATUS(5) = 23 VUEL, minimum excitation limiter output signal (pu).
    #STATUS(5) = 24 VOEL, maximum excitation limiter output signal (pu).
    #STATUS(5) = 25 PLOAD.
    #STATUS(5) = 26 QLOAD.
    #STATUS(5) = 27 GREF, turbine governor reference.
    #STATUS(5) = 28 LCREF, turbine load control reference.
    #STATUS(5) = 29 WVLCTY, wind velocity (m/s).
    #STATUS(5) = 30 WTRBSP, wind turbine rotor speed deviation (pu).
    #STATUS(5) = 31 WPITCH, pitch angle (degrees).
    #STATUS(5) = 32 WAEROT, aerodynamic torque (pu on MBASE).
    #STATUS(5) = 33 WROTRV, rotor voltage (pu on MBASE).
    #STATUS(5) = 34 WROTRI, rotor current (pu on MBASE).
    #STATUS(5) = 35 WPCMND, active power command from wind control
    #(pu on MBASE).
    #STATUS(5) = 36 WQCMND, reactive power command from wind control
    #(pu on MBASE).
    #STATUS(5) = 37 WAUXSG, output of wind auxiliary control (pu on
    #MBASE).


    #ierr, L_vsc_1 = psspy.mdlind(7, '1', 'GEN', 'VAR')
    #ierr, L_vsc_2 = psspy.mdlind(8, '1', 'GEN', 'VAR')
    #        
    #psspy.var_channel([-1,L_vsc_1],)
    #psspy.var_channel([-1,L_vsc_1+1],)
    #psspy.var_channel([-1,L_vsc_2],)
    #psspy.var_channel([-1,L_vsc_2+1],)
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




class test:
    '''Class to simulate tests with PSS/E


    '''
    
    def __init__(self, psspy,dyntools,savdynfile,snpfile):
        self.psspy = psspy
        self.dyntools =dyntools
        self.savdynfile = savdynfile
        self.snpfile = snpfile
        self.channels_yaml = 'channels.yaml'
        self.t_pert = 1.0 # default time for perturbation
        self.t_end = 20.0 # default time to end the simulation
        self.dt = 0.001   # default integration time step
        self.decimation_file = 25
        self.decimation_progress = 1000

    def run(self, outfile):
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

	# for v_ref changes
        if self.data['test_type']=='v_ref_change':
            ibus = self.data['gen_bus']
            id   = self.data['gen_id']
            newval = self.data['change']

            ierr = psspy.increment_vref(ibus, id, newval)

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
        
        channels_str = open(self.channels_yaml,'r').read()
        channels = yaml.load(channels_str)

        chnf = self.dyntools.CHNF(self.outfile)

        t = np.array(chnf.get_data()[2]['time'])
        self.t = t

        results_dict = {'sys':{'time':np.array(np.array(chnf.get_data()[2]['time']))},
                        'bus':{},
                        'sym':{}}

        syms = {}
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
                    buses.update({bus_id:{'u':u}})
                    bus_u_list += [bus_id]                  
                buses.update({'bus_u_list':bus_u_list})
                
                   
            # ANG
            if item == 'phiu':
                if channels[item] == 'all':                
                    sid,flag, string = -1,4,'NUMBER'
                    ierr, iarray = psspy.amachint(-1, flag, string)   
                for item in iarray[0]:
                    sym_id = 'sym_{:d}'.format(item)
                    phiu = np.array(chnf.get_data()[2][name2chan(chnf,'ANGL', item)])
                    if not syms.has_key(sym_id):
                        syms.update({sym_id:{}})
                    syms[sym_id].update({'phiu':phiu})
                    
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
                    syms[sym_id].update({'speed':speed})
                    syms.update({'sym_speed_list':sym_speed_list})

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
                    syms[sym_id].update({'p_gen':p_gen})
                    
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
                    syms[sym_id].update({'q_gen':q_gen})

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
                    


        results_dict['bus'].update(buses)             
        results_dict['sym'].update(syms)             
#    
#            # PGEN
#            if item == 'p_gen':
#                if channels[item] == 'all':                
#                    sid,flag, string = -1,4,'NUMBER'
#                    ierr, iarray = psspy.amachint(-1, flag, string)                
#                sid += 1    
#                psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
#                psspy.chsb(sid,all_buses,[-1,-1,-1,1,16,0])  # STATUS(5) = 16 flow (P and Q).
#    
#            # PLOAD
#            if item == 'p_load':
#                if channels[item] == 'all':                
#                    flag, string = 4,'NUMBER'
#                    ierr, iarray = psspy.alodbusint(-1, flag, string)              
#                sid += 1    
#                psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
#                psspy.chsb(sid,all_buses,[-1,-1,-1,1,25,0])  #STATUS(5) = 25 PLOAD.         
#    
#            # QLOAD
#            if item == 'p_load':
#                if channels[item] == 'all':                
#                    sid,flag, string = -1,4,'NUMBER'
#                    ierr, iarray = psspy.alodbusint(-1, flag, string)                 
#                sid += 1    
#                psspy.bsys(sid,0,[ 0.4, 600.],0,[],len(iarray[0]),iarray[0],0,[],0,[])           
#                psspy.chsb(sid,all_buses,[-1,-1,-1,1,26,0])  #STATUS(5) = 26 PLOAD.  
#    
#    
#    
#
#
#
#
#
#
#
#        
#        py2mat_dict = {}
#        
#        test_id = self.data['test_id']
#
#        data_dict = {}
# 
#        var_list = self.var_list 
#
#        results_dict.update({'sys':{'t':chnf.get_data()[2]['time']}})   
#        
##        for item_var,item_psse_var,item_buses in  var_list:
##            
##            if item_psse_var == 'VAR':      
##                device_name = item_var[0]
##                if not data_dict.has_key(device_name):
##                    data_dict.update({device_name:{}})                
##                item_value = np.array(chnf.get_data()[2][name2chan(chnf,item_psse_var, item_buses)])
##                data_dict[device_name].update({item_var[1]:item_value})
##                
##            if not (item_psse_var == 'SPD' or item_psse_var == 'VAR'):    
##                for item_bus in item_buses:
##                    bus_name = 'bus_{:d}'.format(item_bus) 
##                    if not data_dict.has_key(bus_name):
##                        data_dict.update({bus_name:{}})  
##                    print(item_psse_var)
##                    print(name2chan(chnf,item_psse_var, item_bus))
##                    item_value = np.array(chnf.get_data()[2][name2chan(chnf,item_psse_var, item_bus)])
##                    data_dict[bus_name].update({item_var:item_value})
##                    
##                    ierr, cmpval = self.psspy.gendat(item_bus) 
##                    if ierr == 3:
##                        item_value = np.array(chnf.get_data()[2][name2chan(chnf,item_psse_var, item_bus)])
##                        data_dict[device_name].update({item_var:item_value})
##                        
##                    bus_name = 'bus_{:d}'.format(item_bus)
##                    if not data_dict.has_key(device_name):
##                        data_dict.update({device_name:{}})
##                    ierr, cmpval = self.psspy.gendat(item_bus)
##                    print (ierr)
##                    print (cmpval)
##                    if not(ierr==3 and item_psse_var=='SPD'):
                        
                
        self.results_dict = results_dict
        
        
               
                

##  
#
#
#def dict2h5_l3(file_name, dict_in, compression="gzip"):          
#    f = h5py.File(file_name,'w')
#    
#    for test in data_dict:
##        print test
#        grp = f.create_group(test)
#        for group in data_dict[test]:
##            print group
#            sub_grp = grp.create_group(group)
#            for data in data_dict[test][group]:
#                var_name = data
#                var_values =  data_dict[test][group][data]
##                print var_name, var_values
#                sub_grp.create_dataset(var_name, data=var_values, compression=compression)
#     
#    f.close()
#
#


import xml.etree.ElementTree as ET
from StringIO import StringIO
import json



def interactive_svg(plt,svg_file,ids, curves, distance_factor=0.8):   
    
    # Apparently, this `register_namespace` method works only with
    # python 2.7 and up and is necessary to avoid garbling the XML name
    # space with ns0.
    ET.register_namespace("","http://www.w3.org/2000/svg")



    # Save SVG in a fake file object.
    f = StringIO()
    plt.savefig(f, format="svg")
    
    
    script = '''<script type="text/ecmascript">
        <![CDATA[
    
    	function init(evt)
    	{
    	    if ( window.svgDocument == null )
    	    {
    		svgDocument = evt.target.ownerDocument;
    	    }
    
    	    tooltip = svgDocument.getElementById('tooltip');
    	    tooltip_bg = svgDocument.getElementById('tooltip_bg');
    
    	}
    
    	function ShowTooltip(evt, mouseovertext)
    	{
         var distance_factor = %f;    
    	    tooltip.setAttributeNS(null,"x",distance_factor*evt.clientX+11);
    	    tooltip.setAttributeNS(null,"y",distance_factor*evt.clientY+27);
    	    tooltip.firstChild.data = mouseovertext;
    	    tooltip.setAttributeNS(null,"visibility","visible");
    
    	    length = tooltip.getComputedTextLength();
    	    tooltip_bg.setAttributeNS(null,"width",length+8);
    	    tooltip_bg.setAttributeNS(null,"x",distance_factor*evt.clientX+8);
    	    tooltip_bg.setAttributeNS(null,"y",distance_factor*evt.clientY+14);
    	    tooltip_bg.setAttributeNS(null,"visibility","visibile");
    	}
    
    	function HideTooltip(evt)
    	{
    	    tooltip.setAttributeNS(null,"visibility","hidden");
    	    tooltip_bg.setAttributeNS(null,"visibility","hidden");
    	}
    
        ]]>
      </script>''' %(distance_factor)
    
    style = """<style>
        .caption{
    	font-size: 14px;
    	font-family: Arial;
        }
        .tooltip{
    	font-size: 12px;
        }
        .tooltip_bg{
    	fill: white;
    	stroke: black;
    	stroke-width: 1;
    	opacity: 0.85;
        }
      </style>"""
      
    box = """<rect class="tooltip_bg" id="tooltip_bg"
          x="0" y="0" rx="2" ry="2"
          width="55" height="17" visibility="hidden"/>"""
          
    box_text =   """<text class="tooltip" id="tooltip"
          x="0" y="0" visibility="hidden">Tooltip</text>"""
          
          
      
    # Create XML tree from the SVG file.
    tree, xmlid = ET.XMLID(f.getvalue())
    
    tree.insert(0, ET.XML(style))
    
    
    # Insert the script and save to file.
    tree.insert(0, ET.XML(script))
    

    #tree.insert(0, ET.XML(box))
    #svg_root = xmlid['svg']
    #svg_root.set(onload="init(evt)")
    tree.set( 'onload',"init(evt)")
    
    
    for id_item, curve in zip(ids,curves.get_lines()):
        
        curve.set_gid(id_item)
        el = xmlid[id_item]
        el.set('onmousemove', "ShowTooltip(evt, '{:s}')".format(id_item))
        el.set('onmouseout', "HideTooltip(evt)")

    tree.append(ET.XML(box))
    tree.append(ET.XML(box_text))
    ET.ElementTree(tree).write(svg_file)




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










#plt.rcParams['svg.embed_char_paths'] = 'none'

def test_118():
    
    raw_dyr_dir = os.path.join(r'E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\jmm')
    casedir = os.path.join(r'E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_118\jmm')
#    raw_dyr_dir = os.path.join(r'C:\jmm')
#    casedir = os.path.join(r'C:\jmm')
    tests = [{'case_name':'ieee118_pvsyn_1','test_id':'v_ref_change_26_up_pvsyn_1', 'rst_title':'v_ref_change_26_up', 'test_type':'v_ref_change',   'gen_bus':26, 'gen_id':'1', 'change':0.1}]

    tests = [{'case_name':'ieee118_pvsyn_10','test_id':'v_ref_change_26_up_pvsyn_10', 'rst_title':'v_ref_change_26_up', 'test_type':'v_ref_change',   'gen_bus':26, 'gen_id':'1', 'change':0.1}]
#    tests = [{'case_name':'ieee118_v32_modif','test_id':'v_ref_change_26_up', 'rst_title':'v_ref_change_26_up', 'test_type':'v_ref_change',   'gen_bus':26, 'gen_id':'1', 'change':0.1}]
    tests = [{'case_name':'ieee118_pvsyn_1_100mva','test_id':'v_ref_change_26_up_pvsyn_1', 'rst_title':'v_ref_change_26_up', 'test_type':'v_ref_change',   'gen_bus':26, 'gen_id':'1', 'change':0.1}]
#    tests = [{'case_name':'ieee118_v33_modif','test_id':'v_ref_change_26_up', 'rst_title':'v_ref_change_26_up', 'test_type':'v_ref_change',   'gen_bus':26, 'gen_id':'1', 'change':0.1}]




    vip_buses = range(1,119)
    
    #case_name =  'ieee_12_g_ac78_b3' 
    #raw_dyr_dir = os.path.join(r'E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_12_generic\ieee_12_g_ac78_b3\system')
    #casedir = os.path.join(r'E:\Documents\public\jmmauricio6\INGELECTUS\ingelectus\projects\aress\code\tests\ieee_12_generic\ieee_12_g_ac78_b3\jmm')
    #tests = [{'test_id':'v_ref_change_2_up', 'rst_title':'v_ref_change_2_up', 'test_type':'v_ref_change',   'gen_bus':2, 'gen_id':'1', 'change':0.1}]
    #vip_buses = range(1,13)
    

    #
             
    ##yaml_tests = open(os.path.join(casedir,'tests.yaml'), 'r')
    ##tests = yaml.load(yaml_tests.read())
    #tests = [
    #         {'id':'p_ref_vsc_1_up_large', 'type':'p_ref',   'change_var':'Dp_1', 'change': Dp_large},
    #         {'id':'p_ref_vsc_1_down_large', 'type':'p_ref', 'change_var':'Dp_1', 'change':-Dp_large},
    #         {'id':'q_ref_vsc_1_up_large', 'type':'q_ref',   'change_var':'Dq_1', 'change': Dp_large},
    #         {'id':'q_ref_vsc_1_down_large', 'type':'q_ref', 'change_var':'Dq_1', 'change':-Dp_large},
    #         {'id':'q_ref_vsc_2_up_large', 'type':'q_ref',   'change_var':'Dq_2', 'change': Dp_large},
    #         {'id':'q_ref_vsc_2_down_large', 'type':'q_ref', 'change_var':'Dq_2', 'change':-Dp_large}]
    #         
    #
    #tests = [
    #         {'id':'p_ref_vsc_1_up_small', 'type':'p_ref',   'change_var':'Dp_1', 'change': Dp_small},
    #         {'id':'p_ref_vsc_1_down_small', 'type':'p_ref', 'change_var':'Dp_1', 'change':-Dp_small},
    #         {'id':'q_ref_vsc_1_up_small', 'type':'q_ref',   'change_var':'Dq_1', 'change': Dp_small},
    #         {'id':'q_ref_vsc_1_down_small', 'type':'q_ref', 'change_var':'Dq_1', 'change':-Dp_small},
    #         {'id':'q_ref_vsc_2_up_small', 'type':'q_ref',   'change_var':'Dq_2', 'change': Dp_small},
    #         {'id':'q_ref_vsc_2_down_small', 'type':'q_ref', 'change_var':'Dq_2', 'change':-Dp_small}]
    #
    #  
        
    #datas = np.genfromtxt(os.path.join(casedir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(0), usemask=True ) 
    #gen_thermal_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    #
    #datas = np.genfromtxt(os.path.join(casedir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(1), usemask=True ) 
    #gen_hydro_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    #
    #
    #datas = np.genfromtxt(os.path.join(casedir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(2), usemask=True ) 
    #gen_cond_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    #
    #vip_buses = list(gen_thermal_buses) + list(gen_hydro_buses) + list(gen_cond_buses)
    
    
    case_name = tests[0]['case_name']
    outfile = os.path.join(casedir,case_name + '.out')
    
          
    Dp_large = 100.0
    Dp_small = 50
     
    data_dict = {}        
    
    rst_str_tests = ''
    tests_results = {}
    
    psspy,dyntools,savdynfile,snpfile = psse(case_name,raw_dyr_dir,casedir,vip_buses)
    
    sid = -1
    ierr, buses = psspy.abusint(sid, 2, 'NUMBER')
    ierr, gen_buses = psspy.agenbusint(sid, 2, 'NUMBER')
    
    test_1 = test(psspy,dyntools,savdynfile,snpfile)
    test_1.data = tests[0]
    test_1.vip_buses = vip_buses
    test_1.run(outfile)
    test_1.run(outfile)
    test_1.outfile2dict()
    tests_results.update({tests[0]['test_id']:test_1.results_dict})
    #for item in  tests:
    #    instance_name = "test_{:s}".format(item['test_id'])
    #    print(instance_name)
    #    exec(instance_name + ' = test(psspy,dyntools,savdynfile,snpfile)')
    #    exec(instance_name + ".data = item")  
    #    exec(instance_name + ".vip_buses = vip_buses")  
    #    exec(instance_name + ".run(outfile)")
    #    exec(instance_name + ".outfile2dict()")
    #    to_exec = "tests_results.update({'" + instance_name + "':" + instance_name + ".data_dict})"
    #    print(to_exec)
    #    exec(to_exec)
    
    tests_out = os.path.join(casedir,case_name + '.hf5')
    
    hickle.dump(tests_results, tests_out)

def test_device_writer():
    
    case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'
    gen_types_file = 'tgov_hygov_pvsync_1.tsv'
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
    
    file_name_rst = 'ieee118_pvsyn_1'
    file_name_dyr = 'ieee118_pvsyn_1'
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
#    test_device_writer()
    test_118()
    




