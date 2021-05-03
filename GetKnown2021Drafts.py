'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
import ConfigF as Conf
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


Startups=pd.read_csv(Conf.StartupsPath)


Confirmed=pd.read_csv(Conf.ConfirmedPath)
Newleagues=Confirmed['league_id'].map(str)
Newleagues=list(set(Newleagues))
print(len(Newleagues),"New Leagues")



temppath=os.path.join(THIS_FOLDER,"data/Temp.csv")

picks=mfl.get_multiple_leagues_draftsAll(Newleagues, temppath, year=2021, disable_progess_bar=False)
temp=pd.read_csv(temppath)

temp=temp.merge(Confirmed[["Name","Lineup","Scoring","Teams","Copies","league_id"]], on="league_id")
temp["posrank"] = temp.groupby(["league_id","Position"])["Overall"].rank("dense")

temp["Date"]=temp["Date"].fillna(0)
temp["Date"]=pd.to_datetime(temp["Date"].astype(int), unit='s')
newcodes=list(set(temp["league_id"].map(int)))
Startups["league_id"]=Startups["league_id"].map(int)
Startups=Startups[~Startups.league_id.map(int).isin(newcodes)]
Startups=Startups.append(temp)

temp.to_csv(Conf.StartupsPath)

