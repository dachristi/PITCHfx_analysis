# PITCHfx_analysis


This repository holds the Python code for the analytics behind http://www.battervspitcher.com.  The question we are trying to answer is: “What are the possible outcomes of an at-bat between a particular pitcher and batter?”  This question is not straight-forward to answer because there is so little (if any) pitcher/batter historical data.  The approach taken here is to profile a batter based on all pitches he has seen, and the relative frequency of outcomes (ball, ip-play hit, srike, foul).  Similarly, pitchers are profiled on all pitches they have thrown.  Using the profiles of the 2 players, we can predict at-bat outcomes for particular batter/pitcher match-ups.

The notebook pitchfx_data_collection_and_feature_extraction.ipynb provides the code to extract pitchf/x data from the MLB Gameday XML API.  It also organizes the data from being game-specific to player-specific.  Separating the tasks of data acquisition and feature extraction is highly recommended because of the length of time each task takes.  I supplied 2 Python scripts that I ran on a remote server: batter_feature_extraction.py and feature_feature_extraction.py.  A third script, pitchfx_data_collection.py was used to collect data from the Gameday API.  



