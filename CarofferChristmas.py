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
from App import  app,cache
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc
import random
import base64
image_filename = 'COLOGO.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
CarOfferLogo='data:image/png;base64,{}'.format(encoded_image)

pimage_filename = 'Player.png' # replace with your own image
pencoded_image = base64.b64encode(open(pimage_filename, 'rb').read()).decode('ascii')
pCarOfferLogo='data:image/png;base64,{}'.format(pencoded_image)

UserDict={'ID'+str(i).zfill(3):'User'+str(i) for i in range(0,400)}
'''
df=pd.DataFrame(columns=['Time','Type','Amount','Notes'])
for i in range(0,350):
    df.to_csv('Accounts/'+str(i).zfill(3)+'.csv',index=False)
'''   
CarOfferContest =html.Div([
        html.Div(html.Img(src=CarOfferLogo, height="80px"),style={'width':'100%','height':'200px',}),
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

CarOffBossMode =html.Div([
        html.H1(children='Car Offer Christmas'),
        html.Div(id="wrapper",children=[html.Div(id="contest",)])
        ])

CarOfferTransactions =html.Div([
        html.Div([
            html.Div([html.Img(src=CarOfferLogo, height="80px",style={'width':'600px','height':'100px',"margin":"64px 50px 50px 30px"})],id="wrapper",style={'width':'2048px',"flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([
                dcc.Dropdown(id="Account",className="caroffer",
                         options=[{'label': str(i).zfill(3), 'value': str(i).zfill(3)} for i in range(0,350)],
                         placeholder="First Last Name",
                         style={'width':'1000px',"margin-left":"0px",'font-size':'42px','padding':"12px"}),
                         html.Div("Balance:",id="balance",style={'font-size':'42px','font-weight':'bold',"margin-left":"200px","color":"#ccff00",'height':'86px'})
                ],id="wrapper",style={'width':'2048px',"flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([html.Div([
                    dcc.Input(id="Amount",className="caroffer",type='number',placeholder='Enter Amount',style={'font-size':'42px','width':'300px','height':'86px','margin':'12px','backgroundColor':"#292929",'color':"#fff",}),
                      dcc.Input(id="Notes",className="caroffer",placeholder='Notes',style={'font-size':'42px','width':'1000px','height':'86px','margin':'12px','backgroundColor':"#292929",'color':"#fff",}) ,
                      dbc.Button(
                        "Deposit",
                        id="Deposit",
                        style={'font-size':'42px','width':'250px','height':'86px','margin':'12px','backgroundColor':"#177DDC",'color':"#fff",'borderColor':"#177DDC"}
                            ),
                     dbc.Button(
                        "Withdraw",
                        id="Withdraw",
                        style={'font-size':'42px','width':'250px','height':'86px','margin':'12px','backgroundColor':"#292929",'color':"#177DDC",'borderColor':"#177DDC"}
                            ),
                 ],style={'width':'2048px',"height":"200px",'padding':'40px 0px',"flex-direction": "row","display": "flex","background-color":"#434343","margin":"auto"}
            )],style={'width':'100%',"height":"200px","background-color":"#434343"}),
            html.Div(id="Transactions")
            ])
            ],style={'width':'100%','height':'200px',"flex-direction": "column","display": "flex"})
        # html.Div(id="wrapper",
        #     children=
        #     [
            
        #     html.Div(id="AccountInfo"),
        #     html.Div(id="Transactions"),
        #     dbc.Row([dbc.Col([dcc.Input(id="Amount",placeholder='Enter Amount')],width=1),
        #              dbc.Col([dcc.Input(id="Notes",placeholder='Notes')],width=4),  
        #              dbc.Button(
        #      "Deposit",
        #      id="Deposit",
        #     style={'margin':'4px','backgroundColor':"#fff",'color':"#000",'borderColor':"#000"}
        #         ),
        #             dbc.Button(
        #      "Withdraw",
        #      id="Withdraw",
        #     style={'margin':'4px','backgroundColor':"#fff",'color':"#000",'borderColor':"#000"}
        #         )]),
        #         ]
        #     )
        

CarOfferLeaderBoard=html.Div([
        html.Div([html.Img(src=CarOfferLogo, height="80px",style={'width':'600px','height':'100px',"margin":"64px 50px 50px 30px"})],id="wrapper",style={'width':'2048px',"flex-direction": "row","display": "flex","margin-bottom":"24px","margin":"auto"}), 
        dcc.Interval(id='int',interval=5000),
        html.Div(id="wrapper",children=[html.Div(id="Leaderboard",style={"width":"1000px","margin-bottom":"48px",'font-size':'36px',"margin":"auto","color":"#ccff00","display": "grid","grid-row-gap":"5px","grid-template-columns":"70px 180px 250px 250px","padding": "auto"})])
        ])


def GetBalance(ID):
    data=cache.get(str(ID))
    if data is None:
        data=[{"Time":None,"Transaction":1000,"Notes":"Initial Deposit"}]
        cache.set(str(ID),data)
    if len(data)>0:
        Balance=sum(c["Transaction"] for c in data)
        Inplay=data[len(data)-1]["Transaction"]
    else:
        Balance=0
        Inplay=0
    
    
    Inplay=-Inplay if Inplay<0 else 0
    return Balance,Inplay

def GetTransactions(ID):
    data=cache.get(str(ID))
    if data is None:
        data=[{"Time":None,"Transaction":1000,"Notes":"Initial Deposit"}]
        cache.set(str(ID),data)
    trans=[]
    for i in data:
        trans.append(dbc.Row([dbc.Col(html.H5(str(i["Time"])),width=2),dbc.Col(html.H5(str(i["Transaction"])),width=2),dbc.Col(html.H5(str(i["Notes"])),width=2)]))
    return trans

def transact(ID,Amount,Notes):
    data=cache.get(str(ID))
    data.append({"Time":str(datetime.now()),"Transaction":int(Amount),"Notes":str(Notes)})
    cache.set(str(ID),data)                      
@app.callback(
    [Output(component_id='balance', component_property='children'),
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
    if trigger=='Deposit':
        transact(ID,Amount,Notes)
        Amount=None
    if trigger=='Withdraw':
        transact(ID,-Amount,Notes)
        Amount=None
        
        
    bal,ip=GetBalance(ID)
    
    trans=GetTransactions(ID)
    return ["Balance: "+str(bal)+"("+str(ip)+")"],trans,Amount

@app.callback(
    [Output(component_id='Leaderboard', component_property='children')], # or is there a different one for table
    [Input(component_id='int', component_property='n_intervals')])
    
def Leader (Int):
    print("tRY",Int)
    leaderboard=pd.read_csv('Accounts/Leaderboard.csv')
    leaderboard=leaderboard.sort_values('Balance').reset_index(drop=True)
    led=[]
    for i in range(len(leaderboard)):
        bal,ip=GetBalance(str(leaderboard["ID"].iloc[i])[2:])
        leaderboard["Balance"].iloc[i]=bal
        leaderboard["InPlay"].iloc[i]=bal
    leaderboard=leaderboard.sort_values("Balance",ascending=False)
    led+=[html.Div("Rank",style={"padding":"5px 0px","width":"auto"},className="one-edge-shadow"),
        html.Div([],className="one-edge-shadow"),
        html.Div(str("Name"),style={"padding":"5px 0px"},className="one-edge-shadow"),
        html.Div("$"+str("Balance"),style={"padding":"5px 0px"},className="one-edge-shadow")]
    for i in range(0,10):
        led+=[html.Div("#"+str(i+1),style={"padding":"5px 0px","width":"auto"},className="one-edge-shadow"),
        html.Div(html.Img(src=pCarOfferLogo,style={"color":"white","height":"80px","width":"80px"} ),className="one-edge-shadow"),
        html.Div(str(leaderboard["Name"].iloc[i]),style={"padding":"5px 0px"},className="one-edge-shadow"),
        html.Div("$"+str(leaderboard["Balance"].iloc[i]),style={"padding":"5px 0px"},className="one-edge-shadow")]
    return [led]


@app.callback(
    [Output(component_id='contest', component_property='children')], # or is there a different one for table
    [Input(component_id='sub-int1', component_property='n_intervals')], prevent_initial_call=True)
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