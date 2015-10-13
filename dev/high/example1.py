# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:50:52 2015

@author: jmmauricio
"""

"""
Basic example for highmaps module in python-highcharts
As in highcharts, datasets need to input using "add_data_set" method.
Options can be either set by the "set_options" method as shown here or
by constructing a option dictionary object and input using "set_dict_options" method (recommended)
In highmaps, the map data can be input in multiple ways:
1. add_map_data method: (recommended)
    add_map_data(geojson, **kwargs)
    set map directly to the input (geojson) data 
    geojson is the map data in geojson format
2. set_map_source method:
    set_map_source(map_src, jsonp_map = False)
    map_src is the url (https) where map data is located,
    it is recommended to get map data from highcharts' map collection: 
    https://code.highcharts.com/mapdata/
    jsonp_map is boolean parameter if mapdata is loaded from jsonp
    geojson (from jsonp) or .js are accepted formats. 
    default is javascript (.js) format (from highcharts)
The following example is from Highmaps Demos
GeoJSON areas: http://www.highcharts.com/maps/demo/geojson
"""

from highcharts import Highmap
H = Highmap(width = 650, height = 500)

options = { # construct option dict
                                   
    'chart' :{ 'renderTo' : 'container'
    },
                           
    'title' : {
        'text' : 'GeoJSON in Highmaps'
    },

    'mapNavigation': {
        'enabled': True,
        'buttonOptions': {
            'verticalAlign': 'bottom'
        }
    },

    'colorAxis': {
    },
} 

data = [ # input dataset 
    {
        "code": "CL.TA",
        "value": 728
    },
        {
        "code": "CL.AN",
        "value": 200
    },
]
H.set_dict_options(options) # set options
H.add_data_set(data, 'map', 'Random data', joinBy=['code_hasc', 'code'], # set dataset
                states={
                    'hover': {
                        'color': '#BADA55'
                    }
                },
                dataLabels={
                    'enabled': True,
                    'format': '{point.properties.postal}'
                })

H.set_map_source('http://code.highcharts.com/mapdata/countries/cl/cl-all.js', False) # set map data from the src (jsonp)



fobj = open('/home/jmmauricio/Documents/public/workspace/pypstools/dev/high/map.html', 'w')
fobj.write(H.htmlcontent)

fobj.close()
