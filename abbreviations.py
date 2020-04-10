# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 23:35:02 2020

@author: nlpru
"""
import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
abbreviations_url = 'https://www.predictem.com/nfl/nfl-football-acronyms-abbreviations/'
abbreviations_request = requests.get(abbreviations_url).text
abbreviations_soup = bs(abbreviations_request, 'lxml')
team_abbreviation = []
team_full_name = []

for a in abbreviations_soup.findAll('p')[3].findAll('strong'):
    team_abbreviation.append(a.text)
    team_full_name.append(a.next_sibling.strip(':').strip(' '))

team_abbreviation_series = pd.Series(team_full_name, index = team_abbreviation)
#Rename to match Pro Football Reference conventions
team_abbreviation_series = team_abbreviation_series.rename(index = {'TB':'TAM'})