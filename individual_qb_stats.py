# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:16:54 2020

@author: Nate P
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
player_name = "Matt Ryan"
team_name = "Atlanta Falcons"
url = "https://pro-football-reference.com/players/{}/{}00.htm"
last_name_fletter = player_name.split()[1][0]

def pro_football_url_name(player_name):
    first_name = player_name.split()[0]
    last_name = player_name.split()[1]
    first_name = first_name[:2]
    if len(last_name) < 4:
        last_name = last_name
    else:
        last_name = last_name[:4]
    
    return last_name + first_name

def player_stats(player_name):
    url = "pro-football-reference.com/players/{}/{}00.htm".format(player_name.split()[1][0], pro_football_url_name(player_name))
    player_requests = requests.get(url).text
    player_soup = bs(player_requests, features = 'lxml')
    
def player_team(player_name):
    url = url.format(player_name.split()[1][0], pro_football_url_name(player_name))

ryan_url = url.format(last_name_fletter, pro_football_url_name(player_name))
ryan_request = requests.get(ryan_url).text
ryan_soup = bs(ryan_request, features = 'lxml')
ryan_team_name = ryan_soup.findAll('strong')[4].next_sibling.next_sibling.text

ryan_columns = [th.text for th in ryan_soup.find('table').findAll('th')[:32]]
ryan_index = [th.text for th in ryan_soup.find('table').findAll('th')[32:len(ryan_soup.find('table').findAll('th'))]]
ryan_data = [[td.text for td in tr.findAll('td')] for tr in ryan_soup.find('table').findAll('tr')[1:len(ryan_soup.find('table').findAll('tr'))]]

ryan_df = pd.DataFrame(ryan_data, index = pd.Index(ryan_index, name = 'Year').map(lambda x: x.strip('+').strip('*')), columns = ryan_columns[1:])


"""Spotrac scraping. Assume we have team name"""
spotrac_url = 'https://www.spotrac.com/nfl/{}/{}'
ryan_spotrac_url = spotrac_url.format(team_name.lower().replace(' ', '-'), player_name.lower().replace(' ', '-'))
ryan_spotrac_request = requests.get(ryan_spotrac_url).text
ryan_spotrac_soup = bs(ryan_spotrac_request, features = 'lxml')

def spotrac_average_salary(spotrac_soup):
    """Returns average salary for most recent contract """
    average_salary = ''
    for td in spotrac_soup.find('table').findAll('td'):
        if td.find('span',{'class':'playerLabel'}).text == 'Average Salary':
            average_salary = td.find('span',{'class':'playerValue'}).text
            
    return int(average_salary.strip('$').replace(',',''))
def spotrac_contract_year(spotrac_soup):
    """Returns contract year, or yea BEFORE signing new contract"""
    contract_year = 0
    contract_year = int(spotrac_soup.findAll('td', {'class':'salaryYear center'})[0].text)
    return contract_year - 1

""" What to extract from soup? Team name, Stats, pull contract year, etc """







"""
def spotrac_url_name(player_name):
    
def current_contract_detail(player_name):
""" 