# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:29:27 2020

@author: nlpru
"""

from quarterback_class_v3 import Quarterback
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pickle

"""Script to read in starting quarterbacks from CSV. Create list of Quarterback objects. Proceed to create data set of each QBs contract year"""

# 2019 stats and 2019 salary for QBs who started at least half of their teams games
nfl_stats_salary = pd.read_csv(r'C:\Users\Nate P\Desktop\NFL-Salary-Project-master\nfl_stats_salary.csv')

qbs = list(nfl_stats_salary['Player'].values)
hot_fixes = {'Josh Allen':'https://www.pro-football-reference.com/players/A/AlleJo02.htm', 'Daniel Jones':'https://www.pro-football-reference.com/players/J/JoneDa05.htm'}
qbs_object_list = []
qbs_pickle_object_list = []

"""
Don't accidentally load this code!!!
"""
for name in qbs:
    if name in hot_fixes:
        qbs_object_list.append(Quarterback(name, hot_fixes[name]))
    else:
        try:
            qbs_object_list.append(Quarterback(name))
        except:
            print('{} did not work!'.format(name))

columns = [x.strip() for x in 'Age, Player, Tm, Pos, No., G, GS, QBrec, Cmp, Att, Cmp%, Yds, TD, TD%, Int, Int%, 1D, Lng, Y/A, AY/A, Y/C, Y/G, Rate, QBR, Sk, Yds, NY/A, ANY/A, Sk%, 4QC, GWD, AV'.split(',')]

d = pd.DataFrame(data = None, index = pd.Index(data = [], name = 'Year'), columns = columns)

for qb in qbs_object_list:
    try:
        contract_year_df = qb.qb_stats.loc[[str(qb.contract_df.loc[qb.name, 'Contract Year'])]]
        contract_year_df = contract_year_df.insert(loc = 0, column = 'Player', value = qb.name)
        d = pd.concat([d, contract_year_df])
    except:
        print('{} is on his rookie deal'.format(qb.name))



"""
with open('qb_objects.pkl', 'wb') as output:
    for qb in qbs_object_list:
        pickle.dump(qb, output, pickle.HIGHEST_PROTOCOL)


with open('qb_objects.pkl', 'rb') as input:
    while True:
        try:
            qbs_pickle_object_list.append(pickle.load(input))
        except:
            break
            
"""

"""Loop through QB objects, extract contract year stats """

