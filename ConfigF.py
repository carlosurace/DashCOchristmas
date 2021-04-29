'''
Created on Apr 28, 2021

@author: Carlo Surace
'''
import os

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
        df=df[df["DraftType"]=="SAME"]
    else:
        df=df[df["DraftType"]!="SAME"]
    return df

Categories=["ForReview","ForReviewRookie","Empty","EmptyRookie","Confirmed","ConfirmedRookie","Exclude"]
Paths=[ForReviewPath,ForReviewRookiePath,EmptyPath,EmptyRookiePath,ConfirmedPath,ConfirmedRookiePath,ExcludePath]
Filepathdict=ChangeNameDict=dict(zip(Categories,Paths))
Filters=[[True,False],[True,True],[False,False],[False,True]]