'''
Created on Jun 24, 2020

@author: Carlo
'''
from dash.dependencies import Input, Output,State
import datetime
from datetime import date
from App import app,cache
from mfl_services import mfl_service
mfl = mfl_service(update_player_converter=True)
from layouts import QB,QBR, Players, Dates,GameLogs,Stats,Seasons, SeasonWeeks,Players1,AllPlayers
import dash_bootstrap_components as dbc
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import dash_core_components as dcc
import os
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_table.FormatTemplate as FormatTemplate
import dash_html_components as html
import base64
import datetime
import io
import dash
import ConfigF as Conf
import numpy as np
STYLE = {
    'boxShadow': '#313131' ,
    'background': '#313131' ,
    'color':'#a5d4d9',
    'backgroundColor': '#313131'
}
colors =  {
    'background': '#313131',
    'text': '#a5d4d9',
    'accent': '#D46C39'
}

AllDrafts=pd.DataFrame()
for file in [Conf.StartupsPath,Conf.RookiesPath]:
    n=pd.read_csv(file)
    AllDrafts=AllDrafts.append(n)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

TradesRaw=os.path.join(THIS_FOLDER,'data/RulesTrades.csv')
TradesRaw=pd.read_csv(TradesRaw,parse_dates=['Date'])
TradesRaw["Date"]=TradesRaw["Date"].dt.date
TradesRaw=TradesRaw.sort_values("Date",ascending=False).reset_index(drop=True)
TradesRaw=TradesRaw.fillna("")
TradesRaw=TradesRaw[(TradesRaw.Side1!="")&(TradesRaw.Side2!="")&(~TradesRaw.Side1.isna())&(~TradesRaw.Side2.isna())]


def toggle_modal(n1, n2, is_open):
    print("firing Modal Toggle",is_open,"n1",n1,"n2",n2)
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("TradeModal", "is_open"),
    [Input("OpenModal", "n_clicks"), Input("CloseModal", "n_clicks")],
    [State("TradeModal", "is_open")]
    )(toggle_modal)

@app.callback(Output(component_id='pick',component_property='options'),
              [Input("teams", "value")])
def update_pick(teams):
    return [{'label': str(((i-1)//teams)+1)+"."+str((i-1)%teams+1).zfill(2), 'value':i} for i in range(1,200)]
'''
@app.callback(Output(component_id='SampleCount',component_property='children'),
              [Input("startdate", "value"),
               Input("enddate", "value")])
def update_count(startdate,enddate):
    startdate=datetime.date(*(int(s) for s in startdate.split('-')))
    enddate=datetime.date(*(int(s) for s in enddate.split('-')))

    filt=QB[(QB.Date>=startdate)&(QB.Date<=enddate)&(QB.DraftType!="SAME")]
    count=len(set(filt['league_id']))
    return dbc.Label("Set Sample Range: "+str(count)+" Drafts",style=STYLE)
'''
@app.callback(Output(component_id='franchise',component_property='options'),
              [Input("LeagueId", "value")])
def update_drop(LeagueId):
    if LeagueId:
        if len(LeagueId)==5:
            try:
                frandict=mfl.get_rosters(LeagueId,2020)
                draft=mfl.get_ActiveDraft(LeagueId,2020)
                draft=draft.replace({"Franchise":frandict})
                franchises=set(draft["Franchise"])
                franchises=list(franchises)
                franchises=sorted(franchises)
                return [{'label': i, 'value': i} for i in franchises]
            except:
                return({'label':"league not found", 'value': "league not found"})
    return [{'label':"Enter a valid league First", 'value': "Enter a valid league First"}]

@app.callback(
    Output(component_id='outputtable',component_property='children'),
    [Input("startdate", "value"),
     Input("enddate", "value"),Input("drafted", "value"),Input("LeagueId", "value"),
     Input('franchise', "value"),Input('position', "value"),
     Input('pick', "value"),Input('teams', "value")]
    )
def update_Table(startdate,enddate,drafted,
                 LeagueId,franchise,position,pick,teams
                 ):
    print(franchise)
    nextpickP=""
    draft=None
    franchises=[]
    QB["Drafted"]="No"
    headers=["Player","Position","Draft Count","Median Overall","Median Positional"]
    if LeagueId:
        if len(LeagueId)==5:
            try:
                frandict=mfl.get_rosters(LeagueId,2020)
                draft=mfl.get_ActiveDraft(LeagueId,2020)
                draft=draft.replace({"Franchise":frandict})
                currentpick=min(draft["Overall"][(draft.Player=="")])
                currentpickP=min(draft["Pick"][(draft.Player=="")])
                franchises=set(draft["Franchise"])
                already=set(draft["Player"][(draft.Player!="")])
            except:
                return(dbc.Label("draft not found"))
    startdate=datetime.date(*(int(s) for s in startdate.split('-')))
    enddate=datetime.date(*(int(s) for s in enddate.split('-')))



    PosDic={'QB':4,'RB':5,'WR':1,"TE":0}
    #start=start.strftime('%m/%d/%Y')
    df=pd.DataFrame(columns=["Player","Position","Overall","Positional", "Current Probability Overall","Current Probability Positional"])
    filt=QB[(QB.Date>=startdate)&(QB.Date<=enddate)&(QB.DraftType!="SAME")]

    filt['Median_Overall']=filt.groupby(["Player"])["Overall"].transform('median')
    filt['Median Overall']=filt['Median_Overall'].apply(lambda x: str(int(((x-1)//teams)+1))+"."+str(int((x-1)%teams+1)).zfill(2))
    filt['Median Positional']=filt.groupby(["Player"])["posrank"].transform('median')
    filt['Median Positional']=filt['Position']+filt['Median Positional'].map(str)

    filt['Draft Count']=filt.groupby(["Player"])["Pick"].transform('count')

    if not draft is None:
        filt['Drafted']=filt['Player'].apply(lambda x: "Yes" if x in already else "No")
        headers.append('Drafted')
        if drafted=="Yes":
            filt=filt[(filt.Drafted=="No")]
    filt["condition"]=filt.groupby(["league_id"])["Overall"].rank("dense")


    try:
        print(currentpick)
        filt['overO']=filt['Overall'].apply(lambda x: 1 if x >= currentpick else 0)
        filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
        filt['ProbP']=round(filt['ProbP']*100,0)
        filt['Base Rate Current Overall Pick:'+currentpickP]=filt['ProbP'].map(str)+'%'
        headers.append('Base Rate Current Overall Pick:'+currentpickP)
    except:
        s=1


    if franchise in franchises:
        temp=draft[(draft.Player=="")&(draft.Franchise==franchise)]
        yourcurrentpick=temp["Overall"].iloc[0]
        yourcurrentpickP=temp["Pick"].iloc[0]
        #filt['overO']=filt['Overall'].apply(lambda x: 1 if x >= yourcurrentpick else 0)
        #filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
        #filt['ProbP']=round(filt['ProbP']*100,0)
        #filt['Base Rate Next Pick:'+yourcurrentpickP]=filt['ProbP'].map(str)+'%'
        #headers.append('Base Rate Next Pick:'+yourcurrentpickP)

        filt['overO']=filt['condition'].apply(lambda x: 1 if x >= yourcurrentpick-currentpick+1 else 0)
        filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
        filt['ProbP']=round(filt['ProbP']*100,0)
        filt['Odds Available Next Pick:'+yourcurrentpickP]=filt['ProbP'].map(str)+'%'
        headers.append('Odds Available Next Pick:'+yourcurrentpickP)


        nextpick=temp["Overall"].iloc[1]
        nextpickP=temp["Pick"].iloc[1]
        #filt['overO']=filt['Overall'].apply(lambda x: 1 if x >= nextpick else 0)
        #filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
        #filt['ProbP']=round(filt['ProbP']*100,0)
        #filt['Base Rate 2Picks:'+nextpickP]=filt['ProbP'].map(str)+'%'
        #headers.append('Base Rate 2Picks:'+nextpickP)

        filt['overO']=filt['condition'].apply(lambda x: 1 if x >= (nextpick-currentpick+1) else 0)
        filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
        filt['ProbP']=round(filt['ProbP']*100,0)
        filt['Odds Available 2Picks:'+nextpickP]=filt['ProbP'].map(str)+'%'
        headers.append('Odds Available 2Picks:'+nextpickP)


    pickP=str(((pick-1)//teams)+1)+"."+str((pick-1)%teams+1).zfill(2)
    filt = filt.sort_values(['Median_Overall'])
    if pick:

        try:
            filt['overO']=filt['condition'].apply(lambda x: 1 if x >= pick-currentpick+1 else 0)
            filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
            filt['ProbP']=round(filt['ProbP']*100,0)
            filt['Odds Available Custom Pick:'+pickP]=filt['ProbP'].map(str)+'%'
            headers.append('Odds Available Custom Pick:'+pickP)
            if pick-currentpick <0:
                filt['Odds Available Custom Pick:'+pickP]="Past Pick"

        except:
            filt['overO']=filt['Overall'].apply(lambda x: 1 if x >= pick else 0)
            filt['ProbP']=filt.groupby(["Player"])["overO"].transform('mean')
            filt['ProbP']=round(filt['ProbP']*100,0)
            filt['Base Rate Custom Pick:'+pickP]=filt['ProbP'].map(str)+'%'
            headers.append('Base Rate Custom Pick:'+pickP)



    df=filt
    df=df.drop_duplicates(subset='Player', keep='first')


    df=df[headers]






    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table







@app.callback(
    Output(component_id='outputgraph',component_property='children'),
    [Input("Type", "value"),
     Input("input1", "value"),Input("input2", "value"),Input("input3", "value"),Input("input4", "value"),
     Input("confswitch1", "on"),Input("confswitch2", "on"),Input("confswitch3", "on"),Input("confswitch4", "on"),
     Input("knob1", "value"),Input("knob2", "value"),Input("knob3", "value"),Input("knob4", "value"),
     Input("startdate", "value"),
     Input("enddate", "value"),Input("window", "value")]
    )
def update_Graph(Type,input1,input2,input3,input4,
                 confswitch1,confswitch2,confswitch3,confswitch4,
                 knob1,knob2,knob3,knob4,
                 startdate,enddate,window
                 ):
    startdate=datetime.date(*(int(s) for s in startdate.split('-')))
    enddate=datetime.date(*(int(s) for s in enddate.split('-')))
    print(startdate)
    #startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    #startdate=startdate.dt.date
    #enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    #enddate=enddate.dt.date
    data =list()
    pos=""
    #x_axis.reverse()
    lower=[0]
    lower2=[0]
    lower3=[0]
    lower4=[0]
    if  input1 in Players and (startdate in Dates) and (enddate in Dates):
        days = datetime.timedelta(window)
        median=[]
        upper=[]
        lower=[]
        xdate=[]

        hi=((knob1/2)+50)/100
        lo=(50-(knob1/2))/100
        for date in [i for i in Dates if i >= startdate and i<=enddate]:
            #start = datetime.datetime.strptime(date, '%m/%d/%Y')
            start=date-days
            #start=start.strftime('%m/%d/%Y')
            filt=QB[(QB.Player==input1)&(QB.Date>=start)&(QB.Date<=date)&(QB.DraftType!="SAME")]
            if len(filt)==0:
                continue
            pos=filt["Position"].iloc[0]
            lower.append(-filt[Type].quantile(hi))
            median.append(-filt[Type].quantile(0.5))
            upper.append(-filt[Type].quantile(lo))
            xdate.append(date)
        if confswitch1:
            data.append({'x':xdate,'y':upper,'line':{'color':'#81ecf7','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"upper"})
            data.append({'x':xdate,'y':median,'line':{'color':'#81ecf7','width':2},'marker':{'color':'#1f77b4','size':2},"name":input1})
            data.append({'x':xdate,'y':lower,'line':{'color':'#81ecf7','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"lower"})
        else:
            data.append({'x':xdate,'y':median,'line':{'color':'#81ecf7','width':2},'marker':{'color':'#1f77b4','size':2},"name":input1})

            #Pts=QB[(QB.Player==input1)&(QB.Date>=startdate)&(QB.Date<=enddate)&(QB.DraftType==Type)]
            #Pts=Pts.sort_values(by=['Date'])
            #print(Pts)
            #xdat=Pts['Date']
            #Pts=Pts[Type]
            #data.append({'x':xdat,'y':Pts,'mode':'markers','marker':{'color':'#81ecf7','size':4},'type':'scatter',"name":input1})


    if  input2 in Players and (startdate in Dates) and (enddate in Dates):
        days = datetime.timedelta(window)
        median2=[]
        upper2=[]
        lower2=[]
        xdate2=[]

        hi2=((knob2/2)+50)/100
        lo2=(50-(knob2/2))/100
        for date in [i for i in Dates if i >= startdate and i<=enddate]:
            #start = datetime.datetime.strptime(date, '%m/%d/%Y')
            start=date-days
            #start=start.strftime('%m/%d/%Y')
            filt=QB[(QB.Player==input2)&(QB.Date>=start)&(QB.Date<=date)&(QB.DraftType!="SAME")]
            if len(filt)==0:
                continue
            pos=filt["Position"].iloc[0]
            lower2.append(-filt[Type].quantile(hi2))
            median2.append(-filt[Type].quantile(0.5))
            upper2.append(-filt[Type].quantile(lo2))
            xdate2.append(date)
        if confswitch2:
            data.append({'x':xdate2,'y':upper2,'line':{'color':'#fff','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"upper"})
            data.append({'x':xdate2,'y':median2,'line':{'color':'#fff','width':2},'marker':{'color':'#1f77b4','size':2},"name":input2})
            data.append({'x':xdate2,'y':lower2,'line':{'color':'#fff','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"lower"})
        else:
            data.append({'x':xdate2,'y':median2,'line':{'color':'#fff','width':2},'marker':{'color':'#1f77b4','size':2},"name":input2})

    if  input3 in Players and (startdate in Dates) and (enddate in Dates):
        days = datetime.timedelta(window)
        median3=[]
        upper3=[]
        lower3=[]
        xdate3=[]

        hi3=((knob3/2)+50)/100
        lo3=(50-(knob3/2))/100
        for date in [i for i in Dates if i >= startdate and i<=enddate]:
            #start = datetime.datetime.strptime(date, '%m/%d/%Y')
            start=date-days
            #start=start.strftime('%m/%d/%Y')
            if len(filt)==0:
                continue
            filt=QB[(QB.Player==input3)&(QB.Date>=start)&(QB.Date<=date)&(QB.DraftType!="SAME")]
            pos=filt["Position"].iloc[0]
            lower3.append(-filt[Type].quantile(hi3))
            median3.append(-filt[Type].quantile(0.5))
            upper3.append(-filt[Type].quantile(lo3))
            xdate3.append(date)
        if confswitch3:
            data.append({'x':xdate3,'y':upper3,'line':{'color':'#003efa','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"upper"})
            data.append({'x':xdate3,'y':median3,'line':{'color':'#003efa','width':2},'marker':{'color':'#1f77b4','size':2},"name":input3})
            data.append({'x':xdate3,'y':lower3,'line':{'color':'#003efa','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"lower"})
        else:
            data.append({'x':xdate3,'y':median3,'line':{'color':'#003efa','width':2},'marker':{'color':'#1f77b4','size':2},"name":input3})


    if  input4 in Players and (startdate in Dates) and (enddate in Dates):
        days = datetime.timedelta(window)
        median4=[]
        upper4=[]
        lower4=[]
        xdate4=[]

        hi4=((knob4/2)+50)/100

        lo4=(50-(knob4/2))/100
        for date in [i for i in Dates if i >= startdate and i<=enddate]:
            #start = datetime.datetime.strptime(date, '%m/%d/%Y')
            start=date-days
            #start=start.strftime('%m/%d/%Y')
            if len(filt)==0:
                continue
            filt=QB[(QB.Player==input4)&(QB.Date>=start)&(QB.Date<=date)&(QB.DraftType!="SAME")]
            print(filt)
            pos=filt["Position"].iloc[0]
            lower4.append(-filt[Type].quantile(hi4))
            median4.append(-filt[Type].quantile(0.5))
            upper4.append(-filt[Type].quantile(lo4))
            xdate4.append(date)
        if confswitch4:
            data.append({'x':xdate4,'y':upper4,'line':{'color':'#a881f7','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"upper"})
            data.append({'x':xdate4,'y':median4,'line':{'color':'#a881f7','width':2},'marker':{'color':'#1f77b4','size':2},"name":input4})
            data.append({'x':xdate4,'y':lower4,'line':{'color':'#a881f7','width':2,'dash':'dash'},'marker':{'color':'#1f77b4','size':2},"name":"lower"})
        else:
            data.append({'x':xdate4,'y':median3,'line':{'color':'#a881f7','width':2},'marker':{'color':'#1f77b4','size':2},"name":input4})
    if Type=='Overall':
            tickvals=[-1]+[i for i in range(-12,-250,-12)]
            ticktext=["1st overall"]+["Round "+str(round(i/12)) for i in range(12,250,12)]
            ytitle="Overall Pick"
    else:
            tickvals=[-1,-3,-6,-12,-18,-24,-36,-48,-60,-72,-84]
            ticktext=[pos+"1",pos+"3",pos+"6",pos+"12",pos+"18",pos+"24",pos+"36",pos+"48",pos+"60",pos+"72",pos+"84"]
            ytitle="Positional ADP - "+pos
    toprange=min([min(lower),min(lower2),min(lower3),min(lower4)])
    print(toprange)
    if toprange>-25:
        toprange=-25


    if Type:
        return dcc.Graph(
                id='example',
                figure={
                    'data':data,
                    'layout': {
                        'legend':{
                            'xanchor':"center",
                            'yanchor':"top",
                            'y':500,
                            'x':0.5,
                            "orientation":"h"
                                },
                        'height':500,
                        'title':{'text':'Real Draft Position'},
                        'margin':{'t':'0px'},
                        'xaxis':{
                            'visible':True,
                            'color': colors['text'],
                            'title':{
                                'text':'Date'
                                },
                            'rangemode':'tozero'
                            },
                        'yaxis':{
                            'range':[toprange,0],
                            'fixedrange':True,
                            'visible':True,
                            'showline':True,
                            'color': colors['text'],
                            'title':{
                                'text':ytitle
                                },
                            'rangemode':'tozero',
                            'tickmode':'array',
                            'tickvals':tickvals,
                            'ticktext':ticktext,
                            },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {'color': colors['text']},
                        'bordercolor': colors['text']

                        }

                   }
            )

def display_links(df):
        links = df['link'].to_list()
        rows = []
        for x in links:
            link = '[Link](' +str(x) + ')'
            rows.append(link)
        return rows
@app.callback(
    Output(component_id='TradeTable',component_property='children'),
    [Input("tradeplayer", "value"),Input("QBs", "value"),
     Input("WRs", "value"),Input("TEs", "value"),
     Input("PassTD", "value"),Input("TEPrem", "value")]
    )
def GenerateTradeTable(player,QBs,WRs,TEs,PTD,TEP):
    Trades=TradesRaw
    Trades=Trades.dropna(subset=['Side1','Side2'])
    if player:
        print("Player =",player)
        if type(player)!=list:
            player=[player]
        for p in player:
            print(player)
            Trades=Trades[Trades['Side1'].str.contains(p)|Trades['Side2'].str.contains(p)].reset_index(drop=True)
    if QBs=="1QB":
        Trades=Trades[Trades['Lineup'].str.contains("QB: 1-1")].reset_index(drop=True)
    elif QBs=="SuperFlex":
        Trades=Trades[Trades['Lineup'].str.contains("QB: 1-2")].reset_index(drop=True)
    elif QBs=="2QB":
        Trades=Trades[Trades['Lineup'].str.contains("QB: 2-2")].reset_index(drop=True)
    if WRs=="2WR":
        Trades=Trades[Trades['Lineup'].str.contains("WR: 2")].reset_index(drop=True)
    elif WRs=="3WR":
        Trades=Trades[Trades['Lineup'].str.contains("WR: 3")].reset_index(drop=True)
    if TEs=="1TE":
        Trades=Trades[Trades['Lineup'].str.contains("TE: 1")].reset_index(drop=True)
    elif TEs=="2TE":
        Trades=Trades[Trades['Lineup'].str.contains("TE: 2")].reset_index(drop=True)
    if PTD=="4pt":
        Trades=Trades[Trades['Scoring'].str.contains("pTD: 4")].reset_index(drop=True)
    elif PTD=="6pt":
        Trades=Trades[Trades['Scoring'].str.contains("pTD: 6")].reset_index(drop=True)
    if TEP=="Yes":
        Trades=Trades[Trades['Scoring'].str.contains("TE_PPR: 1.5")|Trades['Scoring'].str.contains("TE_PPR: 1.75")|Trades['Scoring'].str.contains("TE_PPR: 2")].reset_index(drop=True)
    elif TEP=="No":
        Trades=Trades[~Trades['Scoring'].str.contains("TE_PPR: 1.5") & ~Trades['Scoring'].str.contains("TE_PPR: 1.75") & ~Trades['Scoring'].str.contains("TE_PPR: 2")].reset_index(drop=True)
    print(Trades.columns)
    Trades["link"]=["www58.myfantasyleague.com/2021/options?L=30932&O=03" for i in Trades["LeagueID"]]
    Trades["link"]=display_links(Trades)
    Trades=Trades[["Side1","Side2","Date","Scoring","Lineup"]].iloc[0:100]
    Table=dash_table.DataTable(
        id='TradeTab',
        columns=[{"name": i, "id": i,'presentation':'markdown'} if i=="link" else{"name": i, "id": i}for i in Trades.columns],
        data=Trades.to_dict('records'),
        fixed_rows={'headers': True},
        fixed_columns={'headers': True},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_header={
             'fontSize':14,
            'fontFamily': 'helvetica',
            'border': 'thin #a5d4d9 solid',
            'color': '#a5d4d9',
            'backgroundColor': '#313131',
            'padding':'10px'
            },
        style_filter={'color': '#fff', "backgroundColor": "#313131"},
        style_table={'minHeight':'1100px','height': '1100px','maxHeight':'1100px','border': '#000','height': '650px',"width":"95%"},
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
        style_data_conditional=[
                {'if': {'column_id': 'Date'},
             'width': '10%'}])
    return Table

@app.callback(
    Output(component_id='MostTraded',component_property='children'),
    [Input("TimePeriod", "value")]
    )
@cache.memoize(86400)
def GenerateMostTraded(TP):
    #cache.delete_memoized(GenerateMostTraded)
    if TP=='7Days':
        most=pd.read_csv(os.path.join(THIS_FOLDER,'data/Most7.csv'))
    elif TP=='14Days':
        most=pd.read_csv(os.path.join(THIS_FOLDER,'data/Most14.csv'))
    else:
        most=pd.read_csv(os.path.join(THIS_FOLDER,'data/Most30.csv'))
    Table=dash_table.DataTable(
        id='TradeTab',
        columns=[{"name": i, "id": i,'type': 'numeric','format': FormatTemplate.percentage(1).sign(Sign.positive)} if i =="Volume" else {"name": i, "id": i} for i in most.columns],
        data=most.to_dict('records'),
        fixed_rows={'headers': True},
        fixed_columns={'headers': True},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_header={
             'fontSize':25,
            'fontFamily': 'helvetica',
            'border': 'thin #a5d4d9 solid',
            'color': '#a5d4d9',
            'backgroundColor': '#313131',
            'padding':'10px'
            },
        style_filter={'color': '#fff', "backgroundColor": "#313131"},
        style_table={'minHeight':'650px','height': '650px','maxHeight':'650px','border': '#000','height': '650px',"width":"95%"},
        style_cell={
        'fontSize':22,
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
        style_data_conditional=[
                {'if': {'column_id': 'Date'},
             'width': '10%'}])
    return Table



@app.callback(
    Output(component_id='RDPtable',component_property='children'),
    [Input("startdate", "value"),
     Input("enddate", "value"),Input('position', "value"),
     Input('DraftType', "value"),Input("QBs", "value"),
     Input("WRs", "value"),Input("TEs", "value"),
     Input("PassTD", "value"),Input("TEPrem", "value"),Input("potentialpick", "value")
     ]
    )
def update_RDPTable(startdate,enddate,position,DraftType,QBs,WRs,TEs,PTD,TEP,potpick
                 ):

    startdate=datetime.date(*(int(s) for s in startdate.split('-')))
    enddate=datetime.date(*(int(s) for s in enddate.split('-')))
    #start=start.strftime('%m/%d/%Y')

    if DraftType=="StartUp":
        filt=QB[(QB.Date>=startdate)&(QB.Date<=enddate)]
        filt=filt[(filt.Position!="Pick")]
    else:
        QBR.to_csv("RookieTest.csv")
        filt=QBR[(QBR.Date>=startdate)&(QBR.Date<=enddate)]
        filt=filt[(filt.Position!="Pick")]
        QBR.to_csv("RookieTestDate.csv")
        filt=filt[(filt.Teams<16)]
    filt=filt.dropna(subset=['Lineup','Scoring'])
    filt=filt.dropna(subset=['Lineup','Scoring'])
    if QBs=="1QB":
        filt=filt[filt['Lineup'].str.contains("QB: 1,")].reset_index(drop=True)
    elif QBs=="SuperFlex":
        filt=filt[filt['Lineup'].str.contains("QB: 1-2")].reset_index(drop=True)
    elif QBs=="2QB":
        filt=filt[filt['Lineup'].str.contains("QB: 2-2")].reset_index(drop=True)
    if WRs=="2WR":
        filt=filt[filt['Lineup'].str.contains("WR: 2")].reset_index(drop=True)
    elif WRs=="3WR":
        filt=filt[filt['Lineup'].str.contains("WR: 3")].reset_index(drop=True)
    if TEs=="1TE":
        filt=filt[filt['Lineup'].str.contains("TE: 1")].reset_index(drop=True)
    elif TEs=="2TE":
        filt=filt[filt['Lineup'].str.contains("TE: 2")].reset_index(drop=True)
    if PTD=="4pt":
        filt=filt[filt['Scoring'].str.contains("pTD: 4")].reset_index(drop=True)
    elif PTD=="6pt":
        filt=filt[filt['Scoring'].str.contains("pTD: 6")].reset_index(drop=True)
    if TEP=="Yes":
        filt=filt[filt['Scoring'].str.contains("TE_PPR: 1.5")|filt['Scoring'].str.contains("TE_PPR: 1.75")|filt['Scoring'].str.contains("TE_PPR: 2")].reset_index(drop=True)
    elif TEP=="No":
        filt=filt[~filt['Scoring'].str.contains("TE_PPR: 1.5") & ~filt['Scoring'].str.contains("TE_PPR: 1.75") & ~filt['Scoring'].str.contains("TE_PPR: 2")].reset_index(drop=True)
    filt["Overall"]=filt["Overall"]/filt["Copies"]
    filt["Available"]=np.where(filt["Overall"]>=potpick,1,0)
    filt['Median_Overall']=filt.groupby(["Player"])["Overall"].transform('median')
    filt = filt.sort_values(['Median_Overall'])
    filt['Median Overall']=filt['Median_Overall'].apply(lambda x: str(int(((x-1)//12)+1))+"."+str(int((x-1)%12+1)).zfill(2))
    filt['Median Positional']=filt.groupby(["Player"])["posrank"].transform('median')
    filt['Median Positional']=filt['Position']+filt['Median Positional'].map(str)

    filt['Draft Count']=filt.groupby(["Player"])["Pick"].transform('count')
    filt['Availability']=filt.groupby(["Player"])["Available"].transform('sum')
    filt['Availability']=filt['Availability']*100/filt['Draft Count']
    filt['Availability']=filt['Availability'].map(int)
    filt['Availability']=filt['Availability'].map(str)
    filt['Availability']=filt['Availability']+"%"
    filt['percentile']= filt['Draft Count'].pct_change().fillna(0)+0.5
    filt=filt[filt['percentile']>0.5]
    df=filt
    df=df.drop_duplicates(subset='Player', keep='first')
    

    headers=["Player","Position","Draft Count","Median Overall","Median Positional",'Availability']
    df=df[headers]
    df.columns=["Player","Position","Draft Count","Median Overall","Median Positional",'Availability at pick '+str(int(((potpick-1)//12)+1))+"."+str(int((potpick-1)%12+1)).zfill(2)]
    if position != 'All':
        df =df[(df.Position==position)]
    else:
        df =df
    try:
        maxcount=max(df["Draft Count"])
    except:
        maxcount=0
    df=df[(df["Draft Count"]>maxcount*0.07)]


    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table




@app.callback(
    Output(component_id='FCgraph',component_property='children'),
    [Input("Stat", "value"),Input("input1", "value"),Input("startdate", "value"),Input("enddate", "value"),
     Input("input2", "value"),Input("startdate2", "value"),Input("enddate2", "value"),
     Input("input3", "value"),Input("startdate3", "value"),Input("enddate3", "value"),
     Input("input4", "value"),Input("startdate4", "value"),Input("enddate4", "value"),
     Input("split", "value"),Input("split2", "value"),Input("split3", "value"),Input("split4", "value")]
    )
def update_FCGraph(Stat,input1,startdate,enddate,
                 input2,startdate2,enddate2,
                 input3,startdate3,enddate3,
                 input4,startdate4,enddate4,
                 Split, Split2,Split3, Split4):

    print(Split,Split2)
    print(GameLogs['HomeAway'])
    data =list()
    #x_axis.reverse()
    if  input1 in Players1 and (startdate in SeasonWeeks) and (enddate in SeasonWeeks):
        if Split == 'All':
            Pts=GameLogs[Stat][(GameLogs.Rk==input1)&(GameLogs.SeasonWeek>=startdate)&(GameLogs.SeasonWeek<=enddate)]
        else:
            Pts=GameLogs[Stat][(GameLogs.Rk==input1)&(GameLogs.HomeAway==Split)&(GameLogs.SeasonWeek>=startdate)&(GameLogs.SeasonWeek<=enddate)]
        Pts=list(Pts)
        Pts=sorted(Pts)
        xdat=[i*100/(len(Pts)-1) for i in range(len(Pts))]
        data.append({'x':xdat,'y':Pts,'type':'line',"name":input1+" "+startdate+" to "+enddate+" "+Split})
    if  input2 in Players1 and (startdate2 in SeasonWeeks) and (enddate2 in SeasonWeeks):
        if Split2 == 'All':
            Pts=GameLogs[Stat][(GameLogs.Rk==input2)&(GameLogs.SeasonWeek>=startdate2)&(GameLogs.SeasonWeek<=enddate2)]
        else:
            Pts=GameLogs[Stat][(GameLogs.Rk==input2)&(GameLogs.HomeAway==Split2)&(GameLogs.SeasonWeek>=startdate2)&(GameLogs.SeasonWeek<=enddate2)]

            Pts=list(Pts)
        Pts=sorted(Pts)
        xdat=[i*100/(len(Pts)-1) for i in range(len(Pts))]
        data.append({'x':xdat,'y':Pts,'type':'line',"name":input2+" "+startdate2+" to "+enddate2+" "+Split2})
    if  input3 in Players1 and (startdate3 in SeasonWeeks) and (enddate3 in SeasonWeeks):
        if Split3 == 'All':
            Pts=GameLogs[Stat][(GameLogs.Rk==input3)&(GameLogs.SeasonWeek>=startdate3)&(GameLogs.SeasonWeek<=enddate3)]
        else:
            Pts=GameLogs[Stat][(GameLogs.Rk==input3)&(GameLogs.HomeAway==Split3)&(GameLogs.SeasonWeek>=startdate3)&(GameLogs.SeasonWeek<=enddate3)]
        Pts=list(Pts)
        Pts=sorted(Pts)
        xdat=[i*100/(len(Pts)-1) for i in range(len(Pts))]
        data.append({'x':xdat,'y':Pts,'type':'line',"name":input3+" "+startdate3+" to "+enddate3+" "+Split3})
    if input4 in Players1 and (startdate4 in SeasonWeeks) and (enddate4 in SeasonWeeks):
        if Split4 == 'All':
            Pts=GameLogs[Stat][(GameLogs.Rk==input4)&(GameLogs.SeasonWeek>=startdate4)&(GameLogs.SeasonWeek<=enddate4)]
        else:
            Pts=GameLogs[Stat][(GameLogs.Rk==input4)&(GameLogs.HomeAway==Split4)&(GameLogs.SeasonWeek>=startdate4)&(GameLogs.SeasonWeek<=enddate4)]

        Pts=list(Pts)
        Pts=sorted(Pts)
        xdat=[i*100/(len(Pts)-1) for i in range(len(Pts))]
        data.append({'x':xdat,'y':Pts,'type':'line',"name":input4+" "+startdate4+" to "+enddate4+" "+Split4})



    return dcc.Graph(
            id='example',
            figure={
                'data':data,
                'layout': {
                    'legend':{
                        'xanchor':"center",
                        'yanchor':"top",
                        'y':-0.3,
                        'x':0.5
                            },
                    'title':"Floor/Ceiling Distribution",
                    'xaxis':{
                        'title':{
                            'text':'Worst Games    <<< - Percentile - >>>    Best Games'
                            },
                        'rangemode':'tozero',
                        'dtick':10,
                        'nticks':11},
                    'yaxis':{
                        'title':{
                            'text':Stat
                            },
                        'rangemode':'tozero',
                        'dtick':10,
                        'nticks':11},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {'color': colors['text']},
                    'bordercolor': colors['text']
                    }
               }
        )
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        return df
    except Exception as e:
        print(e)
        return None


@app.callback(
    Output(component_id='NewDraftTable',component_property='children'),
    [Input("uploadNewDraftTable", "contents"),
     Input("ApplyChanges", "n_clicks"),
     Input("Type", "value")],
    [State(component_id='ChangeTable', component_property='data'),
    State(component_id='ChangeTable', component_property='columns'),
     State('uploadNewDraftTable', 'filename')]
    )
def update_NewDraftTable(list_of_contents,ApplyChanges,Type,data,columns,Filename):
    ctx = dash.callback_context
    mess=html.H1("")
    filepath=Conf.Filepathdict[Type]
    print(ctx.triggered[0]['prop_id'].split('.')[0])
    if ctx.triggered[0]['prop_id'].split('.')[0] == "uploadNewDraftTable":
        df=parse_contents(list_of_contents,Filename)
        df.to_csv("test.csv")
        if not isinstance(df, pd.DataFrame) or list(df.columns)!=['Date','DraftType','Overall','Pick','Player','Position','league_id','Name','Lineup','Scoring','Teams','Copies','Decision?']:
            mess=html.H1("Error Uploading")
        else:
            df=df[['Date','DraftType','Overall','Pick','Player','Position','league_id','Name','Lineup','Scoring','Teams','Copies',"Decision?"]]
            original=pd.read_csv(os.path.join(THIS_FOLDER,filepath),parse_dates=['Date'])
            newIDs=list(set(df["league_id"]))
            original=original[~original["league_id"].isin(newIDs)]
            original=original.append(df)
            original.to_csv(os.path.join(THIS_FOLDER,filepath),index=False)
            mess=html.H1("Upload Succesful")
    if ctx.triggered[0]['prop_id'].split('.')[0] == "ApplyChanges":
        df = pd.DataFrame(data, columns=[c['name'][1] if type(c['name'])==list else c['name'] for c in columns])
        df["Decision?"]=df["Decision?"].fillna("")
        Add=df[(df["Decision?"]=="Yes")&(df["DraftType"]!="SAME")]
        Confirmed=pd.read_csv(Conf.ConfirmedPath)
        Confirmed=Confirmed.append(Add)
        Confirmed.to_csv(Conf.ConfirmedPath,index=False)
        AddRookie=df[(df["Decision?"]=="Yes")&(df["DraftType"]=="SAME")]
        ConfirmedRookie=pd.read_csv(Conf.ConfirmedRookiePath)
        ConfirmedRookie=ConfirmedRookie.append(AddRookie)
        ConfirmedRookie.to_csv(Conf.ConfirmedRookiePath,index=False)
        no=df[df["Decision?"]=="No"]
        Exclude=pd.read_csv(Conf.ExcludePath)
        Exclude=Exclude.append(no)
        Exclude.to_csv(Conf.ExcludePath,index=False)
        if Type in ["Confirmed","ConfirmedRookie"]:
            df=df[df["Decision?"]!="No"]
        else:
            df=df[df["Decision?"]==""]
        df=df[['Date','DraftType','Overall','Pick','Player','Position','league_id','Name','Lineup','Scoring','Teams','Copies',"Decision?"]]
        df.to_csv(os.path.join(THIS_FOLDER,filepath),index=False)
    df=pd.read_csv(os.path.join(THIS_FOLDER,filepath),parse_dates=['Date'])
    df["Player"]=df["Player"].fillna("")
    df=df[df["Player"]!=""]
    if len(df)>0:
        df["Date"]=pd.to_datetime(df['Date'], errors='coerce')
        df["Date"]=df["Date"].dt.date
    df=df[['Date','DraftType','Overall','Pick','Player','Position','league_id','Name','Lineup','Scoring','Teams','Copies',"Decision?"]]
    return [mess,dash_table.DataTable(
        id='ChangeTable',
        columns=[{"name": i, "id": i,'presentation': 'dropdown',"editable": True} if i=='Decision?' else {"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        export_columns='visible',
        export_format='csv',
        fixed_rows={'headers': True},
        fixed_columns={'headers': True},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_header={
             'fontSize':14,
            'fontFamily': 'helvetica',
            'border': 'thin #a5d4d9 solid',
            'color': '#a5d4d9',
            'backgroundColor': '#313131',
            'padding':'10px'
            },
        style_filter={'color': '#fff', "backgroundColor": "#313131"},
        style_table={'minHeight':'1100px','height': '1100px','maxHeight':'1100px','border': '#000','height': '650px',"width":"95%"},
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
        style_data_conditional=[
                {'if': {'column_id': 'Date'},
             'width': '10%'}],
        dropdown={
            'Decision?': {
                'options': [
                        {'label': i, 'value': i}
                        for i in ["Yes","No",""]
                    ]
                }
            }
)]

@app.callback(
    Output(component_id='DraftChecker',component_property='children'),
    [Input("DraftPlayer", "value"),
     Input("DraftID", "value"),
     Input("DraftType", "value")
     ]
    )
def update_DraftChecker(Player,ID,Type):
    temp=AllDrafts[AllDrafts.columns]
    if Player:
        temp=temp[temp["Player"]==Player]
    if Player:
        temp=temp[temp["league_id"]==str(ID)]
    if Type:
        if Type=="Rookie":
            temp=temp[temp["league_id"]=="SAME"]
        else:
            temp=temp[temp["league_id"]!="SAME"]
    Table=dash_table.DataTable(
        id='TradeTab',
        columns=[{"name": i, "id": i,'presentation':'markdown'} if i=="link" else{"name": i, "id": i}for i in temp.columns],
        data=temp.to_dict('records'),
        fixed_rows={'headers': True},
        fixed_columns={'headers': True},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_header={
             'fontSize':14,
            'fontFamily': 'helvetica',
            'border': 'thin #a5d4d9 solid',
            'color': '#a5d4d9',
            'backgroundColor': '#313131',
            'padding':'10px'
            },
        style_filter={'color': '#fff', "backgroundColor": "#313131"},
        style_table={'minHeight':'1100px','height': '1100px','maxHeight':'1100px','border': '#000','height': '650px',"width":"95%"},
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
        style_data_conditional=[
                {'if': {'column_id': 'Date'},
             'width': '10%'}])
    return Table

@app.callback(
    Output("Draftmodal", "is_open"),
    [Input("Draftopen", "n_clicks"), Input("Draftclose", "n_clicks")],
    [State("Draftmodal", "is_open")],
)
def toggle_modalDraft(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output("startdate", "value"),Output("enddate", "value")],
    [Input("PostDraft", "n_clicks")], prevent_initial_call=True
)
def PostDraft(n1):
    if n1:
        return [datetime.date(2021, 5, 1),max(Dates)]