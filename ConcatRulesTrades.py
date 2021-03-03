'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
import numpy as np
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
import IdConverterMFL

MFLPlayers=IdConverterMFL.id_converter(update=True)

AllPlayers=MFLPlayers.Get_Players()
for player in AllPlayers:
    print(player)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

Rules=os.path.join(THIS_FOLDER,'data/MasterRules.csv')
Rules=pd.read_csv(Rules)
Rules["ID"]=Rules["ID"].map(str)

Trades=os.path.join(THIS_FOLDER,'data/TradesMaster.csv')
Trades=pd.read_csv(Trades)
Trades["LeagueID"]=Trades["LeagueID"].map(str)
RuleTrades=Trades.merge(Rules, left_on="LeagueID", right_on="ID")
Save=os.path.join(THIS_FOLDER,'data/RulesTrades.csv')

pos=['QB','RB','WR','TE','WR+TE','RB+WR+TE','FB','KR','PK','PN','Off','TMQB','TMRB','TMWR','TMTE','TMPK','TMPN','TMDL','TMLB','TMDB',
'Def','ST','DE','DT','DT+DE','LB','CB','S','CB+S']

for col in pos:
    RuleTrades[col]=RuleTrades[col].map(str)
    RuleTrades[col]=np.where(RuleTrades[col]!="nan",col+": "+RuleTrades[col]+", ","")
RuleTrades["Lineup"]=RuleTrades[pos].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
RuleTrades["Lineup"]=RuleTrades["Lineup"].str[:-2]

ppr=["QBTD","RBPPR","WRPPR","TEPPR"]
for col in ppr:
    RuleTrades[col].map(str)
RuleTrades["QBTD"]="QB_pTD: "+RuleTrades["QBTD"]
RuleTrades["RBPPR"]="RB_PPR: "+RuleTrades["RBPPR"]
RuleTrades["WRPPR"]="WR_PPR: "+RuleTrades["WRPPR"]
RuleTrades["TEPPR"]="TE_PPR: "+RuleTrades["TEPPR"]
RuleTrades["Scoring"]=RuleTrades[ppr].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)

for col in ["Side1","Side2"]:
    for letter in ["[","'","]"]:
        RuleTrades[col]=RuleTrades[col].str.replace(letter,'')

RuleTrades=RuleTrades[["Side1","Side2","Date","LeagueID","Scoring","Lineup"]]
RuleTrades.to_csv(Save)
    