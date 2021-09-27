'''
Created on Sep 1, 2021

@author: Carlo Surace
'''

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
from App import  app
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc
import random


UserDict={'ID'+str(i).zfill(3):'User'+str(i) for i in range(0,400)}
'''
df=pd.DataFrame(columns=['Time','Type','Amount','Notes'])
for i in range(0,350):
    df.to_csv('Accounts/'+str(i).zfill(3)+'.csv',index=False)
'''   
CarOfferContest =html.Div([
        html.H1(children='Car Offer Christmas'),
        html.Div(id="wrapper",children=[html.Div(id="contest",)])
        ])

CarOfferTransactions =html.Div([
        html.H1(children='Car Offer Christmas'),
        html.Div(id="wrapper",
            children=
            [
            dcc.Dropdown(id="Account",
                         options=[{'label': str(i).zfill(3), 'value': str(i).zfill(3)} for i in range(0,350)]),
            html.Div(id="AccountInfo"),
            html.Div(id="Transactions"),
            dbc.Row([dbc.Col([dcc.Input(id="Amount",placeholder='Enter Amount')],width=1),
                     dbc.Col([dcc.Input(id="Notes",placeholder='Notes')],width=4),  
                     dbc.Button(
             "Deposit",
             id="Deposit",
            style={'margin':'4px','backgroundColor':"#fff",'color':"#000",'borderColor':"#000"}
                ),
                    dbc.Button(
             "Withdraw",
             id="Withdraw",
            style={'margin':'4px','backgroundColor':"#fff",'color':"#000",'borderColor':"#000"}
                )]),
                ]
            )
        ])

CarOfferLeaderBoard=html.Div([
        html.H1(children='Car Offer Christmas'),
        dcc.Interval(id='int',interval=5000),
        html.Div(id="wrapper",children=[html.Div(id="Leaderboard")])
        ])


def GetBalance(ID):
    try:
        data=pd.read_csv('Accounts/'+str(ID)+'.csv')
        data["sum"]=np.where(data["Type"]=="Withdraw",-data["Amount"],data["Amount"])
        
        lastseen=data["Amount"][data["Type"]=="Withdraw"].reset_index(drop=True)
        try:
            lastseen=lastseen[len(lastseen)-1]
        except:
            lastseen=0
        Balance=data["sum"]=data["sum"].sum()
        Info = dbc.Row([html.H5("Account Balance: $"+str(Balance)),html.H5("Last Withdrawal: $"+str(lastseen))])
        leaderboard=pd.read_csv('Accounts/Leaderboard.csv')
        leaderboard=leaderboard[leaderboard.ID!='ID'+ID].reset_index(drop=True)
        leaderboard.loc[len(leaderboard)]=['ID'+ID,UserDict['ID'+ID],Balance,lastseen]
        leaderboard.to_csv('Accounts/Leaderboard.csv',index=False)
        return Info
    except Exception as inst:
        return html.H5(str(inst))
    
def GetTransactions(ID):
    try:
        data=pd.read_csv('Accounts/'+str(ID)+'.csv')
        trans=[]
        for i in range(len(data)):
            trans.append(dbc.Row([dbc.Col(html.H5(str(data["Time"].iloc[i])),width=2),dbc.Col(html.H5(str(data["Type"].iloc[i])),width=2),dbc.Col(html.H5(str(data["Amount"].iloc[i])),width=2),dbc.Col(html.H5(str(data["Notes"].iloc[i])),width=2)]))
        return trans
    except Exception as inst:
        print(Exception)
        return html.H5(str(inst))

def transact(ID,Amount,Type,Notes):
    data=pd.read_csv('Accounts/'+str(ID)+'.csv')
    data.loc[len(data)]=[str(datetime.now()),Type,int(Amount),str(Notes)]
    data.to_csv('Accounts/'+str(ID)+'.csv',index=False)                         
@app.callback(
    [Output(component_id='AccountInfo', component_property='children'),
     Output(component_id='Transactions', component_property='children'),
     Output(component_id='Amount', component_property='value')], # or is there a different one for table
    [Input(component_id='Account', component_property='value'),
     Input(component_id='Deposit', component_property='n_clicks'),
     Input(component_id='Withdraw', component_property='n_clicks')],
    [State(component_id='Amount', component_property='value'),
     State(component_id='Notes', component_property='value')])
    
def UpdateDrop (ID,D,W,Amount,Notes):
    ctx = dash.callback_context
    trigger=ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger=='Deposit' or trigger=='Withdraw':
        transact(ID,Amount,trigger,Notes)
        Amount=None
        
    Info=GetBalance(ID)
    
    trans=GetTransactions(ID)
    return [Info],trans,Amount

@app.callback(
    [Output(component_id='Leaderboard', component_property='children')], # or is there a different one for table
    [Input(component_id='int', component_property='n_interval')])
    
def Leader (Int):
    print("tRY")
    leaderboard=pd.read_csv('Accounts/Leaderboard.csv')
    leaderboard=leaderboard.sort_values('Balance').reset_index(drop=True)
    led=[]
    for i in range(0,10):
        led.append(dbc.Row([dbc.Col(html.H5(str(i)),width=2),dbc.Col(html.H5(str(leaderboard["Name"].iloc[i])),width=2),dbc.Col(html.H5(str(leaderboard["Balance"].iloc[i])),width=2)]))
    return [led]


@app.callback(
    [Output(component_id='contest', component_property='children')], # or is there a different one for table
    [Input(component_id='sub-int1', component_property='n_interval')], prevent_initial_call=True)
def contest (Int):
    print("tRY")
    num=random.randint(0,400)
    return [html.H1(str(num))]
'''
@app.callback(
    [Output(component_id='main-int', component_property='interval')], # or is there a different one for table
    [Input(component_id='sub-int1', component_property='n_interval')],
    [State(component_id='main-int', component_property='interval')]
    )
def change (trig,int):
    return [int*10]
'''