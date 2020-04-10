# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 20:34:49 2020

@author: nlpru
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

flacco_url = 'https://www.spotrac.com/nfl/denver-broncos/joe-flacco-4000/'
flacco_request = requests.get(flacco_url).text
flacco_soup = bs(flacco_request, 'lxml')


def scrape_spotrac_data(name, team_name):
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

scrape_spotrac_data('Joe Flacco','Denver Broncos')