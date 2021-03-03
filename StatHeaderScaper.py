import pandas
import requests, bs4
import re
## Provides a list of the html tables that can be found at the url
## provided.  The order in the list returned should reflect the order
## that the tables appear.  On pro-football-reference.com, these names
## usually indicate what information they contain.
def findTables(url):
    res = requests.get(url)
    print(res)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    print(soup)
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)
## For example:
## findTables("http://www.pro-football-reference.com/boxscores/201702050atl.htm")
## Pulls a table (indicated by tableID, which can be identified with
## "findTables") from the specified url. The header option determines
## if the function should try to determine the column names and put
## them in the returned data frame. The default for header is True.
## If you get an index error for data_header, try specifying header =
## False. I will include a generated error message for that soon.
def pullTable(url, tableID, header = True):
    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    print(soup)
    tables = soup.findAll('table', id = tableID)
    
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pandas.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)
## For example:
## url = "http://www.pro-football-reference.com/boxscores/201702050atl.htm"
## pullTable(url, "team_stats")
## Finds offensive player data for a given season.
## This one was written with fantasy football GMs in mind.
## stat indicates what statistic is desired.
## the user must specify "passing", "rushing", or "receiving"
## the year indicates the year in which the season of interest started
def seasonFinder (stat, year):
    url = "http://www.pro-football-reference.com/years/" + str(year) + "/" + stat + ".htm"
    if stat == "rushing":
        stat = "rushing_and_receiving"
    dat = pullTable(url, stat, header = False)
    dat = dat.reset_index(drop = True)
    names = dat.columns
    for c in range(0, len(names)):
        replacement = []
        if type (dat.loc[0][c]) == str:
            k = names[c]
            for i in range(0, len(dat[k])):
                p = dat.loc[i][c]
                xx = re.sub("[#@*&^%$!+]", "", p)
                xx = xx.replace("\xa0", "_")
                xx = xx.replace(" ", "_")
                replacement.append(xx)
            dat[k] = replacement
    return(dat)
## seasonFinder("passing", 2016)
## For example:
## tables = ["passing", "rushing", "receiving"]
## years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
##          2009, 2010, 2011, 2012, 2013, 2014, 2015]
## for y in years:
##     for t in tables:
##         SeasonFinder(t, y)
## Finds the play by play table a game with the date and homeTeam provided.
## The date has to be yyyymmdd with a 0 on the end.
## The reference sites use the trailing 0 incase there are multiple games on the same day (it happens in baseball).
## For the 2017 Superbowl the date of February 5th, 2017 would be 201702050.
## The team is the three letter abbrieviation for the home team in lower case.
def playByPlay (date, homeTeam):
    url = "http://www.pro-football-reference.com/boxscores/" +  str(date) + homeTeam + ".htm"
    dat = pullTable(url, "pbp")
    dat = dat.reset_index(drop = True)
    dat = dat.loc[dat["Detail"] != "None"]
    return(dat)
## For example:
## This provides the play by play for the 2017 Superbowl.
## playByPlay("201702050", "atl")
## This function provides an easy way to access NFL scouting combine data.
## The year indicates the year the combine was held.
## The pos argument can be used to specify a position to pull data for.
## If pos is not specified all data will be pulled.
def pullCombine(year, pos = None):
    url = "http://www.pro-football-reference.com/draft/" + str(year) + "-combine.htm"
    dat = pullTable(url, "combine")
    dat["year"] = year
    if pos is not None:
        dat = dat.loc[dat["Pos"] == pos]
    return(dat)
## For example:
## This pulls all data for Quarterbacks in 2016
## pullCombine(2016, "QB")
url="""https://stathead.com/football/pgl_finder.cgi?request=1&game_num_max=99&week_num_max=99&
order_by=age&season_start=1&qb_gwd=0&order_by_asc=0&qb_comeback=0&week_num_min=0&game_num_min=0&
year_min=2020&match=game&year_max=2020&season_end=-1&age_min=0&game_type=R&age_max=99&positions[]=qb&
positions[]=rb&positions[]=wr&positions[]=te&positions[]=e&positions[]=t&positions[]=g&positions[]=c&
positions[]=ol&positions[]=dt&positions[]=de&positions[]=dl&positions[]=ilb&positions[]=olb&
positions[]=lb&positions[]=cb&positions[]=s&positions[]=db&positions[]=k&positions[]=p&cstat[1]=fantasy_points&
ccomp[1]=gt&cval[1]=&cstat[2]=pass_cmp&ccomp[2]=gt&cval[2]=&cstat[3]=rec&ccomp[3]=gt&cval[3]=&cstat[4]=rush_att&
ccomp[4]=gt&cval[4]=&cstat[5]=fumbles_lost&ccomp[5]=gt&cval[5]=&offset=0"""
df=pullTable(url, 'results', header = False)
n=100
for i in range(2):
    print(i)
    offset=str(n)
    url="""https://stathead.com/football/pgl_finder.cgi?request=1&game_num_max=99&week_num_max=99&
    order_by=age&season_start=1&qb_gwd=0&order_by_asc=0&qb_comeback=0&week_num_min=0&game_num_min=0&
    year_min=2020&match=game&year_max=2020&season_end=-1&age_min=0&game_type=R&age_max=99&positions[]=qb&
    positions[]=rb&positions[]=wr&positions[]=te&positions[]=e&positions[]=t&positions[]=g&positions[]=c&
    positions[]=ol&positions[]=dt&positions[]=de&positions[]=dl&positions[]=ilb&positions[]=olb&
    positions[]=lb&positions[]=cb&positions[]=s&positions[]=db&positions[]=k&positions[]=p&cstat[1]=fantasy_points&
    ccomp[1]=gt&cval[1]=&cstat[2]=pass_cmp&ccomp[2]=gt&cval[2]=&cstat[3]=rec&ccomp[3]=gt&cval[3]=&cstat[4]=rush_att&
    ccomp[4]=gt&cval[4]=&cstat[5]=fumbles_lost&ccomp[5]=gt&cval[5]=&offset="""+offset
    try:
        df=df.append(pullTable(url, 'results', header = False))
        n+=100
    except:
        break
df.to_csv("Gamelogs.csv")
