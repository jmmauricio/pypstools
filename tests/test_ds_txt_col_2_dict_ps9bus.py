# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:41:49 2015

@author: jmmauricio
"""

# add pypstools to the path
import sys,os
import numpy as np
from pypstools.tools import raw2pandas
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),'..','pypstools')))

import publisher
import rst_tools
import digsilent_simulation


result_dict = digsilent_simulation.ds_txt_col_2_dict('./Scenario_2_Line 1.txt')