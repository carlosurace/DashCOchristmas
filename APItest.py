'''
Created on Sep 27, 2021

@author: Carlo Surace
'''
from ExportAPI import ExportApi
import json

db=ExportApi(2021)
LS=db.live_scoring(70336, 3, False)
print(LS["liveScoring"]["matchup"][0])
for match in LS["liveScoring"]["matchup"]:
    print ("Team1",match["franchise"][0]["id"],"-",match["franchise"][0]["id"],",","Team2",match["franchise"][1]["id"],"-",match["franchise"][1]["id"])
