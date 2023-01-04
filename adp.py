import pandas as pd

def main():
    replacement_avg_ppg = {"QB": 19.78, "RB": 16.10, "WR": 13.23, "TE": 16.27}

    temp_adp = pd.read_csv('adp.csv')
    cols = temp_adp.columns
    adp = temp_adp.loc[:,["ADP","Players + Rookies (390)"]]
    adp.columns = ['adp','player']
    adp = clean_adp(adp)
    adp = pd.DataFrame(data=adp.to_numpy(), index=adp['player'], columns=["adp", "player", "team", "pos"])
    adp = adp.drop('player', axis = 1)

    url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=500' \
            '&YEAR=2022&START_WEEK=1&END_WEEK=14&CATEGORY=overall&' \
            'POSITION=QB%7CRB%7CWR%7CTE%7CPK&DISPLAY=points&TEAM=*&SORT=AVG'
    lis = pd.read_html(url)
    temp_avgs = lis[1]
    columns = temp_avgs.columns
    avgs = temp_avgs[[columns[1], columns[3]]].copy()
    avgs.columns = ['player', 'avg']
    avgs = clean_avgs(avgs)
    avgs = pd.DataFrame(data=avgs.to_numpy(), index=avgs['player'], columns=["player", "ppg", "team", "pos"])
    avgs = avgs.drop('player', axis = 1)

    df = combined_df(adp,avgs)

def combined_df(adp,ppg):
    rows = []

    for player in adp.index:
        if player in ppg.index:
            rows.append([player, adp['adp'][player], ppg['ppg'][player], adp['team'][player], adp['pos'][player]])

    df = pd.DataFrame(data = rows, columns=["player","adp","ppg","team","pos"])
    return df

def clean_avgs(df):
    df['player'].iloc[38] = 'St.Brown, Amon-Ra DET WR'
    positions, teams = [], []

    for index in df.index:
        current = df['player'].iloc[index]
        elements = current.split(' ')
        if len(elements) < 4:
            print(current)
        player = elements[1] + ' ' + elements[0]
        player = player[:-1]
        teams.append(elements[2])
        positions.append(elements[3])
        df['player'].iloc[index] = player

    df['team'] = teams
    df['pos'] = positions
    df['pos'] = df.pos.astype('category')
    return df

def clean_adp(df):
    positions, teams = [], []

    for index in df.index:
        current = df['player'].iloc[index]
        elements = current.split(' ')
        player = elements[0] + ' ' + elements[1]
        if len(elements) < 4:
            teams.append('FA')
            positions.append(elements[2])
        else:
            teams.append(elements[2])
            positions.append(elements[3])
        df['player'].iloc[index] = player

    df['team'] = teams
    df['pos'] = positions
    df['pos'] = df.pos.astype('category')
    return df

main()