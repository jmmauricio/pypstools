# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:09:31 2015

@author: jmmauricio
"""

"""
hexbin is an axes method or pyplot function that is essentially a
pcolor of a 2-D histogram with hexagonal cells.
"""

import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from mpl_toolkits.basemap import Basemap
from pypstools.tools import raw2pandas
import json

raw_file='/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/system/ieee12g_pvsync_10.raw'
raw_df_dict =  raw2pandas(raw_file)

fig = plt.figure()

ax1 = plt.subplot2grid((1,1), (0,0), rowspan=3)


test_dict = {'sys':{'time':np.array([0.0]),
                    'buses':['1','2','3','4']},
             'bus':{'1':{'u':{'data':np.array([1.0 ])}},
                    '2':{'u':{'data':np.array([0.95])}},
                    '3':{'u':{'data':np.array([1.01])}},
                    '4':{'u':{'data':np.array([1.02])}}}
             }



#test_data = {'tests_file':results_path,
#             'test_id':'test1',
#             'element':'bus',
#             'variable':'u',
#             'resuts_file_type':'dict'}

geo_data = {'geojson_file':'./ieee12g_50_pvs.json',
            'bottom_lat':43,  #  south dakota
            'top_lat':46.5,
            'left_lon':-104,
            'right_lon':-98,
            'mask_oceans':True}
           
plot_data = {'type':'absolute_heatmap',
             'z_max':1.03,
             'z_min':0.92,
             'out_dir':'./png',
             'out_formats':['png'],
             'mesgrid_interpolation':'linear'}
             

llcrnrlat=geo_data['bottom_lat']
urcrnrlat=geo_data['top_lat']
llcrnrlon=geo_data['left_lon']
urcrnrlon=geo_data['right_lon']
lat_ts=20
                
                
land_color = '#ffedcc' 
water_color = '#2980b9'    



map1 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
                llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h', ax=ax1)
          



def geo2idx(geo_dict,id,tag):
    it = 0
    index = None
    for item in geo['features']:        
        
        if item['properties'].has_key('tag'):
            if item['properties']['tag'].has_key(tag.keys()[0]):
                
                if item['properties']['tag'][tag.keys()[0]] == tag[tag.keys()[0]]:
                    if item['properties']['id'] == str(id):
                        index = it
                        break
                
        it += 1
    return index


def geo2points(idx):
    it = 0
    index = None
    for item in geo['features']:        
        
        if item['properties'].has_key('tag'):
            if item['properties']['tag'].has_key(tag.keys()[0]):
                
                if item['properties']['tag'][tag.keys()[0]] == tag[tag.keys()[0]]:
                    if item['properties']['id'] == str(id):
                        index = it
                        break
                
        it += 1
    return points_list
    
ids = map(str, range(1,14))

for id in ids:
    tag = {'power':'substation'}
    geo = json.load(open(geo_data['geojson_file'],'r'))
    idx = geo2idx(geo,id,tag)
#    print(geo['features'][idx]['geometry']['coordinates'])
    
    coord = np.array(geo['features'][idx]['geometry']['coordinates'][0])
    ax1.plot(coord[:,0],coord[:,1], 'o')
    

#delta = 0.025
#x = y = np.arange(-3.0, 3.0, delta)
#X, Y = np.meshgrid(x, y)
#Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
#Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
#Z = Z2-Z1  # difference of Gaussians
#
#x = X.ravel()
#y = Y.ravel()
#z = Z.ravel()
#
#if 1:
#    # make some points 20 times more common than others, but same mean
#    xcond = (-1 < x) & (x < 1)
#    ycond = (-2 < y) & (y < 0)
#    cond = xcond & ycond
#    xnew = x[cond]
#    ynew = y[cond]
#    znew = z[cond]
#    for i in range(20):
#        x = np.hstack((x,xnew))
#        y = np.hstack((y,ynew))
#        z = np.hstack((z,znew))
#
#xmin = x.min()
#xmax = x.max()
#ymin = y.min()
#ymax = y.max()
#
#gridsize=30
#
#plt.subplot(211)
#plt.hexbin(x,y, C=z, gridsize=gridsize, marginals=True, cmap=plt.cm.RdBu,
#           vmax=abs(z).max(), vmin=-abs(z).max())
#plt.axis([xmin, xmax, ymin, ymax])
#cb = plt.colorbar()
#cb.set_label('mean value')
#
#
#plt.subplot(212)
#plt.hexbin(x,y, gridsize=gridsize, cmap=plt.cm.Blues_r)
#plt.axis([xmin, xmax, ymin, ymax])
#cb = plt.colorbar()
#cb.set_label('N observations')
#
#plt.show()