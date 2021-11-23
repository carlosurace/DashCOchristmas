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
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
image_filename = THIS_FOLDER +'/COLOGO.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
CarOfferLogo='data:image/png;base64,{}'.format(encoded_image)

pimage_filename = THIS_FOLDER +'/Player.png' # replace with your own image
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




CarOfferTransactions =html.Div([
    dcc.ConfirmDialog(
        id='confirm',
        message=''
    ),
        html.Div([
            html.Div([html.Img(src=CarOfferLogo, height="80px",style={'width':'600px','height':'100px',"margin":"64px 50px 50px 30px"})],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([
                dcc.Input(id="Account",autoFocus=True,required=True ,minLength=3,maxLength=3,className="caroffer",type='number',placeholder='Acct Num',style={'font-size':'42px','width':'300px','height':'86px','margin':'12px','backgroundColor':"#000",'color':"#fff",}),
                         html.Div("Balance:",id="balance",style={'width':'600px','font-size':'36px','font-weight':'bold','padding':'15px 0px',"margin-left":"24px","color":"#fff",'height':'86px'})
                ],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([
                        html.Div("",id="player",style={'font-size':'36px','font-weight':'bold','padding':'15px 0px',"margin-left":"24px","color":"#fff",'height':'86px'}),
                        html.Div("",id="employee",style={'font-size':'36px','font-weight':'bold','padding':'15px 0px',"margin-left":"24px","color":"#fff",'height':'86px'})
                ],id="wrapper",style={'width':'900px',"flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([html.Div([
                    dcc.Input(id="Amount",className="caroffer",type='number',placeholder='Enter Amount',style={'font-size':'36px','width':'250px','height':'86px','margin':'12px','backgroundColor':"#292929",'color':"#fff",}),
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
                      
                 ],style={'width':'100%',"justify-content": "space-around","height":"200px",'padding':'40px 0px',"flex-direction": "row","display": "flex","background-color":"#434343","margin":"auto"}
            )],style={'width':'100%',"height":"200px","background-color":"#434343"}),
            html.Div([html.Div([
                dcc.Input(id="Notes",className="caroffer",placeholder='Notes',style={'font-size':'42px','width':'850px','height':'86px','margin':'12px','backgroundColor':"#292929",'color':"#fff",}) 
                 ],style={'width':'100%',"justify-content": "space-around","height":"200px",'padding':'0px 0px',"flex-direction": "row","display": "flex","background-color":"#434343","margin":"auto"}
            )],style={'width':'100%',"height":"200px","background-color":"#434343"}),
            html.Div(id="Transactions")
            ])
            ],style={'width':'900px','height':'200px',"flex-direction": "column","display": "flex","margin":"auto"})
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
        html.Div([html.Img(src=CarOfferLogo, height="80px",style={'width':'600px','height':'100px',"margin":"40px 0px 0px 0px"})],id="wrapper",style={"margin":"auto",'width':'800px',"flex-direction": "row","display": "flex","margin-bottom":"24px","margin":"auto"}), 
        dcc.Interval(id='int',interval=5000),
        html.Div([dcc.Input(id="leadersearch",className="caroffer",debounce=False,placeholder='search...',style={'font-size':'42px','width':'300px','height':'49px','margin':'12px 0px','backgroundColor':"#000",'color':"#fff",})],id="wrapper",style={"margin":"auto",'width':'800px',"flex-direction": "row","display": "flex","margin-bottom":"24px","margin":"auto"}),
        html.Div(id="wrapper",children=[html.Div(id="Leaderboard",style={"width":"800px","margin-bottom":"48px",'font-size':'36px',"margin":"auto","color":"#ccff00","display": "grid","grid-row-gap":"10px","grid-template-columns":"90px 130px auto 200px","padding": "auto"})])
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

def GetName(ID):
    data=pd.read_csv("Players.csv")
    names=dict(zip(data["Account"],data["Name"]))
    hosts=dict(zip(data["Account"], data["Employee"]))
    return names.get(ID,0),hosts.get(ID,0)

def transact(ID,Amount,Notes):
    data=cache.get(str(ID))
    data.append({"Time":str(datetime.now()),"Transaction":int(Amount),"Notes":str(Notes)})
    cache.set(str(ID),data)                      
@app.callback(
    [Output(component_id='balance', component_property='children'),
     Output(component_id='Transactions', component_property='children'),
     Output(component_id='Amount', component_property='value'),
     Output(component_id='player', component_property='children'),
     Output(component_id='employee', component_property='children'),
     Output(component_id='confirm', component_property='displayed'),
     Output(component_id='confirm', component_property='message')], # or is there a different one for table
    [Input(component_id='Account', component_property='value'),
     Input(component_id='Deposit', component_property='n_clicks'),
     Input(component_id='Withdraw', component_property='n_clicks')],
    [State(component_id='Amount', component_property='value'),
     State(component_id='Notes', component_property='value')])  
def UpdateDrop (ID,D,W,Amount,Notes):
    ctx = dash.callback_context
    trigger=ctx.triggered[0]['prop_id'].split('.')[0]
    name,host=GetName(ID)
    print(trigger)
    if trigger=='Deposit':
        if ID is None or len(str(ID))!=3 or name==0:
            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,"FAIL: Please Enter Valid Account"
        if Amount is None:
            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,"FAIL: Please Enter Valid Amount"
        transact(ID,Amount,Notes)
        origAmount=Amount
        Amount=None
    if trigger=='Withdraw':
        if ID is None or len(str(ID))!=3 or name==0:
            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,"FAIL: Please Enter Valid Account"
        if Amount is None:
            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,"FAIL: Please Enter Valid Amount"
        bal,ip=GetBalance(ID)
        if Amount>bal:
            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,"FAIL: Insufficient Balance"
        transact(ID,-Amount,Notes)
        origAmount=Amount
        Amount=None
    if ID is None or len(str(ID))!=3:
        return ["Please Enter Valid Account"],[],None,[],[],False,""
    name,host=GetName(ID)
    if name==0:
        return ["Please Enter Valid Account"],[],None,[],[],False,""
    
    
    bal,ip=GetBalance(ID)
    if name==host:
        host=""
    else:
        host="Guest of "+host
    trans=GetTransactions(ID)
    if trigger=='Deposit':
        return ["Balance: "+str(bal)+"("+str(ip)+")"],[],Amount,[name],[host],True,"SUCCESS: "+name+" deposited $"+str(origAmount)
    if trigger=='Withdraw':
        return ["Balance: "+str(bal)+"("+str(ip)+")"],[],Amount,[name],[host],True,"SUCCESS: "+name+" withdrew $"+str(origAmount)
    return ["Balance: "+str(bal)+"("+str(ip)+")"],[],Amount,[name],[host],False,""

Change=html.Div([
    dcc.ConfirmDialog(
        id='confirm-change',
        message='',
    ),
            html.Div([html.Img(src=CarOfferLogo, height="80px",style={'width':'600px','height':'100px',"margin":"64px 50px 50px 30px"})],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([
                dcc.Dropdown(id="changeplayer",className="caroffer",placeholder='player',style={'font-size':'25px','width':'300px','height':'86px','margin':'12px','backgroundColor':"#000",'color':"#fff",}),
                dcc.Dropdown(id="changehost",className="caroffer",placeholder='host',style={'font-size':'25px','width':'300px','height':'86px','margin':'12px','backgroundColor':"#000",'color':"#fff",}),
                         
                ],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
            html.Div([
                        html.Div(["Current ID:",html.Span(id="changeaccount")],style={"width":"450px",'font-size':'36px','font-weight':'bold','padding':'15px 0px',"margin-left":"24px","color":"#fff",'height':'86px'}),
                        html.Div(["Balance:"],id="changebalance",style={'width':'600px','font-size':'36px','font-weight':'bold','padding':'15px 0px',"margin-left":"24px","color":"#fff",'height':'86px'})
                ],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"}),
                html.Div([
                    dcc.Input(id="newaccount",autoFocus=True,required=True ,minLength=3,maxLength=3,className="caroffer",type='number',placeholder='Acct Num',style={'font-size':'42px','width':'300px','height':'86px','margin':'12px','backgroundColor':"#000",'color':"#fff",}),
                    dbc.Button(
                        "change",
                        id="change",
                        style={'font-size':'42px','width':'250px','height':'86px','margin':'12px','backgroundColor':"#177DDC",'color':"#fff",'borderColor':"#177DDC"}
                            )
                        ],id="wrapper",style={'width':'900px',"justify-content": "space-around","flex-direction": "row","display": "flex","margin-bottom":"48px","margin":"auto"})
                    ])


def change(current,new):
    data=cache.get(str(current))
    if data is None:
        data=[{"Time":None,"Transaction":1000,"Notes":"Initial Deposit"}]
    Players=pd.read_csv("Players.csv")
    Players["Account"][Players["Account"]==current]=new
    Players.to_csv("Players.csv",index=False)
    cache.set(str(new),data)

@app.callback(
    Output(component_id='changeplayer', component_property='options'), # or is there a different one for table
    [Input('url', 'pathname')],) 
def UpdateProp(player):
    data=pd.read_csv("Players.csv")
    names=sorted(list(set(data["Name"])))
    return [{"label":i,"value":i} for i in names]



@app.callback(
    Output(component_id='changehost', component_property='options'), # or is there a different one for table
    [Input(component_id='changeplayer', component_property='value')],) 
def UpdateHrop(player):
    data=pd.read_csv("Players.csv")
    if player is not None:
        data=data[data["Name"]==player]
    names=sorted(list(set(data["Employee"])))
    return [{"label":i,"value":i} for i in names]
@app.callback(
    [
     Output(component_id='changeaccount', component_property='children'),
     Output('confirm-change', 'displayed'),
     Output('confirm-change', 'message')], # or is there a different one for table
    [Input(component_id='changehost', component_property='value'),
     Input(component_id='changeplayer', component_property='value'),
     Input(component_id='change', component_property='n_clicks')],
     [State(component_id='changeaccount', component_property='children'),
     State(component_id='newaccount', component_property='value')]) 
def UpdateDrop (host,player,click,current,new):
    
    ctx = dash.callback_context
    trigger=ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger=='change':
        current=current[0]
        print(current)
        if len(str(current))!=3:
            return dash.no_update,True,"Current Player/ID is not specified"
        if len(str(new))!=3:
            return dash.no_update,True,"New ID is not Valid"
        data=pd.read_csv("Players.csv")
        if new in list(data["Account"]):
            return dash.no_update,True,"New ID is already assigned to another player"
        change(current,new)  
    data=pd.read_csv("Players.csv")
    if player is not None:
        data=data[(data["Name"]==player)].reset_index(drop=True)
    if host is not None:
        data=data[(data["Employee"]==host)].reset_index(drop=True)
    if trigger=='change':    
        return [data["Account"][0]],True,player+" has been changed from ID "+str(current)+" to ID "+str(new)
    if len(data)>1:
        return ["please give more detail"],False,""
    if len(data)==0:
        return ["no account"],False,""
    return [data["Account"][0]],False,""

@app.callback(
    [
     Output(component_id='changebalance', component_property='children')], # or is there a different one for table
    [Input(component_id='changeaccount', component_property='children')],) 
def UpdateDrop (ID):
    
    if ID is None or len(str(ID[0]))!=3:
        return ["Please Enter Valid Account"]
    bal,ip=GetBalance(ID[0])
    return ["Balance: "+str(bal)+"("+str(ip)+")"]

@app.callback(
    [Output(component_id='Leaderboard', component_property='children')], # or is there a different one for table
    [Input(component_id='int', component_property='n_intervals'),
    Input(component_id='leadersearch', component_property='value')])
    
def Leader (Int,search):
    print("tRY",Int)
    leaderboard=pd.read_csv('Players.csv')
    leaderboard["Balance"]=0
    leaderboard["InPlay"]=0
    for i in range(len(leaderboard)):
        bal,ip=GetBalance(str(leaderboard["Account"].iloc[i]))
        leaderboard["Balance"].iloc[i]=bal
        leaderboard["InPlay"].iloc[i]=bal
    leaderboard=leaderboard.groupby(["Employee"],as_index=False).agg({"Balance":"sum"})
    leaderboard=leaderboard.sort_values("Balance",ascending=False)
    leaderboard["rank"]=[i+1 for i in range(len(leaderboard))]
    leaderboard["employee"]=leaderboard["Employee"].str.lower()
    if search is not None:
        leaderboard=leaderboard[leaderboard["employee"].str.contains(search.lower())].reset_index(drop=True)
    led=[]
    led+=[html.Div("Rank",style={"padding":"5px 0px","width":"auto"},className="one-edge-shadow"),
        html.Div([],className="one-edge-shadow"),
        html.Div(str("Name"),style={"padding":"5px 0px"},className="one-edge-shadow"),
        html.Div("$"+str("Balance"),style={"padding":"5px 0px"},className="one-edge-shadow")]
    num=len(leaderboard) if len(leaderboard)<10 else 10
    for i in range(0,num):
        led+=[html.Div("#"+str(leaderboard["rank"].iloc[i]),style={"padding":"5px 0px","width":"auto"},className="one-edge-shadow"),
        html.Div(html.Img(src=pCarOfferLogo,style={"color":"white","height":"80px","width":"80px"} ),className="one-edge-shadow"),
        html.Div(str(leaderboard["Employee"].iloc[i]),style={"padding":"5px 0px"},className="one-edge-shadow"),
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