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

from pypstools.tools import raw2pandas
raw_file='/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/system/ieee12g_pvsync_10.raw'
raw_df_dict =  raw2pandas(raw_file)

fig = plt.figure()

ax1 = plt.subplot2grid((2,2), (0,0), rowspan=3)

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