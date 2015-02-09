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

def loc2geojson(loc_path, geojson_path):
    '''Converts PSS/E .loc file to geoJSON file

    '''    
    
    import geojson
    
    loc_file = open(loc_path, 'r')
    
    reading_buses = False
    reading_branches = False
    feat_geo_buses_list = []  
    feat_geo_branches_list = [] 
    
    for row in loc_file.readlines():
#        print(ord(row[0]))

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
            
            
            geo = geojson.Polygon([[(p1.real,p1.imag),
                                  (p2.real,p2.imag),
                                  (p3.real,p3.imag),
                                  (p4.real,p4.imag),
                                  (p1.real,p1.imag)]]) 
                                  
            feat_geo = geojson.Feature(geometry=geo,  properties={"id": bus_id, "name": bus_id, "tag":'substation'})   
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
                print(node_list)
                geo_branch = geojson.LineString(node_list)
                feat_branch = geojson.Feature(geometry=geo_branch,  properties={"id": bus_id, "name":'{:s}_{:s}_{:s}'.format(s[0],s[1],s[2])})  
                
                feat_geo_branches_list += [feat_branch]    
                
             
        
        
        if (reading_branches == True) and (ord(row[0]) == 13):
            
            reading_branches = False            
            
#    geo_buses = geojson.GeometryCollection(geo_buses_list)
    feat_geo_buses    = geojson.FeatureCollection(feat_geo_buses_list) 
    feat_geo_branches = geojson.FeatureCollection(feat_geo_branches_list) 

    feat_geo_total = geojson.FeatureCollection(feat_geo_buses_list + feat_geo_branches_list) 
    
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

if __name__=="__main__":
    
    pass

    #test_tools_dict2h5()
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/bus_2_branch_1.loc'
    loc_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.loc'
    geojson_path = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/jmm/gis/location.json'
    feat_geo_buses, feat_geo_branches, geo_total = loc2geojson(loc_path, geojson_path)
