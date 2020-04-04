# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:27:08 2020

@author: Nate P
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs

class Quarterbacks():
    """URL template for Pro Football Reference """
    pro_fb_url ="https://pro-football-reference.com/players/{}/{}00.htm"
    spotrac_url = 'https://www.spotrac.com/nfl/{}/{}'
    def __init__(self, name):
        self.name = name
        self.pro_fb_url = self.pro_fb_url.format(self.name.split()[1][0], self.pro_football_url_name(self.name))
        self.pro_fb_request = requests.get(self.pro_fb_url).text
        self.pro_fb_soup = bs(self.pro_fb_request, features = 'lxml')
        self.team_name = self.pro_fb_soup.findAll('strong')[4].next_sibling.next_sibling.text
        
        self.spotrac_url = self.spotrac_url.format(self.team_name.lower().replace(' ','-'), self.name.lower().replace(' ','-'))
        self.spotrac_request = requests.get(self.spotrac_url).text
        self.spotrac_soup = bs(self.spotrac_request, features = 'lxml')
        #initialize stats as empty DataFrame
        self.stats = self.stats_df(self.pro_fb_soup)
        self.current_contract_avg_salary = self.spotrac_average_salary(self.spotrac_soup)
        self.contract_year = self.spotrac_contract_year(self.spotrac_soup)
        self.contract_year_stats = self.rookie_contract(self.contract_year)
        
        
    def pro_football_url_name(self, player_name):
        first_name = player_name.split()[0]
        last_name = player_name.split()[1]
        first_name = first_name[:2]
        if len(last_name) < 4:
            last_name = last_name
        else:
            last_name = last_name[:4]
        
        return last_name + first_name
    
    def stats_df(self, soup):
        

        columns = [th.text for th in soup.find('table').findAll('th')[:32]]
        index = [th.text for th in soup.find('table').findAll('th')[32:len(soup.find('table').findAll('th'))]]
        data = [[td.text for td in tr.findAll('td')] for tr in soup.find('table').findAll('tr')[1:len(soup.find('table').findAll('tr'))]]
        df = pd.DataFrame(data, index = pd.Index(index, name = 'Year').map(lambda x: x.strip('+').strip('*')), columns = columns[1:])
        
        return df

    def spotrac_average_salary(self,spotrac_soup):
        """Returns average salary for most recent contract """
        average_salary = ''
        for td in spotrac_soup.find('table').findAll('td'):
            if td.find('span',{'class':'playerLabel'}).text == 'Average Salary':
                average_salary = td.find('span',{'class':'playerValue'}).text
                
        return int(average_salary.strip('$').replace(',',''))       

    def spotrac_contract_year(self,spotrac_soup):
        """Returns contract year, or year BEFORE signing new contract"""
        contract_year = 0
        contract_year = int(spotrac_soup.findAll('td', {'class':'salaryYear center'})[0].text)
        return contract_year - 1
    
    def rookie_contract(self, contract_year):
        try: 
            return self.stats.loc[str(contract_year),:]
        except:
            return "On rookie contract"
            
            
    
     
