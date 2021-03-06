'''
Created on Jun 24, 2020

@author: Carlo
'''
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from App import app,cache
#import ADPAPP
#import DraftApp
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
import dash_daq as daq
import base64
from CarofferChristmas import  CarOfferContest,CarOfferLeaderBoard,CarOfferTransactions,Change
import time
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ImagePath=os.path.join(THIS_FOLDER,'data/analytics logo.jpg')
Image=base64.b64encode(open(ImagePath,'rb').read()).decode('ascii')
Logo='data:image/jpg;base64,{}'.format(Image)



NavbarSignUp=dbc.Navbar(
    children=[html.A(dbc.Row(
                [
                    dbc.Col(html.Img(src=Logo, height="90px"))
                ],
                align="left",
                
            )),
        html.H2("Sign Up")
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

Join=html.Div([NavbarSignUp,html.Br(),html.P("Not a subscriber?"),
    html.Br(),html.P("Join us! Get access to our live REAL draft data and the entire suite of Analytics of Dynasty offerings. Click the Link Below!"),
    html.Br(),dbc.NavItem(dbc.NavLink("Subscribe to AOD Now", active=True, href="https://analyticsofdynasty.com/register/analytics-of-dynasty-subscription/")),
    dcc.Input(id="loading-input-1", value="Input triggers local spinner"),
    dcc.Loading(
            id="loading-1", type="default", children=html.Div(id="loading-output-1")
        )],style={'padding': '30px 30px 30px 30px','color': '#fff'})

NavbarSignUp=dbc.Navbar(
    children=[html.A(dbc.Row(
                [
                    dbc.Col(html.Img(src=Logo, height="90px"))
                ],
                align="left",
                
            )),
        html.H2("Sign Up")
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



body=html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = html.Div([
    body
])


@app.callback(
    Output("loading-output-1", "children"),
    [Input("loading-input-1", "value")],
    prevent_initial_call=True,
)
def input_triggers_spinner(value):
    time.sleep(4)
    return value


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname.lower() == '/caroffer/contest':
        return CarOfferContest
    elif pathname.lower() == '/caroffer':
        return CarOfferLeaderBoard
    elif pathname.lower() == '/caroffer/transactions':
        return CarOfferTransactions
    elif pathname.lower() == '/caroffer/change':
        return Change
    else:
        return Join

if __name__ == '__main__':
    app.run_server(debug=True)