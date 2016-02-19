

# pitchfx_data_collection.py

'''

David Christiansen
2.19.16

This script opens the files in the specified "year" directory (on lines 26 adn 27), reads the per-game data and saves the data specific to each pitcher.  For any given year of the full pitchf/x dataset, this process roughly takes a couple of hours.

Please contact me with any comments or questions!
dc108349@gmail.com

'''





import re, requests
from bs4 import BeautifulSoup
from os import listdir
import pandas as pd
import numpy as np
from datetime import datetime


#---------------------------------------------------------------------------------------------------------------------------------
# Get the list of URLs for the range of specified dates
base_url = 'http://gd2.mlb.com/components/game/mlb/'
year = '2010'

#GameDay - 404 Not Found
# base + year
# http://gd2.mlb.com/components/game/mlb/year_2014/ 

# base + year + month
# http://gd2.mlb.com/components/game/mlb/year_2014/month_06/
# http://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_11/
# http://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_11/gid_2014_06_11_slnmlb_tbamlb_1/
# http://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_11/gid_2014_06_11_slnmlb_tbamlb_1/inning/
#http://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_11/gid_2014_06_11_slnmlb_tbamlb_1/inning/inning_all.xml

r = requests.get(base_url + 'year_' + year)
r.text
soup1 = BeautifulSoup(r.text, 'html')



#---------------------------------------------------------------------------------------------------------------------------------
#Get the data and store in files

months = [ re.sub(' ', '', t.text) for t in soup1.select('a') if t.text.startswith(' month') ]


for month in months:
    print month
    r = requests.get(base_url + 'year_' + year + '/' + month)
    #print r.text
    soup2 = BeautifulSoup(r.text, 'html')
    days = [ re.sub(' ', '', d.text) for d in soup2.select('a') if d.text.startswith(' day')]
    for day in days:
        s = requests.get(base_url + 'year_' + year + '/' + month  + day)
        soup3 = BeautifulSoup(s.text, 'html')
        games = [ re.sub(' ', '', g.text) for g in soup3.select('a') if g.text.startswith(' gid')]
        if games != []:
            for game in games:
                t = requests.get(base_url + 'year_' + year + '/' + month  + day + game + 'inning/inning_all.xml')
                #soup4 = BeautifulSoup(t.text, 'xml')
                # store the game in a file
                #print t.text
                with open("web_page_data/" + str(year) + '/' + str(year) + re.sub('/', '', game) + ".txt", "wb") as file:    
                    file.write(t.text.encode('utf-8'))
                    
# added  + str(year) in with open(...)