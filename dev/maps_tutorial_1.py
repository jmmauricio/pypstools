# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 19:28:35 2015

@author: jmmauricio
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


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

# geographical data
geo ={'sym': {u'U16': {'coordinates': [-70.2147199, -22.1014109]}, 
              u'ANG2': {'coordinates': [-70.366428, -23.0580241]}, 
              u'CTH': {'coordinates': [-70.2632912, -32.9005299]}, 
              u'CTTAR': {'coordinates': [-70.1927888, -20.8053631]}, 
              u'CTM3-TV': {'coordinates': [-70.4118249, -23.089208]}, 
              u'ANG1': {'coordinates': [-70.3667817, -23.0577064]}, 
              u'TG12': {'coordinates': [-65.0515945, -24.7441109]},
              u'CTM2': {'coordinates': [-70.411425, -23.0890095]}, 
              u'TV10': {'coordinates': [-65.0525654, -24.7441937]}, 
              u'CTM1': {'coordinates': [-70.4101927, -23.0894039]}, 
              u'U15': {'coordinates': [-70.2141577, -22.0957479]}, 
              u'U14': {'coordinates': [-70.2144267, -22.0959578]}, 
              u'TG11': {'coordinates': [-65.0519941, -24.744145]}}}

# simulations data
results ={'sym': {u'U16':    {'u':{'data':1.02}}, 
                  u'ANG2':   {'u':{'data':1.00}},
                  u'CTH':    {'u':{'data':1.01}},
                  u'CTTAR':  {'u':{'data':0.99}},
                  u'CTM3-TV':{'u':{'data':0.98}},
                  u'ANG1':   {'u':{'data':1.1}},
                  u'TG12':   {'u':{'data':1.02}},
                  u'CTM2':   {'u':{'data':1.01}},
                  u'TV10':   {'u':{'data':1.0}},
                  u'CTM1':   {'u':{'data':1.0}},
                  u'U15':    {'u':{'data':1.1}},
                  u'U14':    {'u':{'data':0.985}}, 
                  u'TG11':   {'u':{'data':1.0}},}}
              
 
c_list = []     # colors list     
x1_list = []    # x positions list 
y1_list = []    # y positions list 

cm = plt.cm.get_cmap('coolwarm')
  
# conbine geographivcal data with results  
for item in geo['sym']:
    c=1.0
    if item in results['sym']:
        c=results['sym'][item]['u']['data']  
        
    coord = geo['sym'][item]['coordinates']
    
    x1,y1=m(coord[0],coord[1])
    
    c_list += [c]         
    x1_list += [x1]
    y1_list += [y1]
    
# convert lists to numpy arrays
c_array = np.array(c_list)        
x1_array = np.array(x1_list) 
y1_array = np.array(y1_list)   


# scatter plot
s = ax0.scatter( x1_array,y1_array, c=c_array, s=200,cmap=cm)  # scatter plot

# color bar
cb=plt.colorbar(mappable=s, ax=ax0)
cb.set_label('Cbar Label Here')

fig.show()