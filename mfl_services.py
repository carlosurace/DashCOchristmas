from bs4 import BeautifulSoup
import requests
import re
import json
import time
from tqdm import tqdm
from IdConverterMFL import id_converter
import csv
import os
import pandas as pd


class mfl_service:

    def __init__(self, update_player_converter=True):
        # initialize id converter
        self.id_to_player_converter = id_converter(update=update_player_converter)
        self.num_trades_collected = 0


    def get_dynasty_league_ids(self):
        # be nice to MFL servers
        time.sleep(2)

        page = requests.get("http://www68.myfantasyleague.com/2020/index?YEAR=2020&SEARCH=SafeLeagues+Dynasty&submit=Go")

        # check that page downloaded correctly
        if str(page.status_code)[0] != str(2):
            print("Error downloading page.")

        soup = BeautifulSoup(page.content, 'html.parser')

        league_id_list = []
        for league in soup.find_all('a', href=True):
            league_string = re.escape(str(league))
            if 'Dynasty' in league_string:
                pos=league_string.find("2020/home/")
                id = league_string[pos+10:pos+15]

                league_id_list.append(id)
        return league_id_list

    def get_dynasty_league_idsType(self,keyword,LeagueType,year):
        # be nice to MFL servers
        time.sleep(2)

        page = requests.get("http://www68.myfantasyleague.com/"+str(year)+"/index?YEAR="+str(year)+"&SEARCH="+keyword+"&submit=Go")

        # check that page downloaded correctly

        if str(page.status_code)[0] != str(2):
            print(page)
            print("Error downloading page.")

        soup = BeautifulSoup(page.content, 'html.parser')
        league_id_list = []
        for league in soup.find_all('a', href=True):
            league_string = re.escape(str(league))
            if LeagueType in league_string:
                pos=league_string.find(str(year)+"/home/")
                id = league_string[pos+10:pos+15]
                league_id_list.append(id)
        return league_id_list

    def get_dynasty_league_idsType1(self,keyword,LeagueType,year):
        # be nice to MFL servers
        time.sleep(2)

        page = requests.get("http://www68.myfantasyleague.com/"+str(year)+"/index?YEAR="+str(year)+"&SEARCH="+keyword+"&submit=Go")

        # check that page downloaded correctly

        if str(page.status_code)[0] != str(2):
            print(page)
            print("Error downloading page.")

        soup = BeautifulSoup(page.content, 'html.parser')
        league_id_list = []
        for league in soup.find_all('a', href=True):
            league_string = re.escape(str(league))
            pos=league_string.find(str(year)+"/home/")
            id = league_string[pos+10:pos+15]
            league_id_list.append(id)
        return league_id_list

    def get_league_info(self,leaguelist,year):
        count=0
        rules=pd.DataFrame()
        for id in leaguelist:
            count+=1
            #print(count)
            #try:
            xrow=[]
            SF=self.get_starter_rules(id,year)
            PPR=self.get_scoring_rules(id,year)
            name=self.get_name(id,year)
            df=pd.DataFrame(columns=["Name","QBTD","WRPPR","RBPPR","TEPPR"])
            xrow.append(name)
            xrow=xrow+PPR
            df.loc[0] = xrow
            #.split("/")[5].split("\\")[0]
            SF=SF.join(df)
            if count==1:
                rules=SF
            else:
                rules=pd.concat([rules,SF], axis=1, ignore_index=False)
            #print(count)
            count+=1
        return rules
    '''
            except:
                #print("league Failed Concat",id)
                rule=pd.DataFrame(columns=["ID","Fail"])
                rule.loc[0]=[i,"Concat"]
                return rule
    '''


    def make_trade_side_list(self, trade, side, convert_to_player=True):
        # can get errors and pass string when should be dict
        if isinstance(trade, str):
            ##print('Lost another one')
            return
            #trade = json.loads(trade)

        # get players involed in trade as list
        side1_players = trade[side].split(",")

        # remove empty strings
        side1_players = filter(None, side1_players)

        # convert id to players
        if convert_to_player:
            side1_players = self.id_to_player_converter.convert_trade(side1_players)
        return side1_players

    def get_server(self, league_id,year):
        servers=range(55,87)
        for i in servers:
            try:
                server=i
                trade_url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=draftResults&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue
        try:
            page = requests.get(trade_url)
            page.raise_for_status()

            # load json as dictionary
            draft_dict = json.loads(page.text)
        except:
            #print(trade_url)
            #print('Error downloading:', league_id)
            return
        return(server)

    def get_league_trades(self, league_id, year,days, csv_writer=None):
        '''
        Finds all trades in league.  Should return real name of playesr?

        :param league_id: league id to gather trade data from
        :return: list of all trades in league
        '''
        servers=range(55,88)
        for i in servers:
            try:
                server=i
                trade_url = "http://www"+str(server)+".myfantasyleague.com/" + str(year) + "/export?TYPE=transactions&L=" \
                    + str(league_id) + "&TRANS_TYPE=TRADE&DAYS=" + str(days) + "&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                trades_dict = json.loads(page.text)
                break
            except:
                continue
        if server==87:
            #print(trade_url)
            #print('Error downloading:', league_id)
            return

        #trades_dict = load_obj('trade_dict') # for easy testing
        trade_data = []

        # make sure transaction exists
        if 'transactions' in trades_dict and 'transaction' in trades_dict['transactions']:
            for trade in trades_dict['transactions']['transaction']:
                # get players in trade, split into list, convert to real name
                side1_players = self.make_trade_side_list(trade, 'franchise1_gave_up')
                side2_players = self.make_trade_side_list(trade, 'franchise2_gave_up')

                # make sure neither side is empty
                if side1_players is None or side2_players is None:
                    continue

                # weird stuff if pick can't be converted
                if None in side1_players or None in side2_players:
                    continue

                timestamp = int(trade['timestamp'])
                single_trade = [side1_players, side2_players, timestamp, league_id]

                trade_data.append(single_trade)

                if csv_writer is not None:
                    csv_writer.writerow(single_trade)
        self.num_trades_collected += len(trade_data)
        #print(len(trade_data), ", Total:", self.num_trades_collected)
        return trade_data


    def get_multiple_leagues_trades(self, league_list, save_path, year=2017, disable_progess_bar=False):
        all_trades = []
        with open(save_path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["player1", "player2", "time", "league_id"])
            for league in tqdm(league_list, disable=disable_progess_bar):
                all_trades.append(self.get_league_trades(league, year, writer))
        return all_trades

    def get_ActiveDraft(self, league_id, year):
        '''
        Finds all trades in league.  Should return real name of playesr?

        :param league_id: league id to gather trade data from
        :return: list of all trades in league
        '''
        servers=range(55,87)


        for server in servers:
            try:
                trade_url = "http://www"+str(server)+".myfantasyleague.com/" + str(year) +"/export?TYPE=draftResults&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue
        if server==86:
            #print(trade_url)
            #print('Error downloading:', league_id)
            return
        #trades_dict = load_obj('trade_dict') # for easy testing
        trade_data = []
        # make sure transaction exists
        n=1

        typ=draft_dict['draftResults']['draftUnit']['draftType']
        draft=pd.DataFrame(columns=["Pick","Overall","Player","Position","Franchise"])
        for Pick in draft_dict['draftResults']['draftUnit']['draftPick']:
            # get players in trade, split into list, convert to real name
            if not typ:
                    continue

            pos = Pick["round"]+"."+Pick["pick"]
            franch=Pick["franchise"]
            overall=n
            n+=1
            if Pick["player"] == "":
                player =["",""]
            else:
                player = self.id_to_player_converter.convert(Pick["player"])
            if Pick['timestamp'] == "":
                timestamp = ""
            else:
                timestamp = int(Pick['timestamp'])


            draft.loc[len(draft)]=[pos,overall, player[0],player[1], franch]
        return draft

    def get_Draft(self, league_id, year, csv_writer=None):
        '''
        Finds all trades in league.  Should return real name of playesr?

        :param league_id: league id to gather trade data from
        :return: list of all trades in league
        '''
        servers=range(55,87)


        for server in servers:
            try:
                trade_url = "http://www"+str(server)+".myfantasyleague.com/" + str(year) +"/export?TYPE=draftResults&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue
        if server==86:
            #print(trade_url)
            #print('Error downloading:', league_id)
            return
        #trades_dict = load_obj('trade_dict') # for easy testing
        trade_data = []
        # make sure transaction exists
        n=1

        typ=draft_dict['draftResults']['draftUnit']['draftType']
        for Pick in draft_dict['draftResults']['draftUnit']['draftPick']:
            # get players in trade, split into list, convert to real name
            if not typ:
                    continue

            pos = Pick["round"]+"."+Pick["pick"]
            overall=n
            n+=1
            player = self.id_to_player_converter.convert(Pick["player"])
            if Pick['timestamp'] == "":
                timestamp = ""
            else:
                timestamp = int(Pick['timestamp'])


            single_pick = [pos,overall, player[0],player[1], timestamp, league_id,typ]

            trade_data.append(single_pick)

            if csv_writer is not None:
                csv_writer.writerow(single_pick)
        self.num_trades_collected += len(trade_data)
        #print(len(trade_data), ", Total:", self.num_trades_collected)
        return [trade_data,typ]
    def get_multiple_leagues_drafts(self, league_list, save_path, year, disable_progess_bar=False):
        all_picks = []
        with open(save_path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["Pick", "Overall", "Player","Position","Date", "league_id","DraftType"])
            for league in tqdm(league_list, disable=disable_progess_bar):
                try:
                    dat=self.get_Draft(league, year, writer)
                    if not dat:
                        continue
                    all_picks.append(dat[0])
                except:
                    pass
        return all_picks

    def get_Draft1(self, league_id, year, csv_writer=None):
        '''
        Finds all trades in league.  Should return real name of playesr?

        :param league_id: league id to gather trade data from
        :return: list of all trades in league
        '''
        servers=range(55,87)


        for server in servers:
            try:
                trade_url = "http://www"+str(server)+".myfantasyleague.com/" + str(year) +"/export?TYPE=draftResults&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue
        if server==86:
            csv_writer.writerow(["No Server","", '','', '', league_id,''])
            return ["No Server","", '','', '', league_id,'']
        #trades_dict = load_obj('trade_dict') # for easy testing
        trade_data = []
        # make sure transaction exists
        n=1
        p=1
        if not draft_dict:
            csv_writer.writerow(["No Data","", '','', '', league_id,''])
            return ["No Data","", '','', '', league_id,'']
        try:
            try:
                typ=draft_dict['draftResults']['draftUnit']['draftType']

                for Pick in draft_dict['draftResults']['draftUnit']['draftPick']:
                    # get players in trade, split into list, convert to real name
                    pos = Pick["round"]+"."+Pick["pick"]
                    lastpick=draft_dict['draftResults']['draftUnit']['draftPick'][len(draft_dict['draftResults']['draftUnit']['draftPick'])-1]
                    lastpos = lastpick["round"]+"."+lastpick["pick"]
                    overall=n
                    n+=1
                    try:
                        player = self.id_to_player_converter.convert(Pick["player"])
                    except:
                        player = "Pick"
                    if not player:
                        player=["Rookie Pick "+str(p),"Pick"]
                        p+=1
                    if Pick['timestamp'] == "":
                        timestamp=""
                        player="  "
                    else:
                        timestamp=int(Pick['timestamp'])
                    single_pick = [pos,overall, player[0],player[1], timestamp, league_id,typ,lastpos,int(lastpick["round"])-int(Pick["round"])+1]
                    csv_writer.writerow(single_pick)
                    trade_data.append(single_pick)
                    break
                return single_pick
            except:
                d=0
                for div in draft_dict['draftResults']['draftUnit']:
                    d+=1
                    typ=div['draftType']
                    n=1
                    p=1
                    for Pick in div['draftPick']:
                        # get players in trade, split into list, convert to real name
                        pos = Pick["round"]+"."+Pick["pick"]
                        lastpick=div['draftPick'][len(div['draftPick'])-1]
                        lastpos = lastpick["round"]+"."+lastpick["pick"]
                        overall=n
                        n+=1
                        try:
                            player = self.id_to_player_converter.convert(Pick["player"])
                        except:
                            player = "Pick"
                        if not player:
                            player=["Rookie Pick "+str(p),"Pick"]
                            p+=1
                        if Pick['timestamp'] == "":
                            timestamp=""
                            player="  "
                        else:
                            timestamp=int(Pick['timestamp'])
                        single_pick = [pos,overall, player[0],player[1], timestamp, float(league_id)+(d*0.01),typ,lastpos,int(lastpick["round"])-int(Pick["round"])+1]
                        csv_writer.writerow(single_pick)
                        trade_data.append(single_pick)
                        break
                return single_pick
        except:
            csv_writer.writerow( ["Fail","", '','', '', league_id,''])
            return ["Fail","", '','', '', league_id,'']

    def get_multiple_leagues_drafts1(self, league_list, save_path, year, disable_progess_bar=False):
        all_picks = []
        with open(save_path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["Pick", "Overall", "Player","Position","Date", "league_id","DraftType","Last Pick","Draft length"])
            for league in tqdm(league_list, disable=disable_progess_bar):
                dat=self.get_Draft1(league, year, writer)
                if not dat:
                    continue
        return all_picks


    def get_DraftAll(self, league_id, year, csv_writer=None):
        '''
        Finds all trades in league.  Should return real name of playesr?

        :param league_id: league id to gather trade data from
        :return: list of all trades in league
        '''
        servers=range(55,87)


        for server in servers:
            try:
                trade_url = "http://www"+str(server)+".myfantasyleague.com/" + str(year) +"/export?TYPE=draftResults&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(trade_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue
        if server==86:
            #print(trade_url)
            #print('Error downloading:', league_id)
            csv_writer.writerow(["No Server","", '','', '', league_id,''])
            return ["No Server","", '','', '', league_id,'']
        #trades_dict = load_obj('trade_dict') # for easy testing
        trade_data = []
        # make sure transaction exists
        n=1
        p=1
        if not draft_dict:
            csv_writer.writerow(["No Data","", '','', '', league_id,''])
            return ["No Data","", '','', '', league_id,'']
        try:
            try:
                typ=draft_dict['draftResults']['draftUnit']['draftType']

                for Pick in draft_dict['draftResults']['draftUnit']['draftPick']:
                    # get players in trade, split into list, convert to real name
                    pos = Pick["round"]+"."+Pick["pick"]
                    overall=n
                    n+=1
                    try:
                        player = self.id_to_player_converter.convert(Pick["player"])
                    except:
                        player = "Pick"
                    if not player:
                        player=["Rookie Pick "+str(p),"Pick"]
                        p+=1
                    if Pick['timestamp'] == "":
                        timestamp=""
                        player="  "
                    else:
                        timestamp=int(Pick['timestamp'])
                    single_pick = [pos,overall, player[0],player[1], timestamp, league_id,typ]
                    csv_writer.writerow(single_pick)
                    trade_data.append(single_pick)
            except:
                d=0
                for div in draft_dict['draftResults']['draftUnit']:
                    d+=1
                    typ=div['draftType']
                    n=1
                    p=1
                    for Pick in div['draftPick']:
                        # get players in trade, split into list, convert to real name
                        pos = Pick["round"]+"."+Pick["pick"]
                        overall=n
                        n+=1
                        try:
                            player = self.id_to_player_converter.convert(Pick["player"])
                        except:
                            player = "Pick"
                        if not player:
                            player=["Rookie Pick "+str(p),"Pick"]
                            p+=1
                        if Pick['timestamp'] == "":
                            timestamp=""
                            player="  "
                        else:
                            timestamp=int(Pick['timestamp'])
                        single_pick = [pos,overall, player[0],player[1], timestamp, float(league_id)+(d*0.01),typ]
                        csv_writer.writerow(single_pick)
                        trade_data.append(single_pick)
        except:
            csv_writer.writerow( ["Fail","", '','', '', league_id,''])
            return ["Fail","", '','', '', league_id,'']

    def get_multiple_leagues_draftsAll(self, league_list, save_path, year, disable_progess_bar=False):
        all_picks = []
        with open(save_path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["Pick", "Overall", "Player","Position","Date", "league_id","DraftType"])
            for league in tqdm(league_list, disable=disable_progess_bar):
                try:
                    #print(league)
                    dat=self.get_DraftAll(league, year, writer)
                    if not dat:
                        continue
                except:
                    continue
        return all_picks

    def get_name(self,league_id,year):
        servers=range(50,90)
        for server in servers:
            try:
                url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=league&L="\
                + str(league_id) +"&W=&JSON=1"
                page = requests.get(url)
                page.raise_for_status()

                # load json as dictionary
                info = json.loads(page.text)
                break
            except:
                continue
        try:
            return info['league']['name']
        except:
            #print("Failed Name")
            return "Fail"


    def get_scoring_rules(self,league_id,year):
        # load league rules as json

        servers=range(50,90)
        for server in servers:
            try:
                league_scoring_url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=rules&L="\
                + str(league_id) +"&W=&JSON=1"
                page = requests.get(league_scoring_url)
                page.raise_for_status()

                # load json as dictionary
                scoring_rules_json = json.loads(page.content.decode('utf-8'))
                break
            except:
                continue
        rules = {'RB':0,'WR':0,'TE':0,'QB':0}
        # get ppr scoring

        try:
            try:
                x = scoring_rules_json['rules']['positionRules']["positions"]

            except:
                x=False
            if x:
                for pos in scoring_rules_json['rules']['positionRules']["positions"].split("|"):
                    if pos in ['RB','WR','TE','QB']:
                        for rule in scoring_rules_json['rules']['positionRules']["rule"]:
                            try:
                                x=rule['event']
                            except:
                                x=False
                            if "QB" in pos:
                                if x:
                                    if rule['event']['$t']=="#P":
                                        rules[pos] =rules[pos]+ float(rule['points']['$t'].replace("*",""))
                            else:
                                if x:
                                    if rule['event']['$t']=="CC":
                                        rules[pos] =rules[pos]+ float(rule['points']['$t'].replace("*",""))
            else:
                for position in scoring_rules_json['rules']['positionRules']:

                        for pos in position["positions"].split("|"):

                            if pos in ['RB','WR','TE','QB']:
                                if type(position["rule"])!=list:
                                    positionrule=[position["rule"]]
                                else:
                                    positionrule=position["rule"]
                                for rule in positionrule:

                                    try:
                                        x=rule['event']
                                    except:
                                        x=False
                                    if "QB" in pos:
                                        if x:
                                            if rule['event']['$t']=="#P":

                                                rules[pos] =rules[pos]+ float(rule['points']['$t'].replace("*",""))
                                            elif rule['event']['$t']=="#TD":
                                                #print(pos,float(rule['points']['$t'].replace("*","")))
                                                rules[pos] =rules[pos]+ float(rule['points']['$t'].replace("*",""))
                                        else:
                                            continue
                                    else:
                                        if x:
                                            if rule['event']['$t']=="CC":

                                                rules[pos] =rules[pos]+ float(rule['points']['$t'].replace("*",""))
                                        else:
                                            continue
            RBcol=[x for x in rules.keys() if 'RB' in x]
            RBPPR=0
            for i in RBcol:
                p=rules[RBcol[0]]

                RBPPR+=p
            WRcol=[x for x in rules.keys() if 'WR' in x]
            WRPPR=0
            for i in WRcol:
                p=rules[WRcol[0]]
                WRPPR+=p
            TEcol=[x for x in rules.keys() if 'TE' in x]
            TEPPR=0
            for i in TEcol:
                p=rules[TEcol[0]]
                TEPPR+=p
            QBcol=[x for x in rules.keys() if 'QB' in x]
            QB=0
            for i in QBcol:
                p=rules[QBcol[0]]
                QB+=p
            xrow=[QB,WRPPR,RBPPR,TEPPR]
            return(xrow)
        except:
            #print("Failed Scoring")
            return ["Fail","Fail","Fail","Fail"]


    def get_starter_rules(self, league_id,year):

        servers=range(50,87)
        for server in servers:
            try:

                league_rules_url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=league&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(league_rules_url)
                page.raise_for_status()

                # load json as dictionary
                rules_dict = json.loads(page.text)
                break
            except:
                continue
        #soup_rules = BeautifulSoup(league_rules.content, 'html.parser')
        try:
            league__single_rules = {}
            starterCount = rules_dict['league']['starters']['count']
            starterTeams =rules_dict['league']['franchises']['count']
            copies=rules_dict['league']['rostersPerPlayer']
            best=rules_dict['league']["bestLineup"]
            headers=list()
            info=list()
            for pos in rules_dict['league']['starters']['position']:
               headers.append(pos['name'])
               info.append(pos['limit'])
            rules=pd.DataFrame(columns=['ID','count',"Teams",'Copies','BestBall']+headers)
            rules.loc[0]=[league_id,starterCount,starterTeams,copies,best]+info
            return rules
        except:
            rule=pd.DataFrame(columns=["ID","FailRules"])
            rule.loc[0]=[league_id,league_id]
            #print("Failed Starters")
            return rule


    def get_starter_rulesError(self, league_id,year):

        servers=range(50,87)
        for server in servers:
            try:
                league_rules_url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=league&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(league_rules_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue

        league_rules = requests.get(league_rules_url)


        #soup_rules = BeautifulSoup(league_rules.content, 'html.parser')

        rules_dict = json.loads(league_rules.text)
        #print(rules_dict)

        league__single_rules = {}
        starterCount = rules_dict['league']['starters']['count']
        copies=rules_dict['league']['rostersPerPlayer']
        best=rules_dict['league']["bestLineup"]
        headers=list()
        info=list()
        for pos in rules_dict['league']['starters']['position']:
           headers.append(pos['name'])
           info.append(pos['limit'])
        rules=pd.DataFrame(columns=['ID','count','Copies','BestBall']+headers)
        rules.loc[0]=[league_id,starterCount,copies,best]+info
        return rules

    def get_rosters(self, league_id,year):

        servers=range(50,87)
        for server in servers:
            try:
                league_rules_url = "http://www"+str(server)+".myfantasyleague.com/"+str(year)+"/export?TYPE=league&L="\
                + str(league_id) +"&APIKEY=&JSON=1"
                page = requests.get(league_rules_url)
                page.raise_for_status()

                # load json as dictionary
                draft_dict = json.loads(page.text)
                break
            except:
                continue

        league_rules = requests.get(league_rules_url)


        #soup_rules = BeautifulSoup(league_rules.content, 'html.parser')
        try:
            rules_dict = json.loads(league_rules.text)
        except:
            try:
                rules_dict = json.loads(league_rules.text)
            except:
                try:
                    rules_dict = json.loads(league_rules.text)
                except:
                    #print(league_rules_url)
                    #print('Error downloading starters:', league_id)
                    return
        frandict={}
        for fran in rules_dict['league']['franchises']['franchise']:
            frandict[fran["id"]]=fran["name"]


        return frandict

    def get_leagues_rules(self, SAVE_PATH, league_ids, update_all=False, disable_progress_bar=False):

        # if rules json doesn't exist or updating all league rules
        if not os.path.exists(SAVE_PATH) or update_all:
            league_rules = {}
        else:
            league_rules = json.load(open(SAVE_PATH))

        for league_id in tqdm(league_ids, disable=disable_progress_bar):
            # if already have rules, don't redownload
            if league_id in league_rules:
                continue
            league_rules[league_id] = {}

            try:
                # get number of starters
                starter_rules = self.get_starter_rules(league_id)
                if starter_rules is not None:
                    league_rules[league_id]['starters'] = starter_rules
            except:
                print("Error downloading league:", league_id)

        # save league rules to json
        with open(SAVE_PATH, 'w') as fp:
            json.dump(league_rules, fp)
        return league_rules