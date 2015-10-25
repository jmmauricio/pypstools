# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 19:28:35 2015

@author: jmmauricio
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import mpld3
import json 

#sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))

import pypstools.digsilent_simulation as ds




json_path = 'simple_sing.json'
results_path =  'sing_results.txt'

geo = json.load(open(json_path,'r'))

test_dict =  ds.ds_2_dict(results_path)

fig, (ax0) = plt.subplots(nrows=1)   # creates a figure with one axe

geo_data = {'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666}
            

# map creation:            
m = Basemap(projection='merc',
            llcrnrlat=geo_data['bottom_lat'],
            urcrnrlat=geo_data['top_lat'],
            llcrnrlon=geo_data['left_lon'],
            urcrnrlon=geo_data['right_lon'],
            lat_ts=20,resolution='h',ax=ax0)
                
                
# just to define colors:
land_color = '#ffedcc'   
water_color = '#2980b9'    
            
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents(color=land_color, lake_color=water_color,zorder=0)   
m.drawmapboundary(fill_color=water_color)


    

for item in geo['line']:
    lons = geo['line'][item]['coordinates'][0]
    lats = geo['line'][item]['coordinates'][1]
    x,y = m(lons,lats)
    lines_u = ax0.plot( x,y, 'k', lw=2.0, zorder=1)  # scatter plot
        
p_list = []     # colors list  
q_list = []     # colors list   
c_list = []     # colors list     
x_syms_list = []    # x positions list 
y_syms_list = []    # y positions list 
labels_syms = []
cm = plt.cm.get_cmap('coolwarm')
idx = 0
        
## conbine geographivcal data with results  
for item in geo['sym']:
    c=1.0
    if item in test_dict['sym']:
        c=test_dict['sym'][item]['ut']['data'][idx]
        p=test_dict['sym'][item]['p']['data'][idx]
#        q=test_dict['sym'][item]['q']['data'][idx]
        coord = geo['sym'][item]['coordinates']
        
    #    print('{:s}: {:2.3f}'.format(item,c))
        x1,y1=m(coord[0],coord[1])
        
        p_list += [p]
#        q_list += [q]         
        x_syms_list += [x1]
        y_syms_list += [y1]
        labels_syms +=[item]
 
p_array = np.array(p_list)        
x_syms_array = np.array(x_syms_list) 
y_syms_array = np.array(y_syms_list)  
  
#syms_p = ax0.scatter( x_syms_array,p_array, c=p_list, s=p_list,cmap=cm )  # scatter plot
#syms_q = ax0.scatter( x1_list,y1_list, c=q_list, s=q_list,cmap=cm )  # scatter plot


c_list = []     # colors list     
x1_list = []    # x positions list 
y1_list = []    # y positions list 
labels_buses = []
# conbine geographivcal data with results  
for item in geo['bus']:
    c=1.0
    

    if item in test_dict['bus']:
        
        if 'm:u in p.u.' in test_dict['bus'][item]:
            c=test_dict['bus'][item]['m:u in p.u.']['data'][idx]
        elif 'u' in test_dict['bus'][item]:
            c=test_dict['bus'][item]['u']['data'][idx]
                
        if not c==0.0:                
            print(item,c)
            coord = geo['bus'][item]['coordinates']
    
        
            x1,y1=m(coord[0],coord[1])
            labels_buses += ['{:s}: \n{:2.3f} p.u.'.format(item,c)]
            c_list += [c]         
            x1_list += [x1]
            y1_list += [y1]

item = 'Salta 345'
coord = geo['bus'][item]['coordinates']
x1,y1=m(coord[0],coord[1])
labels_buses += ['{:s}: \n{:2.3f} p.u.'.format(item,c)]
c_list += [c]         
x1_list += [x1]
y1_list += [y1]
    
# convert lists to numpy arrays
c_array = np.array(c_list)        
x1_array = np.array(x1_list) 
y1_array = np.array(y1_list)   

v_min = np.min(c_array)
v_max = np.max(c_array)

# scatter plot
bus_u = ax0.scatter( x1_array,y1_array, c=c_array, s=100,cmap=cm, vmax=v_max, vmin=v_min, zorder=2)  # scatter plot
#splot = ax0.scatter( x1_array,y1_array, c=c_array, s=200,cmap=cm )  # scatter plot

# color bar
cb=plt.colorbar(mappable=bus_u, ax=ax0)
cb.set_label('Cbar Label Here')


tooltip = mpld3.plugins.PointLabelTooltip(bus_u, labels=labels_buses)
mpld3.plugins.connect(fig, tooltip)

html = mpld3.fig_to_html(fig)

fobj = open('prueba.html','w')

fobj.write(html)
fobj.close()