# -*- coding: cp1252/latin-1 -*-
"""
Created on Thu Mar 05 12:06:06 2015

@author: 2
"""

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
##                    if not(ierr==3 and item_psse_var=='SPD'):777



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
    
    
        for item_test in  tests_info['tests']:   
        raw_dyr_dir = item_test['raw_dyr_dir']
        out_dir =item_test['out_dir']
        case_name = item_test['case_name']
        rst_title = item_test['rst_title']
        test_type = item_test['test_type']
#        change = item_test['change']    
    
        print(item_test['test_id'])
    
        vip_buses = range(1,119)
        
        case_name = item_test['case_name']
        outfile = os.path.join(out_dir,case_name + '.out')
        
              
        Dp_large = 100.0
        Dp_small = 50
         
        data_dict = {}        
        
        rst_str_tests = ''
        
        
        psspy,dyntools,savdynfile,snpfile = psse(tests_yaml, psse_version = 'PSSE33')
        
        sid = -1
        ierr, buses = psspy.abusint(sid, 2, 'NUMBER')
        ierr, gen_buses = psspy.agenbusint(sid, 2, 'NUMBER')
        
        test_1 = test(psspy,dyntools,savdynfile,snpfile)
        test_1.data = item_test
        test_1.vip_buses = vip_buses
        test_1.run(outfile)
        test_1.run(outfile)
        test_1.outfile2dict()
        tests_results.update({item_test['test_id']:test_1.results_dict})

        
    tests_out = os.path.join(tests_info['hdf5file'])
    
    hickle.dump(tests_results, tests_out)
    
    
#    tests_info = ya.load(open(r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\tests\pvsync\ieee118pvsync_1pv\ieee118_pvsinc_tests.yaml','r'))
    tests_yaml = ya.load(open(r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_118\tests\pvsync\ieee118pvsync_10\ieee118_pvsinc_tests.yaml','r'))
    tests_results = {}
    
    


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
