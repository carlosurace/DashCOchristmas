'''
Created on Mar 17, 2021

@author: Carlo Surace
'''
import pandas as pd
import datetime
import os
import IdConverterMFL
from datetime import date

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
MFLPlayers=IdConverterMFL.id_converter()
AllPlayers=MFLPlayers.Get_Players()
excludepositions=[", Coach",", PK",", TM",", Off",", Def",", KR",", PN",", ST"]
for pos in excludepositions:
    AllPlayers=[p for p in AllPlayers if pos not in p]
AllPlayers=sorted(AllPlayers)
TradesRaw=os.path.join(THIS_FOLDER,'data/RulesTrades.csv')
TradesRaw=pd.read_csv(TradesRaw,parse_dates=['Date'])
TradesRaw["Date"]=TradesRaw["Date"].dt.date
TradesRaw=TradesRaw.sort_values("Date",ascending=False).reset_index(drop=True)



Tradescount=TradesRaw[TradesRaw["Date"]>date.today()-datetime.timedelta(60)]
LeagueCount=len(list(set(Tradescount["LeagueID"])))

print("LeagueCount",LeagueCount)
tradediffs=[7,14,30]
MostDict={}
for dif in tradediffs:
    diff=datetime.timedelta(dif)
    Tradesdiff=TradesRaw[TradesRaw["Date"]>date.today()-diff]
    df=pd.DataFrame(columns=["Player","Volume"])
    for player in AllPlayers:
        print(player)
        df.loc[len(df)]=[player,(Tradesdiff.Side1.str.count(player).sum()+Tradesdiff.Side2.str.count(player).sum())/LeagueCount]
    df=df.sort_values("Volume", ascending=False)
    MostDict[dif]=df

MostDict[7].to_csv(os.path.join(THIS_FOLDER,'data/Most7.csv'),Index=False)
MostDict[14].to_csv(os.path.join(THIS_FOLDER,'data/Most14.csv'),Index=False)
MostDict[30].to_csv(os.path.join(THIS_FOLDER,'data/Most30.csv'),Index=False)