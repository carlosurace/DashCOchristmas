'''
Created on Apr 28, 2021

@author: Carlo Surace
'''
import os
import pandas as pd
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

ForReviewPath=os.path.join(THIS_FOLDER,"data/DraftFiles/ForReview.csv")
ForReviewRookiePath=os.path.join(THIS_FOLDER,"data/DraftFiles/ForReviewRookie.csv")
EmptyRookiePath=os.path.join(THIS_FOLDER,"data/DraftFiles/EmptyRookie.csv")
EmptyPath=os.path.join(THIS_FOLDER,"data/DraftFiles/Empty.csv")
ExcludePath=os.path.join(THIS_FOLDER,"data/DraftFiles/Exclude.csv")
temppath=os.path.join(THIS_FOLDER,"data/DraftFiles/Temp.csv")
ConfirmedPath=os.path.join(THIS_FOLDER,"data/DraftFiles/Confirmed.csv")
ConfirmedRookiePath=os.path.join(THIS_FOLDER,"data/DraftFiles/ConfirmedRookie.csv")

StartupsPath=os.path.join(THIS_FOLDER,"data/DraftFiles/Startups.csv")
RookiesPath=os.path.join(THIS_FOLDER,"data/DraftFiles/Rookies.csv")


Ngroup=10

def FilterPlayer(df,Yes):
    if Yes:
        df=df[df["Player"]!=" "]
    else:
        df=df[df["Player"]==" "]
    return df
def FilterRookie(df,Yes):
    if Yes:
        df=df[df["Draft length"]<7]
    else:
        df=df[df["Draft length"]>8]
    return df

def ApplyFiling(filename,filters,df,category,decision=''):
    tempfile=pd.read_csv(filename)
    df=FilterPlayer(df,filters[0])
    df=FilterRookie(df,filters[1])
    df["Decision?"]=decision
    print(str(len(df)),"drafts entered into",category)
    tempfile=tempfile.append(df)
    tempfile=tempfile[['Date','DraftType','Overall','Pick','Player','Position',"Last Pick","Draft length",'league_id','Name','Lineup','Scoring','Teams','Copies',"Decision?"]]
    tempfile.to_csv(filename,index=False)
    


Categories=["ForReview","ForReviewRookie","Empty","EmptyRookie","Confirmed","ConfirmedRookie","Exclude"]
Paths=[ForReviewPath,ForReviewRookiePath,EmptyPath,EmptyRookiePath,ConfirmedPath,ConfirmedRookiePath,ExcludePath]
Filepathdict=ChangeNameDict=dict(zip(Categories,Paths))
Filters=[[True,False],[True,True],[False,False],[False,True]]