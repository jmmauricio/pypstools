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
from scipy.interpolate import griddata
#sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..')))

import pypstools.digsilent_simulation as ds

results_path =  'sing_results.txt'

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


import json

json_path = '/home/jmmauricio/Documents/public/workspace/pypstools/tests/sing.json'
    
geo = {'bus': {u'Sulfuros 69 B3': {'coordinates': [-69.096290720000013, -24.251675799999997]}, 
u'INACESA UGs 13.8 kV': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
u'Aguas Blancas 23 kV': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
u'Esmeralda Centro 23': {'coordinates': [-70.394444916666671, -23.672617049999999]}, 
u'Arica El Aguila Quiborax 13.8': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
u'CD Iquique SUIQ2 3': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
u'Tocopilla 5 A': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
u'Andes Reactor Shunt 345': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
u'Iquique 13.2': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
u'Guayaques 110kV': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
u'Pozo Almonte 13.8 AT2': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
u'Mantos de la Luna 110': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
u'PMG Portada 0.38': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
u'Pozo Almonte 13.8 AT1': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
u'Collahuasi Quebrada Blanca 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
u'Enaex Endesa 110': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
u'CD Arica 13.8': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
u'Angamos 220': {'coordinates': [-70.369284812499984, -23.0679364125]}, 
u'La Huayca 23': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
u'Chuquicamata ACL 100': {'coordinates': [-70.410537419999997, -23.09085726]}, 
u'Chacaya 110kV': {'coordinates': [-70.410537419999997, -23.09085726]}, 
u'Collahuasi 0.4 UGs': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
u'Parinacota 13.8': {'coordinates': [-70.20645687999999, -22.095315919999997]}, 
u'C\xf3ndores Alto Hospicio 110': {'coordinates': [-70.080608699999999, -20.248854219999998]}, 
u'Chuquicamata S/E AA 100': {'coordinates': [-68.918674247368415, -22.304824826315791]},
 u'Zaldivar 66': {'coordinates': [-69.065586679999996, -24.165433520000001]}, 
 u'Radomiro Tomic 23': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'El Tesoro 220': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'Spence 23': {'coordinates': [-69.28147487999999, -22.804628559999998]},
 u'Mejillones 220': {'coordinates': [-70.418908600000009, -23.095216099999998]}, 
 u'C\xf3ndores 110': {'coordinates': [-68.794145619999995, -20.997399179999999]}, 
 u'Pozo Almonte Cerro Colorado 110': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'Nueva Victoria 220': {'coordinates': [-70.20645687999999, -22.095315919999997]}, 
 u'Andes 345': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'C\xf3ndores Drag\xf3n 13.8': {'coordinates': [-70.080608699999999, -20.248854219999998]}, 
 u'Chacaya CTA 15.75': {'coordinates': [-70.410537419999997, -23.09085726]}, 
 u'CD Antofagasta 13.8': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Terminal(5)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Arica 110': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Chuquicamata Chamy 100': {'coordinates': [-70.410537419999997, -23.09085726]}, 
 u'Norgener 220': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Norgener 5.3': {'coordinates': [-70.20645687999999, -22.095315919999997]}, 
 u'Tocopilla 5 C': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'CD Arica 66': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Sairecabur 3.45kV': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Collahuasi 220': {'coordinates': [-68.636380961538464, -20.978630946153842]}, 
 u'C\xf3ndores 13.8': {'coordinates': [-68.794145619999995, -20.997399179999999]}, u'Gaby 220': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
 u'Tamaya 11': {'coordinates': [-69.096290720000013, -24.251675799999997]}, u'CD Arica GMAR 4.16': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Tocopilla 5 E': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Parinacota Chinchorro 13.8': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
 u'Tocopilla 5 D': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Esmeralda Sur 13.8': {'coordinates': [-70.420201279999986, -23.714600699999998]}, 
 u'Escondida Palestina 66': {'coordinates': [-69.104726839999998, -24.252866260000001]}, u'Parinacota Quiani 66': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
 u'Andes 220': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'GNLM 4.16': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Chuquicamata S/E Salar 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'Mantos Blancos 220': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'C\xf3ndores Alto Hospicio 13.8': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Collahuasi 18 UGs 2': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'CD Iquique MSIQ 6.6': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Arica Putre 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Arica Chapiqui\xf1a 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Chuquicamata S/E Salar 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'El Pe\xf1on UGs 6.6': {'coordinates': [-68.693501999999995, -21.981753322222222]}, u'Iquique Cavancha 13.2': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
 u'Chacaya CTM3-TV 11.5': {'coordinates': [-70.410537419999997, -23.09085726]}, u'ENORChile 0.4 B1': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'Laberinto Lomas Bayas 220': {'coordinates': [-69.503542366666665, -23.433070533333332]}, u'Calama 100': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Chacaya 110kV SSAA': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Collahuasi 23 UGs': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'Chuquicamata CT Salar #1 13.8 kV': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Encuentro 220': {'coordinates': [-69.567846560000007, -22.282244420000001]}, 
 u'Lagunas Norte 23': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Atacama TG1A 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'EB Sierra Gorda 110': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'ENORChile 0.4 B2': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'GNLM 110': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'ANG 1 18 kV': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Escondida Coloso 13.8': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 'Tarapac\xe1 220': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'CD Iquique MAIQ 3': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Sierra Miranda 24': {'coordinates': [-65.051433877777782, -24.746907777777778]}, u'Mejillones Michilla 23': {'coordinates': [-70.418908600000009, -23.095216099999998]}, 
 u'Laberinto Minsal 23 B2': {'coordinates': [-69.503542366666665, -23.433070533333332]}, u'Chuquicamata GIS 220': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'CTM2 4.16': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Pozo Almonte Cerro Colorado 12': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'Iquique Cavancha 4.16': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Sulfuros 13.8 #2': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'CD Iquique 13.8': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'C.D. Estandartes 13.2': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Calama Santa Margarita 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'EB2 110 kV': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Inacesa 23 kV': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Aguas Blancas 13.2 kV': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Chacaya CTM1 13.8': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Antofagasta Ivan Zar 13.8': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Alto Norte 110': {'coordinates': [-70.320282271428567, -23.825838185714286]}, u'Atacama TG1B 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Chuquicamata S/E Km-6 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'C\xf3ndores 220': {'coordinates': [-70.080608699999999, -20.248854219999998]}, 
 u'C.D. Estandartes 0.4 B2': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'C.D. Estandartes 0.4 B3': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Chuquicamata S/E 10 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'C.D. Estandartes 0.4 B1': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Tocopilla 5 B': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Antofagasta Ivan Zar 69': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Tocopilla 100/A': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Tocopilla TG3': {'coordinates': [-70.192130233333344, -20.806507299999996]},
 u'Crucero 220 kV B1': {'coordinates': [-69.56765656666667, -22.276635033333335]}, u'Esmeralda Uribe 23': {'coordinates': [-70.420201279999986, -23.714600699999998]}, 
 u'Laberinto Minsal 110': {'coordinates': [-69.503542366666665, -23.433070533333332]}, u'Chuquicamata S/E Km-6 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'CD Iquique TGIQ 11.5': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'CTM3 4.16': {'coordinates': [-70.080608699999999, -20.248854219999998]},
 u'OLAP 69': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Sulfuros 220': {'coordinates': [-69.096290720000013, -24.251675799999997]}, 
 u'Escondida 220 Reactor': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'El Loa 23': {'coordinates': [-68.693501999999995, -21.981753322222222]}, 
 u'Esmeralda Centro 110': {'coordinates': [-70.394444916666671, -23.672617049999999]}, u'Aguas Blancas 0.4 kV': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'C\xf3ndores Pac\xedfico 13.8': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Desalant 6.6': {'coordinates': [-70.080608699999999, -20.248854219999998]}, 
 u'CD Iquique MIIQ4 3': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'Capricornio 110': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'UGs 6.3': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'El Cobre': {'coordinates': [-69.384604980000006, -23.45384636]}, u'ENORChile 13.2': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'Pozo Almonte 66': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'C\xf3ndores Palafitos 110': {'coordinates': [-70.080608699999999, -20.248854219999998]},
 u'Encuentro 23': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Esmeralda Portada 110': {'coordinates': [-70.394444916666671, -23.672617049999999]}, u'Chuquicamata S/E 10A 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'Mejillones 23': {'coordinates': [-70.418908600000009, -23.095216099999998]}, u'El Pe\xf1on UGS 0.4': {'coordinates': [-68.693501999999995, -21.981753322222222]}, u'Tocopilla Booster': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'PAM_Noracid 13.8': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Atacama TG2A 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Chuquicamata GIS 13.8': {'coordinates': [-70.410537419999997, -23.09085726]}, 
 u'Esperanza 220': {'coordinates': [-69.099327900000006, -22.998954700000002]}, u'MMH 23 kV': {'coordinates': [-68.891850779999999, -22.349059019999999]}, u'Laberinto Lomas Bayas 23 #1': {'coordinates': [-69.503542366666665, -23.433070533333332]}, u'Spence 220': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'Fortuna 6.6 B2': {'coordinates': [-69.099327900000006, -22.998954700000002]}, u'Laberinto Oeste 13.2': {'coordinates': [-68.61979654000001, -23.690351219999997]}, 
 u'Crucero 220 B2': {'coordinates': [-69.56765656666667, -22.276635033333335]}, u'S/E Tap Off Barriles 220 kV': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'Licancabur 3.45kV': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Capricornio 13.8': {'coordinates': [-70.216086283333325, -23.457383166666663]},
 u'Tocopilla U12': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Antofagasta El Negro 110': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Tocopilla U10': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Tocopilla U11': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Andes 23 #2': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Andes 23 #3': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Chacaya CTH 15.75': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Andes 23 #1': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'BESS ANDES': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Radomiro Tomic 220': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Pozo Almonte Pampino 24': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Terminal(9)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Esmeralda Portada 23': {'coordinates': [-70.394444916666671, -23.672617049999999]}, u'Escondida Coloso 220': {'coordinates': [-70.470640485714299, -23.763796514285719]}, 
 u'El Tesoro 23': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'tap off B/S2 Reactor Esc.': {'coordinates': [-69.096290720000013, -24.251675799999997]}, u'Arica Chapiqui\xf1a 3': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Lixiviaci\xf3n 13.8 #12': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Lixiviaci\xf3n 13.8 #11': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Ampliacion La Huayca 23 kV': {'coordinates': [-70.320282271428567, -23.825838185714286]}, u'SS/AA CTM1 4.16': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'Escondida UGs Coloso 0.4': {'coordinates': [-69.104726839999998, -24.252866260000001]}, u'Arica 13.8': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Chuquicamata S/E K1 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Salta TV10 15.75': {'coordinates': [-65.051433877777782, -24.746907777777778]}, u'Arica 13.2': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'PMG La Portada 0.38': {'coordinates': [-70.271410900000006, -18.478808239999999]}, u'Tocopilla U16': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'C\xf3ndores Drag\xf3n 110': {'coordinates': [-70.080608699999999, -20.248854219999998]}, 
 u'Chuquicamata S/E Salar 220': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Mejillones 13.8': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'Escondida Laguna Seca 220': {'coordinates': [-69.059877985714294, -24.340941500000003]}, u'Pozo Almonte 220': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'ANG 2 18 kV': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Arica Chapiqui\xf1a 66': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Parinacota Quiani 13.8': {'coordinates': [-70.271410900000006, -18.478808239999999]}, u'Tocopilla 220 B1': {'coordinates': [-70.212150099999988, -22.09896578333333]}, 
 u'Tocopilla 220 B2': {'coordinates': [-70.212150099999988, -22.09896578333333]}, u'Valle de los Vientos 110kV': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Chuquicamata ACL 13.8': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Fortuna 6.6 B1': {'coordinates': [-69.099327900000006, -22.998954700000002]}, u'Tamaya 110': {'coordinates': [-69.096290720000013, -24.251675799999997]}, u'Esperanza UGs 0.4': {'coordinates': [-69.099327900000006, -22.998954700000002]}, u'Parinacota 220': {'coordinates': [-70.271410900000006, -18.478808239999999]}, u'Zald\xedvar Agua Fresca 6.6 1': {'coordinates': [-69.065586679999996, -24.165433520000001]}, u'Atacama TV2C 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Pozo Almonte Tamarugal 66 kV': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'Sierra Miranda 110': {'coordinates': [-65.051433877777782, -24.746907777777778]}, u'Nueva Victoria 66': {'coordinates': [-70.20645687999999, -22.095315919999997]}, 
 u'Lixiviaci\xf3n 13.8 #22': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Chuquicamata S/E 10 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'Lixiviaci\xf3n 13.8 #21': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Zaldivar Agua Fresca 66 - 1': {'coordinates': [-69.065586679999996, -24.165433520000001]},
 u'Antofagasta Pampa 69': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'EB2 6.9 kV': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'Zald\xedvar Agua Fresca 6.6 2': {'coordinates': [-69.065586679999996, -24.165433520000001]}, u'BESS ANDES DC': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Esmeralda Centro 13.8': {'coordinates': [-70.394444916666671, -23.672617049999999]}, u'La Cruz 23': {'coordinates': [-68.822436780000004, -23.441390460000001]},
 u'Esmeralda 220': {'coordinates': [-70.388889425000002, -23.672719899999997]}, u'El Loa 220': {'coordinates': [-68.693501999999995, -21.981753322222222]},
 u'SQM El Loa 220': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'Chacaya CTM3-TG 15': {'coordinates': [-70.410537419999997, -23.09085726]}, 
 u'Tocopilla TG2': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'CD Iquique MIIQ5 3': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'El Loa 110': {'coordinates': [-68.693501999999995, -21.981753322222222]}, 
 u'Chuquicamata Sopladores 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Mantos Blancos 6.3': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'Esperanza 23': {'coordinates': [-69.099327900000006, -22.998954700000002]}, u'Mantos de la Luna 13.2': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'Escondida El Pe\xf1on 6.6': {'coordinates': [-70.470640485714299, -23.763796514285719]}, u'Arica 66': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'CD Arica MIAR 6.6': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'Terminal(6)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Tocopilla 13.8': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Terminal(13)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Tocopilla220': {'coordinates': [-70.212150099999988, -22.09896578333333]}, u'Tarapac\xe1 TGTAR 11.5': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Chuquicamata S/E AA 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'La Cruz 220': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
 u'C\xf3ndores Palafitos 13.8': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Tocopilla TG1': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Esmeralda 110': {'coordinates': [-69.104726839999998, -24.252866260000001]}, u'Mejillones Michilla 110': {'coordinates': [-70.418908600000009, -23.095216099999998]}, 
 u'Esmeralda Sur 110': {'coordinates': [-70.420201279999986, -23.714600699999998]}, u'Laberinto Lomas Bayas 23 #2': {'coordinates': [-69.503542366666665, -23.433070533333332]},
 u'Chuquicamata Sopladores 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Zald\xedvar 220 B1': {'coordinates': [-69.015008699999996, -24.266093983333334]}, 
 u'Zald\xedvar 220 B2': {'coordinates': [-69.065586679999996, -24.165433520000001]}, u'Esperanza UGs 23': {'coordinates': [-69.099327900000006, -22.998954700000002]}, 
 u'Chuquicamata S/E K1 100': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Enaex 110': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'CD Iquique 66': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'Antofagasta 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Laberinto 220 kV': {'coordinates': [-69.409501140000003, -23.44717567]}, u'Parinacota Chinchorro 66': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
 u'Reactor Lab': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'CD Iquique SUIQ3 3': {'coordinates': [-70.216086283333325, -23.457383166666663]}, 
 u'PAM Noracid 13.8 (trafo)': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Pozo Almonte Tamarugal 23': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'Esmeralda Uribe 110': {'coordinates': [-70.420201279999986, -23.714600699999998]}, u'CTM1 4.16': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Nueva Zaldivar 220 kV': {'coordinates': [-69.06477043999999, -24.163288659999999]}, u'La Cruz 66': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Esmeralda 13.8': {'coordinates': [-69.104726839999998, -24.252866260000001]}, u'MolyCop 13.8': {'coordinates': [-68.891850779999999, -22.349059019999999]}, 
 u'Norgener NTO1 13.8': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Condensador ELECDA Calama': {'coordinates': [-68.794145619999995, -20.997399179999999]}, 
 u'Tocopilla U15': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Capricornio 23': {'coordinates': [-70.216086283333325, -23.457383166666663]}, u'Norgener NTO2 13.8': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'MMH 220 kV': {'coordinates': [-68.891850779999999, -22.349059019999999]}, u'Laberinto Oeste 110': {'coordinates': [-68.61979654000001, -23.690351219999997]}, u'Enaex 0.4': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Tarapac\\xe1 220': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Chuquicamata CT Salar #2 13.8 kV': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Tocopilla U13': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Terminal(12)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Terminal(7)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Parinacota Pukar\xe1 66': {'coordinates': [-70.271410900000006, -18.478808239999999]}, u'Chuquicamata S/E 10A 13.8': {'coordinates': [-68.918674247368415, -22.304824826315791]}, 
 u'Antofagasta Pampa 0.4': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Reactor L2': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Mejillones 110': {'coordinates': [-69.693897800000002, -20.815454819999999]}, u'Desalant 110': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Terminal(4)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Atacama TG2B 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Salta TG12 15.75': {'coordinates': [-65.051433877777782, -24.746907777777778]}, u'EB1 13.8 kV': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Pozo Almonte La Cascada 66': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'nuev': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'MolyCop 220': {'coordinates': [-68.891850779999999, -22.349059019999999]}, 
 u'Lagunas 23': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'EB Sierra Gorda 220': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'El Abra 220': {'coordinates': [-68.693501999999995, -21.981753322222222]}, 
 u'Enaex 4.16': {'coordinates': [-69.098473180000013, -22.926520840000002]}, 
 u'SS/AA CTM2 4.16': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'Reactor Crucero 220': {'coordinates': [-69.77449956000001, -20.257194300000002]}, 
 u'C\xf3ndores Pac\xedfico 110': {'coordinates': [-70.080608699999999, -20.248854219999998]}, u'Pozo Almonte 24': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Collahuasi Quebrada Blanca 220': {'coordinates': [-68.794145619999995, -20.997399179999999]}, 
 u'Chuquicamata Chamy 13.8': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Chuquicamata S/E Km-6 UGs 6.6': {'coordinates': [-68.918674247368415, -22.304824826315791]}, u'Parinacota 66': {'coordinates': [-70.271410900000006, -18.478808239999999]}, u'Terminal(1)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Escondida El Pe\xf1on 66': {'coordinates': [-70.470640485714299, -23.763796514285719]}, u'SS/AA CTM3 4.16': {'coordinates': [-69.28147487999999, -22.804628559999998]}, u'Chacaya CTM2 15': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Gas Atacama 220': {'coordinates': [-70.417396214285716, -23.092590671428574]}, u"Escondida O'Higgins 220": {'coordinates': [-70.214590150000006, -23.692520583333334]}, 
 u'Chuquicamata GIS 100': {'coordinates': [-70.410537419999997, -23.09085726]}, u'Antucoya 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Iquique 66': {'coordinates': [-68.822436780000004, -23.441390460000001]}, 
 u'Atacama TV1C 15': {'coordinates': [-68.585278271428578, -24.01610494285714]}, u'Nueva Victoria 23 1': {'coordinates': [-70.20645687999999, -22.095315919999997]}, u'Escondida Domeyko 220': {'coordinates': [-69.102423979999998, -24.24364898]}, 
 u'El Abra 23': {'coordinates': [-68.693501999999995, -21.981753322222222]}, u'Terminal(11)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, 
 u'Escondida Oxidos 220': {'coordinates': [-69.104726839999998, -24.252866260000001]}, u'Salta TG11 15.75': {'coordinates': [-65.051433877777782, -24.746907777777778]}, 
 u'Tap Off Llanos': {'coordinates': [-69.096290720000013, -24.251675799999997]}, u'Antofagasta 110': {'coordinates': [-68.585278271428578, -24.01610494285714]}, 
 u'Terminal(8)': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Mantos Blancos 23': {'coordinates': [-69.693897800000002, -20.815454819999999]}, 
 u'S/E Tap Off Salar del Carmen 110 kV': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'Pozo Almonte 13.8 AT5': {'coordinates': [-70.271410900000006, -18.478808239999999]}, 
 u'Escondida Bombeo 4.16 #2': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Escondida Bombeo 4.16 #3': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Escondida Bombeo 4.16 #4': {'coordinates': [-69.098473180000013, -22.926520840000002]}, u'Tocopilla U14': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Guayaques 3.45kV': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Pozo Almonte Dolores 24': {'coordinates': [-69.77449956000001, -20.257194300000002]}, u'INACESA UGs  23 kV': {'coordinates': [-68.822436780000004, -23.441390460000001]}, u'Laberinto Minsal 23 B1': {'coordinates': [-69.503542366666665, -23.433070533333332]}, 
 u'Chacaya 220': {'coordinates': [-70.410537419999997, -23.09085726]}, u'CD Iquique SUIQ1 3': {'coordinates': [-70.216086283333325, -23.457383166666663]},
 u'Tarapac\xe1 CTTAR 13.8': {'coordinates': [-70.192130233333344, -20.806507299999996]}, u'Antofagasta La Negra 23': {'coordinates': [-68.585278271428578, -24.01610494285714]}}, 'sym': {u'U16': {'coordinates': [-70.2147199, -22.1014109]}, u'TV1C': {'coordinates': [-70.4165653, -23.0909524]}, u'TV2C': {'coordinates': [-70.4174342, -23.0914427]}, u'ANG2': {'coordinates': [-70.366428, -23.0580241]}, u'TG1B': {'coordinates': [-70.4165561, -23.0911168]}, u'CTH': {'coordinates': [-70.2632912, -32.9005299]}, 
 u'NTO1': {'coordinates': [-70.2098045, -22.0959447]}, u'TG2A': {'coordinates': [-70.4179641, -23.0915108]}, u'CTTAR': {'coordinates': [-70.1927888, -20.8053631]}, 
 u'CTM3-TV': {'coordinates': [-70.4118249, -23.089208]}, u'TG1A': {'coordinates': [-70.4170275, -23.0911367]}, u'ANG1': {'coordinates': [-70.3667817, -23.0577064]}, 
 u'TG12': {'coordinates': [-65.0515945, -24.7441109]}, u'NTO2': {'coordinates': [-70.2102858, -22.0962333]}, u'CTM2': {'coordinates': [-70.411425, -23.0890095]}, 
 u'TV10': {'coordinates': [-65.0525654, -24.7441937]}, u'TG2B': {'coordinates': [-70.4174558, -23.091318]}, u'CTM1': {'coordinates': [-70.4101927, -23.0894039]}, u'U15': {'coordinates': [-70.2141577, -22.0957479]}, u'U14': {'coordinates': [-70.2144267, -22.0959578]}, u'TG11': {'coordinates': [-65.0519941, -24.744145]}}}

          
p_list = []     # colors list  
q_list = []     # colors list   
c_list = []     # colors list     
x1_list = []    # x positions list 
y1_list = []    # y positions list 
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
        x1_list += [x1]
        y1_list += [y1]
        labels_syms +=[item]
    
syms_p = ax0.scatter( x1_list,y1_list, c=p_list, s=p_list,cmap=cm )  # scatter plot
#syms_q = ax0.scatter( x1_list,y1_list, c=q_list, s=q_list,cmap=cm )  # scatter plot


z_list = []     # colors list     
x_list = []    # x positions list 
y_list = []    # y positions list 
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
            z_list += [c]         
            x_list += [x1]
            y_list += [y1]
    
# convert lists to numpy arrays
z_data = np.array(z_list)        
x_data = np.array(x_list) 
y_data = np.array(y_list)   



#splot = ax0.scatter( x1_array,y1_array, c=c_array, s=200,cmap=cm )  # scatter plot

# color bar
#cb=plt.colorbar(mappable=syms_p, ax=ax0)
#cb.set_label('Cbar Label Here')

#fig.show()



xmargin=0
ymargin=0

x_min, y_min = m(geo_data['left_lon'],geo_data['bottom_lat'])
x_max, y_max = m(geo_data['right_lon'],geo_data['top_lat'])

x_add = np.linspace(x_min-xmargin,x_max+xmargin,10)
y_add = np.linspace(y_min-ymargin,y_max+ymargin,10)
  

#    x_grid, y_grid = meshgrid(x_add, y_add)

boundary_x = np.hstack((             x_add, y_add*0+x_add[0],  y_add*0+x_add[-1],              x_add))
boundary_y = np.hstack((x_add*0+min(y_add),            y_add,              y_add,  x_add*0+y_add[-1]))
boundary_z = np.hstack((boundary_x*0.0))+1.0

border = np.array([
#[94521.476730,53150.387758,1.000000],
#[92210.590306,124787.866910,1.000000],
#[101454.136003,177938.254668,1.000000],
#[101454.136003,249575.733820,1.000000],
#[115319.454548,321213.212971,1.000000],
#[138428.318791,406716.010669,1.000000],
#[143050.091639,487597.035518,1.000000],
#[143050.091639,586965.151761,1.000000],
#[140739.205215,667846.176610,1.000000],
#[136117.432367,741794.542186,1.000000],
#[136117.432367,845784.431277,1.000000],
#[203133.138670,859649.749823,1.000000],
#[320988.346307,885069.500490,1.000000],
#[353340.756246,831919.112732,1.000000],
#[374138.734065,746416.315034,1.000000],
#[397247.598307,670157.063034,1.000000],
#[422667.348974,570788.946791,1.000000],
#[436532.667520,499151.467639,1.000000],
#[519724.578793,402094.237820,1.000000],
#[542833.443035,323524.099396,1.000000],
#[662999.537097,279617.257335,1.000000],
#[734637.016249,279617.257335,1.000000],
#[119941.227397,20797.977818,1.000000],
#[193889.592973,20797.977818,1.000000],
#[272459.731398,20797.977818,1.000000],
#[337164.551277,27730.637091,1.000000],
#[390314.939035,27730.637091,1.000000],
#[464263.304611,27730.637091,1.000000],
#[635268.900006,27730.637091,1.000000],
#[706906.379157,39285.069212,1.000000],
#[755434.994067,298104.348729,1.000000],
#[750813.221218,605452.243155,1.000000],
#[723082.584127,864271.522671,1.000000],
[235485.548609,688644.154428,1.000000],
])


border_x = border[:,0]
border_y = border[:,1]
border_z = border[:,2]

#
#x_add = np.hstack((x_data,boundary_x,border_x))
#y_add = np.hstack((y_data,boundary_y,border_y))
#z_add = np.hstack((z_data,boundary_z,border_z))

x_add = np.hstack((x_data,border_x))
y_add = np.hstack((y_data,border_y))
z_add = np.hstack((z_data,border_z))

#x_add = np.hstack((x_data))
#y_add = np.hstack((y_data))
#z_add = np.hstack((z_data))

x_grid = np.linspace(x_min,x_max,500)
y_grid = np.linspace(y_min,y_max,500)

grid_x, grid_y = np.meshgrid(x_add,y_add)

points = np.vstack((x_add,y_add)).T

method = 'linear'
method = 'cubic'

grid_z = griddata(points, z_add, (grid_x, grid_y), method=method)

import scipy
from scipy.interpolate import Rbf  
interp2d =   scipy.interpolate.CloughTocher2DInterpolator(points, z_add, tol=1e-6)

#Creating the interpolation function and populating the output matrix value  
#interp2d = Rbf(x_add, y_add, z_add) 

#grid_z = interp2d(grid_x, grid_y )  


def onclick(event):
    x,y =  (event.xdata, event.ydata)
    print('[{:f},{:f},{:f}],'.format(x, y,1.0))

cid = fig.canvas.mpl_connect('button_press_event', onclick)


ax0.contourf(grid_x, grid_y, grid_z, cmap=cm)       

# scatter plot
bus_u = ax0.scatter( x_add,y_add, c=z_add, s=100,cmap=cm)  # scatter plot

tooltip = mpld3.plugins.PointLabelTooltip(bus_u, labels=labels_buses)
mpld3.plugins.connect(fig, tooltip)

html = mpld3.fig_to_html(fig)

fobj = open('prueba.html','w')

fobj.write(html)
fobj.close()

fig.show()



    
    