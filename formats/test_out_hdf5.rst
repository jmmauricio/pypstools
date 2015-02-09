hdf5 output file structure
==========================
.. code:: python

    tests_dict =
		{'test_1':
		    {'sys':{
			    'time':np.array([...])
			    'buses':['bus_1','bus_2'],
			    'syms':['sym_1'],
			    'loads':['load_1']
			   },
		     'bus':{
			    'bus_1':{'u':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phiu':{'data':np.array([...]), 'units':'deg'},
			             'fehz':np.array([...]), 'units':'Hz'}
			    'bus_2':{'u':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phiu':{'data':np.array([...]), 'units':'deg'},
			             'fehz':np.array([...]), 'units':'Hz'}   
			   },
		     'sym':{
			    'sym_1':{'p':{'data':np.array([...]), 'units':'MW'},
			             'q':{'data':np.array([...]), 'units':'Mvar'},
			             'speed':{'data':np.array([...]), 'units':'pu'},
			             've':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phi':{'data':np.array([...]), 'units':'deg'},
			             'bus_id':'bus_1'}
			   }
		     'load':{
			     'load_1':{'p':{'data':np.array([...]), 'units':'MW'},
			               'q':{'data':np.array([...]), 'units':'Mvar'},
			               'bus_id':'bus_2'}
			    }
		     },
		'test_2':
		    {'sys':{
			    'time':np.array([...])
			    'buses':['bus_1','bus_2'],
			    'syms':['sym_1'],
			    'loads':['load_1']
			   },
		     'bus':{
			    'bus_1':{'u':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phiu':{'data':np.array([...]), 'units':'deg'},
			             'fehz':np.array([...]), 'units':'Hz'}
			    'bus_2':{'u':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phiu':{'data':np.array([...]), 'units':'deg'},
			             'fehz':np.array([...]), 'units':'Hz'}   
			   },
		     'sym':{
			    'sym_1':{'p':{'data':np.array([...]), 'units':'MW'},
			             'q':{'data':np.array([...]), 'units':'Mvar'},
			             'speed':{'data':np.array([...]), 'units':'pu'},
			             've':{'data':np.array([...]), 'units':'pu', 'base':220},
			             'phi':{'data':np.array([...]), 'units':'deg'},
			             'bus_id':'bus_1'}
			   }
		     'load':{
			     'load_1':{'p':{'data':np.array([...]), 'units':'MW'},
			               'q':{'data':np.array([...]), 'units':'Mvar'},
			               'bus_id':'bus_2'}
			    }
		     },
		}  
		    
