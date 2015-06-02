""" Tools for dealing with power system data and results.

(c) 2015 Juan Manuel Mauricio
"""

import numpy as np
import scipy.linalg
import scipy.integrate
import pandas as pd
import h5py
from StringIO import StringIO

def dict_to_h5(file_name, dict_in, dict_deepness=3):  
    ''' Saves a dictionary to hdf5 file

    >>> a=2
    >>> b=3
    >>> c=np.array([1,2,3,4])
    >>> t=np.array([.1,.2,.3,.4])
    >>> data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    >>> file_name = 'foo.hdf5'
    >>> dict2h5(file_name, data_dict) 

    '''        
    f = h5py.File(file_name,'w')
    
    if dict_deepness==3:
        for test in dict_in:

            grp = f.create_group(test)
            for group in dict_in[test]:

                sub_grp = grp.create_group(group)
                for data in dict_in[test][group]:
                    var_name = data
                    var_values =  dict_in[test][group][data]

                    sub_grp.create_dataset(var_name, data=var_values)
                
        f.close()

def h5_to_dict(file_name, dict_deepness=3):  
    ''' Saves a dictionary to hdf5 file

    >>> a=2
    >>> b=3
    >>> c=np.array([1,2,3,4])
    >>> t=np.array([.1,.2,.3,.4])
    >>> data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    >>> file_name = 'foo.hdf5'
    >>> dict_to_h5(file_name, data_dict) 

    '''        
    h5 = h5py.File(file_name,'r')
    
    if dict_deepness==3:
        for test in dict_in:

            grp = f.create_group(test)
            for group in dict_in[test]:

                sub_grp = grp.create_group(group)
                for data in dict_in[test][group]:
                    var_name = data
                    var_values =  dict_in[test][group][data]

                    sub_grp.create_dataset(var_name, data=var_values)
                
        f.close()

        return dict_out

def loc2geojson(loc_path, geojson_path,bus_1,bus_2,bus_1_2_dist, bus_1_lon_lat):
    '''Converts PSS/E .loc file to geoJSON file
    
    Type: Function of tools module

    ----
    
    Converts .loc PSS/E location file to geojson file.
    
    Parameters
    ----------
    loc_path : string 
               .loc file path
    
    geojson_path : string
               .geojson file path
    
    bus_1 : int
            first buss to consider for scaling and positioning
    
    bus_2 : int            
            second bus to consider for scaling
    
    
    bus_1_2_dist : double
                   distance  in meters between bus_1 and bus_2
    
    bus_1_lon_lat : tuple of doubles
                    bus_1 position in (longitude,latitude) degrees.
    
    
    Returns
    -------
    feat_geo_buses : dict 
                     geojson format for buses
    feat_geo_branches : dict 
                     geojson format for branches
    feat_geo_total : dict 
                     geojson format for the total system
    
    Example
    -------

    >>> from pypstools.tools import loc2geojson
    >>> loc_path = 'ieee12g_50_pvs.loc'
    >>> geojson_path = 'ieee12g_50_pvs.json'        
    >>> bus_1,bus_2 = 9,4
    
    >>> bus_1_lon_lat = (-101,44)  #  south dakota
    >>> bus_1_2_dist = 500.0e3
    
    >>> feat_geo_buses, feat_geo_branches, feat_geo_total = loc2geojson(loc_path, geojson_path,bus_1,bus_2,bus_1_2_dist, bus_1_lon_lat)
    
    '''    
    
    import geojson
    
    loc_file = open(loc_path, 'r')

    
    reading_buses = False
    reading_branches = False
    feat_geo_buses_list = []  
    feat_geo_branches_list = [] 
    

    for row in loc_file.readlines():

        if (reading_buses == True) and (ord(row[0]) == 13):

            reading_buses = False
        
        if reading_buses == True:
            
            x = 11.80
            y =  4.30
            angle =  90.0/180.0*np.pi  
            length = 0.80
            width = 0.02
            
            bus_id, x, y, angle, length = row.split()
            
            x = float(x)
            y = float(y)
            angle = float(angle)*np.pi/180.0 -np.pi/2.0
            length = float(length)
            
            p1 =  (length/2.0 - 1j*width)*np.exp(1j*angle) + x + 1j*y
            p2 =  (length/2.0 + 1j*width)*np.exp(1j*angle) + x + 1j*y
            p4 = (-length/2.0 - 1j*width)*np.exp(1j*angle) + x + 1j*y
            p3 = (-length/2.0 + 1j*width)*np.exp(1j*angle) + x + 1j*y   
            
            
            poly_psse = geojson.Polygon([[(p1.real,p1.imag),
                                    (p2.real,p2.imag),
                                    (p3.real,p3.imag),
                                    (p4.real,p4.imag),
                                    (p1.real,p1.imag)]]) 
                                    
                                    
                                  
            feat_geo = geojson.Feature(geometry=poly_psse,  properties={"id": bus_id, "name": bus_id, 
                                                                        "tag":{'power':'substation'}
                                                                        })   
            feat_geo_buses_list += [feat_geo]
            
        if row[0:4]=='CART':
            reading_buses = True      
            
        if row[0:4]=='BRAN':
            reading_buses = False   
            reading_branches = True  
            
        if (reading_branches == True):
            s = row.split()
            branch_nodes_list = s[3:]
            
            N_nodes = len(branch_nodes_list)/2 
            
            node_list = []
            for it_node in range(N_nodes):
                
                node = branch_nodes_list[(2*it_node):(2+2*it_node)]
                node_tuple = tuple(map(float,node))
                node_list += [node_tuple]    
            
            
            if len(node_list)>0:
#                print(node_list)
                geo_branch = geojson.LineString(node_list)
                feat_branch = geojson.Feature(geometry=geo_branch,  properties={"id": '{:s}_{:s}_{:s}'.format(s[0],s[1],s[2]), 
                                                                                "name":'{:s}_{:s}_{:s}'.format(s[0],s[1],s[2]),
                                                                                "tag":{'power':'line'}
                                                                                })  
                
                feat_geo_branches_list += [feat_branch]    
                       
        if (reading_branches == True) and (ord(row[0]) == 13):
            
            reading_branches = False            
            
#    geo_buses = geojson.GeometryCollection(geo_buses_list)
    feat_geo_buses    = geojson.FeatureCollection(feat_geo_buses_list) 
    feat_geo_branches = geojson.FeatureCollection(feat_geo_branches_list) 

    feat_geo_total = geojson.FeatureCollection(feat_geo_buses_list + feat_geo_branches_list) 
    
    x_psse_1,y_psse_1 = feat_geo_total['features'][bus_1-1]['geometry']['coordinates'][0][0]
    x_psse_2,y_psse_2 = feat_geo_total['features'][bus_2-1]['geometry']['coordinates'][0][0]
    
    dist_psse = np.sqrt((x_psse_1-x_psse_2)**2+(y_psse_1-y_psse_2)**2)
    
    psse_dist_to_m = bus_1_2_dist/dist_psse
    
    m_to_latlon = 1.0/110.0e3
    
    scale = psse_dist_to_m*m_to_latlon  
    
    lon, lat = bus_1_lon_lat    
    
    translation = (lon+x_psse_1*scale,lat+y_psse_1*scale)
    for item in feat_geo_total['features']:
        item['geometry'] = coord_transform(item['geometry'],scale,translation) 
        
    geojson.dump(feat_geo_total, open(geojson_path, 'w'))
     

    return feat_geo_buses, feat_geo_branches, feat_geo_total
        
def test_tools_dict2h5():
    a=2
    b=3
    c=np.array([1,2,3,4])
    t=np.array([.1,.2,.3,.4])
    data_dict = {'test_1':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}},
                     'test_2':{'sys':{'t':t},'bus_1':{'a':2,'b':3, 'c':c},'bus_2':{'a':2,'b':3, 'c':2*c}}}
    
    file_name = 'foo.hdf5'
    dict_to_h5(file_name, data_dict) 




def name2chan(chnf, varname, busnumber, bus_to=0):

    '''
    SPD
    FREQ
    ETRM
    PMEC
    VAR 5
    VAR 6
    '''

    if type(chnf)==type(()):
        chan_dict = chnf[1]
        #print type(chnf)

    else:       
        chan_dict = chnf.get_data()[1]

    for it in range(len(chan_dict)-1):

        var_name = chan_dict[it+1].split()[0]

        #print chan_dict
        bus_number = int(chan_dict[it+1].split()[1].split('[')[0])
        
        if varname==var_name and busnumber==bus_number:
            #print str(it+1) + ' : ' + chan_dict[it+1]
            return it+1

        pass

def coord_transform(obj,scale,translation):
    
    
    def transform(lonlat):
        lon_tran,lat_tran = translation

        lon_old,lat_old=lonlat
        lon_new = scale*lon_old+lon_tran
        lat_new = scale*lat_old+lat_tran
        return (lon_new,lat_new)    

    if obj['type'] == 'Point':
        coordinates = tuple(map(func, obj['coordinates']))
    elif obj['type'] in ['LineString', 'MultiPoint']:
        curve_cordinates_new = map(transform,obj['coordinates'])
        coordinates = curve_cordinates_new
    elif obj['type'] in ['MultiLineString', 'Polygon']:
        curve_cordinates_new = []
        for curve_cordinates in obj['coordinates']:
            coordinates = map(transform,curve_cordinates)
            curve_cordinates_new += [coordinates]
        coordinates = curve_cordinates_new
        
    elif obj['type'] == 'MultiPolygon':
        coordinates = [[[
            tuple(map(func, c)) for c in curve]
            for curve in part]
            for part in obj['coordinates']]
    else:
        raise ValueError("Invalid geometry object %s" % repr(obj))
    return {'type': obj['type'], 'coordinates': coordinates}                    

        
        
        
def map_coords(func, obj):
    """
    Returns the coordinates from a Geometry after applying the provided
    function to the tuples.

    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each coordinate array.
    :rtype: list
    :raises ValueError: if the provided object is not a Geometry.
    """

    if obj['type'] == 'Point':
        coordinates = tuple(map(func, obj['coordinates']))
    elif obj['type'] in ['LineString', 'MultiPoint']:
        coordinates = [tuple(map(func, c)) for c in obj['coordinates']]
    elif obj['type'] in ['MultiLineString', 'Polygon']:
        coordinates = map(fun,obj['coordinates'])
        
    elif obj['type'] == 'MultiPolygon':
        coordinates = [[[
            tuple(map(func, c)) for c in curve]
            for curve in part]
            for part in obj['coordinates']]
    else:
        raise ValueError("Invalid geometry object %s" % repr(obj))
    return {'type': obj['type'], 'coordinates': coordinates}


def test_loc2geojson():

    # http://www.geojsonlint.com/
    
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/bus_2_branch_1.loc'
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.loc'
    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.json'

    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_50/results/ieee12g_50_pvs.loc'
    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_50/results/ieee12g_50_pvs.json'    
    
    bus_1,bus_2 = 9,4
    
    bus_1_lon_lat = (-71.5,18.6)  #  rep dominicana
    bus_1_2_dist = 300.0e3

    bus_1_lon_lat = (-101,44)  #  south dakota
    bus_1_2_dist = 500.0e3

    
#    bus_1_lon_lat = (-66.8,18.12) #  puerto rico
#    bus_1_2_dist = 80.0e3
    
#    bus_1_lon_lat = (-30.0,121.0) #   australia
#    bus_1_2_dist = 200.0e3
#    bus_1_lon_lat = -5,-41  #  zamora    

    
    feat_geo_buses, feat_geo_branches, geo_total = loc2geojson(loc_path, geojson_path,bus_1,bus_2,bus_1_2_dist, bus_1_lon_lat)

def gspreadsheet2geojason(spreadsheet_name, mail,password,geojson_path):
    
    import gspread
    import geojson
    import osmapi
    
    osm = osmapi.OsmApi()
    gc = gspread.login(mail,password)
    wkb = gc.open(spreadsheet_name)
    wks_generators = wkb.worksheet('Generators') 
    

# se leen las subestaciones    
    feat_geo_substations_list = []
    
    wks_substations = wkb.worksheet('Substations')
    
    substations_ds_id = wks_substations.range('A2:A61')
    substations_osm_id = wks_substations.range('B2:B61')
    
    
    for ds_id, osm_id in zip(substations_ds_id,substations_osm_id):
        
        osm_id_way =  osm_id.value
        if osm_id_way:
                      
            osm_data = osm.WayGet(osm_id_way)
            print('osm id: {:d}'.format(osm_data['id'])) 
            
            lats, lons = [],[]
            osm_nodes = osm_data['nd']
            for osm_node in osm_nodes:
#                print(osm.NodeGet(osm_node))
                lats += [osm.NodeGet(osm_node)['lat']]
                lons += [osm.NodeGet(osm_node)['lon']]
                
            poly = geojson.Polygon([zip(lons,lats)]) 
                                  
            feat_geo = geojson.Feature(geometry=poly,  properties={"id": unicode(ds_id.value), 
                                                                   "name": unicode(ds_id.value), 
                                                                   "tag":{u'power':u'substation'}})   
            feat_geo_substations_list += [feat_geo]            


# se leen los terminals  

    wks_substations = wkb.worksheet('Terminals')            
    substations_ds_id = wks_substations.range('A2:A317')
    substations_osm_id = wks_substations.range('B2:B317')
    
    
    for ds_id, osm_id in zip(substations_ds_id,substations_osm_id):
        
        osm_id_way =  osm_id.value
        if osm_id_way:
                      
            osm_data = osm.WayGet(osm_id_way)
            print('osm id: {:d}'.format(osm_data['id'])) 
            
            lats, lons = [],[]
            osm_nodes = osm_data['nd']
            for osm_node in osm_nodes:
#                print(osm.NodeGet(osm_node))
                lats += [osm.NodeGet(osm_node)['lat']]
                lons += [osm.NodeGet(osm_node)['lon']]
                
            poly = geojson.Polygon([zip(lons,lats)]) 
                                  
            feat_geo = geojson.Feature(geometry=poly,  properties={"id": unicode(ds_id.value), 
                                                                   "name": unicode(ds_id.value), 
                                                                   "tag":{u'power': u'substation'}})   
            tags_list = [u'name',u'operator', u'voltage'] 
            for tag in tags_list:
                if osm_data[u'tag'].has_key(tag):  
                    feat_geo[u'properties'][u'tag'].update({tag:osm_data[u'tag'][tag]})  
                else:
                    feat_geo[u'properties'][u'tag'].update({tag:u''}) 
            feat_geo_substations_list += [feat_geo]  
            

# se leen las lineas  

    feat_geo_lines_list = []
    wks_lines = wkb.worksheet('Lines')            
    lines_ds_id = wks_lines.range('A2:A204')
    lines_osm_id_1 = wks_lines.range('F2:F204')
    lines_osm_id_2 = wks_lines.range('G2:G204')
    lines_osm_id_3 = wks_lines.range('H2:H204')
    lines_osm_id_4 = wks_lines.range('I2:I204')
    lines_osm_id_5 = wks_lines.range('J2:J204')
    lines_osm_id_6 = wks_lines.range('K2:K204')    
    
    ways_lines = zip(lines_osm_id_1,lines_osm_id_2,lines_osm_id_3,lines_osm_id_4,lines_osm_id_5,lines_osm_id_6)

    
    for ds_id, osm_ids in zip(lines_ds_id,ways_lines):  # una linea pueden ser varios way
        print('line ds id: {:s}'.format(ds_id.value))        
        lats, lons = [],[]         
        line_id_exists = False    
        it_way = 0
        for osm_id in  osm_ids:           # una linea pueden ser varios way
        
            osm_id_way =  osm_id.value
            lats_way = [] # lats of current way
            lons_way = [] # lons of current way         
            if osm_id_way:
                line_id_exists = True
                osm_data = osm.WayGet(osm_id_way)
                print('    line osm way id: {:d}'.format(osm_data['id'])) 

                
                osm_nodes = osm_data['nd']
                for osm_node in osm_nodes:
                    lats_way += [osm.NodeGet(osm_node)['lat']] # lats of current way
                    lons_way += [osm.NodeGet(osm_node)['lon']] # lons of current way
            if it_way > 0 and len(lats_way)>0 and len(lats)>0:        
                last_way_end_lat = lats[-1]
                last_way_end_lon = lons[-1]
                next_way_start_lat = lats_way[0]
                next_way_start_lon = lons_way[0]
                next_way_end_lat = lats_way[-1]
                next_way_end_lon = lons_way[-1]
                
                dist_end_start = ((last_way_end_lat - next_way_start_lat)**2 + (last_way_end_lon - next_way_start_lon)**2)**0.5
                dist_end_end   = ((last_way_end_lat - next_way_end_lat)**2 + (last_way_end_lon - next_way_end_lon)**2)**0.5
                
                if dist_end_start <= dist_end_end:
                    lats += lats_way # lats of current line
                    lons += lons_way # lons of current line  
    
                if dist_end_start > dist_end_end:
                    lons_way.reverse() 
                    lats_way.reverse()
                    lats += lats_way # lats of current line
                    lons += lons_way # lons of current line  
            else:
                    lats += lats_way # lats of current line
                    lons += lons_way # lons of current line                 
            it_way += 1
        if line_id_exists:        
            line = geojson.LineString(zip(lons,lats)) 
            
                
            feat_geo = geojson.Feature(geometry=line,  
                                       properties={"id": unicode(ds_id.value), 
                                                   "name": unicode(ds_id.value), 
                                                   "tag":{u'power': u'line'}})   
            tags_list = [u'frequency',u'cables', u'voltage',u'wires',u'operator'] 
            for tag in tags_list:
                if osm_data[u'tag'].has_key(tag):  
                    feat_geo[u'properties'][u'tag'].update({tag:osm_data[u'tag'][tag]})
                else:
                    feat_geo[u'properties'][u'tag'].update({tag:u''})

            feat_geo_lines_list += [feat_geo]      
    



            
 

            
            
            
    feat_geo_total = geojson.FeatureCollection(feat_geo_substations_list + feat_geo_lines_list)
    
    geojson.dump(feat_geo_total, open(geojson_path, 'w'))
    
    return feat_geo_total


def loc2network(loc_path):
    '''Converts PSS/E .loc file to network file



    '''    
    
    
    loc_file = open(loc_path, 'r')

    
    reading_buses = False
    reading_branches = False

    nodes = []
    edges = []
    
    for row in loc_file.readlines():

        if (reading_buses == True) and (ord(row[0]) == 13):

            reading_buses = False
        
        if reading_buses == True:
            
            x = 11.80
            y =  4.30
            angle =  90.0/180.0*np.pi  
            length = 0.80
            width = 0.02
            
            bus_id, x, y, angle, length = row.split()
            
            x = float(x)
            y = float(y)
            angle = float(angle)*np.pi/180.0 -np.pi/2.0
            length = float(length)
            
            p1 =  (length/2.0 - 1j*width)*np.exp(1j*angle) + x + 1j*y
            p2 =  (length/2.0 + 1j*width)*np.exp(1j*angle) + x + 1j*y
            p4 = (-length/2.0 - 1j*width)*np.exp(1j*angle) + x + 1j*y
            p3 = (-length/2.0 + 1j*width)*np.exp(1j*angle) + x + 1j*y   
            
            node = bus_id
            
            nodes += [node]
            
        if row[0:4]=='CART':
            reading_buses = True      
            
        if row[0:4]=='BRAN':
            reading_buses = False   
            reading_branches = True  
            
        if (reading_branches == True):
            s = row.split()
            branch_nodes_list = s[3:]
            print s
            N_nodes = len(branch_nodes_list)/2 
            edges += [tuple(s[0:2])]
            node_list = []
            for it_node in range(N_nodes):
                
                node = branch_nodes_list[(2*it_node):(2+2*it_node)]
                node_tuple = tuple(map(float,node))
                node_list += [node_tuple]    
            
            
#            if len(node_list)>0:
#                print(node_list)
 
                       
        if (reading_branches == True) and (ord(row[0]) == 13):
            
            reading_branches = False            

        
    return nodes,edges

    
def simplify_ways(geojson_path, simplified_geojson_path):


    


#
    from rdp import rdp

    import json
    import geojson

    geo = json.load(open(geojson_path, 'r'))


#    for item in geo['features']:
#        # substations
#        if item[u'properties'].has_key(u'tag'):
#            if item[u'properties'][u'tag'] == u'substation':
#
#                    coords_list = item[u'geometry'][u'coordinates'][0]
#
#                    lons = []
#                    lats = []
#                    for coord in  coords_list: 
#                        
#                        lons += [coord[0]]
#                        lats += [coord[1]]
#                    
#                    x, y = m( lons, lats )
#                    xy = zip(x,y)
#                    poly = Polygon( xy, edgecolor='blue', facecolor='red', alpha=1.0, lw=5 )
#                    plt.gca().add_patch(poly) 
    
    coords_number = 0
    simplified_coords_number = 0
    for item in geo['features']:
        # lines
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'line':
                coords_list = item[u'geometry'][u'coordinates']
                coords_number += len(coords_list)
                simplified_coords = rdp(coords_list, epsilon=0.001)
                item[u'geometry'][u'coordinates'] = simplified_coords
                simplified_coords_number += len(simplified_coords)
    print('original coords number: {:d}'.format(coords_number))
    print('simplified coords number: {:d}'.format(simplified_coords_number))
    geojson.dump(geo, open(simplified_geojson_path, 'w'))
                

def geo2substations(geojson_file):
    import json
    geo = json.load(open(geojson_file, 'r'))
    substations_list = []
    for item in geo['features']:
        # substations
        if item[u'properties'].has_key(u'tag'):
            if item[u'properties'][u'tag'] == u'substation':
                substations_list += [item[u'properties'][u'name']]
                coords_list = item[u'geometry'][u'coordinates'][0]
                lons = []
                lats = []
                for coord in  coords_list: 
                    
                    lons += [coord[0]]
                    lats += [coord[1]]

    return substations_list

def raw2pandas(raw_file):
    raw_obj = open(raw_file,'r')
    
    raw = raw_obj.readlines()
    
    it = 0
    it_trafo = 0
    row_trafo = ''
    rows_trafo = ''
    reading_trafo = 'False'
    for item in raw:
    #    print(item)
        if item == '0 / END OF BUS DATA, BEGIN LOAD DATA\r\n':
            end_bus = it
        if item == '0 / END OF LOAD DATA, BEGIN FIXED SHUNT DATA\r\n':
            end_load = it
        if item == '0 / END OF FIXED SHUNT DATA, BEGIN GENERATOR DATA\r\n':
            end_shunt = it
        if item == '0 / END OF GENERATOR DATA, BEGIN BRANCH DATA\r\n':
            end_generator = it
        if item == '0 / END OF BRANCH DATA, BEGIN TRANSFORMER DATA\r\n':
            reading_trafo = True           
            end_branch = it
            
        
        if it_trafo == 4:
            it_trafo = 0
            rows_trafo += row_trafo + '\r\n'
            row_trafo = ''
            
        if reading_trafo == True:    
            if it_trafo>0:
                row_trafo += item.replace('\r\n', ', ')
            
            it_trafo += 1
                
        if item == '0 / END OF TRANSFORMER DATA, BEGIN AREA DATA\r\n':
            reading_trafo = 'False'
            end_transformer = it
        it += 1
            
    file_trafos = open('trafos.csv','w')
    file_trafos.write(rows_trafo)
    file_trafos.close()
    
    bus_header = 'I, NAME, BASKV, IDE, AREA, ZONE, OWNER, VM, VA, NVHI, NVLO, EVHI, EVLO'.replace(' ','').split(',')
    load_header = 'I, ID, STATUS, AREA, ZONE, PL, QL, IP, IQ, YP, YQ, OWNER, SCALE, INTRPT'.replace(' ','').split(',')
    fixed_shunt_header = 'I, ID, STATUS, GL, BL'.replace(' ','').split(',')
    generator_header = 'I,ID,PG,QG,QT,QB,VS,IREG,MBASE,ZR,ZX,RT,XT,GTAP,STAT,RMPCT,PT,PB,O1,F1,WMOD,WPF'.replace(' ','').split(',')
    branches_header ='I,J,CKT,R,X,B,RATEA,RATEB,RATEC,GI,BI,GJ,BJ,ST,MET,LEN,O1,F1,...,O4,F4'.replace(' ','').split(',')
    two_w_trafo_header ='I,J,K,CKT,CW,CZ,CM,MAG1,MAG2,NMETR,NAME,STAT,O1,F1,O2,F2,O3,F3,O4,F4,VECGRP,R1-2,X1-2,SBASE1-2WINDV1,NOMV1,ANG1,RATA1,RATB1,RATC1,COD1,CONT1,RMA1,RMI1,VMA1,VMI1,NTP1,TAB1,CR1,CX1,CNXA1,WINDV2,NOMV2 '.replace(' ','').split(',')
    
    
    skiprows = 3
    nrows = end_bus-skiprows
    bus_data = pd.read_csv(raw_file, skiprows=skiprows, header=None, nrows=nrows, names=bus_header)
    
    skiprows = end_bus+1
    nrows = end_load-end_bus-1
    load_data = pd.read_csv(raw_file, skiprows=skiprows, header=None, nrows=nrows, names=load_header)
    
    skiprows = end_load+1
    nrows = end_shunt-end_load-1
    fixed_shunt_data = pd.read_csv(raw_file, skiprows=skiprows, header=None, nrows=nrows, names=fixed_shunt_header)

    skiprows = end_shunt+1
    nrows = end_generator-end_shunt-1
    generator_data = pd.read_csv(raw_file, skiprows=skiprows, header=None, nrows=nrows, names=generator_header)

    skiprows = end_generator+1
    nrows = end_branch-end_generator-1
    branch_data = pd.read_csv(raw_file, skiprows=skiprows, header=None, nrows=nrows, names=branches_header)

    transformer_data = pd.read_csv(StringIO(rows_trafo), header=None, names=two_w_trafo_header)
         
    raw_df_dict = {'bus':bus_data,
                   'load':load_data,
                   'fixed_shunt':fixed_shunt_data,
                   'generator':generator_data,
                   'branch':branch_data,
                   'transformer':transformer_data
                   }
    
    return raw_df_dict
    

if __name__=="__main__":
    
#    test_loc2geojson()
    raw_file='/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/system/ieee12g_pvsync_10.raw'
    raw_df_dict =  raw2pandas(raw_file)
    
#    test_loc2geojson()

#    

##    
#    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/tests/pvsync/jmm/gis/location.loc'
#    buses,edges = loc2network(loc_path)
#    
#    import networkx as nx
#    import matplotlib.pyplot as plt
#    
#    G=nx.Graph()
#    G=nx.path_graph(118)
##    G.add_nodes_from(buses)
##    G.add_edges_from(edges[1:])
#    pos_ini = {1:(-1.0,-1.0)}
#    plt.figure(figsize=(15,15))
#    pos = nx.spring_layout(G, pos=pos_ini, fixed=[1], dim=2, k=0.001, iterations=500)
#    nx.draw_networkx(G,pos=pos)
#    #nx.draw_networkx_nodes(G)
#    
#    #plt.xlim(-0.05,1.05)
#    #plt.ylim(-0.05,1.05)
#    plt.axis('off')
#    plt.savefig('random_geometric_graph.png')
#    plt.show()
#
#
#    
#    
#
#                
#                
#      