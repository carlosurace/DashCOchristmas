'''
Created on Aug 2, 2021

@author: Carlo Surace
'''

from bs4 import BeautifulSoup
import requests
import re
import json
import time
from tqdm import tqdm
from IdConverterMFL import id_converter
import csv
import os
import pandas as pd
from espn_api.baseball import League
import dash_bootstrap_components as dbc

from App import  app
import pandas as pd
import numpy as np


from dash.dependencies import Input,Output,State
import dash
import os
import csv
import sys
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
s = requests.Session()
r = s.get('https://www.espn.com')

swid = s.cookies.get_dict()['SWID']

STATS_MAP = {
    0: 'AB',
    1: 'H',
    2: 'AVG',
    3: '2B',
    4: '3B',
    5: 'HR',
    6: 'XBH', # 2B + 3B + HR
    7: '1B',
    8: 'TB', # 1 * COUNT(1B) + 2 * COUNT(2B) + 3 * COUNT(3B) + 4 * COUNT(HR)
    9: 'SLG',
    10: 'B_BB',
    11: 'B_IBB',
    12: 'HBP',
    13: 'SF', # Sacrifice Fly
    14: 'SH', # Sacrifice Hit - i.e. Sacrifice Bunt
    15: 'SAC', # total sacrifices = SF + SH
    16: 'PA',
    17: 'OBP',
    18: 'OPS', # OBP + SLG
    19: 'RC', # Runs Created = TB * (H + BB) / (AB + BB)
    20: 'R',
    21: 'RBI',
    # 22: '',
    23: 'SB',
    24: 'CS',
    25: 'SB-CS', # net steals
    26: 'GDP',
    27: 'B_SO', # batter strike-outs
    28: 'PS', # pitches seen
    29: 'PPA', # pitches per plate appearance = PS / PA
    # 30: '',
    31: 'CYC',
    32: 'GP', # pitcher games pitched
    33: 'GS', # games started
    34: 'OUTS',  # divide by 3 for IP
    35: 'TBF',
    36: 'P',  # pitches
    37: 'P_H',
    38: 'OBA', # Opponent Batting Average
    39: 'P_BB',
    40: 'P_IBB', # intentional walks allowed
    41: 'WHIP',
    42: 'HBP',
    43: 'OOBP', # Opponent On-Base Percentage
    44: 'P_R',
    45: 'ER',
    46: 'P_HR',
    47: 'ERA',
    48: 'K',
    49: 'K/9',
    50: 'WP',
    51: 'BLK',
    52: 'PK', # pickoff
    53: 'W',
    54: 'L',
    55: 'WPCT', # Win Percentage
    56: 'SVO', # Save opportunity
    57: 'SV',
    58: 'BLSV', # BLown SaVe
    59: 'SV%', # Save percentage
    60: 'HLD',
    # 61: '',
    62: 'CG',
    # 63: '',
    # 64: '',
    65: 'NH', # No-hitters
    66: 'PG', # Perfect Games
    67: 'TC', # Total Chances = PO + A + E
    68: 'PO', # Put Outs
    69: 'A', # Assists
    70: 'OFA', # Outfield Assists
    71: 'FPCT', # Fielding Percentage
    72: 'E',
    73: 'DP', # Double plays turned
    # Not sure what to call the next four
    # 74 is games played where the batter's team won
    # 75 is the same except when the team lost
    # 76 and 77 are the same except for pitchers
    74: 'B_G_W', 
    75: 'B_G_L',
    76: 'P_G_W',
    77: 'P_G_L',
    # 78: ,
    # 79: ,
    # 80: ,
    81: 'G', # Games Played
    82: 'K/BB', # Strikeout to Walk Ratio
    99: 'STARTER',
}
LeagueIds={
    3334:"Bo Jackson",
    4575: "Ted Williams",
    12812: "Sandy Koufax",
    12848: "Frank Thomas",
    31036: "Jackie Robinson",
    9342: "Roger Maris",
    31470: "Roberto Clemente",
    49488: "Rollie Fingers",
    81126:"Oil Can Boyd",
    136347:"Hank Aaron",
    92156970:"Pete Rose",
    52652889:"Barry Bonds",
    73273492:"Babe Ruth",
    50137987:"Lou Gehrig",
    46038856:"Carlton Fisk"
    }

def updatedata():
    master=pd.DataFrame(columns=["Division","Rank","Team","R","HR","RBI","SB","OBP","K","W","SV","ERA","WHIP","GP","IP","Moves"])
    for LID in LeagueIds:
        league = League(league_id=LID, year=2021, debug=True)
        data=league._fetch_league()
        
        df=pd.DataFrame(columns=["Division","Rank","Team","R","HR","RBI","SB","OBP","K","W","SV","ERA","WHIP","GP","IP","Moves"])
        for i in data["teams"]:
            row=[]
            row+=[LeagueIds[LID]]
            row+=[i["currentProjectedRank"]]
            row+=[i["location"]+' '+i["nickname"]]
            for stat in [20,5,21,23,17,48,53,57,47,41,81]:
                row+=[i["valuesByStat"][str(int(stat))]]
            row+=[i["valuesByStat"]['34']/3]
            row+=[i["transactionCounter"]["matchupAcquisitionTotals"]['1']]
            df.loc[len(df)]=row
        df.to_csv(THIS_FOLDER+"/BaseballStandings/"+str(LID)+".csv",index=False)
        master=pd.concat([master,df], axis=0, ignore_index=False)
        print(LeagueIds[LID],"Done")
    master.to_csv(THIS_FOLDER+"/BaseballStandings/MasterStats.csv",index=False)
    rankcols=["R","HR","RBI","SB","OBP","K","W","SV"]
    for col in rankcols:
        master[col] = master[col].rank(ascending=True)
    rankcols1=["ERA","WHIP"]
    for col in rankcols1:
        master[col+"Rank"]= master[col].rank(ascending=False)
    master["Sum"]=master[rankcols+rankcols1].sum(axis=1)
    master["Rank"] = master["Sum"].rank(ascending=False)
    master.to_csv(THIS_FOLDER+"/BaseballStandings/MasterRankings.csv") 

master=pd.DataFrame(columns=["Division","Rank","Team","R","HR","RBI","SB","OBP","K","W","SV","ERA","WHIP","GP","IP","Moves"])
for LID in LeagueIds:
    df=pd.read_csv(THIS_FOLDER+"/BaseballStandings/"+str(LID)+".csv")
    master=pd.concat([master,df], axis=0, ignore_index=False)
master.to_csv(THIS_FOLDER+"/BaseballStandings/MasterStats.csv",index=False)
rankcols=["R","HR","RBI","SB","OBP","K","W","SV"]
for col in rankcols:
    master[col] = master[col].rank(ascending=True)
rankcols1=["ERA","WHIP"]
for col in rankcols1:
    master[col]= master[col].rank(ascending=False)
master["Sum"]=master[rankcols+rankcols1].sum(axis=1)
master["Rank"] = master["Sum"].rank(ascending=False)
master.to_csv(THIS_FOLDER+"/BaseballStandings/MasterRankings.csv",index=False)
#updatedata()


Brent =html.Div([
        html.H1(children='The Carson Wentz Memorial Leaderboard'),
        html.Div(id="wrapper",children=[
        dbc.Row([
            dbc.Col([dbc.Label("View")],width=1),
        
                dbc.Col([dcc.Dropdown(id = 'View',value="Rankings"
                        ,options=[
                            {'label': i, 'value': i} for i in ["Rankings","Stats"]],
                        multi=False
                        ,className="dash-bootstrap"
                    )],width=4),
        dbc.Col([
             dbc.Button(
             "Refresh Data",
             id="BrentRefresh",
            style={'margin':'4px','backgroundColor':"#fff",'color':"#000",'borderColor':"#000"}
                ),
            ],width=2),
        ]),
        dcc.Loading(html.Div(id="Brentdiv"))
        ])
        ])



@app.callback(
    Output(component_id='Brentdiv', component_property='children'), # or is there a different one for table
    [Input(component_id='View', component_property='value'),
     Input(component_id='BrentRefresh', component_property='n_clicks')
    ])
    
def dashtable ( View,click):
    ctx = dash.callback_context
    trigger=ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger=="BrentRefresh":
        updatedata()
    if View =="Rankings":
        file = "/BaseballStandings/MasterRankings.csv"
        data=pd.read_csv(THIS_FOLDER+file)
        data = data[[col for col in data.columns if col not in [""] and "Unnamed" not in col]]
        data=data.sort_values(by='Rank', ascending=True)
    else:
        file = "/BaseballStandings/MasterStats.csv"
        data=pd.read_csv(THIS_FOLDER+file)
        data = data[[col for col in data.columns if col not in ["Rank"] and "Unnamed" not in col]]
        
    tab=dt.DataTable(
        id='Euc return table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        sort_action="native",
        style_header={
             'fontSize':14,
            'fontFamily': 'helvetica',
            'border': 'thin #a5d4d9 solid',
            'color': '#a5d4d9',
            'backgroundColor': '#313131',
            'padding':'10px'
            },
        style_filter={'color': '#fff', "backgroundColor": "#313131"},
        style_table={'minHeight':'auto','height': 'auto','maxHeight':'auto','border': '#000','height': 'auto',"width":"95%"},
        style_data={'whiteSpace': 'pre-line'},
        style_cell={
        'fontSize':12,
        'border': 'thin #a5d4d9 solid',
        'fontFamily': 'helvetica',
        'textAlign': 'left',
        'Width': 'auto',
        'maxWidth': 0,
        'height': 'auto',
        'whiteSpace': 'normal',
        'padding':'10px',
        'color': '#a5d4d9',
        'backgroundColor': '#313131'
        },
        )
    return tab
    
'''
AB
H
OUTS
HR
P_H
P_BB
WHIP
B_BB
HBP
SF
ER
ERA
K
OBP
G
R
RBI
W
SB
SV

abbrev
currentProjectedRank
divisionId
draftDayProjectedRank
draftStrategy
id
isActive
location
logo
logoType
nickname
owners
playoffSeed
points
pointsAdjusted
pointsByStat
pointsDelta
primaryOwner
rankCalculatedFinal
rankFinal
record
roster
tradeBlock
transactionCounter
valuesByStat
waiverRank

draftDetail
gameId
id
members
schedule
scoringPeriodId
seasonId
segmentId
settings
status
teams
'''