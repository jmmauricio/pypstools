""" Tools for plotting and publishing power system simulations ans analysis results.

(c) 2015 Juan Manuel Mauricio
"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg
import hickle
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from StringIO import StringIO
import json
import os

case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'

svg_dir = os.path.join(case_dir,'doc','svg')
png_dir = os.path.join(case_dir,'doc','png')

datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(0), usemask=True ) 
gen_thermal_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)

datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(1), usemask=True ) 
gen_hydro_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)


datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(2), usemask=True ) 
gen_cond_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)

vip_gen_buses = list(gen_thermal_buses) + list(gen_hydro_buses) + list(gen_cond_buses)
#vip_gen_buses = [26,10,87,111,89,61,32]  
#vip_gen_buses = [26,10] 

def interactive_svg(plt,svg_file,ids, ax, distance_factor=0.8):   
    
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
    
    print(ids)
    
    for id_item, curve in zip(ids,ax.get_lines()):
#        line = curve.get_lines()
#        print(line)
        curve.set_gid(id_item)
        el = xmlid[id_item]
        el.set('onmousemove', "ShowTooltip(evt, '{:s}')".format(id_item))
        el.set('onmouseout', "HideTooltip(evt)")

    tree.append(ET.XML(box))
    tree.append(ET.XML(box_text))
    ET.ElementTree(tree).write(svg_file)
    
    
class publish:

    def __init__(self):
        
        self.hdf5file = ''        
        pass

    def plot_pq_w_a_large(self, test_id, individual_figure=True, data_sim = ''):
        '''Plots curves of:
        - Active and reactive powers (generators ans loads)
        - Speeds of generators
        - Voltages of considered buses

        

        '''


        

        self.test_id = test_id
        self.data_dict =  hickle.load(self.hdf5file)
        
        self.t = self.data_dict[test_id]['sys']['t']
        
        
    
        if individual_figure==True:

            fig_p_gen = plt.figure()
            fig_q_gen = plt.figure()
            fig_v = plt.figure()
#            fig_w = plt.figure(figsize=(15,10))
            fig_w = plt.figure()
            fig_p_load = plt.figure()
            fig_q_load = plt.figure()
            
            

            ax_p_gen = fig_p_gen.add_subplot(111)
            ax_p_gen.set_xlim((self.t[0], self.t[-1]))
            ax_p_gen.grid(True)
            ax_p_gen.set_ylabel('Active powers (MW)')
            ax_p_gen.set_xlabel(u'Time (s)')

            ax_q_gen = fig_q_gen.add_subplot(111)
            ax_q_gen.set_ylabel('Reactive powers (Mvar)')
            ax_q_gen.set_xlim((self.t[0], self.t[-1]))
            ax_q_gen.grid(True)
            ax_q_gen.set_xlabel(u'Time (s)')

            ax_p_load = fig_q_load.add_subplot(111)
            ax_p_load.set_xlim((self.t[0], self.t[-1]))
            ax_p_load.grid(True)
            ax_p_load.set_ylabel('Load active powers (MW)')

            ax_q_load = fig_q_load.add_subplot(111)
            ax_q_load.set_xlim((self.t[0], self.t[-1]))
            ax_q_load.grid(True)
            ax_q_load.set_ylabel('Load reactive power (Mvar)')

            ax_volt = fig_v.add_subplot(111)
            ax_volt.set_ylabel('Bus Voltage (pu)')
            ax_volt.set_xlim((self.t[0], self.t[-1]))
            ax_volt.grid(True)
            #ax_volt.set_xlabel(u'Time (s)')

            ax_speed = fig_w.add_subplot(111)
            ax_speed.set_ylabel('Speed (Hz)')
            ax_speed.set_xlim((self.t[0], self.t[-1]))
            ax_speed.grid(True)
            ax_speed.set_xlabel(u'Time (s)')




        vip_gen_bus_names = ['bus_{:d}'.format(item) for item in vip_gen_buses]
        
        bus_names = ['bus_{:d}'.format(item) for item in vip_gen_buses]

  
        ids = vip_gen_bus_names
        speed_coi = self.data_dict[test_id][bus_names[0]]['speed'] 
        for item_bus, item_number in zip(vip_gen_bus_names,vip_gen_buses):

            # generators active power:
            ax_p_gen.plot(self.t, self.data_dict[test_id][item_bus]['p_gen']*100.0,
                      label='$\sf p_{{g{:d}}}$'.format(item_number))          
  
            # generators reactive power:
            ax_q_gen.plot(self.t, self.data_dict[test_id][item_bus]['q_gen']*100.0,
                      label='$\sf q_{{g{:d}}}$'.format(item_number))   

            # generators reactive power:
            ax_volt.plot(self.t, self.data_dict[test_id][item_bus]['volt'],label='$\sf v_{{{:d}}}$'.format(item_number))   
            curve_speed = ax_speed.plot(self.t, (self.data_dict[test_id][item_bus]['speed']),label='$\sf \omega_{{{:d}}}$'.format(item_number), lw=1)   
    #curve_speed.set_gid(item_id)

#        for item_curve, item_id in zip(ax_volt.get_lines(),bus_names):
#            item_curve.set_gid(item_id)
#            ids += [item_id]            
#        ax_speed.legend(loc='best')
        
#        for item_curve, item_id in zip(ax_speed.get_lines(),bus_names):
#            item_curve.set_gid(item_id)
#            ids += [item_id]
#ids = ['G1','G200']

#        ids = ['bus_26','bus_10'] 

        for id_item, line in zip(ids,ax_speed.get_lines()):
            
            line.set_gid(id_item)


        figs_name_list = ['p_gen', 'q_gen','v','w']
        figs_list = [fig_p_gen,fig_q_gen,fig_v,fig_w]
        
        for item_fig_name, item_fig in zip(figs_name_list, figs_list):
            
            fig_name = '{:s}_{:s}_{:s}.png'.format(self.test_id,item_fig_name,data_sim)
            fig_png_path = os.path.join(png_dir,fig_name)        
            fig_name = '{:s}_{:s}_{:s}.svg'.format(self.test_id,item_fig_name,data_sim)
            fig_svg_path = os.path.join(svg_dir,fig_name)
            
            item_fig.savefig(fig_png_path)      
            item_fig.savefig(fig_svg_path) 
            
        
        interactive_svg(fig_w,fig_svg_path,ids, ax_speed, distance_factor=0.8) 
            
            
##        ax_speed.plot(self.t, (speed_coi),label='$\sf \omega_{{{:d}}}$'.format(item_number))   
#
###        ax_speed.set_ylim((48.5,51.5)) *50.0+50.0
###        ax_volt.set_ylim((0.8,1.1))
###        ax_p.set_ylim((2,8))
###        ax_q.set_ylim((-4,8))
#    
#ax_p.legend(loc='best',ncol=3)
#ax_q.legend(loc='best',ncol=3)
##        ax_volt.legend(loc='best',ncol=3)
##        ax_speed.legend(loc='best',ncol=3)
#
#bus_names = ['bus_{:d}'.format(item) for item in [1]]
#
###        for item_bus, item_number in zip(bus_names,[1]):
###            print(item_bus)
###            ax_pq_load.plot(self.t, self.data_dict[item_bus]['p_load']*100.0,label='$\sf p_{{l{:d}}}$'.format(item_number))            
###            ax_pq_load.plot(self.t, self.data_dict[item_bus]['q_load']*100.0,label='$\sf q_{{l{:d}}}$'.format(item_number))   
###
        
#
#
#
#ierr, ival_icon = psspy.mdlind(2, '1', 'GEN', 'ICON')
#ierr, pvsyn_mode = psspy.dsival('ICON', ival_icon) 
#####
#
#pvsyn_mode_str = 'None'
#if pvsyn_mode==1: pvsyn_mode_str = 'Power'
#if pvsyn_mode==2: pvsyn_mode_str = 'Energy'
##fig_title = '$\sf H={:2.1f},\; K_d = {:2.2f}, \; K_f = {:2.2f}, \; K_v = {:2.2f}$, Mode: {:s}'.format((self.H),(self.K_d),((self.K_f)), (self.K_v), pvsyn_mode_str)
#fig_title = 'hola'
#fig_pq_gen.suptitle(fig_title)
#fig_v.suptitle(fig_title)  
#fig_w.suptitle(fig_title) 
##        data_sim = 'H_{:2.1f}'.format(self.H)  
##        data_sim += '_K_d_{:2.1f}'.format(self.K_d)   
##        data_sim += '_R_s_{:2.3f}'.format(self.R_s)  
##        data_sim += '_X_s_{:2.3f}'.format(self.X_s)  
##        data_sim += '_K_f_{:2.1f}'.format(self.K_f)  
##        data_sim += '_K_v_{:2.1f}'.format(self.K_v)
##        data_sim = data_sim.replace('.','p').replace('-','m').replace(' ','')   
#
#data_sim = 'prueba'
#rst_str = ''
#svg_dir = os.path.join(casedir,'..','jmm','doc','svg')
#png_dir = os.path.join(casedir,'..','jmm','doc','png')
##rst_str += rst.chapter(self.rst_title)
#fig_name = '{:s}_pgen_qgen_{:s}.png'.format(self.test_id,data_sim)        
##fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'png',fig_name)
#fig_path = os.path.join(casedir)
#fig_name = '{:s}_pgen_qgen_{:s}.svg'.format(self.test_id,data_sim)        
#fig_path = os.path.join(svg_dir,fig_name)
#fig_pq_gen.savefig(fig_path)
#rst_str += rst.section('Generated powers')
#rst_str += rst.figure(fig_name,align='center')
#
#fig_name = '{:s}_v_{:s}.png'.format(self.test_id,data_sim)         
#fig_path = os.path.join(png_dir,fig_name)
#fig_name = '{:s}_v_{:s}_mod.svg'.format(self.test_id,data_sim)         
#fig_path = os.path.join(svg_dir,fig_name)
#fig_v.savefig(fig_path)     
#interactive_svg(fig_v,fig_path,ids, ax_speed, distance_factor=0.8)
#
#fig_name = '{:s}_omega_{:s}.png'.format(self.test_id,data_sim)         
#fig_path = os.path.join(png_dir,fig_name)
#fig_name = '{:s}_omega_{:s}.svg'.format(self.test_id,data_sim)         
#fig_path = os.path.join(svg_dir,fig_name)
#fig_w.savefig(fig_path)   
#interactive_svg(fig_w,fig_path,ids, ax_speed, distance_factor=0.8)
###        rst_str += rst.section('Voltages and speeds')
###        rst_str += rst.figure(fig_name,align='center')
###
###        fig_name = '{:s}_pq_load_{:s}.png'.format(self.test_id,data_sim)
###        fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'png',fig_name)        
###        fig_name = '{:s}_pq_load_{:s}.svg'.format(self.test_id,data_sim)
###        fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'svg',fig_name)
###        fig_pq_load.savefig(fig_path)      
###        rst_str += rst.section('Load powers')
###        rst_str += rst.figure(fig_name,align='center')
###        
###        rst_name=self.rst_title.replace(' ','_').replace(',','')
###        file_rst = file(os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,rst_name+'.rst'), 'w')
###        file_rst.write(rst_str)
###        file_rst.close()
##        plt.show()
##
###        import scipy.io
###        mat_name = 'test_p_{:d}_q1_{:d}_q2_{:d}.mat'.format(int(self.Dp),int(self.Dq_1),int(self.Dq_2)).replace('-','neg')
###        mat_file_path = os.path.join(casedir, 'identification', mat_name)
###        scipy.io.savemat(mat_file_path, py2mat_dict)
###        file_pkl = open(config_file, 'a')
###        pickle.dump(mat_file_path, file_pkl,protocol=-1)
###        file_pkl.close()        
####        configuration.update({'matfiles':{mat_name:mat_file_path}}
###        
###        file_pkl = open(config_file, 'r')
###        config = pickle.load(file_pkl)
###        file_pkl.close()
###        file_pkl = open(config_file, 'w')
###        config.update({mat_name.split('.')[0]:mat_name})
###        pickle.dump(config, file_pkl,protocol=-1)
###        file_pkl.close()


    def coi_speed(self):
        '''Computes COI speed

        '''
        it_spd = 0
        for item_bus, item_number in zip(bus_names,vip_buses):
            if it_spd == 0:            
                speeds = self.data_dict[item_bus]['speed'] 
            if it_spd > 0:            
                speeds +=  self.data_dict[item_bus]['speed']                
                
            it_spd += 1
            
        speed_coi = speeds/(4.0)
        return speed_coi 


if __name__ == '__main__':
    
    pub = publish()

    casedir = r'/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'
    tests_out = os.path.join(casedir,'tests_out.hdf5')    
    pub.hdf5file = tests_out
    pub.plot_pq_w_a_large('test_v_ref_change_111_up')