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
import ast
import ConfigF as Conf

MFLPlayers=IdConverterMFL.id_converter(update=True)

AllPlayers=MFLPlayers.Get_Players()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

Rules=os.path.join(THIS_FOLDER,'data/MasterRules.csv')
Rules=pd.read_csv(Rules)
Rules["ID"]=Rules["ID"].map(str)

Trades=os.path.join(THIS_FOLDER,'data/TradesMaster.csv')
Trades=pd.read_csv(Trades,parse_dates=['Date'])
print(max(Trades['Date']))
Trades["LeagueID"]=Trades["LeagueID"].map(str)

Save=os.path.join(THIS_FOLDER,'data/RulesTrades.csv')

pos=['QB','RB','WR','TE','WR+TE','RB+WR+TE','FB','KR','PK','PN','Off','TMQB','TMRB','TMWR','TMTE','TMPK','TMPN','TMDL','TMLB','TMDB',
'Def','ST','DE','DT','DT+DE','LB','CB','S','CB+S']

for col in pos:
    Rules[col]=Rules[col].map(str)
    Rules[col]=np.where(Rules[col]!="nan",col+": "+Rules[col]+", ","")
Rules["Lineup"]=Rules[pos].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
Rules["Lineup"]=Rules["Lineup"].str[:-2]

ppr=["QBTD","RBPPR","WRPPR","TEPPR"]
for col in ppr:
    Rules[col].map(str)
Rules["QBTD"]="QB pTD: "+Rules["QBTD"]
Rules["RBPPR"]="RB PPR: "+Rules["RBPPR"]
Rules["WRPPR"]="WR PPR: "+Rules["WRPPR"]
Rules["TEPPR"]="TE PPR: "+Rules["TEPPR"]
Rules["Scoring"]=Rules[ppr].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)



Vet=pd.read_csv(Conf.ConfirmedPath)
Rook=pd.read_csv(Conf.ConfirmedRookiePath)
Vet=Vet[["league_id","Scoring","Lineup"]]
Rook=Rook[["league_id","Scoring","Lineup"]]

drafts=pd.concat([Vet,Rook], axis=0, ignore_index=False)
drafts.columns=["ID","Scoring","Lineup"]
Rules=pd.concat([Rules,drafts], axis=0, ignore_index=False)
RuleTrades=Trades.merge(Rules, left_on="LeagueID", right_on="ID")

for col in ["Side1","Side2"]:
    #RuleTrades[col]=RuleTrades[col].str.replace('"',"'")
    RuleTrades[col]=RuleTrades[col].apply(lambda x: ast.literal_eval(str(x)))
    RuleTrades[col]=["\n".join([", ".join(list(i)) if type(i)==tuple else i for i in RuleTrades[col].loc[n]]) if type(RuleTrades[col].loc[n])==list else RuleTrades[col].loc[n] for n in range(len(RuleTrades))]
    '''
    for letter in ["'),","\),","', '"]:
        RuleTrades[col]=RuleTrades[col].str.replace(letter,' \n')
    for letter in ["\['","'\]","\[","\]","\('","\("]:
        RuleTrades[col]=RuleTrades[col].str.replace(letter,'')
    for letter in ["',"]:
        RuleTrades[col]=RuleTrades[col].str.replace(letter,',')
    for letter in ["'\)","\)"," '"]:
        RuleTrades[col]=RuleTrades[col].str.replace(letter,' ')
    '''
RuleTrades=RuleTrades.sort_values("Date",ascending=False).reset_index(drop=True)
print(max(Trades['Date']))
RuleTrades=RuleTrades[["Side1","Side2","Date","LeagueID","Scoring","Lineup"]]
RuleTrades=RuleTrades.drop_duplicates()
RuleTrades.to_csv(Save)
