'''
Created on Jul 22, 2021

@author: Carlo Surace
'''
from App import  app
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import dash_bootstrap_components as dbc
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import time 

from numpy import argmax
from numpy import array
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sphinx.writers.texinfo import smart_capwords
from multiprocessing.connection import answer_challenge
import pickle
from sklearn.metrics.pairwise import euclidean_distances

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

#reset print options for debugging
pd.set_option("display.max_columns", 100) 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#load data
ADP= pd.read_csv(os.path.join(THIS_FOLDER,"data/ADP.csv"))

statscolumns = [col for col in ADP.columns]


# dash lay out


'''
    dcc.Dropdown(id = 'Player',value=None
            ,options=[
                {'label': i, 'value': i} for i in sorted(ADP.Player.unique())],
            multi=False,
            className="dash-bootstrap"
        ),
    dcc.Dropdown(id = 'Season',value=None
            ,options=[
                {'label': i, 'value': i} for i in sorted(ADP['Current Year'].unique())],
            multi=False,
            className="dash-bootstrap"
        ),
'''
   
ADPComps =html.Div([
        html.H1(children='AOD Comparison Engine'),
        html.Div(id="wrapper",children=[
        dbc.Row([
            dbc.Col([dbc.Label("Player")],width=1),
        
                dbc.Col([dcc.Dropdown(id = 'Player',value=None
                        ,options=[
                            {'label': i, 'value': i} for i in sorted(ADP.Player.unique())],
                        multi=False
                        ,className="dash-bootstrap"
                    )],width=11),
        ]),
        dbc.Row([
            dbc.Col([dbc.Label("Year(Y1)")],width=1),
                dbc.Col([dcc.Dropdown(id = 'Season',value=None
                        ,options=[
                            {'label': i, 'value': i} for i in sorted(ADP.Year.unique())],
                        multi=False
                        ,className="dash-bootstrap"
                    )],width=11),
        ]),
        dbc.Row([
            dbc.Col([dbc.Label("Comparison Stats")],width=1),
                dbc.Col([dcc.Dropdown(id = 'CompStats',
                        options=[
                            {'label': i, 'value': i} for i in statscolumns],
                        multi=True
                        ,value=["POS.ADP","Y1 Finish"]
                        ,className="dash-bootstrap"
                    )],width=11),
        ]),
        dbc.Row([
            dbc.Col([dbc.Label("Analyze Stats")],width=1),
                dbc.Col([dcc.Dropdown(id = 'DispStats',
                        options=[
                            {'label': i, 'value': i} for i in statscolumns],
                        multi=True
                        ,value=["POS ADP Y2"]
                        ,className="dash-bootstrap"
                    )],width=11),
        ])
                
                ]),
        html.Div(id="emptydiv")
                                        ])

'''
html.Div(id="wrapper",children=[dbc.Row([
                    dbc.Label("Pos:"),
                    dbc.Col([
                    dcc.Dropdown(id = 'ADPPos',
                        options=[
                            {'label': i, 'value': i} for i in ["QB","RB","WR","TE"]]
                        ,value="RB"
                        ,clearable=False
                        ,className="dash-bootstrap"
                    )],width=1),
                    dbc.Label("Age:"),
                    dcc.Input(id="ADPAge",
                       debounce=True,
                       type="number",
                       value=23),
                    dbc.Label("PosADP:"),
                    dcc.Input(id="ADPCurrent",
                       debounce=True,
                       type="number",
                       value=12),
                    dbc.Label("PosFinish:"),
                    dcc.Input(id="ADPFinish",
                       debounce=True,
                       type="number",
                       value=12)
                    ])])
'''
    # replace whole dt w/ div and then give an ID (callback sets children of that div to be a dt, return that) (entry should be in call back)

# call back making season unique
@app.callback(
    [Output(component_id='Season', component_property='options'),
     Output(component_id='Season', component_property='value')], # or is there a different one for table
    [Input(component_id='Player', component_property='value')],
    [State(component_id='Season', component_property='value')])
    
def UpdateDrop (Player,Season):
    opts=sorted(ADP['Year'][ADP.Player==Player].unique())
    if Season in opts:
        return [{'label': i, 'value': i} for i in opts],Season
    else:
        return [{'label': i, 'value': i} for i in opts],None

# call back that limits model options to requisite make
@app.callback(
    Output(component_id='emptydiv', component_property='children'), # or is there a different one for table
    [Input(component_id='Player', component_property='value'),
    Input(component_id='Season', component_property='value'),
    Input(component_id='CompStats', component_property='value'),
    Input(component_id='DispStats', component_property='value'),    
    ])
    
def dashtable ( Player,Season,stats,dispstats):
    '''
    if  Player and Season and stats:
        bballtrial=universe[universe.columns]
        #Grab Test Player
        PlayerData = bballtrial[(bballtrial['Player']==Player) & (bballtrial['Current Year']==Season)].reset_index(drop=True)
        bballtrial=bballtrial[bballtrial["POS"]==PlayerData["POS"].iloc[0]]
        #remove visual columns, leaving only scaled data
        scaledstats = ['s' + stat for stat in stats]
        y=PlayerData[scaledstats].iloc[0].values.reshape(1,-1)
        NEWx=bballtrial[scaledstats]
        arr=NEWx.values # converts from df to array 
        bballtrial["Euc"]=euclidean_distances(y,arr)[0] #assign list of euclidean distances to a new column, list must be exactly the same length as the df
        bballtrial=bballtrial.sort_values("Euc").reset_index(drop=True)
        bballtrial = bballtrial.iloc[0:10]
        bballtrial=bballtrial[['Player','Current Year','Position']+stats+["Current Year Finish","Next Year Pos ADP"]]
        arr=NEWx.values 
        # print(len(bballtrial))
        return dt.DataTable(
        id='Euc return table',
        columns=[{"name": i, "id": i} for i in bballtrial.columns],
        data=bballtrial.to_dict('records'),
    )
    else:
    '''
    if  Player and Season and stats:
        bballtrial=ADP[ADP.columns]
        #statscolumns = list(df5.columns[3:20, 27:68]) # columns 26 thru 67, 73-75 3 THRU 20, 27 THRU 68
        scaledstats= ['s' + stat for stat in stats]
        
        min_max_scaler = preprocessing.MinMaxScaler()
        scaled = min_max_scaler.fit_transform(bballtrial[stats])
        #rename scaled data columns
        x=pd.DataFrame(scaled,columns=scaledstats) # was scaled stats before
        bballtrial=pd.concat([bballtrial[['Player','Year',"POS"]+stats+dispstats],x],axis=1, ignore_index=False)
        PlayerData = bballtrial[(bballtrial["Player"]==Player) & (bballtrial['Year']==Season)].reset_index(drop=True)
        bballtrial=bballtrial[bballtrial["POS"]==PlayerData["POS"].iloc[0]]
        #remove visual columns, leaving only scaled data
        y=PlayerData[scaledstats].iloc[0].values.reshape(1,-1)
        bballtrial=bballtrial.dropna(subset=scaledstats+dispstats)
        NEWx=bballtrial[scaledstats]
        arr=NEWx.values # converts from df to array 
        print(PlayerData)
        try:
            bballtrial["Euc"]=euclidean_distances(y,arr)[0] #assign list of euclidean distances to a new column, list must be exactly the same length as the df
            bballtrial=bballtrial.sort_values("Euc").reset_index(drop=True)
            bballtrial=bballtrial[bballtrial["Player"]!=Player]
            bballtrial = bballtrial.iloc[0:10]
            bballtrial=bballtrial[['Player','Year',"POS"]+stats+dispstats]
        except:
            PlayerData=PlayerData[['Player','Year',"POS"]+stats]
            return [dt.DataTable(
                id='Ctable',
                columns=[{"name": i, "id": i} 
                         for i in PlayerData.columns],
                data=PlayerData.to_dict('records'),
                fixed_rows={'headers': True},
                fixed_columns={'headers': True},
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
            }),html.H1("Error, Check that Comparison Stats are present for this Player/Season")]
        
        arr=NEWx.values 
        PlayerData=PlayerData[['Player','Year',"POS"]+stats+dispstats]
        # print(len(bballtrial))
        return [dt.DataTable(
                id='Ctable',
                columns=[{"name": i, "id": i} 
                         for i in PlayerData.columns],
                data=PlayerData.to_dict('records'),
                fixed_rows={'headers': True},
                fixed_columns={'headers': True},
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
        }),
        dt.DataTable(
        id='Euc return table',
        columns=[{"name": i, "id": i} for i in bballtrial.columns],
        data=bballtrial.to_dict('records'),
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
        )]+[html.H1(cstat+": "+str(bballtrial[cstat].mean())) for cstat in dispstats]