from __future__ import division

import pandas as pd
import numpy as np 
import re
from datetime import datetime
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import seaborn as sns

from os import listdir




batters = [ file for file in listdir('current_batters/current_batters') if file.endswith('.csv') ]
pitchers = [ file for file in listdir('current_pitchers') if file.endswith('.csv') ]
player_ids = pd.read_csv('player_ids.csv', header=0)

list_of_current_batters = batters
list_of_current_pitchers = pitchers





# batter vs pitcher images

t1 = datetime.now()

count_set = [ '0, 0', '0, 1', '0, 2', '1, 0', '1, 1', '1, 2', '2, 0', '2, 1', '2, 2', \
                '3, 0', '3, 1', '3, 2' ]


# Map the zone to the geometric strike zone
x = [ 1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6, 1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6, 1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6,\
0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7]
y = [ 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 4, 4, 5, 5, 6, 6, 5, 5, 6, 6, 5, 5, 6, 6,\
3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4]



heads_up_results = list()

for batter_file in list_of_current_batters[300:]:  
    batter = pd.read_csv('current_batters/current_batters/' + batter_file, header=0)
    
    if (len(batter)) > 1000:
        
        batter_firstname = player_ids[player_ids.MLBCODE == float(batter_file[:-4])].FIRSTNAME.tolist()[0]
        batter_lastname = player_ids[player_ids.MLBCODE == float(batter_file[:-4])].LASTNAME.tolist()[0]
        batter_name = batter_firstname + ' ' + batter_lastname
        
        strike = []
        in_play = []
        ball = []
        foul = []

        for des in batter.des:
            if 'Strike' in des: strike.append(1)
            else: strike.append(0)
            if 'In play' in des: in_play.append(1)
            else: in_play.append(0)
            if 'Ball' in des: ball.append(1)
            else: ball.append(0)
            if 'Foul' in des: foul.append(1)
            else: foul.append(0)

        batter2 = batter[['zone', 'end_speed']]
        batter2.loc[:, 'strike'] = strike
        batter2.loc[:, 'in_play'] = in_play
        batter2.loc[:, 'ball'] = ball
        batter2.loc[:, 'foul'] = foul

        batter2.loc[:, 'totals'] = np.ones(len(batter2))
        batter3 = batter2[['strike', 'totals', 'zone']].groupby('zone').sum()
        rf_strike = np.array(batter3.strike / batter3.totals)

        batter3 = batter2[['in_play', 'totals', 'zone']].groupby('zone').sum()
        rf_in_play = np.array(batter3.in_play / batter3.totals)

        batter3 = batter2[['ball', 'totals', 'zone']].groupby('zone').sum()
        rf_ball = np.array(batter3.ball / batter3.totals)

        batter3 = batter2[['foul', 'totals', 'zone']].groupby('zone').sum()
        rf_foul = np.array(batter3.foul / batter3.totals)

        zone = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14 ] * 4    # note 10 does not exist on the MLB map
        event = ['ball']*13 + ['in_play']*13 + ['strike']*13 + ['foul']*13

        pbl_zone = list(rf_ball) + list(rf_in_play) + list(rf_strike) + list(rf_foul)
        data = pd.DataFrame( zip(zone, event, pbl_zone), columns = ['zone', 'event', 'pbl_zone'])


        #sns.set_style('whitegrid')

        # Strike Zone Heat Map
        # Percentage of Strikes per Pitches Thrown in a Particular Zone

        SP = list(data[data.event=='strike'].pbl_zone)
        IP = list(data[data.event=='in_play'].pbl_zone)
        BP = list(data[data.event=='ball'].pbl_zone)
        FP = list(data[data.event=='foul'].pbl_zone)
    
        #-----------------------------------------------------------------------------------------------
        # pitcher
        for pitcher_file in list_of_current_pitchers:

            pitcher = pd.read_csv('current_pitchers/' + pitcher_file, header=0)

            if (len(pitcher)) > 1000:
                pitcher_firstname = player_ids[player_ids.MLBCODE == float(pitcher_file[:-4])].FIRSTNAME.tolist()[0]
                pitcher_lastname = player_ids[player_ids.MLBCODE == float(pitcher_file[:-4])].LASTNAME.tolist()[0]
                pitcher_name = pitcher_firstname + ' ' + pitcher_lastname

                c = [ str(pitcher.ball_count[i])+', '+str(pitcher.strike_count[i]) for i in xrange(len(pitcher))]
                pitcher2 = pitcher
                pitcher2['count'] = c
                del(c)

                pitcher2['totals'] = np.ones(len(pitcher2))
                pitcher2 = pitcher2[['count', 'zone', 'totals']].groupby(['count', 'zone']).sum()/ \
                            pitcher2[['count', 'totals']].groupby(['count']).sum()


                d_rf = {}
                for j in count_set:
                    k = list()
                    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]:
                        try:
                            k.append(float(pitcher2.loc[(j, i)]))
                        except KeyError:
                            k.append(0)
                    d_rf[j] = k


                #rf = list(pitcher2.totals)
                #rf_pitch_per_zone = list(pitcher2.totals)
                #print rf
                #rf = [rf[0]]*4 + [rf[1]]*4 + [rf[2]]*4 + [rf[3]]*4 + [rf[4]]*4 + [rf[5]]*4 + [rf[6]]*4 + [rf[7]]*4 + [rf[8]]*4 + \
                #[rf[9]]*7 + [rf[10]]*7 + [rf[11]]*7 + [rf[12]]*7
                #print rf
                #pitch_zone = np.array(rf_pitch_per_zone)

                #print pitch_zone


                # Simulate an at-bat



                des_strikeout = 0
                des_inplay = 0
                des_walk = 0
                N = 10000
                for j in range(N):
                    i = 0
                    strike_count = 0
                    inplay_count = 0
                    ball_count = 0
                    foul_count = 0

                    while 1:

                        i += 1
                        n = np.random.random(1)
                        #rf = list(pitcher2.totals)
                        rf_pitch_per_zone = d_rf[str(ball_count)+', '+str(strike_count)]
                        #print rf
                        #rf = [rf[0]]*4 + [rf[1]]*4 + [rf[2]]*4 + [rf[3]]*4 + [rf[4]]*4 + [rf[5]]*4 + [rf[6]]*4 + [rf[7]]*4 + [rf[8]]*4 + \
                        #[rf[9]]*7 + [rf[10]]*7 + [rf[11]]*7 + [rf[12]]*7
                        #print rf
                        pitch_zone = np.array(rf_pitch_per_zone)

                        pbl_strike = sum(pitch_zone * SP)
                        pbl_inplay = sum(pitch_zone * IP)
                        pbl_ball = sum(pitch_zone * BP)
                        pbl_foul = sum(pitch_zone * FP)

                        if n < pbl_strike: strike_count += 1
                        elif pbl_strike <= n < pbl_strike + pbl_inplay: inplay_count += 1
                        elif pbl_strike + pbl_inplay <= n < pbl_strike + pbl_inplay + pbl_ball: ball_count += 1
                        elif pbl_strike + pbl_inplay + pbl_ball <= n: 
                            foul_count += 1
                            if strike_count < 2: strike_count+=1
                        else: pass #print "problem with counter"

                        if strike_count == 3: des_strikeout+=1; break
                        if inplay_count == 1: des_inplay+=1; break
                        if ball_count == 4: des_walk+=1; break
                """
                heads_up_results = pd.DataFrame({'Probability of Strike Out':(des_strikeout/N), 'Probability of Ball in Play':\
                                               (des_inplay/N), 'Probability of Walk':(des_walk/N)}, index=[1, 2, 3])

                #print heads_up_results
                sns.set_style('whitegrid')
                g = sns.barplot(x = ['Walk', 'Strike Out', 'In-play'], y = [des_walk/N, des_strikeout/N, des_inplay/N], \
                              palette="Blues_d")

                g.figure.suptitle('Batter %s vs Pitcher %s: Probabilities of At-Bat Outcomes' % (batter_name, pitcher_name), fontsize='14') 
                g.set_xlabel('')
                g.set_ylabel('Probability of Outcome')
                #print "Include average results, pre-calculated and stored or taken from the mlb site for the most recent or all years."
                plt.ylim(0, 0.9)
                plt.savefig('matchup_images/%s_vs_%s_at_bat_prediction.png' %(batter_name, pitcher_name))
                plt.close() 
                """

                t = 'Batter %s vs Pitcher %s: Probabilities of At-Bat Outcomes' % (batter_name, pitcher_name)
                heads_up_results.append([ t, des_strikeout/N, des_inplay/N, des_walk/N ])
df = pd.DataFrame(heads_up_results)
df.columns = [ 'title', 'strikeout', 'inplay', 'walk' ]
df.to_csv('results.csv', index=False)
            
print datetime.now() - t1

