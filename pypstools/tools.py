""" Tools for dealing with power system data and results.

(c) 2015 Juan Manuel Mauricio
"""

import numpy as np
import scipy.linalg
import scipy.integrate
import h5py

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


    buses_dist : list with two tuples 
                 [(bus_1_number,x_1,y_1),(bus_2_number,x_2,y_2)]
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
                                    
                                    
                                  
            feat_geo = geojson.Feature(geometry=poly_psse,  properties={"id": bus_id, "name": bus_id, "tag":'substation'})   
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
                feat_branch = geojson.Feature(geometry=geo_branch,  properties={"tag":'line', "id": bus_id, "name":'{:s}_{:s}_{:s}'.format(s[0],s[1],s[2])})  
                
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
    #    #test_tools_dict2h5()
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/bus_2_branch_1.loc'
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.loc'
    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.json'
    bus_1,bus_2 = 26,111
    
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
                                  
            feat_geo = geojson.Feature(geometry=poly,  properties={"id": unicode(ds_id.value), "name": unicode(ds_id.value), "tag":'substation'})   
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
                                  
            feat_geo = geojson.Feature(geometry=poly,  properties={"id": unicode(ds_id.value), "name": unicode(ds_id.value), "tag":'substation'})   
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
        for osm_id in  osm_ids:           # una linea pueden ser varios way
            osm_id_way =  osm_id.value
         
            if osm_id_way:
                line_id_exists = True
                osm_data = osm.WayGet(osm_id_way)
                print('    line osm way id: {:d}'.format(osm_data['id'])) 
                
                
                osm_nodes = osm_data['nd']
                for osm_node in osm_nodes:
    #                print(osm.NodeGet(osm_node))
                    lats += [osm.NodeGet(osm_node)['lat']]
                    lons += [osm.NodeGet(osm_node)['lon']]
                
        if line_id_exists:        
            line = geojson.LineString(zip(lons,lats)) 
                              
            feat_geo = geojson.Feature(geometry=line,  properties={"id": unicode(ds_id.value), "name": unicode(ds_id.value), "tag":'line'})   
            feat_geo_lines_list += [feat_geo]      
    



            
 

            
            
            
    feat_geo_total = geojson.FeatureCollection(feat_geo_substations_list + feat_geo_lines_list)
    
    geojson.dump(feat_geo_total, open(geojson_path, 'w'))
    
    return feat_geo_total


def loc2network(loc_path):
    '''Converts PSS/E .loc file to etwork file



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
                

    
if __name__=="__main__":
    mail = 'jmmauricio6@gmail.com'
    file_password = open('/home/jmmauricio/password.yaml')
    password = file_password.read().rstrip()
    file_password.close()
    
#    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/osm/osm.json'
#    simplified_geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/cdec_sing_10_14/osm/osm_simplified.json'
#    spreadsheet_name = 'red_sing_id'
#    
#    feat_geo_total = gspreadsheet2geojason(spreadsheet_name,mail,password,geojson_path)
#    
#    simplify_ways(geojson_path, simplified_geojson_path)
#    
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_118/tests/pvsync/jmm/gis/location.loc'
    buses,edges = loc2network(loc_path)
    
    import networkx as nx
    import matplotlib.pyplot as plt
    
    G=nx.Graph()
    G=nx.path_graph(118)
#    G.add_nodes_from(buses)
#    G.add_edges_from(edges[1:])
    pos_ini = {1:(-1.0,-1.0)}
    plt.figure(figsize=(15,15))
    pos = nx.spring_layout(G, pos=pos_ini, fixed=[1], dim=2, k=0.001, iterations=500)
    nx.draw_networkx(G,pos=pos)
    #nx.draw_networkx_nodes(G)
    
    #plt.xlim(-0.05,1.05)
    #plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.savefig('random_geometric_graph.png')
    plt.show()


    
    

                
                
      