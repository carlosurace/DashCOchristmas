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

statscolumns = ["Current Year Age","Current Year Pos ADP","Current Year Finish"]

#statscolumns = list(df5.columns[3:20, 27:68]) # columns 26 thru 67, 73-75 3 THRU 20, 27 THRU 68
scaledstatcolumns= ['s' + stat for stat in statscolumns]

min_max_scaler = preprocessing.MinMaxScaler()
scaled = min_max_scaler.fit_transform(ADP[statscolumns])
#rename scaled data columns
x=pd.DataFrame(scaled,columns=scaledstatcolumns) # was scaled stats before
# print(df5[['Player','Season', 'Offensive Role']+statscolumns])
# BBALL.Player = BBALL.Player + ', ' BBALL.School
universe=pd.concat([ADP[['Player','Current Year',"Position","Current Year Finish","Next Year Pos ADP"]+statscolumns],x],axis=1, ignore_index=False)

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
        html.H1(children='ADP Comps'),
        html.Div(id="wrapper",children=[
                dcc.Dropdown(id = 'Stats',
                        options=[
                            {'label': i, 'value': i} for i in statscolumns],
                        multi=True
                        ,value=statscolumns
                        ,className="dash-bootstrap"
                    ),
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
                ]),
        html.Div(id="emptydiv")
                                        ])
    # replace whole dt w/ div and then give an ID (callback sets children of that div to be a dt, return that) (entry should be in call back)

# call back making season unique
@app.callback(
    [Output(component_id='Season', component_property='options'),
     Output(component_id='Season', component_property='value')], # or is there a different one for table
    [Input(component_id='Player', component_property='value')])
    
def UpdateDrop (Player):
    return [{'label': i, 'value': i} for i in sorted(ADP['Current Year'][ADP.Player==Player].unique())],None

# call back that limits model options to requisite make
@app.callback(
    Output(component_id='emptydiv', component_property='children'), # or is there a different one for table
    [#Input(component_id='Player', component_property='value'),
    #Input(component_id='Season', component_property='value'),
    Input(component_id='Stats', component_property='value'),
    Input(component_id='ADPPos', component_property='value'),
    Input(component_id='ADPAge', component_property='value'),
    Input(component_id='ADPCurrent', component_property='value'),
    Input(component_id='ADPFinish', component_property='value')])
    
def dashtable ( stats,Pos,Age,Current,Finish):
    '''
    if  Player and Season and stats:
        bballtrial=universe[universe.columns]
        #Grab Test Player
        PlayerData = bballtrial[(bballtrial['Player']==Player) & (bballtrial['Current Year']==Season)].reset_index(drop=True)
        bballtrial=bballtrial[bballtrial["Position"]==PlayerData["Position"].iloc[0]]
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
    bballtrial=ADP[ADP.columns]
    bballtrial.loc[len(bballtrial)]=["TestPlayer",2021,Age,Current,Pos,Finish,"?"]
    #Grab Test Player
    statscolumns = ["Current Year Age","Current Year Pos ADP","Current Year Finish"]
    #statscolumns = list(df5.columns[3:20, 27:68]) # columns 26 thru 67, 73-75 3 THRU 20, 27 THRU 68
    scaledstatcolumns= ['s' + stat for stat in stats]
    
    min_max_scaler = preprocessing.MinMaxScaler()
    scaled = min_max_scaler.fit_transform(bballtrial[stats])
    #rename scaled data columns
    x=pd.DataFrame(scaled,columns=scaledstatcolumns) # was scaled stats before
    bballtrial=pd.concat([bballtrial[['Player','Current Year',"Position"]+statscolumns+["Next Year Pos ADP"]],x],axis=1, ignore_index=False)
    PlayerData = bballtrial[(bballtrial["Player"]=="TestPlayer") & (bballtrial['Current Year']==2021)].reset_index(drop=True)
    bballtrial=bballtrial[bballtrial["Position"]==PlayerData["Position"].iloc[0]]
    #remove visual columns, leaving only scaled data
    scaledstats = ['s' + stat for stat in stats]
    y=PlayerData[scaledstats].iloc[0].values.reshape(1,-1)
    NEWx=bballtrial[scaledstats]
    arr=NEWx.values # converts from df to array 
    print(PlayerData)
    bballtrial["Euc"]=euclidean_distances(y,arr)[0] #assign list of euclidean distances to a new column, list must be exactly the same length as the df
    bballtrial=bballtrial.sort_values("Euc").reset_index(drop=True)
    bballtrial = bballtrial.iloc[0:10]
    bballtrial=bballtrial[['Player','Current Year',"Position"]+statscolumns+["Next Year Pos ADP"]]
    arr=NEWx.values 
    # print(len(bballtrial))
    return [dt.DataTable(
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
    style_table={'minHeight':'auto','height': 'auto','maxHeight':'auto','border': '#000','height': '650px',"width":"95%"},
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
    ),html.H1(bballtrial["Next Year Pos ADP"][bballtrial["Player"]!="TestPlayer"].mean())]