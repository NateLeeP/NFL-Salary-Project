# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:10:58 2020

@author: nlpru
"""

"""Nine Quareterback in list had issues. Not sure paritcular issue. Will go through scraping procedure with each one to catch problem"""

import pandas as pd
import requests 
from bs4 import BeautifulSoup as bs
import re

qbs_error = ["Jameis Winston", "Dak Prescott", "Derek Carr", "Kyle Allen", "Jimmy Garoppolo", "Gardner Minshew", "Josh Allen", "Daniel Jones","Joe Flacco"]

jw = "Jameis Winston"
mr = "Matt Ryan"

#Build out functions for testing on QBs
# What are steps in Quarterback class scraping process? URL for pro-football reference. Soup from profootball reference. Data from profootball reference.
# URL for Spotrac. Contract Year for Spotrac. Average Salary for current contract. 

# Does it make more sense to create dataframe with QB contract years? For easy reference? Probably. Don't need contract year stats. 
"""
def pro_football_url(name):
    url = 'https://www.pro-football-reference.com/players/{}/{}00.htm'.format(name.split()[1][0], name.split()[1][:4] + name.split()[0][:2])
    return url
"""
def scrape_qb_data_pro_football(name):
    # Pattern to account for players with 'II' after their name. Will match on fisrt name last name. 
    pattern = re.compile(r'\w+ \w+')
    url = 'https://www.pro-football-reference.com/players/{}/{}00.htm'.format(name.split()[1][0], name.split()[1][:4] + name.split()[0][:2])
    # Scrape QB data. Return Soup
    qb_request = requests.get(url).text
    qb_soup = bs(qb_request, "lxml")
    if pattern.search(qb_soup.find('h1', {'itemprop':'name'}).text.strip())[0] == name:
        qb_soup = qb_soup
    else:
        url = url.replace('00','01')
        qb_request = requests.get(url).text
        qb_soup = bs(qb_request, "lxml")
        if pattern.search(qb_soup.find('h1', {'itemprop':'name'}).text.strip())[0]  == name:
            qb_soup = qb_soup
        else:
            url = url.replace('01','02')
            qb_request = requests.get(url).text
            qb_soup = bs(qb_request,'lxml')
    
    return qb_soup
    
    """
    url = url.replace('01','02')
    qb_request = requests.get(url).text
    qb_soup = bs(qb_request, 'lxml')
    if qb_soup.find('h1', {'itemprop':'name'}).text == name:
        return qb_soup
    """
    
def qb_stats(soup):
    # Using scraped QB data, create reable dataframe. Return Team name as well.
    headers = [th.text for th in soup.findAll('tr')[0].findAll('th')]
    index = [th.text for th in soup.find('table').findAll('th')[32:len(soup.find('table').findAll('th'))]]
    stats = [[td.text for td in tr.findAll('td')] for tr in soup.find('table').findAll('tr')[1:len(soup.find('table').findAll('tr'))]]
    
    qb_df = pd.DataFrame(stats, index = pd.Index(index, name = 'Year'),  columns = headers[1:len(headers)])
    if soup.find('span',{'itemprop':'affiliation'}):
        team_name = soup.find('span',{'itemprop':'affiliation'}).text
    else:
        team_name = qb_df.loc['2019','Tm']
    return qb_df, team_name


"""Issues discovered: Team name. Team name not scraped correctly. What to do with players without a team?? Winston, Flacco, etc. 
Using url with Dak Prescott finds a 'Dave Preston'. Do not want him. What to do?"""
    
""" Issue #1: Not reading team name correctly. Issue with Kyle Allen, Jimmy Garoppolo, Gardner Minshew. """
""" ISSUE SOLVED!!! Onto next issue"""

"""Issue 2. What to do for players without teams? Use their last known team affiliation. Remember: Goal of team name is to pass
into spotrac. Spotrac looks up players using team name. Spotrac sorts free agents by their most recent team. 
Extract most recent team name (abbreviation) from stats df. Using abbreviation to team name conversion Series, return team name"""

# Scrape team_name/abbreviation
abbreviations_url = 'https://www.predictem.com/nfl/nfl-football-acronyms-abbreviations/'
abbreviations_request = requests.get(abbreviations_url).text
abbreviations_soup = bs(abbreviations_request, 'lxml')
team_abbreviation = []
team_full_name = []

for a in abbreviations_soup.findAll('p')[3].findAll('strong'):
    team_abbreviation.append(a.text)
    team_full_name.append(a.next_sibling.strip(':').strip(' '))

team_abbreviation_series = pd.Series(team_full_name, index = team_abbreviation)

""" You are close!! Stopping at 5:35. Success!! Updated qb_stats Needed to use 'if', 'else'. Not 'try', 'except'."""

"""Next Problem: How do I adjust for Dak Prescott, Josh Allen, etc. """
"""May have figured it out!!! Continue to work on 'scrape_qb_data_pro_football. See above"""
""" Final problems: Josh allen and Daniel Jones. Will sleep on this. Getting closer! Multiple players named Josh Allen so matchign on name alone not enough!!
"""









    