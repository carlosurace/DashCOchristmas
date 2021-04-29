'''
Created on Jun 24, 2020

@author: Carlo
'''
from mfl_services import mfl_service
import pandas as pd
# create a mfl service instance and create/update the player_id to name converter
mfl = mfl_service(update_player_converter=True)
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
for letter in ["ENFL(D)"]:
    draftpath=os.path.join(THIS_FOLDER,'data/All.csv')
    IDs=os.path.join(THIS_FOLDER,"data/2021IDsConfirmed.csv")
    IDs=pd.read_csv(IDs)
    draft=pd.read_csv(draftpath)
    already=draft['league_id'].map(str)
    Newleagues=IDs['league_id'].map(str)
    #Leagues2020=mfl.get_dynasty_league_idsType1(letter,'(SF/TE',2020)
    #print(len(Leagues2020),"2020 Leagues")
    #Leagues2021=mfl.get_dynasty_league_idsType1(letter,'(SF/TE',2021)
    #print(len(Leagues2021),"2021 Leagues")
    #Newleagues=[str(league) for league in Leagues2021 if str(league) not in already]
    #Newleagues=[str(league) for league in Newleagues if str(league) not in Leagues2020]
    #Newleagues=["29275"]
    print(len(Newleagues),"New Leagues")
    #search=pd.read_csv(os.path.join(THIS_FOLDER,"Temp.csv"))
    #search=list(search["ID"])


    temppath=os.path.join(THIS_FOLDER,"data/Temp.csv")

    picks=mfl.get_multiple_leagues_draftsAll(Newleagues, temppath, year=2021, disable_progess_bar=False)
    temp=pd.read_csv(temppath)
    newcodes=list(set(temp["league_id"].map(int)))
    draft["league_id"]=draft["league_id"].map(int)
    draft=draft[~draft.league_id.map(int).isin(newcodes)]
    draft=draft.append(temp)
    draft["posrank"] = draft.groupby(["league_id","Position"])["Overall"].rank("dense")
    draft.to_csv(draftpath)
