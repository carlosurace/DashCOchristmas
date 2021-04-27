'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
import numpy as np
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
def GetNewDrafts():
    ForReview=pd.read_csv(os.path.join(THIS_FOLDER,"data/ForReview.csv"))
    temppath=os.path.join(THIS_FOLDER,"data/Temp.csv")
    draftpath=os.path.join(THIS_FOLDER,'data/DraftMaster.csv')
    draftpathcsv=pd.read_csv(draftpath)
    already=ForReview.append(draftpathcsv)
    already=list(set(draftpathcsv["league_id"].map(int).map(str)))
    Leagues2021=mfl.get_dynasty_league_idsType1(" ",'(SF/TE',2021)
    Leagues2021=list(set(Leagues2021))
    
    Newleagues=[str(league) for league in Leagues2021 if str(league) not in already]
    print(len(Leagues2021),"2021 Leagues")
    for n in range(len(Newleagues)//200):
        picks=mfl.get_multiple_leagues_drafts1(Newleagues[n*100,(n+1)*100], temppath, year=2021, disable_progess_bar=False)
        #newcodes=list(set(temp["league_id"].map(int)))
        #draft["league_id"]=draft["league_id"].map(int)
        #draft=draft[~draft.league_id.map(int).isin(newcodes)]
        #draft=draft.append(temp)
        #draft["posrank"] = draft.groupby(["league_id","Position"])["Overall"].rank("dense")
        #draft.to_csv(draftpath)
    
        temp=pd.read_csv(temppath)
        temp["Date"]=temp["Date"].fillna(0)
        temp["Date"]=pd.to_datetime(temp["Date"].astype(int), unit='s')
        temp["Player"]=temp["Player"].fillna(" ")
        temp=temp[temp["Player"]!=" "]
        NewDrafts=list(set(temp["league_id"].map(int).map(str)))
        rules=pd.DataFrame()
        n=0
        for i in NewDrafts:
            print(i)
            n+=1
            print(n,"/",len(NewDrafts),"Rules")
            rule=mfl.get_league_info([i],2021)
            if isinstance(rule, pd.DataFrame):
                rules=pd.concat([rules,rule], axis=0, ignore_index=False)
                print(rule)
        
                print(n,"/",len(NewDrafts),"Rules")
            else:
                print("Not Df")
                rule=pd.DataFrame(columns=["ID"])
                rule["ID"].loc[0]=i
                rules=pd.concat([rules,rule], axis=0, ignore_index=False)
        
        pos=['QB','RB','WR','TE','WR+TE','RB+WR+TE','FB','KR','PK','PN','Off','TMQB','TMRB','TMWR','TMTE','TMPK','TMPN','TMDL','TMLB','TMDB',
        'Def','ST','DE','DT','DT+DE','LB','CB','S','CB+S']
        realpos=[]
        for col in pos:
            try:
                rules[col]=rules[col].map(str)
                rules[col]=np.where(rules[col]!="nan",col+": "+rules[col]+", ","")
                realpos.append(col)
            except:
                continue
        rules["Lineup"]=rules[realpos].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
        #RuleDrafts["Lineup"]=np.where(RuleDrafts["Lineup"]!="nan",RuleDrafts["Lineup"].str[:-2],"")
        
        ppr=["QBTD","RBPPR","WRPPR","TEPPR"]
        for col in ppr:
            rules[col].map(str)
        rules["QBTD"]="QB_pTD: "+rules["QBTD"].map(str)
        rules["RBPPR"]="RB_PPR: "+rules["RBPPR"].map(str)
        rules["WRPPR"]="WR_PPR: "+rules["WRPPR"].map(str)
        rules["TEPPR"]="TE_PPR: "+rules["TEPPR"].map(str)
        rules["Scoring"]=rules[ppr].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)
    
        rules=rules[["ID","Name","Lineup","Scoring","Teams","Copies"]]
        temp["league_id"]=temp["league_id"].map(int)
        temp["league_id"]=temp["league_id"].map(str)
        rules["ID"]=rules["ID"].map(int)
        rules["ID"]=rules["ID"].map(str)
        temp=temp.merge(rules, left_on="league_id", right_on="ID")
        ForReview=ForReview.append(temp)
        ForReview=ForReview[['Date','DraftType','Overall','Pick','Player','Position','league_id','Name','Lineup','Scoring','Teams','Copies']]
        ForReview["Decision?"]
        ForReview.to_csv(os.path.join(THIS_FOLDER,"data/ForReview.csv"),index=False)
#draftpathcsv=draftpathcsv.append(temp)
#draftpathcsv.to_csv(draftpath)
'''
def UpdateLeagueList():
    ForReview=pd.read_csv(os.path.join(THIS_FOLDER,"data/ForReview.csv"))
    temppath=os.path.join(THIS_FOLDER,"data/Temp.csv")
    draftpath=os.path.join(THIS_FOLDER,'data/2021DraftsAll.csv')
    draftpathcsv=pd.read_csv(draftpath)
    already=ForReview.append(draftpathcsv)
    already=list(set(draftpathcsv["league_id"].map(int).map(str)))
    draftpathcsv=draftpathcsv.append(temp)
    draftpathcsv.to_csv(draftpath)
'''


GetNewDrafts()


