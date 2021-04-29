'''
Created on Apr 29, 2021

@author: Carlo Surace
'''
52546


from mfl_services import mfl_service
import pandas as pd
import numpy as np
import ConfigF as Conf
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


print(mfl.get_scoring_rules(52546,2021))