""" Tools for plotting and publishing power system simulations ans analysis results.

(c) 2015 Juan Manuel Mauricio
"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg


class publish:

    def __init__(self, psspy):

    	pass

    def plot_pq_w_a_large(self):
        

        self.test_id = self.data['test_id']

        individual_figure==True
    
        if individual_figure==True:

            fig_p_gen = plt.figure()
            fig_q_gen = plt.figure()
            fig_v = plt.figure()
            fig_w = plt.figure()
            fig_p_load = plt.figure()
            fig_q_load = plt.figure()

            ax_p_gen = fig_p_gen.add_subplot(111)
            ax_p_gen.set_xlim((self.t[0], self.t[-1]))
            ax_p_gen.grid(True)
            ax_p_gen.set_ylabel('Active powers (MW)')
            ax_p.set_xlabel(u'Time (s)')

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


  
        ids = []
        speed_coi = self.data_dict[bus_names[0]]['speed'] 
        for item_bus, item_number in zip(vip_gen_bus_names,vip_gen_buses):

            # generators active power:
            ax_p.plot(self.t, self.data_dict[item_bus]['p_gen']*100.0,
                      label='$\sf p_{{g{:d}}}$'.format(item_number))          
  
            # generators reactive power:
            ax_q.plot(self.t, self.data_dict[item_bus]['q_gen']*100.0,
                      label='$\sf q_{{g{:d}}}$'.format(item_number))   

            # generators reactive power:
            ax_volt.plot(self.t, self.data_dict[item_bus]['volt'],label='$\sf v_{{{:d}}}$'.format(item_number))   
            curve_speed = ax_speed.plot(self.t, (self.data_dict[item_bus]['speed']),label='$\sf \omega_{{{:d}}}$'.format(item_number))   
    #curve_speed.set_gid(item_id)

        for item_curve, item_id in zip(ax_volt.get_lines(),bus_names):
            item_curve.set_gid(item_id)
            ids += [item_id]            

        for item_curve, item_id in zip(ax_speed.get_lines(),bus_names):
            item_curve.set_gid(item_id)
            ids += [item_id]

#        ax_speed.plot(self.t, (speed_coi),label='$\sf \omega_{{{:d}}}$'.format(item_number))   

##        ax_speed.set_ylim((48.5,51.5)) *50.0+50.0
##        ax_volt.set_ylim((0.8,1.1))
##        ax_p.set_ylim((2,8))
##        ax_q.set_ylim((-4,8))
    
ax_p.legend(loc='best',ncol=3)
ax_q.legend(loc='best',ncol=3)
#        ax_volt.legend(loc='best',ncol=3)
#        ax_speed.legend(loc='best',ncol=3)

bus_names = ['bus_{:d}'.format(item) for item in [1]]

##        for item_bus, item_number in zip(bus_names,[1]):
##            print(item_bus)
##            ax_pq_load.plot(self.t, self.data_dict[item_bus]['p_load']*100.0,label='$\sf p_{{l{:d}}}$'.format(item_number))            
##            ax_pq_load.plot(self.t, self.data_dict[item_bus]['q_load']*100.0,label='$\sf q_{{l{:d}}}$'.format(item_number))   
##
##        ax_pq_load.legend(loc='best')



ierr, ival_icon = psspy.mdlind(2, '1', 'GEN', 'ICON')
ierr, pvsyn_mode = psspy.dsival('ICON', ival_icon) 
####

pvsyn_mode_str = 'None'
if pvsyn_mode==1: pvsyn_mode_str = 'Power'
if pvsyn_mode==2: pvsyn_mode_str = 'Energy'
#fig_title = '$\sf H={:2.1f},\; K_d = {:2.2f}, \; K_f = {:2.2f}, \; K_v = {:2.2f}$, Mode: {:s}'.format((self.H),(self.K_d),((self.K_f)), (self.K_v), pvsyn_mode_str)
fig_title = 'hola'
fig_pq_gen.suptitle(fig_title)
fig_v.suptitle(fig_title)  
fig_w.suptitle(fig_title) 
#        data_sim = 'H_{:2.1f}'.format(self.H)  
#        data_sim += '_K_d_{:2.1f}'.format(self.K_d)   
#        data_sim += '_R_s_{:2.3f}'.format(self.R_s)  
#        data_sim += '_X_s_{:2.3f}'.format(self.X_s)  
#        data_sim += '_K_f_{:2.1f}'.format(self.K_f)  
#        data_sim += '_K_v_{:2.1f}'.format(self.K_v)
#        data_sim = data_sim.replace('.','p').replace('-','m').replace(' ','')   

data_sim = 'prueba'
rst_str = ''
svg_dir = os.path.join(casedir,'..','jmm','doc','svg')
png_dir = os.path.join(casedir,'..','jmm','doc','png')
#rst_str += rst.chapter(self.rst_title)
fig_name = '{:s}_pgen_qgen_{:s}.png'.format(self.test_id,data_sim)        
#fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'png',fig_name)
fig_path = os.path.join(casedir)
fig_name = '{:s}_pgen_qgen_{:s}.svg'.format(self.test_id,data_sim)        
fig_path = os.path.join(svg_dir,fig_name)
fig_pq_gen.savefig(fig_path)
rst_str += rst.section('Generated powers')
rst_str += rst.figure(fig_name,align='center')

fig_name = '{:s}_v_{:s}.png'.format(self.test_id,data_sim)         
fig_path = os.path.join(png_dir,fig_name)
fig_name = '{:s}_v_{:s}_mod.svg'.format(self.test_id,data_sim)         
fig_path = os.path.join(svg_dir,fig_name)
fig_v.savefig(fig_path)     
interactive_svg(fig_v,fig_path,ids, ax_speed, distance_factor=0.8)

fig_name = '{:s}_omega_{:s}.png'.format(self.test_id,data_sim)         
fig_path = os.path.join(png_dir,fig_name)
fig_name = '{:s}_omega_{:s}.svg'.format(self.test_id,data_sim)         
fig_path = os.path.join(svg_dir,fig_name)
fig_w.savefig(fig_path)   
interactive_svg(fig_w,fig_path,ids, ax_speed, distance_factor=0.8)
##        rst_str += rst.section('Voltages and speeds')
##        rst_str += rst.figure(fig_name,align='center')
##
##        fig_name = '{:s}_pq_load_{:s}.png'.format(self.test_id,data_sim)
##        fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'png',fig_name)        
##        fig_name = '{:s}_pq_load_{:s}.svg'.format(self.test_id,data_sim)
##        fig_path = os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,'svg',fig_name)
##        fig_pq_load.savefig(fig_path)      
##        rst_str += rst.section('Load powers')
##        rst_str += rst.figure(fig_name,align='center')
##        
##        rst_name=self.rst_title.replace(' ','_').replace(',','')
##        file_rst = file(os.path.join(casedir,'..','..','doc','source','gen_load_pvsync',self.test_id,rst_name+'.rst'), 'w')
##        file_rst.write(rst_str)
##        file_rst.close()
#        plt.show()
#
##        import scipy.io
##        mat_name = 'test_p_{:d}_q1_{:d}_q2_{:d}.mat'.format(int(self.Dp),int(self.Dq_1),int(self.Dq_2)).replace('-','neg')
##        mat_file_path = os.path.join(casedir, 'identification', mat_name)
##        scipy.io.savemat(mat_file_path, py2mat_dict)
##        file_pkl = open(config_file, 'a')
##        pickle.dump(mat_file_path, file_pkl,protocol=-1)
##        file_pkl.close()        
###        configuration.update({'matfiles':{mat_name:mat_file_path}}
##        
##        file_pkl = open(config_file, 'r')
##        config = pickle.load(file_pkl)
##        file_pkl.close()
##        file_pkl = open(config_file, 'w')
##        config.update({mat_name.split('.')[0]:mat_name})
##        pickle.dump(config, file_pkl,protocol=-1)
##        file_pkl.close()


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



