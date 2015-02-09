'''


gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o vector2mesh.so vector2mesh.c
'''
from __future__ import division
import numpy as np

cimport numpy as np

DTYPE = np.int

ctypedef np.int_t DTYPE_t

def interpol_1(X,Y,Z):
    cdef double suma
    cdef double itf
    cdef int i
    cdef int j    
    cdef double dist_x
    cdef double dist_y
    cdef double dist
    cdef double item_x
    cdef double item_y
    cdef double item_z
    
    cdef np.ndarray grid_x = np.zeros(100, dtype=DTYPE)
    cdef np.ndarray grid_y = np.zeros(100, dtype=DTYPE)    
    cdef np.ndarray grid_z = np.zeros(100, dtype=DTYPE)
    
    grid_x, grid_y = np.mgrid[min(X):max(X):100j, min(Y):max(Y):100j]
    grid_z = grid_x*0.0
    
    for i in range(100):
        for j in range(100):
            x = grid_x[i,j]
            y = grid_y[i,j]
            suma = 0.0
            itf = 0.0
            for item_x,item_y,item_z in zip(X,Y,Z):
                
                dist_x = np.abs(x - item_x) 
                dist_y = np.abs(y - item_y) 
                
                dist = (dist_x**2.0 + dist_y**2.0)**0.5
                
                if dist < 10.0:
                    dist = 10.0
                    
                suma +=  item_z*1.0*np.exp(-(dist/100000.0)**2)
                itf += 1.0
                
            grid_z[i,j] = suma/itf
    return grid_x,grid_y,grid_z
