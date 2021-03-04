'''
Created on Mar 4, 2021

@author: Carlo Surace
'''
'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

Rules=os.path.join(THIS_FOLDER,'data/MasterRules.csv')
Rules=pd.read_csv(Rules)
Rules=Rules["ID"].map(str)
print(len(Rules))
Tradepath=os.path.join(THIS_FOLDER,'data/TradesMaster.csv')
Trades=pd.read_csv(Tradepath)
trades=[]
print(len(Rules))
for league in Rules[0:10]:
    try:
        trades+=mfl.get_league_trades(league, 2021, csv_writer=None)
        print(league,"success")
    except:
        print(league,"fail")
        continue
df = pd.DataFrame(trades, columns=["Side1","Side2","Date","LeagueID"])
df["Date"]=pd.to_datetime(df["Date"].astype(int), unit='s')
Trades=pd.concat([Trades,df], axis=0, ignore_index=False)
Trades.drop_duplicates()
Tradepath=os.path.join(THIS_FOLDER,'data/TradesMaster.csv')
Trades.to_csv(Tradepath)
