'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
import numpy as np
import ConfigF as Conf
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def GetConfirmedDrafts(search):
    already=pd.DataFrame()
    for Path in [Conf.ConfirmedPath,Conf.ConfirmedRookiePath]:
        already=already.append(pd.read_csv(Path))
    already=list(set(already["league_id"].map(int).map(str)))
    return already

def GetNewDrafts():
    Newleagues = GetConfirmedDrafts(" ")
    print(len(Newleagues),"Empty Leagues")
    for n in range(len(Newleagues)//Conf.Ngroup):
        try:
            print("iteration",n,"Groups of",Conf.Ngroup)
            draftlist=Newleagues[n*Conf.Ngroup:(n+1)*Conf.Ngroup]
            mfl.get_multiple_leagues_drafts1(draftlist, Conf.temppath, year=2021, disable_progess_bar=False)
            temp=pd.read_csv(Conf.temppath)
            temp["Date"]=temp["Date"].fillna(0)
            temp["Date"]=pd.to_datetime(temp["Date"].astype(int), unit='s')
            temp=temp[(temp["DraftType"]!=" ")&temp["DraftType"]!=""]
            draftlist=list(set(temp["league_id"].map(int).map(str)))
            rules=pd.DataFrame()
            n=0
            for i in draftlist:
                print(i)
                n+=1
                print(n,"/",len(draftlist),"Rules")
                rule=mfl.get_league_info([i],2021)
                if isinstance(rule, pd.DataFrame):
                    rules=pd.concat([rules,rule], axis=0, ignore_index=False)
                    print(rule)

                    print(n,"/",len(draftlist),"Rules")
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
                if col not in rule.columns:
                    rules[col]=rules[col]
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
            temp["Player"]=temp["Player"].fillna(" ")
            temp=temp[temp["Player"]!=" "]
            newIDs=list(set(temp["league_id"]))
            print(len(newIDs),"New Drafts Kicked off")
            
            for file in [Conf.ConfirmedPath,Conf.ConfirmedRookiePath]:
                Empty=pd.read_csv(file)
                Empty=Empty[~Empty["league_id"].isin(newIDs)]
                Empty.to_csv(file)
            for a in range(2):
                Conf.ApplyFiling(Conf.Paths[a],Conf.Filters[a],temp,Conf.Categories[a],"Yes")
        except:
            continue

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


