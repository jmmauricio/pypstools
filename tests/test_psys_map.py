# -*- coding: utf-8 -*-
"""
Example converting ds txt output to python dict and plotting results

Created on Sat Mar 21 12:13:25 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))
import pypstools.publisher as pub


fig, (ax0) = plt.subplots(nrows=1)




geo_data = {'geojson_file':'./geojson.json',
            'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666,
            'mask_oceans':True}

llcrnrlat=geo_data['bottom_lat']
urcrnrlat=geo_data['top_lat']
llcrnrlon=geo_data['left_lon']
urcrnrlon=geo_data['right_lon']
lat_ts=20

m = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
            llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h',ax=ax0)

land_color = '#ffedcc' 
water_color = '#2980b9'    


m.drawcoastlines()
m.drawstates()
m.drawcountries()   
#m.drawmapboundary(fill_color=water_color) 

            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'sing_simple'}
            
            
pub.psys_map(geo_data, plot_data,ax0)

fig.show()

              
                

                