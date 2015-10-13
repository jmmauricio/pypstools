# -*- coding: latin-1 -*-
'''

Dictionary called **Models** with PSS/E Models

The dictionary contains info about:

    * CON number (J, J+1, ..., J+NC)
    * Description of the constant
    * Typical values


'''



psse_models_dic={
'DEGOV1':{  #  ANEXO 15 MODELOS DINÁMICOS - Asep www.asep.gob.pa/electric/Anexos/ANEXO_15_expa.pdf
    'CONs':[
        {'J':{'Description':u'T1 (sec)','typical':5.0}},
        {'J+1':{'Description':u'T2 (sec)','typical':0.05}},
        {'J+2':{'Description':u'T3 (sec)','typical':0.95 }},
        {'J+3':{'Description':u'K','typical':15.0}},
        {'J+4':{'Description':u'T4 (sec)','typical':5.1}},
        {'J+5':{'Description':u'T5 (sec)','typical':0.322}},
        {'J+6':{'Description':u'T6 (sec)','typical':0.0}},
        {'J+7':{'Description':u'TD (0<TD<12*DELT) (sec)','typical':0.002}},
        {'J+8':{'Description':u'TMAX','typical':0.8}},
        {'J+9':{'Description':u'TMIN','typical':0.387}},
        {'J+10':{'Description':u'DROOP','typical':0.03}},
        {'J+11':{'Description':u'TE','typical':0.05}}
        ],
    'ICONs':[
        {'M':{'typical':0.03, 'Description':u'Droop control (0:Throttle, 1:Power)','typical':0}}
        ],
     'STATEs':[
        {'K':{'Description':u'Electric control box 1'}},
        {'K+1':{'Description':u'Electric control box 2'}},
        {'K+2':{'Description':u'Actuator 1'}},
        {'K+3':{'Description':u'Actuator 2'}},
        {'K+4':{'Description':u'Actuator 3'}},
        {'K+5':{'Description':u'Power transducer'}}
    ]},
'HYGOV':{ 
    'CONs':[
        {'J':{'Description':u'R, permanent droop','typical':5.0, 'values':[]}},
        {'J+1':{'Description':u'r, temporary droop','typical':0.05, 'values':[]}},
        {'J+2':{'Description':u'Tr (>0) governor time constant','typical':0.95, 'values':[] }},
        {'J+3':{'Description':u'Tf (>0) filter time constant','typical':15.0, 'values':[]}},
        {'J+4':{'Description':u'Tg (>0) servo time constant','typical':5.1, 'values':[]}},
        {'J+5':{'Description':u'+ VELM, gate velocity limit','typical':0.322, 'values':[]}},
        {'J+6':{'Description':u'GMAX, maximum gate limit','typical':0.0, 'values':[]}},
        {'J+7':{'Description':u'GMIN, minimum gate limit','typical':0.002, 'values':[]}},
        {'J+8':{'Description':u'TW (>0) water time constant','typical':0.8, 'values':[]}},
        {'J+9':{'Description':u'At, turbine gain','typical':0.387, 'values':[]}},
        {'J+10':{'Description':u'Dturb, turbine damping','typical':0.03, 'values':[]}},
        {'J+11':{'Description':u'qNL, no power flow','typical':0.05, 'values':[]}}
        ],
    'STATEs':[
        {'K':{'Description':u'e, filter output'}},
        {'K+1':{'Description':u'c, desired gate'}},
        {'K+2':{'Description':u'g, gate opening'}},
        {'K+3':{'Description':u'q, turbine flow'}}
        ],
    'VARs':[
        {'L':{'Description':u'Speed reference'}},
        {'L+1':{'Description':u'h, turbine head'}}
    ]},
'TGOV1':{ 
    'CONs':[
        {'J':{'Description':u'R','typical':5.0, 'values':[]}},
        {'J+1':{'Description':u'T1 (>0) (sec)','typical':0.05, 'values':[]}},
        {'J+2':{'Description':u'VMAX','typical':0.95, 'values':[] }},
        {'J+3':{'Description':u'VMIN','typical':15.0, 'values':[]}},
        {'J+4':{'Description':u'T2 (sec)','typical':5.1, 'values':[]}},
        {'J+5':{'Description':u'T3 (>0) (sec)','typical':0.322, 'values':[]}},
        {'J+6':{'Description':u'Dt','typical':0.0, 'values':[]}}
        ],
    'STATEs':[
        {'K':{'Description':u'Valve opening'}},
        {'K+1':{'Description':u'Turbine power'}}
        ],
    'VARs':[
        {'L':{'Description':'Reference'}}
    ]},
'GENSAL':{ #  ** BUS NAME  16024 PIURA 
    'CONs':[
        {'J':{'Description':u"T'do (>0) (sec)",'typical':4.0, 'values':[]  }},
        {'J+1':{'Description':u"T''do (>0) (sec)",'typical':0.035, 'values':[]  }},
        {'J+2':{'Description':u"T''qo (>0) (sec)",'typical':0.05, 'values':[]   }},
        {'J+3':{'Description':u"H, Inertia",'typical':2.0, 'values':[]  }},
        {'J+4':{'Description':u"D, Speed damping",'typical':0.0, 'values':[]  }},
        {'J+5':{'Description':u'X_d','typical':1.6, 'values':[] }},
        {'J+6':{'Description':u'X_q','typical':1.04, 'values':[]   }},
        {'J+7':{'Description':u"X'd",'typical':0.48, 'values':[]  }},
        {'J+8':{'Description':u"X''_d = X''_q",'typical':0.32, 'values':[] }},
        {'J+9':{'Description':u'X_l','typical':0.224, 'values':[] }},
        {'J+10':{'Description':u'S(1.0)','typical':0.15, 'values':[]  }},
        {'J+11':{'Description':u'S(1.2)','typical':0.4, 'values':[]   }}
        ],
     'STATEs':[
        {'K':{'Description':u"E'q", 'name':'e_1_q', 'tex':"$\sf e'_q$"}},
        {'K+1':{'Description':u'psi_k_d', 'name':'psi_k_q', 'tex':'$\sf\psi kq$'}},
        {'K+2':{'Description':u'psi"q', 'name':'psi_2_q', 'tex':'$\sf\psi''_q$'}},
        {'K+3':{'Description':u'speed (pu)', 'name':'omega', 'tex':'$\sf \omega$'}},
        {'K+4':{'Description':u'angle (radians)', 'name':'delta', 'tex':'$\sf\delta$'}}  
    ]},
'GENROU':{  
    'CONs':[
        {'J':{'Description':u"T'do (>0) (sec)",'typical':0, 'values':[]  }},
        {'J+1':{'Description':u"T''do (>0) (sec)",'typical':0 , 'values':[] }},
        {'J+2':{'Description':u"Tqo (>0) (sec)",'typical':0 , 'values':[] }},        
        {'J+3':{'Description':u"T''qo (>0) (sec)",'typical':0 , 'values':[]  }},
        {'J+4':{'Description':u"H, Inertia",'typical':0 , 'values':[] }},
        {'J+5':{'Description':u"D, Speed damping",'typical':0.0, 'values':[]  }},
        {'J+6':{'Description':u'X_d','typical':0, 'values':[] }},
        {'J+7':{'Description':u'X_q','typical':0, 'values':[]   }},
        {'J+8':{'Description':u"X'd",'typical':0, 'values':[]  }},
        {'J+9':{'Description':u"X'd",'typical':0, 'values':[]  }},
        {'J+10':{'Description':u"X''_d = X''_q",'typical':0, 'values':[] }},
        {'J+11':{'Description':u'X_l','typical':0, 'values':[] }},
        {'J+12':{'Description':u'S(1.0)','typical':0, 'values':[]  }},
        {'J+13':{'Description':u'S(1.2)','typical':0, 'values':[]   }}
        ],
     'STATEs':[
        {'K'  :{'Description':u"E'q", 'name':'e_1_q', 'tex':"$\sf e'_q$"}},
        {'K+1':{'Description':u"E'd", 'name':'e_1_d', 'tex':"$\sf e'_d$"}},
        {'K+2':{'Description':u'psi_k_d', 'name':'psi_k_d','tex':'$\sf \psi_{kd}$'}},
        {'K+3':{'Description':u'psi_k_q', 'name':'psi_k_q','tex':'$\sf \psi_{kq}$'}},
        {'K+4':{'Description':u'speed (pu)', 'name':'omega', 'tex':'$\sf \omega$'}},
        {'K+5':{'Description':u'angle (radians)', 'name':'delta', 'tex':'$\sf \delta$'}}    
    ]},
'EXAC4':{
    'CONs':[
        {'J':{'Description':u"T_r (sec)",'typical':0.02}},
        {'J+1':{'Description':u"V_imax",'typical':10.0}},
        {'J+2':{'Description':u"V_imin",'typical':-10.0}},
        {'J+3':{'Description':u"T_c",'typical':2.0}},
        {'J+4':{'Description':u"T_b (s)",'typical':10.0}},
        {'J+5':{'Description':u'K_a','typical':200}},
        {'J+6':{'Description':u'T_a','typical':0.1}},
        {'J+7':{'Description':u"V_rmax",'typical':5.0}},
        {'J+8':{'Description':u"V_rmin",'typical':0.0}},
        {'J+9':{'Description':u'K_c','typical':0.0}}
    ]},
'EXBAS':{
    'CONs':[
        {'J':{'Description':u"TR, voltage transducer time constant (sec)",'typical':0.023}},
        {'J+1':{'Description':u"KP, proportional gain",'typical':1.000}},
        {'J+2':{'Description':u"KI, integral (reset) gain",'typical':0.000}},
        {'J+3':{'Description':u"KA, gain",'typical':354.900}},
        {'J+4':{'Description':u"TA, bridge time constant (sec)",'typical':0.010}},
        {'J+5':{'Description':u"TB, lag time constant (sec)",'typical':0.043}},
        {'J+6':{'Description':u"TC, lead time constant (sec)",'typical':0.190}},
        {'J+7':{'Description':u"VRMAX, maximum control output (pu)",'typical':8.330}},
        {'J+8':{'Description':u"VRMIN, minimum control output (pu)",'typical':-6.660}},
        {'J+9':{'Description':u"KF, rate feedback gain",'typical':0.029}},
        {'J+10':{'Description':u"TF, rate feedback time constant (>0) (sec)",'typical':2.600}},
        {'J+11':{'Description':u"TF1, feedback lead time constant (sec)",'typical':0.043}},
        {'J+12':{'Description':u"TF2, feedback lag time constant (sec)",'typical':0.190}},
        {'J+13':{'Description':u"KE, exciter field proportional constant",'typical':1.000  }},
        {'J+14':{'Description':u"TE, exciter field time constant (>0) (sec)",'typical':0.300   }},
        {'J+15':{'Description':u"KC, rectifier regulation factor (pu)",'typical':0.200}},
        {'J+16':{'Description':u"KD, exciter regulation factor (pu)",'typical': 0.000}},
        {'J+17':{'Description':u"E1, exciter flux at knee of curve (pu)",'typical':6.2400}},
        {'J+18':{'Description':u"SE(E1), saturation factor at knee of curve",'typical':0.1700}},
        {'J+19':{'Description':u"E2, maximum exciter flux (pu)",'typical':8.3300}},
        {'J+20':{'Description':u"SE(E2), saturation factor at maximum exciter flux (pu)",'typical':0.1820}},
    ]},
'SEXS':{
    'CONs':[ # From PSSE example savnw.dyr
        {'J':{'Description':u"TA/TB",'typical':0.1, 'values':[]}},
        {'J+1':{'Description':u"TB (>0) (sec)",'typical':10.000, 'values':[]}},
        {'J+2':{'Description':u"K",'typical':100.0, 'values':[]}},
        {'J+3':{'Description':u"TE (sec)",'typical':0.1, 'values':[]}},
        {'J+4':{'Description':u"EMIN (pu on EFD base)",'typical':0.0, 'values':[]}},
        {'J+5':{'Description':u"EMAX (pu on EFD base)",'typical':4.0, 'values':[]}}
    ]},
'STAB1':{
    'CONs':[ # From PSSE example savnw.dyr
        {'J':{'Description':u"K/T (sec)-1",'typical':0.1, 'values':[]}},
        {'J+1':{'Description':u"T (sec) (>0)",'typical':10.000, 'values':[]}},
        {'J+2':{'Description':u"T1/T3",'typical':100.0, 'values':[]}},
        {'J+3':{'Description':u"T3 (sec) (>0)",'typical':0.1, 'values':[]}},
        {'J+4':{'Description':u"T2/T4",'typical':0.0, 'values':[]}},
        {'J+5':{'Description':u"T4 (sec) (>0)",'typical':4.0, 'values':[]}},
        {'J+6':{'Description':u"HLIM",'typical':4.0, 'values':[]}}
    ]},
'GPINVB':{ # 50 Hz system
    'type':'USRMDL', 'type_code':1, 'IT':1, 
    'ICONs':[ 
        {'M':{'Description':u'LVRT SWITCH (LVE), 0=DISABLED, 1=ENABLED (1)               ', 'typical':1}}, 
        {'M+1':{'Description':u'LVRT MODE (LVMOD), 0=NO CURRENT, 1=MAX IQ, 2=FIXED PF (1)  ', 'typical':1}}, 
        {'M+2':{'Description':u'GENERATOR TRIP FLAG, 0=NOT TRIPPED (0, DO NOT CHANGE) (0)  ', 'typical':0}}, 
        {'M+3':{'Description':u'GENERATOR STATUS FLAG, 0=ON (0, DO NOT CHANGE)        (0)  ', 'typical':0}}, 
        {'M+4':{'Description':u'COUNTER FOR PLL PHASE UNWRAPPING  (0, DO NOT CHANGE)  (0)  ', 'typical':0}}, 
        {'M+5':{'Description':u'LVRT FLAG, 0=DEACTIVATED, 1=ACTIVATED (0, DO NOT CHANGE)(0)', 'typical':0}}, 
        {'M+6':{'Description':u'POST-LVRT FLAG,1=IN POST-LVRT, 0= NOT (0, DO NOT CHANGE)(0)', 'typical':0}}, 
        {'M+7':{'Description':u'ACTIVE PWR MGMT FLAG,1=ACT, 0=NOT (0, DO NOT CHANGE)  (0)  ', 'typical':0}}  
        ], 
    'CONs':[ 
        {'J':{'Description':u'PV ARRAY VOC/VMP RATIO (1.25)                              ', 'typical':1.250}}, 
        {'J+1':{'Description':u'PV ARRAY ISC/IMP RATIO (1.07)                              ', 'typical':1.070}}, 
        {'J+2':{'Description':u'DC LINK TIME CONSTANT, SEC (0.005)                         ', 'typical':0.005}}, 
        {'J+3':{'Description':u'INVERTER AC THERMAL CURRENT LIMIT, PU (1.10)               ', 'typical':1.100}}, 
        {'J+4':{'Description':u'DC VOLTAGE REGULATOR PROPORTIONAL GAIN(3.0)                ', 'typical':3.000}}, 
        {'J+5':{'Description':u'DC VOLTAGE REGULATOR INTERGRAL GAIN (10.0)                 ', 'typical':10.000}}, 
        {'J+6':{'Description':u'Q REGULATOR PROPORTIONAL GAIN(0.1)                         ', 'typical':0.100}}, 
        {'J+7':{'Description':u'Q REGULATOR INTEGRAL GAIN (6.0)                            ', 'typical':6.000}}, 
        {'J+8':{'Description':u'NOT USED (0.0)                                             ', 'typical':0.000}}, 
        {'J+9':{'Description':u'NOT USED (0.0)                                             ', 'typical':0.000}}, 
        {'J+10':{'Description':u'LVRT VOLTAGE SETPOINT (VLIM), PU (0.85)                    ', 'typical':0.850}}, 
        {'J+11':{'Description':u'LVRT VOLTAGE RESET POINT (VRES), PU (0.50)                 ', 'typical':0.500}}, 
        {'J+12':{'Description':u'LVRT DIP VOLTAGE (VDIP), PU(0.00)                          ', 'typical':0.000}}, 
        {'J+13':{'Description':u'LVRT CURVE TIME (T1), SEC (1.0)                            ', 'typical':1.000}}, 
        {'J+14':{'Description':u'LVRT CURVE TIME (T2), SEC (2.1)                            ', 'typical':2.100}}, 
        {'J+15':{'Description':u'LVRT CURVE TIME (T3), SEC (3.01)                           ', 'typical':3.010}}, 
        {'J+16':{'Description':u'OVERVOLTAGE #1 PICKUP, PU (1.42)                           ', 'typical':1.420}}, 
        {'J+17':{'Description':u'OVERVOLTAGE #1 DELAY, SEC (0.016)                          ', 'typical':0.016}}, 
        {'J+18':{'Description':u'OVERVOLTAGE #2 PICKUP, PU (1.27)                           ', 'typical':1.270}}, 
        {'J+19':{'Description':u'OVERVOLTAGE #2 DELAY, SEC (1.5)                            ', 'typical':1.500}}, 
        {'J+20':{'Description':u'OVERVOLTAGE #3 PICKUP, PU (1.17)                           ', 'typical':1.170}}, 
        {'J+21':{'Description':u'OVERVOLTAGE #3 DELAY, SEC (4.0)                            ', 'typical':4.000}}, 
        {'J+22':{'Description':u'UNDERVOLTAGE #1 PICKUP, PU (0.80)                          ', 'typical':0.800}}, 
        {'J+23':{'Description':u'UNDERVOLTAGE #1 DELAY, SEC (0.5)                           ', 'typical':0.500}}, 
        {'J+24':{'Description':u'UNDERVOLTAGE #2 PICKUP, PU (0.9)                           ', 'typical':0.900}}, 
        {'J+25':{'Description':u'UNDERVOLTAGE #2 DELAY, SEC (2.0)                           ', 'typical':2.000}}, 
        {'J+26':{'Description':u'OVERFREQUENCY #1 PICKUP, HZ (62.5)                         ', 'typical':52.500}}, 
        {'J+27':{'Description':u'OVERFREQUENCY #1 DELAY, SEC (0.016)                        ', 'typical':0.016}}, 
        {'J+28':{'Description':u'OVERFREQUENCY #2 PICKUP, HZ (61.5)                         ', 'typical':51.500}}, 
        {'J+29':{'Description':u'OVERFREQUENCY #2 DELAY, SEC (30.0)                         ', 'typical':30.000}}, 
        {'J+30':{'Description':u'UNDERFREQUENCY #1 PICKUP, HZ (57.5)                        ', 'typical':47.500}}, 
        {'J+31':{'Description':u'UNDERFREQUENCY #1 DELAY, SEC (10.0)                        ', 'typical':10.000}}, 
        {'J+32':{'Description':u'UNDERFREQUENCY #2 PICKUP, HZ (56.5)                        ', 'typical':46.500}}, 
        {'J+33':{'Description':u'UNDERFREQUENCY #2 DELAY, SEC (0.08)                        ', 'typical':0.080}}, 
        {'J+34':{'Description':u'NOT USED (0.0)                                             ', 'typical':0.000}}, 
        {'J+35':{'Description':u'ACTIVE CURRENT RAMP UP RATE LIMIT, PU/SEC (0.2)            ', 'typical':0.200}}, 
        {'J+36':{'Description':u'REACTIVE CURRENT RAMP UP RATE LIMIT, PU/SEC (0.2)          ', 'typical':0.200}}, 
        {'J+37':{'Description':u'REACTIVE CURRENT INJECTION LIMIT, PU (0.8)                 ', 'typical':0.800}}, 
        {'J+38':{'Description':u'ACTIVE POWER VS FREQUENCY SLOPE, (-0.4)                    ', 'typical':-0.400}}, 
        {'J+39':{'Description':u'FREQUENCY SET POINT, (50.2 OR 60.5; 999 TO DISABLE)  (60.5)', 'typical':50.200}}, 
        {'J+40':{'Description':u'FREQUENCY RESET POINT, (50.05 OR 60.05)  (60.05)           ', 'typical':50.050}}, 
        {'J+41':{'Description':u'PLL PROPORTIONAL GAIN (0.3)                                ', 'typical':0.300}}, 
        {'J+42':{'Description':u'PLL INTEGRAL GAIN (1.0)                                    ', 'typical':1.000}}, 
        {'J+43':{'Description':u'BATTERY ENERGY, MWh  (1.0)                                 ', 'typical':1.000}}, 
        {'J+44':{'Description':u'BATTERY INITIAL SOC, PU   (0.8)                            ', 'typical':0.800}}  
        ],
    'STATEs':[ 
        {'K':{'Description':u'DC LINK, VOLTAGE, PU                                      '}}, 
        {'K+1':{'Description':u'DC VOLTAGE REG INTEGRATOR, PU ON MBASE                    '}}, 
        {'K+2':{'Description':u'Q CONTROLLER INTEGRATOR OUTPUT, PU ON MBASE               '}}, 
        {'K+3':{'Description':u'NOT USED                                                  '}}, 
        {'K+4':{'Description':u'FILTERED TERMINAL BUS FREQUENCY, HZ                       '}}, 
        {'K+5':{'Description':u'PLL FIRST INTEGRATOR,RAD/S                                '}}, 
        {'K+6':{'Description':u'PLL SECOND INTEGRATOR,RAD                                 '}}, 
        {'K+7':{'Description':u'STATE OF CHARGE (SOC) INTEGRATOR                          '}} 
        ], 
    'VARs':[ 
        {'L':{'Description':u'PV CELL THERMAL VOLTAGE CONSTANT                           '}}, 
        {'L+1':{'Description':u'INITIAL INVERTER ACTIVE POWER, PU ON MBASE                 '}}, 
        {'L+2':{'Description':u'INITIAL INVERTER REACTIVE POWER, PU ON MBASE               '}}, 
        {'L+3':{'Description':u'MEMORY FOR OVERVOLTAGE TIMER #1                            '}}, 
        {'L+4':{'Description':u'MEMORY FOR OVERVOLTAGE TIMER #2                            '}}, 
        {'L+5':{'Description':u'MEMORY FOR OVERVOLTAGE TIMER #3                            '}}, 
        {'L+6':{'Description':u'MEMORY FOR UNDERVOLTAGE TIMER #1                           '}}, 
        {'L+7':{'Description':u'MEMORY FOR UNDERVOLTAGE TIMER #2                           '}}, 
        {'L+8':{'Description':u'MEMORY FOR OVERFREQUENCY TIMER #1                          '}}, 
        {'L+9':{'Description':u'MEMORY FOR OVERFREQUENCY TIMER #2                          '}}, 
        {'L+10':{'Description':u'MEMORY FOR UNDERFREQUENCY TIMER #1                         '}}, 
        {'L+11':{'Description':u'MEMORY FOR UNDERFREQUENCY TIMER #2                         '}}, 
        {'L+12':{'Description':u'NOT USED                                                   '}}, 
        {'L+13':{'Description':u'MEMORY FOR PLL                                             '}}, 
        {'L+14':{'Description':u'INITIAL POWER FACTOR ANGLE, RADIANS                        '}}, 
        {'L+15':{'Description':u'NOT USED                                                   '}}, 
        {'L+16':{'Description':u'NOT USED                                                   '}}, 
        {'L+17':{'Description':u'MEMORY FOR LVRT TIMER                                      '}}, 
        {'L+18':{'Description':u'NOT USED                                                   '}}, 
        {'L+19':{'Description':u'MEMORY FOR POST-LVRT TIMER                                 '}}, 
        {'L+20':{'Description':u'MEMORY FOR ACTIVE POWER MGMT (LAST ACTIVE POWER WHEN      *'}}, 
        {'L+21':{'Description':u'MEMORY FOR ACTIVE POWER MGMT (LAST ACTIVE POWER)           '}}, 
        {'L+22':{'Description':u'MEMORY FOR POST-LVRT RESPONSE (LAST REACTIVE CURRENT)      '}}, 
        {'L+23':{'Description':u'MEMORY FOR POST-LVRT RESPONSE (LAST ACTIVE CURRENT)        '}}, 
        {'L+24':{'Description':u'HIGHEST FREQUENCY, HZ                                      '}}, 
        {'L+25':{'Description':u'PBAT REFERENCE TO BE SET BY THE PCC                        '}}, 
        {'L+26':{'Description':u'SOC  TO BE READ BY THE PCC                                 '}}, 
        {'L+27':{'Description':u'IRRADIATION VARIATION FACTOR                               '}} 
        ]},
'PVSYN2':{  #  ANEXO 15 MODELOS DINÁMICOS - Asep www.asep.gob.pa/electric/Anexos/ANEXO_15_expa.pdf
    'CONs':[
        {'J':{'Description':u'T1 (sec)','typical':5.0}},
        {'J+1':{'Description':u'T2 (sec)','typical':0.05}},
        {'J+2':{'Description':u'T3 (sec)','typical':0.95 }},
        {'J+3':{'Description':u'K','typical':15.0}},
        {'J+4':{'Description':u'T4 (sec)','typical':5.1}},
        {'J+5':{'Description':u'T5 (sec)','typical':0.322}},
        {'J+6':{'Description':u'T6 (sec)','typical':0.0}},
        {'J+7':{'Description':u'TD (0<TD<12*DELT) (sec)','typical':0.002}},
        {'J+8':{'Description':u'TMAX','typical':0.8}},
        {'J+9':{'Description':u'TMIN','typical':0.387}},
        {'J+10':{'Description':u'DROOP','typical':0.03}},
        {'J+11':{'Description':u'TE','typical':0.05}}
        ],
    'ICONs':[
        {'M':{'typical':0.03, 'Description':u'Droop control (0:Throttle, 1:Power)','typical':0}}
        ],
     'STATEs':[
        {'K'  :{'Description':u"Df_t_p", 'name':'Df_t_p', 'tex':"$\sf \\Delta f'_t $"}},
        {'K+1':{'Description':u"DV_t_m_p", 'name':'DV_t_m_p', 'tex':"$\sf  \\Delta V'_t $"}},
        {'K+2':{'Description':u'omega', 'name':'omega','tex':'$\sf \\omega $'}},
        {'K+3':{'Description':u'theta', 'name':'theta','tex':'$\sf \\theta $'}},
        {'K+4':{'Description':u'xi_q (pu)', 'name':'xi_q', 'tex':'$\sf \\xi_q$'}},
        {'K+5':{'Description':u'xi_p (radians)', 'name':'xi_p', 'tex':'$\sf \\xi_p$'}},  
        {'K+6':{'Description':u'i_r_filt (pu)', 'name':'i_r_filt', 'tex':'$\sf i_r^{filt}$'}},
        {'K+7':{'Description':u'i_i_filt (radians)', 'name':'i_i_filt', 'tex':'$\sf i_i^{filt}$'}}
    ]},
}


'''
DEGOV según aguero:
'DEGOV1':{
    'CONs':[
        {'J':{'Description':u'T1 (sec)','typical':0.03}},
        {'J+1':{'Description':u'T2 (sec)','typical':0.01}},
        {'J+2':{'Description':u'T3 (sec)','typical':1.6 }},
        {'J+3':{'Description':u'K','typical':3.31}},
        {'J+4':{'Description':u'T4 (sec)','typical':0.14}},
        {'J+5':{'Description':u'T5 (sec)','typical':0.28}},
        {'J+6':{'Description':u'T6 (sec)','typical':0.6}},
        {'J+7':{'Description':u'TD (0<TD<12*DELT) (sec)','typical':0.03}},
        {'J+8':{'Description':u'TMAX','typical':1.1}},
        {'J+9':{'Description':u'TMIN','typical':0.0}},
        {'J+10':{'Description':u'DROOP','typical':0.03}},
        {'J+11':{'Description':u'TE','typical':0.04}}
        ],
    'ICONs':[
        {'M':{'typical':0.03, 'Description':u'Droop control (0:Throttle, 1:Power)','typical':0}}
        ],
     'STATEs':[
        {'K':{'Description':u'Electric control box 1'}},
        {'K+1':{'Description':u'Electric control box 2'}},
        {'K+2':{'Description':u'Actuator 1'}},
        {'K+3':{'Description':u'Actuator 2'}},
        {'K+4':{'Description':u'Actuator 3'}},
        {'K+5':{'Description':u'Power transducer'}}
    ]},
'GENSAL':{
    'CONs':[
        {'J':{'Description':u"T'do (>0) (sec)",'typical':3.9  }},
        {'J+1':{'Description':u"T''do (>0) (sec)",'typical':0.028  }},
        {'J+2':{'Description':u"T''qo (>0) (sec)",'typical':0.226   }},
        {'J+3':{'Description':u"H, Inertia",'typical':0.44  }},
        {'J+4':{'Description':u"D, Speed damping",'typical':0.0  }},
        {'J+5':{'Description':u'X_d','typical':2.76 }},
        {'J+6':{'Description':u'X_q','typical':1.78   }},
        {'J+7':{'Description':u"X'd",'typical':0.17  }},
        {'J+8':{'Description':u"X''_d = X''_q",'typical':0.25 }},
        {'J+9':{'Description':u'X_l','typical':0.44 }},
        {'J+10':{'Description':u'S(1.0)','typical':1.29  }},
        {'J+11':{'Description':u'S(1.2)','typical':1.98   }}
    ]},

'DEGOV1':{  #  ** BUS NAME  16024 PIURA  
    'CONs':[
        {'J':{'Description':u'T1 (sec)','typical':0.5}},
        {'J+1':{'Description':u'T2 (sec)','typical':0.02}},
        {'J+2':{'Description':u'T3 (sec)','typical':7.2 }},
        {'J+3':{'Description':u'K','typical':0.155}},
        {'J+4':{'Description':u'T4 (sec)','typical':-0.018}},
        {'J+5':{'Description':u'T5 (sec)','typical':0.130}},
        {'J+6':{'Description':u'T6 (sec)','typical':0.250}},
        {'J+7':{'Description':u'TD (0<TD<12*DELT) (sec)','typical':0.05}},
        {'J+8':{'Description':u'TMAX','typical':0.75}},
        {'J+9':{'Description':u'TMIN','typical':0.0}},
        {'J+10':{'Description':u'DROOP','typical':0.083}},
        {'J+11':{'Description':u'TE','typical':0.0}}
        ],
    'ICONs':[
        {'M':{'typical':0.03, 'Description':u'Droop control (0:Throttle, 1:Power)','typical':0}}
        ],
     'STATEs':[
        {'K':{'Description':u'Electric control box 1'}},
        {'K+1':{'Description':u'Electric control box 2'}},
        {'K+2':{'Description':u'Actuator 1'}},
        {'K+3':{'Description':u'Actuator 2'}},
        {'K+4':{'Description':u'Actuator 3'}},
        {'K+5':{'Description':u'Power transducer'}}
    ]},
'''





