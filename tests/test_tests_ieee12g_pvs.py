""" IEEE12g Simulations

(c) 2015 Juan Manuel Mauricio
"""

import sys,os

sys.path.append(os.path.join('..','pypstools'))

import psse_simulation

def test_12():
    
    tests_results_list = []

    # IEEE12g 10% PVSYNC
#    tests_10_gen_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_10_gen_trip.yaml'
#    tests_10_gen_trip.set_up(yaml_file)
#    tests_results = tests_10_gen_trip.run_tests()
#    tests_results_list += [tests_results]
#    
#    tests_10_load_change = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_10_load_change.yaml'
#    tests_10_load_change.set_up(yaml_file)
#    tests_results = tests_10_load_change.run_tests()
#    tests_results_list += [tests_results]

#    tests_10_load_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_10_load_trip.yaml'
#    tests_10_load_trip.set_up(yaml_file)
#    tests_results = tests_10_load_trip.run_tests()
#    tests_results_list += [tests_results]    

#    tests_10_bus_fault = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_10_bus_fault.yaml'
#    tests_10_bus_fault.set_up(yaml_file)
#    tests_results = tests_10_bus_fault.run_tests()
#    tests_results_list += [tests_results]

#    tests_10_line_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_10_line_trip.yaml'
#    tests_10_line_trip.set_up(yaml_file)
#    tests_results = tests_10_line_trip.run_tests()
#    tests_results_list += [tests_results]


#    # IEEE12g 30% PVSYNC
#    test_30_gen_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_30_gen_trip.yaml'
#    test_30_gen_trip.set_up(yaml_file)
#    tests_results = test_30_gen_trip.run_tests()
#    tests_results_list += [tests_results]
#    
#    test_30_load_change = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_30_load_change.yaml'
#    test_30_load_change.set_up(yaml_file)
#    tests_results = test_30_load_change.run_tests()
#    tests_results_list += [tests_results]
#    
#    test_30_bus_fault = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_30_bus_fault.yaml'
#    test_30_bus_fault.set_up(yaml_file)
#    tests_results = test_30_bus_fault.run_tests()
#    tests_results_list += [tests_results]
#
#    test_30_line_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_30_line_trip.yaml'
#    test_30_line_trip.set_up(yaml_file)
#    tests_results = test_30_line_trip.run_tests()
#    tests_results_list += [tests_results]
    tests_30_load_trip = psse_simulation.tests()
    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_30_load_trip.yaml'
    tests_30_load_trip.set_up(yaml_file)
    tests_results = tests_30_load_trip.run_tests()
    tests_results_list += [tests_results]    
    
    
#    # IEEE12g 50% PVSYNC
#    test_50_gen_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_50_gen_trip.yaml'
#    test_50_gen_trip.set_up(yaml_file)
#    tests_results = test_50_gen_trip.run_tests()
#    tests_results_list += [tests_results]
#    
#    test_50_load_change = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_50_load_change.yaml'
#    test_50_load_change.set_up(yaml_file)
#    tests_results = test_50_load_change.run_tests()
#    tests_results_list += [tests_results]
#    
#    test_50_bus_fault = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_50_bus_fault.yaml'
#    test_50_bus_fault.set_up(yaml_file)
#    tests_results = test_50_bus_fault.run_tests()
#    tests_results_list += [tests_results]
#
#    test_50_line_trip = psse_simulation.tests()
#    yaml_file = r'E:\Documents\public\jmmauricio6\RESEARCH\benches\ieee_12_generic\tests\ieee12g_pvsync\tests_ieee12g_pvsync_50_line_trip.yaml'
#    test_50_line_trip.set_up(yaml_file)
#    tests_results = test_50_line_trip.run_tests()
#    tests_results_list += [tests_results]
#    psspy = tests_10_load_trip.psspy
    return tests_results_list

if __name__ == '__main__':
    
    tests_results_list,psspy = test_12()