# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:28:03 2015

@author: jmmauricio
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Polygon

import json

fig = plt.figure()

ax1 = plt.subplot2grid((2,2), (0,0), rowspan=3)
ax2 = plt.subplot2grid((2,2), (0,1))
ax3 = plt.subplot2grid((2,2), (1,1))


geo_data = {'geojson_file':'./geojson_simplified.json',
            'bottom_lat':-25.275,  #  sing
            'top_lat':-17.372,
            'left_lon':-71.960,
            'right_lon':-64.666,
            'mask_oceans':True}
            
plot_data = {'out_dir':'./png',
             'out_formats':['svg'],
             'map_name':'sing_simple'}
             
llcrnrlat=geo_data['bottom_lat']
urcrnrlat=geo_data['top_lat']
llcrnrlon=geo_data['left_lon']
urcrnrlon=geo_data['right_lon']
lat_ts=20
                
                
land_color = '#ffedcc' 
water_color = '#2980b9'    

map1 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h', ax=ax1)
                
map1.drawmapboundary(fill_color=water_color)
map1.fillcontinents(color=land_color, lake_color=water_color)
map1.drawcoastlines()
map1.drawcountries()
map1.drawstates()



llcrnrlon=-70.7574
urcrnrlat=-21.4249
urcrnrlon=-67.8708
llcrnrlat=-23.7175

map2 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h', ax=ax2)

map2.drawmapboundary(fill_color=water_color)
map2.fillcontinents(color=land_color,lake_color=water_color)
map2.drawcoastlines()

llcrnrlon=-69.4865
urcrnrlat=-23.9543
urcrnrlon=-68.7648
llcrnrlat=-24.5203


map3 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h', ax=ax3)

map3.drawmapboundary(fill_color=water_color)
map3.fillcontinents(color=land_color,lake_color=water_color)
map3.drawcoastlines()




import shapefile 

world_countries_shapes = shapefile.Reader('/home/jmmauricio/Documents/private/maps/world/ne_10m_admin_0_countries.shp')
world_states_shapes = shapefile.Reader('/home/jmmauricio/Documents/private/maps/world/ne_10m_admin_1_states_provinces.shp')

it_state = 0
for item in world_states_shapes.fields:
     if item[0] == 'iso_3166_2':
         break
     it_state += 1


it_field = 0
for item in world_countries_shapes.fields:
     if item[0] == 'ISO_A3':
         break
     it_field += 1


state2i = {}
it = 0
for state_sh in world_states_shapes.records():
    state2i.update({state_sh[14]:it})
    it += 1
    
    
ctry2i = {}
it = 0
for ctry_sh in world_countries_shapes.records():
    ctry2i.update({ctry_sh[it_field-1]:it})
    it += 1
    
 
    
facecolor='#f0b37e'  

geo = json.load(open(geo_data['geojson_file'], 'r'))

maps = [map1,map2,map3]
axes = [ax1,ax2,ax3]


for m,ax in zip(maps, axes):
    
    states = ['AR.JY','AR.SA','AR.CT']  
    
    for item in states:
        geo2i = state2i[item]
        sh_points =np.array( world_states_shapes.shapes()[geo2i].points )
        x, y = m( sh_points[:,0], sh_points[:,1] )
        xy = zip(x,y)
        
        poly = Polygon( xy, edgecolor=facecolor, facecolor=facecolor, alpha=1.0, lw=2 )
        ax.add_patch(poly)

    countries= ['BOL','PER']  
        
    for item in countries:
        geo2i = ctry2i[item]
        sh_points =np.array( world_countries_shapes.shapes()[geo2i].points )
        x, y = m( sh_points[:,0], sh_points[:,1] )
        xy = zip(x,y)
        poly = Polygon( xy, edgecolor=facecolor, facecolor=facecolor, alpha=1.0, lw=2 )
        ax.add_patch(poly)
    
    
    
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
                
                if geo_data.has_key('buses_id'):
                    if geo_data['buses_id'].has_key(int(item[u'properties'][u'id'])):
                        if geo_data['buses_id'][int(item[u'properties'][u'id'])].has_key('facecolor'):
                            facecolor = geo_data['buses_id'][int(item[u'properties'][u'id'])]['facecolor']
                        if geo_data['buses_id'][int(item[u'properties'][u'id'])].has_key('label'):
                            ax.text(x[0],y[0],geo_data['buses_id'][int(item[u'properties'][u'id'])]['label'])
                        
                        
                poly = Polygon( xy, edgecolor=facecolor, facecolor=facecolor, alpha=1.0, lw=2 )
                ax.add_patch(poly) 
    
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

                x, y = m( lons, lats )
    
                m.plot(x,y, 'g')    
                
                
#plt.show()
plt.savefig('map.svg')
plt.close()