# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:16:00 2015

@author: jmmauricio
"""
import requests
import time

columns = ('year', 'month', 'day', 'hour', 'price_type', 'id_serie', 'price')

url = 'http://www.mainsfrequency.com/frequenz9.php'

fobj = open('out.dat', 'w')
fobj.write('time, freq \n')

fobj.close()

time_prev = 0

while True:
    response = requests.get(url)
    t = response.text.split('<z>')[1].split('</z>')[0]
    
    if t != time_prev:
        freq = response.text.split('<f>')[1].split('</f>')[0]
        fobj = open('out.dat', 'a')
        fobj.write('{:s}, {:s} \n'.format(t,freq))
        
        fobj.close()

        
        
        print(t, freq)
    time_prev = t
    
    time.sleep(0.2)
