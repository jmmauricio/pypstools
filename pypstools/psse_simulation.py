""" Tools for simulation with PSS/E.

(c) 2015 Juan Manuel Mauricio
"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg

import analysis, publisher


class test:
    '''Class to simulate tests with PSS/E


    '''
    
    def __init__(self, psspy):

	self.psspy = psspy
	self.t_pert = 1.0 # default time for perturbation
        self.t_end = 20.0 # default time to end the simulation
    	self.dt = 0.001   # default integration time step

    def run(self):

	psspy = self.psspy

        # load sav and snp:
        psspy.case(savdynfile)  # sav file with generators and loads converted
        psspy.rstr(snpfile)     # snp file with channels defined   
        psspy.strt(0,outfile1)  # initialization (again)

        # system initialization
        psspy.strt(0,outfile1)
        psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f, self.dt,_f,_f,_f,_f,_f])

	# runs without perturbation until t=1s
        psspy.run(0, self.t_pert,1000,10,100)

	# for v_ref changes
        if self.data['test_type']=='v_ref_change':
            ibus = self.data['gen_bus']
            id   = self.data['gen_id']
            newval = self.data['change']

            ierr = psspy.increment_vref(ibus, id, newval)

            t_end = self.t_end
            psspy.run(0, t_end,1000,100,100)

        
        if self.data['test_type']=='freq_change':
            t_ends = np.arange(1.0,2.0,0.01)
            for t_end in t_ends:
                #print(t_end)
            
                ierr, number = psspy.mdlind(1, '1', 'GEN', 'STATE')
                psspy.change_state(number, [(t_end-1.0)*0.1,0.0,(t_end-1.0)*0.1])
                psspy.run(0, t_end,1000,1,0)
                

                
        if self.data[self.data['test_type']]=='p_ref_change':      
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
        chnf = dyntools.CHNF(outfile1)
        print chnf.get_data()[1]
        t = np.array(chnf.get_data()[2]['time'])
        self.t = t
        py2mat_dict = {}
        
        test_id = self.data['test_id']
        data_dict = {}
        var_list =      [('volt','VOLT',vip_buses), ('speed','SPD',vip_buses), ('p_gen','POWR',vip_buses),
                         ('q_gen','VARS',vip_buses), ('freq','FREQ',vip_buses), ('theta','ANGL',vip_buses)]


        data_dict.update({'sys':{'t':chnf.get_data()[2]['time']}})     
        for item_var,item_psse_var,item_buses in  var_list:
            
            if item_psse_var == 'VAR':      
                device_name = item_var[0]
                if not data_dict.has_key(device_name):
                    data_dict.update({device_name:{}})                
                item_value = np.array(chnf.get_data()[2][name2chan(chnf,item_psse_var, item_buses)])
                data_dict[device_name].update({item_var[1]:item_value})
            else:
                for item_bus in item_buses:
                    device_name = 'bus_{:d}'.format(item_bus)
                    if not data_dict.has_key(device_name):
                        data_dict.update({device_name:{}})                
                    item_value = np.array(chnf.get_data()[2][name2chan(chnf,item_psse_var, item_bus)])
                    data_dict[device_name].update({item_var:item_value})
                
        self.data_dict = data_dict
        
        
               
                

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


#plt.rcParams['svg.embed_char_paths'] = 'none'



        
Dp_large = 100.0
Dp_small = 50
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
tests = [{'id':'p_ref_vsc_1_up', 'type':'freq_change',   'change_var':'Dp_1', 'change':100.0}]
tests = [{'id':'p_ref_vsc_1_up', 'rst_title':'p_ref_vsc_1_up', 'type':'q_ref_change',   'change_var':'Dp_1', 'change':100.0, 'devices':{'vsc1':10.0}}]
tests = [{'test_id':'v_ref_change_26_up', 'rst_title':'v_ref_change_26_up', 'type':'v_ref_change',   'gen_bus':1, 'gen_id':'1', 'change':0.1}]


data_dict = {}        

rst_str_tests = ''




for item in  tests:
    instance_name = "test_{:s}".format(item['test_id'])
    print instance_name
    exec(instance_name + ' = test()')
    exec(instance_name + ".data = item")  
    exec(instance_name + ".run()")
    exec(instance_name + ".outfile2dict()")
exec(instance_name + ".draw()")



