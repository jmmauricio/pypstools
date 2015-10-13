from highcharts import Highmap
from highcharts.highmaps.highmap_helper import jsonp_loader, js_map_loader, geojson_handler, interpolateRGB

H = Highmap(height=550)
map_url = 'http://code.highcharts.com/mapdata/countries/cl/cl-all.js'
data_url = 'http://www.highcharts.com/samples/data/jsonp.php?filename=us-capitals.json&callback=?'
geojson = js_map_loader(map_url)
data = [{u'lon': -86.300629, u'abbrev': u'AL', u'capital': u'Montgomery', u'lat': 32.38012, 'z': 205764, u'parentState': u'Alabama', u'population': 205764}, 
        {u'lon': -92.274494, u'abbrev': u'AR', u'capital': u'Little Rock', u'lat': 34.748655, 'z': 193524, u'parentState': u'Arkansas', u'population': 193524}, 
        ]


# geographical data
geo ={'sym': {u'U16': {'coordinates': [-70.2147199, -22.1014109]}, 
              u'ANG2': {'coordinates': [-70.366428, -23.0580241]}, 
              u'CTH': {'coordinates': [-70.2632912, -23.9005299]}, 
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
                  

data = []
                 
for item in geo['sym'].keys():
    
    data += [{u'lon': geo['sym'][item]['coordinates'][0],
              u'lat': geo['sym'][item]['coordinates'][1],
              u'abbrev': item, 
              u'capital': item, 
              'z': results['sym'][item]['u']['data'], 
              u'parentState':item, 
              u'population': results['sym'][item]['u']['data']}]
    
                    
options = {
    'title': {
            'text': 'Highmaps lat/lon demo'
        },

    'tooltip': {
        'formatter': "function () {\
                            return this.point.capital + ', ' + this.point.parentState + '<br>Lat: ' + this.point.lat + ' Lon: ' + this.point.lon + '<br>Population: ' + this.point.population;\
                        }",
        'crosshairs': [{
            'zIndex': 5,
            'dashStyle': 'dot',
            'snap': False,
            'color': 'gray'
        }, {
            'zIndex': 5,
            'dashStyle': 'dot',
            'snap': False,
            'color': 'gray'
        }]
    },
}

max_p = max([item['population'] for item in data])

for item in data:
    item.update({'z':item['population']})
    item.update({'color':interpolateRGB([0,10,255],[255,10,0],item['population']/max_p)})

H.add_map_data(geojson, name='Basemap' ,borderColor='#606060',
            nullColor='rgba(200, 200, 200, 0.2)',
            showInLegend=False) 
H.add_data_set(geojson_handler(geojson, 'mapline'),
    'mapline','Separators', showInLegend=False, enableMouseTracking=False)    
H.add_data_set(data,'mapbubble','Cities', dataLabels={
                    'enabled': True,
                    'format': '{point.capital}'
                }, maxSize='12%', is_coordinate=True)

H.set_dict_options(options)


fobj = open('/home/jmmauricio/Documents/public/workspace/pypstools/dev/high/map.html', 'w')
fobj.write(H.htmlcontent)

fobj.close()
