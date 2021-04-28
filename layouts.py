'''
Created on Jun 24, 2020

@author: Carlo
'''
import dash
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
from flask import send_from_directory
import os
import dash_html_components as html
import pandas as pd
import numpy as np
import json
import datetime
import time
import pandas as pd
from App import app
import IdConverterMFL
import base64
import dash_table
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
import ConfigF as Conf


ImagePath=os.path.join(THIS_FOLDER,'data/analytics logo.jpg')
Image=base64.b64encode(open(ImagePath,'rb').read()).decode('ascii')
Logo='data:image/jpg;base64,{}'.format(Image)

GameLogs= pd.read_csv(os.path.join(THIS_FOLDER,"data/GameLogs.csv"))

MFLPlayers=IdConverterMFL.id_converter()

AllPlayers=MFLPlayers.Get_Players()
excludepositions=[", Coach",", PK",", TM",", Off",", Def",", KR",", PN",", ST"]
for pos in excludepositions:
    AllPlayers=[p for p in AllPlayers if pos not in p]
AllPlayers=sorted(AllPlayers)
Players1=set(GameLogs['Rk'])
Players1=list(Players1)
Players1=sorted(Players1)

AllPicks=[str(i)+"." + str(n).zfill(2) for i in range(1,35) for n in range(1,13,1)]+["2022 Round " + str(n) for n in range(1,5,1)]+["2021 Round " + str(n) for n in range(1,5,1)]

Seasons=set(GameLogs['season'])
Seasons=list(Seasons)
Seasons=sorted(Seasons)

Weeks=set(GameLogs['Week'])
Weeks=list(Weeks)
Weeks=sorted(Weeks)

SeasonWeeks=GameLogs['SeasonWeek']
SeasonWeeks=set(SeasonWeeks)
SeasonWeeks=list(SeasonWeeks)
SeasonWeeks=sorted(SeasonWeeks)
GameLogs.columns=['Unnamed: 0', 'Rk', 'Player', 'Pos', 'Age', 'Date', 'Lg', 'Tm',
       'HomeAway', 'Opp', 'Result', 'G#', 'Week', 'Day', 'Completions',
       'Pass Attempts', 'Completion%', 'Pass Yds', 'Pass TDs', 'Interceptions',
       'Pass TD Rate', 'Sacks', 'Yds Lost to Sack', 'Yds lost/Sack',
       'Adj Yds lost/Sack', 'Carries', 'Rush Yds', 'Yds/Carry', 'Rush TDs',
       'Targets', 'Receptions', 'Receive Yds', 'Yds/Rec', 'Receive TDs',
       'Catch%', 'Yards per Target', 'Std Pts', 'PPR Points', 'DKPts', 'FDPts',
       'Fumbles', 'Fumbles Lost', 'Forced Fumbles', 'Fumbles Recovered',
       'Fum Rec Yds', 'Fum Rec TDs', 'season', 'SeasonWeek']
GameLogs['HomeAway']=GameLogs['HomeAway'].fillna('H')
GameLogs['Opportunities']=GameLogs['Targets']+GameLogs['Carries']
Stats=GameLogs.columns[14:]



QB =pd.read_csv(os.path.join(THIS_FOLDER,"data/All.csv"),parse_dates=['Date'])
QB['Date'] =QB['Date'].fillna(0)
QB['Date'] = QB['Date'].astype(float)
QB['Date'] = pd.to_datetime(QB['Date'].astype(int), unit='s')
QB['Date'] = QB['Date'].dt.date


Players=QB[(QB.DraftType!="SAME")]
Players["rank"] = Players.groupby(["league_id"])["Overall"].rank("average")
Players = Players.sort_values(['rank'])
Players.drop_duplicates(subset ="Player",
                     keep = 'first', inplace = True)
Players=Players['Player'].map(str)
Players=list(Players)

Dates=set(QB['Date'])
Dates=list(Dates)
Dates=sorted(Dates)
DraftTypes=["Overall","Positional"]

STYLE = {
    'boxShadow': '#313131' ,
    'background': '#313131' ,
    'color':'#a5d4d9',
    'backgroundColor': '#313131',
    'margin':'3px'
}

HeaderSTYLE = {
    'boxShadow': '#313131' ,
    'background': '#313131' ,
    'color':'#a5d4d9',
    'backgroundColor': '#313131',
    'font-weight': '600',
    'text-decoration': 'underline'
}

page = {
    'margins': '15px' ,
}


NavbarRDP=dbc.Navbar(
    children=[html.A(dbc.Row(
                [
                    dbc.Col(html.Img(src=Logo, height="90px"))
                ],
                align="left",
                no_gutters=True,
            )),
        html.H2("Real Draft Position")
        #dbc.NavItem(dbc.NavLink("Welcome", href="/Home")),
        #dbc.NavItem(dbc.NavLink("MFL Draft Helper", href="/DraftHelper")),
        #dbc.NavItem(dbc.NavLink("RDP Graph", href="/RDPGraph")),
        #dbc.NavItem(dbc.NavLink("RDP Table", href="/RDPTable")),
        #dbc.NavItem(dbc.NavLink("Floor-Ceiling Graphs", href="/FloorCeilingGraphs"))
    ],
    style={'text':{'color':'#313131 !important'},'color':'#313131 !important'},
    color="primary",
    dark=True,
)
NavbarTrades=dbc.Navbar(
    children=[html.A(dbc.Row(
                [
                    dbc.Col(html.Img(src=Logo, height="90px"))
                ],
                align="left",
                no_gutters=True,
            )),
        html.H2("AOD Trade Database"),
        
        #dbc.NavItem(dbc.NavLink("Welcome", href="/Home")),
        #dbc.NavItem(dbc.NavLink("MFL Draft Helper", href="/DraftHelper")),
        #dbc.NavItem(dbc.NavLink("RDP Graph", href="/RDPGraph")),
        #dbc.NavItem(dbc.NavLink("RDP Table", href="/RDPTable")),
        #dbc.NavItem(dbc.NavLink("Floor-Ceiling Graphs", href="/FloorCeilingGraphs"))
    ],
    style={'text':{'color':'#313131 !important'},'color':'#313131 !important'},
    color="primary",
    dark=True,
)


NavbarAdmin=dbc.Navbar(
    children=[html.A(dbc.Row(
                [
                    dbc.Col(html.Img(src=Logo, height="90px"))
                ],
                align="left",
                no_gutters=True,
            )),
        html.H2("AOD Draft Selection Portal"),
    ],
    style={'text':{'color':'#313131 !important'},'color':'#313131 !important'},
    color="primary",
    dark=True,
)






playercard1 = dbc.Card(
    [html.Div([
    dbc.FormGroup(
        [
        dbc.Label("Pick as Statistic",width=6,style=STYLE),
        dbc.Col(
            dcc.Dropdown(
                    id='Stat',
                    options=[{'label': i, 'value':i} for i in Stats],
                    value="PPR Points",
                    clearable=True
                    ),
            width=6,
            )
            ],
        row=True
    ),
    dbc.Row(
        [
        dbc.Label("Player",width=6,style=STYLE),
        dbc.Label("Start Date",width=2,style=STYLE),
        dbc.Label("End Date",width=2,style=STYLE),
        dbc.Label("Split",width=2,style=STYLE)
            ]
    ),
    dbc.Row(
        [
        dbc.Col(
            dcc.Dropdown(
                    id='input1',
                    options=[{'label': i, 'value':i} for i in Players1],
                    value="search",
                    searchable=True,
                    clearable=True
                    ),
            width=6
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='startdate',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value="2019-01",
                    searchable=True
                    ),
            width=2
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='enddate',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value=max(SeasonWeeks),
                    searchable=True
                    ),
            width=2
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='split',
                    options=[{'label': 'Home', 'value':'H'},
                             {'label': 'Away', 'value':'@'},
                             {'label': 'All', 'value':'All'}],
                    value='All',
                    searchable=True,
                    ),
            width=2
            )
            ],
        no_gutters=True
    ),
    dbc.Row(
        [
        dbc.Col(
            dcc.Dropdown(
                    id='input2',
                    options=[{'label': i, 'value':i} for i in Players1],
                    value="search",
                    searchable=True,
                    clearable=True
                    ),
            width=6
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='startdate2',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value="2019-01",
                    searchable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='enddate2',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value=max(SeasonWeeks),
                    searchable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='split2',
                    options=[{'label': 'Home', 'value':'H'},
                             {'label': 'Away', 'value':'@'},
                             {'label': 'All', 'value':'All'}],
                    value='All',
                    searchable=True
                    ),
            width=2
            )
            ],
        no_gutters=True
    ),

    dbc.Row(
        [
        dbc.Col(
            dcc.Dropdown(
                    id='input3',
                    options=[{'label': i, 'value':i} for i in Players1],
                    value="search",
                    searchable=True,
                    clearable=True
                    ),
            width=6
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='startdate3',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value="2019-01",
                    searchable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='enddate3',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value=max(SeasonWeeks),
                    searchable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='split3',
                    options=[{'label': 'Home', 'value':'H'},
                             {'label': 'Away', 'value':'@'},
                             {'label': 'All', 'value':'All'}],
                    value='All',
                    searchable=True
                    ),
            width=2
            )
            ],
        no_gutters=True
    ),
    dbc.Row(
        [
        dbc.Col(
            dcc.Dropdown(
                    id='input4',
                    options=[{'label': i, 'value':i} for i in Players1],
                    value="search",
                    searchable=True,
                    clearable=True
                    ),
            width=6
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='startdate4',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value="2019-01",
                    searchable=True,
                    clearable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='enddate4',
                    options=[{'label': i, 'value':i} for i in SeasonWeeks],
                    value=max(SeasonWeeks),
                    searchable=True,
                    clearable=True
                    ),
            width={"size": 2, "offset": 0}
            ),
        dbc.Col(
            dcc.Dropdown(
                    id='split4',
                    options=[{'label': 'Home', 'value':'H'},
                             {'label': 'Away', 'value':'@'},
                             {'label': 'All', 'value':'All'}],
                    value='All',
                    searchable=True
                    ),
            width=2
            )
            ],
        no_gutters=True
    )],className="dash-bootstrap")
    ],
    body=True,
)



pickcard =dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    dbc.Label("No. of Teams",style=STYLE),
                        ],width=6
                    ),
                    dbc.Col(
                        [
                    dbc.Label("Custom Pick",style=STYLE),
                        ],width=6
                    ),

                ],
                no_gutters=True
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='teams',
                                        options=[{'label': i, 'value':i} for i in [8,10,12,14,16]],
                                        value=12,
                                        searchable=True,
                                        clearable=False
                                    )
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='pick',
                                        value=10,
                                        searchable=True,
                                        clearable=False)
                        ],
                        width=6
                    )
                ],
                no_gutters=True
            )
        ],
        className="dash-bootstrap"),
    ]
)

draftcard =dbc.Card(
    [
        html.Div(
        [
        dbc.Label("Remove Already Drafted Players?",style=STYLE),
        dcc.Dropdown(id='drafted',
                    options=[
                        {'label': 'Yes', 'value': "Yes"},
                        {'label': 'No', 'value': "No"}
                    ],
                    value="Yes",
                    searchable=False,
                    clearable=False
                    ),
            ],
            className="dash-bootstrap"),
        ])

leaguecard =dbc.Card(
    [
        html.Div(
            [
                dbc.Label("MFL League ID",style=STYLE),
                dcc.Input(id="LeagueId", type="text",placeholder="Enter League ID"),
             ],
             className="dash-bootstrap"),
        ])

franchisecard = dbc.Card(
    [
        html.Div(
        [
            dbc.Label("Choose Your Franchise",style=STYLE),
             dcc.Dropdown(
                id='franchise',
                    searchable=True,
                    clearable=False,
                    value="Enter a valid league First"
                ) ,
             ],
             className="dash-bootstrap"),
        ])

datecard = dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    html.Div(id='SampleCount'),
                        ],width={'offset':4}
                    ),

                ],
                no_gutters=True
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='startdate',
                                        options=[{'label': i, 'value':i} for i in Dates],
                                        value=max(Dates)-datetime.timedelta(30),
                                        searchable=True,
                                        clearable=False
                                    )
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='enddate',
                                        options=[{'label': i, 'value':i} for i in Dates],
                                        value=max(Dates),
                                        searchable=True,
                                        clearable=False)
                        ],
                        width=6
                    )
                ],
                no_gutters=True
            )
        ],
        className="dash-bootstrap"),
    ]
)

filtercard = dbc.Card(
    [
    html.Div(
        [

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("DraftType",style=STYLE),width=1
                    ),
                    dbc.Col(
                        dbc.Label("Position",style=STYLE),width=5
                    ),
                    dbc.Col(
                        dbc.Label("ADP Range",style=STYLE),width=4
                    ),


                ],
                no_gutters=True
            ),
            dbc.Row(
                [   
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='DraftType',
                                        options=[{'label': i, 'value':i} for i in ['StartUp','Rookie']],
                                        value='StartUp',
                                        searchable=True,
                                        clearable=False
                                    )
                        ],
                        width=1
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='position',
                                        options=[{'label': i, 'value':i} for i in ['All','QB',"RB","WR","TE","Pick"]],
                                        value='All',
                                        searchable=True,
                                        clearable=False
                                    )
                        ],
                        width=1
                    ),
                    dbc.Col(
                        [
                            dcc.RangeSlider(
                                id='ADP',
                                min=0,
                                max=400,
                                step=1,
                                value=[0, 400],
                                marks={i: '{}'.format('R'+str(int(i/12))) for i in range(12,400,12)}
                            )
                        ],
                        width=10
                    )

                ],
                no_gutters=True
            )
        ],
        className="dash-bootstrap"),
    ]
)



tradecard = dbc.Card(
    [
    html.Div(id="wrapper",children=
        [dbc.Modal(
            [
                dbc.ModalHeader("Most Traded Players",style={"backgroundColor":"#4a4a4a","color":"#fff"}),
                dcc.Dropdown(
                        id='TimePeriod',
                        options=[{'label': i, 'value':i} for i in ["7Days","14Days","30Days"]],
                        value="30Days",
                        clearable=False,
                        className="dash-bootstrap"
                    ),
                dcc.Loading(dbc.ModalBody(id="StatsDisplay",children=[html.Div(id="MostTraded")],
                    style={"backgroundColor":"#4a4a4a","color":"#fff"}),type='circle'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="CloseModal",color='dark'),style={"backgroundColor":"#4a4a4a","color":"#fff"}
                ),
            ],
        id="TradeModal",
        is_open=False,
        style={"max-width": "none", "width": "60%","backgroundColor":"#fff","color":"#fff"}
        ),
        dbc.Row([dbc.Label("Player",style=HeaderSTYLE)]),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                                    id='tradeplayer',
                                    options=[{'label': i, 'value':i} for i in AllPlayers+AllPicks],
                                    value=None,
                                    searchable=True,
                                    clearable=True,
                                    multi=True,
                                    className="dash-bootstrap"
                                ),width=10),
                dbc.Col(
                    [dbc.Button(
                            "Most Traded",
                            id="OpenModal",
                            color='dark',
                        ),
                    ],
                    width=2
                )
                
            ],
            no_gutters=True
        ),
        html.Br(),
        dbc.Row([dbc.Label("Starter Format",style=HeaderSTYLE)]),
        dbc.Row(
            [
                dbc.Label("QBs:  ",style=STYLE),
                dbc.Col(
                    dbc.RadioItems(id="QBs",
                        options=[{'label': i, 'value':i} for i in ["Any","1QB","SuperFlex","2QB"]],
                        inline=True,
                        value="Any",
                        style={'color':'#000 !important'},
                        inputStyle={"color": "#ccff00"}
                        ),
                    width=2
                ),
                dbc.Label("WRs:  ",style=STYLE),
                dbc.Col(
                    dbc.RadioItems(id="WRs",
                            options=[{'label': i, 'value':i} for i in ["Any","2WR","3WR"]],
                            inline=True,
                            value="Any",
                            style={'color':'#000 !important'},
                            inputStyle={"color": "#ccff00"}
                        ),
                    width=2
                ),
                dbc.Label("TEs:  ",style=STYLE),
                dbc.Col(
                    dbc.RadioItems(id="TEs",
                            options=[{'label': i, 'value':i} for i in ["Any","1TE","2TE"]],
                            inline=True,
                            value="Any",
                            style={'color':'#000 !important'},
                            inputStyle={"color": "#ccff00"}
                        ),
                    width=2
                )
            ],
            no_gutters=True
        ),
        html.Br(),
        dbc.Row([dbc.Label("Scoring Format",style=HeaderSTYLE)]),
        dbc.Row(
            [
                dbc.Label("Pass TD:  ",style=STYLE),
                dbc.Col(
                    dbc.RadioItems(id="PassTD",
                            options=[{'label': i, 'value':i} for i in ["Any","4pt","6pt"]],
                            inline=True,
                            value="Any",
                            style={'color':'#000 !important'},
                            inputStyle={"color": "#ccff00"}
                        ),
                    width=2
                ),
                dbc.Label("TE Premium:  ",style=STYLE),
                dbc.Col(
                    dbc.RadioItems(id="TEPrem",
                            options=[{'label': i, 'value':i} for i in ["Any","Yes","No"]],
                            inline=True,
                            value="Any",
                            style={'color':'#000 !important'},
                            inputStyle={"color": "#ccff00"}
                        ),
                    width=2
                ),
            ],
            no_gutters=True
        ),
    ],
    className="dash-bootstrap"
    ),
],style={"padding":"20px","width":"95%"})




playercard = dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    dbc.Label("Players",style=STYLE),
                        ],width={"size": 3, "offset": 5},
                    )
                ]
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Dropdown(
                            id='input1',
                            options=[{'label': i, 'value':i} for i in Players],
                            value="search",
                            searchable=True,
                            clearable=True
                            )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='input2',
                                        options=[{'label': i, 'value':i} for i in Players],
                                        value="search",
                                        searchable=True,
                                        clearable=True
                                    )
                        ],
                        width=2
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='input3',
                                        options=[{'label': i, 'value':i} for i in Players],
                                        value="search",
                                        searchable=True,
                                        clearable=True
                                    )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='input4',
                                        options=[{'label': i, 'value':i} for i in Players],
                                        value="search",
                                        searchable=True,
                                        clearable=True
                                    )
                        ],
                        width=3
                    ),
                ],
                no_gutters=True
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                           daq.BooleanSwitch(
                                            on=True,
                                            id='confswitch1',
                                            color='#a5d4d9'
                                        )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.BooleanSwitch(
                                            on=True,
                                            id='confswitch2',
                                            color='#a5d4d9'
                                        )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.BooleanSwitch(
                                            on=True,
                                            id='confswitch3',
                                            color='#a5d4d9'
                                        )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.BooleanSwitch(
                                            on=True,
                                            id='confswitch4',
                                            color='#a5d4d9'
                                        )
                        ],
                        width=3
                    ),
                ],
                no_gutters=True
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                           daq.Knob(
                                        min=60,
                                        max=90,
                                        value=80,
                                        size=50,
                                        label={'label': 'Confidence Interval'},
                                        scale={'custom': {60:'60%',70:'70%',80:'80%',90:'90%'}},
                                        id='knob1'
                            ),
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.Knob(
                                        min=60,
                                        max=90,
                                        value=80,
                                        size=50,
                                        label={'label': 'Confidence Interval'},
                                        scale={'custom': {60:'60%',70:'70%',80:'80%',90:'90%'}},
                                        id='knob2'
                            ),
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.Knob(
                                        min=60,
                                        max=90,
                                        value=80,
                                        size=50,
                                        label={'label': 'Confidence Interval','style':{'margin':0}},
                                        scale={'custom': {60:'60%',70:'70%',80:'80%',90:'90%'}},
                                        id='knob3'
                            ),
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            daq.Knob(
                                        min=60,
                                        max=90,
                                        value=80,
                                        size=50,
                                        label={'label': 'Confidence Interval'},
                                        scale={'custom': {60:'60%',70:'70%',80:'80%',90:'90%'}},
                                        id='knob4'
                            ),
                        ],
                        width=3
                    ),
                ],
                no_gutters=True
            )
        ],
        className="dash-bootstrap"
        ),
    ]
)

typecard = dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    dbc.Label("Pick ADP Type",style=STYLE),
                        ],width={'offset':4},
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id='Type',
                                options=[
                                    {'label': 'Overall', 'value': 'Overall'},
                                    {'label': 'Positional', 'value': 'posrank'}
                                ],
                                value='Overall',
                                searchable=False,
                                clearable=False
                            )
                        ],
                    )
                ],
            ),
        ],
        className="dash-bootstrap"),
    ]
)
windowcard = dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    dbc.Label("Pick Rolling Window for Confidence Intervals",style=STYLE),
                        ],width={'offset':1},
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id='window',
                                options=[
                                    {'label': '10 Days', 'value': 10},
                                    {'label': '30 days', 'value': 30},
                                    {'label': '60 Days', 'value': 60},
                                    {'label': '90 days', 'value': 90}
                                ],
                                value=30,
                                searchable=False,
                                clearable=False
                            )
                        ],
                    )
                ],
            ),
        ],
        className="dash-bootstrap"),
    ]
)
datecard2 = dbc.Card(
    [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                    dbc.Label("Start-End Date",style=STYLE),
                        ],width={'offset':4}
                    ),

                ],
                no_gutters=True
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='startdate',
                                        options=[{'label': i, 'value':i} for i in Dates],
                                        value='2020-03-20',
                                        searchable=True,
                                        clearable=False
                                    )
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                        id='enddate',
                                        options=[{'label': i, 'value':i} for i in Dates],
                                        value=max(Dates),
                                        searchable=True,
                                        clearable=False)
                        ],
                        width=6
                    )
                ],
                no_gutters=True
            )
        ],
        className="dash-bootstrap"),
    ]
)

DraftHelper=html.Div([
    html.Div(
    children=[
            html.Div(children=[html.Div(
                [
                    dbc.Button(
                        "Instructions",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                    ),
                    dbc.Collapse(
                        html.Div([html.H4("How to use (Currently setup for SF/TE Prem, more league types on the way!)"),
                      html.H5("Don't have a current MFL draft, but want to see what types of players are available at a certain pick?"),
                      html.P("No need to enter an MFL league ID, just change the custom pick to whichever you want to analyze and the base rate for players availability at that pick will be calculated"),
                      html.H5("Base Rate vs Odds Available"),
                      html.P("Base Rate - reflects the percentage of drafts in the sample in which the player made it to the pick in question. In this sense it's a gauge of value. If you're OTC and a player is a available with a base rate of 20%, that means that the player makes it to this point 20% of the time and is relatively good value"),
                      html.P("Odds Available - changes based on how the draft has gone so far. Example: usually the consensus top four have very low odds of making it to 1.05. However, if someone took Kalen Ballage at 1.01 that would change those odds significantly!"),
                      html.H5("MFL League ID and Franchise"),
                      html.P("Enter the 5-digit league code found in the URL of any of your league's pages, the franchise dropdown box will populate with available teams. Choose your franchise. The Base Rates and Odds Available for your next two picks will be displayed. Don't forget you still have that custom pick in case you are considering trading for a pick you don't have yet and want to see who may be available there."),
                      html.H5("Position and ADP Range"),
                      html.P("These are just filters")
                      ],style={'padding': '30px 30px 30px 30px','color': '#fff'}),
                        id="collapse",
                    ),
                ]
            ),
            dbc.Row(
                    [
                    dbc.Col([draftcard,html.Br(),datecard,pickcard], width=6),
                    dbc.Col([leaguecard,html.Br(),franchisecard], width=6)
                    ],
                align='center'
                ),
            dbc.Row(
                    [
                    dbc.Col(filtercard, width=12)
                    ],
                align='center'
                ),
            html.Br()
            ])
        ],
    ),
    html.Div(
    children=[
        dbc.Row(
            [
            dbc.Col(html.Div([dcc.Loading(
                id="loading-2",
                type="default",
                children=html.Div(id='outputtable')
                )]),
            width=12)
            ]
        )
    ]
    )],style={'padding': '0px 20px 20px 20px'})


RDP_graph=html.Div(
    children=[
        html.Br(),
            dbc.Row(
                    [

                    dbc.Col([typecard,html.Br(),windowcard,html.Br(),datecard2], width=4),
                    dbc.Col(playercard, width=8)
                    ],
                align='center'
                ),
            dbc.Row(
                    [
                    dbc.Col(dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div(id='outputgraph')
                        ),
                    width=12)
                    ],
                no_gutters=True
                ),
            html.Div([html.H3("What Am I Looking At???"),
                      html.H4("Graph"),
                      html.P("The graph shows the trend of their draft position over a specified time range. It shows median draft position from REAL DYNASTY STARTUP DRAFTS"),
                      html.H4("Confidence Interval"),
                      html.P("You'll notice an upper and lower range when you select a player, this is their confidence interval. The default confidence interval is 80% meaning we are 80% confident that the player with be drafted within this interval. This helps visualize the width and skewness of the distribution!"),
                      html.P("This can be removed with the toggle switch under each player and adjusted with the dial."),
                      html.H4("Rolling Window"),
                      html.P("The rolling window sets the lookback period for calculating the mean and confidence intervals. The default is 30 days, so at every date point on the x-axis, the Y-axis values are using all drafts t-minus 30 to calculate the metrics."),
                      html.H4("Overall Vs Positional"),
                      html.P("Want to see trends and confidence intervals on a positional basis? Use the drop down in the top left to switch and see how a player is being valued within their position group!")
                      ],style={'padding': '30px 30px 30px 30px','color': '#fff'})
        ],
    )

RDP_table=html.Div([
    html.Div(
    children=[
        NavbarRDP,
        html.Div(children=[html.Br(),
            dbc.Row(
                    [
                    dbc.Col([datecard], width=12)],
                align='center'
                ),
            dbc.Row(
                    [
                    dbc.Col(filtercard, width=12)
                    ],
                align='center'
                ),
            html.Br()
            ])
        ],
    ),
    html.Div(
    children=[
        dbc.Row(
            [
            dbc.Col(html.Div([dcc.Loading(
                id="loading-3",
                type="default",
                children=html.Div(id='RDPtable')
                )]),
            width=12)
            ]
        )
    ]
    )],style={'padding': '0px 20px 20px 20px'})

FCgraph=html.Div(children=[
    dbc.Container(fluid=True,children=[
        dbc.Row(
                [
                dbc.Col(html.Div(id='FCgraph'), width=12)
                ]
            ),
        dbc.Row(
                [

                dbc.Col(playercard1, md=12)
                ]
            )
        ]),

    ]
)

TradeFinder=html.Div([
    NavbarTrades,
    html.Div(
    children=[tradecard,html.Br(),dcc.Loading(
                id="loading-4",
                type="default",
                children=[html.Div(id='TradeTable')]
                )]
    )],style={'padding': '0px'})


Admin=html.Div([
    NavbarAdmin,
    html.Div(
    children=[html.Br(),
              dbc.Row([
                    dbc.Col([
                      dcc.Upload(
                        id='uploadNewDraftTable',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        }
                        )
                    ],width=2),
                    dbc.Col([
                        dcc.Dropdown(
                                id='Type',
                                options=[{'label': i, 'value':i} for i in Conf.Categories],
                                value="ForReview",
                                clearable=False
                                ),
                    ],width=2),
                    dbc.Col([
                  dbc.Button("Apply Changes",
                            id="ApplyChanges",
                            color='dark')
                  ],width=2),
                ]),
              dcc.Loading(
                type="default",
                children=[html.Div(id='NewDraftTable',
                                   children=[dash_table.DataTable(id='ChangeTable')])]
                )]
    )],style={'padding': '0px'})