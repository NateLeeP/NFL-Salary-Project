# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:27:08 2020

@author: Nate P
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import re
from abbreviations import team_abbreviation_series as TAS

class Quarterback():
    """URL template for Pro Football Reference """

    
    def __init__(self, name):
        self.name = name
        #scrape team name and stats at same time, so as not to make multiple requests
        self.qb_stats_team_name = self.qb_stats(self.scrape_qb_data_pro_football(self.name))
        #Scrape function returns a tuple
        self.team_name = self.qb_stats_team_name[1]
        self.qb_stats = self.qb_stats_team_name[0]
        #Spotrac needs team name and player name to find data. 
        self.contract_df = self.scrape_spotrac_data(self.name,self.team_name)
        
    def __str__(self):
        return '{} Quarterback Class'.format(self.name)
    def __repr__(self):
        return '{} Quarterback Class'.format(self.name)

    
    def scrape_qb_data_pro_football(self, name):
        """ Returns a Beautiful Soup soup object"""
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
    
    def qb_stats(self, soup):
        # Using scraped QB data, create reable dataframe. Returns Pandas DataFrame object, team_name as a string.
        headers = [th.text for th in soup.findAll('tr')[0].findAll('th')]
        index = [th.text for th in soup.find('table').findAll('th')[32:len(soup.find('table').findAll('th'))]]
        stats = [[td.text for td in tr.findAll('td')] for tr in soup.find('table').findAll('tr')[1:len(soup.find('table').findAll('tr'))]]
        
        qb_df = pd.DataFrame(stats, index = pd.Index(index, name = 'Year'),  columns = headers[1:len(headers)])
        if soup.find('span',{'itemprop':'affiliation'}):
            team_name = soup.find('span',{'itemprop':'affiliation'}).text
        else:
            team_name = qb_df.loc['2019','Tm']
            team_name = TAS[team_name]

            
        return qb_df, team_name
    def scrape_spotrac_data(self, name, team_name):
        spotrac_url = 'https://www.spotrac.com/nfl/{}/{}'.format(team_name.lower().replace(' ','-'), name.lower().replace(' ','-'))
        spotrac_request = requests.get(spotrac_url).text
        spotrac_soup = bs(spotrac_request, features = 'lxml')
        
        def spotrac_average_salary(spotrac_soup):
            """Returns average salary for most recent contract """
            average_salary = ''
            if spotrac_soup.find('table').find('span',{'class':'playerLabel'}):
                for td in spotrac_soup.find('table').findAll('td'):
                    if td.find('span',{'class':'playerLabel'}).text == 'Average Salary':
                        average_salary = td.find('span',{'class':'playerValue'}).text
            else:
                average_salary = spotrac_soup.find('tr').find('td',{'class':'salaryAmt result'})
            return int(average_salary.strip('$').replace(',',''))       
    
        def spotrac_contract_year(spotrac_soup):
            """Returns contract year, or year BEFORE signing new contract"""
            contract_year = 0
            contract_year = int(spotrac_soup.findAll('td', {'class':'salaryYear center'})[0].text)
            return contract_year - 1
        
        sal = spotrac_average_salary(spotrac_soup)
        contract_year = spotrac_contract_year(spotrac_soup)
        
        return pd.DataFrame(data = {'Salary':sal, 'Contract Year':contract_year}, index = pd.Index(data = [self.name], name = 'Player'))
    

            
            
    
     
