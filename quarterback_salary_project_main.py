# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:29:27 2020

@author: nlpru
"""

from quarterback_class_v1 import Quarterback
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pickle

"""Script to read in starting quarterbacks from CSV. Create list of Quarterback objects. Proceed to create data set of each QBs contract year"""

# 2019 stats and 2019 salary for QBs who started at least half of their teams games
nfl_stats_salary = pd.read_csv(r'C:\Users\nlpru\Desktop\NFL Salary Project\NFL Project CSV\nfl_stats_salary.csv')

qbs = list(nfl_stats_salary['Player'].values)

qbs_object_list = []
qbs_pickle_object_list = []

"""
Don't accidentally load this code!!!
"""
for name in qbs:
    try:
        qb_object = Quarterback(name)
        qbs_object_list.append(qb_object)
    except:
        print("{} did not work!".format(name))


with open('qb_objects.pkl', 'wb') as output:
    for qb in qbs_object_list:
        pickle.dump(qb, output, pickle.HIGHEST_PROTOCOL)


with open('qb_objects.pkl', 'rb') as input:
    while True:
        try:
            qbs_pickle_object_list.append(pickle.load(input))
        except:
            break