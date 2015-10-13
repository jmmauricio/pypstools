""" Tools for plotting and publishing power system simulations and analysis results.

(c) 2015 Juan Manuel Mauricio

https://www.packtpub.com/books/content/plotting-geographical-data-using-basemap

"""
from __future__ import division, print_function

import numpy as np
import scipy.linalg

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import xml.etree.ElementTree as ET
from StringIO import StringIO
import json
import os
import yaml




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
     font-family: Arial;
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
        self.freq_base = 60.0
        self.lw = 2.0
        self.legends = True
        self.png_dir = '.'
        self.svg_dir = '.'
        
        
    def publisher(self, yaml_file):
        '''Create figures with multiple axis and curves from .hdf5 tests result files
        and considering yaml file configuration.
        
        Example of yaml file
        --------------------
        
        .. code:: python
        
                # YAML
                - name: figura 1              # figure
                  file: ./speed_gen_zoom_1.svg
                  axes:                       # axes
                  - # axe 1
                    curves:                   # curves group
                    - 
                      file: ./ieee118_pvsyn_1_100mva.hf5
                      test_id: v_ref_change_26_up_pvsyn_1
                      element_type: sym
                      elements: [sym_26, sym_111]
                      legends:  ['$\omega_{26}$', '$\omega_{111}$']
                      variable: speed
                    ylabel: Speed (pu)
                    scale: 50.0
                    offset: 50.0
                    ylimits: [49.96,50.01]
                  - # axe 2
                    curves:
                    - 
                      file: ./ieee118_v33_modif.hf5
                      test_id: v_ref_change_26_up
                      element_type: sym
                      elements: [sym_26, sym_111]
                      legends:  ['$\omega_{26}$', '$\omega_{111}$']
                      variable: speed
                    ylabel: Speed (pu)
                    xlabel: Time (s)
                    scale: 50.0
                    offset: 50.0
                    ylimits: [49.96,50.01]
                - name: figura 2              # figure
                  file: ./pq_gen_zoom_1.svg
                  axes:                       # axes
                  - # axe 1
                    curves:                   # curves group
                    - 
                      file:./ieee118_pvsyn_1_100mva.hf5
                      test_id: v_ref_change_26_up_pvsyn_1
                      element_type: sym
                      elements: [sym_110]
                      legends:  ['$p_{110}$']
                      variable: p_gen
                    ylabel: Power (MW)
                    scale: 100.0
                  - # axe 2
                    curves:
                    - 
                      file: ./ieee118_v33_modif.hf5
                      test_id: v_ref_change_26_up
                      element_type: sym
                      elements: [sym_110]
                      legends:  ['$p_{110}$']
                      variable: p_gen
                    ylabel: Power (MW)
                    xlabel: Time (s)
                    scale: 100.0


        '''        
        
        import hickle
        ya = yaml.load(open(yaml_file,'r').read())

        figures = []
        
        for item_fig in ya:            
            if item_fig.has_key('fig_height') and item_fig.has_key('fig_width'):
                figure = plt.figure(figsize=(item_fig['fig_height'],item_fig['fig_width']))
            else:
                figure = plt.figure()
                
                

            
            figures += [figure]
            
            n_axes = len(item_fig['axes'])
            it_axe = 0
            for item_axe in item_fig['axes']:

                it_axe += 1
                axe = figure.add_subplot(n_axes,1,it_axe)
                
                if item_axe.has_key('scale'): scale = item_axe['scale'] 
                else: scale=1.0

                if item_axe.has_key('offset'): offset = item_axe['offset'] 
                else: offset=0.0                   
                    
                for item_curve_group in item_axe['curves']:
                    print(item_curve_group['file'])
                    h_tests = hickle.load(item_curve_group['file'])
                    
                    if not h_tests.has_key(item_curve_group['test_id']):
                        print('{:s} Test id is not availabe'.format(item_curve_group['test_id']))
                        print("Availables id's are:")
                        print(h_tests.keys())
                        return  
                    
                    
                    h = h_tests[item_curve_group['test_id']]
                    
                    if not item_curve_group['elements'] == 'all_gen':
                        for (item_curve, item_legend) in zip(item_curve_group['elements'], item_curve_group['legends']):
    
                            t = h['sys']['time']

                            if item_curve_group.has_key('scale'): scale = item_curve_group['scale']
                            if item_curve_group.has_key('offset'): offset = item_curve_group['offset'] 

                            var = offset + scale*h[item_curve_group['element_type']][str(item_curve)][item_curve_group['variable']]['data']

                            axe.plot(t,var, label=item_legend, lw=2.0)

                    if item_curve_group['elements'] == 'all_gen':  # to plot all generators
                        for item_curve in h['syms']:
                            item_legend = item_curve_group['legends']
                            t = h['sys']['time']
#                            print(h['sym'])
                            var = offset + scale*h[item_curve_group['element_type']][item_curve][item_curve_group['variable']]['data']
                            axe.plot(t,var, label=item_legend, lw=2.0)
                            
                            
                axe.set_xlim((t[0], t[-1]))
                
                loc = 'best'
                ncol = 1
                if item_axe.has_key('legend_position'):
                    loc = item_axe['legend_position']
                if item_axe.has_key('ncol'):
                    ncol = item_axe['ncol']
                    
                axe.legend(loc=loc, ncol=ncol)
                    
                axe.grid(True)
                
                axe.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

                if item_axe.has_key('xlabel'): axe.set_xlabel(item_axe['xlabel']) 
                if item_axe.has_key('ylabel'): axe.set_ylabel(item_axe['ylabel']) 
                if item_axe.has_key('ylimits'): axe.set_ylim(item_axe["ylimits"])
            figure.savefig(item_fig['file']) 
            
            

        return figures,h_tests


    def plot_pq_w_a_large(self, test_id, individual_figure=True, data_sim = ''):
        '''Plots curves of:
        - Active and reactive powers (generators ans loads)
        - Speeds of generators
        - Voltages of considered buses

        

        '''


        
        
        self.test_id = test_id
        self.data_dict =  hickle.load(self.hdf5file)
        
        if not self.data_dict.has_key(test_id):
            print('{:s} Test id is not availabe'.format(test_id))
            print("Availables id's are:")
            print(self.data_dict.keys())
            return 
        
        
        
        self.t = self.data_dict[test_id]['sys']['time']
        
        
        vip_gen_buses = self.vip_gen_buses
        png_dir = self.png_dir
        svg_dir = self.svg_dir 
        
    
        if individual_figure==True:

            fig_p_gen = plt.figure()
            fig_q_gen = plt.figure()
            fig_v = plt.figure()
#            fig_w = plt.figure(figsize=(15,10))
            fig_w = plt.figure(figsize=(12,8))
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
            from matplotlib.ticker import MultipleLocator, FormatStrFormatter
            majorFormatter = FormatStrFormatter('%2.3f')
            ax_speed.yaxis.set_major_formatter(majorFormatter)
            
            axes_list = [ax_p_gen,ax_q_gen,ax_volt,ax_speed]

            for item_axe in axes_list:
                # Shrink current axis by 20%
                box = ax_speed.get_position()
                item_axe.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                
                





        vip_gen_bus_names = ['bus_{:d}'.format(item) for item in vip_gen_buses]
        
        bus_names = ['bus_{:d}'.format(item) for item in vip_gen_buses]
        sym_names = ['bus_{:d}'.format(item) for item in vip_gen_buses]
  
        ids = vip_gen_bus_names
#        speed_coi = self.data_dict[test_id][bus_names[0]]['speed'] 
        for item_sym in self.data_dict[test_id]['sym']['sym_speed_list']:

            item_number = int(item_sym.split('_')[1])
            
            # generators active power:
            ax_p_gen.plot(self.t, self.data_dict[test_id]['sym'][item_sym]['p_gen']*100.0,
                      label='$\sf p_{{g{:d}}}$'.format(item_number), lw=self.lw)          
  
            # generators reactive power:
            ax_q_gen.plot(self.t, self.data_dict[test_id]['sym'][item_sym]['q_gen']*100.0,
                      label='$\sf q_{{g{:d}}}$'.format(item_number), lw=self.lw)   

            number = int(item_sym.split('_')[1])
            ax_speed.plot(self.t, ((self.data_dict[test_id]['sym'][item_sym]['speed']+1.0)*self.freq_base),
                          label='$\sf \omega_{{{:d}}}$'.format(item_number), lw=self.lw)  
                          
                          
            if self.legends == True:
                for item_axe in axes_list:
                    ax_speed.legend(loc='center left', ncol=2, bbox_to_anchor=(1, 0.5))

        for item_bus in self.data_dict[test_id]['bus']['bus_u_list']:
            # voltages:
            ax_volt.plot(self.t, self.data_dict[test_id]['bus'][item_bus]['u'],
                         label='$\sf v_{{{:d}}}$'.format(item_number), lw=self.lw) 
                         
                         
                         

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

        
        figs_name_list = ['p_gen', 'q_gen','v','w']
        figs_list = [fig_p_gen,fig_q_gen,fig_v,fig_w]

#        figs_name_list = ['w']
#        figs_list = [fig_w]
        
        # assignation of an id for each curve        
        for item_axe in axes_list:
            for id_item, curve in zip(ids,item_axe.get_lines()):
                curve.set_gid(id_item)
                   

        
        for item_fig_name, item_fig in zip(figs_name_list, figs_list):
            
            fig_name = '{:s}_{:s}_{:s}.png'.format(self.test_id,item_fig_name,data_sim)
            fig_png_path = os.path.join(png_dir,fig_name)        
            fig_name = '{:s}_{:s}_{:s}.svg'.format(self.test_id,item_fig_name,data_sim)
            fig_svg_path = os.path.join(svg_dir,fig_name)
            
            item_fig.savefig(fig_png_path)      
            item_fig.savefig(fig_svg_path) 
            
            interactive_svg(item_fig,fig_svg_path,ids, item_fig.axes[0], distance_factor=0.8) 
 
            
            
##        ax_speed.plot(self.t, (speed_coi),label='$\sf \omega_{{{:d}}}$'.format(item_number))   
#
###        ax_speed.set_ylim((48.5,51.5)) *50.0+50.0
###        ax_volt.set_ylim((0.8,1.1))
###        ax_p.set_ylim((2,8))
###        ax_q.set_ylim((-4,8))
#    
        
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

def loc2geojson():
    ''' Converts pss/e bus location file .loc to geojson '''
    print (hola)

    
def psys_map(geo_data, plot_data, ax=None):  
    
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    import json
    import numpy as np
    from scipy.interpolate import griddata
    from matplotlib import cm
    

    
    
    ## Map generation
    geo = json.load(open(geo_data['geojson_file'], 'r'))
    llcrnrlat=geo_data['bottom_lat']
    urcrnrlat=geo_data['top_lat']
    llcrnrlon=geo_data['left_lon']
    urcrnrlon=geo_data['right_lon']
    lat_ts=20
                
                
    m = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h',ax=ax)
                
                
                
    ## System topology (from geojason)                
    from matplotlib.patches import Polygon
#    
#    m.drawcoastlines()
#    m.drawmapboundary(fill_color='#2980b9')
#    m.fillcontinents(color='#ffedcc',lake_color='#2980b9')
#    m.drawstates()
#    m.drawcountries()                  
    
              

 
    for item in geo['features']:
        # lines
        if not item[u'properties'].has_key(u'tag'):            
            item[u'properties'].update({u'tag':''})
            
        if item[u'properties'][u'tag'].has_key(u'power'):
            
            if item[u'properties'][u'tag'][u'power'] == u'line':
                

                coords_list = item[u'geometry'][u'coordinates']
                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]
                
                x, y = m( lons, lats   )

                m.plot(x,y, 'k')     


    for item in geo['features']:
        # substations
        if not item[u'properties'].has_key(u'tag'):            
            item[u'properties'].update({u'tag':''})
            
        if item[u'properties'][u'tag'].has_key(u'power'):
            
            if item[u'properties'][u'tag'][u'power'] == u'substation':

                coords_list = item[u'geometry'][u'coordinates'][0]

                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]
                
                x, y = m( lons, lats )
                xy = zip(x,y)
                facecolor='blue'
                if geo_data.has_key('buses_id'):
                    if geo_data['buses_id'].has_key(int(item[u'properties'][u'id'])):
                        if geo_data['buses_id'][int(item[u'properties'][u'id'])].has_key('facecolor'):
                            facecolor = geo_data['buses_id'][int(item[u'properties'][u'id'])]['facecolor']
                        if geo_data['buses_id'][int(item[u'properties'][u'id'])].has_key('label'):
                            plt.gca().text(x[0],y[0],geo_data['buses_id'][int(item[u'properties'][u'id'])]['label'])
                        
                        
                poly = Polygon( xy, edgecolor=facecolor, facecolor=facecolor, alpha=1.0, lw=2 )
                ax.add_patch(poly)     
                
    map_name = plot_data['map_name']
    out_dir = plot_data['out_dir']
    for item in plot_data['out_formats']:
        plt.savefig(os.path.join(out_dir, 'map_{:s}.{:s}'.format(map_name,item)))
        plt.close()
    return m


def psys_heatmap(test_data, geo_data, plot_data, time, test_dict = {},ax=None):
    '''Creates a heatmap considering geografical data, power system simulation results and grid topology

    
    '''
    from mpl_toolkits.basemap import Basemap
    
    import json
    import numpy as np
    from scipy.interpolate import griddata
    from matplotlib import cm
    

    
    
    ## Map generation
    geo = json.load(open(geo_data['geojson_file'], 'r'))
    llcrnrlat=geo_data['bottom_lat']
    urcrnrlat=geo_data['top_lat']
    llcrnrlon=geo_data['left_lon']
    urcrnrlon=geo_data['right_lon']
    lat_ts=20
                
                
    m = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h',ax=ax)
                
                
                
    ## System topology (from geojason)                
    from matplotlib.patches import Polygon
    
                
                
    for item in geo['features']:
        # substations
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'substation':
                    coords_list = item[u'geometry'][u'coordinates'][0]
                    lons = []
                    lats = []
                    for coord in  coords_list: 
                        
                        lons += [coord[0]]
                        lats += [coord[1]]
                    
                    x, y = m( lons, lats )
                    xy = zip(x,y)
                    poly = Polygon( xy, facecolor='red', alpha=1.0 )
                    plt.gca().add_patch(poly) 
        # lines
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'line':
                coords_list = item[u'geometry'][u'coordinates']
                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]
                
                x, y = m( lons, lats )

                m.plot(x,y, 'r', lw=2) 



    if test_data['resuts_file_type'] == 'hdf5':
        h = hickle.load(test_data['tests_file'])
        
    if test_data['resuts_file_type'] == 'dstxt':
        import pypstools

        ds = pypstools.digsilent_simulation

        test_dict, type_list =  ds.ds_txt_col_2_dict(test_data['tests_file'])
        h = {test_data['test_id']:test_dict}

    if test_data['resuts_file_type'] == 'h_dict':

        h = {test_data['test_id']:test_dict}


    if test_data['resuts_file_type'] == 'raw_dict':
        element = test_data['element']
        variable = test_data['variable']
        ids = test_dict[element]['I']
        h = {test_data['test_id']:{}}
        
        h[test_data['test_id']].update({'sys':{'time':[],
                                        'buses':map(unicode,test_dict['bus']['I'].values)}})
        h[test_data['test_id']].update({element:{}})   
                           
        for item  in test_dict[element]['I'].values:
            a = test_dict[element]
            var_value = (a[variable][a['I'] == item]).values
            
            h[test_data['test_id']][element].update({unicode(item):{variable:{'data':var_value}}})
            
            
            
        
    test_id = test_data['test_id']
    t=np.array(h[test_id]['sys']['time'])
    
    if len(t) <= 1:
        t_index = 0
    else:
        t_index = np.where(t>time)[0][0]
    
    element = test_data['element']
    variable  = test_data['variable']
    
    x_data = []
    y_data = []
    z_data = []
#    h[test_id]['sys']['buses'] = ['bus_{:d}'.format(num) for num in range(1,119)]
    buses = h[test_id]['sys']['buses']
    for item in geo['features']:
        # substations
        if not item[u'properties'].has_key(u'tag'):            
            item[u'properties'].update({u'tag':''})
            
        if item[u'properties'][u'tag'].has_key(u'power'):
            
            if item[u'properties'][u'tag'][u'power'] == u'substation':
#                print(item[u'properties'][u'id'])
#                print(item[u'properties'][u'id'])
#                print(buses[0]==item[u'properties'][u'id'])
                if item[u'properties'][u'id'] in buses:
                    

                    if h[test_id][element].has_key(item[u'properties'][u'id']): 

                        coords_list = item[u'geometry'][u'coordinates'][0]
                        x_d, y_d = m(coords_list[0][0],coords_list[0][1])
                        x_data += [x_d] 
                        y_data += [y_d]
                        x_d, y_d = m(coords_list[2][0],coords_list[2][1])
                        x_data += [x_d] 
                        y_data += [y_d]

                        idx = buses.index(item[u'properties'][u'id'])
#                        print(h[test_id][element])
                        var = h[test_id][element][item[u'properties'][u'id']][variable]['data'][t_index]
                        z_data += [var,var]
#                        print(var)
                        
    
    if plot_data.has_key('z_min'):
        z_min = plot_data['z_min']
    else:
        z_min = np.min(z_data) 
                
    if plot_data.has_key('z_max'):
        z_max = plot_data['z_max']
    else:
        z_max = np.max(z_data)
    
    z_average = (z_min+z_max)/2.0   
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)    
    z_data = np.array(z_data)

    xmargin=0
    ymargin=0
    
    x_min, y_min = m(geo_data['left_lon'],geo_data['bottom_lat'])
    x_max, y_max = m(geo_data['right_lon'],geo_data['top_lat'])
    
    x_add = np.linspace(x_min-xmargin,x_max+xmargin,10)
    y_add = np.linspace(y_min-ymargin,y_max+ymargin,10)
  

#    x_grid, y_grid = meshgrid(x_add, y_add)

    boundary_x = np.hstack((             x_add, y_add*0+x_add[0],  y_add*0+x_add[-1],              x_add))
    boundary_y = np.hstack((x_add*0+min(y_add),            y_add,              y_add,  x_add*0+y_add[-1]))
    boundary_z = np.hstack((boundary_x*0.0))
#    
    x_add = np.hstack((x_data,boundary_x))
    y_add = np.hstack((y_data,boundary_y))
    z_add = np.hstack((z_data,boundary_z))

    x_grid = np.linspace(x_min,x_max,500)
    y_grid = np.linspace(y_min,y_max,500)
    grid_x, grid_y = np.meshgrid(x_grid,y_grid)

    points = np.vstack((x_add,y_add)).T
    
    if plot_data.has_key('mesgrid_interpolation'):
        method = plot_data['mesgrid_interpolation']
    else: method = 'linear'
    
    grid_z = griddata(points, z_add, (grid_x, grid_y), method=method)
    bound_level = 0.8
    bound_delta = 0.005
     
    index = np.where((np.logical_and(grid_z<(bound_level+bound_delta), grid_z>(bound_level-bound_delta))))
    
    print(len(index[0]))
    if len(index[0])>0:
    #    print(grid_z)    
    #    print(index)
    #    print(grid_x[index].shape)
        x_add = np.hstack((x_add,grid_x[index]))
        y_add = np.hstack((y_add,grid_y[index]))
        print(index)
        boundary_z_2 = np.hstack((grid_x[index]*0.0+z_average))
        boundary_z = np.hstack((boundary_x*0.0+z_average))
        z_add = np.hstack((z_data,boundary_z,boundary_z_2))
    
        points = np.vstack((x_add,y_add)).T
    grid_z = griddata(points, z_add, (grid_x, grid_y), method=method)

#    print('z_min:' + str(z_min))
#    print('z_max:' + str(z_max))
    levels =np.linspace(z_min,z_max,20)
#    
    
    lons, lats = m(grid_x,grid_y,inverse=True)
    
    
#    topo = interp(topoin,lons1,lats1,lons,lats,order=1)

#
#
#        
    m.contourf(grid_x, grid_y, grid_z, cmap=cm.RdBu_r, extend='both', levels=levels)   
     
    m.scatter(x_data, y_data, z_data*0.0+1)   
#   
    land_color = '#ffedcc' 
    water_color = '#2980b9'    

    draw_map = True
    if geo_data.has_key('draw_map'):   
        draw_map = geo_data['draw_map']
   
    if draw_map:
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()   
        m.drawmapboundary(fill_color=water_color) 
      
        if geo_data['mask_oceans'] == True:
            print('masking oceans')
            from mpl_toolkits.basemap import maskoceans
            lonpt, latpt = m(grid_x,grid_y,inverse=True)
            grid_z = maskoceans(lonpt, latpt, grid_z, resolution='h', grid=1.25)




#    m.fillcontinents(lake_color=water_color)
    

    
    for item in plot_data['out_formats']:
        out_dir = plot_data['out_dir']
        plt.savefig(os.path.join(out_dir, 'map_' + test_id + '_{0:05d}.png'.format(int(1000*time))))
        plt.close()
       

    return 1
    


def psys_heatmap_add(test_data, geo_data, plot_data, time, test_dict = {},ax=None):
    '''Creates a heatmap considering geografical data, power system simulation results and grid topology

    
    '''
    from mpl_toolkits.basemap import Basemap
    
    import json
    import numpy as np
    from scipy.interpolate import griddata
    from matplotlib import cm
    

    
    
    ## Map generation
    geo = json.load(open(geo_data['geojson_file'], 'r'))
    llcrnrlat=geo_data['bottom_lat']
    urcrnrlat=geo_data['top_lat']
    llcrnrlon=geo_data['left_lon']
    urcrnrlon=geo_data['right_lon']
    lat_ts=20
                
                
    m = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h',ax=ax)
                
                
                
    ## System topology (from geojason)                
    from matplotlib.patches import Polygon
    
                
                
    for item in geo['features']:
        # substations
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'substation':
                    coords_list = item[u'geometry'][u'coordinates'][0]
                    lons = []
                    lats = []
                    for coord in  coords_list: 
                        
                        lons += [coord[0]]
                        lats += [coord[1]]
                    
                    x, y = m( lons, lats )
                    xy = zip(x,y)
                    poly = Polygon( xy, facecolor='red', alpha=1.0 )
                    plt.gca().add_patch(poly) 
        # lines
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'line':
                coords_list = item[u'geometry'][u'coordinates']
                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]
                
                x, y = m( lons, lats )

                m.plot(x,y, 'r', lw=2) 



    if test_data['resuts_file_type'] == 'hdf5':
        h = hickle.load(test_data['tests_file'])
        
    if test_data['resuts_file_type'] == 'dstxt':
        import pypstools

        ds = pypstools.digsilent_simulation

        test_dict, type_list =  ds.ds_txt_col_2_dict(test_data['tests_file'])
        h = {test_data['test_id']:test_dict}

    if test_data['resuts_file_type'] == 'h_dict':

        h = {test_data['test_id']:test_dict}


    if test_data['resuts_file_type'] == 'raw_dict':
        element = test_data['element']
        variable = test_data['variable']
        ids = test_dict[element]['I']
        h = {test_data['test_id']:{}}
        
        h[test_data['test_id']].update({'sys':{'time':[],
                                        'buses':map(unicode,test_dict['bus']['I'].values)}})
        h[test_data['test_id']].update({element:{}})   
                           
        for item  in test_dict[element]['I'].values:
            a = test_dict[element]
            var_value = (a[variable][a['I'] == item]).values
            
            h[test_data['test_id']][element].update({unicode(item):{variable:{'data':var_value}}})
            
            
            
        
    test_id = test_data['test_id']
    t=np.array(h[test_id]['sys']['time'])
    
    if len(t) <= 1:
        t_index = 0
    else:
        t_index = np.where(t>time)[0][0]
    
    element = test_data['element']
    variable  = test_data['variable']
    
    x_data = []
    y_data = []
    z_data = []

    x_centers = []
    y_centers = []
    z_centers = []
    
    N = 200

    x_min, y_min = m(geo_data['left_lon'],geo_data['bottom_lat'])
    x_max, y_max = m(geo_data['right_lon'],geo_data['top_lat'])
    
    x_grid = np.linspace(x_min,x_max,N)
    y_grid = np.linspace(y_min,y_max,N)
    
    grid_x, grid_y = np.meshgrid(x_grid,y_grid)
    
    grid_z = 0.0*grid_x
    
#    h[test_id]['sys']['buses'] = ['bus_{:d}'.format(num) for num in range(1,119)]
    buses = h[test_id]['sys']['buses']
    for item in geo['features']:
        # substations
        if not item[u'properties'].has_key(u'tag'):            
            item[u'properties'].update({u'tag':''})
            
        if item[u'properties'][u'tag'].has_key(u'power'):
            
            if item[u'properties'][u'tag'][u'power'] == u'substation':
#                print(item[u'properties'][u'id'])
#                print(item[u'properties'][u'id'])
#                print(buses[0]==item[u'properties'][u'id'])
                if item[u'properties'][u'id'] in buses:
                    

                    if h[test_id][element].has_key(item[u'properties'][u'id']): 

                        coords_list = item[u'geometry'][u'coordinates'][0]
                        x_d_1, y_d_1 = m(coords_list[0][0],coords_list[0][1])
                        x_data += [x_d_1] 
                        y_data += [y_d_1]
                        x_d_2, y_d_2 = m(coords_list[2][0],coords_list[2][1])
                        x_data += [x_d_2] 
                        y_data += [y_d_2]
                        
                        

                        idx = buses.index(item[u'properties'][u'id'])

                        var = h[test_id][element][item[u'properties'][u'id']][variable]['data'][t_index]
                        z_data += [var,var]
                    
                    x_center = 0.5*(x_d_1 + x_d_2)
                    y_center = 0.5*(y_d_1 + y_d_2)

                    x_centers += [x_center] 
                    y_centers += [y_center]
                    z_centers += [var]        
                    
                    max_dist = 30000.0
#                    it_j = 0
                    for it_i in range(N):    
#                        if np.abs(x_center - grid_x[it_i,it_j]) > max_dist: continue                       
                        for it_j in range(N):
                            if np.abs(x_center - grid_x[it_i,it_j])> max_dist: continue  
                            if np.abs(y_center - grid_y[it_i,it_j])> max_dist: continue
                            dist = ((x_center - grid_x[it_i,it_j])**2.0+(y_center - grid_y[it_i,it_j])**2.0)**0.5
                            z = max_dist-dist
                            if z <= 0.0:
                                z = 0.0
                            grid_z[it_i, it_j] = grid_z[it_i, it_j] + z/max_dist*var
#                    print(dist)
                                

    if plot_data.has_key('z_min'):
        z_min = plot_data['z_min']
    else:
        z_min = np.min(z_data) 
                
    if plot_data.has_key('z_max'):
        z_max = plot_data['z_max']
    else:
        z_max = np.max(z_data)
    
    z_average = (z_min+z_max)/2.0  
                        
    levels =np.linspace(z_min,z_max,20)
   
    lons, lats = m(grid_x,grid_y,inverse=True)
    m.contourf(grid_x, grid_y, grid_z, cmap=cm.RdBu_r, extend='both', levels=levels)     
     
#    m.scatter(x_centers, y_centers, z_centers)   
#   
    land_color = '#ffedcc' 
    water_color = '#2980b9'    

    draw_map = True
    if geo_data.has_key('draw_map'):   
        draw_map = geo_data['draw_map']
   
    if draw_map:
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()   
        m.drawmapboundary(fill_color=water_color) 
      
        if geo_data['mask_oceans'] == True:
            print('masking oceans')
            from mpl_toolkits.basemap import maskoceans
            lonpt, latpt = m(grid_x,grid_y,inverse=True)
            grid_z = maskoceans(lonpt, latpt, grid_z, resolution='h', grid=1.25)




#    m.fillcontinents(lake_color=water_color)
    

    
    for item in plot_data['out_formats']:
        out_dir = plot_data['out_dir']
        plt.savefig(os.path.join(out_dir, 'map_' + test_id + '_{0:05d}.png'.format(int(1000*time))))
        plt.close()
       

    return 1   
#    for item in geo['features']:
#    if item [u'properties'].has_key(u'tag'):
#        if item [u'properties'][u'tag'] == u'substation':
#            coords_list = item[u'geometry'][u'coordinates'][0]
#            lons = []
#            lats = []
#            for coord in  coords_list: 
#                
#                lons += [coord[0]]
#                lats += [coord[1]]
#                
#            bus_num = item[u'properties'][u'name']
#             
#
#            sym_id = 'sym_{:s}'.format(bus_num)
#            
#            if sym_id in h[test_id]['sym']['sym_speed_list']:
#    #                    if h[test_id].has_key(bus_id):
#                u = h[test_id]['sym'][sym_id][variable][t_index]
#                print(u)             
#                x,y,var_array = draw_screen_poly( lats, lons, m, u )
#    #            print(x)
#                X = np.hstack((X, x))
#                Y = np.hstack((Y, y))
#                Z = np.hstack((Z, var_array)) 
#                
                    
                    
  
##    ax = fig.add_subplot(111)
##    m.scatter(X, Y, Z)
##    fig = plt.figure()
##    ax = fig.add_subplot(111) 
#    
##    ax.plot_trisurf(X,Y,U)
##    plt.show()
#    
#    m.drawcoastlines()
#    m.drawstates()
#    
#    # draw parallels and meridians.
#    #m.drawparallels(np.arange(-90.,91.,30.))
#    #m.drawmeridians(np.arange(-180.,181.,60.))
#    m.drawmapboundary(fill_color='aqua', zorder=3) 
#    m.fillcontinents(zorder=1)
#    plt.savefig(png_path)  
##    plt.savefig('pruebas_3d.svg')             

    
#    def interpol_1(X,Y,Z):
#        grid_x, grid_y = np.mgrid[min(X):max(X):10j, min(Y):max(Y):10j]
#        grid_z = grid_x*0.0
#        
#        for i in range(grid_x.shape[0]):
#            for j in range(grid_x.shape[1]):
#                x = grid_x[i,j]
#                y = grid_y[i,j]
#                suma = 0
#                itf = 0
#                for item_x,item_y,item_z in zip(X,Y,Z):
#                    dist_x = abs(x - item_x) 
#                    dist_y = abs(y - item_y) 
#                    dist = (dist_x**2.0 + dist_y**2.0)**0.5
#                    if dist < 10.0:
#                        dist = 10.0
#                    suma +=  item_z*1.0*np.exp(-(dist/100000.0)**2)
#                    itf += 1.0
#                    
#                grid_z[i,j] = suma/itf
#        return grid_x,grid_y,grid_z
        
                    
    #import vector2mesh            
    #grid_x,grid_y,grid_z = vector2mesh.interpol_1(X,Y,Z)
    #plt.contourf(grid_x, grid_y, grid_z)
                    


    


    
              
    #points = np.vstack((X,Y)).T
    #
    #positions = np.vstack([grid_x.ravel(), grid_y.ravel()])
    #values = Z
    #kernel = stats.gaussian_kde(values)
    #ZZ = np.reshape(kernel(positions).T, grid_x.shape)
    #
    #import matplotlib.pyplot as plt
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.imshow(np.rot90(ZZ), cmap=plt.cm.gist_earth_r,
    #          extent=[xmin, xmax, ymin, ymax])
    ##ax.plot(m1, m2, 'k.', markersize=2)
    #ax.set_xlim([xmin, xmax])
    #ax.set_ylim([ymin, ymax])
    #plt.show()
    
    
    #tx = np.linspace(min(X), max(X), 100)
    #ty = np.linspace(min(X), max(Y), 100)
    #XI, YI = np.meshgrid(tx, ty)
    #
    ## use RBF
    ##rbf = Rbf(X, Y, Z, epsilon=1.0)
    ##ZI = rbf(XI, YI)
    #
    ## plot the result
    ##n = plt.normalize(-2., 2.)
    #plt.subplot(1, 1, 1)
    
    #plt.scatter(X, Y, 100, Z, cmap=cm.jet)
    #plt.title('RBF interpolation - multiquadrics')
    ##plt.xlim(0, 1)
    ##plt.ylim(0, 1)
    #plt.colorbar()
    #
    
    
    
    
    
    
    


def heatmap2(yaml_file, mask_oceans = False):

    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    import json
    import numpy as np
    from scipy.interpolate import griddata
    from matplotlib import cm
    
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    
    geo = json.load(open(geojson_path, 'r'))
    llcrnrlat=-5.964
    urcrnrlat=15.904
    llcrnrlon=-10.823
    urcrnrlon=25.118
    lat_ts=20
                
                
    m = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h')
                
    from matplotlib.patches import Polygon

    h = hickle.load(tests_out)
    


    grid_x, grid_y = np.mgrid[m.xmin:m.xmax:200j, m.ymin:m.ymax:200j]  
    
    t=np.array(h[test_id]['sys']['t'])
    t_index = np.where(t>time)[0][0]
    
    def gauss2d(grid_x, grid_y, fwhm = 1.0, center=None):
        """ Make a square gaussian kernel.
        size is the length of a side of the square
        fwhm is full-width-half-maximum, which
        can be thought of as an effective radius.
        """
        x0, y0 = center
    
        
        return np.exp(-4*np.log(2) * ((grid_x-x0)**2 + (grid_y-y0)**2) / fwhm**2) 






    it = 0
    for item in geo['features']:
        if item [u'properties'].has_key(u'tag'):
            if item [u'properties'][u'tag'] == u'substation':
                coords_list = item[u'geometry'][u'coordinates'][0]
                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]
                    
                bus_num = item[u'properties'][u'name']
                 
    
                bus_id = 'bus_{:s}'.format(bus_num)
                if h[test_id].has_key(bus_id):
                    u = h[test_id][bus_id][variable][t_index]
#                    print(u)             
                x,y = m(lons[0],lats[0])
#        if u>10.0:
#            u=10.0
#        if u<-10.0:
#            u=-10.0            
#        print(u)       
        if it == 0:
            grid_z_0 = gauss2d(grid_x, grid_y, fwhm = (m.xmax-m.xmin)*0.1, center=(x,y))*(u-1.0)
        if it > 0:
            grid_z_0 += gauss2d(grid_x, grid_y, fwhm = (m.xmax-m.xmin)*0.1, center=(x,y))*(u-1.0)
            
                
        it += 1
           

#    plt.imshow(np.arctan(10.0*grid_z_0))
    plt.imshow(grid_z_0)
    plt.show()
    
    return grid_z_0
    
    
    
def interpolate1d():
    import matplotlib.pyplot as plt
    from scipy.interpolate import UnivariateSpline, InterpolatedUnivariateSpline
    from scipy import interpolate
    from mpl_toolkits.mplot3d import axes3d
    from scipy.interpolate import griddata
    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.tri as tri
    
    U = np.array([1.1, 1.05, 1.0, 0.9, 0.95, 0.97])
    X = np.array([0.2,  0.4, 0.6, 1.2,  1.3,  1.7])
    Y = np.array([0.3,  0.4, 0.8, 0.9,  1.0,  1.3])
    
    U=np.hstack((1.0,1.0,U,1.0,1.0))
    X=np.hstack((0.0,0.0,X,2.0,2.0))
    Y=np.hstack((0.0,1.5,Y,1.5,0.0))


    #s = UnivariateSpline(X, U, s=1000)
    #s = InterpolatedUnivariateSpline(X, U)
    #s = interpolate.interp1d(X, U)
    s = interpolate.BarycentricInterpolator(X, U)
    s = interpolate.PchipInterpolator(X, U)
    #s = interpolate.PiecewisePolynomial(X, U)
    #s = interpolate.KroghInterpolator(X, U)
    xs = np.linspace(min(X), max(X), 1000)
    us = s(xs)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(X,U)
    ax.plot(xs,us)
    fig.savefig('pruebas_1d.png')


    #s = UnivariateSpline(X, U, s=1000)
    #s = InterpolatedUnivariateSpline(X, U)
    #s = interpolate.interp1d(X, U)
    s = interpolate.BarycentricInterpolator(X, U)
    s = interpolate.PchipInterpolator(X, U)
    #s = interpolate.PiecewisePolynomial(X, U)
    #s = interpolate.KroghInterpolator(X, U)
    
    xs = np.linspace(min(X), max(X), 100)
    
    for i in range(100):
        for k in range(X.shape[0]):
            dist = (X[i] - xs[0])

    us = s(xs)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(X,U)
    ax.plot(xs,us)
    fig.savefig('pruebas_1d_ext.png')
        
    
def interpolate3d():    
    points = np.vstack((X,Y)).T
    values = U
    
    grid_x, grid_y = np.mgrid[min(X):max(X):100j, min(Y):max(Y):200j]
    
    
    grid_z0 = griddata(points, values, (grid_x, grid_y), method='linear')
    
    # Create a custom triangulation
    triang = tri.Triangulation(X, Y)
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, U)
    ax.contourf(grid_x, grid_y, grid_z0, cmap=cm.coolwarm)
    ax.plot_trisurf(X,Y,U)
    plt.show()
    fig.savefig('pruebas_3d.png')    

def test_118_plots():    

    case_dir = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'


    
    datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(0), usemask=True ) 
    gen_thermal_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    
    datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(1), usemask=True ) 
    gen_hydro_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    
    
    datas = np.genfromtxt(os.path.join(case_dir,'tgov_hygov_base.tsv'), skiprows=1, delimiter='\t', usecols=(2), usemask=True ) 
    gen_cond_buses = np.array(datas[np.logical_not(datas.mask)], dtype=np.integer)
    
    vip_gen_buses = list(gen_thermal_buses) + list(gen_hydro_buses) + list(gen_cond_buses)
    #vip_gen_buses = [26,10,87,111,89,61,32]  
    #vip_gen_buses = [26,10] 


    casedir = r'/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'
    tests_out = r'/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/ieee118_v33_modif.hf5'    
    
    
    pub = publish()    
    pub.svg_dir = os.path.join(case_dir,'doc','svg')
    pub.png_dir = os.path.join(case_dir,'doc','png')
    pub.vip_gen_buses = vip_gen_buses
    pub.hdf5file = tests_out
    print(pub.hdf5file)
    pub.plot_pq_w_a_large(u'v_ref_change_26_up')  
    
    
def test_118_omega_animation():
    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.json'
    case_dir = r'/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm'
    tests_out = os.path.join(case_dir,'ieee118_v33_modif.hf5')
    png_path  = os.path.join(case_dir,'doc','png', 't_2.png')
    variable = 'speed'
    time = 0.1
    test_id =  u'test_1'
#    heatmap1(test_id, case_dir, geojson_path, png_path, tests_out, variable, time, mask_oceans = False)
#    grid_z_0 = heatmap2(test_id, case_dir, geojson_path, png_path, tests_out, variable, time, mask_oceans = False)    
    for time in np.linspace(0.5,7.5,150):
        png_path  = os.path.join(case_dir,'doc','png', 'animation_speed', 't_speed_{0:05d}.png'.format(int(1000*time)))
        heatmap1(test_id, case_dir, geojson_path, png_path, tests_out, variable, time, mask_oceans = False)

    #convert -delay 20 -loop 0 *.png myimage.gif



if __name__ == '__main__':
    
    pub = publish()
#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/doc/pub.yaml')
#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/pvsync/pub.yaml')
#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/pvsync/pub_ieee118_10.yaml')
#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/pvsync/pub_ieee118_10_gtrip.yaml')
#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/pvsync/pub_ieee118_1pv_gtrip.yaml')
#    figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/pvsync/ieee12g_pvsync_10/gtrip/pub_ieee12g_10_gtrip.yaml')
#    figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/pvsync/ieee12g_pvsync_10/ltrip/pub_ieee12g_10_ltrip.yaml')
#    figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/pub_ieee12g_10_line_trip.yaml')
    figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/pub_ieee12g_10_bus_fault.yaml')

#    figures = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/pvsync/ieee12g_pvsync_10/gtrip/pub_ieee12g_10_v_ref.yaml')

    yaml_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/geopsys_pvsinc_10.yaml'    
    yaml_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/doc/geopsys_pvsinc_30.yaml'   
##    m = heatmap(yaml_file, mask_oceans = False)
#
#    yaml_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/osm/geopsys.yaml'    
#    m, ya = psys_map(yaml_file, mask_oceans = False)
#    hm = heatmap(yaml_file, mask_oceans = False)
##        
#        
##    test_118_omega_animation()
##    test_118_plots()
    
