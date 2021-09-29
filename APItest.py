'''
Created on Sep 27, 2021

@author: Carlo Surace
'''
from ExportAPI import ExportApi
from ImportAPI import ImportApi
import json
import pandas as pd




class session():
    def __init__(self, username,password,year):
        im=ImportApi(year,True)
        im.login(username,password)
        self.im=im
        #resp=im.blind_bid_waiver_request(None, ["10940_0.1_14083"],70336,"0005")
        #print(resp)
        db=ExportApi(year,True)
        db.login(username,password)
        self.db=db
        playerdict={}
        playerIDdict={}
        playerPosdict={}
        playerTeamdict={}
        Players=db.players(L=70336)
        for p in Players["players"]["player"]:
            playerIDdict.update({p["name"]:p["id"]})
            playerdict.update({p["id"]:p["name"]})
            playerPosdict.update({p["id"]:p["position"]})
            playerTeamdict.update({p["id"]:p["team"]})
        self.playerIDdict=playerIDdict
        self.playerdict=playerdict
        self.year=year

    def GetMyLeagues(self):
        ML=self.db.myLeagues(self.year)
        LeagueIDs={}
        TeamIDs={}
        for l in ML["leagues"]["league"]:
            LeagueIDs.update({l["name"]:l["league_id"]})
            TeamIDs.update({l["league_id"]:l["franchise_id"]})
        return LeagueIDs,TeamIDs
    
    
    
    def LiveScoreDisplay(self,L,W,details=False):
        LS=self.db.live_scoring(L, W, details)
        print(LS["liveScoring"]["matchup"][0])
        for match in LS["liveScoring"]["matchup"]:
            print ("Team1",match["franchise"][0]["id"],"-",match["franchise"][0]["id"],",","Team2",match["franchise"][1]["id"],"-",match["franchise"][1]["id"])
    
    def GetPlayerID(self,player):
        return self.playerIDdict[player]
    
    def GetPlayerName(self,id):
        return self.playerdict[id]
    
    def GetPlayerPosition(self,id):
        return self.playerPosdict[id]
    
    def GetPlayerTeam(self,id):
        return self.playerTeamdict[id]
    
    def FetchMyRosters(self):
        LeagueIDs,TeamIDs=self.GetMyLeagues()
        LeagueDF=pd.DataFrame(index=range(40))
        for L in LeagueIDs:
            
            Lid=LeagueIDs[L]
            Fid=TeamIDs[Lid]
            r=self.db.rosters(Lid, Fid)
            players=[]
            for p in r["rosters"]["franchise"]["player"]:
                players.append(self.GetPlayerName(p['id']))
            for i in range(40-len(players)):
                players.append("")
            LeagueDF[L]=players
            print(L,"Complete")
        print(LeagueDF)
        
    
    
sess=session("attitudeadjustment","Sheba28!",2021)
sess.FetchMyRosters()    
    
