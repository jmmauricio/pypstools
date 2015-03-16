# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:17:50 2015

@author: jmmauricio
"""

import sys,os

sys.path.append(os.path.join('..','pypstools'))

import publisher

pub = publisher.publish()


#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_30/bus_fault/pub_ieee12g_30_bus_fault.yaml')
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_50/bus_fault/pub_ieee12g_50_bus_fault.yaml')


#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/gen_trip/pub_ieee12g_10_gen_trip.yaml')
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_30/gen_trip/pub_ieee12g_30_gen_trip.yaml')
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_50/gen_trip/pub_ieee12g_50_gen_trip.yaml')

#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/load_trip/pub_ieee12g_10_load_trip.yaml')

# plots ok
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/load_trip/pub_ieee12g_10_load_trip.yaml')
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/gen_trip/pub_ieee12g_10_gen_trip.yaml')
#figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/bus_fault/pub_ieee12g_10_bus_fault.yaml')
figures,h_tests = pub.publisher('/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/doc/source/pvsync/ieee12g_pvsync_10/line_trip/pub_ieee12g_10_line_trip.yaml')