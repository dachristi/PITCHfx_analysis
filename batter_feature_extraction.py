'''

David Christiansen
2.19.16

This script opens the files in the specified "year" directory (on lines 26 adn 27), reads the per-game data and saves the data specific to each batter.  For any given year of the full pitchf/x dataset, this process roughly takes a couple of hours.

Please contact me with any comments or questions!
dc108349@gmail.com

'''






#---------------------------------------------------------------------------------------------------------------------------
import re, requests
from bs4 import BeautifulSoup
from os import listdir
import pandas as pd
import numpy as np
from datetime import datetime


#---------------------------------------------------------------------------------------------------------------------------
# feature extraction function
# done 2014, 2015, 2013, 2012, 2011, 2010

year = 2010
opening_date = datetime.strptime('2010 04 05', '%Y %m %d')
# openning days
# 4/5/2015
# 3/30/2014
# 3/31/2013
# 4/5/2012
# 3/31/2011
# 4/05/2010




def feature_extract(pitch):
    batter = re.findall('batter="(.*?)"', str(at_bat))[0]
    pitcher = re.findall('pitcher="(.*?)"', str(at_bat))[0]
    season = year
    ax = re.findall('ax="(.*?)"', str(pitch))[0]
    ay = re.findall('ay="(.*?)"', str(pitch))[0]
    az = re.findall('az="(.*?)"', str(pitch))[0]
    break_angle = re.findall('break_angle="(.*?)"', str(pitch))[0]
    break_length = re.findall('break_length="(.*?)"', str(pitch))[0]
    break_y = re.findall('break_y="(.*?)"', str(pitch))[0]
    cc = re.findall('cc="(.*?)"', str(pitch))[0]
    des = re.findall('des="(.*?)"', str(pitch))[0]
    end_speed = re.findall('end_speed="(.*?)"', str(pitch))[0]
    #event_num = re.findall('event_num="(.*?)"', str(pitch))[0]
    ID = re.findall(' id="(.*?)"', str(pitch))[0]
    mt = re.findall('mt="(.*?)"', str(pitch))[0]
    nasty = re.findall('nasty="(.*?)"', str(pitch))[0]
    pfx_x = re.findall('pfx_x="(.*?)"', str(pitch))[0]
    pfx_z = re.findall('pfx_z="(.*?)"', str(pitch))[0]
    pitch_type = re.findall('pitch_type="(.*?)"', str(pitch))[0]
    #play_guid = re.findall('play_guid="(.*?)"', str(pitch))[0]
    px = re.findall('px="(.*?)"', str(pitch))[0]
    pz = re.findall('pz="(.*?)"', str(pitch))[0]
    spin_dir = re.findall('spin_dir="(.*?)"', str(pitch))[0]
    spin_rate = re.findall('spin_rate="(.*?)"', str(pitch))[0]
    break_y = re.findall('break_y="(.*?)"', str(pitch))[0]
    start_speed = re.findall('start_speed="(.*?)"', str(pitch))[0]
    sv_id = re.findall('sv_id="(.*?)"', str(pitch))[0]
    sz_bot = re.findall('sz_bot="(.*?)"', str(pitch))[0]
    sz_top = re.findall('sz_top="(.*?)"', str(pitch))[0]
    tfs = re.findall('tfs="(.*?)"', str(pitch))[0]

    tfs_zulu = re.findall('tfs_zulu="(.*?)"', str(pitch))[0]
    tfs_zulu = re.sub('T', ' ', tfs_zulu)
    tfs_zulu = re.sub('Z', '', tfs_zulu)

    Type = re.findall(' type="(.*?)"', str(pitch))[0]
    type_confidence = re.findall(' type_confidence="(.*?)"', str(pitch))[0]
    vx0 = re.findall(' vx0="(.*?)"', str(pitch))[0]
    vy0 = re.findall(' vy0="(.*?)"', str(pitch))[0]
    vz0 = re.findall(' vz0="(.*?)"', str(pitch))[0]
    x = re.findall(' x="(.*?)"', str(pitch))[0]
    x0 = re.findall(' x0="(.*?)"', str(pitch))[0]
    y = re.findall(' y="(.*?)"', str(pitch))[0]
    y0 = re.findall(' y0="(.*?)"', str(pitch))[0]
    z0 = re.findall(' z0="(.*?)"', str(pitch))[0]
    zone = re.findall('zone="(.*?)"', str(pitch))[0]

    profile = [batter, pitcher, season, ax, ay, az, break_angle, break_length, break_y,\
               des, end_speed, ID, mt, nasty, pfx_x, pfx_z, pitch_type,\
               px, pz, spin_dir, spin_rate, start_speed, sv_id, sz_bot, sz_top, tfs,\
               tfs_zulu, Type, type_confidence, vx0, vy0, vz0, x, x0, y, y0, z0, zone]
    return profile


#profile2 = feature_extract(str(pitch))

columns = ['batter', 'pitcher', 'season', 'ax', 'ay', 'az', 'break_angle', 'break_length', 'break_y',\
               'des', 'end_speed', 'ID', 'mt', 'nasty', 'pfx_x', 'pfx_z', 'pitch_type',\
               'px', 'pz', 'spin_dir', 'spin_rate', 'start_speed', 'sv_id', 'sz_bot', 'sz_top', 'tfs',\
               'tfs_zulu', 'Type', 'type_confidence', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0', 'z0', 'zone']


# deleted event_num, play_guid


#---------------------------------------------------------------------------------------------------------------------------



files = [ file for file in listdir('web_page_data/'+str(year)) if file.endswith('.txt') and \
            datetime.strptime( re.findall('gid_(.{10})', file)[0].replace('_', ' '), '%Y %m %d' ) \
             >= opening_date ]

i = 0
bad_data = []
bad_data_frames = []
print len(files)

for file in files:
    with open( 'web_page_data/'+str(year)+'/'+file, 'rb') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html')
    if i%100==0: print i, 'of', len(files)
    i += 1
    for at_bat in soup.findAll('atbat'):
        x = []
        batter = re.findall('batter="(.+?)"', str(at_bat))
        pitcher = re.findall('pitcher="(.+?)"', str(at_bat))
        for pitch in at_bat.findAll('pitch'):
            try:
                x.append(feature_extract(pitch))
            except:
                bad_data.append([pitch])
                continue
        try:
            at_bat_data = pd.DataFrame(x)
            at_bat_data.columns = columns
            batter_file = str(batter[0])+'.csv'
            if batter_file in listdir('batter_data'):
                at_bat_data.to_csv('batter_data/'+batter_file, header=False, mode='a', index=False)
            else:
                at_bat_data.to_csv('batter_data/'+batter_file, header=True, mode='a', index=False)
        except:
            bad_data_frames.append(x)


